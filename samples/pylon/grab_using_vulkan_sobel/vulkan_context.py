"""Vulkan helpers shared by the buffer factory, the filters and the display.

Everything Vulkan-specific that does not belong to one particular algorithm is
collected here so the grab loop and the filters stay short:

* VulkanContext: instance, device, queue, memory allocation and command submission.
* VulkanBuffer:  a VkBuffer with its own memory, optionally mapped for CPU access.
* GpuImage:      a Mono8 image stored in a VulkanBuffer.
* ComputeShader: a compute pipeline plus the descriptor sets that bind buffers to it.

Vulkan handles such as VkDevice, VkBuffer or VkCommandBuffer are cffi pointers
created by the Khronos Python "vulkan" package; they are documented by their
Vulkan type name. Memory property flags (VkMemoryPropertyFlags) are plain ints.
"""

import base64
import ctypes
import zlib

import vulkan as vk

HOST_VISIBLE = vk.VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | vk.VK_MEMORY_PROPERTY_HOST_COHERENT_BIT
DEVICE_LOCAL = vk.VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT
BUFFER_USAGE = (vk.VK_BUFFER_USAGE_STORAGE_BUFFER_BIT | vk.VK_BUFFER_USAGE_TRANSFER_SRC_BIT | vk.VK_BUFFER_USAGE_TRANSFER_DST_BIT)
FENCE_TIMEOUT_NANOSECONDS = 5_000_000_000


def decode_spirv(blob):
    """Decode a SPIR-V module embedded as a zlib-compressed base64 string.

    Args:
        blob (str): Base64 text of the zlib-compressed SPIR-V module, e.g.
            SOBEL_SPIRV_BASE64.

    Returns:
        bytes: The SPIR-V bytecode, ready to be passed to ComputeShader.
    """
    return zlib.decompress(base64.b64decode(blob))


class VulkanBuffer:
    """A VkBuffer with its own VkDeviceMemory, optionally permanently mapped."""

    def __init__(self, device, handle, memory, size, mapping=None):
        """Wrap an existing buffer; use VulkanContext.create_buffer() to create one.

        Args:
            device (VkDevice): Device that owns the buffer and its memory.
            handle (VkBuffer): The buffer object.
            memory (VkDeviceMemory): Memory bound to the buffer. The buffer
                owns it and frees it in destroy().
            size (int): Usable size of the buffer in bytes.
            mapping (cffi buffer or None): CPU view of the memory returned by
                vkMapMemory, or None if the memory is not mapped.
        """
        self.device = device
        self.handle = handle
        self.memory = memory
        self.size = size
        self.mapping = mapping

    @property
    def address(self):
        """Address of the mapped memory, as expected by pylon.BufferFactory.

        Only valid for mapped buffers.

        Returns:
            int: Address of the first byte of the mapped memory.
        """
        return int(vk.ffi.cast("uintptr_t", vk.ffi.from_buffer(self.mapping)))

    def destroy(self):
        """Unmap the memory, then destroy the buffer and free its memory.

        The GPU must no longer use the buffer.
        """
        if self.mapping is not None:
            self.mapping = None
            # Release the CPU pointer to the memory.
            vk.vkUnmapMemory(self.device, self.memory)
        # Destroy the buffer object, then free the memory behind it (separate objects in Vulkan).
        vk.vkDestroyBuffer(self.device, self.handle, None)
        vk.vkFreeMemory(self.device, self.memory, None)


class GpuImage:
    """A Mono8 image stored in a VulkanBuffer, with rows packed without padding.

    The shaders process four Mono8 pixels per 32-bit word, so the width must
    be a multiple of 4. The stride (bytes per row) is then equal to the width.
    """

    def __init__(self, buffer, width, height):
        """Describe the image stored in buffer.

        Use VulkanContext.create_image() or create_mapped_image() to create
        an image together with its buffer.

        Args:
            buffer (VulkanBuffer): Buffer holding at least width * height bytes.
                The image owns it and destroys it in destroy().
            width (int): Image width in pixels; must be a multiple of 4.
            height (int): Image height in pixels.

        Raises:
            ValueError: If width is not a multiple of 4.
        """
        if width % 4:
            raise ValueError(f"image width must be a multiple of 4, got {width}")
        self.buffer = buffer
        self.width = width
        self.height = height
        self.stride = width

    def destroy(self):
        """Destroy the buffer of the image. The GPU must no longer use it."""
        self.buffer.destroy()


