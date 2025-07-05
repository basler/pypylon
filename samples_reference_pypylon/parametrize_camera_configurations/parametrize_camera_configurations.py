#!/usr/bin/env python3
"""
parametrize_camera_configurations.py

This sample demonstrates how to use configuration event handlers by applying standard
configurations and registering custom configuration event handlers.

Configuration event handlers are derived from the ConfigurationEventHandler base class
and provide methods that are called when the state of the instant camera object changes,
e.g. when the camera object is opened or closed.

This is equivalent to samples_reference_c++/ParametrizeCamera_Configurations/
"""

from typing import Optional
import pypylon.pylon as pylon
from pypylon import genicam


class CustomConfigurationEventHandler(pylon.ConfigurationEventHandler):
    """Custom configuration event handler that prints information about camera state changes."""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    def OnOpened(self, camera: pylon.InstantCamera):
        """Called when the camera is opened."""
        print(f"[{self.name}] OnOpened: Camera opened")
    
    def OnClosed(self, camera: pylon.InstantCamera):
        """Called when the camera is closed."""
        print(f"[{self.name}] OnClosed: Camera closed")
    
    def OnGrabStart(self, camera: pylon.InstantCamera):
        """Called when grabbing starts."""
        print(f"[{self.name}] OnGrabStart: Grabbing started")
    
    def OnGrabStop(self, camera: pylon.InstantCamera):
        """Called when grabbing stops."""
        print(f"[{self.name}] OnGrabStop: Grabbing stopped")


class PixelFormatAndAoiConfiguration(pylon.ConfigurationEventHandler):
    """Custom configuration handler that sets pixel format and AOI."""
    
    def OnOpened(self, camera: pylon.InstantCamera):
        """Configure pixel format and AOI when camera is opened."""
        try:
            print("[PixelFormatAndAoiConfiguration] Configuring pixel format and AOI...")
            
            # Try to set offsets to minimum
            try:
                if hasattr(camera, 'OffsetX') and camera.OffsetX.IsWritable():
                    camera.OffsetX.Value = camera.OffsetX.Min
                if hasattr(camera, 'OffsetY') and camera.OffsetY.IsWritable():
                    camera.OffsetY.Value = camera.OffsetY.Min
            except (genicam.GenericException, AttributeError):
                pass
            
            # Try to maximize width and height
            try:
                if hasattr(camera, 'Width') and camera.Width.IsWritable():
                    camera.Width.Value = camera.Width.Max
                if hasattr(camera, 'Height') and camera.Height.IsWritable():
                    camera.Height.Value = camera.Height.Max
            except (genicam.GenericException, AttributeError):
                pass
            
            # Try to set pixel format to Mono8
            try:
                if hasattr(camera, 'PixelFormat') and camera.PixelFormat.IsWritable():
                    camera.PixelFormat.Value = "Mono8"
            except (genicam.GenericException, AttributeError):
                pass
            
            print("[PixelFormatAndAoiConfiguration] Configuration applied successfully")
            
        except Exception as e:
            print(f"[PixelFormatAndAoiConfiguration] Error during configuration: {e}")


