#!/usr/bin/env python3

"""
Grab Strategies Sample

This sample shows the use of the different grab strategies available in pypylon.

There are different strategies to grab images with the InstantCamera grab engine:
* One By One: This strategy is the default grab strategy. Acquired images are processed in their arrival order.
* Latest Image Only: Differs from the One By One strategy by a single image output queue. Therefore, only the latest
  image is kept in the output queue, all other grabbed images are skipped.
* Latest Images: Extends the above strategies by adjusting the size of output queue. If the output queue has a size of
  1, it is equal to the Latest Image Only strategy. Consequently, setting the output queue size to 
  MaxNumBuffer is equal to One by One.
* Upcoming Image Grab: Ensures that the image grabbed is the next image received from the camera. When retrieving an 
  image, a buffer is queued into the input queue and then the call waits for the upcoming image. Subsequently, image data 
  is grabbed into the buffer and returned. Note: This strategy can't be used together with USB camera devices.

Equivalent C++ sample: samples_reference_c++/Grab_Strategies/Grab_Strategies.cpp
"""

from pypylon import pylon
from pypylon import genicam
import sys
import time
from typing import Optional


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def demonstrate_one_by_one_strategy(camera: pylon.InstantCamera) -> None:
    """Demonstrate the GrabStrategy_OneByOne strategy."""
    print_section("Grab using the GrabStrategy_OneByOne default strategy:")
    
    # The GrabStrategy_OneByOne strategy is used. The images are processed
    # in the order of their arrival.
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    
    # In the background, the grab engine thread retrieves the
    # image data and queues the buffers into the internal output queue.
    
    # Issue software triggers. For each call, wait up to 1000 ms until the camera is ready for triggering the next image.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()
            print(f"Triggered image {i + 1}")
    
    # For demonstration purposes, wait for the last image to appear in the output queue.
    time.sleep(3.0)
    
    # Check that grab results are waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("Grab results wait in the output queue.")
    
    # All triggered images are still waiting in the output queue
    # and are now retrieved.
    # The grabbing continues in the background, e.g. when using hardware trigger mode,
    # as long as the grab engine does not run out of buffers.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        buffers_in_queue += 1
        grab_result.Release()
    
    print(f"Retrieved {buffers_in_queue} grab results from output queue.")
    
    # Stop the grabbing.
    camera.StopGrabbing()


def demonstrate_latest_image_only_strategy(camera: pylon.InstantCamera) -> None:
    """Demonstrate the GrabStrategy_LatestImageOnly strategy."""
    print_section("Grab using strategy GrabStrategy_LatestImageOnly:")
    
    # The GrabStrategy_LatestImageOnly strategy is used. The images are processed
    # in the order of their arrival but only the last received image
    # is kept in the output queue.
    # This strategy can be useful when the acquired images are only displayed on the screen.
    # If the processor has been busy for a while and images could not be displayed automatically
    # the latest image is displayed when processing time is available again.
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    
    # Execute the software trigger, wait actively until the camera accepts the next frame trigger or until the timeout occurs.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()
            print(f"Triggered image {i + 1}")
    
    # Wait for all images.
    time.sleep(3.0)
    
    # Check whether the grab result is waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("A grab result waits in the output queue.")
    
    # Only the last received image is waiting in the internal output queue
    # and is now retrieved.
    # The grabbing continues in the background, e.g. when using the hardware trigger mode.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        print(f"Skipped {grab_result.GetNumberOfSkippedImages()} images.")
        buffers_in_queue += 1
        grab_result.Release()
    
    print(f"Retrieved {buffers_in_queue} grab result from output queue.")
    
    # Stop the grabbing.
    camera.StopGrabbing()


