# Triggered Image Acquisition

Triggered acquisition is used when image capture must happen at a specific moment in time, rather than continuously.

Without triggering, the camera runs freely and frames may miss the relevant moment. With triggering, an external event triggers the camera and captures the object at exactly the right moment.

This ensures the following:

- Images are synchronized with the real world.
- Measurements are repeatable.
- Systems behave deterministically.

Examples of external events that can be used as triggers:

- Moving object reaching a specific position
- Sensor detecting a part
- PLC signal in an automation system
- Lighting pulse or strobe event

This visualization summarizes a typical workflow:

```text
Trigger → Exposure → Readout → Transfer → Application
```

The **trigger** lets the camera start an **exposure**. This is **read out** from the sensor, preprocessed, and **transferred** to the host. At the end, it is passed on to the **application**.

## Typical Use Cases

Use triggered acquisition in the following situations:

- **Timing is critical:** The image must correspond exactly to a physical event, e.g., for high-speed sorting.
- **Motion must be frozen precisely:** You want to capture fast-moving objects at the same position, e.g., for conveyor belt inspection.
- **External systems control the process:** PLCs, sensors, encoders, or other hardware define when to capture, e.g., in robotics applications.
- **Deterministic behavior is required:** Each trigger results in exactly one frame with defined timing, e.g., for measurement systems.

## Software Trigger

A **software trigger** allows you to start an **exposure** via a software call instead of an external hardware event. This can be useful if the source isn't a hardware event but a state change of the computing system. This is usually as precise as a hardware trigger but sufficient in a lot of cases. The main advantage is that it's easier than connecting an output from the computing system to the camera/cameras.

```python
camera.TriggerSelector.Value = "FrameStart"
camera.TriggerMode.Value = "On"
camera.TriggerSource .Value = "Software"
camera.ExecuteSoftwareTrigger()
```

### Example: Periodic Software Trigger (1 Hz)

The following example uses a software trigger to start the exposure of an image every second.

```python
import time
from pypylon import pylon

def process(image):
    h, w = image.shape[:2]
    center_pixel = image[h // 2, w // 2]
    print("Center pixel:", center_pixel)

with pylon.InstantCamera(pylon.FirstFound) as camera:

    # Open is necessary before accessing the parameters.
    camera.Open()

    # Enable trigger mode.
    camera.TriggerSelector.Value = "FrameStart"
    camera.TriggerMode.Value = "On"
    camera.TriggerSource.Value = "Software"

    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    while camera.IsGrabbing():
        camera.ExecuteSoftwareTrigger()

        with camera.RetrieveResult(2000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                process(image)
            else:
                print("Grab failed:", grab_result.ErrorDescription)

        time.sleep(1.0)

```

## Hardware Trigger

If a **software trigger** isn't precise enough for your use case or if a hardware signal is already available, using a **hardware trigger** is the best option.

In this case, [depending on the camera model](cameras.md), there are one or more inputs available that can act as a **trigger input**. A **rising edge** or **falling edge** can be used to trigger an event like **start of exposure** of the camera.

```python
camera.TriggerSource.Value = "Line1"
camera.TriggerSelector.Value = "FrameStart"
camera.TriggerActivation.Value = "RisingEdge"
```

### Example: Hardware Trigger Acquisition

In the following example, the input line 1 on the first camera found is used to start the exposure and output the center pixel.

```python
from pypylon import pylon

def process(image):
    height, width = image.shape[:2]
    center_pixel = image[height // 2, width // 2]
    print("Center pixel:", center_pixel)

with pylon.InstantCamera(pylon.FirstFound) as camera:

    # Open is necessary before accessing the parameters.
    camera.Open()

    # Configure hardware trigger
    camera.TriggerSelector.Value = "FrameStart"
    camera.TriggerMode.Value = "On"
    camera.TriggerActivation.Value = "RisingEdge"
    camera.TriggerSource.Value = "Line1"

    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                process(image)
            else:
                print("Grab failed:", grab_result.ErrorDescription)
```
