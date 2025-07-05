#!/usr/bin/env python3
"""
parametrize_camera_native_parameter_access.py

This sample demonstrates the 'native' approach for configuring a camera using
direct property access to camera parameters.

The native approach allows direct access to camera parameters as properties
of the InstantCamera object, similar to how C++ BaslerUniversalInstantCamera
works. This is the easiest way to access parameters.

This is equivalent to samples_reference_c++/ParametrizeCamera_NativeParameterAccess/
"""

from typing import Optional
import pypylon.pylon as pylon
from pypylon import genicam


def main() -> int:
    """
    Main function demonstrating native parameter access.
    
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
        
        # Open the camera for parameter access
        camera.Open()
        
        # Get camera device information using native parameter access
        print("Camera Device Information")
        print("=========================")
        
        # Access string parameters directly as properties
        print(f"Vendor           : {camera.DeviceVendorName.Value}")
        print(f"Model            : {camera.DeviceModelName.Value}")
        print(f"Firmware version : {camera.DeviceFirmwareVersion.Value}\n")
        
        # Camera settings
        print("Camera Device Settings")
        print("======================")
        
        # Set the AOI (Area of Interest) using native parameter access
        # On some cameras, the offsets are read-only
        # Therefore, we must use "Try" functions that only perform the action
        # when parameters are writable. Otherwise, we would get an exception.
        
        # Try to set offsets to minimum if they are writable
        try:
            if camera.OffsetX.IsWritable():
                camera.OffsetX.Value = camera.OffsetX.Min
        except (genicam.GenericException, AttributeError):
            # Parameter may not exist or may be read-only
            pass
        
        try:
            if camera.OffsetY.IsWritable():
                camera.OffsetY.Value = camera.OffsetY.Min
        except (genicam.GenericException, AttributeError):
            # Parameter may not exist or may be read-only
            pass
        
        # Some properties have restrictions
        # We can check min/max values and use proper values
        try:
            # Set width to 202 if possible, otherwise use nearest valid value
            if camera.Width.IsWritable():
                desired_width = 202
                # Ensure the value is within bounds and respects increment
                min_width = camera.Width.Min
                max_width = camera.Width.Max
                inc_width = camera.Width.Inc
                
                # Adjust to valid value
                if desired_width < min_width:
                    desired_width = min_width
                elif desired_width > max_width:
                    desired_width = max_width
                
                # Adjust to increment
                if inc_width > 1:
                    desired_width = min_width + ((desired_width - min_width) // inc_width) * inc_width
                
                camera.Width.Value = desired_width
        except (genicam.GenericException, AttributeError):
            pass
        
        try:
            # Set height to 101 if possible, otherwise use nearest valid value
            if camera.Height.IsWritable():
                desired_height = 101
                # Ensure the value is within bounds and respects increment
                min_height = camera.Height.Min
                max_height = camera.Height.Max
                inc_height = camera.Height.Inc
                
                # Adjust to valid value
                if desired_height < min_height:
                    desired_height = min_height
                elif desired_height > max_height:
                    desired_height = max_height
                
                # Adjust to increment
                if inc_height > 1:
                    desired_height = min_height + ((desired_height - min_height) // inc_height) * inc_height
                
                camera.Height.Value = desired_height
        except (genicam.GenericException, AttributeError):
            pass
        
        # Display current AOI settings
        try:
            print(f"OffsetX          : {camera.OffsetX.Value}")
        except (genicam.GenericException, AttributeError):
            print("OffsetX          : (not available)")
        
        try:
            print(f"OffsetY          : {camera.OffsetY.Value}")
        except (genicam.GenericException, AttributeError):
            print("OffsetY          : (not available)")
        
        try:
            print(f"Width            : {camera.Width.Value}")
        except (genicam.GenericException, AttributeError):
            print("Width            : (not available)")
        
        try:
            print(f"Height           : {camera.Height.Value}")
        except (genicam.GenericException, AttributeError):
            print("Height           : (not available)")
        
        # Access the PixelFormat enumeration
        old_pixel_format = None
        try:
            old_pixel_format = camera.PixelFormat.Value
            print(f"Old PixelFormat  : {old_pixel_format}")
            
            # Set the pixel format to Mono8 if available
            if hasattr(camera.PixelFormat, 'SetValue'):
                # Try to set to Mono8
                try:
                    camera.PixelFormat.Value = "Mono8"
                    print(f"New PixelFormat  : {camera.PixelFormat.Value}")
                except genicam.GenericException:
                    print("Could not set PixelFormat to Mono8")
        except (genicam.GenericException, AttributeError):
            print("PixelFormat parameter not available")
        
        # Set the new gain to 50% -> Min + ((Max-Min) / 2)
        #
        # Note: Some newer camera models may have auto functions enabled.
        #       To be able to set the gain value to a specific value
        #       the Gain Auto function must be disabled first.
        
        # Try to disable gain auto function if it exists
        try:
            if hasattr(camera, 'GainAuto') and camera.GainAuto.IsWritable():
                camera.GainAuto.Value = "Off"
        except (genicam.GenericException, AttributeError):
            pass
        
        # Check to see which Standard Feature Naming Convention (SFNC) is used by the camera device
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # Access the Gain float parameter. This is available for USB camera devices.
            # USB camera devices are compliant to SFNC version 2.0.
            try:
                if hasattr(camera, 'Gain') and camera.Gain.IsWritable():
                    # Set gain to 50% of range
                    gain_min = camera.Gain.Min
                    gain_max = camera.Gain.Max
                    gain_50_percent = gain_min + (gain_max - gain_min) * 0.5
                    camera.Gain.Value = gain_50_percent
                    print(f"Gain (50%)       : {camera.Gain.Value:.2f} "
                          f"(Min: {gain_min:.2f}; Max: {gain_max:.2f})")
            except (genicam.GenericException, AttributeError) as e:
                print(f"Gain parameter access failed: {e}")
        else:
            # Access the GainRaw integer parameter. This is available for GigE camera devices.
            try:
                if hasattr(camera, 'GainRaw') and camera.GainRaw.IsWritable():
                    # Set gain to 50% of range
                    gain_min = camera.GainRaw.Min
                    gain_max = camera.GainRaw.Max
                    gain_inc = camera.GainRaw.Inc
                    gain_50_percent = gain_min + ((gain_max - gain_min) // 2)
                    # Adjust to increment
                    if gain_inc > 1:
                        gain_50_percent = gain_min + ((gain_50_percent - gain_min) // gain_inc) * gain_inc
                    camera.GainRaw.Value = gain_50_percent
                    print(f"Gain (50%)       : {camera.GainRaw.Value} "
                          f"(Min: {gain_min}; Max: {gain_max}; Inc: {gain_inc})")
            except (genicam.GenericException, AttributeError) as e:
                print(f"GainRaw parameter access failed: {e}")
        
        # Restore the old pixel format if we changed it
        if old_pixel_format is not None:
            try:
                camera.PixelFormat.Value = old_pixel_format
            except (genicam.GenericException, AttributeError):
                pass
        
        # Close the camera
        camera.Close()
        
        print("\nNative parameter access demonstration completed successfully!")
        
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
    
    print("=== Native Parameter Access Sample ===")
    print("This sample demonstrates native parameter access using direct property access.")
    print("Camera parameters are accessed as properties of the InstantCamera object.\n")
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
        sys.exit(1) 