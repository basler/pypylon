#!/usr/bin/env python3
"""
device_removal_handling.py

This sample demonstrates how to handle device removal and reconnection events
when using Basler cameras. It shows how to implement robust camera applications
that can gracefully handle camera disconnections and automatic reconnections.

This sample illustrates:
- Device removal detection and handling
- Automatic device reconnection
- Proper resource cleanup during disconnection
- Event-driven device management
- Recovery strategies for interrupted operations

This is equivalent to samples_reference_c++/DeviceRemovalHandling/

Note: To test device removal, you can disconnect and reconnect the camera
USB cable or network cable during execution.
"""

from typing import Optional
import time
import threading
import pypylon.pylon as pylon
from pypylon import genicam as geni, pylon as py


class DeviceRemovalHandler:
    """Handles device removal and reconnection events."""
    
    def __init__(self, device_info: py.DeviceInfo):
        self.device_info = device_info
        self.camera: Optional[py.InstantCamera] = None
        self.is_connected = False
        self.is_running = False
        self.reconnect_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
        # Statistics
        self.images_grabbed = 0
        self.connection_lost_count = 0
        self.reconnection_count = 0
        
    def connect(self) -> bool:
        """Connect to the camera device."""
        try:
            with self.lock:
                if self.camera is not None:
                    return True
                
                print(f"Connecting to {self.device_info.GetModelName()}...")
                
                # Create camera instance
                tlf = py.TlFactory.GetInstance()
                self.camera = py.InstantCamera(tlf.CreateDevice(self.device_info))
                
                # Register configuration for software triggering
                self.camera.RegisterConfiguration(py.SoftwareTriggerConfiguration(), 
                                                py.RegistrationMode_ReplaceAll, 
                                                py.Cleanup_Delete)
                
                # Open the camera
                self.camera.Open()
                
                # Set camera parameters for demonstration
                self.configure_camera()
                
                self.is_connected = True
                print(f"[SUCCESS] Connected to {self.device_info.GetModelName()}")
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            self.cleanup()
            return False
    
    def configure_camera(self) -> None:
        """Configure camera parameters using modern C++ API style."""
        try:
            if self.camera is None:
                return
            
            print("🔧 Configuring camera with modern API...")
            
            # Set exposure time using SDK-matching extended methods
            exposure_configured = False
            
            # Try ExposureTime first (SFNC 2.0+ style)
            if hasattr(self.camera, 'ExposureTime') and self.camera.ExposureTime.IsWritable():
                exposure = self.camera.ExposureTime
                target_exposure = 10000.0  # 10ms in microseconds
                
                # Safe setting with value correction (exactly like SDK)
                if exposure.TrySetValue(target_exposure, py.EIntegerValueCorrection.IntegerValueCorrection_Nearest if hasattr(py, 'EIntegerValueCorrection') else None):
                    print(f"✓ Set ExposureTime to {exposure.GetValue()} µs using TrySetValue with correction")
                    exposure_configured = True
                else:
                    # Fallback to regular TrySetValue
                    if exposure.TrySetValue(target_exposure):
                        print(f"✓ Set ExposureTime to {exposure.GetValue()} µs using TrySetValue")
                        exposure_configured = True
            
            # Try ExposureTimeRaw as fallback (SFNC 1.x style)
            elif hasattr(self.camera, 'ExposureTimeRaw') and self.camera.ExposureTimeRaw.IsWritable():
                exposure = self.camera.ExposureTimeRaw
                target_exposure = 10000
                
                # Demonstrate range-based setting
                print(f"ExposureTimeRaw range: {exposure.GetMin()} - {exposure.GetMax()}")
                
                # Safe setting with automatic value correction
                if exposure.TrySetValue(target_exposure, py.EIntegerValueCorrection.IntegerValueCorrection_Nearest if hasattr(py, 'EIntegerValueCorrection') else None):
                    print(f"✓ Set ExposureTimeRaw to {exposure.GetValue()} using TrySetValue with correction")
                    exposure_configured = True
                elif exposure.TrySetValue(target_exposure):
                    print(f"✓ Set ExposureTimeRaw to {exposure.GetValue()} using TrySetValue")
                    exposure_configured = True
                else:
                    # Try setting to 25% of the range
                    if exposure.TrySetValuePercentOfRange and exposure.TrySetValuePercentOfRange(25.0):
                        print(f"✓ Set ExposureTimeRaw to 25% of range: {exposure.GetValue()}")
                        exposure_configured = True
            
            if not exposure_configured:
                print("⚠️ Could not configure exposure time")
            
            # Set image dimensions using extended methods
            if hasattr(self.camera, 'Width') and self.camera.Width.IsWritable():
                width = self.camera.Width
                target_width = 640
                
                # Demonstrate GetValueOrDefault (SDK-matching method)
                current_width = width.GetValueOrDefault(width.GetMin())
                print(f"Current Width: {current_width} (min: {width.GetMin()}, max: {width.GetMax()})")
                
                # Safe setting with range checking
                if target_width >= width.GetMin() and target_width <= width.GetMax():
                    if width.TrySetValue(target_width):
                        print(f"✓ Set Width to {width.GetValue()}")
                    else:
                        print(f"⚠️ Failed to set Width to {target_width}")
                else:
                    # Set to 50% of range instead
                    if width.TrySetValuePercentOfRange and width.TrySetValuePercentOfRange(50.0):
                        print(f"✓ Set Width to 50% of range: {width.GetValue()}")
            
            # Configure pixel format using enumeration extended methods
            if hasattr(self.camera, 'PixelFormat'):
                pixel_format = self.camera.PixelFormat
                print(f"Current PixelFormat: {pixel_format.GetValueOrDefault('Unknown')}")
                
                # Try to set to Mono8 if available (SDK-matching method)
                if pixel_format.CanSetValue and pixel_format.CanSetValue("Mono8"):
                    if pixel_format.TrySetValue("Mono8"):
                        print(f"✓ Set PixelFormat to Mono8")
                    else:
                        print("⚠️ Failed to set PixelFormat to Mono8")
                else:
                    print("ℹ️ Mono8 not available, keeping current format")
            
            # Configure gain if available
            if hasattr(self.camera, 'Gain') and self.camera.Gain.IsWritable():
                gain = self.camera.Gain
                print(f"Gain range: {gain.GetMin()} - {gain.GetMax()}")
                
                # Set gain to minimum for best image quality
                if gain.TrySetToMinimum and gain.TrySetToMinimum():
                    print(f"✓ Set Gain to minimum: {gain.GetValue()}")
                elif gain.TrySetValue and gain.TrySetValue(gain.GetMin()):
                    print(f"✓ Set Gain to minimum: {gain.GetValue()}")
            elif hasattr(self.camera, 'GainRaw') and self.camera.GainRaw.IsWritable():
                gain = self.camera.GainRaw
                print(f"GainRaw range: {gain.GetMin()} - {gain.GetMax()}")
                
                # Set gain to minimum using SDK-matching method
                if gain.TrySetToMinimum and gain.TrySetToMinimum():
                    print(f"✓ Set GainRaw to minimum: {gain.GetValue()}")
            
            # Configure network parameters for GigE cameras using extended methods
            if hasattr(self.camera, 'GevSCPSPacketSize') and self.camera.GevSCPSPacketSize.IsWritable():
                packet_size = self.camera.GevSCPSPacketSize
                
                # Get parameter information using SDK-matching methods
                if hasattr(packet_size, 'GetInfo'):
                    param_name = packet_size.GetInfo(py.EParameterInfo.ParameterInfo_Name if hasattr(py, 'EParameterInfo') else 0)
                    print(f"Configuring {param_name}")
                
                target_packet_size = 1500
                
                # Safe setting with fallback
                if packet_size.TrySetValue and packet_size.TrySetValue(target_packet_size):
                    print(f"✓ Set packet size to {packet_size.GetValue()}")
                elif packet_size.GetValueOrDefault and packet_size.TrySetValue:
                    # Try setting to current value + 100 as a test
                    current = packet_size.GetValueOrDefault(1500)
                    if packet_size.TrySetValue(current):
                        print(f"✓ Confirmed packet size: {packet_size.GetValue()}")
                
            # Disable auto functions using boolean extended methods
            for auto_param_name in ['ExposureAuto', 'GainAuto', 'BalanceWhiteAuto']:
                if hasattr(self.camera, auto_param_name):
                    auto_param = getattr(self.camera, auto_param_name)
                    if auto_param.IsWritable():
                        # Try to set to "Off" for enumeration, False for boolean
                        if hasattr(auto_param, 'CanSetValue') and auto_param.CanSetValue("Off"):
                            if auto_param.TrySetValue("Off"):
                                print(f"✓ Set {auto_param_name} to Off")
                        elif hasattr(auto_param, 'TrySetValue'):
                            if auto_param.TrySetValue(False):
                                print(f"✓ Set {auto_param_name} to False")
            
            print("✅ Camera configuration completed using modern API")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not fully configure camera parameters: {e}")
            print("ℹ️ This is normal for some camera types or in emulation mode")
    
    def disconnect(self) -> None:
        """Disconnect from the camera device."""
        with self.lock:
            print(f"[CONNECT] Disconnecting from camera...")
            self.is_connected = False
            self.cleanup()
            print("[SUCCESS] Disconnected")
    
    def cleanup(self) -> None:
        """Clean up camera resources."""
        try:
            if self.camera is not None:
                if self.camera.IsGrabbing():
                    self.camera.StopGrabbing()
                if self.camera.IsOpen():
                    self.camera.Close()
                self.camera = None
        except Exception as e:
            print(f"Warning during cleanup: {e}")
    
    def start_grabbing(self) -> bool:
        """Start image grabbing."""
        try:
            with self.lock:
                if not self.is_connected or self.camera is None:
                    return False
                
                if not self.camera.IsGrabbing():
                    self.camera.StartGrabbing(py.GrabStrategy_LatestImageOnly)
                    print("[IMAGE] Started grabbing images")
                
                self.is_running = True
                return True
                
        except Exception as e:
            print(f"[ERROR] Failed to start grabbing: {e}")
            self.handle_device_removal()
            return False
    
    def stop_grabbing(self) -> None:
        """Stop image grabbing."""
        try:
            with self.lock:
                self.is_running = False
                if self.camera is not None and self.camera.IsGrabbing():
                    self.camera.StopGrabbing()
                    print("[STOP] Stopped grabbing images")
        except Exception as e:
            print(f"Warning during stop grabbing: {e}")
    
    def grab_single_image(self) -> bool:
        """Grab a single image with device removal handling."""
        try:
            with self.lock:
                if not self.is_connected or self.camera is None:
                    return False
                
                # Wait for camera to be ready for software trigger
                if self.camera.CanWaitForFrameTriggerReady():
                    self.camera.WaitForFrameTriggerReady(1000, py.TimeoutHandling_ThrowException)
                    self.camera.ExecuteSoftwareTrigger()
                
                # Retrieve the image
                grab_result = self.camera.RetrieveResult(5000, py.TimeoutHandling_ThrowException)
                
                if grab_result.GrabSucceeded():
                    self.images_grabbed += 1
                    if self.images_grabbed % 10 == 0:
                        print(f"[IMAGE] Grabbed {self.images_grabbed} images")
                    grab_result.Release()
                    return True
                else:
                    print(f"[ERROR] Grab failed: {grab_result.GetErrorDescription()}")
                    grab_result.Release()
                    return False
                    
        except py.TimeoutException:
            print("⏰ Timeout during image grab")
            return False
        except geni.GenericException as e:
            print(f"[ERROR] Camera error during grab: {e}")
            self.handle_device_removal()
            return False
        except Exception as e:
            print(f"[ERROR] Unexpected error during grab: {e}")
            self.handle_device_removal()
            return False
    
    def handle_device_removal(self) -> None:
        """Handle device removal event."""
        if not self.is_connected:
            return  # Already handling removal
        
        print("\n🚨 Device removal detected!")
        self.connection_lost_count += 1
        
        # Clean up current connection
        self.disconnect()
        
        # Start reconnection attempt in background thread
        if self.reconnect_thread is None or not self.reconnect_thread.is_alive():
            self.reconnect_thread = threading.Thread(target=self.attempt_reconnection, daemon=True)
            self.reconnect_thread.start()
    
    def attempt_reconnection(self) -> None:
        """Attempt to reconnect to the device."""
        print("🔄 Starting automatic reconnection...")
        max_attempts = 10
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            print(f"🔄 Reconnection attempt {attempt}/{max_attempts}")
            
            # Wait before attempting to reconnect
            time.sleep(2.0)
            
            # Check if device is available
            if self.is_device_available():
                if self.connect():
                    self.reconnection_count += 1
                    print(f"[SUCCESS] Reconnection successful! (Attempt {attempt})")
                    
                    # Restart grabbing if it was running
                    if self.is_running:
                        self.start_grabbing()
                    
                    return
                else:
                    print(f"[ERROR] Reconnection attempt {attempt} failed")
            else:
                print(f"🔍 Device not available (attempt {attempt})")
        
        print(f"[ERROR] Failed to reconnect after {max_attempts} attempts")
        print("[IDEA] Please check device connection and restart the application")
    
    def is_device_available(self) -> bool:
        """Check if the device is available."""
        try:
            tlf = py.TlFactory.GetInstance()
            devices = tlf.EnumerateDevices()
            for device in devices:
                if (device.GetSerialNumber() == self.device_info.GetSerialNumber() and
                    device.GetModelName() == self.device_info.GetModelName()):
                    return True
            return False
        except Exception:
            return False
    
    def get_status(self) -> dict:
        """Get current status information."""
        with self.lock:
            return {
                'connected': self.is_connected,
                'grabbing': self.camera.IsGrabbing() if self.camera else False,
                'images_grabbed': self.images_grabbed,
                'connection_lost_count': self.connection_lost_count,
                'reconnection_count': self.reconnection_count,
                'device_name': self.device_info.GetModelName(),
                'serial_number': self.device_info.GetSerialNumber()
            }


