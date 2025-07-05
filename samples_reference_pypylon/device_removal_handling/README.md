# Device Removal Handling Sample

## Description
This sample demonstrates how to handle device removal and reconnection events when using Basler cameras. It shows how to implement robust camera applications that can gracefully handle camera disconnections and automatically attempt reconnections.

Device removal can occur due to:
- USB cable disconnection/reconnection
- Network cable disconnection (GigE cameras)
- Power supply issues
- System USB port problems
- Camera overheating protection

This sample shows how to:
- Detect device removal events during operation
- Implement automatic reconnection strategies
- Properly clean up resources during disconnection
- Maintain operation statistics and status information
- Handle errors gracefully without crashing the application
- Provide user feedback about connection status

## Equivalent C++ Sample
`samples_reference_c++/DeviceRemovalHandling/`

## Prerequisites
- pypylon
- A Basler camera (USB or GigE)

## Usage
```bash
python device_removal_handling.py
```

[IDEA] **Testing Device Removal**: To test the device removal handling, simply disconnect and reconnect the camera cable while the sample is running.

## Key Features Demonstrated

### 1. Device Removal Detection
- Automatic detection of camera disconnection during operations
- Error handling for grab operations when device is removed
- Graceful handling of timeout and communication errors

### 2. Automatic Reconnection
- Background thread for reconnection attempts
- Configurable retry logic with maximum attempt limits
- Device availability checking before reconnection attempts
- Automatic resumption of grabbing after successful reconnection

### 3. Resource Management
- Proper cleanup of camera resources during disconnection
- Thread-safe operations using locks
- Memory management for grab results and camera instances

### 4. Status Monitoring
- Real-time connection status tracking
- Operation statistics (images grabbed, disconnections, reconnections)
- Periodic status display during operation

### 5. Error Recovery
- Robust error handling for various failure scenarios
- Recovery from communication timeouts
- Handling of consecutive grab failures

## Sample Output
```
=== Device Removal Handling Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678

[SUCCESS] Connected to Basler acA1920-40gm
[IMAGE] Started grabbing images

[IMAGE] Starting image acquisition...
[IDEA] To test device removal, disconnect and reconnect the camera cable.
[IDEA] Press Ctrl+C to stop the demonstration.

[IMAGE] Grabbed 10 images
[IMAGE] Grabbed 20 images
[IMAGE] Grabbed 30 images

🚨 Device removal detected!
[CONNECT] Disconnecting from camera...
[SUCCESS] Disconnected
🔄 Starting automatic reconnection...
🔄 Reconnection attempt 1/10
🔍 Device not available (attempt 1)
🔄 Reconnection attempt 2/10
[SUCCESS] Connected to Basler acA1920-40gm
[SUCCESS] Reconnection successful! (Attempt 2)
[IMAGE] Started grabbing images

[IMAGE] Grabbed 40 images
[IMAGE] Grabbed 50 images

==================================================
DEVICE STATUS
==================================================
Device Name      : Basler acA1920-40gm
Serial Number    : 12345678
Connected        : [SUCCESS] Yes
Grabbing         : [SUCCESS] Yes
Images Grabbed   : 67
Disconnections   : 1
Reconnections    : 1
==================================================

[STOP] Stopping demonstration...
[SUCCESS] Disconnected
Device removal handling demonstration completed!
```

## Code Highlights

### DeviceRemovalHandler Class
```python
class DeviceRemovalHandler:
    def __init__(self, device_info: pylon.DeviceInfo):
        self.device_info = device_info
        self.camera: Optional[pylon.InstantCamera] = None
        self.is_connected = False
        self.is_running = False
        self.lock = threading.Lock()
        
        # Statistics
        self.images_grabbed = 0
        self.connection_lost_count = 0
        self.reconnection_count = 0
```

### Device Removal Detection
```python
def grab_single_image(self) -> bool:
    try:
        with self.lock:
            if not self.is_connected or self.camera is None:
                return False
            
            # Execute software trigger and grab image
            self.camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException)
            self.camera.ExecuteSoftwareTrigger()
            grab_result = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            
            if grab_result.GrabSucceeded():
                self.images_grabbed += 1
                return True
                
    except (pylon.TimeoutException, genicam.GenericException) as e:
        print(f"[ERROR] Camera error: {e}")
        self.handle_device_removal()
        return False
```

