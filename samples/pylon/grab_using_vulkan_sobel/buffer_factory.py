"""pylon buffer factory that lets the camera grab directly into Vulkan memory."""

from pypylon import pylon


class VulkanBufferFactory(pylon.BufferFactory):
    """Allocates the pylon grab buffers in Vulkan memory (zero copy).

    The memory is mapped into the address space of the application, so pylon
    can write the images into it, and the GPU reads them in place. Each grab
    buffer is wrapped in a GpuImage, which pylon hands back as
    grab_result.BufferContext.
    """

    def __init__(self, gpu, width, height, prefer_device_local=True):
        """Configure the factory; buffers are allocated later by pylon.

        Args:
            gpu (VulkanContext): Context used to allocate the Vulkan memory.
            width (int): Image width in pixels (camera.Width.Value); must be a
                multiple of 4.
            height (int): Image height in pixels (camera.Height.Value).
            prefer_device_local (bool): Place the grab buffers in GPU memory
                that is visible to the CPU, if available. If False, they are
                placed in host memory.
        """
        super().__init__()
        self.gpu = gpu
        self.width = width
        self.height = height
        self.prefer_device_local = prefer_device_local

    def AllocateBuffer(self, buffer_size):
        """Allocate one grab buffer in mapped Vulkan memory.

        pylon calls this for each grab buffer when grabbing starts, possibly
        from an internal pylon thread.

        Args:
            buffer_size (int): Size of the buffer pylon needs, in bytes.

        Returns:
            tuple[int, GpuImage]: The address pylon writes the image to, and
            the GpuImage wrapping the buffer. pylon hands the GpuImage back as
            grab_result.BufferContext and passes it to FreeBuffer().
        """
        image = self.gpu.create_mapped_image(
            self.width, self.height, buffer_size, self.prefer_device_local
        )
        return image.buffer.address, image

    def FreeBuffer(self, buffer, context):
        """Free one grab buffer.

        pylon calls this for each grab buffer when grabbing stops. Exceptions
        raised here are logged and ignored by pylon.

        Args:
            buffer (int): Address returned by AllocateBuffer().
            context (GpuImage): Image returned by AllocateBuffer().
        """
        # Normally the GPU is done with the buffer already, but an error or
        # Ctrl+C may have interrupted the grab loop while GPU work was pending.
        self.gpu.wait_idle()
        context.destroy()
