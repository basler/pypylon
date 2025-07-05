# Camera Events Sample

## Description

This sample demonstrates how to register and handle camera events in pypylon. Camera events provide real-time notifications about camera states and operations, allowing applications to respond to camera occurrences independently of image grabbing.

## Equivalent C++ Sample

`samples_reference_c++/Grab_CameraEvents/`

## Prerequisites

- pypylon
- Basler camera (USB3 Vision, GigE Vision, or Camera Link)
- Camera supporting event notifications

## Usage

```bash
python grab_camera_events.py
```

## Key Features Demonstrated

### 1. **Camera Event Handler Classes**
- `SampleCameraEventHandler`: Processes specific camera events with event type distinction
- `DetailedCameraEventHandler`: Provides comprehensive event information extraction
- `SampleImageEventHandler`: Demonstrates image event handling alongside camera events

### 2. **Event Types Supported**
- **Exposure End Events**: Notification when sensor exposure completes
  - Event data: Frame ID, Timestamp
  - Available before image data transfer completes
- **Event Overrun Events**: Warning when events are being dropped due to high frequency
  - Indicates insufficient bandwidth for event processing

### 3. **SFNC Version Compatibility**
- **SFNC 2.0+** (USB cameras): Uses `EventExposureEndData`, `EventExposureEndFrameID`, `EventExposureEndTimestamp`
- **SFNC 1.x** (GigE cameras): Uses `ExposureEndEventData`, `ExposureEndEventFrameID`, `ExposureEndEventTimestamp`

### 4. **Event Registration Patterns**
- Multiple handlers for the same event
- Event-specific user IDs for handler distinction
- Individual node-based event registration

### 5. **Event Configuration**
- Event support detection
- Event activation/deactivation
- Different notification modes (`On`, `GenICamEvent`)

## Code Highlights

### Event Handler Implementation
```python
class SampleCameraEventHandler(pylon.CameraEventHandler):
    def OnCameraEvent(self, camera, userProvidedId, node):
        if userProvidedId == EventID.EXPOSURE_END:
            # Access event data based on SFNC version
            if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
                frame_id = camera.EventExposureEndFrameID.Value
                timestamp = camera.EventExposureEndTimestamp.Value
            else:
                frame_id = camera.ExposureEndEventFrameID.Value
                timestamp = camera.ExposureEndEventTimestamp.Value
```

### Event Registration
```python
# Enable camera event processing
camera.GrabCameraEvents.Value = True

# Register handlers for different event data nodes
camera.RegisterCameraEventHandler(handler, "EventExposureEndData", 
                                EventID.EXPOSURE_END, 
                                pylon.RegistrationMode_ReplaceAll, 
                                pylon.Cleanup_None)
```

### Event Configuration
```python
# Configure Exposure End events
camera.EventSelector.Value = "ExposureEnd"
camera.EventNotification.Value = "On"  # or "GenICamEvent"
```

## Sample Output

```
=== Camera Events Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678
[SUCCESS] Camera event processing enabled

[CONFIG] Registering camera event handlers...
   📡 Using SFNC 2.0+ event parameters
   [SUCCESS] Camera event handlers registered successfully

[CONFIG] Configuring Exposure End events...
   [SUCCESS] Exposure End events enabled with 'On'

[START] Starting to grab 5 images...
[IMAGE] Camera events will be displayed as they occur.

🖼️  Image 1 grabbed: 1920x1080

[MainEventHandler] Camera Event Received
========================================
[IMAGE] Exposure End Event (SFNC 2.0+)
   Frame ID: 1
   Timestamp: 1234567890123
   Event Count: 1

[DetailedEventHandler] Event #1
Device: Basler acA1920-40gm
User ID: 100
Node Name: EventExposureEndFrameID
Node Value: 1

EVENT STATISTICS
==================================================
Exposure End Events: 5
Event Overrun Events: 0
Images Grabbed: 5
Total Event Callbacks: 10
```

## Important Notes

### Event Processing
- **Must Enable**: `camera.GrabCameraEvents.Value = True` (disabled by default)
- **Performance**: Event handlers should perform minimal processing to avoid blocking
- **Threading**: Event callbacks run in separate threads

### SFNC Version Handling
- **USB Cameras**: Typically use SFNC 2.0+ parameters
- **GigE Cameras**: Often use SFNC 1.x parameters
- **Detection**: Use `camera.GetSfncVersion()` to determine appropriate parameters

### Event Timing
- Events can arrive before corresponding image data
- Useful for synchronization and real-time monitoring
- Independent of image grabbing operations

### Camera-Specific Behavior
- Not all cameras support all event types
- Event Overrun typically available on GigE cameras
- Some cameras use different notification modes

## Troubleshooting

### Events Not Received
1. **Check Event Support**: Ensure camera supports events
2. **Enable Processing**: Set `camera.GrabCameraEvents.Value = True`
3. **Verify Configuration**: Check event selector and notification settings
4. **SFNC Version**: Use correct parameter names for camera's SFNC version

### Event Overrun Warnings
- Indicates events are being dropped
- Reduce event frequency or increase processing speed
- Consider using event overrun as a monitoring mechanism

### Performance Issues
- Keep event handlers lightweight
- Avoid blocking operations in event callbacks
- Consider queuing events for later processing

## Applications

### Real-time Synchronization
- Coordinate with external systems
- Trigger processing based on exposure completion
- Monitor camera timing

### Quality Control
- Detect event overruns indicating system stress
- Monitor frame rates and timing
- Implement error detection and recovery

### Advanced Triggering
- Implement complex trigger sequences
- Chain operations based on camera events
- Build state machines using event notifications

## Related Samples

- `grab_strategies/` - Basic image grabbing strategies
- `grab_using_exposure_end_event/` - Specific exposure end event usage
- `parametrize_camera_configurations/` - Camera configuration management

This sample provides a foundation for implementing sophisticated camera event handling in pypylon applications, enabling real-time monitoring and coordination with camera operations. 