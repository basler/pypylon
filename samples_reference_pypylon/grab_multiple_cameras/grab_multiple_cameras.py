#!/usr/bin/env python3

"""
Multiple Cameras Grabbing Sample

This sample illustrates how to grab and process images from multiple cameras
using the InstantCameraArray class. The InstantCameraArray class represents
an array of instant camera objects. It provides almost the same interface
as the instant camera for grabbing.

The main purpose of the InstantCameraArray is to simplify waiting for images and
camera events of multiple cameras in one thread. This is done by providing a single
RetrieveResult method for all cameras in the array.

Alternatively, the grabbing can be started using the internal grab loop threads
of all cameras in the InstantCameraArray. The grabbed images can then be processed by one or more
image event handlers. Please note that this is not shown in this example.

Equivalent C++ sample: samples_reference_c++/Grab_MultipleCameras/Grab_MultipleCameras.cpp
"""

import os
from pypylon import pylon
from pypylon import genicam
import sys
from typing import List, Optional


def setup_emulated_cameras(num_cameras: int = 3) -> None:
    """Setup emulated cameras for testing when no physical cameras are available."""
    os.environ["PYLON_CAMEMU"] = str(num_cameras)


def print_camera_info(cameras: pylon.InstantCameraArray) -> None:
    """Print information about all cameras in the array."""
    print(f"Found {cameras.GetSize()} cameras:")
    for i, cam in enumerate(cameras):
        print(f"  Camera {i}: {cam.GetDeviceInfo().GetModelName()}")
    print()


def main() -> int:
    """Main function demonstrating multiple camera grabbing."""
    
    # Number of images to be grabbed
    count_of_images_to_grab = 10
    
    # Limits the amount of cameras used for grabbing.
    # It is important to manage the available bandwidth when grabbing with multiple cameras.
    # This applies, for instance, if two GigE cameras are connected to the same network adapter via a switch.
    # To manage the bandwidth, the GevSCPD interpacket delay parameter and the GevSCFTD transmission delay
    # parameter can be set for each GigE camera device.
    # The "Controlling Packet Transmission Timing with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
    # Application Notes (AW000649xx000)
    # provide more information about this topic.
    # The bandwidth used by a GigE camera device can be limited by adjusting the packet size.
    max_cameras_to_use = 2
    
    # The exit code of the sample application
    exit_code = 0
    
    try:
        # Setup emulated cameras for testing (remove this line when using physical cameras)
        setup_emulated_cameras(3)
        
        # Get the transport layer factory
        tl_factory = pylon.TlFactory.GetInstance()
        
        # Get all attached devices and exit application if no device is found
        devices = tl_factory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RuntimeException("No camera present.")
        
        print(f"Found {len(devices)} device(s)")
        
        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices
        cameras = pylon.InstantCameraArray(min(len(devices), max_cameras_to_use))
        
        # Create and attach all Pylon Devices
        for i, cam in enumerate(cameras):
            cam.Attach(tl_factory.CreateDevice(devices[i]))
            print(f"Using device {i}: {cam.GetDeviceInfo().GetModelName()}")
        
        print()
        print(f"Starting grabbing from {cameras.GetSize()} cameras...")
        print(f"Will grab {count_of_images_to_grab} images total")
        print()
        
        # Starts grabbing for all cameras starting with index 0. The grabbing
        # is started for one camera after the other. That's why the images of all
        # cameras are not taken at the same time.
        # However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
        # According to their default configuration, the cameras are
        # set up for free-running continuous acquisition.
        cameras.StartGrabbing()
        
        # Grab count_of_images_to_grab from the cameras
        for i in range(count_of_images_to_grab):
            if not cameras.IsGrabbing():
                break
            
            print(f"Grabbing image {i + 1}/{count_of_images_to_grab}...")
            
            # Wait for an image from any camera and then retrieve it. A timeout of 5000 ms is used.
            grab_result = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            
            # Image grabbed successfully?
            if grab_result.GrabSucceeded():
                # When the cameras in the array are created the camera context value
                # is set to the index of the camera in the array.
                # The camera context is a user settable value.
                # This value is attached to each grab result and can be used
                # to determine the camera that produced the grab result.
                camera_context_value = grab_result.GetCameraContext()
                
                # Print the index and the model name of the camera
                camera_model = cameras[camera_context_value].GetDeviceInfo().GetModelName()
                print(f"  Camera {camera_context_value}: {camera_model}")
                
                # Now, the image data can be processed
                print(f"  GrabSucceeded: {grab_result.GrabSucceeded()}")
                print(f"  SizeX: {grab_result.GetWidth()}")
                print(f"  SizeY: {grab_result.GetHeight()}")
                
                # Access the image data as numpy array
                img = grab_result.GetArray()
                print(f"  Gray value of first pixel: {img[0, 0]}")
                
                # Optional: Display the grabbed image (requires GUI support)
                # pylon.DisplayImage(camera_context_value, grab_result)
                
                print()
            else:
                print(f"  Error: {grab_result.GetErrorCode():#x} {grab_result.GetErrorDescription()}")
            
            # Release the grab result
            grab_result.Release()
        
        print("Grabbing completed successfully!")
        print()
        
        # Stop grabbing
        cameras.StopGrabbing()
        
        # Close all cameras
        for cam in cameras:
            cam.Close()
        
    except genicam.GenericException as e:
        # Error handling
        print("An exception occurred:")
        print(f"{e}")
        exit_code = 1
    except pylon.RuntimeException as e:
        # Pylon-specific error handling
        print("A pylon runtime exception occurred:")
        print(f"{e}")
        exit_code = 1
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred:")
        print(f"{e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    print("=== Multiple Cameras Grabbing Sample ===")
    print("This sample demonstrates how to grab images from multiple cameras using pypylon.")
    print("Note: Using emulated cameras for demonstration. Remove the setup_emulated_cameras() call for physical cameras.")
    print("Press Ctrl+C to stop the application.")
    print()
    
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        exit_code = 0
    
    print("Application finished.")
    # Wait for user input before exiting (optional)
    input("Press Enter to exit...")
    sys.exit(exit_code) 