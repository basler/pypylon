# Working with Images

This topic explains how image data is represented in pypylon, how to safely access it, and how to prepare it for further processing (e.g., with NumPy, OpenCV, or AI frameworks).

## Image Representation

In pypylon, images are exposed, e.g., as **NumPy arrays**, which means that they can be used directly in scientific and machine vision workflows.

This is a typical workflow:

```PlainText
Camera → GrabResult → Buffer → NumPy Array
```

## Accessing Image Data

It's essential to know when to copy the data from the grab result and when not to. Copying too much wastes time, while copying too little can lead to crashes or incorrect pixel data.

| Code                  | Description               | Copy Required?      |
| --------------------- | ------------------------- | ------------------- |
| `.Array`              | Returns a NumPy copy      | No (already a copy) |
| `.GetMemoryView()`    | Returns a buffer view     | Yes                 |
| `.GetArrayZeroCopy()` | Returns a zero-copy array | Yes                 |

- `grab_result.Array` is a copy of the internal buffer.
- `grab_result.GetMemoryView()` is a **view into an internal buffer** (except for pixel types where `pylon.IsPacked(grab_result.PixelType)` is True).
- `grab_result.GetArrayZeroCopy()` is a **view into an internal buffer** providing a NumPy array without copying (except for pixel types where `pylon.IsPacked(grab_result.PixelType)` is True).
- The grab result buffer is released when leaving the `with` block or `grab_result.Release()` is called.
- Accessing a memory view or zero-copy array after a buffer has been released can lead to invalid memory access.

Correct usage:

```Python
with camera.RetrieveResult(5000) as grab_result:
    if grab_result.GrabSucceeded():
        image = grab_result.Array
```

## Image Shape and Format

The shape of the array depends on the pixel format:

| Pixel Format | Shape Example      |
| ------------ | ------------------ |
| Mono8        | (height, width)    |
| RGB8/BGR8    | (height, width, 3) |

You can inspect the shape directly:

```Python
print(image.shape)
```

## Pixel Format Conversion

Depending on the camera configuration, the raw image format may not be suitable and may require conversion.

Example: Converting to BGR (OpenCV-compatible)

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

image = converter.Convert(grab_result).GetArray()
```

!!! info
    In `ImageFormatConverter`, `OutputPixelFormat` is a plain attribute that holds a pixel-type value, not a parameter node. Assign it directly (`converter.OutputPixelFormat = pylon.PixelType_BGR8packed`). It has no `.Value` accessor.

### Converting Directly Into a NumPy Array (`ConvertToArray`)

`converter.Convert(src)` returns a `PylonImage`. Reading its pixels with `.Array` (or `.GetArray()`), makes an **additional copy** of the converted buffer. If you only need the result as a NumPy array, use `converter.ConvertToArray(src)` instead. This pre-allocates a NumPy array with the correct shape and data type and lets the converter write the converted pixels **directly into that array**, avoiding the extra copy.

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

# Equivalent result to converter.Convert(grab_result).Array, but without the extra copy.
image = converter.ConvertToArray(grab_result)
```

`ConvertToArray` accepts the same source types as `Convert` (a grab result, a `PylonImage`, a data component, or any `IImage`), and the resulting array's shape and data type reflect the `OutputPixelFormat`:

- `PixelType_Mono8` → `(height, width)`, `uint8`
- `PixelType_Mono16` → `(height, width)`, `uint16`
- `PixelType_RGB8packed` / `PixelType_BGR8packed` → `(height, width, 3)`, `uint8`

A bit-packed output format (one for which `pylon.IsPacked(pixel_type)` is True) has no unambiguous NumPy shape/data type, so `ConvertToArray` raises `ValueError` for it by default. Pass `raw=True` to obtain the converted bytes as a flat `uint8` array instead:

```Python
# raw=True returns a flat uint8 array of the converted bytes,
# which is also how to handle bit-packed output formats.
raw_bytes = converter.ConvertToArray(grab_result, raw=True)
```

| Approach                                  | Result                                       | Extra Copy? |
| ----------------------------------------- | -------------------------------------------- | ----------- |
| `converter.Convert(src).Array`            | NumPy array via intermediate `PylonImage`    | Yes         |
| `converter.ConvertToArray(src)`           | NumPy array written in place                 | No          |
| `converter.ConvertToArray(src, raw=True)` | Flat `uint8` array (also for packed formats) | No          |

### Why Conversion Is Necessary

- Cameras often output raw or Bayer formats.
- Applications typically expect:
    - BGR (OpenCV)
    - RGB (visualization)

## Common Pitfalls

### Using Data After Buffer Release

```Python
with camera.RetrieveResult(...) as grab_result:
    image = grab_result.Array # NumPy array
    memory_view = grab_result.GetMemoryView()
    with grab_result.GetArrayZeroCopy() as zero_copy_array:
        ... process zero_copy_array (NumPy array) ...
```

 This is unsafe because `memory_view` may now reference invalid memory. Always use `result.Array` if needed outside the block or keep the `grab_result` alive.

### Ignoring the Pixel Format

Always verify or explicitly set the pixel format. Ignoring this, may lead to the following consequences:

- Wrong color interpretation
- Incorrect processing results

### Performance Overheads

The following actions may reduce the performance:

- Copying large images costs time
- Conversion adds CPU load

Strategies to avoid this:

- Reducing the region of interest (ROI) (see [Configuring Camera Parameters](pypylon-configuring-camera-parameters.md))
- Avoiding unnecessary conversions

## Using Images in Processing Pipelines

Because images are NumPy arrays, they can be used directly with [OpenCV](#opencv), [NumPy Operations](#numpy-operations), and [AI/ML Frameworks](#aiml-frameworks).

This is a generalized illustration of an image pipeline.

```PlainText
Camera → GrabResult → NumPy Array → Processing → Output
```

This represents the central data flow of most computer vision systems.

### OpenCV

```Python
import cv2

cv2.imshow("image", image)
cv2.waitKey(1)
```

### NumPy Operations

```Python
mean = image.mean()
```

### AI/ML Frameworks

- PyTorch
- TensorFlow

### Sample Image Processing Pipeline Using NumPy

NumPy enables fast, vectorized image processing directly on acquired images.

The following sample is a small but realistic image processing pipeline using NumPy.

#### Sample Code

```Python
import numpy as np
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:

    camera.StartGrabbingMax(100)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array

                # Do something with the image data.

                if image.ndim == 3:
                    gray = image.mean(axis=2)
                else:
                    gray = image

                norm = gray / 255.0

                binary = norm > 0.5

                mean_intensity = norm.mean()
                bright_pixel_ratio = binary.mean()

                print(f"Mean intensity: {mean_intensity:.3f}")
                print(f"Bright pixels: {bright_pixel_ratio*100:.1f}%")
```

Here are some explanations of the individual steps:

- Grayscale conversion:

    ```Python
    gray = image.mean(axis=2)
    ```

- Normalization:

    ```Python
    norm = gray / 255.0
    ```

- Thresholding:

    ```Python
    binary = norm > 0.5
    ```

- Statistical evaluation:

    ```Python
    mean_intensity = norm.mean()
    bright_pixel_ratio = binary.mean()
    ```

A generalized NumPy image pipeline looks like this:

```PlainText
Raw Image → NumPy Array → Processing → Features → Decision
```

## Key Takeaways

- Images are provided as NumPy arrays.
- Always copy buffer data when needed.
- Ensure you're using correct pixel formats.
- Conversion may be required for downstream processing.
