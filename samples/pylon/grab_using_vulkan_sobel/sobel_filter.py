"""Sobel edge detection as a GPU image filter.

This file contains everything the algorithm needs: the compute shader, the
output image and the commands that run the shader. Use it as a template for
your own filters, e.g. dewarping or defect pixel correction.

The SPIR-V module is embedded as a zlib/base64 blob, so no shader compiler is
needed.
"""

from image_filter import ImageFilter
from vulkan_context import ComputeShader, decode_spirv

SOBEL_SPIRV_BASE64 = (
    "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"
)


class SobelFilter(ImageFilter):
    """Sobel edge magnitude of a Mono8 image; the output is a Mono8 image of the same size.

    GPU resources owned by this filter:

    * the Sobel compute shader,
    * the output image in GPU-local memory,
    * one pre-recorded command buffer per input image (managed by ImageFilter).
    """

    def __init__(self, gpu, width, height):
        """Create the Sobel shader and the output image.

        Args:
            gpu (VulkanContext): Context used to create the resources.
            width (int): Width of the input and output images in pixels; must
                be a multiple of 4.
            height (int): Height of the input and output images in pixels.

        Raises:
            ValueError: If width is not a multiple of 4.
        """
        super().__init__(gpu)
        # Shader interface: binding 0 = input image, binding 1 = output image,
        # push constants = width, height and stride.
        self.shader = ComputeShader(
            gpu,
            decode_spirv(SOBEL_SPIRV_BASE64),
            buffer_count=2,
            push_constant_count=3,
        )
        self.output_image = gpu.create_image(width, height)

    def record(self, command_buffer, input_image):
        """Record one dispatch of the Sobel shader from input_image to the output image.

        Args:
            command_buffer (VkCommandBuffer): Command buffer in the recording
                state.
            input_image (GpuImage): Mono8 image to filter; same size as the
                output image.
        """
        buffers = self.shader.bind_buffers(
            [input_image.buffer, self.output_image.buffer]
        )
        # Each shader invocation filters four packed Mono8 pixels;
        # a workgroup consists of 16 x 16 invocations.
        self.shader.dispatch(
            command_buffer,
            buffers,
            push_constants=[input_image.width, input_image.height, input_image.stride],
            group_count_x=(input_image.stride // 4 + 15) // 16,
            group_count_y=(input_image.height + 15) // 16,
        )

    def destroy(self):
        """Release the command buffers, the output image, and the shader."""
        super().destroy()
        self.output_image.destroy()
        self.shader.destroy()
