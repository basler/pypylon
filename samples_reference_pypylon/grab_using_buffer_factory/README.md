# Custom Buffer Factory Sample

## Description

This sample demonstrates how to use a user-provided buffer factory for advanced buffer management. Using a buffer factory is optional and intended for advanced use cases only. A buffer factory is necessary when you want to grab into externally supplied buffers, such as those from other image processing libraries or custom memory management systems.

## Equivalent C++ Sample

`samples_reference_c++/Grab_UsingBufferFactory/`

## Prerequisites

- pypylon
- numpy (for buffer management)
- Basic understanding of memory management concepts

**Note**: This is an advanced feature for specialized use cases. Most applications should use the default buffer management provided by pypylon.

## Usage

```bash
python grab_using_buffer_factory.py
```

## Key Features Demonstrated

### 1. **Custom Buffer Factory Implementation**
- Custom buffer allocation strategies
- Buffer context tracking and management
- Thread-safe buffer operations
- Memory usage statistics and monitoring

### 2. **External Buffer Integration**
- Integration with external image processing libraries
- Custom memory management schemes
- Zero-copy operations with other systems
- Specialized buffer allocation strategies

### 3. **Advanced Memory Management**
- Memory pool management
- Buffer lifecycle tracking
- Aligned memory allocation
- Resource cleanup and garbage collection

### 4. **Buffer Context Management**
- Unique buffer identification
- Usage statistics tracking
- Buffer state management
- Context-based buffer retrieval

### 5. **Integration Patterns**
- External library buffer sharing
- Memory pool implementations
- Custom allocation strategies
- Performance optimization techniques

## Important Note

[WARNING] **pypylon API Limitation**: Unlike the C++ pylon API, pypylon doesn't directly support custom buffer factories through the `SetBufferFactory()` method. This sample demonstrates the concepts and shows how custom buffer management would work, serving as a foundation for understanding advanced buffer management patterns.

## Code Highlights

### Custom Buffer Factory Class
```python
class CustomBufferFactory:
    def __init__(self, max_buffers=10, alignment=32):
        self.max_buffers = max_buffers
        self.alignment = alignment
        self.buffers = {}
        self.buffer_lock = threading.Lock()
    
    def allocate_buffer(self, size):
        buffer_array = np.zeros(size, dtype=np.uint8)
        buffer_context = self.next_buffer_id
        self.buffers[buffer_context] = BufferInfo(buffer_context, size, buffer_array)
        return buffer_array, buffer_context
```

### Buffer Information Tracking
```python
class BufferInfo:
    def __init__(self, buffer_id, size, buffer_data):
        self.buffer_id = buffer_id
        self.size = size
        self.buffer_data = buffer_data
        self.allocated_time = time.time()
        self.usage_count = 0
```

### Thread-Safe Operations
```python
def free_buffer(self, buffer_context):
    with self.buffer_lock:
        if buffer_context in self.buffers:
            buffer_info = self.buffers[buffer_context]
            self.current_memory -= buffer_info.size
            del self.buffers[buffer_context]
```

### External Library Integration
```python
# Example: OpenCV integration
opencv_buffers = []
for i in range(3):
    buffer_array, buffer_context = buffer_factory.allocate_buffer(1920 * 1080)
    opencv_buffers.append((buffer_array, buffer_context))
    # Use buffer_array with OpenCV processing
```

## Sample Output

```
=== Custom Buffer Factory Sample ===
This sample demonstrates advanced buffer management
using a custom buffer factory implementation.

[WARNING]  Note: pypylon doesn't directly support custom buffer factories
   like the C++ API. This sample demonstrates the concepts and
   shows how custom buffer management would work.

[CONFIG] Setting up camera with custom buffer factory...
Using device: Basler acA1920-40gm
Serial Number: 12345678
📷 Camera configured for buffer factory demonstration
[SUCCESS] Camera setup complete

[START] Starting grab with buffer factory (5 images)...
📏 Estimated image size: 2073600 bytes (1920x1080)
📦 Allocated buffer 1000: 2073600 bytes
   Active buffers: 1
   Current memory: 1.98 MB
📦 Allocated buffer 1001: 2073600 bytes
   Active buffers: 2
   Current memory: 3.96 MB
📦 Pre-allocated 5 buffers

🖼️  Image 1:
   📏 Size: 1920x1080
   📦 Buffer Context: 1000
   [INFO] Buffer Usage: 1
   [STATS] Mean Intensity: 127.5

🖼️  Image 2:
   📏 Size: 1920x1080
   📦 Buffer Context: 1001
   [INFO] Buffer Usage: 1
   [STATS] Mean Intensity: 128.2

[SUCCESS] Grab complete: 5/5 images

[INFO] Buffer Factory Statistics:
   Total Allocated: 5
   Total Freed: 5
   Active Buffers: 0
   Current Memory Mb: 0.00
   Peak Memory Mb: 9.89
   Max Buffers: 5
```

## Applications

### Real-Time Processing Pipelines
```python
# Integration with real-time processing
class RTProcessingBufferFactory(CustomBufferFactory):
    def allocate_buffer(self, size):
        # Allocate buffers optimized for real-time processing
        buffer_array = np.zeros(size, dtype=np.uint8, order='C')
        # Pin memory for GPU transfer
        return buffer_array, self.next_buffer_id
```

