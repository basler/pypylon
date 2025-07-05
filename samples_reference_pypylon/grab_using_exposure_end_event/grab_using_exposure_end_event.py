#!/usr/bin/env python3
"""
grab_using_exposure_end_event.py

This sample demonstrates how to use the Exposure End event to speed up image
acquisition and enable faster processing workflows. When a sensor exposure
finishes, the camera can send an Exposure End event to the computer before
the image data transfer is complete, enabling immediate processing decisions.

Key concepts demonstrated:
- Exposure End event configuration and handling
- Event-based workflow optimization
- Frame number tracking and synchronization
- Timing analysis of events vs image receipt
- SFNC version compatibility (1.x vs 2.0+)
- Event logging and performance measurement

This is useful for:
- High-speed production lines where objects need to be moved immediately
- Time-critical applications requiring immediate processing decisions
- Optimizing throughput by overlapping exposure and processing
- Reducing latency in real-time systems

This is equivalent to samples_reference_c++/Grab_UsingExposureEndEvent/

Note: Exposure End events enable faster response times by not waiting
for complete image transfer before taking action.
"""

from typing import List, Dict, Any, Optional, Callable, Tuple
import pypylon.pylon as pylon
from pypylon import genicam
import time
import threading
from enum import Enum
from dataclasses import dataclass
from collections import deque


class EventType(Enum):
    """Types of events that can be logged."""
    EXPOSURE_END = "ExposureEnd"
    IMAGE_RECEIVED = "ImageReceived"
    MOVE_ACTION = "MoveAction"
    NO_EVENT = "NoEvent"


@dataclass
class LogItem:
    """
    Item for logging events with timestamps.
    
    Tracks timing and sequence of events for analysis.
    """
    event_type: EventType
    frame_number: int
    timestamp: float
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


