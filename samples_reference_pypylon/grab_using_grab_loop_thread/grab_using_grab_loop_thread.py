#!/usr/bin/env python3
"""
grab_using_grab_loop_thread.py

This sample demonstrates how to use the grab loop thread provided by the InstantCamera
class for multi-threaded image acquisition and processing. The grab loop thread handles
image retrieval in the background while the main thread remains responsive for user
interaction or other processing tasks.

Key concepts demonstrated:
- Grab loop thread for background image processing
- Multiple image event handlers for processing chains
- Non-blocking image acquisition
- Interactive camera control
- Software triggering with grab loop thread
- Thread-safe image processing

The grab loop thread is particularly useful for:
- Real-time image processing applications
- Interactive camera control interfaces
- Applications requiring responsive user interfaces
- Multi-threaded processing pipelines
- Background image acquisition while performing other tasks

This is equivalent to samples_reference_c++/Grab_UsingGrabLoopThread/
"""

from typing import Optional, List
import pypylon.pylon as pylon
from pypylon import genicam
import time
import threading
import sys
import os

# Import for cross-platform keyboard input
try:
    import msvcrt  # Windows
    PLATFORM_WINDOWS = True
except ImportError:
    import select
    import tty
    import termios
    PLATFORM_WINDOWS = False


class ImageProcessingEventHandler(pylon.ImageEventHandler):
    """
    Primary image event handler for processing grabbed images.
    
    This handler demonstrates how to process images in the grab loop thread
    and collect statistics about the image acquisition process.
    """
    
    def __init__(self, name: str = "ImageProcessor"):
        super().__init__()
        self.name = name
        self.image_count = 0
        self.successful_grabs = 0
        self.failed_grabs = 0
        self.total_pixels = 0
        self.processing_times = []
        self.lock = threading.Lock()
    
    def OnImageGrabbed(self, camera: pylon.InstantCamera, grab_result: pylon.GrabResult) -> None:
        """
        Called when an image is grabbed by the grab loop thread.
        
        Args:
            camera: The camera that grabbed the image
            grab_result: The grab result containing image data
        """
        with self.lock:
            self.image_count += 1
            
            processing_start = time.time()
            
            if grab_result.GrabSucceeded():
                self.successful_grabs += 1
                
                # Process image data
                width = grab_result.GetWidth()
                height = grab_result.GetHeight()
                pixel_format = grab_result.GetPixelType()
                
                # Update statistics
                self.total_pixels += width * height
                
                print(f"\n🖼️  [{self.name}] Image {self.image_count} processed:")
                print(f"    📏 Size: {width}x{height}")
                print(f"    🎨 Format: {pixel_format}")
                print(f"    [INFO] Frame ID: {grab_result.GetID()}")
                print(f"    ⏱️  Block ID: {grab_result.GetBlockID()}")
                
                # Simulate image processing
                self.simulate_image_processing(grab_result)
                
            else:
                self.failed_grabs += 1
                print(f"\n[ERROR] [{self.name}] Image {self.image_count} grab failed:")
                print(f"    Error: {grab_result.GetErrorCode()} - {grab_result.GetErrorDescription()}")
            
            processing_time = time.time() - processing_start
            self.processing_times.append(processing_time)
            
            # Print processing time every 10 images
            if self.image_count % 10 == 0:
                avg_processing_time = sum(self.processing_times[-10:]) / min(10, len(self.processing_times))
                print(f"    ⚡ Average processing time (last 10): {avg_processing_time:.3f}s")
    
    def simulate_image_processing(self, grab_result: pylon.GrabResult) -> None:
        """
        Simulate image processing operations.
        
        Args:
            grab_result: The grab result to process
        """
        try:
            # Get image data as numpy array
            image_array = grab_result.GetArray()
            
            if image_array is not None:
                # Simulate basic image analysis
                mean_intensity = float(image_array.mean())
                min_intensity = float(image_array.min())
                max_intensity = float(image_array.max())
                
                print(f"    [STATS] Mean intensity: {mean_intensity:.1f}")
                print(f"    📉 Min/Max: {min_intensity:.0f}/{max_intensity:.0f}")
                
                # Simulate processing delay (remove in production)
                time.sleep(0.01)  # 10ms processing simulation
                
        except Exception as e:
            print(f"    [WARNING]  Processing error: {e}")
    
    def get_statistics(self) -> dict:
        """Get processing statistics."""
        with self.lock:
            total_processing_time = sum(self.processing_times)
            avg_processing_time = total_processing_time / len(self.processing_times) if self.processing_times else 0
            
            return {
                'total_images': self.image_count,
                'successful_grabs': self.successful_grabs,
                'failed_grabs': self.failed_grabs,
                'success_rate': (self.successful_grabs / self.image_count * 100) if self.image_count > 0 else 0,
                'total_pixels': self.total_pixels,
                'avg_processing_time': avg_processing_time,
                'total_processing_time': total_processing_time
            }