class VulkanContext:
    """Vulkan instance, device and queue, plus helpers to allocate and run GPU work.

    window_size=None runs headless. Otherwise an SDL window is created first,
    because the Vulkan device must be chosen so that it can present to it.

    Use it as a context manager; all Vulkan objects are destroyed on exit.
    """

    def __init__(self, device_index=None, window_size=None):
        """Create the Vulkan instance, pick a device, and create a queue.

        Args:
            device_index (int or None): Index into vkEnumeratePhysicalDevices,
                or None to prefer a discrete GPU.
            window_size (tuple[int, int] or None): Width and height of the
                window in pixels, or None to run headless. A window requires
                PySDL2 and a device whose compute queue can present to it.

        Raises:
            RuntimeError: If SDL fails, device_index is invalid, or no device
                provides the required queue.
            ImportError: If a window is requested but PySDL2 is not installed.
        """
        self.display_enabled = window_size is not None
        self.window = None
        self.surface = None
        instance_extensions = []
        if self.display_enabled:
            import sdl2
            import sdl2.vulkan as sdl_vulkan

            self.sdl2 = sdl2
            self.sdl_vulkan = sdl_vulkan
            if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
                raise RuntimeError(sdl2.SDL_GetError().decode("utf-8", "replace"))
            if sdl_vulkan.SDL_Vulkan_LoadLibrary(None) != 0:
                raise RuntimeError(sdl2.SDL_GetError().decode("utf-8", "replace"))

            self.window = sdl2.SDL_CreateWindow(
                b"pypylon Vulkan - Original | Processed",
                sdl2.SDL_WINDOWPOS_UNDEFINED,
                sdl2.SDL_WINDOWPOS_UNDEFINED,
                *window_size,
                sdl2.SDL_WINDOW_VULKAN | sdl2.SDL_WINDOW_SHOWN,
            )
            if not self.window:
                raise RuntimeError(sdl2.SDL_GetError().decode("utf-8", "replace"))

            extension_count = ctypes.c_uint()
            if not sdl_vulkan.SDL_Vulkan_GetInstanceExtensions(
                self.window, ctypes.byref(extension_count), None
            ):
                raise RuntimeError(sdl2.SDL_GetError().decode("utf-8", "replace"))
            extension_names = (ctypes.c_char_p * extension_count.value)()
            if not sdl_vulkan.SDL_Vulkan_GetInstanceExtensions(
                self.window, ctypes.byref(extension_count), extension_names
            ):
                raise RuntimeError(sdl2.SDL_GetError().decode("utf-8", "replace"))
            instance_extensions = [
                extension_names[index].decode("ascii")
                for index in range(extension_count.value)
            ]

        application_info = vk.VkApplicationInfo(
            pApplicationName="pypylon vulkan sobel",
            applicationVersion=vk.VK_MAKE_VERSION(1, 0, 0),
            pEngineName="none",
            engineVersion=vk.VK_MAKE_VERSION(1, 0, 0),
            apiVersion=vk.VK_MAKE_VERSION(1, 1, 0),
        )
        # The instance is the connection between this app and the Vulkan loader/driver.
        # Extensions from SDL are required for creating a window surface.
        self.instance = vk.vkCreateInstance(
            vk.VkInstanceCreateInfo(
                pApplicationInfo=application_info,
                ppEnabledLayerNames=[],
                ppEnabledExtensionNames=instance_extensions,
            ),
            None,
        )

        if self.display_enabled:
            surface_value = ctypes.c_uint64()
            instance_address = int(vk.ffi.cast("uintptr_t", self.instance))
            if not self.sdl_vulkan.SDL_Vulkan_CreateSurface(
                self.window,
                ctypes.c_void_p(instance_address),
                ctypes.byref(surface_value),
            ):
                raise RuntimeError(self.sdl2.SDL_GetError().decode("utf-8", "replace"))
            self.surface = vk.ffi.cast("VkSurfaceKHR", surface_value.value)
            self._destroy_surface = vk.vkGetInstanceProcAddr(
                self.instance, "vkDestroySurfaceKHR"
            )
            self._surface_support = vk.vkGetInstanceProcAddr(
                self.instance, "vkGetPhysicalDeviceSurfaceSupportKHR"
            )

        self.physical_device, self.queue_family = self._pick_physical_device(
            device_index
        )
        # Query the GPU name, type and limits.
        properties = vk.vkGetPhysicalDeviceProperties(self.physical_device)
        self.device_name = properties.deviceName
        # Query the memory heaps/types the GPU offers (used to choose where buffers live).
        self.memory_properties = vk.vkGetPhysicalDeviceMemoryProperties(
            self.physical_device
        )

        device_extensions = (
            [vk.VK_KHR_SWAPCHAIN_EXTENSION_NAME] if self.display_enabled else []
        )
        self.device = vk.vkCreateDevice(
            self.physical_device,
            vk.VkDeviceCreateInfo(
                pQueueCreateInfos=[
                    vk.VkDeviceQueueCreateInfo(
                        queueFamilyIndex=self.queue_family, pQueuePriorities=[1.0]
                    )
                ],
                ppEnabledLayerNames=[],
                ppEnabledExtensionNames=device_extensions,
            ),
            None,
        )
        # Fetch the queue that command buffers are submitted to.
        self.queue = vk.vkGetDeviceQueue(self.device, self.queue_family, 0)

        # Command buffers are allocated from a pool; RESET_COMMAND_BUFFER lets them be re-recorded individually.
        self.command_pool = vk.vkCreateCommandPool(
            self.device,
            vk.VkCommandPoolCreateInfo(
                queueFamilyIndex=self.queue_family,
                flags=vk.VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT,
            ),
            None,
        )
        # Fence the CPU waits on until submitted work has finished (see run()).
        self.fence = vk.vkCreateFence(self.device, vk.VkFenceCreateInfo(flags=0), None)

        print(f"Vulkan device: {self.device_name}")

    def __enter__(self):
        """Enter the with block.

        Returns:
            VulkanContext: This context.
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy all Vulkan objects when leaving the with block.

        Exceptions raised in the with block are not suppressed.

        Args:
            exception_type (type or None): Type of the exception raised in the
                with block, or None.
            exception_value (BaseException or None): The exception, or None.
            traceback (types.TracebackType or None): Its traceback, or None.
        """
        self.destroy()

    # -- setup ------------------------------------------------------------

    def _pick_physical_device(self, device_index):
        """Choose a GPU and a queue family that supports compute (and presentation).

        Args:
            device_index (int or None): Index into vkEnumeratePhysicalDevices,
                or None to try all devices, discrete GPUs first.

        Returns:
            tuple[VkPhysicalDevice, int]: The device and the index of its queue
            family to use.

        Raises:
            RuntimeError: If there is no Vulkan device, device_index is
                invalid, or no device has a suitable queue family.
        """
        # List all GPUs the driver exposes.
        devices = vk.vkEnumeratePhysicalDevices(self.instance)
        if not devices:
            raise RuntimeError("no Vulkan device found")
        if device_index is not None:
            if device_index < 0 or device_index >= len(devices):
                raise RuntimeError(f"invalid Vulkan device index: {device_index}")
            candidates = [devices[device_index]]
        else:
            ranking = {
                vk.VK_PHYSICAL_DEVICE_TYPE_DISCRETE_GPU: 0,
                vk.VK_PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU: 1,
                vk.VK_PHYSICAL_DEVICE_TYPE_VIRTUAL_GPU: 2,
                vk.VK_PHYSICAL_DEVICE_TYPE_CPU: 3,
            }
            # Prefer discrete GPUs; vkGetPhysicalDeviceProperties reports the device type.
            candidates = sorted(
                devices,
                key=lambda device: ranking.get(
                    vk.vkGetPhysicalDeviceProperties(device).deviceType, 4
                ),
            )

        for device in candidates:
            if self.display_enabled:
                extensions = {
                    extension.extensionName
                    for extension in vk.vkEnumerateDeviceExtensionProperties(
                        device, None
                    )
                }
                if vk.VK_KHR_SWAPCHAIN_EXTENSION_NAME not in extensions:
                    continue
            # Queue families group queues by capability (compute, graphics, transfer...).
            families = vk.vkGetPhysicalDeviceQueueFamilyProperties(device)
            for index, family in enumerate(families):
                if not family.queueFlags & vk.VK_QUEUE_COMPUTE_BIT:
                    continue
                if not self.display_enabled or self._surface_support(
                    device, index, self.surface
                ):
                    return device, index

        if device_index is not None:
            requirement = "compute and present" if self.display_enabled else "compute"
            raise RuntimeError(
                f"Vulkan device {device_index} has no {requirement} queue"
            )
        requirement = "compute queue that can present" if self.display_enabled else "compute queue"
        raise RuntimeError(f"no Vulkan device has a {requirement}")

    # -- images and buffers -----------------------------------------------

    def _find_memory_type(self, type_bits, required, preferred=0):
        """Find a memory type with the required and, if possible, preferred properties.

        Args:
            type_bits (int): Bit mask of the memory types allowed for the
                resource (VkMemoryRequirements.memoryTypeBits).
            required (int): VkMemoryPropertyFlags the memory type must have.
            preferred (int): VkMemoryPropertyFlags the memory type should have
                in addition; ignored if no such type exists.

        Returns:
            int: Index of the memory type.

        Raises:
            RuntimeError: If no allowed memory type has the required properties.
        """
        properties = self.memory_properties
        for wanted in (required | preferred, required):
            for index in range(properties.memoryTypeCount):
                if not type_bits & (1 << index):
                    continue
                flags = properties.memoryTypes[index].propertyFlags
                if flags & wanted == wanted:
                    return index
        raise RuntimeError("no suitable Vulkan memory type")

    def create_buffer(self, size, required, preferred=0, mapped=False):
        """Create a storage buffer with its own memory.

        Args:
            size (int): Size of the buffer in bytes.
            required (int): VkMemoryPropertyFlags the memory must have, e.g.
                DEVICE_LOCAL or HOST_VISIBLE.
            preferred (int): VkMemoryPropertyFlags the memory should have in
                addition, if the GPU offers such memory.
            mapped (bool): Map the memory into the address space of the
                application. Requires HOST_VISIBLE in required.

        Returns:
            VulkanBuffer: The new buffer.

        Raises:
            RuntimeError: If the GPU has no memory with the required properties.
        """
        # Create the buffer object (just a handle; it has no memory yet).
        handle = vk.vkCreateBuffer(
            self.device,
            vk.VkBufferCreateInfo(
                size=size,
                usage=BUFFER_USAGE,
                sharingMode=vk.VK_SHARING_MODE_EXCLUSIVE,
            ),
            None,
        )
        # Ask the driver for the size, alignment and allowed memory types.
        requirements = vk.vkGetBufferMemoryRequirements(self.device, handle)
        # Allocate device memory of a suitable type.
        memory = vk.vkAllocateMemory(
            self.device,
            vk.VkMemoryAllocateInfo(
                allocationSize=requirements.size,
                memoryTypeIndex=self._find_memory_type(
                    requirements.memoryTypeBits, required, preferred
                ),
            ),
            None,
        )
        # Attach the memory to the buffer (offset 0).
        vk.vkBindBufferMemory(self.device, handle, memory, 0)

        pointer = None
        if mapped:
            # Map the memory so the CPU (and pylon) can write to it directly.
            pointer = vk.vkMapMemory(self.device, memory, 0, requirements.size, 0)

        return VulkanBuffer(self.device, handle, memory, size, pointer)

    def create_image(self, width, height):
        """Create an image in GPU-local memory, e.g. for the output of a filter.

        Args:
            width (int): Image width in pixels; must be a multiple of 4.
            height (int): Image height in pixels.

        Returns:
            GpuImage: The new image. Its content is undefined until written.

        Raises:
            ValueError: If width is not a multiple of 4.
        """
        buffer = self.create_buffer(width * height, required=DEVICE_LOCAL)
        return GpuImage(buffer, width, height)

    def create_mapped_image(self, width, height, size, prefer_device_local=True):
        """Create an image the CPU can write to, e.g. as a pylon grab buffer.

        Args:
            width (int): Image width in pixels; must be a multiple of 4.
            height (int): Image height in pixels.
            size (int): Size of the buffer in bytes, at least width * height.
                It is rounded up to a multiple of 4.
            prefer_device_local (bool): Place the memory on the GPU if the
                driver offers GPU-local memory that is also visible to the CPU.
                If False, the memory is in host memory.

        Returns:
            GpuImage: The new image. image.buffer.address is the CPU address
            of its memory.

        Raises:
            ValueError: If width is not a multiple of 4.
        """
        buffer = self.create_buffer(
            (size + 3) & ~3,
            required=HOST_VISIBLE,
            preferred=DEVICE_LOCAL if prefer_device_local else 0,
            mapped=True,
        )
        return GpuImage(buffer, width, height)

    # -- commands ---------------------------------------------------------

    def allocate_command_buffer(self):
        """Allocate an empty command buffer from the command pool of the context.

        Returns:
            VkCommandBuffer: The command buffer. Release it with
            free_command_buffer().
        """
        return vk.vkAllocateCommandBuffers(
            self.device,
            vk.VkCommandBufferAllocateInfo(
                commandPool=self.command_pool,
                level=vk.VK_COMMAND_BUFFER_LEVEL_PRIMARY,
                commandBufferCount=1,
            ),
        )[0]

    def free_command_buffer(self, command_buffer):
        """Return a command buffer to the command pool.

        Args:
            command_buffer (VkCommandBuffer): Command buffer allocated by this
                context. The GPU must no longer execute it.
        """
        vk.vkFreeCommandBuffers(self.device, self.command_pool, 1, [command_buffer])

    def record_commands(self, record):
        """Allocate a command buffer and let record fill it with commands.

        Args:
            record (Callable[[VkCommandBuffer], None]): Function that records
                commands into the command buffer passed to it, e.g. via
                ComputeShader.dispatch().

        Returns:
            VkCommandBuffer: The recorded command buffer. It can be submitted
            with run() any number of times.
        """
        command_buffer = self.allocate_command_buffer()
        vk.vkBeginCommandBuffer(command_buffer, vk.VkCommandBufferBeginInfo(flags=0))
        record(command_buffer)
        vk.vkEndCommandBuffer(command_buffer)
        return command_buffer

    def run(self, command_buffer):
        """Submit a recorded command buffer and wait until the GPU has finished it.

        Args:
            command_buffer (VkCommandBuffer): Command buffer recorded with
                record_commands().

        Raises:
            vk.VkTimeout: If the GPU does not finish within 5 seconds.
        """
        # Set the fence to unsignaled before reuse.
        vk.vkResetFences(self.device, 1, [self.fence])
        # The fence is signaled when the GPU has executed the command buffer.
        vk.vkQueueSubmit(
            self.queue,
            1,
            [vk.VkSubmitInfo(pCommandBuffers=[command_buffer])],
            self.fence,
        )
        vk.vkWaitForFences(
            self.device, 1, [self.fence], vk.VK_TRUE, FENCE_TIMEOUT_NANOSECONDS
        )

    def wait_idle(self):
        """Block until the GPU has finished all submitted work."""
        vk.vkDeviceWaitIdle(self.device)

    def destroy(self):
        """Wait for the GPU, then destroy the device, instance, and window.

        All buffers, images, shaders, and command buffers created with this
        context must be destroyed before.
        """
        # Block until the GPU is idle so nothing is destroyed while in use.
        vk.vkDeviceWaitIdle(self.device)
        # Destroy in reverse order of creation: device-level objects, device, surface, instance.
        vk.vkDestroyFence(self.device, self.fence, None)
        vk.vkDestroyCommandPool(self.device, self.command_pool, None)
        vk.vkDestroyDevice(self.device, None)
        if self.surface is not None:
            self._destroy_surface(self.instance, self.surface, None)
        vk.vkDestroyInstance(self.instance, None)
        if self.display_enabled:
            self.sdl2.SDL_DestroyWindow(self.window)
            self.sdl_vulkan.SDL_Vulkan_UnloadLibrary()
            self.sdl2.SDL_Quit()


