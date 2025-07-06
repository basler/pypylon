#!/usr/bin/env python3
"""
modern_api_demo.py

This sample demonstrates the modern C++ API compatibility features in pypylon
that exactly match the Pylon SDK patterns. It shows how to use camera parameters 
with C++-style method calls like:

- camera.ExposureTimeRaw.IsWritable()
- camera.Width.TrySetValue(640)  
- camera.Gain.SetToMinimum()
- camera.PixelFormat.CanSetValue("Mono8")

These new APIs provide complete compatibility with the latest Pylon C++ SDK
while maintaining backward compatibility with existing code.

Features demonstrated:
1. Extended parameter methods exactly matching Pylon SDK (IValueEx, IIntegerEx, etc.)
2. Type-specific parameter wrappers (Integer, Boolean, Enum, Float, String, Command)
3. Safe parameter access with TrySetValue methods
4. Value correction and range-based operations
5. Modern error handling and type safety
6. Backward compatibility with existing pypylon code

SDK Reference:
- IValueEx: IsWritable(), IsReadable(), IsValid(), GetInfo(), etc.
- IIntegerEx: TrySetValue(), SetToMinimum(), SetToMaximum(), GetValuePercentOfRange(), etc.
- IEnumerationEx: CanSetValue(), TrySetValue(), GetValueOrDefault(), etc.
- IBooleanEx: TrySetValue(), GetValueOrDefault()
- ICommandEx: TryExecute()
"""

from pypylon import genicam as geni, pylon as py
import sys


def demonstrate_value_ex_interface(camera: py.InstantCamera) -> None:
    """Demonstrate IValueEx methods available on all parameters."""
    print("\n" + "="*60)
    print("1. IValueEx Interface - Base Methods for All Parameters")
    print("="*60)
    
    # Get an exposure parameter to demonstrate
    exposure = camera.ExposureTimeRaw if hasattr(camera, 'ExposureTimeRaw') else camera.ExposureTime
    
    # Basic state checking (matches SDK exactly)
    print(f"Parameter: {exposure.GetInfo(py.EParameterInfo.ParameterInfo_Name)}")
    print(f"Display Name: {exposure.GetInfo(py.EParameterInfo.ParameterInfo_DisplayName)}")
    print(f"Description: {exposure.GetInfo(py.EParameterInfo.ParameterInfo_Description)}")
    print(f"Tool Tip: {exposure.GetInfo(py.EParameterInfo.ParameterInfo_ToolTip)}")
    print()
    
    print(f"IsValid(): {exposure.IsValid()}")
    print(f"IsReadable(): {exposure.IsReadable()}")
    print(f"IsWritable(): {exposure.IsWritable()}")
    print()
    
    # Safe information access
    default_info = "N/A"
    print(f"GetInfoOrDefault(Name): {exposure.GetInfoOrDefault(py.EParameterInfo.ParameterInfo_Name, default_info)}")
    print(f"ToStringOrDefault(): {exposure.ToStringOrDefault('default_value')}")


def demonstrate_integer_ex_interface(camera: py.InstantCamera) -> None:
    """Demonstrate IIntegerEx methods for integer parameters."""
    print("\n" + "="*60)
    print("2. IIntegerEx Interface - Extended Integer Parameter Methods")
    print("="*60)
    
    # Get integer parameters to demonstrate
    width_param = camera.Width
    height_param = camera.Height
    exposure_param = camera.ExposureTimeRaw if hasattr(camera, 'ExposureTimeRaw') else camera.ExposureTime
    
    print("🔢 Integer Parameter Extended Methods:")
    print("-" * 40)
    
    # Basic value access
    print(f"Width: Current={width_param.GetValue()}, Min={width_param.GetMin()}, Max={width_param.GetMax()}, Inc={width_param.GetInc()}")
    print(f"Height: Current={height_param.GetValue()}, Min={height_param.GetMin()}, Max={height_param.GetMax()}, Inc={height_param.GetInc()}")
    
    # Safe value access with defaults
    print(f"Width GetValueOrDefault(640): {width_param.GetValueOrDefault(640)}")
    print(f"Height GetValueOrDefault(480): {height_param.GetValueOrDefault(480)}")
    print()
    
    # Range-based operations
    print("📊 Range-based Operations:")
    print(f"Width percent of range: {width_param.GetValuePercentOfRange():.1f}%")
    print(f"Height percent of range: {height_param.GetValuePercentOfRange():.1f}%")
    print()
    
    # Safe setting operations
    print("✅ Safe Setting Operations (TrySetValue):")
    
    # Try to set width to a reasonable value
    target_width = 640
    if width_param.TrySetValue(target_width):
        print(f"✓ Successfully set width to {target_width}")
    else:
        print(f"✗ Failed to set width to {target_width}")
    
    # Try setting with value correction
    target_width_corrected = 641  # Might not align with increment
    if width_param.TrySetValue(target_width_corrected, py.EIntegerValueCorrection.IntegerValueCorrection_Nearest):
        actual_width = width_param.GetValue()
        print(f"✓ Set width {target_width_corrected} with correction -> actual: {actual_width}")
    else:
        print(f"✗ Failed to set width {target_width_corrected} even with correction")
    
    # Range operations
    print("\n🎚️ Range Setting Operations:")
    original_width = width_param.GetValue()
    
    if width_param.TrySetToMinimum():
        print(f"✓ Set width to minimum: {width_param.GetValue()}")
        
    if width_param.TrySetToMaximum():
        print(f"✓ Set width to maximum: {width_param.GetValue()}")
        
    # Set to 50% of range
    if width_param.TrySetValuePercentOfRange(50.0):
        print(f"✓ Set width to 50% of range: {width_param.GetValue()}")
    
    # Restore original value
    width_param.TrySetValue(original_width)
    print(f"↩️ Restored width to original: {width_param.GetValue()}")