class DiagnosticEventHandler(pylon.ImageEventHandler):
    """
    Secondary image event handler for diagnostic purposes.
    
    This handler demonstrates how multiple handlers can be chained
    for different processing purposes.
    """
    
    def __init__(self, name: str = "Diagnostics"):
        super().__init__()
        self.name = name
        self.diagnostic_count = 0
        self.timestamp_history = []
        self.lock = threading.Lock()
    
    def OnImageGrabbed(self, camera: pylon.InstantCamera, grab_result: pylon.GrabResult) -> None:
        """Called when an image is grabbed."""
        with self.lock:
            self.diagnostic_count += 1
            current_time = time.time()
            
            if grab_result.GrabSucceeded():
                self.timestamp_history.append(current_time)
                
                # Calculate frame rate from last 10 frames
                if len(self.timestamp_history) > 1:
                    if len(self.timestamp_history) >= 10:
                        recent_timestamps = self.timestamp_history[-10:]
                        time_span = recent_timestamps[-1] - recent_timestamps[0]
                        fps = 9 / time_span if time_span > 0 else 0
                        print(f"    [INFO] [{self.name}] Frame rate: {fps:.1f} FPS")
                
                # Keep only last 20 timestamps for memory efficiency
                if len(self.timestamp_history) > 20:
                    self.timestamp_history = self.timestamp_history[-20:]
            
            # Print diagnostic info every 5 images
            if self.diagnostic_count % 5 == 0:
                print(f"    🔍 [{self.name}] Diagnostic checkpoint - {self.diagnostic_count} images processed")


class UserInputHandler:
    """
    Handler for user input in a cross-platform way.
    
    Provides non-blocking input functionality for interactive camera control.
    """
    
    def __init__(self):
        self.running = True
        self.input_thread = None
        self.latest_input = None
        self.input_lock = threading.Lock()
    
    def start_input_thread(self):
        """Start the input handling thread."""
        self.input_thread = threading.Thread(target=self._input_worker, daemon=True)
        self.input_thread.start()
    
    def _input_worker(self):
        """Worker thread for handling user input."""
        while self.running:
            try:
                user_input = input().strip().lower()
                with self.input_lock:
                    self.latest_input = user_input
            except (EOFError, KeyboardInterrupt):
                break
    
    def get_input(self) -> Optional[str]:
        """Get the latest user input (non-blocking)."""
        with self.input_lock:
            input_value = self.latest_input
            self.latest_input = None
            return input_value
    
    def stop(self):
        """Stop the input handler."""
        self.running = False


def check_grab_loop_support(camera: pylon.InstantCamera) -> bool:
    """Check if the camera supports grab loop thread functionality."""
    try:
        # Check if camera can be queried for frame trigger readiness
        # This is a prerequisite for grab loop thread usage
        if not camera.CanWaitForFrameTriggerReady():
            print("[ERROR] Camera doesn't support frame trigger readiness queries")
            print("   This is required for grab loop thread functionality")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Error checking grab loop support: {e}")
        return False


def setup_camera_configuration(camera: pylon.InstantCamera) -> None:
    """Set up camera configuration for grab loop thread usage."""
    print("[CONFIG] Setting up camera configuration...")
    
    # Register software trigger configuration
    camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                               pylon.RegistrationMode_ReplaceAll, 
                               pylon.Cleanup_Delete)
    print("   [SUCCESS] Software trigger configuration registered")


def register_event_handlers(camera: pylon.InstantCamera) -> tuple:
    """
    Register image event handlers for grab loop thread processing.
    
    Returns:
        Tuple of (primary_handler, diagnostic_handler)
    """
    print("[CONFIG] Registering image event handlers...")
    
    # Create event handlers
    primary_handler = ImageProcessingEventHandler("PrimaryProcessor")
    diagnostic_handler = DiagnosticEventHandler("DiagnosticMonitor")
    
    # Register handlers
    camera.RegisterImageEventHandler(primary_handler, 
                                   pylon.RegistrationMode_Append, 
                                   pylon.Cleanup_Delete)
    
    camera.RegisterImageEventHandler(diagnostic_handler, 
                                   pylon.RegistrationMode_Append, 
                                   pylon.Cleanup_Delete)
    
    print("   [SUCCESS] Image event handlers registered")
    return primary_handler, diagnostic_handler


def start_grab_loop_thread(camera: pylon.InstantCamera) -> None:
    """Start the grab loop thread."""
    print("[CONFIG] Starting grab loop thread...")
    
    # Start grabbing using the grab loop thread
    # The grab loop thread will handle image retrieval and deliver results to event handlers
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
    
    print("   [SUCCESS] Grab loop thread started")
    print("   🔄 Images will be processed in background thread")


