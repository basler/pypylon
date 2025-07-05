#!/usr/bin/env python3
"""
parametrize_camera_user_sets.py

This sample demonstrates how to use user configuration sets (user sets) and how to
configure the camera to start up with the user defined settings of user set 1.

User sets allow you to save and restore complete camera configurations.
You can also configure your camera using the pylon Viewer and store your custom
settings in a user set of your choice.

This is equivalent to samples_reference_c++/ParametrizeCamera_UserSets/

ATTENTION:
Executing this sample will overwrite all current settings in user set 1.
"""

from typing import Optional
import pypylon.pylon as pylon
from pypylon import genicam


def display_camera_info(camera: pylon.InstantCamera) -> None:
    """Display basic camera information."""
    try:
        info = camera.GetDeviceInfo()
        print(f"Using device: {info.GetModelName()}")
        print(f"Serial Number: {info.GetSerialNumber()}")
        print(f"Vendor: {info.GetVendorName()}\n")
    except Exception as e:
        print(f"Could not retrieve camera information: {e}")


def check_user_set_support(camera: pylon.InstantCamera) -> bool:
    """Check if the camera supports user sets."""
    try:
        # Check if UserSetSelector parameter exists and is writable
        if hasattr(camera, 'UserSetSelector') and camera.UserSetSelector.IsWritable():
            return True
        else:
            print("The device doesn't support user sets.")
            return False
    except (genicam.GenericException, AttributeError):
        print("The device doesn't support user sets.")
        return False


def get_current_default_user_set(camera: pylon.InstantCamera) -> tuple:
    """Get the current default user set for restoration later."""
    old_default_user_set = None
    old_default_user_set_selector = None
    
    try:
        # Used for USB cameras (SFNC 2.0+)
        if hasattr(camera, 'UserSetDefault') and camera.UserSetDefault.IsReadable():
            old_default_user_set = camera.UserSetDefault.Value
            print(f"Current default user set (SFNC 2.0+): {old_default_user_set}")
    except (genicam.GenericException, AttributeError):
        pass
    
    try:
        # Used for GigE cameras (SFNC 1.x)
        if hasattr(camera, 'UserSetDefaultSelector') and camera.UserSetDefaultSelector.IsReadable():
            old_default_user_set_selector = camera.UserSetDefaultSelector.Value
            print(f"Current default user set selector (SFNC 1.x): {old_default_user_set_selector}")
    except (genicam.GenericException, AttributeError):
        pass
    
    return old_default_user_set, old_default_user_set_selector


def restore_default_user_set(camera: pylon.InstantCamera, old_default_user_set, old_default_user_set_selector) -> None:
    """Restore the original default user set."""
    try:
        # Restore for USB cameras (SFNC 2.0+)
        if old_default_user_set is not None:
            if hasattr(camera, 'UserSetDefault') and camera.UserSetDefault.IsWritable():
                camera.UserSetDefault.Value = old_default_user_set
                print(f"Restored default user set to: {old_default_user_set}")
    except (genicam.GenericException, AttributeError):
        pass
    
    try:
        # Restore for GigE cameras (SFNC 1.x)
        if old_default_user_set_selector is not None:
            if hasattr(camera, 'UserSetDefaultSelector') and camera.UserSetDefaultSelector.IsWritable():
                camera.UserSetDefaultSelector.Value = old_default_user_set_selector
                print(f"Restored default user set selector to: {old_default_user_set_selector}")
    except (genicam.GenericException, AttributeError):
        pass


def load_default_settings(camera: pylon.InstantCamera) -> None:
    """Load default camera settings."""
    try:
        print("Loading default settings...")
        camera.UserSetSelector.Value = "Default"
        camera.UserSetLoad.Execute()
        print("Default settings loaded successfully")
    except Exception as e:
        print(f"Error loading default settings: {e}")


def configure_camera_parameters(camera: pylon.InstantCamera) -> None:
    """Configure camera parameters for demonstration."""
    print("Configuring camera parameters...")
    
    # Disable auto functions first to allow manual setting of gain and exposure
    try:
        if hasattr(camera, 'GainAuto') and camera.GainAuto.IsWritable():
            camera.GainAuto.Value = "Off"
            print("  Turned off Gain Auto")
    except (genicam.GenericException, AttributeError):
        print("  GainAuto not available or not writable")
    
    try:
        if hasattr(camera, 'ExposureAuto') and camera.ExposureAuto.IsWritable():
            camera.ExposureAuto.Value = "Off"
            print("  Turned off Exposure Auto")
    except (genicam.GenericException, AttributeError):
        print("  ExposureAuto not available or not writable")
    
    # Set gain and exposure time values
    # Check SFNC version to determine which parameters to use
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
        # Cameras based on SFNC 2.0 or later (e.g., USB cameras)
        try:
            if hasattr(camera, 'Gain') and camera.Gain.IsWritable():
                camera.Gain.Value = camera.Gain.Min
                print(f"  Set Gain to minimum: {camera.Gain.Value}")
        except (genicam.GenericException, AttributeError):
            print("  Gain parameter not available or not writable")
        
        try:
            if hasattr(camera, 'ExposureTime') and camera.ExposureTime.IsWritable():
                camera.ExposureTime.Value = camera.ExposureTime.Min
                print(f"  Set ExposureTime to minimum: {camera.ExposureTime.Value}")
        except (genicam.GenericException, AttributeError):
            print("  ExposureTime parameter not available or not writable")
    else:
        # Cameras based on SFNC 1.x (e.g., GigE cameras)
        try:
            if hasattr(camera, 'GainRaw') and camera.GainRaw.IsWritable():
                camera.GainRaw.Value = camera.GainRaw.Min
                print(f"  Set GainRaw to minimum: {camera.GainRaw.Value}")
        except (genicam.GenericException, AttributeError):
            print("  GainRaw parameter not available or not writable")
        
        try:
            if hasattr(camera, 'ExposureTimeRaw') and camera.ExposureTimeRaw.IsWritable():
                camera.ExposureTimeRaw.Value = camera.ExposureTimeRaw.Min
                print(f"  Set ExposureTimeRaw to minimum: {camera.ExposureTimeRaw.Value}")
        except (genicam.GenericException, AttributeError):
            print("  ExposureTimeRaw parameter not available or not writable")


