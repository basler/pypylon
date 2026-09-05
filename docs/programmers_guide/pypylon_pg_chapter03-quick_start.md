# 3. Quick Start

This chapter provides a **gentle entry point** into pypylon by walking through a minimal working example and explaining *how the system behaves conceptually*. The goal is not only to show code that works, but to build an intuition you can reuse in more complex systems.

---

## What This Example Demonstrates

In its simplest form, image acquisition with pypylon follows a consistent pattern:

```PlainText
Discover camera → Open → Start grabbing → Retrieve image → Process
```

The example below performs exactly these steps once, which makes it ideal for:

- verifying that your installation works
- testing camera connectivity
- understanding the acquisition lifecycle

---

## Minimal Working Example

```Python
from pypylon import pylon

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbingMax(1)

    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            print(image.shape)
```

---

## Step-by-Step Explanation


### 1. Create and Manage the Camera

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
```

This line does two important things:

- selects the **first available camera**
- it uses the transport layer factory to create a pylon device object
- wraps it in an `InstantCamera` object for easy use

`InstantCamera`

Using `with` ensures that:

- resources are released automatically
- the camera is properly closed even if an error occurs

---

### 2. Start Acquisition

```Python
camera.StartGrabbingMax(1)
```

This opens the camera, if it is not already open, starts the acquisition engine and tells the camera to:

- acquire exactly **one frame**
- then stop automatically

This is ideal for testing because it avoids infinite loops.

The camera can also be opened beforehand with a call to Open.
```Python
camera.Open()
```

Opening creates the connection and puts the camera into a state where:

- parameters can be configured
- acquisition can be started

---

### 3. Retrieve the Grab Result

```Python
with camera.RetrieveResult(5000) as grab_result:
```

This call blocks until:

- a frame is available **or**
- the timeout (5000 ms) is reached

Internally, you are pulling an image from a **buffer queue**.

---

### 4. Validate the Grab

```Python
if grab_result.GrabSucceeded():
```

Even if a grab result is returned, the acquisition may have failed (e.g. transport errors). Always check success before using the data.

---

### 5. Lifetime of the Image Data

Grab results use buffers from a buffer pool. When you access `grab_result.Array`, you get a copy of the grab result buffer data.
Alternatively, you can use GetMemoryView() or GetArrayZeroCopy() to access the data without copying.

The buffer from the grab result becomes invalid after leaving the `with` block because the `grab_result` is released and we need to make a copy if we need to use the pixel data outside the with block.
The Array function creates a copy of the pixel data.

```Python
image = grab_result.Array
```

---

### 6. Use the Image

```Python
print(image.shape)
```

This simply confirms that:

- the image exists
- the data has a valid shape

---

## Mental Model: What Happens Internally

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

- the **camera runs asynchronously** (producing frames)
- your Python code **consumes frames synchronously**

Buffers sit in between and decouple both worlds.

---

## Key Takeaways

- Always check `GrabSucceeded()`

`GrabSucceeded()`

- Always copy image data before leaving the result scope or releasing the grab result, e.g. with help of the Array function.

- Use `StartGrabbingMax(1)` for simple tests You can use `GrabOne(5000)` alternatively.

`StartGrabbingMax(1)`

- Use `with` to ensure safe resource handling

`with`

Once you understand this pattern, you can scale it to:

- continuous acquisition loops
- triggered systems
- multi-camera setups

---
