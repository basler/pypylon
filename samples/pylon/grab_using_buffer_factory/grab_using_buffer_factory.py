#!/usr/bin/env python3
"""\
This sample demonstrates how to use a user-provided buffer factory to grab
directly into NumPy arrays.

Using a buffer factory is optional and intended for advanced use cases only.
A buffer factory is only necessary if you want to grab into externally
supplied buffers.

The buffer factory below returns the NumPy array backing each buffer as the
buffer's context, so grab_result.BufferContext gives zero-copy access to
the very array pylon filled with image data - no extra copy through
grab_result.Array is needed.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon
import numpy as np

# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 5


class NumpyBufferFactory(pylon.BufferFactory):
    """A user-provided buffer factory that grabs directly into NumPy arrays."""

    def AllocateBuffer(self, buffer_size):
        """Allocates a flat NumPy array of buffer_size bytes for pixel data.

        The array itself is returned as the context, so pypylon keeps it
        alive between AllocateBuffer() and FreeBuffer() - no extra buffer
        bookkeeping is required here. The context can later be retrieved
        from a grab result by accessing grab_result.BufferContext.

        Warning: This method can be called by different threads.
        """
        print("Allocating buffer.")
        # note: if you are working with fixed image properties,
        # you can also preallocate an array of the exact size and reuse it for all buffers,
        # and skip the reshaping after grabbing.
        buffer_array = np.empty(buffer_size, dtype=np.uint8)
        return buffer_array.ctypes.data, buffer_array

    def FreeBuffer(self, buffer, context):
        """Frees a previously allocated buffer.

        The backing NumPy array (context) is released once this method
        returns and pypylon drops its own reference to it.

        Warning: This method can be called by different threads.
        """
        print("Buffer released.")

    def OnReleased(self):
        """Called when the buffer factory is released.

        This method is called once when the buffer factory is no longer
        needed by pypylon. It can be used to clean up any resources that
        were allocated in AllocateBuffer().

        Warning: This method can be called by different threads.
        """
        print("Buffer factory released.")


exit_code = 0
try:
    # The buffer factory is kept alive for as long as it is
    # attached to the InstantCamera object.
    numpy_buffer_factory = NumpyBufferFactory()

    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        camera.PixelFormat.Value = "Mono8" # The sample only works for Mono8 2D image payloads, force it here.

        # Use our own implementation of a buffer factory.
        camera.SetBufferFactory(numpy_buffer_factory)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = COUNT_OF_IMAGES_TO_GRAB

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            with camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            ) as grab_result:
                # Image grabbed successfully?
                if grab_result.GrabSucceeded():
                    if grab_result.PayloadType == pylon.PayloadType_Image:
                        # The buffer context is the exact NumPy array that pylon
                        # filled with pixel data - a zero-copy view, reshaped to
                        # the actual image dimensions.
                        buffer_array = grab_result.BufferContext
                        pixel_count = grab_result.Width * grab_result.Height
                        # copy=False makes reshape() raise a ValueError instead of
                        # silently copying, so a zero-copy view is guaranteed.
                        # reshape() returns a view of the original array, so the buffer context array is not changed.
                        # For other image formats, you may need to take PixelType and PaddingX into account when reshaping.
                        image = np.reshape(
                            buffer_array[:pixel_count],
                            (grab_result.Height, grab_result.Width),
                            copy=False,
                        )

                        print(f"SizeX: {image.shape[1]}; SizeY: {image.shape[0]}; "
                              f"Gray value of first pixel: {image[0, 0]}")

                        # Attach the NumPy array to a PylonImage for display.
                        pylon_image = pylon.PylonImage()
                        pylon_image.AttachMemoryView(
                            memoryview(image), pylon.PixelType_Mono8, image.shape[1], image.shape[0], 0
                        )
                        pylon.DisplayImage(1, pylon_image)

                        # Warning: the buffer context (NumPy array) content is only valid until the grab result is released.
                        # Otherwise, the buffer will be reused for the next grab and the data will be overwritten.
                    else:
                        print("This sample only works for 2D image payloads.")
                else:
                    print("Error: ", f"{grab_result.ErrorCode:#x}", grab_result.ErrorDescription)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
