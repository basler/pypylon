# Quick Start

This topic shows you the first steps in pypylon by means of a simple workflow.

The goal is not only to show code that works but to give you an idea how to reuse and adapt the sample code in more complex scenarios.

In its simplest form, image acquisition with pypylon involves the following steps:

- Discovering the camera
- Opening the camera
- Starting image acquisition
- Retrieving images
- Processing the images

The following example demonstrates these steps. It has the following additional benefits:

- It allows you to verify that your installation works.
- You can test camera connectivity.
- It helps you to understand the acquisition lifecycle.

**Example:**

```Python
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            print(image.shape)
```

Let's break this sample down into its individual steps:

1. Creating and managing the camera

      ```Python
      with pylon.InstantCamera(pylon.FirstFound) as camera:
      ```

      This line does two important things:

      - It selects the **first available camera**, uses the transport layer factory to create a pylon device object, and wraps it in an `InstantCamera` object for easy use.
      - Using `with` ensures that resources are released automatically and that the camera is closed properly even if an error occurs.

2. Starting acquisition

      ```Python
      camera.StartGrabbingMax(1)
      ```

      This opens the camera, if it's not open already, starts the acquisition engine, and tells the camera to do the following:

      - Acquire exactly **one frame**.
      - Stop acquisition afterwards.

      This is ideal for testing because it avoids infinite loops.

      The camera can also be opened beforehand with a call to Open.

      ```Python
      camera.Open()
      ```

      Opening creates the connection and readies the camera for the following tasks:

      - Configuring parameters
      - Starting acquisition

3. Retrieving the grab result

      ```Python
      with camera.RetrieveResult(5000) as grab_result:
      ```

      This call blocks until either of these events happens:

      - A frame is available.<br>
      **or**
      - The timeout (5000 ms) is reached.

      Internally, you are pulling an image from a **buffer queue**.

4. Validating the grab

      ```Python
      if grab_result.GrabSucceeded():
      ```

      Even if a grab result is returned, the acquisition may have failed (e.g., transport errors). Always check success before using the data.

5. Creating a copy of the pixel data (optional)

      Grab results use buffers from a buffer pool. When you access `grab_result.Array`, you get a copy of the grab result buffer data. Alternatively, you can use `GetMemoryView()` or `GetArrayZeroCopy()` to access the data without copying.

      The buffer from the grab result becomes invalid after leaving the `with` block because the `grab_result` is released. To use the pixel data outside the `with` block, you would need to make a copy of it. You can use the `Array` function to create a copy of the pixel data.

      ```Python
      image = grab_result.Array
      ```

6. Using the image

      ```Python
      print(image.shape)
      ```

      This confirms the following:

      - The image exists.
      - The data has a valid shape.

## Mental Model

This visualization illustrates what happens internally.

```PlainText
Camera (hardware)
      ↓
pylon driver + buffers
      ↓
Transport layer (USB/GigE)
      ↓
RetrieveResult()
      ↓
NumPy array (your application)
```

Key idea:

- The **camera runs asynchronously** (producing frames).
- Your Python code **consumes frames synchronously**.

Buffers sit in between and decouple both worlds (camera and application).

## Key Takeaways

- Always check `GrabSucceeded()`.
- Always copy image data before leaving the result scope or releasing the grab result, e.g., using the `Array` function.
- Use `StartGrabbingMax(1)` for simple tests. Alternatively, you can use `GrabOne(5000)`.<br>
`StartGrabbingMax(1)` grabs exactly one image. `GrabOne(5000)` grabs one image but times out after 5000 µs.
- Use `with` to ensure safe resource handling.

Once you have understood this pattern, you can build on it to write code for the following tasks:

- Building [continuous acquisition](pypylon-image-acquisition.md) loops
- Configuring [triggered acquisition](pypylon-triggered-image-acquisition.md)
- Designing a [multi-camera setup](pypylon-multi-camera-systems.md)
