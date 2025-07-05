# Grab Using Grab Loop Thread Sample

## Description

This sample demonstrates how to use the grab loop thread provided by the InstantCamera class for multi-threaded image acquisition and processing. The grab loop thread handles image retrieval in the background while the main thread remains responsive for user interaction or other processing tasks.

## Equivalent C++ Sample

`samples_reference_c++/Grab_UsingGrabLoopThread/`

## Prerequisites

- pypylon
- Basler camera supporting frame trigger readiness queries
- Python threading support

## Usage

```bash
python grab_using_grab_loop_thread.py
```

## Key Features Demonstrated

### 1. **Grab Loop Thread Architecture**
- Background image acquisition using InstantCamera's grab loop thread
- Non-blocking image processing through event handlers
- Responsive main thread for user interaction
- Thread-safe processing with proper synchronization

### 2. **Multiple Event Handlers**
- Primary image processing handler with statistics
- Diagnostic handler for performance monitoring
- Event handler chaining for processing pipelines
- Thread-safe data collection and reporting

### 3. **Interactive Camera Control**
- Real-time camera triggering
- Statistics monitoring during operation
- Help system and user guidance
- Graceful shutdown handling

### 4. **Performance Monitoring**
- Frame rate calculation
- Processing time measurement
- Image statistics collection
- Memory usage optimization

### 5. **Thread Safety**
- Proper synchronization with locks
- Safe data access between threads
- Exception handling in multi-threaded environment

## Code Highlights

### Starting Grab Loop Thread
```python
# Start grabbing using the grab loop thread
# Images are processed automatically by event handlers
camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
```

### Image Event Handler
```python
class ImageProcessingEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grab_result):
        # This runs in the grab loop thread
        with self.lock:  # Thread-safe processing
            if grab_result.GrabSucceeded():
                # Process image data
                self.process_image(grab_result)
```

### Thread-Safe Statistics
```python
def get_statistics(self) -> dict:
    with self.lock:
        return {
            'total_images': self.image_count,
            'success_rate': self.success_rate,
            'avg_processing_time': self.avg_processing_time
        }
```

### Interactive Control
```python
# Non-blocking camera control
while True:
    user_input = input_handler.get_input()
    if user_input == 't':
        trigger_camera(camera)
    elif user_input == 'e':
        break
```

## Sample Output

```
=== Grab Loop Thread Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678

[CONFIG] Setting up camera configuration...
   [SUCCESS] Software trigger configuration registered

[CONFIG] Registering image event handlers...
   [SUCCESS] Image event handlers registered

[CONFIG] Starting grab loop thread...
   [SUCCESS] Grab loop thread started
   🔄 Images will be processed in background thread

============================================================
INTERACTIVE CAMERA CONTROL
============================================================
Commands:
  't' or 'T' - Trigger camera
  's' or 'S' - Show statistics
  'h' or 'H' - Show help
  'e' or 'E' - Exit
============================================================

Enter command (t/s/h/e): t
🔫 Triggering camera...
   [SUCCESS] Camera triggered successfully

🖼️  [PrimaryProcessor] Image 1 processed:
    📏 Size: 1920x1080
    🎨 Format: Mono8
    [INFO] Frame ID: 1
    ⏱️  Block ID: 0
    [STATS] Mean intensity: 127.5
    📉 Min/Max: 0/255
    [INFO] [DiagnosticMonitor] Frame rate: 15.2 FPS

FINAL STATISTICS
==================================================
Total Images: 5
Successful Grabs: 5
Failed Grabs: 0
Success Rate: 100.0%
Total Pixels Processed: 10,368,000
Average Processing Time: 0.012s
Total Processing Time: 0.058s
```

## Important Notes

### Grab Loop Thread Requirements
- **Frame Trigger Readiness**: Camera must support `CanWaitForFrameTriggerReady()`
- **Event Handlers**: Must register image event handlers for processing
- **Thread Safety**: All data access must be thread-safe

### Threading Architecture
- **Grab Loop Thread**: Handles image acquisition automatically
- **Event Handler Threads**: Process images in background
- **Main Thread**: Remains responsive for user interaction
- **Input Thread**: Handles user input non-blocking

### Performance Considerations
- **Processing Time**: Keep event handlers lightweight
- **Memory Usage**: Release grab results promptly
- **Synchronization**: Use locks judiciously to avoid bottlenecks

## Applications

### Real-time Processing
- Live image analysis while maintaining UI responsiveness
- Continuous monitoring applications
- Quality control systems with user interaction

### Interactive Applications
- Camera control software with live preview
- Scientific imaging applications
- Industrial inspection systems

### Processing Pipelines
- Multi-stage image processing
- Parallel processing chains
- Data collection with real-time feedback

## Troubleshooting

### Camera Not Supporting Grab Loop
```python
# Check if camera supports frame trigger readiness
if not camera.CanWaitForFrameTriggerReady():
    print("Camera doesn't support grab loop thread")
```

### Thread Safety Issues
```python
# Always use locks for shared data
with self.lock:
    self.shared_data = new_value
```

### Performance Problems
- Minimize processing in event handlers
- Use separate threads for heavy processing
- Consider using queues for inter-thread communication

### Memory Leaks
- Always release grab results: `grab_result.Release()`
- Stop grabbing before closing camera
- Properly clean up event handlers

## Advanced Usage

### Custom Processing Pipeline
```python
class CustomProcessingHandler(pylon.ImageEventHandler):
    def __init__(self):
        super().__init__()
        self.processing_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self._process_worker)
        self.processing_thread.start()
    
    def OnImageGrabbed(self, camera, grab_result):
        # Queue image for processing
        self.processing_queue.put(grab_result.GetArray())
    
    def _process_worker(self):
        while True:
            image = self.processing_queue.get()
            # Perform heavy processing
            self.process_image(image)
```

### Multiple Camera Support
```python
# Multiple cameras can each have their own grab loop thread
camera1.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
camera2.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)
```

### Error Recovery
```python
class RobustEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grab_result):
        try:
            self.process_image(grab_result)
        except Exception as e:
            self.handle_error(e)
            # Continue processing other images
```

## Related Samples

- `grab_strategies/` - Different grabbing strategies
- `grab_camera_events/` - Camera event handling
- `grab_multiple_cameras/` - Multi-camera handling

## Technical Details

### Thread Architecture
```
Main Thread          Grab Loop Thread       Event Handler Thread
     |                        |                        |
     ├─ User Input            ├─ Image Acquisition     ├─ Image Processing
     ├─ Statistics            ├─ Buffer Management     ├─ Statistics Update
     └─ Control Flow          └─ Event Triggering      └─ Data Analysis
```

### Event Flow
1. User triggers camera
2. Grab loop thread acquires image
3. Image event handlers process result
4. Statistics updated thread-safely
5. Main thread remains responsive

### Memory Management
- Grab results are automatically managed
- Event handlers should not store grab results
- Use `GetArray()` to copy image data if needed

This sample provides a comprehensive foundation for implementing responsive, multi-threaded image acquisition applications using pypylon's grab loop thread functionality. 