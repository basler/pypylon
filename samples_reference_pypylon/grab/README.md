# Basic Image Grabbing Sample

## Description

This sample illustrates how to grab and process images using the InstantCamera class. The images are grabbed and processed asynchronously, i.e., while the application is processing a buffer, the acquisition of the next buffer is done in parallel.

The InstantCamera class uses a pool of buffers to retrieve image data from the camera device. Once a buffer is filled and ready, the buffer can be retrieved from the camera object for processing. The buffer and additional image data are collected in a grab result. The grab result is held by a smart pointer after retrieval. The buffer is automatically reused when explicitly released or when the smart pointer object is destroyed.

## Equivalent C++ Sample

`samples_reference_c++/Grab/`

## Prerequisites

- pypylon
- numpy (automatically installed with pypylon)

## Usage

```bash
python grab.py
```

## Key Features Demonstrated

- Creating an InstantCamera object with the first available camera device
- Configuring the camera's buffer pool (MaxNumBuffer parameter)
- Starting continuous image acquisition
- Retrieving grab results in a loop
- Accessing image data and properties
- Proper error handling and resource cleanup

## Sample Output

```
=== Basic Image Grabbing Sample ===
This sample demonstrates how to grab and process images using pypylon.
Press Ctrl+C to stop the application.

Using device: Basler acA1920-40gm

SizeX: 1920
SizeY: 1200
Gray value of first pixel: 145

SizeX: 1920
SizeY: 1200
Gray value of first pixel: 147

...
```

## Code Highlights

### Camera Initialization
```python
# Create an instant camera object with the camera device found first
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
```

### Buffer Pool Configuration
```python
# The parameter MaxNumBuffer can be used to control the count of buffers
# allocated for grabbing. The default value of this parameter is 10.
camera.MaxNumBuffer.Value = 5
```

### Grabbing Loop
```python
# Start grabbing with maximum number of images
camera.StartGrabbingMax(count_of_images_to_grab)

while camera.IsGrabbing():
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
    if grab_result.GrabSucceeded():
        # Access image data
        img = grab_result.Array
        print(f"Gray value of first pixel: {img[0, 0]}")
    
    grab_result.Release()
```

## Notes

- The sample grabs 100 images by default and then stops automatically
- The timeout for RetrieveResult is set to 5000ms (5 seconds)
- Image data is accessed as a numpy array through the `Array` property
- The sample works with both physical and emulated cameras
- GUI display functionality is commented out but can be enabled with `pylon.DisplayImage()`

## Error Handling

The sample includes comprehensive error handling:
- GenericException for pylon-specific errors
- General Exception for unexpected errors
- KeyboardInterrupt for graceful shutdown
- Proper resource cleanup in all cases

## Performance Considerations

- The buffer pool size (MaxNumBuffer) affects memory usage and grabbing performance
- Smaller buffer pools reduce memory usage but may cause frame drops under high load
- The sample demonstrates asynchronous grabbing for optimal performance 