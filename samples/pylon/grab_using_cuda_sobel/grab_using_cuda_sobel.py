#!/usr/bin/env python3
"""\
This sample demonstrates how to improve processing speed by using a custom
image buffer factory with algorithms that run on a CUDA-capable GPU.

This is a true zero-copy GPU processing pipeline: the buffer factory
(CudaPinnedBufferFactory) allocates pinned, mapped host memory and hands the
mapped host pointer back to pylon, so the camera DMAs the image data directly
into GPU-accessible memory. The grab result therefore only carries a pointer
into this shared memory - no intermediate host-to-device copy is made before
running the GPU algorithm.

A CUDA Sobel edge-detection kernel then runs directly on that buffer, which
is accessed through its device pointer (obtained via
cudaHostGetDevicePointer from the CUDA Python bindings).

This is the Python counterpart of the Grab_UsingCudaSobel C++ sample.

Requirements:
- An NVIDIA GPU, a recent CUDA Toolkit, and a working CUDA runtime.
- The device must support mapped pinned memory (canMapHostMemory).

Python packages:
 - numpy
 - pypylon
 - cupy-cuda12x
 - cuda-bindings

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon
import numpy as np
import cupy as cp
from cuda.bindings import runtime as cuda_runtime

# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 200
RETRIEVE_TIMEOUT_MS = 5000


def select_cuda_device_for_zero_copy(device_id=0):
    """Selects a CUDA device and verifies that it supports mapped pinned memory.

    Zero-copy access from the GPU to the camera's pinned host buffers only
    works if the selected device can map host memory, so this must be
    checked before any pinned memory is allocated.
    """
    cp.cuda.runtime.setDevice(device_id)

    device_properties = cp.cuda.runtime.getDeviceProperties(device_id)
    if not device_properties["canMapHostMemory"]:
        raise RuntimeError(
            "CUDA device cannot map host memory (required for zero-copy)."
        )

    print("Using GPU:", device_properties["name"].decode())


class CudaPinnedBufferFactory(pylon.BufferFactory):
    """A user-provided buffer factory that allocates pinned, GPU-mapped memory.

    The pinned, mapped memory is directly addressable by the GPU, so a CUDA
    kernel can read the grabbed image without an explicit host-to-device copy.
    """

    def AllocateBuffer(self, buffer_size):
        """Allocates buffer_size bytes of pinned, mapped host memory.

        The memory is allocated with the "mapped" flag so that, in addition
        to being page-locked (pinned) for fast host <-> device transfers, it
        is also directly addressable by the GPU (zero-copy access): the
        camera's DMA engine writes the grabbed image directly into memory
        the GPU can read.

        The context is a dictionary holding the pinned memory and a NumPy
        view of it, so pypylon keeps both alive between AllocateBuffer() and
        FreeBuffer(). The context can later be retrieved from a grab result
        by accessing grab_result.BufferContext.

        Warning: This method can be called by different threads.
        """
        pinned_allocation = cp.cuda.PinnedMemory(
            buffer_size,
            flags=cp.cuda.runtime.hostAllocMapped
        )
        pinned_memory = cp.cuda.PinnedMemoryPointer(pinned_allocation, 0)

        host_array = np.frombuffer(
            pinned_memory,
            dtype=np.uint8,
            count=buffer_size
        )

        context = {
            "host": host_array,
            "mem": pinned_memory
        }

        return host_array.ctypes.data, context

    def FreeBuffer(self, buffer, context):
        """Frees a previously allocated buffer.

        Dropping the references here lets CuPy free the pinned, mapped
        memory immediately instead of waiting for it to be garbage-collected
        along with the context dictionary.

        Warning: This method can be called by different threads.
        """
        context["host"] = None
        context["mem"] = None

    def OnReleased(self):
        """Called when the buffer factory is released.

        Warning: This method can be called by different threads.
        """
        print("Buffer factory released.")


def gpu_pointer_from_grab_result(grab_result):
    """Returns a GPU-accessible MemoryPointer for a grab result's buffer.

    The buffer factory only allocates mapped, pinned host memory; it does
    not allocate separate GPU device memory. To let the GPU read that memory
    directly (zero-copy), the device-side address must be looked up
    explicitly - it is not necessarily the same as the host pointer, even
    though both addresses often coincide on systems with unified virtual
    addressing (UVA).
    """
    context = grab_result.BufferContext
    pinned_memory = context["mem"]

    status, device_pointer = cuda_runtime.cudaHostGetDevicePointer(
        pinned_memory.ptr, 0
    )
    if status != cuda_runtime.cudaError_t.cudaSuccess:
        raise RuntimeError(f"cudaHostGetDevicePointer failed: {status}")
    buffer_bytes = grab_result.PayloadSize

    # Wrap the device pointer so CuPy can create an ndarray backed by it.
    unowned_memory = cp.cuda.UnownedMemory(
        device_pointer, buffer_bytes, owner=pinned_memory
    )
    return cp.cuda.MemoryPointer(unowned_memory, offset=0)


# CUDA kernel implementing a Sobel filter for edge detection: the sharper
# the edge in the source image, the brighter the corresponding output pixel.
SOBEL_KERNEL = cp.RawKernel(r'''
extern "C" __global__
void sobel(
    const unsigned char* source_image,
    unsigned char* destination_image,
    int width,
    int height)
{
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x < 1 || y < 1 ||
        x >= width - 1 ||
        y >= height - 1)
        return;

    int p00 = source_image[(y - 1) * width + (x - 1)];
    int p01 = source_image[(y - 1) * width + x];
    int p02 = source_image[(y - 1) * width + (x + 1)];

    int p10 = source_image[y * width + (x - 1)];
    int p12 = source_image[y * width + (x + 1)];

    int p20 = source_image[(y + 1) * width + (x - 1)];
    int p21 = source_image[(y + 1) * width + x];
    int p22 = source_image[(y + 1) * width + (x + 1)];

    int horizontal_gradient =
        -p00 + p02
        -2 * p10 + 2 * p12
        -p20 + p22;

    int vertical_gradient =
        -p00 - 2 * p01 - p02
        +p20 + 2 * p21 + p22;

    float magnitude = sqrtf(
        (float)(horizontal_gradient * horizontal_gradient +
                vertical_gradient * vertical_gradient)
    );

    if (magnitude > 255.0f)
        magnitude = 255.0f;

    destination_image[y * width + x] =
        (unsigned char)magnitude;
}
''', "sobel")


exit_code = 0
try:
    # Select a CUDA device and make sure it supports mapped, pinned host
    # memory, so the zero-copy buffer factory below works correctly.
    select_cuda_device_for_zero_copy()

    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        # The Sobel kernel below only supports Mono8 images, force it here.
        camera.PixelFormat.Value = "Mono8"

        width = camera.Width.Value
        height = camera.Height.Value

        # Use our own implementation of a buffer factory.
        factory = CudaPinnedBufferFactory()
        camera.SetBufferFactory(factory)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 5

        block = (16, 16)
        grid = (
            (width + block[0] - 1) // block[0],
            (height + block[1] - 1) // block[1]
        )

        # The buffer that holds the Sobel-filtered image.
        gpu_output = cp.empty(
            (height, width),
            dtype=cp.uint8
        )

        # A dedicated stream for the Sobel kernel. Using an explicit stream
        # makes it clear which work must complete - and be synchronized -
        # before the camera's buffer (gpu_input) may be reused.
        stream = cp.cuda.Stream()

        # Start the grabbing of COUNT_OF_IMAGES_TO_GRAB images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

        # StopGrabbing is called automatically by the RetrieveResult method
        # when COUNT_OF_IMAGES_TO_GRAB images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            with camera.RetrieveResult(
                RETRIEVE_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
            ) as grab_result:

                # Image grabbed successfully?
                if grab_result.GrabSucceeded():
                    if grab_result.PayloadType == pylon.PayloadType_Image:
                        # Obtain the GPU-accessible pointer for the grab result's
                        # zero-copy buffer.
                        gpu_pointer = gpu_pointer_from_grab_result(grab_result)

                        # Wrap the pointer in a GPU array matching the image shape.
                        gpu_input = cp.ndarray(
                            shape=(height, width),
                            dtype=cp.uint8,
                            memptr=gpu_pointer
                        )

                        # Run the Sobel filter directly on the camera's zero-copy
                        # buffer (gpu_input).
                        with stream:
                            SOBEL_KERNEL(
                                grid,
                                block,
                                (
                                    gpu_input,
                                    gpu_output,
                                    np.int32(width),
                                    np.int32(height)
                                )
                            )

                        # Wait for the kernel to finish reading gpu_input before
                        # releasing the grab result below, so the camera's
                        # buffer can safely be handed back to pylon for reuse.
                        stream.synchronize()

                        # Until now, the result was stored entirely in GPU memory.
                        # Transfer it into host memory so it can be displayed.
                        sobel_cpu = cp.asnumpy(gpu_output)

                        # Display the grabbed image.
                        pylon.DisplayImage(1, grab_result)

                        # Display the result of the Sobel filter.
                        sobel_image = pylon.PylonImage()
                        sobel_image.AttachMemoryView(
                            memoryview(sobel_cpu),
                            pylon.PixelType_Mono8,
                            width,
                            height,
                            0
                        )
                        pylon.DisplayImage(2, sobel_image)
                    else:
                        print("This sample only works for 2D image payloads.")
                else:
                    print(
                        "Error:",
                        f"{grab_result.ErrorCode:#x}",
                        grab_result.ErrorDescription,
                    )

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)