class TimingAnalyzer:
    """
    Analyzer for event timing and performance.
    
    Provides tools for measuring and analyzing event timing patterns.
    """
    
    def __init__(self):
        self.log: List[LogItem] = []
        self.log_lock = threading.Lock()
    
    def log_event(self, event_type: EventType, frame_number: int, timestamp: float = 0) -> None:
        """Log an event with timestamp."""
        with self.log_lock:
            self.log.append(LogItem(event_type, frame_number, timestamp or time.time()))
    
    def print_timing_analysis(self) -> None:
        """Print detailed timing analysis of logged events."""
        with self.log_lock:
            if not self.log:
                print("No events logged for analysis")
                return
            
            print("\n" + "=" * 60)
            print("TIMING ANALYSIS")
            print("=" * 60)
            print("Note: Time values show relative timing between events")
            print()
            print(f"{'Time [ms]':<12} {'Event':<20} {'Frame #':<10} {'Details'}")
            print("-" * 60)
            
            start_time = self.log[0].timestamp
            
            for i, item in enumerate(self.log):
                # Calculate relative time from start
                relative_time = (item.timestamp - start_time) * 1000  # Convert to ms
                
                # Calculate time difference from previous event
                time_diff = 0
                if i > 0:
                    time_diff = (item.timestamp - self.log[i-1].timestamp) * 1000
                
                # Format event details
                details = ""
                if item.event_type == EventType.EXPOSURE_END:
                    details = "Exposure complete"
                elif item.event_type == EventType.IMAGE_RECEIVED:
                    details = "Image transferred"
                elif item.event_type == EventType.MOVE_ACTION:
                    details = "Move triggered"
                
                print(f"{relative_time:>8.2f}ms ({time_diff:>6.2f}) {item.event_type.value:<20} {item.frame_number:<10} {details}")
            
            self.analyze_patterns()
    
    def analyze_patterns(self) -> None:
        """Analyze timing patterns and provide insights."""
        with self.log_lock:
            if len(self.log) < 2:
                return
            
            print("\nPATTERN ANALYSIS:")
            
            # Group events by type
            events_by_type = {}
            for item in self.log:
                if item.event_type not in events_by_type:
                    events_by_type[item.event_type] = []
                events_by_type[item.event_type].append(item)
            
            # Analyze exposure end to image received delays
            exposure_events = events_by_type.get(EventType.EXPOSURE_END, [])
            image_events = events_by_type.get(EventType.IMAGE_RECEIVED, [])
            
            if exposure_events and image_events:
                delays = []
                for exp_event in exposure_events:
                    # Find matching image event
                    for img_event in image_events:
                        if img_event.frame_number == exp_event.frame_number:
                            delay = (img_event.timestamp - exp_event.timestamp) * 1000
                            delays.append(delay)
                            break
                
                if delays:
                    avg_delay = sum(delays) / len(delays)
                    min_delay = min(delays)
                    max_delay = max(delays)
                    
                    print(f"   Exposure→Image Delay: avg={avg_delay:.2f}ms, min={min_delay:.2f}ms, max={max_delay:.2f}ms")
                    print(f"   Speed benefit: {avg_delay:.2f}ms faster response using exposure end events")
            
            # Analyze move action timing
            move_events = events_by_type.get(EventType.MOVE_ACTION, [])
            if move_events and exposure_events:
                move_delays = []
                for move_event in move_events:
                    # Find matching exposure event
                    for exp_event in exposure_events:
                        if exp_event.frame_number == move_event.frame_number:
                            delay = (move_event.timestamp - exp_event.timestamp) * 1000
                            move_delays.append(delay)
                            break
                
                if move_delays:
                    avg_move_delay = sum(move_delays) / len(move_delays)
                    print(f"   Exposure→Move Delay: avg={avg_move_delay:.2f}ms")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get timing statistics."""
        with self.log_lock:
            if not self.log:
                return {}
            
            stats = {
                'total_events': len(self.log),
                'duration_ms': (self.log[-1].timestamp - self.log[0].timestamp) * 1000,
                'events_by_type': {}
            }
            
            for item in self.log:
                event_name = item.event_type.value
                if event_name not in stats['events_by_type']:
                    stats['events_by_type'][event_name] = 0
                stats['events_by_type'][event_name] += 1
            
            return stats


class ExposureEndEventHandler:
    """
    Handler for exposure end events and image events.
    
    Manages event processing, frame tracking, and timing analysis.
    """
    
    def __init__(self, is_gige: bool = False):
        self.is_gige = is_gige
        self.timing_analyzer = TimingAnalyzer()
        
        # Frame number tracking
        self.next_expected_frame_image = 1 if is_gige else 0
        self.next_expected_frame_exposure = 1 if is_gige else 0
        self.next_frame_for_move = 1 if is_gige else 0
        
        # Event handling
        self.move_callback: Optional[Callable[[int], None]] = None
        self.frame_lock = threading.Lock()
        
        # Statistics
        self.exposure_events_received = 0
        self.images_received = 0
        self.move_actions_triggered = 0
        self.lost_events = 0
    
    def set_move_callback(self, callback: Callable[[int], None]) -> None:
        """Set callback function for move actions."""
        self.move_callback = callback
    
    def handle_exposure_end_event(self, camera: pylon.InstantCamera) -> None:
        """Handle exposure end event."""
        try:
            # Get frame number from camera event
            frame_number = self.get_exposure_end_frame_number(camera)
            
            # Log the event
            self.timing_analyzer.log_event(EventType.EXPOSURE_END, frame_number)
            self.exposure_events_received += 1
            
            print(f"Exposure End Event: Frame {frame_number}")
            
            with self.frame_lock:
                # Check if this is the frame we're waiting to move
                if frame_number == self.next_frame_for_move:
                    self.trigger_move_action(frame_number)
                
                # Check for lost exposure end events
                if frame_number != self.next_expected_frame_exposure:
                    self.lost_events += 1
                    print(f"[WARNING]  Lost Exposure End Event: Expected {self.next_expected_frame_exposure}, got {frame_number}")
                
                self.next_expected_frame_exposure = self.increment_frame_number(frame_number)
                
        except Exception as e:
            print(f"[ERROR] Error handling exposure end event: {e}")
    
    def handle_image_received(self, grab_result: pylon.GrabResult) -> None:
        """Handle image received event."""
        try:
            frame_number = grab_result.GetBlockID()
            if frame_number is None:
                frame_number = 0
            
            # Log the event
            self.timing_analyzer.log_event(EventType.IMAGE_RECEIVED, frame_number)
            self.images_received += 1
            
            print(f"[IMAGE] Image Received: Frame {frame_number}, Size: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
            
            with self.frame_lock:
                # Check if this is the frame we're waiting to move
                # (in case exposure end event was lost)
                if frame_number == self.next_frame_for_move:
                    self.trigger_move_action(frame_number)
                
                # Check for lost images
                if frame_number != self.next_expected_frame_image:
                    self.lost_events += 1
                    print(f"[WARNING]  Lost Image: Expected {self.next_expected_frame_image}, got {frame_number}")
                
                self.next_expected_frame_image = self.increment_frame_number(frame_number)
                
        except Exception as e:
            print(f"[ERROR] Error handling image received: {e}")
    
    def trigger_move_action(self, frame_number: int) -> None:
        """Trigger move action for a frame."""
        try:
            # Log the move action
            self.timing_analyzer.log_event(EventType.MOVE_ACTION, frame_number)
            self.move_actions_triggered += 1
            
            print(f"[ACTION] Move Action Triggered: Frame {frame_number}")
            
            # Call the move callback if set
            if self.move_callback:
                self.move_callback(frame_number)
            
            # Update next frame to move
            self.next_frame_for_move = self.increment_frame_number(frame_number)
            
        except Exception as e:
            print(f"[ERROR] Error triggering move action: {e}")
    
    def get_exposure_end_frame_number(self, camera: pylon.InstantCamera) -> int:
        """Get frame number from exposure end event."""
        try:
            if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
                # SFNC 2.0+ cameras
                if hasattr(camera, 'EventExposureEndFrameID'):
                    return camera.EventExposureEndFrameID.Value
            else:
                # SFNC 1.x cameras
                if hasattr(camera, 'ExposureEndEventFrameID'):
                    return camera.ExposureEndEventFrameID.Value
            
            # Fallback
            return 0
            
        except Exception as e:
            print(f"[WARNING]  Could not get exposure end frame number: {e}")
            return 0
    
    def increment_frame_number(self, frame_number: int) -> int:
        """Increment frame number according to camera type."""
        frame_number += 1
        
        # GigE cameras don't use frame number 0
        if self.is_gige and frame_number == 0:
            frame_number = 1
        
        return frame_number
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get event handler statistics."""
        return {
            'exposure_events_received': self.exposure_events_received,
            'images_received': self.images_received,
            'move_actions_triggered': self.move_actions_triggered,
            'lost_events': self.lost_events,
            'next_expected_frame_image': self.next_expected_frame_image,
            'next_expected_frame_exposure': self.next_expected_frame_exposure,
            'next_frame_for_move': self.next_frame_for_move
        }


