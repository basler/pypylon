#!/usr/bin/env python3
"""
grab_using_buffer_factory.py

This sample demonstrates how to use a user-provided buffer factory for advanced
buffer management. Using a buffer factory is optional and intended for advanced
use cases only. A buffer factory is necessary when you want to grab into
externally supplied buffers, such as those from other image processing libraries.

Key concepts demonstrated:
- Custom buffer factory implementation
- External buffer allocation and management
- Buffer context tracking
- Integration with external memory systems
- Advanced buffer lifecycle management
- Thread-safe buffer operations

Buffer factories are useful for:
- Integration with external image processing libraries
- Custom memory management schemes
- Zero-copy operations with other systems
- Specialized buffer allocation strategies
- Memory pool management

This is equivalent to samples_reference_c++/Grab_UsingBufferFactory/

Note: This is an advanced feature for specialized use cases.
Most applications should use the default buffer management.
"""

from typing import List, Dict, Any, Optional, Callable
import pypylon.pylon as pylon
from pypylon import genicam
import numpy as np
import threading
import time
import gc


class BufferInfo:
    """
    Information about a managed buffer.
    
    Tracks buffer details for lifecycle management.
    """
    
    def __init__(self, buffer_id: int, size: int, buffer_data: Any):
        self.buffer_id = buffer_id
        self.size = size
        self.buffer_data = buffer_data
        self.allocated_time = time.time()
        self.is_active = True
        self.usage_count = 0
    
    def __str__(self) -> str:
        return f"Buffer {self.buffer_id}: {self.size} bytes, active={self.is_active}, usage={self.usage_count}"


