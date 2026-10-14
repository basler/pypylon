# Integration with OpenCV

This topic explains how to integrate pypylon image acquisition with OpenCV for visualization and image processing.

## Why Use OpenCV?

OpenCV is one of the most widely-used computer vision libraries. It provides the following features:

- Fast image processing algorithms
- Visualization tools
- Support for feature detection, filtering, and analysis
- Interoperability with NumPy

Since pypylon images are already NumPy arrays, integration is seamless.

## Basic Workflow

```PlainText
Camera → pypylon → NumPy Array → OpenCV → Display/Processing
```

## Simple Example

```Python
import cv2
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array

            # Display using OpenCV
            cv2.imshow("image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
```

## Color Format Considerations

OpenCV expects images in **BGR** format, while cameras may output the following formats:

- Mono (grayscale)
- Bayer
- RGB

### Converting Images to OpenCV-Compatible Formats

For a live loop, prefer `converter.ConvertToArray(grab_result)`: This writes the converted pixels directly into a pre-allocated NumPy array and avoids the extra copy of `converter.Convert(grab_result).Array` (see [Working with Images](pypylon-working-with-images.md) for details).

```Python
converter = pylon.ImageFormatConverter()
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
image = converter.ConvertToArray(grab_result)
```

## Live Display Loop

```Python
import cv2
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array

                cv2.imshow("Live", image)

                if cv2.waitKey(1) == 27:  # ESC to exit
                    break

    cv2.destroyAllWindows()
```

## Typical OpenCV Operations

### Grayscale Conversion

```Python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

### Edge Detection

```Python
edges = cv2.Canny(image, 50, 150)
```

### Blur/Filtering

```Python
blur = cv2.GaussianBlur(image, (5, 5), 0)
```

### Drawing Overlays

```Python
cv2.rectangle(image, (50, 50), (200, 200), (0, 255, 0), 2)
```

## Combining NumPy and OpenCV

This example demonstrates a complete vision pipeline combining pypylon, NumPy, and OpenCV. It continuously grabs images from the camera, extracts a fixed region of interest (ROI), computes a simple statistic (mean intensity), and visualizes the result directly in the live image.

These are the steps:

1. An ROI is defined and extracted using NumPy slicing.
2. The mean intensity of the ROI is calculated.
3. The ROI is visualized using an OpenCV rectangle overlay.
4. The result of a simple rule-based decision ("bright region") is displayed on the image.

This pattern represents a common real-world workflow:

```PlainText
Acquire → Select ROI → Compute Feature → Visualize → Decide
```

```Python
import cv2
from pypylon import pylon
import numpy as np

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array

                # Define ROI coordinates
                y1, y2 = 100, 200
                x1, x2 = 200, 300

                # Extract ROI
                roi = image[y1:y2, x1:x2]

                # Compute statistics
                mean = np.mean(roi)

                # Draw rectangle around ROI
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if mean > 100:
                    cv2.putText(image, "Bright Region", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow("Live", image)

                if cv2.waitKey(1) == 27:
                    break

    cv2.destroyAllWindows()
```

## Key Takeaways

- pypylon integrates seamlessly with OpenCV via NumPy.
- Color conversion is often required.
- OpenCV provides powerful visualization and processing tools.
- Combining NumPy  and OpenCV enables flexible pipelines.
