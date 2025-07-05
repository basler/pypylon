#!/usr/bin/env python3
"""
grab_camera_events.py

This sample demonstrates how to register event handlers for camera events sent by
Basler cameras. Camera events provide notifications about various camera states and
occurrences, such as exposure completion, event overruns, and other camera-specific events.

Key concepts demonstrated:
- Camera event handler registration and usage
- Multiple event types (Exposure End, Event Overrun)
- SFNC version compatibility (2.0+ vs older versions)
- Event data access (FrameID, Timestamp, etc.)
- Event activation and deactivation
- Multiple handlers for the same event

Camera events are particularly useful for:
- Synchronizing with camera operations
- Monitoring camera status
- Detecting potential issues (overruns)
- Precise timing coordination

This is equivalent to samples_reference_c++/Grab_CameraEvents/
"""

from typing import Optional
import pypylon.pylon as pylon
from pypylon import genicam


# Event IDs for distinguishing different events
class EventID:
    """Event identifiers for distinguishing different camera events."""
    EXPOSURE_END = 100
    EVENT_OVERRUN = 200
    # More events can be added here as needed


class SampleCameraEventHandler(pylon.CameraEventHandler):
    """
    Example camera event handler that processes specific camera events.
    
    This handler demonstrates how to access event data and distinguish between
    different event types using user-provided IDs.
    """
    
    def __init__(self, name: str = "SampleHandler"):
        super().__init__()
        self.name = name
        self.exposure_end_count = 0
        self.event_overrun_count = 0
    
    def OnCameraEvent(self, camera: pylon.InstantCamera, userProvidedId: int, node: genicam.INode) -> None:
        """
        Called when a camera event is received.
        
        Args:
            camera: The camera that sent the event
            userProvidedId: User-defined ID to distinguish event types
            node: The node containing event data
        """
        print(f"\n[{self.name}] Camera Event Received")
        print("=" * 40)
        
        try:
            if userProvidedId == EventID.EXPOSURE_END:
                self.handle_exposure_end_event(camera)
            elif userProvidedId == EventID.EVENT_OVERRUN:
                self.handle_event_overrun_event(camera)
            else:
                print(f"Unknown event ID: {userProvidedId}")
                
        except Exception as e:
            print(f"Error handling camera event: {e}")
    
    def handle_exposure_end_event(self, camera: pylon.InstantCamera) -> None:
        """Handle Exposure End events."""
        self.exposure_end_count += 1
        
        try:
            # Check SFNC version to use appropriate parameters
            if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
                # SFNC 2.0+ (USB cameras)
                if hasattr(camera, 'EventExposureEndFrameID') and camera.EventExposureEndFrameID.IsReadable():
                    frame_id = camera.EventExposureEndFrameID.Value
                    timestamp = camera.EventExposureEndTimestamp.Value
                    print(f"[IMAGE] Exposure End Event (SFNC 2.0+)")
                    print(f"   Frame ID: {frame_id}")
                    print(f"   Timestamp: {timestamp}")
                    print(f"   Event Count: {self.exposure_end_count}")
                else:
                    print("[IMAGE] Exposure End Event (SFNC 2.0+ - data not available)")
            else:
                # SFNC 1.x (GigE cameras)
                if hasattr(camera, 'ExposureEndEventFrameID') and camera.ExposureEndEventFrameID.IsReadable():
                    frame_id = camera.ExposureEndEventFrameID.Value
                    timestamp = camera.ExposureEndEventTimestamp.Value
                    print(f"[IMAGE] Exposure End Event (SFNC 1.x)")
                    print(f"   Frame ID: {frame_id}")
                    print(f"   Timestamp: {timestamp}")
                    print(f"   Event Count: {self.exposure_end_count}")
                else:
                    print("[IMAGE] Exposure End Event (SFNC 1.x - data not available)")
                    
        except Exception as e:
            print(f"[IMAGE] Exposure End Event (error accessing data: {e})")
    
    def handle_event_overrun_event(self, camera: pylon.InstantCamera) -> None:
        """Handle Event Overrun events."""
        self.event_overrun_count += 1
        
        try:
            # Event Overrun events are typically available on SFNC 1.x cameras
            if hasattr(camera, 'EventOverrunEventFrameID') and camera.EventOverrunEventFrameID.IsReadable():
                frame_id = camera.EventOverrunEventFrameID.Value
                timestamp = camera.EventOverrunEventTimestamp.Value
                print(f"[WARNING]  Event Overrun Event")
                print(f"   Frame ID: {frame_id}")
                print(f"   Timestamp: {timestamp}")
                print(f"   Overrun Count: {self.event_overrun_count}")
                print(f"   Warning: Camera events are being dropped!")
            else:
                print(f"[WARNING]  Event Overrun Event (data not available)")
                print(f"   Overrun Count: {self.event_overrun_count}")
                
        except Exception as e:
            print(f"[WARNING]  Event Overrun Event (error accessing data: {e})")
    
    def get_statistics(self) -> dict:
        """Get event statistics."""
        return {
            'exposure_end_count': self.exposure_end_count,
            'event_overrun_count': self.event_overrun_count
        }


