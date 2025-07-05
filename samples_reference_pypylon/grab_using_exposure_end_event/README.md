# Exposure End Event Sample

## Description

This sample demonstrates how to use the Exposure End event to speed up image acquisition and enable faster processing workflows. When a sensor exposure finishes, the camera can send an Exposure End event to the computer before the image data transfer is complete, enabling immediate processing decisions and reducing system latency.

## Equivalent C++ Sample

`samples_reference_c++/Grab_UsingExposureEndEvent/`

## Prerequisites

- pypylon
- Basler camera supporting exposure end events
- Understanding of camera events and timing concepts

**Note**: pypylon has limited exposure end event support compared to the C++ API. This sample demonstrates the concepts and timing benefits through simulation.

## Usage

```bash
python grab_using_exposure_end_event.py
```

## Key Features Demonstrated

### 1. **Exposure End Event Handling**
- Event configuration and registration
- Frame number tracking and synchronization
- SFNC version compatibility (1.x vs 2.0+)
- Event timing analysis and logging

### 2. **Workflow Optimization**
- Immediate processing decisions after exposure
- Overlapping exposure and processing
- Reduced latency in time-critical applications
- Move action triggering based on exposure completion

### 3. **Timing Analysis**
- Event vs image receipt timing comparison
- Performance measurement and logging
- Pattern analysis and insights
- Speed benefit quantification

### 4. **Frame Synchronization**
- Frame number tracking across events
- Lost event detection and handling
- Event sequence validation
- Multi-threaded event processing

### 5. **Production Line Simulation**
- Move action triggering
- Object/sensor positioning control
- Time-critical decision making
- Real-time workflow optimization

## Code Highlights

### Event Handler Implementation
```python
class ExposureEndEventHandler:
    def handle_exposure_end_event(self, camera):
        frame_number = self.get_exposure_end_frame_number(camera)
        self.timing_analyzer.log_event(EventType.EXPOSURE_END, frame_number)
        
        # Trigger move action immediately
        if frame_number == self.next_frame_for_move:
            self.trigger_move_action(frame_number)
```

### Timing Analysis
```python
def analyze_patterns(self):
    # Calculate exposure→image delays
    for exp_event in exposure_events:
        for img_event in image_events:
            if img_event.frame_number == exp_event.frame_number:
                delay = (img_event.timestamp - exp_event.timestamp) * 1000
                delays.append(delay)
```

### Event Configuration
```python
def configure_exposure_end_events(self):
    # Select exposure end event
    camera.EventSelector.Value = "ExposureEnd"
    # Enable event notification
    camera.EventNotification.Value = "On"
    # Enable camera event processing
    camera.GrabCameraEvents = True
```

### Frame Number Handling
```python
def increment_frame_number(self, frame_number):
    frame_number += 1
    # GigE cameras don't use frame number 0
    if self.is_gige and frame_number == 0:
        frame_number = 1
    return frame_number
```

## Sample Output

```
=== Exposure End Event Sample ===
This sample demonstrates how to use exposure end events
to speed up image acquisition and processing workflows.

[CONFIG] Benefits of Exposure End Events:
   • Faster response times by not waiting for image transfer
   • Immediate processing decisions after exposure completes
   • Optimized throughput by overlapping exposure and processing
   • Reduced latency in time-critical applications

[CONFIG] Setting up camera for exposure end events...
Using device: Basler acA1920-40gm
Serial Number: 12345678
Camera type: USB
SFNC Version: 2.0+
[SUCCESS] Camera setup complete

[CONFIG] Configuring exposure end events...
   [CONFIG] Exposure end event selected
   [NOTIFY] Event notification enabled
[SUCCESS] Exposure end events configured

[START] Starting exposure end event demonstration (10 images)...

[TARGET] Exposure End Event: Frame 1
[IMAGE] Image Received: Frame 1, Size: 1920x1080
[ACTION] Move Action Triggered: Frame 1
   [RUN] Move action executed for frame 1
   [PIN] Object/sensor can be moved now (before image transfer completes)

============================================================
TIMING ANALYSIS
============================================================
Time [ms]    Event                Frame #    Details
------------------------------------------------------------
    0.00ms (  0.00) ExposureEnd          1          Exposure complete
    1.25ms (  1.25) MoveAction           1          Move triggered
   12.45ms ( 11.20) ImageReceived        1          Image transferred

[INFO] PATTERN ANALYSIS:
   Exposure→Image Delay: avg=12.45ms, min=10.20ms, max=15.30ms
   Speed benefit: 12.45ms faster response using exposure end events
   Exposure→Move Delay: avg=1.25ms
```

## Important Notes

### pypylon API Limitations
- **Limited Event Support**: pypylon doesn't provide the same level of camera event support as the C++ API
- **Simulation Approach**: This sample demonstrates concepts through simulation
- **Timing Benefits**: Shows the theoretical timing advantages of exposure end events

### SFNC Version Differences
- **SFNC 2.0+**: Uses `EventExposureEndFrameID`
- **SFNC 1.x**: Uses `ExposureEndEventFrameID`
- **Parameter Names**: Different event parameter names between versions

### Camera Type Considerations
- **GigE Cameras**: Frame numbers start at 1, never use 0
- **USB Cameras**: Frame numbers can start at 0
- **Event Support**: Not all cameras support exposure end events

