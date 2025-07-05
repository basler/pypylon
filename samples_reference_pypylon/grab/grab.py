#!/usr/bin/env python3

"""
Basic Image Grabbing Sample

This sample illustrates how to grab and process images using the InstantCamera class.
The images are grabbed and processed asynchronously, i.e., while the application is 
processing a buffer, the acquisition of the next buffer is done in parallel.

The InstantCamera class uses a pool of buffers to retrieve image data from the camera 
device. Once a buffer is filled and ready, the buffer can be retrieved from the camera 
object for processing. The buffer and additional image data are collected in a grab result. 
The grab result is held by a smart pointer after retrieval. The buffer is automatically 
reused when explicitly released or when the smart pointer object is destroyed.

Equivalent C++ sample: samples_reference_c++/Grab/Grab.cpp
"""

from pypylon import pylon
from pypylon import genicam
import sys
from typing import Optional


def main() -> int:
    """Main function that demonstrates basic image grabbing."""
    
    # Number of images to be grabbed
    count_of_images_to_grab = 100
    
    # The exit code of the sample application
    exit_code = 0
    
    try:
        # Create an instant camera object with the camera device found first
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Print the model name of the camera
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        print()
        
        # Open the camera to access parameters
        camera.Open()
        
        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 5
        
        # Start the grabbing of count_of_images_to_grab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(count_of_images_to_grab)
        
        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when count_of_images_to_grab images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            
            # Image grabbed successfully?
            if grab_result.GrabSucceeded():
                # Access the image data
                print(f"SizeX: {grab_result.Width}")
                print(f"SizeY: {grab_result.Height}")
                
                # Access the image data as numpy array
                img = grab_result.Array
                print(f"Gray value of first pixel: {img[0, 0]}")
                print()
                
                # Optional: Display the grabbed image (requires GUI support)
                # pylon.DisplayImage(1, grab_result)
                
            else:
                print(f"Error: {grab_result.ErrorCode:#x} {grab_result.ErrorDescription}")
            
            # Release the grab result
            grab_result.Release()
        
        # Close the camera
        camera.Close()
        
    except genicam.GenericException as e:
        # Error handling
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
    print("=== Basic Image Grabbing Sample ===")
    print("This sample demonstrates how to grab and process images using pypylon.")
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