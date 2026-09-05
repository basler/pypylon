# 8. Configuring Camera Parameters

## Exposure

The **Exposure Time** defines how long the camera sensor is exposed to light for each captured frame. It is one of the most important parameters in image acquisition because it directly influences image brightness, motion blur, and signal quality.

### Conceptual Meaning

```PlainText
Short exposure → less light → darker image
Long exposure  → more light → brighter image
```

During exposure, the sensor collects photons and converts them into an electrical signal. The longer this integration time, the more light is accumulated.

### Effects of Exposure Time

- **Brightness**
    - Longer exposure increases brightness
    - Shorter exposure reduces brightness
- **Motion Blur**
    - Long exposure → moving objects appear blurred
    - Short exposure → motion is frozen
- **Image Noise**
    - Very short exposures may lead to noisy images (low signal)
    - Longer exposures improve signal quality but may introduce blur

### Practical Tradeoffs

| Goal | Recommended Exposure |
| --- | --- |
| Freeze fast motion | Short exposure |
| Maximize brightness | Long exposure |
| Stable measurement | Balanced exposure |

### Configuration Example

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000  # value, usually in microseconds
```

- `ExposureAuto = Off` ensures manual control

`ExposureAuto = Off`

- `ExposureTime` is specified in **microseconds (µs)**

`ExposureTime`

### Key Insight

Exposure time defines the **integration window of the sensor**. It must always be chosen in relation to:

- scene brightness
- motion speed
- frame rate requirements

Choosing the correct exposure is a fundamental step in building a reliable vision system.

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000  # value is in microseconds; check ValueRange for valid values
#alternatively:
camera.ExposureTimeAbs.SetValue(3000, pylon.FloatValueCorrection_ClipToRange)
```

## Gain

The **Gain** setting controls the electronic amplification of the sensor signal after exposure. Unlike exposure time, gain does not increase the amount of captured light but amplifies the existing signal.

### Conceptual Meaning

```PlainText
Low gain  → weak amplification → darker but cleaner image
High gain → strong amplification → brighter but noisier image
```

### Effects of Gain

- **Brightness**
    - Increasing gain makes the image brighter
    - Does not add real signal, only amplifies what is already captured
- **Image Noise**
    - Higher gain amplifies both signal and noise
    - Excessive gain leads to grainy images
- **Detail Quality**
    - High gain can reduce contrast and fine detail visibility

### When to Use Gain

- Use gain when:
    - exposure time cannot be increased (e.g. motion constraints)
- Avoid excessive gain when:
    - image quality and signal-to-noise ratio are critical

👉 General rule: **Prefer longer exposure over higher gain whenever possible**.

### Configuration Example

```Python
camera.GainAuto.Value = "Off"
camera.Gain.Value = 5
```

## ROI

The **Region of Interest (ROI)** defines the rectangular portion of the sensor that is actually read out and transferred for each frame. Instead of capturing the full sensor area, ROI allows you to focus only on the relevant part of the scene.

### Conceptual Meaning

```PlainText
Full sensor → large image → more data
Smaller ROI → cropped image → less data
```

ROI effectively "crops" the sensor at the hardware level, meaning unused pixel regions are not even read out or transmitted.

### Why Use ROI?

- **Increase Frame Rate**
    - Less data per frame → faster readout → higher FPS
- **Reduce Bandwidth**
    - Especially important for GigE cameras
- **Lower Processing Load**
    - Smaller images → faster image processing (OpenCV / AI)
- **Focus on Relevant Area**
    - Ignore irrelevant parts of the scene

### Practical Examples

| Use Case | Benefit of ROI |
| --- | --- |
| Tracking a small object | Faster processing & less noise |
| High-speed inspection | Increased frame rate |
| Edge detection in a zone | Reduced computation |

### Important Constraints

- ROI dimensions must follow hardware constraints (increments, alignment)
- Maximum ROI equals full sensor resolution
- Changing ROI often requires stopping acquisition

### Configuration Example

```Python
camera.StopGrabbing()

camera.Width.Value = 640
camera.Height.Value = 480

camera.StartGrabbing()
```

### Key Insight

ROI is one of the most effective performance tools in machine vision systems. By reducing the amount of data at the source, you improve:

- throughput
- latency
- system scalability

Unlike software cropping, ROI eliminates unnecessary data *before* it enters the pipeline.

---