### Timing Precision
- **Hardware Events**: Actual events provide microsecond precision
- **Software Simulation**: Simulation shows millisecond-level timing
- **Network Latency**: GigE cameras may have network-related delays

## Applications

### High-Speed Production Lines
```python
def production_line_controller(frame_number):
    """Control production line based on exposure completion."""
    # Move conveyor belt immediately after exposure
    conveyor.move_to_next_position()
    # Trigger external inspection systems
    inspection_system.start_analysis()
    # Update production counters
    production_counter.increment()
```

### Quality Control Systems
```python
def quality_control_trigger(frame_number):
    """Trigger quality control based on exposure end."""
    # Start defect detection immediately
    defect_detector.analyze_exposure(frame_number)
    # Prepare rejection mechanism
    rejection_system.prepare_for_frame(frame_number)
```

### Motion Control Systems
```python
def motion_control_handler(frame_number):
    """Handle motion control based on exposure timing."""
    # Update robot position
    robot_arm.move_to_next_position()
    # Synchronize with external triggers
    external_trigger.fire_after_exposure(frame_number)
```

### Real-Time Sorting
```python
def sorting_system_trigger(frame_number):
    """Control sorting system based on exposure end."""
    # Prepare sorting decision
    sorter.prepare_decision(frame_number)
    # Update tracking system
    object_tracker.update_position(frame_number)
```

## Performance Benefits

### Timing Advantages
```
Traditional Workflow:
Exposure → Image Transfer → Processing → Action
Total Time: Exposure + Transfer + Processing + Action

Optimized Workflow:
Exposure → Action (immediate)
Parallel:  Image Transfer → Processing
Total Time: max(Exposure + Action, Transfer + Processing)
```

### Latency Reduction
- **Immediate Response**: Actions start as soon as exposure completes
- **Parallel Processing**: Image transfer happens while actions execute
- **Throughput Increase**: Reduced cycle time per operation
- **System Efficiency**: Better resource utilization

## Troubleshooting

### Event Not Supported
```python
if not hasattr(camera, 'EventSelector'):
    print("Camera doesn't support events")
    # Fall back to traditional timing methods
    use_traditional_workflow()
```

### Event Configuration Issues
```python
try:
    camera.EventSelector.Value = "ExposureEnd"
    camera.EventNotification.Value = "On"
except genicam.AccessException:
    print("Could not configure exposure end events")
    # Check camera documentation for supported events
```

### Frame Number Mismatches
```python
# Handle frame number synchronization issues
if frame_number != expected_frame_number:
    print(f"Frame mismatch: expected {expected_frame_number}, got {frame_number}")
    # Resynchronize frame tracking
    resync_frame_numbers(frame_number)
```

### Timing Variations
```python
# Monitor timing consistency
timing_variations = analyze_event_timing()
if timing_variations > threshold:
    print("High timing variation detected")
    # Adjust timing expectations or increase buffers
```

## Advanced Usage

### Multi-Camera Synchronization
```python
class MultiCameraEventHandler:
    def __init__(self, cameras):
        self.cameras = cameras
        self.event_sync = EventSynchronizer()
    
    def handle_exposure_end(self, camera_id, frame_number):
        # Synchronize events across multiple cameras
        self.event_sync.register_event(camera_id, frame_number)
        if self.event_sync.all_cameras_ready():
            self.trigger_synchronized_action()
```

### Adaptive Timing
```python
class AdaptiveTimingController:
    def __init__(self):
        self.timing_history = []
        self.adaptation_threshold = 5.0  # ms
    
    def adapt_timing(self, measured_delay):
        self.timing_history.append(measured_delay)
        if len(self.timing_history) > 10:
            avg_delay = sum(self.timing_history[-10:]) / 10
            if abs(avg_delay - self.expected_delay) > self.adaptation_threshold:
                self.adjust_timing_parameters(avg_delay)
```

### Event Filtering
```python
class EventFilter:
    def __init__(self, filter_criteria):
        self.criteria = filter_criteria
    
    def should_process_event(self, event_type, frame_number):
        # Filter events based on specific criteria
        if event_type == EventType.EXPOSURE_END:
            return frame_number % self.criteria.frame_interval == 0
        return True
```

## Related Samples

- `grab_camera_events/` - General camera event handling
- `grab_chunk_image/` - Chunk data with timing information
- `grab_strategies/` - Different grabbing strategies
- Real-time processing samples

## Technical Details

### Event Timing Flow
```
Camera Sensor:     [Exposure Start] -------- [Exposure End] -------- [Readout Complete]
Camera Events:                               ↑ Event Sent
Image Transfer:                                                      ↑ Transfer Start → Complete
Action Trigger:                              ↑ Immediate Action
```

### Performance Metrics
- **Event Latency**: Time from exposure end to event receipt
- **Action Latency**: Time from event receipt to action execution
- **Transfer Overlap**: Percentage of transfer time overlapped with actions
- **Throughput Gain**: Improvement in frames processed per second

### System Integration
- **Hardware Triggers**: Integration with external trigger systems
- **Motion Control**: Synchronization with robotic systems
- **Quality Systems**: Integration with inspection equipment
- **Production Control**: Interface with manufacturing execution systems

This sample provides a comprehensive foundation for implementing exposure end event handling to optimize acquisition workflows in pypylon applications, demonstrating significant timing advantages for time-critical systems. 