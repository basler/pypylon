#!/usr/bin/env python3
"""
parametrize_camera_generic_parameter_access.py

This sample demonstrates the 'generic' approach for configuring a camera using
the GenApi nodemaps represented by the INodeMap interface.

The generic approach uses string-based parameter names to access camera parameters
through the node map, similar to how the C++ pylon API works with CStringParameter,
CIntegerParameter, etc.

This is equivalent to samples_reference_c++/ParametrizeCamera_GenericParameterAccess/
"""

from typing import Optional
import pypylon.pylon as pylon
from pypylon import genicam


def main() -> int:
    """
    Main function demonstrating generic parameter access.
    
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
        
        # Get the node map for parameter access
        nodemap = camera.GetNodeMap()
        
        # Open the camera for parameter access
        camera.Open()
        
        # Get camera device information using generic parameter access
        print("Camera Device Information")
        print("=========================")
        
        # Access string parameters using generic approach
        vendor_name = pylon.CStringParameter(nodemap, "DeviceVendorName")
        model_name = pylon.CStringParameter(nodemap, "DeviceModelName")
        firmware_version = pylon.CStringParameter(nodemap, "DeviceFirmwareVersion")
        
        print(f"Vendor           : {vendor_name.GetValue()}")
        print(f"Model            : {model_name.GetValue()}")
        print(f"Firmware version : {firmware_version.GetValue()}\n")
        
        # Camera settings
        print("Camera Device Settings")
        print("======================")
        
        # Set the AOI (Area of Interest) using generic parameter access
        # Get the integer nodes describing the AOI
        offset_x = pylon.CIntegerParameter(nodemap, "OffsetX")
        offset_y = pylon.CIntegerParameter(nodemap, "OffsetY")
        width = pylon.CIntegerParameter(nodemap, "Width")
        height = pylon.CIntegerParameter(nodemap, "Height")
        
        # On some cameras, the offsets are read-only
        # Therefore, we must use "Try" functions that only perform the action
        # when parameters are writable. Otherwise, we would get an exception.
        offset_x.TrySetToMinimum()
        offset_y.TrySetToMinimum()
        
        # Some properties have restrictions
        # We use API functions that automatically perform value corrections
        # Alternatively, you can use GetInc() / GetMin() / GetMax() to make sure you set a valid value
        width.SetValue(202, pylon.IntegerValueCorrection_Nearest)
        height.SetValue(101, pylon.IntegerValueCorrection_Nearest)
        
        print(f"OffsetX          : {offset_x.GetValue()}")
        print(f"OffsetY          : {offset_y.GetValue()}")
        print(f"Width            : {width.GetValue()}")
        print(f"Height           : {height.GetValue()}")
        
        # Access the PixelFormat enumeration type node
        pixel_format = pylon.CEnumParameter(nodemap, "PixelFormat")
        
        # Remember the current pixel format
        old_pixel_format = pixel_format.GetValue()
        print(f"Old PixelFormat  : {old_pixel_format}")
        
        # Set the pixel format to Mono8 if available
        if pixel_format.CanSetValue("Mono8"):
            pixel_format.SetValue("Mono8")
            print(f"New PixelFormat  : {pixel_format.GetValue()}")
        
        # Set the new gain to 50% -> Min + ((Max-Min) / 2)
        #
        # Note: Some newer camera models may have auto functions enabled.
        #       To be able to set the gain value to a specific value
        #       the Gain Auto function must be disabled first.
        
        # Access the enumeration type node GainAuto
        # We use a "Try" function that only performs the action if the parameter is writable
        gain_auto = pylon.CEnumParameter(nodemap, "GainAuto")
        gain_auto.TrySetValue("Off")
        
        # Check to see which Standard Feature Naming Convention (SFNC) is used by the camera device
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # Access the Gain float type node. This node is available for USB camera devices.
            # USB camera devices are compliant to SFNC version 2.0.
            try:
                gain = pylon.CFloatParameter(nodemap, "Gain")
                if gain.TrySetValuePercentOfRange(50.0):
                    print(f"Gain (50%)       : {gain.GetValue():.2f} "
                          f"(Min: {gain.GetMin():.2f}; Max: {gain.GetMax():.2f})")
            except genicam.GenericException as e:
                print(f"Gain parameter access failed: {e}")
        else:
            # Access the GainRaw integer type node. This node is available for GigE camera devices.
            try:
                gain_raw = pylon.CIntegerParameter(nodemap, "GainRaw")
                if gain_raw.TrySetValuePercentOfRange(50.0):
                    print(f"Gain (50%)       : {gain_raw.GetValue()} "
                          f"(Min: {gain_raw.GetMin()}; Max: {gain_raw.GetMax()}; Inc: {gain_raw.GetInc()})")
            except genicam.GenericException as e:
                print(f"GainRaw parameter access failed: {e}")
        
        # Restore the old pixel format
        pixel_format.SetValue(old_pixel_format)
        
        # Close the camera
        camera.Close()
        
        print("\nGeneric parameter access demonstration completed successfully!")
        
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
    
    print("=== Generic Parameter Access Sample ===")
    print("This sample demonstrates generic parameter access using string-based node names.")
    print("The camera will be configured using the INodeMap interface.\n")
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
        sys.exit(1) 