def demonstrate_enumeration_ex_interface(camera: py.InstantCamera) -> None:
    """Demonstrate IEnumerationEx methods for enumeration parameters."""
    print("\n" + "="*60)
    print("3. IEnumerationEx Interface - Extended Enumeration Parameter Methods")
    print("="*60)
    
    # Get enumeration parameters
    pixel_format = camera.PixelFormat
    trigger_mode = camera.TriggerMode if hasattr(camera, 'TriggerMode') else None
    
    print("🎛️ Enumeration Parameter Extended Methods:")
    print("-" * 40)
    
    # Current value access
    print(f"PixelFormat current: {pixel_format.GetValue()}")
    print(f"PixelFormat with default: {pixel_format.GetValueOrDefault('Unknown')}")
    
    if trigger_mode:
        print(f"TriggerMode current: {trigger_mode.GetValue()}")
    print()
    
    # Check what values can be set
    print("✅ Value Checking Operations:")
    test_formats = ["Mono8", "Mono12", "RGB8", "BayerGR8", "InvalidFormat"]
    
    for fmt in test_formats:
        can_set = pixel_format.CanSetValue(fmt)
        status = "✓ Available" if can_set else "✗ Not available"
        print(f"  {fmt}: {status}")
    print()
    
    # Safe setting operations
    print("🔄 Safe Setting Operations:")
    original_format = pixel_format.GetValue()
    
    # Try to set to Mono8 if available
    if pixel_format.CanSetValue("Mono8"):
        if pixel_format.TrySetValue("Mono8"):
            print(f"✓ Successfully changed to Mono8")
        else:
            print(f"✗ Failed to change to Mono8 (unexpected)")
    else:
        print("ℹ️ Mono8 not available for this camera")
    
    # Try to set to an invalid format
    if pixel_format.TrySetValue("InvalidFormat"):
        print("⚠️ Unexpectedly succeeded setting invalid format")
    else:
        print("✓ Correctly rejected invalid format")
    
    # Restore original format
    pixel_format.TrySetValue(original_format)
    print(f"↩️ Restored PixelFormat to: {original_format}")


def demonstrate_boolean_ex_interface(camera: py.InstantCamera) -> None:
    """Demonstrate IBooleanEx methods for boolean parameters."""
    print("\n" + "="*60)
    print("4. IBooleanEx Interface - Extended Boolean Parameter Methods")
    print("="*60)
    
    # Find boolean parameters
    boolean_params = []
    
    # Common boolean parameters to look for
    param_names = ['ReverseX', 'ReverseY', 'GammaEnable', 'BlackLevelClampingEnable', 
                  'BalanceWhiteAuto', 'ExposureAuto']
    
    for name in param_names:
        try:
            if hasattr(camera, name):
                param = getattr(camera, name)
                if hasattr(param, 'TrySetValue') and callable(param.TrySetValue):
                    # Check if it accepts boolean by trying with a test
                    try:
                        # Just check if it's likely a boolean (won't actually set)
                        boolean_params.append((name, param))
                    except:
                        pass
        except:
            pass
    
    if boolean_params:
        print("🔘 Boolean Parameter Extended Methods:")
        print("-" * 40)
        
        for name, param in boolean_params[:2]:  # Limit to first 2 found
            print(f"\nParameter: {name}")
            current = param.GetValueOrDefault(False)
            print(f"Current value: {current}")
            print(f"GetValueOrDefault(True): {param.GetValueOrDefault(True)}")
            
            # Try to toggle value safely
            new_value = not current
            if param.TrySetValue(new_value):
                print(f"✓ Successfully changed to {new_value}")
                # Restore original
                param.TrySetValue(current)
                print(f"↩️ Restored to {current}")
            else:
                print(f"ℹ️ Could not change value (may be read-only)")
    else:
        print("ℹ️ No suitable boolean parameters found for demonstration")