### GPU Processing Integration
```python
# Example: CUDA buffer integration
class CUDABufferFactory(CustomBufferFactory):
    def allocate_buffer(self, size):
        # Allocate CUDA-compatible buffers
        buffer_array = cuda.pinned_array(size, dtype=np.uint8)
        return buffer_array, self.next_buffer_id
```

### Memory Pool Management
```python
# Pre-allocated memory pools
class PooledBufferFactory(CustomBufferFactory):
    def __init__(self, pool_size=10, buffer_size=1920*1080):
        super().__init__()
        self.pool = [np.zeros(buffer_size, dtype=np.uint8) 
                     for _ in range(pool_size)]
        self.available_buffers = list(range(pool_size))
```

## Advanced Usage Patterns

### External Library Integration
```python
# OpenCV integration example
def integrate_with_opencv(buffer_factory):
    # Allocate buffer compatible with OpenCV
    buffer_array, context = buffer_factory.allocate_buffer(1920 * 1080)
    
    # Use with OpenCV
    cv_image = buffer_array.reshape((1080, 1920))
    processed = cv2.GaussianBlur(cv_image, (5, 5), 0)
    
    # Return buffer to factory
    buffer_factory.free_buffer(context)
```

### Custom Memory Alignment
```python
def allocate_aligned_buffer(size, alignment=64):
    """Allocate buffer with specific alignment requirements."""
    # Ensure proper alignment for SIMD operations
    buffer = np.zeros(size + alignment - 1, dtype=np.uint8)
    aligned_ptr = buffer.ctypes.data
    offset = aligned_ptr % alignment
    if offset:
        aligned_ptr += alignment - offset
    return buffer, aligned_ptr
```

### Zero-Copy Operations
```python
class ZeroCopyBufferFactory(CustomBufferFactory):
    """Buffer factory optimized for zero-copy operations."""
    
    def allocate_shared_buffer(self, size):
        """Allocate shared memory buffer."""
        # Use shared memory for zero-copy between processes
        shared_buffer = mmap.mmap(-1, size)
        return shared_buffer, self.next_buffer_id
```

## Performance Considerations

### Memory Alignment
- Align buffers to cache line boundaries (64 bytes)
- Use appropriate alignment for SIMD operations
- Consider NUMA topology for multi-CPU systems

### Buffer Reuse
- Implement buffer pools to reduce allocation overhead
- Pre-allocate buffers during initialization
- Reuse buffers for similar-sized images

### Thread Safety
- Use proper locking mechanisms for buffer management
- Consider lock-free data structures for high-performance scenarios
- Minimize contention between allocation and deallocation

## Troubleshooting

### Memory Issues
```python
# Monitor memory usage
def check_memory_usage(buffer_factory):
    stats = buffer_factory.get_statistics()
    if stats['current_memory_mb'] > 100:  # 100MB threshold
        print("Warning: High memory usage detected")
```

### Buffer Leaks
```python
# Detect buffer leaks
def detect_buffer_leaks(buffer_factory):
    stats = buffer_factory.get_statistics()
    if stats['total_allocated'] != stats['total_freed']:
        leak_count = stats['total_allocated'] - stats['total_freed']
        print(f"Warning: {leak_count} buffers not freed")
```

### Performance Optimization
```python
# Profile buffer operations
import cProfile

def profile_buffer_operations():
    profiler = cProfile.Profile()
    profiler.enable()
    # Run buffer operations
    profiler.disable()
    profiler.print_stats()
```

## Integration Examples

### NumPy Integration
```python
def create_numpy_compatible_buffer(width, height, dtype=np.uint8):
    """Create buffer compatible with NumPy operations."""
    size = width * height * np.dtype(dtype).itemsize
    buffer_array, context = buffer_factory.allocate_buffer(size)
    # Reshape for NumPy operations
    numpy_view = buffer_array.view(dtype).reshape((height, width))
    return numpy_view, context
```

### OpenCV Integration
```python
def create_opencv_compatible_buffer(width, height, channels=1):
    """Create buffer compatible with OpenCV operations."""
    size = width * height * channels
    buffer_array, context = buffer_factory.allocate_buffer(size)
    # Create OpenCV-compatible view
    cv_image = buffer_array.reshape((height, width, channels))
    return cv_image, context
```

### PIL/Pillow Integration
```python
def create_pil_compatible_buffer(width, height, mode='L'):
    """Create buffer compatible with PIL operations."""
    size = width * height * (3 if mode == 'RGB' else 1)
    buffer_array, context = buffer_factory.allocate_buffer(size)
    # Create PIL Image from buffer
    pil_image = Image.frombuffer(mode, (width, height), buffer_array)
    return pil_image, context
```

## Related Samples

- `grab/` - Basic image grabbing
- `grab_strategies/` - Different grabbing strategies
- `grab_multiple_cameras/` - Multi-camera buffer management
- Memory optimization samples

## Technical Details

### Buffer Lifecycle
```
Allocation → Usage → Release → Cleanup
     ↓         ↓        ↓        ↓
   Context   Tracking  Return   GC
```

### Memory Management
- Automatic garbage collection for unused buffers
- Reference counting for buffer usage
- Memory pool recycling strategies
- Peak memory usage tracking

### Thread Safety
- Thread-safe allocation/deallocation
- Atomic operations for counters
- Lock-free access patterns where possible
- Proper synchronization primitives

This sample provides a comprehensive foundation for implementing advanced buffer management strategies in pypylon applications, even though direct buffer factory support is not available in the Python API. 