def display_status(handler: DeviceRemovalHandler) -> None:
    """Display current status information."""
    status = handler.get_status()
    
    print("\n" + "=" * 50)
    print("DEVICE STATUS")
    print("=" * 50)
    print(f"Device Name      : {status['device_name']}")
    print(f"Serial Number    : {status['serial_number']}")
    print(f"Connected        : {'[SUCCESS] Yes' if status['connected'] else '[ERROR] No'}")
    print(f"Grabbing         : {'[SUCCESS] Yes' if status['grabbing'] else '[ERROR] No'}")
    print(f"Images Grabbed   : {status['images_grabbed']}")
    print(f"Disconnections   : {status['connection_lost_count']}")
    print(f"Reconnections    : {status['reconnection_count']}")
    print("=" * 50)


def main() -> int:
    """
    Main function demonstrating device removal handling.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Device Removal Handling Sample ===")
        print("This sample demonstrates robust camera connection handling.")
        print("You can test device removal by disconnecting and reconnecting the camera.\n")
        
        # Find the first available camera
        tlf = py.TlFactory.GetInstance()
        devices = tlf.EnumerateDevices()
        if len(devices) == 0:
            print("[ERROR] No camera devices found!")
            return 1
        
        # Use the first device
        device_info = devices[0]
        print(f"Using device: {device_info.GetModelName()}")
        print(f"Serial Number: {device_info.GetSerialNumber()}\n")
        
        # Create device removal handler
        handler = DeviceRemovalHandler(device_info)
        
        # Connect to the camera
        if not handler.connect():
            print("[ERROR] Failed to connect to camera")
            return 1
        
        # Start grabbing images
        if not handler.start_grabbing():
            print("[ERROR] Failed to start grabbing")
            return 1
        
        print("\n[IMAGE] Starting image acquisition...")
        print("[IDEA] To test device removal, disconnect and reconnect the camera cable.")
        print("[IDEA] Press Ctrl+C to stop the demonstration.\n")
        
        # Main grabbing loop
        consecutive_failures = 0
        max_consecutive_failures = 5
        status_interval = 50  # Show status every N images
        
        try:
            while consecutive_failures < max_consecutive_failures:
                # Grab an image
                if handler.grab_single_image():
                    consecutive_failures = 0
                    
                    # Display status periodically
                    if handler.images_grabbed % status_interval == 0:
                        display_status(handler)
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        print(f"\n[ERROR] Too many consecutive failures ({max_consecutive_failures})")
                        break
                
                # Small delay between grabs
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n\n[STOP] Stopping demonstration...")
        
        # Stop grabbing
        handler.stop_grabbing()
        
        # Display final status
        display_status(handler)
        
        # Disconnect
        handler.disconnect()
        
        print("\nDevice removal handling demonstration completed!")
        
    except genicam.GenericException as e:
        print(f"[ERROR] An exception occurred: {e}")
        exit_code = 1
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        exit_code = 1
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        
        sys.exit(1) 