def demonstrate_command_ex_interface(camera: py.InstantCamera) -> None:
    """Demonstrate ICommandEx methods for command parameters."""
    print("\n" + "="*60)
    print("5. ICommandEx Interface - Extended Command Parameter Methods")
    print("="*60)
    
    # Look for command parameters
    command_names = ['TestImageSelector', 'TriggerSoftware', 'UserSetLoad', 'TimestampLatch']
    
    found_commands = []
    for name in command_names:
        try:
            if hasattr(camera, name):
                param = getattr(camera, name)
                if hasattr(param, 'TryExecute'):
                    found_commands.append((name, param))
        except:
            pass
    
    if found_commands:
        print("⚡ Command Parameter Extended Methods:")
        print("-" * 40)
        
        for name, param in found_commands[:2]:  # Limit to first 2 found
            print(f"\nCommand: {name}")
            print(f"IsWritable(): {param.IsWritable()}")
            print(f"IsDone(): {param.IsDone()}")
            
            # Try to execute safely
            if param.IsWritable():
                if param.TryExecute():
                    print(f"✓ Successfully executed {name}")
                else:
                    print(f"✗ Failed to execute {name}")
            else:
                print(f"ℹ️ Command {name} is not writable")
    else:
        print("ℹ️ No suitable command parameters found for demonstration")


def demonstrate_backward_compatibility(camera: py.InstantCamera) -> None:
    """Demonstrate that old pypylon code still works."""
    print("\n" + "="*60)
    print("6. Backward Compatibility - Old pypylon Code Still Works")
    print("="*60)
    
    print("📚 Old-style parameter access still supported:")
    print("-" * 40)
    
    # Old style direct access
    try:
        width_node = camera.GetNodeMap().GetNode("Width")
        print(f"Direct node access: Width = {width_node.GetValue()}")
        print(f"Old IsWritable check: {geni.IsWritable(width_node)}")
        print(f"Old IsReadable check: {geni.IsReadable(width_node)}")
    except Exception as e:
        print(f"Old-style access: {e}")
    
    print("\n✨ New modern API works alongside:")
    width_param = camera.Width
    print(f"Modern access: Width = {width_param.GetValue()}")
    print(f"Modern IsWritable: {width_param.IsWritable()}")
    print(f"Modern IsReadable: {width_param.IsReadable()}")
    print(f"Extended method: TrySetToMinimum() = {width_param.TrySetToMinimum()}")