class ComputeShader:
    """A compute shader that reads and writes storage buffers.

    Bundles the Vulkan objects one shader needs (pipeline, layouts and
    descriptor sets). An algorithm only calls bind_buffers() once per buffer
    combination and dispatch() while recording its commands.

    The shader must declare buffer_count storage buffers at bindings 0, 1, ...
    of descriptor set 0 and, optionally, push_constant_count 32-bit push constants.
    """

    DESCRIPTOR_SETS_PER_POOL = 16

    def __init__(self, gpu, spirv, buffer_count, push_constant_count=0):
        """Create the compute pipeline for a SPIR-V module.

        Args:
            gpu (VulkanContext): Context that provides the device.
            spirv (bytes): SPIR-V bytecode with a compute entry point "main",
                e.g. from decode_spirv().
            buffer_count (int): Number of storage buffers the shader declares.
            push_constant_count (int): Number of 32-bit push constants the
                shader declares; 0 if it uses none.
        """
        self.gpu = gpu
        self.buffer_count = buffer_count
        self.push_constant_size = 4 * push_constant_count
        device = gpu.device

        bindings = [
            vk.VkDescriptorSetLayoutBinding(
                binding=slot,
                descriptorType=vk.VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
                descriptorCount=1,
                stageFlags=vk.VK_SHADER_STAGE_COMPUTE_BIT,
            )
            for slot in range(buffer_count)
        ]
        # Descriptor set layout: declares which resources the shader expects (here storage buffers).
        self.set_layout = vk.vkCreateDescriptorSetLayout(
            device, vk.VkDescriptorSetLayoutCreateInfo(pBindings=bindings), None
        )
        push_constant_ranges = []
        if self.push_constant_size:
            push_constant_ranges.append(
                vk.VkPushConstantRange(
                    stageFlags=vk.VK_SHADER_STAGE_COMPUTE_BIT,
                    offset=0,
                    size=self.push_constant_size,
                )
            )
        # Pipeline layout: the full shader interface = descriptor set layouts + push constant range.
        self.pipeline_layout = vk.vkCreatePipelineLayout(
            device,
            vk.VkPipelineLayoutCreateInfo(
                pSetLayouts=[self.set_layout],
                pPushConstantRanges=push_constant_ranges,
            ),
            None,
        )

        # Wrap the SPIR-V bytecode in a shader module object.
        module = vk.vkCreateShaderModule(
            device, vk.VkShaderModuleCreateInfo(codeSize=len(spirv), pCode=spirv), None
        )
        # The nested structs must stay referenced until the call returns, so
        # they are bound to locals instead of being built inline.
        stage = vk.VkPipelineShaderStageCreateInfo(
            stage=vk.VK_SHADER_STAGE_COMPUTE_BIT, module=module, pName="main"
        )
        create_info = vk.VkComputePipelineCreateInfo(
            stage=stage, layout=self.pipeline_layout
        )
        # Compile the shader into a pipeline (VK_NULL_HANDLE = no pipeline cache).
        self.pipeline = vk.vkCreateComputePipelines(
            device, vk.VK_NULL_HANDLE, 1, [create_info], None
        )[0]
        # The module is no longer needed once the pipeline exists.
        vk.vkDestroyShaderModule(device, module, None)

        # Descriptor sets are allocated from pools; a new pool is added when the current one is full.
        self.descriptor_pools = []
        self.free_sets_in_pool = 0

    def bind_buffers(self, buffers):
        """Create a descriptor set that binds buffers[i] to binding slot i.

        Descriptor sets live until the shader is destroyed, so create them once
        and reuse them, e.g. while recording a command buffer.

        Args:
            buffers (list[VulkanBuffer]): One buffer per binding slot of the
                shader, in slot order.

        Returns:
            VkDescriptorSet: The descriptor set to pass to dispatch().

        Raises:
            ValueError: If the number of buffers does not match buffer_count.
        """
        if len(buffers) != self.buffer_count:
            raise ValueError(
                f"shader expects {self.buffer_count} buffers, got {len(buffers)}"
            )
        device = self.gpu.device
        if self.free_sets_in_pool == 0:
            self.descriptor_pools.append(
                vk.vkCreateDescriptorPool(
                    device,
                    vk.VkDescriptorPoolCreateInfo(
                        maxSets=self.DESCRIPTOR_SETS_PER_POOL,
                        pPoolSizes=[
                            vk.VkDescriptorPoolSize(
                                type=vk.VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
                                descriptorCount=self.DESCRIPTOR_SETS_PER_POOL
                                * self.buffer_count,
                            )
                        ],
                    ),
                    None,
                )
            )
            self.free_sets_in_pool = self.DESCRIPTOR_SETS_PER_POOL
        descriptor_set = vk.vkAllocateDescriptorSets(
            device,
            vk.VkDescriptorSetAllocateInfo(
                descriptorPool=self.descriptor_pools[-1], pSetLayouts=[self.set_layout]
            ),
        )[0]
        self.free_sets_in_pool -= 1

        buffer_infos = [
            vk.VkDescriptorBufferInfo(buffer=buffer.handle, offset=0, range=buffer.size)
            for buffer in buffers
        ]
        writes = [
            vk.VkWriteDescriptorSet(
                dstSet=descriptor_set,
                dstBinding=slot,
                descriptorCount=1,
                descriptorType=vk.VK_DESCRIPTOR_TYPE_STORAGE_BUFFER,
                pBufferInfo=[buffer_info],
            )
            for slot, buffer_info in enumerate(buffer_infos)
        ]
        # Point each binding of the set at its actual buffer.
        vk.vkUpdateDescriptorSets(device, len(writes), writes, 0, None)
        return descriptor_set

    def dispatch(
        self,
        command_buffer,
        descriptor_set,
        push_constants,
        group_count_x,
        group_count_y,
    ):
        """Record a dispatch of group_count_x * group_count_y workgroups.

        A barrier is recorded first, so the shader sees everything that
        previously submitted work (e.g. the preceding filter) has written.

        Args:
            command_buffer (VkCommandBuffer): Command buffer in the recording
                state, e.g. the one passed to ImageFilter.record().
            descriptor_set (VkDescriptorSet): Buffers to bind, created with
                bind_buffers() of this shader.
            push_constants (list[int]): Values of the push constants as
                unsigned 32-bit integers, one per declared push constant.
                Ignored if the shader has no push constants.
            group_count_x (int): Number of workgroups in x direction.
            group_count_y (int): Number of workgroups in y direction.
        """
        vk.vkCmdPipelineBarrier(
            command_buffer,
            vk.VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
            vk.VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
            0,
            1,
            [
                vk.VkMemoryBarrier(
                    srcAccessMask=vk.VK_ACCESS_SHADER_WRITE_BIT,
                    dstAccessMask=vk.VK_ACCESS_SHADER_READ_BIT,
                )
            ],
            0,
            None,
            0,
            None,
        )
        # Select the compute pipeline (shader) to run.
        vk.vkCmdBindPipeline(
            command_buffer, vk.VK_PIPELINE_BIND_POINT_COMPUTE, self.pipeline
        )
        # Bind the buffers.
        vk.vkCmdBindDescriptorSets(
            command_buffer,
            vk.VK_PIPELINE_BIND_POINT_COMPUTE,
            self.pipeline_layout,
            0,
            1,
            [descriptor_set],
            0,
            None,
        )
        if self.push_constant_size:
            # Push constants: small values (sizes) sent to the shader without a buffer.
            values = vk.ffi.new(f"uint32_t[{len(push_constants)}]", push_constants)
            vk.vkCmdPushConstants(
                command_buffer,
                self.pipeline_layout,
                vk.VK_SHADER_STAGE_COMPUTE_BIT,
                0,
                self.push_constant_size,
                values,
            )
        vk.vkCmdDispatch(command_buffer, group_count_x, group_count_y, 1)

    def destroy(self):
        """Destroy the pipeline and all descriptor sets created by bind_buffers().

        The GPU must no longer execute commands that use the shader.
        """
        device = self.gpu.device
        # Destroying a pool also frees all descriptor sets allocated from it.
        for pool in self.descriptor_pools:
            vk.vkDestroyDescriptorPool(device, pool, None)
        self.descriptor_pools.clear()
        vk.vkDestroyPipeline(device, self.pipeline, None)
        vk.vkDestroyPipelineLayout(device, self.pipeline_layout, None)
        vk.vkDestroyDescriptorSetLayout(device, self.set_layout, None)