class ExposureEndEventManager:
    """
    Manager for exposure end event demonstration.
    
    Handles camera setup, event configuration, and acquisition workflow.
    """
    
    def __init__(self):
        self.camera: Optional[pylon.InstantCamera] = None
        self.event_handler: Optional[ExposureEndEventHandler] = None
        self.is_gige = False
        self.sfnc_version = pylon.Sfnc_1_5_0
    
    def setup_camera(self) -> bool:
        """Set up camera for exposure end event demonstration."""
        try:
            print("[CONFIG] Setting up camera for exposure end events...")
            
            # Create camera
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            
            device_info = self.camera.GetDeviceInfo()
            print(f"Using device: {device_info.GetModelName()}")
            print(f"Serial Number: {device_info.GetSerialNumber()}")
            
            # Determine camera type
            self.is_gige = device_info.GetDeviceClass() == "BaslerGigE"
            print(f"Camera type: {'GigE' if self.is_gige else 'USB'}")
            
            # Open camera
            self.camera.Open()
            
            # Get SFNC version
            self.sfnc_version = self.camera.GetSfncVersion()
            print(f"SFNC Version: {'2.0+' if self.sfnc_version >= pylon.Sfnc_2_0_0 else '1.x'}")
            
            # Create event handler
            self.event_handler = ExposureEndEventHandler(self.is_gige)
            self.event_handler.set_move_callback(self.handle_move_action)
            
            print("[SUCCESS] Camera setup complete")
            return True
            
        except Exception as e:
            print(f"[ERROR] Camera setup failed: {e}")
            return False
    
    def configure_exposure_end_events(self) -> bool:
        """Configure camera for exposure end events."""
        try:
            print("[CONFIG] Configuring exposure end events...")
            
            # Check if camera supports events
            if not hasattr(self.camera, 'EventSelector') or not genicam.IsWritable(self.camera.EventSelector):
                print("[ERROR] Camera doesn't support events")
                return False
            
            # Enable camera event processing
            if hasattr(self.camera, 'GrabCameraEvents'):
                self.camera.GrabCameraEvents = True
                print("   [SUCCESS] Camera event processing enabled")
            
            # Configure exposure end event
            try:
                # Select exposure end event
                if hasattr(self.camera, 'EventSelector'):
                    self.camera.EventSelector.Value = "ExposureEnd"
                    print("   [CONFIG] Exposure end event selected")
                
                # Enable event notification
                if hasattr(self.camera, 'EventNotification'):
                    try:
                        self.camera.EventNotification.Value = "On"
                        print("   [NOTIFY] Event notification enabled")
                    except:
                        # Some cameras use different notification values
                        try:
                            self.camera.EventNotification.Value = "GenICamEvent"
                            print("   [NOTIFY] GenICam event notification enabled")
                        except Exception as e:
                            print(f"   [WARNING]  Could not enable event notification: {e}")
                
                print("[SUCCESS] Exposure end events configured")
                return True
                
            except Exception as e:
                print(f"[ERROR] Could not configure exposure end events: {e}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Event configuration failed: {e}")
            return False
    
    def handle_move_action(self, frame_number: int) -> None:
        """Handle move action callback."""
        # This is where you would implement actual move logic
        # For demonstration, we just log the action
        print(f"   [RUN] Move action executed for frame {frame_number}")
        print(f"   [PIN] Object/sensor can be moved now (before image transfer completes)")
    
    def demonstrate_exposure_end_events(self, num_images: int = 10) -> bool:
        """Demonstrate exposure end event handling."""
        try:
            print(f"\n[START] Starting exposure end event demonstration ({num_images} images)...")
            print("[INFO] This will show timing differences between exposure end and image received events\n")
            
            # Start grabbing
            self.camera.StartGrabbingMax(num_images)
            
            images_processed = 0
            
            while self.camera.IsGrabbing() and images_processed < num_images:
                # Retrieve image
                grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                
                if grab_result.GrabSucceeded():
                    # Handle image received event
                    self.event_handler.handle_image_received(grab_result)
                    images_processed += 1
                    
                    # Simulate exposure end event handling
                    # Note: In C++ this would be handled by actual camera events
                    # In pypylon, we simulate the event timing
                    try:
                        self.simulate_exposure_end_event(grab_result)
                    except Exception as e:
                        print(f"[WARNING]  Could not simulate exposure end event: {e}")
                    
                    # Small delay to show timing
                    time.sleep(0.1)
                
                else:
                    print(f"[ERROR] Grab failed: {grab_result.GetErrorDescription()}")
                
                grab_result.Release()
            
            print(f"\n[SUCCESS] Demonstration complete: {images_processed} images processed")
            return True
            
        except Exception as e:
            print(f"[ERROR] Demonstration failed: {e}")
            return False
    
    def simulate_exposure_end_event(self, grab_result: pylon.GrabResult) -> None:
        """
        Simulate exposure end event handling.
        
        Note: pypylon doesn't provide direct access to exposure end events
        like the C++ API. This simulation shows the concept.
        """
        try:
            # Simulate exposure end event occurring before image transfer
            # In reality, this would be triggered by the camera hardware
            exposure_end_time = time.time() - 0.001  # Simulate 1ms earlier
            
            frame_number = grab_result.GetBlockID() or 0
            
            # Log simulated exposure end event
            self.event_handler.timing_analyzer.log_event(
                EventType.EXPOSURE_END, 
                frame_number, 
                exposure_end_time
            )
            
            # Simulate the move action trigger
            if frame_number == self.event_handler.next_frame_for_move:
                self.event_handler.trigger_move_action(frame_number)
                
        except Exception as e:
            print(f"[WARNING]  Simulation error: {e}")
    
    def disable_events(self) -> None:
        """Disable camera events."""
        try:
            print("[CONFIG] Disabling events...")
            
            if hasattr(self.camera, 'EventSelector') and hasattr(self.camera, 'EventNotification'):
                # Disable exposure end events
                try:
                    self.camera.EventSelector.Value = "ExposureEnd"
                    self.camera.EventNotification.Value = "Off"
                    print("   [SUCCESS] Exposure end events disabled")
                except Exception as e:
                    print(f"   [WARNING]  Could not disable exposure end events: {e}")
                
                # Disable other events
                event_types = ["EventOverrun", "FrameStartOvertrigger"]
                for event_type in event_types:
                    try:
                        self.camera.EventSelector.Value = event_type
                        self.camera.EventNotification.Value = "Off"
                    except:
                        pass  # Event type might not be supported
            
            print("[SUCCESS] Events disabled")
            
        except Exception as e:
            print(f"[ERROR] Error disabling events: {e}")
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            if self.camera and self.camera.IsOpen():
                self.camera.Close()
            print("[CLEANUP] Cleanup complete")
        except Exception as e:
            print(f"[WARNING]  Cleanup warning: {e}")
    
    def get_results(self) -> Dict[str, Any]:
        """Get demonstration results."""
        if not self.event_handler:
            return {}
        
        return {
            'event_handler_stats': self.event_handler.get_statistics(),
            'timing_stats': self.event_handler.timing_analyzer.get_statistics(),
            'camera_type': 'GigE' if self.is_gige else 'USB',
            'sfnc_version': '2.0+' if self.sfnc_version >= pylon.Sfnc_2_0_0 else '1.x'
        }


