# Configuring Camera Parameters

This topic provides descriptions of some of the most commonly used parameters.

## Exposure Time

The **exposure time** defines how long the camera sensor is exposed to light for each frame. It's one of the most important parameters in image acquisition because it directly influences image brightness, motion blur, and signal quality.

### Effects of Exposure Time

During exposure, the sensor collects photons and converts them into an electrical signal. The longer the exposure time, the more light is accumulated. This visualization summarizes this:

```PlainText
Short exposure → less light → darker image
Long exposure  → more light → brighter image
```

The length of the exposure time has the following effects:

- **Brightness**
    - Longer exposure increases brightness.
    - Shorter exposure reduces brightness.
- **Motion Blur**
    - Long exposure results in moving objects appearing blurred.
    - Short exposure results in moving objects appearing frozen.
- **Image Noise**
    - Very short exposures may lead to noisy images (low signal).
    - Longer exposures improve signal quality but may introduce motion blur.

Depending on your application, you have to decide which effect to prioritize when specifying the exposure time. The following table may serve as guidance.

| Goal                | Recommended Exposure |
| ------------------- | -------------------- |
| Freeze fast motion  | Short exposure       |
| Maximize brightness | Long exposure        |
| Stable measurement  | Balanced exposure    |

### Configuration Example

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000  # Value, usually in microseconds
```

- `ExposureAuto = Off` ensures manual control.
- `ExposureTime` is specified in **microseconds (µs)**.

### Key Takeaways

The exposure time must always be chosen in relation to:

- Scene brightness
- Motion speed
- Frame rate requirements

Specifying the correct exposure time is a fundamental step in building a reliable vision system.

```Python
camera.ExposureAuto.Value = "Off"
camera.ExposureTime.Value = 3000  # Value is in microseconds. Check ValueRange for valid values.
#alternatively:
camera.ExposureTimeAbs.SetValue(3000, pylon.FloatValueCorrection_ClipToRange)
```

## Gain

The **gain** controls the electronic amplification of the sensor signal after exposure. Unlike exposure time, gain doesn't increase the amount of captured light but amplifies the existing signal. This visualization summarizes this:

```PlainText
Low gain  → weak amplification → darker but cleaner image
High gain → strong amplification → brighter but noisier image
```

### Effects of Gain

- **Brightness**
    - Increasing gain makes the image brighter.
    - Doesn't add to the actual signal strength. It only amplifies what has already been captured.
- **Image Noise**
    - Higher gain amplifies both signal and noise.
    - Excessive gain leads to grainy images.
- **Detail Quality**
    - High gain may reduce contrast and fine detail visibility.

### Configuration Example

```Python
camera.GainAuto.Value = "Off"
camera.Gain.Value = 5
```

### Key Takeaways

- Use gain when you can't increase the exposure time (e.g., because of the risk of creating motion blur).
- Avoid excessive gain when image quality and signal-to-noise ratio are critical.

General rule: **Prefer longer exposure times over higher gain whenever possible**.

## ROI

The **region of interest (ROI)** defines the part of the sensor that is actually read out and transferred for each frame. By default, the ROI is the same size as the sensor (full resolution). Changing its width and height allows you to focus only on the relevant part of the scene. This visualization summarizes this:

```PlainText
Full sensor → large image → more data
Part of the sensor → cropped image → less data
```

If you reduce the ROI, any pixels outside of the specified region aren't read out or transmitted.

You can adjust the ROI using the `Width`, `Height`, `OffsetX` and `OffsetY` parameters. `Width` + `OffsetX` are limited by `MaxWidth` and `Height` + `OffsetY` ar limited by `MaxHeight`.

!!! info
    - ROI dimensions are subject to hardware constraints (increments, alignment).
    - Maximum ROI equals full sensor resolution.
    - To change the ROI, image acquisition must be stopped.

### Effects of ROI Changes

- **Increased frame rate:** Less data per frame means faster readout and higher frame rates (fps).
- **Reduced bandwidth:** This is especially important for GigE cameras.
- **Lower processing load:** Smaller images allow for faster image processing (OpenCV/AI).
- **Focus on relevant area:** Allows you to ignore irrelevant parts of the scene.

The following table may serve as guidance how a smaller ROI may benefit your application.

| Use Case                 | Benefit of Smaller ROI           |
| ------------------------ | -------------------------------- |
| Tracking a small object  | Faster processing and less noise |
| High-speed inspection    | Increased frame rate             |
| Edge detection in a zone | Reduced computation              |

### Configuration Example

```Python
camera.StopGrabbing()

camera.Width.Value = 640
camera.Height.Value = 480

camera.StartGrabbing()
```

### Key Takeaways

Reducing the ROI is one of the most effective performance tools in machine vision systems. By reducing the amount of data at the source, you improve the following aspects:

- Throughput
- Latency
- System scalability

Unlike image cropping by software, reducing the ROI eliminates unnecessary data **before** it enters the pipeline.

## Static Defect Pixel Correction

[Defect pixel correction](defect-pixel-correction.md) allows you to minimize the influence of sensitivity differences of individual pixels of the sensor. This feature is not available on all cameras. Therefore, it's important to make provisions for it not being available on the current device.

!!! info
    - Use `pylon.StaticDefectPixelCorrection` with `camera.NodeMap`.
    - Use `ListType_Factory` to read factory-provided defect pixels.
    - Use `ListType_User` to read/update user-specific defect pixels.
    - Catch `pylon.RuntimeException` and `pylon.InvalidArgumentException` for unsupported models.

### Configuration Example

```Python
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:
    # Read the factory defect pixel list.
    factory_ok, factory_pixels = pylon.StaticDefectPixelCorrection.GetDefectPixelList(
        camera.NodeMap,
        [],
        pylon.StaticDefectPixelCorrection.ListType_Factory,
    )

    # Build/update the user list as (x, y) or (x, y, type) tuples.
    user_pixels = [(100, 200), (300, 400, 0)]

    try:
        normalize_ok, normalized_pixels = pylon.StaticDefectPixelCorrection.NormalizePixelList(
            camera.NodeMap,
            user_pixels,
        )

        set_ok, written_pixels = pylon.StaticDefectPixelCorrection.SetDefectPixelList(
            camera.NodeMap,
            normalized_pixels,
            pylon.StaticDefectPixelCorrection.ListType_User,
        )

        get_ok, read_back_pixels = pylon.StaticDefectPixelCorrection.GetDefectPixelList(
            camera.NodeMap,
            [],
            pylon.StaticDefectPixelCorrection.ListType_User,
        )
    except (pylon.RuntimeException, pylon.InvalidArgumentException):
        # Camera does not provide this feature.
        pass
```

### Key Takeaways

Treat static defect pixel correction as a device-dependent feature: use it when available and degrade gracefully when it's not available.
