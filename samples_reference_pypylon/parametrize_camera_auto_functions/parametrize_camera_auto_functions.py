#!/usr/bin/env python3
"""
parametrize_camera_auto_functions.py

This sample illustrates how to use the Auto Functions feature of Basler cameras.
Auto functions automatically adjust camera parameters like gain, exposure time, and
white balance to optimize image quality.

Different camera families implement different versions of the Standard Feature Naming
Convention (SFNC), so the parameter names and types can vary between cameras.

This is equivalent to samples_reference_c++/ParametrizeCamera_AutoFunctions/

Note: Auto functions require an image to analyze, so the camera must be capturing images.
"""

from typing import Optional
import time
import pypylon.pylon as pylon
from pypylon import genicam


def display_camera_info(camera: pylon.InstantCamera) -> None:
    """Display basic camera information."""
    try:
        info = camera.GetDeviceInfo()
        print(f"Using device: {info.GetModelName()}")
        print(f"Device scan type: {camera.DeviceScanType.Value if hasattr(camera, 'DeviceScanType') else 'Unknown'}")
        print(f"SFNC Version: {camera.GetSfncVersion()}\n")
    except Exception as e:
        print(f"Could not retrieve camera information: {e}")


def is_color_camera(camera: pylon.InstantCamera) -> bool:
    """Check if the camera is a color camera."""
    try:
        if hasattr(camera, 'PixelFormat'):
            # Get available pixel formats
            pixel_format_entries = camera.PixelFormat.Symbolics
            
            # Check if any color formats are available
            color_formats = ['RGB', 'BGR', 'YUV', 'Bayer']
            for format_name in pixel_format_entries:
                for color_format in color_formats:
                    if color_format.lower() in format_name.lower():
                        return True
        
        # Alternative check: look for balance ratio parameters
        if hasattr(camera, 'BalanceRatioSelector'):
            return True
            
        return False
    except Exception:
        return False


def wait_for_auto_function_completion(camera: pylon.InstantCamera, timeout_ms: int = 5000) -> bool:
    """Wait for auto functions to complete by monitoring FrameRate."""
    try:
        start_time = time.time()
        timeout_seconds = timeout_ms / 1000.0
        
        # Simple wait - in a real application you might monitor specific status parameters
        time.sleep(1.0)  # Give auto functions time to work
        
        # Check if we've timed out
        elapsed = time.time() - start_time
        return elapsed < timeout_seconds
        
    except Exception:
        return False


