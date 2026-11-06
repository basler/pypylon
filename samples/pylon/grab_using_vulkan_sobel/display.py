"""Window that shows the original and the processed image side by side.

A compute shader composes both Mono8 images into an RGBA canvas in GPU memory,
which is then copied into the swapchain image of the window. The images never
leave the GPU. The SPIR-V module is embedded as a zlib/base64 blob.
"""

import ctypes

import vulkan as vk

from vulkan_context import DEVICE_LOCAL, ComputeShader, decode_spirv

MAXIMUM_WINDOW_WIDTH = 1920
MAXIMUM_WINDOW_HEIGHT = 1080


DISPLAY_SPIRV_BASE64 = (
    "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"
)


class ImageDisplay:
    """Shows two images of the same size side by side in the window of the VulkanContext.

    If the VulkanContext has no window (headless mode), show() does nothing
    and is_open() always returns True.

    Use it as a context manager; the swapchain and shader are destroyed on exit.
    """

    @staticmethod
    def window_size_for(width, height):
        """Compute the window size for two images side by side.

        The window is scaled down, keeping the aspect ratio, to fit into
        MAXIMUM_WINDOW_WIDTH x MAXIMUM_WINDOW_HEIGHT; it is never scaled up.

        Args:
            width (int): Width of one image in pixels.
            height (int): Height of one image in pixels.

        Returns:
            tuple[int, int]: Window width and height in pixels, to be passed to
            VulkanContext as window_size.
        """
        scale = min(
            1.0, MAXIMUM_WINDOW_WIDTH / (2 * width), MAXIMUM_WINDOW_HEIGHT / height
        )
        return round(2 * width * scale), round(height * scale)

    def __init__(self, gpu):
        """Create the swapchain, canvas, and composition shader for the window of gpu.

        Does nothing if gpu has no window.

        Args:
            gpu (VulkanContext): Context created with a window_size, or
                without one for headless mode.

        Raises:
            RuntimeError: If the window surface does not support copying
                images into it.
        """
        self.gpu = gpu
        self.enabled = gpu.window is not None
        if not self.enabled:
            return
        # Swapchain/surface functions are extensions and are looked up by name.
        self.get_surface_capabilities = vk.vkGetInstanceProcAddr(
            gpu.instance, "vkGetPhysicalDeviceSurfaceCapabilitiesKHR"
        )
        self.get_surface_formats = vk.vkGetInstanceProcAddr(
            gpu.instance, "vkGetPhysicalDeviceSurfaceFormatsKHR"
        )
        self.get_present_modes = vk.vkGetInstanceProcAddr(
            gpu.instance, "vkGetPhysicalDeviceSurfacePresentModesKHR"
        )
        self.create_swapchain = vk.vkGetDeviceProcAddr(
            gpu.device, "vkCreateSwapchainKHR"
        )
        self.get_swapchain_images = vk.vkGetDeviceProcAddr(
            gpu.device, "vkGetSwapchainImagesKHR"
        )
        self.acquire_next_image = vk.vkGetDeviceProcAddr(
            gpu.device, "vkAcquireNextImageKHR"
        )
        self.queue_present = vk.vkGetDeviceProcAddr(gpu.device, "vkQueuePresentKHR")
        self.destroy_swapchain = vk.vkGetDeviceProcAddr(
            gpu.device, "vkDestroySwapchainKHR"
        )

        # Image count, size limits and usage flags the window surface supports.
        surface_capabilities = self.get_surface_capabilities(
            gpu.physical_device, gpu.surface
        )
        if not (
            surface_capabilities.supportedUsageFlags
            & vk.VK_IMAGE_USAGE_TRANSFER_DST_BIT
        ):
            raise RuntimeError("surface does not support transfer-destination images")

        # Pixel formats / color spaces the surface can display.
        formats = self.get_surface_formats(gpu.physical_device, gpu.surface)
        preferred_formats = (
            vk.VK_FORMAT_B8G8R8A8_UNORM,
            vk.VK_FORMAT_R8G8B8A8_UNORM,
        )
        self.surface_format = next(
            (
                candidate_format
                for wanted in preferred_formats
                for candidate_format in formats
                if candidate_format.format == wanted
            ),
            formats[0],
        )

        drawable_width = ctypes.c_int()
        drawable_height = ctypes.c_int()
        gpu.sdl_vulkan.SDL_Vulkan_GetDrawableSize(
            gpu.window, ctypes.byref(drawable_width), ctypes.byref(drawable_height)
        )
        if surface_capabilities.currentExtent.width != 0xFFFFFFFF:
            width = surface_capabilities.currentExtent.width
            height = surface_capabilities.currentExtent.height
        else:
            width = min(
                max(drawable_width.value, surface_capabilities.minImageExtent.width),
                surface_capabilities.maxImageExtent.width,
            )
            height = min(
                max(drawable_height.value, surface_capabilities.minImageExtent.height),
                surface_capabilities.maxImageExtent.height,
            )
        self.width = width
        self.height = height

        # Available presentation modes (MAILBOX = low-latency, FIFO = vsync, always available).
        present_modes = self.get_present_modes(gpu.physical_device, gpu.surface)
        if vk.VK_PRESENT_MODE_MAILBOX_KHR in present_modes:
            present_mode = vk.VK_PRESENT_MODE_MAILBOX_KHR
        else:
            present_mode = vk.VK_PRESENT_MODE_FIFO_KHR

        image_count = surface_capabilities.minImageCount + 1
        if surface_capabilities.maxImageCount:
            image_count = min(image_count, surface_capabilities.maxImageCount)
        if (
            surface_capabilities.supportedCompositeAlpha
            & vk.VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR
        ):
            composite_alpha = vk.VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR
        else:
            composite_alpha = next(
                flag
                for flag in (
                    vk.VK_COMPOSITE_ALPHA_PRE_MULTIPLIED_BIT_KHR,
                    vk.VK_COMPOSITE_ALPHA_POST_MULTIPLIED_BIT_KHR,
                    vk.VK_COMPOSITE_ALPHA_INHERIT_BIT_KHR,
                )
                if surface_capabilities.supportedCompositeAlpha & flag
            )

        # The swapchain is a queue of images that get shown in the window.
        # TRANSFER_DST usage lets us copy our canvas buffer into them.
        self.swapchain = self.create_swapchain(
            gpu.device,
            vk.VkSwapchainCreateInfoKHR(
                surface=gpu.surface,
                minImageCount=image_count,
                imageFormat=self.surface_format.format,
                imageColorSpace=self.surface_format.colorSpace,
                imageExtent=vk.VkExtent2D(width=width, height=height),
                imageArrayLayers=1,
                imageUsage=vk.VK_IMAGE_USAGE_TRANSFER_DST_BIT,
                imageSharingMode=vk.VK_SHARING_MODE_EXCLUSIVE,
                preTransform=surface_capabilities.currentTransform,
                compositeAlpha=composite_alpha,
                presentMode=present_mode,
                clipped=vk.VK_TRUE,
                oldSwapchain=vk.VK_NULL_HANDLE,
            ),
            None,
        )
        # Retrieve the images the swapchain created.
        self.images = self.get_swapchain_images(gpu.device, self.swapchain)
        # Semaphores synchronize GPU work: this one signals that an acquired image is ready.
        self.image_available = vk.vkCreateSemaphore(
            gpu.device, vk.VkSemaphoreCreateInfo(flags=0), None
        )
        # One semaphore per swapchain image: signals that drawing to it finished, so it may be presented.
        self.render_finished = [
            vk.vkCreateSemaphore(
                gpu.device, vk.VkSemaphoreCreateInfo(flags=0), None
            )
            for _ in self.images
        ]
        # A fence lets the CPU wait for the GPU; created signaled so the first wait returns at once.
        self.fence = vk.vkCreateFence(
            gpu.device,
            vk.VkFenceCreateInfo(flags=vk.VK_FENCE_CREATE_SIGNALED_BIT),
            None,
        )
        # Command buffer that records the display work (re-recorded every frame).
        self.command_buffer = gpu.allocate_command_buffer()
        self.canvas = gpu.create_buffer(
            width * height * 4, required=DEVICE_LOCAL, preferred=0, mapped=False
        )

        # Shader interface: binding 0 = original image, binding 1 = processed image,
        # binding 2 = canvas; push constants = image width, height, stride and canvas width, height.
        self.shader = ComputeShader(
            gpu,
            decode_spirv(DISPLAY_SPIRV_BASE64),
            buffer_count=3,
            push_constant_count=5,
        )
        # Descriptor sets per (original, processed) image pair; pylon reuses its
        # grab buffers, so only a few sets are ever created.
        self.bound_images = {}

    def bind_images(self, original_image, processed_image):
        """Get the descriptor set that binds both images and the canvas to the shader.

        The descriptor set is created on first use of an image pair and reused
        afterwards.

        Args:
            original_image (GpuImage): Image shown on the left.
            processed_image (GpuImage): Image shown on the right.

        Returns:
            VkDescriptorSet: Descriptor set for the composition shader.
        """
        key = (original_image, processed_image)
        if key not in self.bound_images:
            self.bound_images[key] = self.shader.bind_buffers(
                [original_image.buffer, processed_image.buffer, self.canvas]
            )
        return self.bound_images[key]

    def is_open(self):
        """Handle pending window events and report whether to keep running.

        Returns:
            bool: False once the window was closed or Esc was pressed;
            always True in headless mode.
        """
        if not self.enabled:
            return True
        sdl2 = self.gpu.sdl2
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == sdl2.SDL_QUIT:
                return False
            if (
                event.type == sdl2.SDL_KEYDOWN
                and event.key.keysym.sym == sdl2.SDLK_ESCAPE
            ):
                return False
        return True

    def show(self, original_image, processed_image):
        """Show original_image (left) and processed_image (right) and wait until shown.

        Does nothing in headless mode.

        Args:
            original_image (GpuImage): Mono8 image, e.g. the grab buffer.
            processed_image (GpuImage): Mono8 image of the same size, e.g. the
                output of the last filter.

        Raises:
            vk.VkException: If presenting fails, e.g. vk.VkErrorOutOfDateKhr
                when the window surface has changed.
        """
        if not self.enabled:
            return
        gpu = self.gpu
        display_set = self.bind_images(original_image, processed_image)
        # Wait until the previous frame's GPU work is done before reusing the command buffer.
        vk.vkWaitForFences(
            gpu.device, 1, [self.fence], vk.VK_TRUE, 0xFFFFFFFFFFFFFFFF
        )
        # Get the index of the next swapchain image to draw into; image_available is signaled when it is usable.
        image_index = self.acquire_next_image(
            gpu.device,
            self.swapchain,
            0xFFFFFFFFFFFFFFFF,
            self.image_available,
            vk.VK_NULL_HANDLE,
        )
        # Set the fence back to unsignaled; the submit below will signal it again.
        vk.vkResetFences(gpu.device, 1, [self.fence])
        # Discard the old recording and start a new one.
        vk.vkResetCommandBuffer(self.command_buffer, 0)
        vk.vkBeginCommandBuffer(
            self.command_buffer,
            vk.VkCommandBufferBeginInfo(
                flags=vk.VK_COMMAND_BUFFER_USAGE_ONE_TIME_SUBMIT_BIT
            ),
        )

        # Compose both images into the canvas; one 16x16 workgroup per tile of the canvas.
        self.shader.dispatch(
            self.command_buffer,
            display_set,
            push_constants=[
                original_image.width,
                original_image.height,
                original_image.stride,
                self.width,
                self.height,
            ],
            group_count_x=(self.width + 15) // 16,
            group_count_y=(self.height + 15) // 16,
        )

        # Barrier: the canvas must be fully written before the copy reads it.
        vk.vkCmdPipelineBarrier(
            self.command_buffer,
            vk.VK_PIPELINE_STAGE_COMPUTE_SHADER_BIT,
            vk.VK_PIPELINE_STAGE_TRANSFER_BIT,
            0,
            1,
            [
                vk.VkMemoryBarrier(
                    srcAccessMask=vk.VK_ACCESS_SHADER_WRITE_BIT,
                    dstAccessMask=vk.VK_ACCESS_TRANSFER_READ_BIT,
                )
            ],
            0,
            None,
            0,
            None,
        )
        image = self.images[image_index]
        # Image barrier: change the layout from UNDEFINED to TRANSFER_DST so it can be copied into.
        vk.vkCmdPipelineBarrier(
            self.command_buffer,
            vk.VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
            vk.VK_PIPELINE_STAGE_TRANSFER_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [
                vk.VkImageMemoryBarrier(
                    srcAccessMask=0,
                    dstAccessMask=vk.VK_ACCESS_TRANSFER_WRITE_BIT,
                    oldLayout=vk.VK_IMAGE_LAYOUT_UNDEFINED,
                    newLayout=vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                    srcQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                    dstQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                    image=image,
                    subresourceRange=vk.VkImageSubresourceRange(
                        aspectMask=vk.VK_IMAGE_ASPECT_COLOR_BIT,
                        baseMipLevel=0,
                        levelCount=1,
                        baseArrayLayer=0,
                        layerCount=1,
                    ),
                )
            ],
        )
        # Copy the canvas buffer into the swapchain image.
        vk.vkCmdCopyBufferToImage(
            self.command_buffer,
            self.canvas.handle,
            image,
            vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            1,
            [
                vk.VkBufferImageCopy(
                    bufferOffset=0,
                    bufferRowLength=0,
                    bufferImageHeight=0,
                    imageSubresource=vk.VkImageSubresourceLayers(
                        aspectMask=vk.VK_IMAGE_ASPECT_COLOR_BIT,
                        mipLevel=0,
                        baseArrayLayer=0,
                        layerCount=1,
                    ),
                    imageOffset=vk.VkOffset3D(x=0, y=0, z=0),
                    imageExtent=vk.VkExtent3D(
                        width=self.width, height=self.height, depth=1
                    ),
                )
            ],
        )
        # Image barrier: switch the layout to PRESENT_SRC so the image can be shown.
        vk.vkCmdPipelineBarrier(
            self.command_buffer,
            vk.VK_PIPELINE_STAGE_TRANSFER_BIT,
            vk.VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [
                vk.VkImageMemoryBarrier(
                    srcAccessMask=vk.VK_ACCESS_TRANSFER_WRITE_BIT,
                    dstAccessMask=0,
                    oldLayout=vk.VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                    newLayout=vk.VK_IMAGE_LAYOUT_PRESENT_SRC_KHR,
                    srcQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                    dstQueueFamilyIndex=vk.VK_QUEUE_FAMILY_IGNORED,
                    image=image,
                    subresourceRange=vk.VkImageSubresourceRange(
                        aspectMask=vk.VK_IMAGE_ASPECT_COLOR_BIT,
                        baseMipLevel=0,
                        levelCount=1,
                        baseArrayLayer=0,
                        layerCount=1,
                    ),
                )
            ],
        )
        # Finish recording.
        vk.vkEndCommandBuffer(self.command_buffer)

        # Submit to the GPU: wait for the image, run the commands, signal render_finished and the fence.
        vk.vkQueueSubmit(
            gpu.queue,
            1,
            [
                vk.VkSubmitInfo(
                    pWaitSemaphores=[self.image_available],
                    pWaitDstStageMask=[vk.VK_PIPELINE_STAGE_TRANSFER_BIT],
                    pCommandBuffers=[self.command_buffer],
                    pSignalSemaphores=[self.render_finished[image_index]],
                )
            ],
            self.fence,
        )
        # Show the image in the window once rendering has finished.
        self.queue_present(
            gpu.queue,
            vk.VkPresentInfoKHR(
                pWaitSemaphores=[self.render_finished[image_index]],
                pSwapchains=[self.swapchain],
                pImageIndices=[image_index],
            ),
        )
        # Wait for the GPU so timing covers the full frame.
        vk.vkWaitForFences(
            gpu.device, 1, [self.fence], vk.VK_TRUE, 0xFFFFFFFFFFFFFFFF
        )

    def __enter__(self):
        """Enter the with block.

        Returns:
            ImageDisplay: This display.
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Destroy the display resources when leaving the with block.

        Exceptions raised in the with block are not suppressed.

        Args:
            exception_type (type or None): Type of the exception raised in the
                with block, or None.
            exception_value (BaseException or None): The exception, or None.
            traceback (types.TracebackType or None): Its traceback, or None.
        """
        self.destroy()

    def destroy(self):
        """Wait for the GPU, then destroy the swapchain, canvas, and shader.

        The window itself belongs to the VulkanContext. Does nothing in
        headless mode.
        """
        if not self.enabled:
            return
        gpu = self.gpu
        # Make sure the GPU is idle, then destroy objects in reverse creation order.
        vk.vkDeviceWaitIdle(gpu.device)
        self.shader.destroy()
        self.canvas.destroy()
        vk.vkDestroyFence(gpu.device, self.fence, None)
        for semaphore in self.render_finished:
            vk.vkDestroySemaphore(gpu.device, semaphore, None)
        vk.vkDestroySemaphore(gpu.device, self.image_available, None)
        gpu.free_command_buffer(self.command_buffer)
        self.destroy_swapchain(gpu.device, self.swapchain, None)