class SimpleImageEventHandler(pylon.ImageEventHandler):
    """Simple image event handler that prints image information."""
    
    def OnImageGrabbed(self, camera: pylon.InstantCamera, grab_result: pylon.GrabResult):
        """Called when an image is grabbed."""
        if grab_result.GrabSucceeded():
            print(f"[ImageEventHandler] Image grabbed successfully: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
        else:
            print(f"[ImageEventHandler] Image grab failed: {grab_result.GetErrorDescription()}")


def demonstrate_continuous_acquisition(camera: pylon.InstantCamera) -> None:
    """Demonstrate continuous acquisition with default configuration."""
    print("=" * 60)
    print("Grab using continuous acquisition:")
    print("=" * 60)
    
    # For continuous acquisition, we can use the default configuration
    # or register a custom configuration handler
    
    # Register a custom configuration handler for demonstration
    config_handler = CustomConfigurationEventHandler("ContinuousAcquisition")
    camera.RegisterConfiguration(config_handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
    
    # Open the camera (this will trigger OnOpened)
    camera.Open()
    
    # Grab some images
    images_to_grab = 3
    camera.StartGrabbingMax(images_to_grab)
    
    while camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            print(f"  Grabbed image: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
        grab_result.Release()
    
    # Close the camera (this will trigger OnClosed)
    camera.Close()
    print()


def demonstrate_software_trigger(camera: pylon.InstantCamera) -> None:
    """Demonstrate software trigger configuration."""
    print("=" * 60)
    print("Grab using software trigger mode:")
    print("=" * 60)
    
    # Register the standard configuration event handler for software triggering
    camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                                pylon.RegistrationMode_ReplaceAll, 
                                pylon.Cleanup_Delete)
    
    # Add a custom configuration handler for demonstration
    config_handler = CustomConfigurationEventHandler("SoftwareTrigger")
    camera.RegisterConfiguration(config_handler, pylon.RegistrationMode_Append, pylon.Cleanup_Delete)
    
    # Open the camera (configurations will be applied)
    camera.Open()
    
    # Check if camera can be triggered
    if camera.CanWaitForFrameTriggerReady():
        # Grab some images using software trigger
        images_to_grab = 3
        camera.StartGrabbingMax(images_to_grab)
        
        while camera.IsGrabbing():
            # Wait for camera to be ready for next trigger
            camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException)
            
            # Execute software trigger
            camera.ExecuteSoftwareTrigger()
            
            # Retrieve the result
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grab_result.GrabSucceeded():
                print(f"  Triggered image: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
            grab_result.Release()
    else:
        print("  Camera does not support software triggering")
    
    camera.Close()
    print()


def demonstrate_single_frame_acquisition(camera: pylon.InstantCamera) -> None:
    """Demonstrate single frame acquisition configuration."""
    print("=" * 60)
    print("Grab using single frame acquisition:")
    print("=" * 60)
    
    # Register the standard configuration handler for single frame acquisition
    camera.RegisterConfiguration(pylon.AcquireSingleFrameConfiguration(), 
                                pylon.RegistrationMode_ReplaceAll, 
                                pylon.Cleanup_Delete)
    
    # Add a custom configuration handler for demonstration
    config_handler = CustomConfigurationEventHandler("SingleFrame")
    camera.RegisterConfiguration(config_handler, pylon.RegistrationMode_Append, pylon.Cleanup_Delete)
    
    # Use GrabOne for single frame acquisition
    grab_result = camera.GrabOne(5000)
    if grab_result.GrabSucceeded():
        print(f"  Single frame grabbed: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
    grab_result.Release()
    
    # For continuous single frame grabbing, it's more efficient to open the camera first
    camera.Open()
    
    # Grab multiple single frames
    for i in range(3):
        grab_result = camera.GrabOne(5000)
        if grab_result.GrabSucceeded():
            print(f"  Single frame {i+1}: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
        grab_result.Release()
    
    camera.Close()
    print()


def demonstrate_multiple_configurations(camera: pylon.InstantCamera) -> None:
    """Demonstrate using multiple configuration handlers."""
    print("=" * 60)
    print("Grab using multiple configuration objects:")
    print("=" * 60)
    
    # Register single frame acquisition configuration
    camera.RegisterConfiguration(pylon.AcquireSingleFrameConfiguration(), 
                                pylon.RegistrationMode_ReplaceAll, 
                                pylon.Cleanup_Delete)
    
    # Register additional configuration handler for pixel format and AOI
    camera.RegisterConfiguration(PixelFormatAndAoiConfiguration(), 
                                pylon.RegistrationMode_Append, 
                                pylon.Cleanup_Delete)
    
    # Register image event handler for demonstration
    camera.RegisterImageEventHandler(SimpleImageEventHandler(), 
                                   pylon.RegistrationMode_Append, 
                                   pylon.Cleanup_Delete)
    
    # Create a configuration event handler that we'll deregister later
    temp_config_handler = CustomConfigurationEventHandler("Temporary")
    camera.RegisterConfiguration(temp_config_handler, pylon.RegistrationMode_Append, pylon.Cleanup_None)
    
    print("\nGrab with all configuration handlers active:")
    grab_result = camera.GrabOne(5000)
    if grab_result.GrabSucceeded():
        print(f"  Image with all configurations: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
    grab_result.Release()
    
    # Deregister the temporary configuration handler
    camera.DeregisterConfiguration(temp_config_handler)
    del temp_config_handler
    
    print("\nGrab with temporary configuration handler removed:")
    grab_result = camera.GrabOne(5000)
    if grab_result.GrabSucceeded():
        print(f"  Image without temporary config: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
    grab_result.Release()
    
    print()


def main() -> int:
    """
    Main function demonstrating configuration event handlers.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        # Create an instant camera object with the first camera device found
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Print the model name of the camera
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}\n")
        
        # Demonstrate different configuration approaches
        demonstrate_continuous_acquisition(camera)
        demonstrate_software_trigger(camera)
        demonstrate_single_frame_acquisition(camera)
        demonstrate_multiple_configurations(camera)
        
        print("Configuration event handlers demonstration completed successfully!")
        
    except genicam.GenericException as e:
        print(f"An exception occurred: {e}")
        exit_code = 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit_code = 1
    finally:
        # Ensure pylon resources are released
        
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    print("=== Configuration Event Handlers Sample ===")
    print("This sample demonstrates various configuration event handlers and their usage.")
    print("Configuration handlers are called when camera state changes occur.\n")
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
        sys.exit(1) 