### Automatic Reconnection Logic
```python
def attempt_reconnection(self) -> None:
    print("🔄 Starting automatic reconnection...")
    max_attempts = 10
    
    for attempt in range(1, max_attempts + 1):
        print(f"🔄 Reconnection attempt {attempt}/{max_attempts}")
        time.sleep(2.0)  # Wait before retry
        
        if self.is_device_available() and self.connect():
            self.reconnection_count += 1
            print(f"[SUCCESS] Reconnection successful! (Attempt {attempt})")
            
            # Restart grabbing if it was running
            if self.is_running:
                self.start_grabbing()
            return
    
    print(f"[ERROR] Failed to reconnect after {max_attempts} attempts")
```

### Device Availability Check
```python
def is_device_available(self) -> bool:
    try:
        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        for device in devices:
            if (device.GetSerialNumber() == self.device_info.GetSerialNumber() and
                device.GetModelName() == self.device_info.GetModelName()):
                return True
        return False
    except Exception:
        return False
```

### Thread-Safe Resource Cleanup
```python
def cleanup(self) -> None:
    try:
        if self.camera is not None:
            if self.camera.IsGrabbing():
                self.camera.StopGrabbing()
            if self.camera.IsOpen():
                self.camera.Close()
            self.camera = None
    except Exception as e:
        print(f"Warning during cleanup: {e}")
```

### Status Monitoring
```python
def get_status(self) -> dict:
    with self.lock:
        return {
            'connected': self.is_connected,
            'grabbing': self.camera.IsGrabbing() if self.camera else False,
            'images_grabbed': self.images_grabbed,
            'connection_lost_count': self.connection_lost_count,
            'reconnection_count': self.reconnection_count,
            'device_name': self.device_info.GetModelName(),
            'serial_number': self.device_info.GetSerialNumber()
        }
```

## Reconnection Strategies

### 1. Immediate Retry
- Attempts reconnection as soon as disconnection is detected
- Good for temporary connection issues

### 2. Exponential Backoff
- Increases delay between retry attempts
- Reduces system load during extended outages

### 3. Maximum Attempt Limit
- Prevents infinite retry loops
- Allows application to fail gracefully after reasonable attempts

### 4. Background Threading
- Reconnection attempts don't block main application
- Allows user interface to remain responsive

## Error Handling Scenarios

### Connection Errors
- **Initial Connection Failure**: Graceful error reporting and exit
- **Mid-Operation Disconnection**: Automatic detection and cleanup
- **Reconnection Failure**: Retry logic with maximum attempts

### Timeout Errors
- **Grab Timeouts**: Treated as potential device removal
- **Trigger Ready Timeouts**: Handled without terminating application
- **Configuration Timeouts**: Proper error reporting and recovery

### Resource Errors
- **Memory Issues**: Proper cleanup and resource release
- **Thread Safety**: Locks prevent race conditions
- **Exception Handling**: Comprehensive error catching and reporting

## Best Practices

### Application Design
1. **Always Use Try-Catch**: Wrap camera operations in exception handlers
2. **Resource Cleanup**: Implement proper cleanup in finally blocks
3. **Thread Safety**: Use locks for shared camera resources
4. **Status Monitoring**: Provide user feedback about connection status

### Error Recovery
1. **Graceful Degradation**: Continue operation when possible
2. **User Notification**: Inform users about connection issues
3. **Retry Logic**: Implement reasonable retry strategies
4. **Resource Management**: Clean up properly during failures

### Testing
1. **Physical Disconnection**: Test with actual cable disconnections
2. **Power Cycling**: Test with camera power interruptions
3. **Network Issues**: Test with network connectivity problems (GigE)
4. **Extended Outages**: Test behavior during long disconnections

## Common Disconnection Scenarios

### USB Cameras
- Cable disconnection/reconnection
- USB port power management
- System USB driver issues
- Camera overheating protection

### GigE Cameras
- Network cable disconnection
- Network switch issues
- IP address conflicts
- Firewall blocking
- Power over Ethernet (PoE) issues

## Troubleshooting

### Reconnection Fails
- [SUCCESS] Check physical cable connections
- [SUCCESS] Verify camera power supply
- [SUCCESS] Check USB/network driver status
- [SUCCESS] Ensure no other applications are using the camera

### Application Hangs
- [SUCCESS] Implement proper timeout handling
- [SUCCESS] Use background threads for reconnection
- [SUCCESS] Add comprehensive exception handling
- [SUCCESS] Ensure proper resource cleanup

### Memory Leaks
- [SUCCESS] Release grab results properly
- [SUCCESS] Clean up camera instances
- [SUCCESS] Stop background threads on exit
- [SUCCESS] Call PylonTerminate() in finally blocks

## Related Samples
- `grab` - Basic image acquisition
- `grab_multiple_cameras` - Multi-camera handling with InstantCameraArray
- `parametrize_camera_configurations` - Configuration event handlers 