def save_to_user_set(camera: pylon.InstantCamera, user_set: str) -> None:
    """Save current settings to specified user set."""
    try:
        print(f"\nSaving currently active settings to {user_set}...")
        print("ATTENTION: This will overwrite all settings previously saved in this user set.")
        
        camera.UserSetSelector.Value = user_set
        camera.UserSetSave.Execute()
        print(f"Settings saved to {user_set} successfully")
    except Exception as e:
        print(f"Error saving to {user_set}: {e}")


def load_user_set(camera: pylon.InstantCamera, user_set: str) -> None:
    """Load settings from specified user set."""
    try:
        print(f"\nLoading {user_set} settings...")
        camera.UserSetSelector.Value = user_set
        camera.UserSetLoad.Execute()
        print(f"{user_set} settings loaded successfully")
    except Exception as e:
        print(f"Error loading {user_set}: {e}")


def display_current_settings(camera: pylon.InstantCamera, title: str) -> None:
    """Display current camera settings."""
    print(f"\n{title}")
    print("=" * len(title))
    
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
        # SFNC 2.0+ parameters
        try:
            if hasattr(camera, 'Gain') and camera.Gain.IsReadable():
                print(f"Gain          : {camera.Gain.Value:.2f}")
        except (genicam.GenericException, AttributeError):
            print("Gain          : (not available)")
        
        try:
            if hasattr(camera, 'ExposureTime') and camera.ExposureTime.IsReadable():
                print(f"Exposure time : {camera.ExposureTime.Value:.1f}")
        except (genicam.GenericException, AttributeError):
            print("Exposure time : (not available)")
    else:
        # SFNC 1.x parameters
        try:
            if hasattr(camera, 'GainRaw') and camera.GainRaw.IsReadable():
                print(f"Gain          : {camera.GainRaw.Value}")
        except (genicam.GenericException, AttributeError):
            print("Gain          : (not available)")
        
        try:
            if hasattr(camera, 'ExposureTimeRaw') and camera.ExposureTimeRaw.IsReadable():
                print(f"Exposure time : {camera.ExposureTimeRaw.Value}")
        except (genicam.GenericException, AttributeError):
            print("Exposure time : (not available)")


def set_default_user_set(camera: pylon.InstantCamera, user_set: str) -> None:
    """Set the specified user set as default."""
    try:
        print(f"\nSetting {user_set} as default user set...")
        
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ cameras
            if hasattr(camera, 'UserSetDefault') and camera.UserSetDefault.IsWritable():
                camera.UserSetDefault.Value = user_set
                print(f"Default user set set to: {user_set}")
        else:
            # SFNC 1.x cameras
            if hasattr(camera, 'UserSetDefaultSelector') and camera.UserSetDefaultSelector.IsWritable():
                camera.UserSetDefaultSelector.Value = user_set
                print(f"Default user set selector set to: {user_set}")
    except Exception as e:
        print(f"Error setting default user set: {e}")


def main() -> int:
    """
    Main function demonstrating user set management.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        # Create an instant camera object with the first camera device found
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        # Display camera information
        display_camera_info(camera)
        
        # Open the camera
        camera.Open()
        
        # Check if the camera supports user sets
        if not check_user_set_support(camera):
            camera.Close()
            return 1
        
        # Remember the current default user set selector for restoration later
        old_default_user_set, old_default_user_set_selector = get_current_default_user_set(camera)
        
        # Load default settings
        load_default_settings(camera)
        
        # Configure camera parameters for demonstration
        configure_camera_parameters(camera)
        
        # Save to user set 1
        save_to_user_set(camera, "UserSet1")
        
        # Display default settings
        load_user_set(camera, "Default")
        display_current_settings(camera, "Default settings")
        
        # Display user set 1 settings
        load_user_set(camera, "UserSet1")
        display_current_settings(camera, "User set 1 settings")
        
        # Demonstrate setting user set as default
        set_default_user_set(camera, "UserSet1")
        
        # Restore the original default user set
        restore_default_user_set(camera, old_default_user_set, old_default_user_set_selector)
        
        # Close the camera
        camera.Close()
        
        print("\nUser set management demonstration completed successfully!")
        print("\nNote: When the camera is power-cycled, it will start with the configured default user set.")
        
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
    
    print("=== User Set Management Sample ===")
    print("This sample demonstrates how to save and load camera configurations using user sets.")
    print("WARNING: This sample will overwrite all current settings in user set 1!\n")
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
        sys.exit(1) 