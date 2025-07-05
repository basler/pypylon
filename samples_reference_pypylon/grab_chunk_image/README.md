# Chunk Image Sample

## Description

This sample demonstrates how to use chunk features with Basler cameras in pypylon. Chunk features allow cameras to append additional metadata to image data, such as timestamps, frame counters, and CRC checksums. This metadata is transferred as separate "chunks" alongside the image data, providing valuable information for synchronization, timing analysis, and data integrity verification.

## Equivalent C++ Sample

`samples_reference_c++/Grab_ChunkImage/`

## Prerequisites

- pypylon
- Basler camera supporting chunk features
- Camera with chunk mode capability

## Usage

```bash
python grab_chunk_image.py
```

## Key Features Demonstrated

### 1. **Chunk Mode Configuration**
- Enable chunk mode on the camera
- Configure specific chunk features (timestamp, frame counter, CRC)
- Validate chunk support before processing

### 2. **Chunk Data Access Methods**
- **Generic Access**: Via chunk data node map (works with all grab result types)
- **Native Access**: Via grab result members (recommended for device-specific results)

### 3. **Chunk Feature Types**
- **Timestamp Chunks**: Precise timing information for each image
- **Frame Counter Chunks**: Sequential frame numbering
- **CRC Checksum Chunks**: Data integrity verification

### 4. **Performance Optimization**
- Static chunk node map pool sizing
- Efficient chunk data processing
- Memory management for chunk operations

### 5. **Data Validation**
- Payload type verification
- CRC checksum validation
- Error handling for corrupted data

## Code Highlights

### Chunk Mode Configuration
```python
# Enable chunk mode
camera.ChunkModeActive.Value = True

# Configure timestamp chunk
camera.ChunkSelector.Value = "Timestamp"
camera.ChunkEnable.Value = True

# Configure CRC checksum chunk
camera.ChunkSelector.Value = "PayloadCRC16"
camera.ChunkEnable.Value = True
```

### Generic Chunk Data Access
```python
# Access via chunk data node map
chunk_node_map = grab_result.ChunkDataNodeMap
if genicam.IsAvailable(chunk_node_map.ChunkTimestamp):
    timestamp_node = chunk_node_map.ChunkTimestamp
    if genicam.IsReadable(timestamp_node):
        timestamp = timestamp_node.Value
```

### Native Chunk Data Access
```python
# Access via grab result members (recommended)
if hasattr(grab_result, 'ChunkTimestamp'):
    if genicam.IsReadable(grab_result.ChunkTimestamp):
        timestamp = grab_result.ChunkTimestamp.Value
```

### Performance Optimization
```python
# Optimize chunk performance with static node map pool
camera.StaticChunkNodeMapPoolSize.Value = camera.MaxNumBuffer.Value
```

### Data Validation
```python
# Validate payload type
if grab_result.PayloadType != pylon.PayloadType_ChunkData:
    print("Unexpected payload type")

# Validate CRC if available
if grab_result.HasCRC():
    if grab_result.CheckCRC():
        print("CRC validation passed")
    else:
        print("CRC validation failed!")
```

## Sample Output

```
=== Chunk Image Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678

[CONFIG] Configuring chunk features...
   [SUCCESS] Chunk mode activated
   [SUCCESS] Timestamp chunk enabled
   [INFO]  Frame counter chunk not available (normal for some cameras)
   [SUCCESS] CRC checksum chunk enabled

[CONFIG] Optimizing chunk performance...
   [SUCCESS] Static chunk node map pool size set to 10

[START] Starting to grab 5 images with chunk data...
[INFO] Chunk data will be processed and displayed.

[IMAGE] Image Info:
   Size: 1920x1080
   Format: Mono8
   Buffer Size: 2073600 bytes
   First Pixel Value: 128
[SUCCESS] CRC validation passed

[ChunkProcessor] Image 1 grabbed successfully
==================================================
[TIME] Timestamp (Generic): 1234567890123456
[TIME] Timestamp (Native): 1234567890123456
[SECURE] CRC16 (Native): 0x1A2B

CHUNK DATA STATISTICS
==================================================
Images Processed: 5
Timestamp Chunks: 5
Frame Counter Chunks: 0
CRC Chunks: 5
CRC Errors: 0

Chunk Features Status:
  Timestamp: [SUCCESS]
  Framecounter: [ERROR]
  Crc: [SUCCESS]
```