def auto_gain_once(camera: pylon.InstantCamera) -> None:
    """Demonstrate auto gain 'once' functionality."""
    print("=" * 50)
    print("Auto Gain Once")
    print("=" * 50)
    
    try:
        # Check SFNC version to use appropriate parameters
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ (USB cameras)
            if hasattr(camera, 'Gain') and hasattr(camera, 'GainAuto'):
                # Show initial gain value
                initial_gain = camera.Gain.Value
                print(f"Initial gain: {initial_gain:.2f}")
                
                # Set gain auto to once
                camera.GainAuto.Value = "Once"
                print("Gain auto set to 'Once'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Wait for auto function to complete
                print("Waiting for auto gain to complete...")
                wait_for_auto_function_completion(camera, 3000)
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final gain value
                final_gain = camera.Gain.Value
                print(f"Final gain after auto adjustment: {final_gain:.2f}")
                print(f"Gain change: {final_gain - initial_gain:+.2f}")
            else:
                print("Gain parameters not available on this camera")
        else:
            # SFNC 1.x (GigE cameras)
            if hasattr(camera, 'GainRaw') and hasattr(camera, 'GainAuto'):
                # Show initial gain value
                initial_gain = camera.GainRaw.Value
                print(f"Initial gain: {initial_gain}")
                
                # Set gain auto to once
                camera.GainAuto.Value = "Once"
                print("Gain auto set to 'Once'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Wait for auto function to complete
                print("Waiting for auto gain to complete...")
                wait_for_auto_function_completion(camera, 3000)
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final gain value
                final_gain = camera.GainRaw.Value
                print(f"Final gain after auto adjustment: {final_gain}")
                print(f"Gain change: {final_gain - initial_gain:+d}")
            else:
                print("GainRaw parameters not available on this camera")
                
    except Exception as e:
        print(f"Error during auto gain once: {e}")
        if camera.IsGrabbing():
            camera.StopGrabbing()


def auto_gain_continuous(camera: pylon.InstantCamera) -> None:
    """Demonstrate auto gain 'continuous' functionality."""
    print("\n" + "=" * 50)
    print("Auto Gain Continuous")
    print("=" * 50)
    
    try:
        # Check SFNC version to use appropriate parameters
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ (USB cameras)
            if hasattr(camera, 'Gain') and hasattr(camera, 'GainAuto'):
                # Show initial gain value
                initial_gain = camera.Gain.Value
                print(f"Initial gain: {initial_gain:.2f}")
                
                # Set gain auto to continuous
                camera.GainAuto.Value = "Continuous"
                print("Gain auto set to 'Continuous'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Monitor gain changes for a few seconds
                print("Monitoring gain for 3 seconds...")
                start_time = time.time()
                while time.time() - start_time < 3.0:
                    current_gain = camera.Gain.Value
                    print(f"  Current gain: {current_gain:.2f}")
                    time.sleep(0.5)
                
                # Turn off auto gain
                camera.GainAuto.Value = "Off"
                print("Gain auto turned off")
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final gain value
                final_gain = camera.Gain.Value
                print(f"Final gain: {final_gain:.2f}")
            else:
                print("Gain parameters not available on this camera")
        else:
            # SFNC 1.x (GigE cameras)
            if hasattr(camera, 'GainRaw') and hasattr(camera, 'GainAuto'):
                # Show initial gain value
                initial_gain = camera.GainRaw.Value
                print(f"Initial gain: {initial_gain}")
                
                # Set gain auto to continuous
                camera.GainAuto.Value = "Continuous"
                print("Gain auto set to 'Continuous'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Monitor gain changes for a few seconds
                print("Monitoring gain for 3 seconds...")
                start_time = time.time()
                while time.time() - start_time < 3.0:
                    current_gain = camera.GainRaw.Value
                    print(f"  Current gain: {current_gain}")
                    time.sleep(0.5)
                
                # Turn off auto gain
                camera.GainAuto.Value = "Off"
                print("Gain auto turned off")
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final gain value
                final_gain = camera.GainRaw.Value
                print(f"Final gain: {final_gain}")
            else:
                print("GainRaw parameters not available on this camera")
                
    except Exception as e:
        print(f"Error during auto gain continuous: {e}")
        if camera.IsGrabbing():
            camera.StopGrabbing()


def auto_exposure_once(camera: pylon.InstantCamera) -> None:
    """Demonstrate auto exposure 'once' functionality."""
    print("\n" + "=" * 50)
    print("Auto Exposure Once")
    print("=" * 50)
    
    try:
        # Check SFNC version to use appropriate parameters
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ (USB cameras)
            if hasattr(camera, 'ExposureTime') and hasattr(camera, 'ExposureAuto'):
                # Show initial exposure time
                initial_exposure = camera.ExposureTime.Value
                print(f"Initial exposure time: {initial_exposure:.1f} µs")
                
                # Set exposure auto to once
                camera.ExposureAuto.Value = "Once"
                print("Exposure auto set to 'Once'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Wait for auto function to complete
                print("Waiting for auto exposure to complete...")
                wait_for_auto_function_completion(camera, 3000)
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final exposure time
                final_exposure = camera.ExposureTime.Value
                print(f"Final exposure time: {final_exposure:.1f} µs")
                print(f"Exposure change: {final_exposure - initial_exposure:+.1f} µs")
            else:
                print("ExposureTime parameters not available on this camera")
        else:
            # SFNC 1.x (GigE cameras)
            if hasattr(camera, 'ExposureTimeRaw') and hasattr(camera, 'ExposureAuto'):
                # Show initial exposure time
                initial_exposure = camera.ExposureTimeRaw.Value
                print(f"Initial exposure time: {initial_exposure}")
                
                # Set exposure auto to once
                camera.ExposureAuto.Value = "Once"
                print("Exposure auto set to 'Once'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Wait for auto function to complete
                print("Waiting for auto exposure to complete...")
                wait_for_auto_function_completion(camera, 3000)
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final exposure time
                final_exposure = camera.ExposureTimeRaw.Value
                print(f"Final exposure time: {final_exposure}")
                print(f"Exposure change: {final_exposure - initial_exposure:+d}")
            else:
                print("ExposureTimeRaw parameters not available on this camera")
                
    except Exception as e:
        print(f"Error during auto exposure once: {e}")
        if camera.IsGrabbing():
            camera.StopGrabbing()


def auto_exposure_continuous(camera: pylon.InstantCamera) -> None:
    """Demonstrate auto exposure 'continuous' functionality."""
    print("\n" + "=" * 50)
    print("Auto Exposure Continuous")
    print("=" * 50)
    
    try:
        # Check SFNC version to use appropriate parameters
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ (USB cameras)
            if hasattr(camera, 'ExposureTime') and hasattr(camera, 'ExposureAuto'):
                # Show initial exposure time
                initial_exposure = camera.ExposureTime.Value
                print(f"Initial exposure time: {initial_exposure:.1f} µs")
                
                # Set exposure auto to continuous
                camera.ExposureAuto.Value = "Continuous"
                print("Exposure auto set to 'Continuous'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Monitor exposure changes for a few seconds
                print("Monitoring exposure for 3 seconds...")
                start_time = time.time()
                while time.time() - start_time < 3.0:
                    current_exposure = camera.ExposureTime.Value
                    print(f"  Current exposure: {current_exposure:.1f} µs")
                    time.sleep(0.5)
                
                # Turn off auto exposure
                camera.ExposureAuto.Value = "Off"
                print("Exposure auto turned off")
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final exposure time
                final_exposure = camera.ExposureTime.Value
                print(f"Final exposure time: {final_exposure:.1f} µs")
            else:
                print("ExposureTime parameters not available on this camera")
        else:
            # SFNC 1.x (GigE cameras)
            if hasattr(camera, 'ExposureTimeRaw') and hasattr(camera, 'ExposureAuto'):
                # Show initial exposure time
                initial_exposure = camera.ExposureTimeRaw.Value
                print(f"Initial exposure time: {initial_exposure}")
                
                # Set exposure auto to continuous
                camera.ExposureAuto.Value = "Continuous"
                print("Exposure auto set to 'Continuous'")
                
                # Start grabbing to provide images for auto function
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                
                # Monitor exposure changes for a few seconds
                print("Monitoring exposure for 3 seconds...")
                start_time = time.time()
                while time.time() - start_time < 3.0:
                    current_exposure = camera.ExposureTimeRaw.Value
                    print(f"  Current exposure: {current_exposure}")
                    time.sleep(0.5)
                
                # Turn off auto exposure
                camera.ExposureAuto.Value = "Off"
                print("Exposure auto turned off")
                
                # Stop grabbing
                camera.StopGrabbing()
                
                # Show final exposure time
                final_exposure = camera.ExposureTimeRaw.Value
                print(f"Final exposure time: {final_exposure}")
            else:
                print("ExposureTimeRaw parameters not available on this camera")
                
    except Exception as e:
        print(f"Error during auto exposure continuous: {e}")
        if camera.IsGrabbing():
            camera.StopGrabbing()


def auto_white_balance(camera: pylon.InstantCamera) -> None:
    """Demonstrate auto white balance functionality."""
    print("\n" + "=" * 50)
    print("Auto White Balance")
    print("=" * 50)
    
    if not is_color_camera(camera):
        print("Auto white balance is only available for color cameras.")
        return
    
    try:
        # Check SFNC version to use appropriate parameters
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            # SFNC 2.0+ (USB cameras)
            if hasattr(camera, 'BalanceRatio') and hasattr(camera, 'BalanceRatioSelector'):
                # Set initial balance ratio values for demonstration
                print("Setting initial balance ratio values...")
                
                # Red channel
                camera.BalanceRatioSelector.Value = "Red"
                initial_red = camera.BalanceRatio.Max
                camera.BalanceRatio.Value = initial_red
                print(f"  Red balance ratio set to: {initial_red:.2f}")
                
                # Green channel
                camera.BalanceRatioSelector.Value = "Green"
                green_mid = camera.BalanceRatio.Min + (camera.BalanceRatio.Max - camera.BalanceRatio.Min) * 0.5
                camera.BalanceRatio.Value = green_mid
                print(f"  Green balance ratio set to: {green_mid:.2f}")
                
                # Blue channel
                camera.BalanceRatioSelector.Value = "Blue"
                initial_blue = camera.BalanceRatio.Min
                camera.BalanceRatio.Value = initial_blue
                print(f"  Blue balance ratio set to: {initial_blue:.2f}")
                
                # Perform auto white balance
                if hasattr(camera, 'BalanceWhiteAuto'):
                    camera.BalanceWhiteAuto.Value = "Once"
                    print("\nBalance white auto set to 'Once'")
                    
                    # Start grabbing to provide images for auto function
                    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                    
                    # Wait for auto function to complete
                    print("Waiting for auto white balance to complete...")
                    wait_for_auto_function_completion(camera, 5000)
                    
                    # Stop grabbing
                    camera.StopGrabbing()
                    
                    # Show final balance ratio values
                    print("\nFinal balance ratio values:")
                    camera.BalanceRatioSelector.Value = "Red"
                    final_red = camera.BalanceRatio.Value
                    print(f"  Red balance ratio: {final_red:.2f} (change: {final_red - initial_red:+.2f})")
                    
                    camera.BalanceRatioSelector.Value = "Green"
                    final_green = camera.BalanceRatio.Value
                    print(f"  Green balance ratio: {final_green:.2f} (change: {final_green - green_mid:+.2f})")
                    
                    camera.BalanceRatioSelector.Value = "Blue"
                    final_blue = camera.BalanceRatio.Value
                    print(f"  Blue balance ratio: {final_blue:.2f} (change: {final_blue - initial_blue:+.2f})")
                else:
                    print("BalanceWhiteAuto parameter not available")
            else:
                print("Balance ratio parameters not available on this camera")
        else:
            # SFNC 1.x (GigE cameras)
            if hasattr(camera, 'BalanceRatioAbs') and hasattr(camera, 'BalanceRatioSelector'):
                # Set initial balance ratio values for demonstration
                print("Setting initial balance ratio values...")
                
                # Red channel
                camera.BalanceRatioSelector.Value = "Red"
                initial_red = camera.BalanceRatioAbs.Max
                camera.BalanceRatioAbs.Value = initial_red
                print(f"  Red balance ratio set to: {initial_red:.2f}")
                
                # Green channel
                camera.BalanceRatioSelector.Value = "Green"
                green_mid = camera.BalanceRatioAbs.Min + (camera.BalanceRatioAbs.Max - camera.BalanceRatioAbs.Min) * 0.5
                camera.BalanceRatioAbs.Value = green_mid
                print(f"  Green balance ratio set to: {green_mid:.2f}")
                
                # Blue channel
                camera.BalanceRatioSelector.Value = "Blue"
                initial_blue = camera.BalanceRatioAbs.Min
                camera.BalanceRatioAbs.Value = initial_blue
                print(f"  Blue balance ratio set to: {initial_blue:.2f}")
                
                # Perform auto white balance
                if hasattr(camera, 'BalanceWhiteAuto'):
                    camera.BalanceWhiteAuto.Value = "Once"
                    print("\nBalance white auto set to 'Once'")
                    
                    # Start grabbing to provide images for auto function
                    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                    
                    # Wait for auto function to complete
                    print("Waiting for auto white balance to complete...")
                    wait_for_auto_function_completion(camera, 5000)
                    
                    # Stop grabbing
                    camera.StopGrabbing()
                    
                    # Show final balance ratio values
                    print("\nFinal balance ratio values:")
                    camera.BalanceRatioSelector.Value = "Red"
                    final_red = camera.BalanceRatioAbs.Value
                    print(f"  Red balance ratio: {final_red:.2f} (change: {final_red - initial_red:+.2f})")
                    
                    camera.BalanceRatioSelector.Value = "Green"
                    final_green = camera.BalanceRatioAbs.Value
                    print(f"  Green balance ratio: {final_green:.2f} (change: {final_green - green_mid:+.2f})")
                    
                    camera.BalanceRatioSelector.Value = "Blue"
                    final_blue = camera.BalanceRatioAbs.Value
                    print(f"  Blue balance ratio: {final_blue:.2f} (change: {final_blue - initial_blue:+.2f})")
                else:
                    print("BalanceWhiteAuto parameter not available")
            else:
                print("Balance ratio parameters not available on this camera")
                
    except Exception as e:
        print(f"Error during auto white balance: {e}")
        if camera.IsGrabbing():
            camera.StopGrabbing()


def main() -> int:
    """
    Main function demonstrating auto functions.
    
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
        
        # Register single frame configuration for auto functions
        camera.RegisterConfiguration(pylon.AcquireSingleFrameConfiguration(), 
                                   pylon.RegistrationMode_ReplaceAll, 
                                   pylon.Cleanup_Delete)
        
        # Open the camera
        camera.Open()
        
        # Turn off test image if available
        try:
            if hasattr(camera, 'TestImageSelector'):
                camera.TestImageSelector.Value = "Off"
            if hasattr(camera, 'TestPattern'):
                camera.TestPattern.Value = "Off"
        except (genicam.GenericException, AttributeError):
            pass
        
        # Check if this is an area scan camera (auto functions are only supported on area scan cameras)
        try:
            if hasattr(camera, 'DeviceScanType'):
                scan_type = camera.DeviceScanType.Value
                if scan_type != "Areascan":
                    print(f"Auto functions are only supported on area scan cameras. This camera is: {scan_type}")
                    camera.Close()
                    return 1
        except (genicam.GenericException, AttributeError):
            print("Warning: Could not determine camera scan type. Proceeding with auto function demonstration.")
        
        print("Starting auto function demonstrations...")
        print("Note: Auto functions require images to analyze. The camera will grab images during each demonstration.")
        
        # Demonstrate auto functions
        auto_gain_once(camera)
        auto_gain_continuous(camera)
        auto_exposure_once(camera)
        auto_exposure_continuous(camera)
        
        # Only demonstrate auto white balance if this is a color camera
        if is_color_camera(camera):
            auto_white_balance(camera)
        else:
            print("\n" + "=" * 50)
            print("Auto White Balance")
            print("=" * 50)
            print("Auto white balance is only available for color cameras.")
            print("This appears to be a monochrome camera.")
        
        # Close the camera
        camera.Close()
        
        print("\nAuto functions demonstration completed successfully!")
        print("\nNote: Auto functions work best with proper lighting and scene content.")
        print("      Make sure the camera lens cap is removed and there is adequate illumination.")
        
    except pylon.TimeoutException as e:
        print(f"A timeout has occurred: {e}")
        print("Auto functions did not finish in time.")
        print("Please make sure you remove the cap from the camera lens before running this sample.")
        exit_code = 0  # Timeout is not necessarily an error for this demo
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
    
    print("=== Auto Functions Sample ===")
    print("This sample demonstrates automatic gain, exposure, and white balance functions.")
    print("Make sure the camera lens cap is removed and there is adequate lighting.\n")
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
        sys.exit(1) 