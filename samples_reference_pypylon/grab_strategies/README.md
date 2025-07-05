# Grab Strategies Sample

## Description

This sample demonstrates the use of the different grab strategies available in pypylon. Grab strategies control how images are queued and retrieved from the camera's internal buffer system.

There are different strategies to grab images with the InstantCamera grab engine:
- **One By One**: This strategy is the default grab strategy. Acquired images are processed in their arrival order.
- **Latest Image Only**: Differs from the One By One strategy by using a single image output queue. Therefore, only the latest image is kept in the output queue, all other grabbed images are skipped.
- **Latest Images**: Extends the above strategies by adjusting the size of output queue. If the output queue has a size of 1, it is equal to the Latest Image Only strategy. Consequently, setting the output queue size to MaxNumBuffer is equal to One by One.
- **Upcoming Image Grab**: Ensures that the image grabbed is the next image received from the camera. When retrieving an image, a buffer is queued into the input queue and then the call waits for the upcoming image. Subsequently, image data is grabbed into the buffer and returned. Note: This strategy can't be used together with USB camera devices.

## Equivalent C++ Sample

`samples_reference_c++/Grab_Strategies/`

## Prerequisites

- pypylon
- Camera that supports software triggering and frame trigger ready queries

## Usage

```bash
python grab_strategies.py
```

## Key Features Demonstrated

- Software trigger configuration
- Different grab strategies (OneByOne, LatestImageOnly, LatestImages, UpcomingImage)
- Output queue size manipulation
- Frame trigger ready detection
- Grab result queue management
- Handling of skipped images

## Sample Output

```
=== Grab Strategies Sample ===
This sample demonstrates different grab strategies available in pypylon.
Press Ctrl+C to stop the application.

Using device: Basler acA1920-40gm
MaxNumBuffer set to 15
Camera supports frame trigger ready query.

============================================================
Grab using the GrabStrategy_OneByOne default strategy:
============================================================
Triggered image 1
Triggered image 2
Triggered image 3
Grab results wait in the output queue.
Retrieved 3 grab results from output queue.

============================================================
Grab using strategy GrabStrategy_LatestImageOnly:
============================================================
Triggered image 1
Triggered image 2
Triggered image 3
A grab result waits in the output queue.
Skipped 2 images.
Retrieved 1 grab result from output queue.

============================================================
Grab using strategy GrabStrategy_LatestImages:
============================================================
Set output queue size to 2
Triggered image 1
Triggered image 2
Triggered image 3
Grab results wait in the output queue.
Skipped 1 image(s).
Retrieved 2 grab results from output queue.
Setting output queue size to 1 makes it equivalent to LatestImageOnly
Setting output queue size to 15 makes it equivalent to OneByOne

============================================================
Grab using the GrabStrategy_UpcomingImage strategy:
============================================================
Successfully grabbed upcoming image
No grab result waits in the output queue.
```

## Code Highlights

### Software Trigger Configuration
```python
# Register the standard configuration event handler for enabling software triggering
camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                            pylon.RegistrationMode_ReplaceAll, 
                            pylon.Cleanup_Delete)
```

### Frame Trigger Ready Check
```python
# Can the camera device be queried whether it is ready to accept the next frame trigger?
if camera.CanWaitForFrameTriggerReady():
    # Use software triggering
    if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
        camera.ExecuteSoftwareTrigger()
```

### Grab Strategy Usage
```python
# Start grabbing with specific strategy
camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
camera.StartGrabbing(pylon.GrabStrategy_LatestImages)
camera.StartGrabbing(pylon.GrabStrategy_UpcomingImage)
```

### Output Queue Size Configuration
```python
# Adjust output queue size for LatestImages strategy
camera.OutputQueueSize.Value = 2

# Queue size = 1 → equivalent to LatestImageOnly
camera.OutputQueueSize.Value = 1

# Queue size = MaxNumBuffer → equivalent to OneByOne
camera.OutputQueueSize.Value = camera.MaxNumBuffer.Value
```

## Notes

- The sample uses software triggering to demonstrate the different strategies
- USB cameras do not support the UpcomingImage strategy
- The sample requires cameras that support frame trigger ready queries
- Each strategy is demonstrated with 3 triggered images
- The output shows how many images were skipped for each strategy

## Grab Strategy Comparison

| Strategy | Queue Size | Behavior | Use Case |
|----------|------------|----------|----------|
| OneByOne | MaxNumBuffer | All images processed in order | High precision, no frame loss |
| LatestImageOnly | 1 | Only latest image kept | Real-time display, low latency |
| LatestImages | Configurable | Latest N images kept | Balanced performance |
| UpcomingImage | N/A | Next image guaranteed | Synchronized acquisition |

## Performance Considerations

- **OneByOne**: Highest memory usage, no frame loss
- **LatestImageOnly**: Lowest memory usage, potential frame loss
- **LatestImages**: Configurable trade-off between memory and frame loss
- **UpcomingImage**: Synchronized but potentially slower acquisition

## Error Handling

The sample includes comprehensive error handling:
- GenericException for pylon-specific errors
- Camera capability checks (trigger ready, USB detection)
- Proper resource cleanup and camera closure
- Graceful handling of unavailable strategies 