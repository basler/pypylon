# Sample Code

This chapter provides practical, ready-to-use code snippets for common pypylon tasks. This sample code can be used as building blocks for real-world applications.

## Single Image Snapshot

Capture a single image and process it.

```Python
from pypylon import pylon

def process(image):
    print(image.shape)

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            process(image)
```

## Continuous Acquisition Loop

Process images continuously.

```Python
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

while camera.IsGrabbing():
    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            process(grab_result.Array)
```

## Saving Image to Disk

```Python
import cv2

pylon.ImagePersistence.Save(pylon.ImageFileFormat_Png, "image.png", grab_result)
```

## Configuring Software Trigger

```Python
pylon.SoftwareTriggerConfiguration.ApplyConfiguration(camera.NodeMap)
camera.ExecuteSoftwareTrigger()
```

## Configuring Hardware Trigger

```Python
pylon.ConfigurationHelper.DisableAllTriggers(camera.NodeMap)
camera.TriggerSelector.Value = "FrameStart"
camera.TriggerMode.Value = "On"
camera.TriggerSource.Value = "Line1"
```

## Configuring Exposure and Gain

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000

camera.GainAuto.Value = "Off"
camera.Gain.Value = 5
```

## Specifying a Region Of Interest (ROI)

For more details, see [Configuring Camera Parameters](pypylon-configuring-camera-parameters.md#roi).

Get the top left corner from a camera.

```Python
camera.StopGrabbing()

camera.Width.Value = 640
camera.Height.Value = 480
camera.OffsetX.Value = 0
camera.OffsetY.Value = 0

camera.StartGrabbing()
```

Get the center region from a camera.

```Python
camera.StopGrabbing()

camera.Width.Value = 640
camera.Height.Value = 480
camera.OffsetX.Value = (camera.MaxWidth - camera.Width) / 2
camera.OffsetY.Value = (camera.MaxHeight - camera.Height) / 2

camera.StartGrabbing()
```

## Converting Image to OpenCV Format

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

image = converter.Convert(grab_result).GetArray()
```

## Displaying Image with OpenCV

```Python
import cv2

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

!!! info
    Alternatively, you can use the `pylonDisplay` image function.

## Capturing with Timeout Handling

```Python
from pypylon import pylon

try:
    with camera.RetrieveResult(
        1000,
        pylon.TimeoutHandling_ThrowException
    ) as grab_result:
        if grab_result.GrabSucceeded():
            process(grab_result.Array)

except Exception as e:
    log_error(e)
```

## Multi-Camera Setup

Using [multiple cameras](pypylon-multi-camera-systems.md) efficiently is best done with `InstantCameraArray`. It allows grabbing from all cameras in a single loop.

```Python
from pypylon import pylon

RETRIEVE_TIMEOUT_MS = 5000

factory = pylon.TlFactory.GetInstance()
devices = factory.EnumerateDevices()
camera_count = len(devices)

with pylon.InstantCameraArray(camera_count) as cameras:
    # Attach devices
    for i, camera in enumerate(cameras):
        camera.Attach(factory.CreateDevice(devices[i]))
        print("Using device:", camera.DeviceInfo.ModelName)

    # Start acquisition
    cameras.StartGrabbing()

    while cameras.IsGrabbing():
        with cameras.RetrieveResult(
            RETRIEVE_TIMEOUT_MS,
            pylon.TimeoutHandling_ThrowException
        ) as grab_result:

            if grab_result.GrabSucceeded():

                # Identify source camera
                camera_index = grab_result.CameraContext
                camera_name = cameras[camera_index].DeviceInfo.ModelName

                # Access image data (GenDC-safe)
                image = grab_result.Array

                print(
                    f"Camera {camera_index}: {camera_name}"
                    f" SizeX: {grab_result.Width} SizeY: {grab_result.Height} "
                    f" First pixel: {image[0, 0]}"
                )

            else:
                print("Error:", grab_result.ErrorCode, grab_result.ErrorDescription)
```

## Threaded Processing

```Python
import threading
import queue

image_queue = queue.Queue()

def grab_loop():
    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image_queue.put(grab_result.Array)


def process_loop():
    while True:
        image = image_queue.get()
        process(image)
        image_queue.task_done()
```

## Safe Shutdown Pattern

```Python
import threading

stop_event = threading.Event()

while not stop_event.is_set():
    # processing loop
    pass

stop_event.set()
camera.StopGrabbing()
```

## Recording Video

```Python
import cv2

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30, (640, 480))

out.write(image)
```

## Basic Processing Example (ROI + Decision)

```Python
import numpy as np

roi = image[100:200, 200:300]
mean = np.mean(roi)

if mean > 100:
    print("OK")
else:
    print("NOK")
```

## Key Takeaways

- Sample code speeds up development.
- Combine code snippets to build more complex applications.
- Adapt sample code to your specific use case.
