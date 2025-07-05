# Multiple Cameras Grabbing Sample

## Description

This sample illustrates how to grab and process images from multiple cameras using the InstantCameraArray class. The InstantCameraArray class represents an array of instant camera objects. It provides almost the same interface as the instant camera for grabbing.

The main purpose of the InstantCameraArray is to simplify waiting for images and camera events of multiple cameras in one thread. This is done by providing a single RetrieveResult method for all cameras in the array.

Alternatively, the grabbing can be started using the internal grab loop threads of all cameras in the InstantCameraArray. The grabbed images can then be processed by one or more image event handlers (not shown in this example).

## Equivalent C++ Sample

`samples_reference_c++/Grab_MultipleCameras/`

## Prerequisites

- pypylon
- Multiple cameras connected to the system (or emulated cameras for testing)

## Usage

```bash
python grab_multiple_cameras.py
```

## Key Features Demonstrated

- Using InstantCameraArray to manage multiple cameras
- Device enumeration and camera attachment
- Camera context values for identifying grab results
- Round-robin image grabbing from multiple cameras
- Proper resource management for multiple cameras

## Sample Output

```
=== Multiple Cameras Grabbing Sample ===
This sample demonstrates how to grab images from multiple cameras using pypylon.
Note: Using emulated cameras for demonstration. Remove the setup_emulated_cameras() call for physical cameras.
Press Ctrl+C to stop the application.

Found 3 device(s)
Using device 0: Emulation
Using device 1: Emulation

Starting grabbing from 2 cameras...
Will grab 10 images total

Grabbing image 1/10...
  Camera 0: Emulation
  GrabSucceeded: True
  SizeX: 640
  SizeY: 480
  Gray value of first pixel: 145

Grabbing image 2/10...
  Camera 1: Emulation
  GrabSucceeded: True
  SizeX: 640
  SizeY: 480
  Gray value of first pixel: 132

...

Grabbing completed successfully!

Application finished.
Press Enter to exit...
```

## Code Highlights

### Camera Array Creation
```python
# Get all attached devices
devices = tl_factory.EnumerateDevices()

# Create an array of instant cameras for the found devices
cameras = pylon.InstantCameraArray(min(len(devices), max_cameras_to_use))

# Attach devices to cameras
for i, cam in enumerate(cameras):
    cam.Attach(tl_factory.CreateDevice(devices[i]))
```

### Multi-Camera Grabbing
```python
# Start grabbing from all cameras
cameras.StartGrabbing()

# Retrieve results from any camera
grab_result = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

# Identify which camera produced the result
camera_context_value = grab_result.GetCameraContext()
camera_model = cameras[camera_context_value].GetDeviceInfo().GetModelName()
```

### Camera Context Usage
```python
# The camera context identifies which camera produced a grab result
camera_context_value = grab_result.GetCameraContext()

# Use context to access the specific camera
specific_camera = cameras[camera_context_value]
print(f"Image from: {specific_camera.GetDeviceInfo().GetModelName()}")
```

## Notes

- The sample limits the number of cameras to 2 to manage bandwidth
- Images are not grabbed simultaneously from all cameras by default
- For synchronized capture, hardware triggering should be used
- The sample includes emulated camera setup for testing without physical hardware
- Each grab result includes a camera context value to identify the source camera

## Bandwidth Management

When using multiple cameras, bandwidth management is crucial:

### GigE Cameras
- Adjust `GevSCPD` (interpacket delay) parameter
- Adjust `GevSCFTD` (frame transmission delay) parameter
- Consider network adapter limitations

### USB Cameras
- USB bandwidth is shared among all connected devices
- Consider using USB hubs with separate controllers

### Example bandwidth configuration:
```python
# For GigE cameras, adjust timing parameters
camera.GevSCPD.Value = 1000  # Interpacket delay in ticks
camera.GevSCFTD.Value = 2000  # Frame transmission delay in ticks
```

## Synchronization

For synchronized image capture from multiple cameras:

1. **Software Trigger**: Use software triggering with trigger distribution
2. **Hardware Trigger**: Connect external trigger signal to all cameras
3. **IEEE 1588 PTP**: Use Precision Time Protocol for GigE cameras
4. **Action Commands**: Use action commands for frame-accurate triggering

## Error Handling

The sample includes comprehensive error handling:
- Device enumeration validation
- RuntimeException for missing cameras
- GenericException for pylon-specific errors
- Proper resource cleanup for all cameras
- Graceful handling of grabbing interruption

## Performance Considerations

- **Camera Limit**: Limiting cameras prevents bandwidth saturation
- **Buffer Management**: Each camera maintains its own buffer pool
- **Context Switching**: Camera array handles context switching automatically
- **Memory Usage**: Multiple cameras increase memory requirements

## Testing with Emulated Cameras

The sample includes emulated camera support:
```python
# Enable 3 emulated cameras for testing
os.environ["PYLON_CAMEMU"] = "3"
```

Remove or comment out the `setup_emulated_cameras()` call when using physical cameras. 