def interactive_camera_control(camera: pylon.InstantCamera) -> None:
    """Provide interactive camera control interface."""
    print("\n" + "=" * 60)
    print("INTERACTIVE CAMERA CONTROL")
    print("=" * 60)
    print("Commands:")
    print("  't' or 'T' - Trigger camera")
    print("  's' or 'S' - Show statistics")
    print("  'h' or 'H' - Show help")
    print("  'e' or 'E' - Exit")
    print("=" * 60)
    
    input_handler = UserInputHandler()
    input_handler.start_input_thread()
    
    try:
        while True:
            print("\nEnter command (t/s/h/e): ", end="", flush=True)
            
            # Wait for user input with timeout
            start_time = time.time()
            user_input = None
            
            while time.time() - start_time < 0.1:  # Check every 100ms
                user_input = input_handler.get_input()
                if user_input is not None:
                    break
                time.sleep(0.01)
            
            if user_input is not None:
                if user_input in ['t', 'T']:
                    trigger_camera(camera)
                elif user_input in ['s', 'S']:
                    show_statistics(camera)
                elif user_input in ['h', 'H']:
                    show_help()
                elif user_input in ['e', 'E']:
                    print("Exiting...")
                    break
                else:
                    print(f"Unknown command: {user_input}")
            
            # Small delay to prevent busy waiting
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nReceived interrupt signal")
    finally:
        input_handler.stop()


def trigger_camera(camera: pylon.InstantCamera) -> None:
    """Trigger the camera if ready."""
    try:
        print("🔫 Triggering camera...")
        
        # Wait for camera to be ready for trigger (timeout: 1000ms)
        if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            camera.ExecuteSoftwareTrigger()
            print("   [SUCCESS] Camera triggered successfully")
        else:
            print("   ⏰ Camera not ready for trigger")
            
    except pylon.TimeoutException:
        print("   ⏰ Timeout waiting for camera trigger readiness")
    except Exception as e:
        print(f"   [ERROR] Error triggering camera: {e}")


def show_statistics(camera: pylon.InstantCamera) -> None:
    """Show current grabbing statistics."""
    print("\n" + "=" * 40)
    print("GRABBING STATISTICS")
    print("=" * 40)
    print(f"Camera: {camera.GetDeviceInfo().GetModelName()}")
    print(f"Status: {'Grabbing' if camera.IsGrabbing() else 'Stopped'}")
    print(f"Open: {'Yes' if camera.IsOpen() else 'No'}")
    print("=" * 40)


def show_help() -> None:
    """Show help information."""
    print("\n" + "=" * 50)
    print("GRAB LOOP THREAD HELP")
    print("=" * 50)
    print("This sample demonstrates grab loop thread usage:")
    print()
    print("• Grab loop thread runs in background")
    print("• Images are processed by event handlers")
    print("• Main thread remains responsive")
    print("• Multiple event handlers can be chained")
    print("• Software triggering works with grab loop")
    print()
    print("Commands:")
    print("  t/T - Trigger camera to capture image")
    print("  s/S - Show current statistics")
    print("  h/H - Show this help")
    print("  e/E - Exit the application")
    print("=" * 50)


def main() -> int:
    """
    Main function demonstrating grab loop thread usage.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Grab Loop Thread Sample ===")
        print("This sample demonstrates multi-threaded image acquisition")
        print("using the grab loop thread provided by InstantCamera.\n")
        
        # Create camera instance
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        print(f"Serial Number: {camera.GetDeviceInfo().GetSerialNumber()}")
        
        # Open camera
        camera.Open()
        
        # Check grab loop support
        if not check_grab_loop_support(camera):
            camera.Close()
            return 1
        
        # Set up camera configuration
        setup_camera_configuration(camera)
        
        # Register event handlers
        primary_handler, diagnostic_handler = register_event_handlers(camera)
        
        # Start grab loop thread
        start_grab_loop_thread(camera)
        
        # Interactive camera control
        interactive_camera_control(camera)
        
        # Stop grabbing
        print("\n[CONFIG] Stopping grab loop thread...")
        camera.StopGrabbing()
        print("   [SUCCESS] Grab loop thread stopped")
        
        # Display final statistics
        print("\n" + "=" * 50)
        print("FINAL STATISTICS")
        print("=" * 50)
        stats = primary_handler.get_statistics()
        print(f"Total Images: {stats['total_images']}")
        print(f"Successful Grabs: {stats['successful_grabs']}")
        print(f"Failed Grabs: {stats['failed_grabs']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Total Pixels Processed: {stats['total_pixels']:,}")
        print(f"Average Processing Time: {stats['avg_processing_time']:.3f}s")
        print(f"Total Processing Time: {stats['total_processing_time']:.3f}s")
        
        # Close camera
        camera.Close()
        
        print("\nGrab loop thread demonstration completed successfully!")
        print("\nNote: The grab loop thread enables responsive applications")
        print("      with background image processing capabilities.")
        
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
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        
        sys.exit(1) 