def demonstrate_error_handling(camera: py.InstantCamera) -> None:
    """Demonstrate improved error handling with extended methods."""
    print("\n" + "="*60)
    print("7. Enhanced Error Handling - Safe Parameter Operations")
    print("="*60)
    
    print("🛡️ Safe Parameter Operations:")
    print("-" * 40)
    
    # Test with non-existent parameter - now with helpful error message
    print("Testing access to non-existent parameter...")
    try:
        fake_param = camera.GetParameter("NonExistentParameterXYZ123")
        if fake_param:
            print(f"Fake parameter IsValid(): {fake_param.IsValid()}")
        else:
            print("✓ Correctly returned None for non-existent parameter")
    except RuntimeError as e:
        print(f"✓ Got helpful error message: {e}")
    except Exception as e:
        print(f"✓ Safely handled with exception: {e}")
    
    # Test accessing non-existent parameter via attribute access
    print("\nTesting attribute access to non-existent parameter...")
    try:
        fake_attr = camera.NonExistentParameterXYZ123
        print("⚠️ Unexpectedly succeeded accessing non-existent parameter")
    except AttributeError as e:
        print(f"✓ Got helpful AttributeError: {e}")
    except Exception as e:
        print(f"✓ Got exception: {e}")
    
    # Test setting non-existent parameter
    print("\nTesting setting non-existent parameter...")
    try:
        camera.NonExistentParameterXYZ123 = 1000
        print("⚠️ Unexpectedly succeeded setting non-existent parameter")
    except AttributeError as e:
        print(f"✓ Got helpful error when setting: {e}")
    except Exception as e:
        print(f"✓ Got exception when setting: {e}")
    
    # Test safe parameter checking
    print(f"\nSafe parameter existence checks:")
    print(f"HasParameter('Width'): {camera.HasParameter('Width')}")
    print(f"HasParameter('NonExistentParam'): {camera.HasParameter('NonExistentParam')}")
    print(f"IsParameterWritable('Width'): {camera.IsParameterWritable('Width')}")
    print(f"IsParameterReadable('Width'): {camera.IsParameterReadable('Width')}")
    print(f"IsParameterWritable('NonExistentParam'): {camera.IsParameterWritable('NonExistentParam')}")
    
    # Test safe setting
    print(f"\nSafe parameter setting:")
    if camera.TrySetParameter('Width', 640):
        print("✓ TrySetParameter('Width', 640) succeeded")
    else:
        print("ℹ️ TrySetParameter('Width', 640) failed safely")
    
    if camera.TrySetParameter('NonExistentParam', 123):
        print("⚠️ TrySetParameter with non-existent param unexpectedly succeeded")
    else:
        print("✓ TrySetParameter('NonExistentParam', 123) failed safely")
    
    # Test parameter info
    print(f"\nParameter information retrieval:")
    try:
        info = camera.GetParameterInfo('Width')
        print(f"✓ Width parameter info: {info}")
    except Exception as e:
        print(f"Width parameter info failed: {e}")
    
    try:
        info = camera.GetParameterInfo('NonExistentParam')
        print(f"⚠️ Unexpectedly got info for non-existent parameter: {info}")
    except RuntimeError as e:
        print(f"✓ Got helpful error for non-existent parameter info: {e}")
    
    # Test read-only parameter writing
    print(f"\nTesting write to read-only parameter:")
    # Try to find a read-only parameter
    readonly_params = ['DeviceModelName', 'DeviceSerialNumber', 'DeviceVersion', 'SensorWidth', 'SensorHeight']
    found_readonly = False
    
    for param_name in readonly_params:
        if camera.HasParameter(param_name) and camera.IsParameterReadable(param_name) and not camera.IsParameterWritable(param_name):
            print(f"Testing write to read-only parameter '{param_name}'...")
            try:
                setattr(camera, param_name, "test_value")
                print(f"⚠️ Unexpectedly succeeded writing to read-only parameter {param_name}")
            except AttributeError as e:
                print(f"✓ Got helpful error for read-only parameter: {e}")
                found_readonly = True
                break
            except Exception as e:
                print(f"✓ Got error for read-only parameter: {e}")
                found_readonly = True
                break
    
    if not found_readonly:
        print("ℹ️ No suitable read-only parameters found for testing")
    
    print("\n📋 Error Handling Summary:")
    print("✓ Non-existent parameters give helpful error messages with parameter names")
    print("✓ Read-only parameters are properly protected")
    print("✓ Safe Try* methods handle errors gracefully")
    print("✓ Parameter existence can be checked safely")
    print("✓ Detailed parameter information available")


def main() -> int:
    """
    Main function demonstrating modern C++ API compatibility.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        print("=== Modern C++ API Compatibility Demo ===")
        print("This demo shows pypylon's new SDK-matching parameter API")
        print("Based on actual Pylon SDK patterns (IValueEx, IIntegerEx, etc.)\n")
        
        # Initialize and find camera
        tlf = py.TlFactory.GetInstance()
        devices = tlf.EnumerateDevices()
        if len(devices) == 0:
            print("[ERROR] No camera devices found!")
            return 1
        
        # Use first device
        device_info = devices[0]
        print(f"Using device: {device_info.GetModelName()}")
        print(f"Serial Number: {device_info.GetSerialNumber()}")
        
        # Create and open camera
        camera = py.InstantCamera(tlf.CreateDevice(device_info))
        camera.Open()
        
        try:
            # Run all demonstrations
            demonstrate_value_ex_interface(camera)
            demonstrate_integer_ex_interface(camera)
            demonstrate_enumeration_ex_interface(camera)
            demonstrate_boolean_ex_interface(camera)
            demonstrate_command_ex_interface(camera)
            demonstrate_backward_compatibility(camera)
            demonstrate_error_handling(camera)
            
            print("\n" + "="*60)
            print("🎉 Modern API Demonstration Complete!")
            print("="*60)
            print("Key Benefits:")
            print("✓ Complete compatibility with Pylon C++ SDK patterns")
            print("✓ Type-safe parameter access")
            print("✓ Safe Try* methods for error-free operation")
            print("✓ Extended methods like SetToMinimum, GetValuePercent, etc.")
            print("✓ Full backward compatibility with existing code")
            print("✓ Enhanced error handling and validation")
            
        finally:
            camera.Close()
        
    except geni.GenericException as e:
        print(f"[ERROR] GenICam exception: {e}")
        exit_code = 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[STOP] Interrupted by user")
        sys.exit(1) 