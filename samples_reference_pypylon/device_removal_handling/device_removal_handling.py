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
from pypylon import genicam


class DeviceRemovalHandler:
    """Handles device removal and reconnection events."""
    
    def __init__(self, device_info: pylon.DeviceInfo):
        self.device_info = device_info
        self.camera: Optional[pylon.InstantCamera] = None
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
                self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(self.device_info))
                
                # Register configuration for software triggering
                self.camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                                                pylon.RegistrationMode_ReplaceAll, 
                                                pylon.Cleanup_Delete)
                
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
        """Configure camera parameters."""
        try:
            if self.camera is None:
                return
            
            # Set a reasonable exposure time
            if hasattr(self.camera, 'ExposureTime') and self.camera.ExposureTime.IsWritable():
                self.camera.ExposureTime.Value = 10000  # 10ms
            elif hasattr(self.camera, 'ExposureTimeRaw') and self.camera.ExposureTimeRaw.IsWritable():
                exposure_target = 10000
                min_exp = self.camera.ExposureTimeRaw.Min
                max_exp = self.camera.ExposureTimeRaw.Max
                if exposure_target < min_exp:
                    exposure_target = min_exp
                elif exposure_target > max_exp:
                    exposure_target = max_exp
                self.camera.ExposureTimeRaw.Value = exposure_target
            
            # Set packet size for GigE cameras if available
            if hasattr(self.camera, 'GevSCPSPacketSize') and self.camera.GevSCPSPacketSize.IsWritable():
                self.camera.GevSCPSPacketSize.Value = 1500
                
        except Exception as e:
            print(f"Warning: Could not configure camera parameters: {e}")
    
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
                    self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
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
                    self.camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException)
                    self.camera.ExecuteSoftwareTrigger()
                
                # Retrieve the image
                grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                
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
                    
        except pylon.TimeoutException:
            print("⏰ Timeout during image grab")
            return False
        except genicam.GenericException as e:
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
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
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
        pylon.PylonInitialize()
        
        print("=== Device Removal Handling Sample ===")
        print("This sample demonstrates robust camera connection handling.")
        print("You can test device removal by disconnecting and reconnecting the camera.\n")
        
        # Find the first available camera
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
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
    finally:
        # Ensure pylon resources are released
        pylon.PylonTerminate()
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        pylon.PylonTerminate()
        sys.exit(1) 