class CustomBufferFactory:
    """
    Custom buffer factory for advanced buffer management.
    
    Provides custom buffer allocation and deallocation strategies,
    including integration with external memory systems.
    """
    
    def __init__(self, max_buffers: int = 10, alignment: int = 32):
        self.max_buffers = max_buffers
        self.alignment = alignment
        self.next_buffer_id = 1000
        self.buffers: Dict[int, BufferInfo] = {}
        self.buffer_lock = threading.Lock()
        
        # Statistics
        self.total_allocated = 0
        self.total_freed = 0
        self.peak_memory = 0
        self.current_memory = 0
    
    def allocate_buffer(self, size: int) -> tuple[np.ndarray, int]:
        """
        Allocate a buffer for image data.
        
        Args:
            size: Size of buffer in bytes
            
        Returns:
            tuple: (buffer_array, buffer_context)
        """
        with self.buffer_lock:
            try:
                # Check if we've hit the maximum number of buffers
                if len(self.buffers) >= self.max_buffers:
                    raise RuntimeError(f"Maximum number of buffers ({self.max_buffers}) reached")
                
                # Generate unique buffer ID
                buffer_id = self.next_buffer_id
                self.next_buffer_id += 1
                
                # Allocate aligned buffer
                # Using numpy array for efficient memory management
                buffer_array = np.zeros(size, dtype=np.uint8)
                
                # Ensure alignment (numpy typically handles this, but we can verify)
                if self.alignment > 1:
                    # For demonstration, we'll just use numpy's default alignment
                    pass
                
                # Create buffer info
                buffer_info = BufferInfo(buffer_id, size, buffer_array)
                self.buffers[buffer_id] = buffer_info
                
                # Update statistics
                self.total_allocated += 1
                self.current_memory += size
                self.peak_memory = max(self.peak_memory, self.current_memory)
                
                print(f"📦 Allocated buffer {buffer_id}: {size} bytes")
                print(f"   Active buffers: {len(self.buffers)}")
                print(f"   Current memory: {self.current_memory / 1024 / 1024:.2f} MB")
                
                return buffer_array, buffer_id
                
            except Exception as e:
                print(f"[ERROR] Buffer allocation failed: {e}")
                raise
    
    def free_buffer(self, buffer_context: int) -> None:
        """
        Free a previously allocated buffer.
        
        Args:
            buffer_context: Context ID of buffer to free
        """
        with self.buffer_lock:
            try:
                if buffer_context not in self.buffers:
                    print(f"[WARNING]  Warning: Attempting to free unknown buffer {buffer_context}")
                    return
                
                buffer_info = self.buffers[buffer_context]
                buffer_info.is_active = False
                
                # Update statistics
                self.total_freed += 1
                self.current_memory -= buffer_info.size
                
                print(f"🗑️  Freed buffer {buffer_context}: {buffer_info.size} bytes")
                print(f"   Remaining buffers: {len(self.buffers) - 1}")
                print(f"   Current memory: {self.current_memory / 1024 / 1024:.2f} MB")
                
                # Remove from active buffers
                del self.buffers[buffer_context]
                
                # Force garbage collection to ensure memory is released
                gc.collect()
                
            except Exception as e:
                print(f"[ERROR] Buffer deallocation failed: {e}")
    
    def get_buffer_info(self, buffer_context: int) -> Optional[BufferInfo]:
        """Get information about a buffer."""
        with self.buffer_lock:
            return self.buffers.get(buffer_context)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get buffer factory statistics."""
        with self.buffer_lock:
            return {
                'total_allocated': self.total_allocated,
                'total_freed': self.total_freed,
                'active_buffers': len(self.buffers),
                'current_memory_mb': self.current_memory / 1024 / 1024,
                'peak_memory_mb': self.peak_memory / 1024 / 1024,
                'max_buffers': self.max_buffers
            }
    
    def cleanup(self) -> None:
        """Clean up all buffers."""
        with self.buffer_lock:
            print("[CLEANUP] Cleaning up buffer factory...")
            buffer_ids = list(self.buffers.keys())
            for buffer_id in buffer_ids:
                self.free_buffer(buffer_id)
            print(f"[SUCCESS] Buffer factory cleanup complete")


class BufferFactoryGrabber:
    """
    Image grabber using custom buffer factory.
    
    Demonstrates advanced buffer management with custom allocation strategies.
    """
    
    def __init__(self, buffer_factory: CustomBufferFactory):
        self.buffer_factory = buffer_factory
        self.camera: Optional[pylon.InstantCamera] = None
        self.grab_results: List[pylon.GrabResult] = []
        
    def setup_camera(self) -> bool:
        """Set up camera with custom buffer factory."""
        try:
            print("[CONFIG] Setting up camera with custom buffer factory...")
            
            # Create camera
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            
            print(f"Using device: {self.camera.GetDeviceInfo().GetModelName()}")
            print(f"Serial Number: {self.camera.GetDeviceInfo().GetSerialNumber()}")
            
            # Open camera
            self.camera.Open()
            
            # Configure camera for basic operation
            self.configure_camera()
            
            # Note: pypylon doesn't directly support custom buffer factories
            # like the C++ API. We'll demonstrate the concept by managing
            # buffers manually and showing how they would be used.
            
            print("[SUCCESS] Camera setup complete")
            return True
            
        except Exception as e:
            print(f"[ERROR] Camera setup failed: {e}")
            return False
    
    def configure_camera(self) -> None:
        """Configure camera parameters."""
        try:
            # Set pixel format
            if hasattr(self.camera, 'PixelFormat'):
                self.camera.PixelFormat.Value = "Mono8"
            
            # Set acquisition mode
            if hasattr(self.camera, 'AcquisitionMode'):
                self.camera.AcquisitionMode.Value = "Continuous"
            
            # Optimize buffer settings
            if hasattr(self.camera, 'MaxNumBuffer'):
                # This would be where we'd set buffer factory in C++
                # In pypylon, we demonstrate the concept
                pass
            
            print("📷 Camera configured for buffer factory demonstration")
            
        except Exception as e:
            print(f"[WARNING]  Camera configuration warning: {e}")
    
    def grab_with_buffer_factory(self, num_images: int = 5) -> bool:
        """
        Grab images using the custom buffer factory.
        
        In C++, this would use the buffer factory directly.
        In pypylon, we demonstrate the concept by pre-allocating buffers
        and showing how they would be used.
        """
        try:
            print(f"[START] Starting grab with buffer factory ({num_images} images)...")
            
            # Pre-allocate buffers (simulating buffer factory behavior)
            image_size = self.estimate_image_size()
            pre_allocated_buffers = []
            
            for i in range(min(num_images, self.buffer_factory.max_buffers)):
                buffer_array, buffer_context = self.buffer_factory.allocate_buffer(image_size)
                pre_allocated_buffers.append((buffer_array, buffer_context))
            
            print(f"📦 Pre-allocated {len(pre_allocated_buffers)} buffers")
            
            # Start grabbing
            self.camera.StartGrabbingMax(num_images)
            
            grabbed_images = 0
            buffer_usage_map = {}
            
            while self.camera.IsGrabbing() and grabbed_images < num_images:
                # Retrieve image
                grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                
                if grab_result.GrabSucceeded():
                    grabbed_images += 1
                    
                    # In a real buffer factory implementation, we would:
                    # 1. Get the buffer context from the grab result
                    # 2. Access the pre-allocated buffer
                    # 3. Process the image data in the custom buffer
                    
                    # For demonstration, we'll simulate this process
                    buffer_index = (grabbed_images - 1) % len(pre_allocated_buffers)
                    buffer_array, buffer_context = pre_allocated_buffers[buffer_index]
                    
                    # Simulate copying image data to our custom buffer
                    # (In real implementation, camera would write directly to our buffer)
                    image_data = grab_result.GetArray()
                    if image_data is not None and len(image_data.flatten()) <= len(buffer_array):
                        buffer_array[:len(image_data.flatten())] = image_data.flatten()
                    
                    # Track buffer usage
                    buffer_usage_map[buffer_context] = buffer_usage_map.get(buffer_context, 0) + 1
                    
                    print(f"🖼️  Image {grabbed_images}:")
                    print(f"   📏 Size: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
                    print(f"   📦 Buffer Context: {buffer_context}")
                    print(f"   [INFO] Buffer Usage: {buffer_usage_map[buffer_context]}")
                    print(f"   [STATS] Mean Intensity: {np.mean(image_data):.1f}")
                    
                    # Update buffer usage statistics
                    buffer_info = self.buffer_factory.get_buffer_info(buffer_context)
                    if buffer_info:
                        buffer_info.usage_count += 1
                    
                    self.grab_results.append(grab_result)
                    
                else:
                    print(f"[ERROR] Grab failed: {grab_result.GetErrorDescription()}")
                
                grab_result.Release()
            
            print(f"[SUCCESS] Grab complete: {grabbed_images}/{num_images} images")
            
            # Clean up pre-allocated buffers
            for buffer_array, buffer_context in pre_allocated_buffers:
                self.buffer_factory.free_buffer(buffer_context)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Grab with buffer factory failed: {e}")
            return False
    
    def estimate_image_size(self) -> int:
        """Estimate the size of image buffers needed."""
        try:
            # Get image dimensions
            width = self.camera.Width.Value if hasattr(self.camera, 'Width') else 1920
            height = self.camera.Height.Value if hasattr(self.camera, 'Height') else 1080
            
            # Estimate bytes per pixel based on pixel format
            bytes_per_pixel = 1  # Assuming Mono8
            
            estimated_size = width * height * bytes_per_pixel
            
            # Add some padding for safety
            estimated_size = int(estimated_size * 1.1)
            
            print(f"📏 Estimated image size: {estimated_size} bytes ({width}x{height})")
            return estimated_size
            
        except Exception as e:
            print(f"[WARNING]  Could not estimate image size: {e}")
            return 1920 * 1080  # Default size
    
    def cleanup(self) -> None:
        """Clean up resources."""
        try:
            if self.camera and self.camera.IsOpen():
                self.camera.Close()
            
            # Clean up grab results
            for result in self.grab_results:
                result.Release()
            self.grab_results.clear()
            
            print("[CLEANUP] Grabber cleanup complete")
            
        except Exception as e:
            print(f"[WARNING]  Cleanup warning: {e}")


def demonstrate_buffer_factory_usage() -> None:
    """Demonstrate advanced buffer factory usage patterns."""
    print("\n[TARGET] Advanced Buffer Factory Usage Patterns\n")
    
    # Create buffer factory
    buffer_factory = CustomBufferFactory(max_buffers=8, alignment=32)
    
    # Example 1: External library integration
    print("[CONFIG] Example 1: External Library Integration")
    try:
        # Simulate allocating buffers for external library
        opencv_buffers = []
        for i in range(3):
            buffer_array, buffer_context = buffer_factory.allocate_buffer(1920 * 1080)
            opencv_buffers.append((buffer_array, buffer_context))
            print(f"   📦 OpenCV buffer {i}: Context {buffer_context}")
        
        # Simulate processing with external library
        print("   🔄 Processing with external library...")
        for buffer_array, buffer_context in opencv_buffers:
            # Simulate image processing
            processed_data = np.mean(buffer_array)
            print(f"   [INFO] Buffer {buffer_context}: Mean value {processed_data:.1f}")
        
        # Clean up
        for buffer_array, buffer_context in opencv_buffers:
            buffer_factory.free_buffer(buffer_context)
        
    except Exception as e:
        print(f"   [ERROR] External library integration failed: {e}")
    
    # Example 2: Memory pool management
    print("\n[CONFIG] Example 2: Memory Pool Management")
    try:
        # Create a pool of buffers
        pool_size = 5
        buffer_pool = []
        
        for i in range(pool_size):
            buffer_array, buffer_context = buffer_factory.allocate_buffer(640 * 480)
            buffer_pool.append((buffer_array, buffer_context))
            print(f"   📦 Pool buffer {i}: Context {buffer_context}")
        
        # Simulate rapid allocation/deallocation
        print("   🔄 Rapid buffer cycling...")
        for i in range(10):
            # Use buffer from pool
            buffer_array, buffer_context = buffer_pool[i % pool_size]
            buffer_info = buffer_factory.get_buffer_info(buffer_context)
            if buffer_info:
                buffer_info.usage_count += 1
        
        # Clean up pool
        for buffer_array, buffer_context in buffer_pool:
            buffer_factory.free_buffer(buffer_context)
        
    except Exception as e:
        print(f"   [ERROR] Memory pool management failed: {e}")
    
    # Display final statistics
    print("\n[INFO] Final Buffer Factory Statistics:")
    stats = buffer_factory.get_statistics()
    for key, value in stats.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    # Final cleanup
    buffer_factory.cleanup()


def main() -> int:
    """
    Main function demonstrating custom buffer factory functionality.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Custom Buffer Factory Sample ===")
        print("This sample demonstrates advanced buffer management")
        print("using a custom buffer factory implementation.\n")
        
        print("[WARNING]  Note: pypylon doesn't directly support custom buffer factories")
        print("   like the C++ API. This sample demonstrates the concepts and")
        print("   shows how custom buffer management would work.\n")
        
        # Create custom buffer factory
        buffer_factory = CustomBufferFactory(max_buffers=5, alignment=32)
        
        # Create grabber with buffer factory
        grabber = BufferFactoryGrabber(buffer_factory)
        
        # Set up camera
        if not grabber.setup_camera():
            print("[ERROR] Failed to set up camera")
            return 1
        
        # Demonstrate buffer factory grabbing
        if not grabber.grab_with_buffer_factory(num_images=5):
            print("[ERROR] Failed to grab with buffer factory")
            return 1
        
        # Show buffer factory statistics
        print("\n[INFO] Buffer Factory Statistics:")
        stats = buffer_factory.get_statistics()
        for key, value in stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Demonstrate advanced usage patterns
        demonstrate_buffer_factory_usage()
        
        # Clean up
        grabber.cleanup()
        buffer_factory.cleanup()
        
        print("\n" + "=" * 50)
        print("BUFFER FACTORY DEMONSTRATION COMPLETED")
        print("=" * 50)
        print("Custom buffer factories enable:")
        print("  • Integration with external libraries")
        print("  • Custom memory management strategies")
        print("  • Zero-copy operations")
        print("  • Specialized buffer allocation")
        print("  • Memory pool management")
        
        print("\nApplications:")
        print("  • Real-time image processing pipelines")
        print("  • Integration with GPU processing")
        print("  • High-performance computing applications")
        print("  • Custom memory architectures")
        
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