## Important Notes

### Chunk Feature Availability
- **Timestamp**: Available on most cameras
- **Frame Counter**: May not be available on USB cameras (they use generic counters)
- **CRC Checksum**: Available on most cameras for data integrity

### Performance Considerations
- **Node Map Creation**: Creating node maps for each grab result can be time-consuming
- **Static Pool**: Use `StaticChunkNodeMapPoolSize` to pre-create node maps
- **Memory Usage**: Chunk data increases memory usage per grab result

### Data Integrity
- **CRC Validation**: Use CRC chunks to verify data integrity
- **Payload Type**: Always verify payload type is `PayloadType_ChunkData`
- **Error Handling**: Implement robust error handling for chunk access

### Camera Compatibility
- **USB Cameras**: May not provide explicit frame counter chunks
- **GigE Cameras**: Typically support all chunk features
- **Emulated Cameras**: May have limited chunk support

## Troubleshooting

### Chunk Mode Not Supported
```python
# Check if camera supports chunk features
if not hasattr(camera, 'ChunkModeActive'):
    print("Camera doesn't support chunk features")
```

### Chunk Data Not Available
```python
# Always check readability before accessing
if genicam.IsReadable(grab_result.ChunkTimestamp):
    timestamp = grab_result.ChunkTimestamp.Value
else:
    print("Timestamp chunk not available")
```

### Performance Issues
```python
# Optimize with static node map pool
camera.StaticChunkNodeMapPoolSize.Value = camera.MaxNumBuffer.Value
```

### CRC Validation Failures
- Check camera connection quality
- Verify cable integrity
- Monitor for electrical interference
- Consider enabling error correction features

## Applications

### Multi-Camera Synchronization
- Use timestamp chunks for precise frame correlation
- Implement master-slave trigger relationships
- Synchronize multiple camera streams

### Quality Control
- CRC validation for industrial applications
- Data integrity verification in critical systems
- Automatic error detection and retry mechanisms

### Time-Critical Applications
- Precise timing for high-speed applications
- Trigger correlation with external events
- Performance monitoring and optimization

### Data Analysis
- Frame rate analysis using timestamps
- Temporal correlation of image sequences
- Statistical analysis of camera performance

## Advanced Usage

### Custom Chunk Processing
```python
class CustomChunkHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grab_result):
        if grab_result.GrabSucceeded():
            # Custom chunk processing logic
            self.process_custom_chunks(grab_result)
```

### Multiple Chunk Features
```python
# Enable multiple chunk features
chunk_features = ["Timestamp", "PayloadCRC16", "Width", "Height"]
for feature in chunk_features:
    try:
        camera.ChunkSelector.Value = feature
        camera.ChunkEnable.Value = True
    except Exception as e:
        print(f"Feature {feature} not available: {e}")
```

### Performance Monitoring
```python
# Monitor chunk processing performance
import time
start_time = time.time()
# ... chunk processing ...
processing_time = time.time() - start_time
```

## Related Samples

- `grab_camera_events/` - Camera event handling
- `grab_strategies/` - Different grabbing strategies
- `grab_using_buffer_factory/` - Custom buffer management

## Technical Details

### Chunk Data Structure
- First chunk: Always image data
- Subsequent chunks: Metadata based on enabled features
- Each chunk has header and payload sections

### Memory Layout
```
[Image Data Chunk][Timestamp Chunk][CRC Chunk]...
```

### Node Map Architecture
- Each grab result has associated chunk data node map
- Node maps provide GenICam parameter access
- Static pools improve performance by pre-creating maps

This sample provides a comprehensive foundation for implementing chunk data processing in pypylon applications, enabling precise timing, data integrity verification, and advanced camera synchronization capabilities. 