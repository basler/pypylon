#!/usr/bin/env python3

"""
Camera Configuration Load and Save Sample

This sample application demonstrates how to save or load the features of a camera
to or from a file. This is useful for:
- Backing up camera configurations
- Sharing camera settings between cameras
- Restoring camera settings after firmware updates
- Creating standardized camera configurations

The FeaturePersistence class provides static methods for saving and loading
camera parameters to/from a .pfs (Pylon Feature Stream) file.

Equivalent C++ sample: samples_reference_c++/ParametrizeCamera_LoadAndSave/ParametrizeCamera_LoadAndSave.cpp
"""

from pypylon import pylon
from pypylon import genicam
import sys
import os
from typing import Optional


def save_camera_configuration(camera: pylon.InstantCamera, filename: str) -> bool:
    """
    Save camera configuration to file.
    
    Args:
        camera: The camera instance to save configuration from
        filename: The filename to save to (should have .pfs extension)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"Saving camera's node map to file: {filename}")
        
        # Save the content of the camera's node map to the file
        pylon.FeaturePersistence.Save(filename, camera.GetNodeMap())
        
        # Check if file was created successfully
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"Configuration saved successfully ({file_size} bytes)")
            return True
        else:
            print("Warning: Configuration file was not created")
            return False
            
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False


def load_camera_configuration(camera: pylon.InstantCamera, filename: str, validate: bool = True) -> bool:
    """
    Load camera configuration from file.
    
    Args:
        camera: The camera instance to load configuration to
        filename: The filename to load from
        validate: Whether to validate all node values after loading
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(filename):
            print(f"Error: Configuration file '{filename}' not found")
            return False
        
        print(f"Reading file back to camera's node map: {filename}")
        
        # Load the content of the file back to the camera's node map
        # The validate parameter enables validation of all node values
        pylon.FeaturePersistence.Load(filename, camera.GetNodeMap(), validate)
        
        print("Configuration loaded successfully")
        if validate:
            print("All parameter values validated")
        
        return True
        
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False


def display_camera_info(camera: pylon.InstantCamera) -> None:
    """Display basic camera information."""
    try:
        info = camera.GetDeviceInfo()
        print(f"Camera Information:")
        print(f"  Model: {info.GetModelName()}")
        print(f"  Serial: {info.GetSerialNumber()}")
        print(f"  Vendor: {info.GetVendorName()}")
        print()
    except Exception as e:
        print(f"Could not retrieve camera information: {e}")


def demonstrate_parameter_changes(camera: pylon.InstantCamera) -> None:
    """Demonstrate some parameter changes to show that configuration persistence works."""
    try:
        print("Making some parameter changes for demonstration...")
        
        # Try to modify some common parameters if they exist
        if hasattr(camera, 'Width') and camera.Width.IsWritable():
            original_width = camera.Width.Value
            new_width = max(camera.Width.Min, original_width - 100)
            camera.Width.Value = new_width
            print(f"  Changed Width from {original_width} to {new_width}")
        
        if hasattr(camera, 'Height') and camera.Height.IsWritable():
            original_height = camera.Height.Value
            new_height = max(camera.Height.Min, original_height - 100)
            camera.Height.Value = new_height
            print(f"  Changed Height from {original_height} to {new_height}")
        
        if hasattr(camera, 'ExposureTime') and camera.ExposureTime.IsWritable():
            try:
                original_exposure = camera.ExposureTime.Value
                new_exposure = min(camera.ExposureTime.Max, original_exposure * 1.5)
                camera.ExposureTime.Value = new_exposure
                print(f"  Changed ExposureTime from {original_exposure:.1f} to {new_exposure:.1f}")
            except:
                print("  Could not modify ExposureTime (may be in auto mode)")
        
        print()
        
    except Exception as e:
        print(f"Error making parameter changes: {e}")


def main() -> int:
    """Main function demonstrating camera configuration save and load."""
    
    # The name of the pylon feature stream file
    config_filename = "NodeMap.pfs"
    
    # The exit code of the sample application
    exit_code = 0
    
    try:
        # Create an instant camera object with the camera device found first
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Display camera information
        display_camera_info(camera)
        
        # Open the camera to access parameters
        camera.Open()
        
        print("=== Saving Camera Configuration ===")
        
        # Save the current camera configuration
        if not save_camera_configuration(camera, config_filename):
            print("Failed to save configuration")
            return 1
        
        print()
        print("=== Modifying Camera Parameters ===")
        
        # Make some changes to demonstrate that loading works
        demonstrate_parameter_changes(camera)
        
        print("=== Loading Camera Configuration ===")
        
        # Load the configuration back (this should restore the original settings)
        if not load_camera_configuration(camera, config_filename, validate=True):
            print("Failed to load configuration")
            return 1
        
        print()
        print("=== Configuration Persistence Demonstration Complete ===")
        print(f"The camera configuration has been saved to and loaded from '{config_filename}'")
        print("Original settings have been restored.")
        
        # Close the camera
        camera.Close()
        
        # Clean up the created file (optional)
        try:
            if os.path.exists(config_filename):
                print(f"\nCleaning up: Removing '{config_filename}'")
                os.remove(config_filename)
        except Exception as e:
            print(f"Warning: Could not remove configuration file: {e}")
        
    except genicam.GenericException as e:
        # Error handling
        print("A GenICam exception occurred:")
        print(f"{e}")
        exit_code = 1
    except Exception as e:
        # Handle any other exceptions
        print("An unexpected error occurred:")
        print(f"{e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    print("=== Camera Configuration Load and Save Sample ===")
    print("This sample demonstrates how to save and load camera configurations using pypylon.")
    print("Press Ctrl+C to stop the application.")
    print()
    
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        exit_code = 0
    
    print("\nApplication finished.")
    # Wait for user input before exiting (optional)
    input("Press Enter to exit...")
    sys.exit(exit_code) 