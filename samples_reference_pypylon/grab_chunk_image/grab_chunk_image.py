#!/usr/bin/env python3
"""
grab_chunk_image.py

This sample demonstrates how to use chunk features with Basler cameras. Chunk features
allow cameras to append additional metadata to image data, such as timestamps, frame
counters, and CRC checksums. This metadata is transferred as separate "chunks" alongside
the image data.

Key concepts demonstrated:
- Enabling chunk mode and specific chunk features
- Accessing chunk data from grab results
- Generic vs native parameter access for chunk data
- CRC validation for data integrity
- Payload type validation
- Image event handlers for chunk processing
- Static chunk node map pool optimization

Chunk data is useful for:
- Precise timestamping of images
- Frame synchronization in multi-camera systems
- Data integrity verification
- Camera diagnostics and monitoring
- Trigger correlation and timing analysis

This is equivalent to samples_reference_c++/Grab_ChunkImage/
"""

from typing import Optional, List, Dict, Any
import pypylon.pylon as pylon
from pypylon import genicam
import time


class ChunkImageEventHandler(pylon.ImageEventHandler):
    """
    Image event handler that processes chunk data attached to grab results.
    
    This handler demonstrates both generic node map access and native 
    chunk data access methods.
    """
    
    def __init__(self, name: str = "ChunkImageHandler"):
        super().__init__()
        self.name = name
        self.image_count = 0
        self.chunk_statistics = {
            'timestamp_count': 0,
            'framecounter_count': 0,
            'crc_count': 0,
            'crc_errors': 0
        }
    
    def OnImageGrabbed(self, camera: pylon.InstantCamera, grab_result: pylon.GrabResult) -> None:
        """
        Called when an image is grabbed.
        
        Args:
            camera: The camera that grabbed the image
            grab_result: The grab result containing image and chunk data
        """
        self.image_count += 1
        
        if grab_result.GrabSucceeded():
            print(f"\n[{self.name}] Image {self.image_count} grabbed successfully")
            print("=" * 50)
            
            # Demonstrate chunk data access
            self.process_chunk_data(grab_result)
            
        else:
            print(f"\n[{self.name}] Image {self.image_count} grab failed")
            print(f"Error: {grab_result.ErrorCode} - {grab_result.ErrorDescription}")
    
    def process_chunk_data(self, grab_result: pylon.GrabResult) -> None:
        """Process chunk data from the grab result."""
        try:
            # Method 1: Generic parameter access via chunk data node map
            self.access_chunk_data_generic(grab_result)
            
            # Method 2: Native parameter access via grab result members
            self.access_chunk_data_native(grab_result)
            
        except Exception as e:
            print(f"[ERROR] Error processing chunk data: {e}")
    
    def access_chunk_data_generic(self, grab_result: pylon.GrabResult) -> None:
        """
        Access chunk data via the generic chunk data node map.
        This method works with all grab result types.
        """
        try:
            # Get the chunk data node map
            chunk_node_map = grab_result.ChunkDataNodeMap
            
            # Access timestamp chunk via node map
            if genicam.IsAvailable(chunk_node_map.ChunkTimestamp):
                timestamp_node = chunk_node_map.ChunkTimestamp
                if genicam.IsReadable(timestamp_node):
                    timestamp = timestamp_node.Value
                    print(f"[TIME] Timestamp (Generic): {timestamp}")
                    self.chunk_statistics['timestamp_count'] += 1
            
            # Access frame counter chunk via node map (if available)
            if genicam.IsAvailable(chunk_node_map.ChunkFramecounter):
                framecounter_node = chunk_node_map.ChunkFramecounter
                if genicam.IsReadable(framecounter_node):
                    framecounter = framecounter_node.Value
                    print(f"[COUNT] Frame Counter (Generic): {framecounter}")
                    self.chunk_statistics['framecounter_count'] += 1
                    
        except Exception as e:
            print(f"[WARNING]  Generic chunk data access error: {e}")
    
    def access_chunk_data_native(self, grab_result: pylon.GrabResult) -> None:
        """
        Access chunk data via native grab result members.
        This is the recommended approach for device-specific grab results.
        """
        try:
            # Access timestamp chunk via native access
            if hasattr(grab_result, 'ChunkTimestamp') and genicam.IsReadable(grab_result.ChunkTimestamp):
                timestamp = grab_result.ChunkTimestamp.Value
                print(f"[TIME] Timestamp (Native): {timestamp}")
            
            # Access frame counter chunk via native access
            if hasattr(grab_result, 'ChunkFramecounter') and genicam.IsReadable(grab_result.ChunkFramecounter):
                framecounter = grab_result.ChunkFramecounter.Value
                print(f"[COUNT] Frame Counter (Native): {framecounter}")
            
            # Access CRC chunk data (if available)
            if hasattr(grab_result, 'ChunkPayloadCRC16') and genicam.IsReadable(grab_result.ChunkPayloadCRC16):
                crc = grab_result.ChunkPayloadCRC16.Value
                print(f"[SECURE] CRC16 (Native): 0x{crc:04X}")
                self.chunk_statistics['crc_count'] += 1
                
        except Exception as e:
            print(f"[WARNING]  Native chunk data access error: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get chunk processing statistics."""
        return {
            'images_processed': self.image_count,
            **self.chunk_statistics
        }


def check_chunk_support(camera: pylon.InstantCamera) -> bool:
    """Check if the camera supports chunk features."""
    try:
        if hasattr(camera, 'ChunkModeActive') and genicam.IsWritable(camera.ChunkModeActive):
            return True
        else:
            print("[ERROR] Camera doesn't support chunk features")
            return False
    except Exception as e:
        print(f"[ERROR] Error checking chunk support: {e}")
        return False


def configure_chunk_features(camera: pylon.InstantCamera) -> Dict[str, bool]:
    """
    Configure various chunk features on the camera.
    
    Returns:
        Dict of chunk features and their enable status
    """
    chunk_status = {
        'timestamp': False,
        'framecounter': False,
        'crc': False
    }
    
    try:
        print("[CONFIG] Configuring chunk features...")
        
        # Enable chunk mode
        camera.ChunkModeActive.Value = True
        print("   [SUCCESS] Chunk mode activated")
        
        # Configure timestamp chunk
        try:
            camera.ChunkSelector.Value = "Timestamp"
            camera.ChunkEnable.Value = True
            chunk_status['timestamp'] = True
            print("   [SUCCESS] Timestamp chunk enabled")
        except Exception as e:
            print(f"   [WARNING]  Timestamp chunk could not be enabled: {e}")
        
        # Configure frame counter chunk (may not be available on all cameras)
        try:
            camera.ChunkSelector.Value = "Framecounter"
            camera.ChunkEnable.Value = True
            chunk_status['framecounter'] = True
            print("   [SUCCESS] Frame counter chunk enabled")
        except Exception as e:
            print("   [INFO]  Frame counter chunk not available (normal for some cameras)")
        
        # Configure CRC checksum chunk
        try:
            camera.ChunkSelector.Value = "PayloadCRC16"
            camera.ChunkEnable.Value = True
            chunk_status['crc'] = True
            print("   [SUCCESS] CRC checksum chunk enabled")
        except Exception as e:
            print(f"   [WARNING]  CRC checksum chunk could not be enabled: {e}")
        
        return chunk_status
        
    except Exception as e:
        print(f"[ERROR] Error configuring chunk features: {e}")
        return chunk_status


def disable_chunk_mode(camera: pylon.InstantCamera) -> None:
    """Disable chunk mode on the camera."""
    try:
        print("\n[CONFIG] Disabling chunk mode...")
        camera.ChunkModeActive.Value = False
        print("   [SUCCESS] Chunk mode disabled")
    except Exception as e:
        print(f"   [ERROR] Error disabling chunk mode: {e}")


def optimize_chunk_performance(camera: pylon.InstantCamera) -> None:
    """
    Optimize performance for chunk data processing.
    
    Creating node maps for each grab result can be time-consuming.
    Pre-creating a static pool of node maps can improve performance.
    """
    try:
        print("[CONFIG] Optimizing chunk performance...")
        
        # Set static chunk node map pool size to match buffer count
        if hasattr(camera, 'StaticChunkNodeMapPoolSize') and hasattr(camera, 'MaxNumBuffer'):
            camera.StaticChunkNodeMapPoolSize.Value = camera.MaxNumBuffer.Value
            print(f"   [SUCCESS] Static chunk node map pool size set to {camera.MaxNumBuffer.Value}")
        else:
            print("   [INFO]  Static chunk node map pool not available")
            
    except Exception as e:
        print(f"   [WARNING]  Performance optimization failed: {e}")


def validate_chunk_data(grab_result: pylon.GrabResult) -> bool:
    """
    Validate chunk data integrity and format.
    
    Returns:
        bool: True if chunk data is valid
    """
    try:
        # Check payload type
        if grab_result.PayloadType != pylon.PayloadType_ChunkData:
            print(f"[ERROR] Unexpected payload type: {grab_result.PayloadType}")
            return False
        
        # Check CRC if available
        if grab_result.HasCRC():
            if grab_result.CheckCRC():
                print("[SUCCESS] CRC validation passed")
                return True
            else:
                print("[ERROR] CRC validation failed - image data may be corrupted!")
                return False
        else:
            print("[INFO]  CRC not available for this grab result")
            return True
            
    except Exception as e:
        print(f"[ERROR] Error validating chunk data: {e}")
        return False


def display_image_info(grab_result: pylon.GrabResult) -> None:
    """Display basic image information."""
    try:
        print(f"[IMAGE] Image Info:")
        print(f"   Size: {grab_result.Width}x{grab_result.Height}")
        print(f"   Format: {grab_result.PixelType}")
        print(f"   Buffer Size: {grab_result.ImageSize} bytes")
        
        # Display first pixel value as example
        if grab_result.ImageSize > 0:
            image_buffer = grab_result.GetArray()
            if image_buffer is not None and len(image_buffer) > 0:
                print(f"   First Pixel Value: {image_buffer.flat[0]}")
        
    except Exception as e:
        print(f"[WARNING]  Error displaying image info: {e}")


def main() -> int:
    """
    Main function demonstrating chunk image processing.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Chunk Image Sample ===")
        print("This sample demonstrates chunk data processing in pypylon.")
        print("Chunk data provides additional metadata alongside image data.\n")
        
        # Create camera instance
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        print(f"Serial Number: {camera.GetDeviceInfo().GetSerialNumber()}")
        
        # Create chunk image event handler
        chunk_handler = ChunkImageEventHandler("ChunkProcessor")
        
        # Register image event handler
        camera.RegisterImageEventHandler(chunk_handler, 
                                       pylon.RegistrationMode_Append, 
                                       pylon.Cleanup_Delete)
        
        # Open camera
        camera.Open()
        
        # Check chunk support
        if not check_chunk_support(camera):
            camera.Close()
            return 1
        
        # Optimize chunk performance
        optimize_chunk_performance(camera)
        
        # Configure chunk features
        chunk_status = configure_chunk_features(camera)
        
        # Verify at least one chunk feature is enabled
        if not any(chunk_status.values()):
            print("[ERROR] No chunk features could be enabled")
            camera.Close()
            return 1
        
        # Start grabbing images
        images_to_grab = 5
        print(f"\n[START] Starting to grab {images_to_grab} images with chunk data...")
        print("[INFO] Chunk data will be processed and displayed.\n")
        
        camera.StartGrabbingMax(images_to_grab)
        
        # Process images with chunk data
        while camera.IsGrabbing():
            try:
                # Retrieve grab result
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                
                if grab_result.GrabSucceeded():
                    # Display basic image information
                    display_image_info(grab_result)
                    
                    # Validate chunk data
                    if validate_chunk_data(grab_result):
                        print("[SUCCESS] Chunk data validation passed")
                    else:
                        print("[WARNING]  Chunk data validation issues detected")
                    
                    # The OnImageGrabbed event handler will process the chunk data
                    
                else:
                    print(f"[ERROR] Grab failed: {grab_result.ErrorCode} - {grab_result.ErrorDescription}")
                
                # Release grab result
                grab_result.Release()
                
            except pylon.TimeoutException:
                print("⏰ Timeout waiting for image")
                break
            except Exception as e:
                print(f"[ERROR] Error during grabbing: {e}")
                break
        
        # Disable chunk mode
        disable_chunk_mode(camera)
        
        # Close camera
        camera.Close()
        
        # Display statistics
        print("\n" + "=" * 50)
        print("CHUNK DATA STATISTICS")
        print("=" * 50)
        stats = chunk_handler.get_statistics()
        print(f"Images Processed: {stats['images_processed']}")
        print(f"Timestamp Chunks: {stats['timestamp_count']}")
        print(f"Frame Counter Chunks: {stats['framecounter_count']}")
        print(f"CRC Chunks: {stats['crc_count']}")
        print(f"CRC Errors: {stats['crc_errors']}")
        
        print(f"\nChunk Features Status:")
        for feature, enabled in chunk_status.items():
            status = "[SUCCESS]" if enabled else "[ERROR]"
            print(f"  {feature.title()}: {status}")
        
        print("\nChunk image processing demonstration completed successfully!")
        print("\nNote: Chunk data provides valuable metadata for synchronization,")
        print("      timing analysis, and data integrity verification.")
        
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