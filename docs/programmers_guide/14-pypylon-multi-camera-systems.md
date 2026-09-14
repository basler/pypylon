# Multi-Camera Systems

This topic explains how to design, configure, and operate systems that use multiple cameras simultaneously.

Multi-camera setups are common in industrial applications such as inspection, 3D reconstruction, and synchronized data acquisition. They are used when a single camera isn't sufficient to capture all the required information.

Typical use cases:

- Capturing different viewpoints of an object
- Increasing the field of view
- Increasing throughput
- Parallel inspection of multiple objects

## Fundamental Challenges

Working with multiple cameras introduces several challenges:

- Synchronization (timing)
- Bandwidth limitations (especially when using GigE cameras)
- CPU load (processing multiple streams)
- Device identification and mapping

## Device Identification

Each camera must have a unique identifier, typically its serial number.

```python
for device_info in device_info_list:
    print(device_info.GetSerialNumber())
```

Mapping example:

```text
Camera 40123456 → Left view
Camera 40123478 → Right view
```

Avoid using indices such as `devices[0]` because the order in which cameras are enumerated may change. For more details, see [Enumerating Cameras](pypylon-discovering-and-selecting-cameras.md#selecting-a-camera).

## Creating Multiple Camera Instances

```python
from pypylon import pylon

factory = pylon.TlFactory.GetInstance()
device_info_list = factory.EnumerateDevices()

cameras = []

for device_info in device_info_list:
    camera = pylon.InstantCamera(factory.CreateDevice(device_info))
    camera.Open()
    cameras.append(camera)
```

This creates and opens one camera instance per device.

## Acquisition Methods

When using multiple cameras, you have to decide on an acquisition method: [sequential](#sequential-acquisition) or [parallel](#parallel-acquisition).

### Sequential Acquisition

This means that image processing is done one camera after the other.

```text
Cam1 → Capture → Process
Cam2 → Capture → Process
```

Key characteristics of this method:

- Simple to implement
- Not time-synchronized
- Slower overall

### Parallel Acquisition

This means that images from several cameras are processed together.

```text
Cam1 → Capture →
                → Process
Cam2 → Capture →
```

Key characteristics of this method:

- Cameras acquire simultaneously
- Required for synchronization
- Higher CPU and bandwidth requirements

## Synchronization Methods

To synchronize cameras, you can choose between software and hardware synchronization. The advantages and disadvantages are similar to software vs. hardware [triggering](pypylon-triggered-image-acquisition.md).

### Software Synchronization

Key characteristics of this method:

- Trigger cameras via software
- Limited precision
- Affected by operating system scheduling

Example:

```python
camera.ExecuteSoftwareTrigger()
```

### Hardware Synchronization (Recommended)

```text
Master camera → trigger signal → Slave cameras
```

Key characteristics of this method:

- Precise timing
- Deterministic behavior
- Required for stereo or measurement systems

## Bandwidth Considerations (GigE)

Multiple GigE cameras share the same network bandwidth.

Potential problems:

- Packet loss
- Dropped frames
- Increased latency

You can use one of the following strategies to mitigate potential problems:

- Use dedicated network interface cards (NICs)
- Enable jumbo frames (MTU 9000)
- Reduce ROI or frame rate
- Configure packet delay

## Processing Architecture

### Single-Threaded

```text
Acquire all → process all
```

- Simple
- Limited scalability

### Multi-Threaded (Recommended)

```text
Camera threads → queue → processing threads
```

- Scalable
- Better CPU utilization
- More complex to implement

## Example Patterns

### Basic Multi-Camera Loop (Sequential Polling)

```python
from pypylon import pylon

def process(image):
    print(image.shape)

factory = pylon.TlFactory.GetInstance()
device_info_list = factory.EnumerateDevices()

cameras = [pylon.InstantCamera(factory.CreateDevice(device_info)) for device_info in device_info_list]

for camera in cameras:
    camera.Open()
    camera.StartGrabbing()

while any(camera.IsGrabbing() for camera in cameras):
    for camera in cameras:
        if camera.IsGrabbing():
            with camera.RetrieveResult(1000) as grab_result:
                if grab_result.GrabSucceeded():
                    image = grab_result.Array
                    # Do processing on image here, e.g. call a function.
                    process(image)
```

### Advanced Approach: InstantCameraArray (Recommended)

pypylon provides a dedicated abstraction for multi-camera setups: `InstantCameraArray`.

This class manages multiple cameras and provides a **single unified `RetrieveResult()` call**, including information about which camera delivered the image.

```python
from pypylon import pylon

def process(image):
    print(image.shape)

COUNT_OF_IMAGES_TO_GRAB = 100
RETRIEVE_TIMEOUT_MS = 5000

factory = pylon.TlFactory.GetInstance()
device_info_list = factory.EnumerateDevices()

with pylon.InstantCameraArray(len(device_info_list)) as cameras:

    for i, camera in enumerate(cameras):
        camera.Attach(factory.CreateDevice(device_info_list[i]))
        print("Using device:", camera.DeviceInfo.ModelName)

    cameras.StartGrabbing()

    for i in range(COUNT_OF_IMAGES_TO_GRAB):
        if not cameras.IsGrabbing():
            break

        with cameras.RetrieveResult(
            RETRIEVE_TIMEOUT_MS,
            pylon.TimeoutHandling_ThrowException
        ) as grab_result:

            if grab_result.GrabSucceeded():
                cam_idx = grab_result.CameraContext
                print(f"Camera {cam_idx}: {cameras[cam_idx].DeviceInfo.ModelName}")
                image = grab_result.Array
                # Do processing on image here, e.g. call a function.
                process(image)
            else:
                print("Error:", grab_result.ErrorDescription)
```

!!! info "Why `InstantCameraArray` Is Important"
    Compared to manual looping, this approach provides:

    - single acquisition loop for all cameras
    - automatic camera context tracking (`camera.CameraContext`)
    - simpler synchronization handling
    - more efficient thread usage

    Conceptually:

    ```text
    Multiple Cameras → InstantCameraArray → Unified RetrieveResult() → Processing
    ```

## Practical Design Guidelines

- Always identify cameras by serial number.
- Prefer hardware synchronization.
- Reduce bandwidth where possible (e.g., by specifying a [ROI](pypylon-configuring-camera-parameters.md#roi) or lowering the frame rate).
- Use separate processing threads for scalability.
- Monitor system load (CPU, network).

## Common Pitfalls

- Relying on device index.
- Exceeding network bandwidth.
- Ignoring synchronization requirements.
- Blocking processing in acquisition loop.

## Mental Model

```text
Multiple Cameras → Acquisition → Buffers → Processing → Results
```

## Key Takeaways

- Multi-camera systems require careful design.
- Synchronization is critical for many applications.
- Bandwidth and CPU must be considered early.
- Scalable architectures use parallel processing.
