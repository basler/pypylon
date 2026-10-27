#!/usr/bin/env python3
"""\
This sample illustrates how to grab images into Vulkan memory and process them on the GPU.

The images are not copied (zero copy): a custom buffer factory
(VulkanBufferFactory) allocates the pylon grab buffers in Vulkan memory that is
mapped into the address space of the application. The camera writes each image
into that memory, and the GPU reads it in place.

Each grabbed Mono8 image then runs through GPU filters. This sample uses one
Sobel edge detection filter. To add your own filter, e.g. dewarping or defect
pixel correction, derive it from ImageFilter like SobelFilter, create it next
to the Sobel filter below and chain it in the grab loop. The original image and
the final result are shown side by side.

Files:
    grab_using_vulkan_sobel.py  camera setup and grab loop (this file)
    buffer_factory.py           grab buffers in Vulkan memory (zero copy)
    image_filter.py             base class for GPU filters
    sobel_filter.py             Sobel filter: shader, output image and commands
    display.py                  window showing original and result side by side
    vulkan_context.py           Vulkan device, memory and compute shader helpers

Requirements: Python 3.10 or newer, vulkan (the Khronos Python bindings) and a
Vulkan 1.1 compute device. The window additionally requires PySDL2 and a compute
queue that can present.

Packages that need to be installed:
- pypylon
- vulkan
- PySDL2

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound:
https://docs.baslerweb.com/camera-emulation

PYLON_CAMEMU=1 ~/pypylon-vulkan-venv/bin/python3 grab_using_vulkan_sobel.py

"""

import argparse
import sys
import time

from pypylon import pylon

from buffer_factory import VulkanBufferFactory
from display import ImageDisplay
from sobel_filter import SobelFilter
from vulkan_context import VulkanContext


def parse_arguments():
    """Parse and validate the command line arguments.

    Exits the program with a usage message if an argument is invalid.

    Returns:
        argparse.Namespace: The arguments, with the attributes vulkan_device
        (int or None), host_memory (bool).
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--vulkan-device",
        type=int,
        default=None,
        help="index into vkEnumeratePhysicalDevices (default: prefer discrete GPU)",
    )
    parser.add_argument(
        "--host-memory",
        action="store_true",
        help="place the grab buffers in host memory instead of GPU memory "
        "that is visible to the host",
    )
    arguments = parser.parse_args()
    return arguments

# Number of images to be grabbed.
COUNT_OF_IMAGES_TO_GRAB = 100

# The exit code of the sample application.
exit_code = 0

try:
    arguments = parse_arguments()

    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        camera.PixelFormat.Value = "Mono8"
        # The GPU shaders process four Mono8 pixels at once; the width must be a multiple of 4.
        camera.Width.SetValue(
            camera.Width.Value // 4 * 4, pylon.IntegerValueCorrection_Down
        )
        width = camera.Width.Value
        height = camera.Height.Value
        print(f"Image size: {width} x {height}")

        window_size = ImageDisplay.window_size_for(width, height)

        # Each filter owns the GPU resources of its algorithm.
        # Add your own filters here, e.g. DewarpingFilter(gpu, width, height) as dewarping_filter.
        with (
            VulkanContext(arguments.vulkan_device, window_size) as gpu,
            SobelFilter(gpu, width, height) as sobel_filter,
            ImageDisplay(gpu) as display,
        ):
            # Zero copy: pylon grabs directly into Vulkan memory.
            camera.SetBufferFactory(
                VulkanBufferFactory(
                    gpu, width, height, prefer_device_local=not arguments.host_memory
                )
            )

            # The parameter MaxNumBuffer can be used to control the count of buffers
            # allocated for grabbing. The default value of this parameter is 10.
            camera.MaxNumBuffer.Value = 8

            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB, pylon.GrabStrategy_LatestImageOnly)

            while camera.IsGrabbing() and display.is_open():
                with camera.RetrieveResult(
                        5000, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    if not grab_result.GrabSucceeded():
                        print("Error:", grab_result.ErrorCode, grab_result.ErrorDescription)
                        continue

                    # The grab buffer is Vulkan memory; the GPU reads it in place.
                    camera_image = grab_result.BufferContext

                    result_image = sobel_filter.process(camera_image)
                    # Chain further filters here, e.g.:
                    # result_image = dewarping_filter.process(result_image)

                    display.show(camera_image, result_image)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