class DetailedCameraEventHandler(pylon.CameraEventHandler):
    """
    Detailed camera event handler that prints comprehensive information about events.
    
    This handler demonstrates how to extract detailed information from event nodes.
    """
    
    def __init__(self, name: str = "DetailedHandler"):
        super().__init__()
        self.name = name
        self.event_count = 0
    
    def OnCameraEvent(self, camera: pylon.InstantCamera, userProvidedId: int, node: genicam.INode) -> None:
        """Called when a camera event is received."""
        self.event_count += 1
        
        print(f"\n[{self.name}] Event #{self.event_count}")
        print(f"Device: {camera.GetDeviceInfo().GetModelName()}")
        print(f"User ID: {userProvidedId}")
        print(f"Node Name: {node.GetName()}")
        
        try:
            # Try to get the value from the node
            value_node = genicam.CValuePtr(node)
            if value_node.IsValid():
                print(f"Node Value: {value_node.ToString()}")
            else:
                print("Node Value: (not accessible)")
        except Exception as e:
            print(f"Node Value: (error: {e})")


class SampleImageEventHandler(pylon.ImageEventHandler):
    """
    Example image event handler for demonstration.
    
    This shows how image events and camera events can work together.
    """
    
    def __init__(self):
        super().__init__()
        self.image_count = 0
    
    def OnImageGrabbed(self, camera: pylon.InstantCamera, grab_result: pylon.GrabResult) -> None:
        """Called when an image is grabbed."""
        self.image_count += 1
        if grab_result.GrabSucceeded():
            print(f"🖼️  Image {self.image_count} grabbed: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
        else:
            print(f"🖼️  Image {self.image_count} grab failed: {grab_result.GetErrorDescription()}")


def check_event_support(camera: pylon.InstantCamera) -> bool:
    """Check if the camera supports events."""
    try:
        if hasattr(camera, 'EventSelector') and genicam.IsAvailable(camera.EventSelector):
            return True
        else:
            print("[ERROR] The camera doesn't support events.")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking event support: {e}")
        return False


def configure_exposure_end_event(camera: pylon.InstantCamera) -> bool:
    """Configure and enable Exposure End events."""
    try:
        print("[CONFIG] Configuring Exposure End events...")
        
        # Select the Exposure End event
        camera.EventSelector.Value = "ExposureEnd"
        
        # Enable event notification
        # Different cameras may use different values
        if hasattr(camera, 'EventNotification'):
            try:
                camera.EventNotification.Value = "On"
                print("   [SUCCESS] Exposure End events enabled with 'On'")
                return True
            except genicam.GenericException:
                try:
                    # Some cameras (scout-f, scout-g, aviator GigE) use different values
                    camera.EventNotification.Value = "GenICamEvent"
                    print("   [SUCCESS] Exposure End events enabled with 'GenICamEvent'")
                    return True
                except genicam.GenericException as e:
                    print(f"   [ERROR] Failed to enable Exposure End events: {e}")
                    return False
        else:
            print("   [ERROR] EventNotification parameter not available")
            return False
            
    except Exception as e:
        print(f"   [ERROR] Error configuring Exposure End events: {e}")
        return False


def configure_event_overrun_event(camera: pylon.InstantCamera) -> bool:
    """Configure and enable Event Overrun events (if supported)."""
    try:
        print("[CONFIG] Configuring Event Overrun events...")
        
        # Check if Event Overrun is supported
        if hasattr(camera, 'EventSelector'):
            # Try to select Event Overrun
            try:
                camera.EventSelector.Value = "EventOverrun"
                
                # Enable event notification
                if hasattr(camera, 'EventNotification'):
                    try:
                        camera.EventNotification.Value = "On"
                        print("   [SUCCESS] Event Overrun events enabled with 'On'")
                        return True
                    except genicam.GenericException:
                        try:
                            camera.EventNotification.Value = "GenICamEvent"
                            print("   [SUCCESS] Event Overrun events enabled with 'GenICamEvent'")
                            return True
                        except genicam.GenericException as e:
                            print(f"   [ERROR] Failed to enable Event Overrun events: {e}")
                            return False
                else:
                    print("   [ERROR] EventNotification parameter not available")
                    return False
                    
            except genicam.GenericException:
                print("   [INFO]  Event Overrun events not supported by this camera")
                return False
        else:
            print("   [ERROR] EventSelector parameter not available")
            return False
            
    except Exception as e:
        print(f"   [ERROR] Error configuring Event Overrun events: {e}")
        return False


def disable_camera_events(camera: pylon.InstantCamera) -> None:
    """Disable all camera events."""
    try:
        print("\n[CONFIG] Disabling camera events...")
        
        # Disable Exposure End events
        try:
            camera.EventSelector.Value = "ExposureEnd"
            camera.EventNotification.Value = "Off"
            print("   [SUCCESS] Exposure End events disabled")
        except Exception as e:
            print(f"   [WARNING]  Could not disable Exposure End events: {e}")
        
        # Disable Event Overrun events (if supported)
        try:
            camera.EventSelector.Value = "EventOverrun"
            camera.EventNotification.Value = "Off"
            print("   [SUCCESS] Event Overrun events disabled")
        except Exception as e:
            print("   [INFO]  Event Overrun events not supported or already disabled")
            
    except Exception as e:
        print(f"   [ERROR] Error disabling events: {e}")


def register_event_handlers(camera: pylon.InstantCamera, 
                          sample_handler: SampleCameraEventHandler,
                          detailed_handler: DetailedCameraEventHandler) -> None:
    """Register camera event handlers for different events and data nodes."""
    try:
        print("[CONFIG] Registering camera event handlers...")
        
        # Determine which event data nodes to use based on SFNC version
        if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
            print("   📡 Using SFNC 2.0+ event parameters")
            
            # Register handler for Exposure End event data
            camera.RegisterCameraEventHandler(sample_handler, "EventExposureEndData", 
                                            EventID.EXPOSURE_END, 
                                            pylon.RegistrationMode_ReplaceAll, 
                                            pylon.Cleanup_None)
            
            # Register detailed handlers for individual data nodes
            camera.RegisterCameraEventHandler(detailed_handler, "EventExposureEndFrameID", 
                                            EventID.EXPOSURE_END,
                                            pylon.RegistrationMode_Append, 
                                            pylon.Cleanup_None)
            
            camera.RegisterCameraEventHandler(detailed_handler, "EventExposureEndTimestamp", 
                                            EventID.EXPOSURE_END,
                                            pylon.RegistrationMode_Append, 
                                            pylon.Cleanup_None)
            
        else:
            print("   📡 Using SFNC 1.x event parameters")
            
            # Register handler for Exposure End event data
            camera.RegisterCameraEventHandler(sample_handler, "ExposureEndEventData", 
                                            EventID.EXPOSURE_END,
                                            pylon.RegistrationMode_ReplaceAll, 
                                            pylon.Cleanup_None)
            
            # Register handler for Event Overrun (typically available on SFNC 1.x)
            camera.RegisterCameraEventHandler(sample_handler, "EventOverrunEventData", 
                                            EventID.EVENT_OVERRUN,
                                            pylon.RegistrationMode_Append, 
                                            pylon.Cleanup_None)
            
            # Register detailed handlers for individual data nodes
            camera.RegisterCameraEventHandler(detailed_handler, "ExposureEndEventFrameID", 
                                            EventID.EXPOSURE_END,
                                            pylon.RegistrationMode_Append, 
                                            pylon.Cleanup_None)
            
            camera.RegisterCameraEventHandler(detailed_handler, "ExposureEndEventTimestamp", 
                                            EventID.EXPOSURE_END,
                                            pylon.RegistrationMode_Append, 
                                            pylon.Cleanup_None)
        
        print("   [SUCCESS] Camera event handlers registered successfully")
        
    except Exception as e:
        print(f"   [ERROR] Error registering event handlers: {e}")


def main() -> int:
    """
    Main function demonstrating camera event handling.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Camera Events Sample ===")
        print("This sample demonstrates camera event handling in pypylon.")
        print("Camera events provide notifications about camera states and operations.\n")
        
        # Create camera instance
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        print(f"Serial Number: {camera.GetDeviceInfo().GetSerialNumber()}")
        
        # Create event handlers
        sample_handler = SampleCameraEventHandler("MainEventHandler")
        detailed_handler = DetailedCameraEventHandler("DetailedEventHandler")
        image_handler = SampleImageEventHandler()
        
        # Register configuration for software triggering
        camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                                   pylon.RegistrationMode_ReplaceAll, 
                                   pylon.Cleanup_Delete)
        
        # Register image event handler
        camera.RegisterImageEventHandler(image_handler, 
                                       pylon.RegistrationMode_Append, 
                                       pylon.Cleanup_Delete)
        
        # IMPORTANT: Enable camera event processing (disabled by default)
        camera.GrabCameraEvents.Value = True
        print("[SUCCESS] Camera event processing enabled\n")
        
        # Open camera
        camera.Open()
        
        # Check if camera supports events
        if not check_event_support(camera):
            camera.Close()
            return 1
        
        print(f"Camera SFNC Version: {camera.GetSfncVersion()}")
        
        # Register event handlers
        register_event_handlers(camera, sample_handler, detailed_handler)
        
        # Configure events
        exposure_end_enabled = configure_exposure_end_event(camera)
        event_overrun_enabled = configure_event_overrun_event(camera)
        
        if not exposure_end_enabled:
            print("[WARNING]  Warning: Exposure End events could not be enabled")
        
        # Start grabbing images
        images_to_grab = 5
        print(f"\n[START] Starting to grab {images_to_grab} images...")
        print("[IMAGE] Camera events will be displayed as they occur.\n")
        
        camera.StartGrabbingMax(images_to_grab)
        
        # Grab images and trigger events
        while camera.IsGrabbing():
            try:
                # Wait for camera to be ready for software trigger
                if camera.CanWaitForFrameTriggerReady():
                    camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException)
                    camera.ExecuteSoftwareTrigger()
                
                # Retrieve result (this will trigger events)
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                grab_result.Release()
                
            except pylon.TimeoutException:
                print("⏰ Timeout waiting for image")
                break
            except Exception as e:
                print(f"[ERROR] Error during grabbing: {e}")
                break
        
        # Disable events
        disable_camera_events(camera)
        
        # Close camera
        camera.Close()
        
        # Display statistics
        print("\n" + "=" * 50)
        print("EVENT STATISTICS")
        print("=" * 50)
        stats = sample_handler.get_statistics()
        print(f"Exposure End Events: {stats['exposure_end_count']}")
        print(f"Event Overrun Events: {stats['event_overrun_count']}")
        print(f"Images Grabbed: {image_handler.image_count}")
        print(f"Total Event Callbacks: {detailed_handler.event_count}")
        
        print("\nCamera events demonstration completed successfully!")
        print("\nNote: Camera events provide real-time notifications independent of image grabbing.")
        print("      They are useful for synchronization and monitoring camera operations.")
        
    except genicam.GenericException as e:
        print(f"[ERROR] A pylon exception occurred: {e}")
        exit_code = 1
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        exit_code = 1
    finally:
        # Ensure pylon resources are released
        
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        
        sys.exit(1) 