def demonstrate_latest_images_strategy(camera: pylon.InstantCamera) -> None:
    """Demonstrate the GrabStrategy_LatestImages strategy."""
    print_section("Grab using strategy GrabStrategy_LatestImages:")
    
    # The GrabStrategy_LatestImages strategy is used. The images are processed
    # in the order of their arrival, but only a number of the images received last
    # are kept in the output queue.
    
    # The size of the output queue can be adjusted.
    # When using this strategy the OutputQueueSize parameter can be changed during grabbing.
    camera.OutputQueueSize.Value = 2
    print(f"Set output queue size to {camera.OutputQueueSize.Value}")
    
    camera.StartGrabbing(pylon.GrabStrategy_LatestImages)
    
    # Execute the software trigger, wait actively until the camera accepts the next frame trigger or until the timeout occurs.
    for i in range(3):
        if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()
            print(f"Triggered image {i + 1}")
    
    # Wait for all images.
    time.sleep(3.0)
    
    # Check whether the grab results are waiting.
    if camera.GetGrabResultWaitObject().Wait(0):
        print("Grab results wait in the output queue.")
    
    # Only the images received last are waiting in the internal output queue
    # and are now retrieved.
    # The grabbing continues in the background, e.g. when using the hardware trigger mode.
    buffers_in_queue = 0
    while True:
        grab_result = camera.RetrieveResult(0, pylon.TimeoutHandling_Return)
        if not grab_result.IsValid():
            break
        if grab_result.GetNumberOfSkippedImages():
            print(f"Skipped {grab_result.GetNumberOfSkippedImages()} image(s).")
        buffers_in_queue += 1
        grab_result.Release()
    
    print(f"Retrieved {buffers_in_queue} grab results from output queue.")
    
    # When setting the output queue size to 1 this strategy is equivalent to grab strategy GrabStrategy_LatestImageOnly.
    camera.OutputQueueSize.Value = 1
    print(f"Setting output queue size to 1 makes it equivalent to LatestImageOnly")
    
    # When setting the output queue size to MaxNumBuffer this strategy is equivalent to GrabStrategy_OneByOne.
    camera.OutputQueueSize.Value = camera.MaxNumBuffer.Value
    print(f"Setting output queue size to {camera.MaxNumBuffer.Value} makes it equivalent to OneByOne")
    
    # Stop the grabbing.
    camera.StopGrabbing()


def demonstrate_upcoming_image_strategy(camera: pylon.InstantCamera) -> None:
    """Demonstrate the GrabStrategy_UpcomingImage strategy."""
    print_section("Grab using the GrabStrategy_UpcomingImage strategy:")
    
    # The Upcoming Image grab strategy can't be used together with USB camera devices.
    # For more information, see the advanced topics section of the pylon Programmer's Guide.
    if camera.IsUsb():
        print("The GrabStrategy_UpcomingImage strategy cannot be used with USB camera devices.")
        return
    
    # Reconfigure the camera to use continuous acquisition.
    pylon.AcquireContinuousConfiguration().OnOpened(camera)
    
    # The GrabStrategy_UpcomingImage strategy is used. A buffer for grabbing
    # is queued each time when RetrieveResult()
    # is called. The image data is grabbed into the buffer and returned.
    # This ensures that the image grabbed is the next image
    # received from the camera.
    # All images are still transported to the computer.
    camera.StartGrabbing(pylon.GrabStrategy_UpcomingImage)
    
    # Queues a buffer for grabbing and waits for the grab to finish.
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grab_result.GrabSucceeded():
        print("Successfully grabbed upcoming image")
    grab_result.Release()
    
    # Sleep.
    time.sleep(1.0)
    
    # Check no grab result is waiting, because no buffers are queued for grabbing.
    if not camera.GetGrabResultWaitObject().Wait(0):
        print("No grab result waits in the output queue.")
    
    # Stop the grabbing.
    camera.StopGrabbing()


def main() -> int:
    """Main function demonstrating different grab strategies."""
    
    exit_code = 0
    
    try:
        # Create an instant camera object for the camera device found first.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Register the standard configuration event handler for enabling software triggering.
        # The software trigger configuration handler replaces the default configuration
        # as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
        
        # Print the model name of the camera.
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        
        # The MaxNumBuffer parameter can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 15
        print(f"MaxNumBuffer set to {camera.MaxNumBuffer.Value}")
        
        # Open the camera.
        camera.Open()
        
        # Can the camera device be queried whether it is ready to accept the next frame trigger?
        if camera.CanWaitForFrameTriggerReady():
            print("Camera supports frame trigger ready query.")
            
            # Demonstrate different grab strategies
            demonstrate_one_by_one_strategy(camera)
            demonstrate_latest_image_only_strategy(camera)
            demonstrate_latest_images_strategy(camera)
            demonstrate_upcoming_image_strategy(camera)
            
        else:
            # See the documentation of InstantCamera.CanWaitForFrameTriggerReady() for more information.
            print("\nThis sample can only be used with cameras that can be queried whether they are ready to accept the next frame trigger.")
        
        # Close the camera
        camera.Close()
        
    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred:")
        print(f"{e}")
        exit_code = 1
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred:")
        print(f"{e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    print("=== Grab Strategies Sample ===")
    print("This sample demonstrates different grab strategies available in pypylon.")
    print("Press Ctrl+C to stop the application.")
    print()
    
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        exit_code = 0
    
    # Wait for user input before exiting (optional)
    input("Press Enter to exit...")
    sys.exit(exit_code) 