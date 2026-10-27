"""Base class for GPU image filters."""


class ImageFilter:
    """A GPU algorithm that turns an input GpuImage into an output GpuImage.

    Filters can be chained: the output of one filter is the input of the next.

    To write a filter (see sobel_filter.py for an example):

    * Create all GPU resources the algorithm needs in __init__, e.g. a
      ComputeShader, and store the result image in self.output_image.
    * Implement record() to record the GPU commands for one input image.
    * Release the resources in destroy() and call super().destroy().

    process() records the commands once per input image and replays them for
    all later frames. pylon reuses a fixed set of grab buffers, so after the
    first few frames, no more commands are recorded. A filter that cannot be
    pre-recorded, e.g. because it changes parameters per frame, can override
    process() instead.

    Filters are context managers; their GPU resources are released on exit.
    """

    def __init__(self, gpu):
        """Prepare the filter; subclasses create their GPU resources here.

        Args:
            gpu (VulkanContext): Context used to create resources and run
                commands.
        """
        self.gpu = gpu
        self.output_image = None
        self.recorded_commands = {}

    def __enter__(self):
        """Enter the with block.

        Returns:
            ImageFilter: This filter.
        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Release the GPU resources of the filter when leaving the with block.

        Exceptions raised in the with block are not suppressed.

        Args:
            exception_type (type or None): Type of the exception raised in the
                with block, or None.
            exception_value (BaseException or None): The exception, or None.
            traceback (types.TracebackType or None): Its traceback, or None.
        """
        self.destroy()

    def process(self, input_image):
        """Run the filter on input_image and wait until the GPU has finished.

        Args:
            input_image (GpuImage): Image to process, e.g. a grab buffer
                (grab_result.BufferContext) or the output of another filter.

        Returns:
            GpuImage: self.output_image. The same image is returned on every
            call, so its content is only valid until the next call.
        """
        command_buffer = self.recorded_commands.get(input_image)
        if command_buffer is None:
            command_buffer = self.gpu.record_commands(
                lambda new_command_buffer: self.record(new_command_buffer, input_image)
            )
            self.recorded_commands[input_image] = command_buffer
        self.gpu.run(command_buffer)
        return self.output_image

    def record(self, command_buffer, input_image):
        """Record the commands that compute self.output_image from input_image.

        Subclasses must implement this method. It is called once per input
        image; the recorded commands are replayed for later frames.

        Args:
            command_buffer (VkCommandBuffer): Command buffer in the recording
                state.
            input_image (GpuImage): Image the commands read from.

        Raises:
            NotImplementedError: If the subclass does not implement it.
        """
        raise NotImplementedError

    def destroy(self):
        """Wait for the GPU and free the recorded command buffers.

        Subclasses release their own resources after calling super().destroy().
        """
        self.gpu.wait_idle()
        for command_buffer in self.recorded_commands.values():
            self.gpu.free_command_buffer(command_buffer)
        self.recorded_commands.clear()