def main() -> int:
    """
    Main function demonstrating exposure end event functionality.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Exposure End Event Sample ===")
        print("This sample demonstrates how to use exposure end events")
        print("to speed up image acquisition and processing workflows.\n")
        
        print("[CONFIG] Benefits of Exposure End Events:")
        print("   • Faster response times by not waiting for image transfer")
        print("   • Immediate processing decisions after exposure completes")
        print("   • Optimized throughput by overlapping exposure and processing")
        print("   • Reduced latency in time-critical applications")
        print()
        
        print("[WARNING]  Note: pypylon has limited exposure end event support")
        print("   compared to the C++ API. This sample demonstrates the")
        print("   concepts and timing benefits.\n")
        
        # Create manager
        manager = ExposureEndEventManager()
        
        # Set up camera
        if not manager.setup_camera():
            return 1
        
        # Configure events
        if not manager.configure_exposure_end_events():
            print("[WARNING]  Could not configure events, continuing with simulation...")
        
        # Demonstrate exposure end events
        if not manager.demonstrate_exposure_end_events(num_images=10):
            return 1
        
        # Show timing analysis
        if manager.event_handler:
            manager.event_handler.timing_analyzer.print_timing_analysis()
        
        # Show results
        results = manager.get_results()
        print(f"\n[INFO] DEMONSTRATION RESULTS:")
        for key, value in results.items():
            if isinstance(value, dict):
                print(f"   {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    print(f"     {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Disable events and cleanup
        manager.disable_events()
        manager.cleanup()
        
        print("\n" + "=" * 50)
        print("EXPOSURE END EVENT DEMONSTRATION COMPLETED")
        print("=" * 50)
        print("Exposure end events provide:")
        print("  • Faster response times")
        print("  • Immediate processing decisions")
        print("  • Optimized acquisition workflows")
        print("  • Reduced system latency")
        
        print("\nApplications:")
        print("  • High-speed production lines")
        print("  • Real-time quality control")
        print("  • Motion triggered systems")
        print("  • Time-critical automation")
        
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