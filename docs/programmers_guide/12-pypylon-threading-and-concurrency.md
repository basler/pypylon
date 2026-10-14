# Threading and Concurrency

This topic explains how threading and concurrency are used in pypylon applications and how to structure acquisition and processing pipelines for performance and scalability.

This visualization illustrates how image acquisition works in a Python application.

```text
Camera → Native Thread → Buffer Queue → Python Application
```

- Image acquisition runs in a **native (C++) thread** inside pylon.
- Your Python code retrieves images from a **buffer queue**.
- This separation enables asynchronous acquisition.

In many applications, image acquisition is faster than processing:

```text
Camera → 100 fps
Processing → 20 fps
```

Without concurrency:

- Buffers fill up.
- Frames are dropped.
- Latency increases.

## Basic Execution Model

A single-threaded approach is the simplest form of an image acquisition pipeline.

```text
Acquire → Process → Acquire → Process
```

Example:

```python
while camera.IsGrabbing():
    with camera.RetrieveResult(5000) as grab_result:
        if grab_result.GrabSucceeded():
            image = grab_result.Array
            process(image)
```

This has the following disadvantages:

- Processing blocks acquisition.
- Poor CPU utilization
- Limited scalability

## Producer–Consumer Pattern (Recommended)

This is a more sophisticated approach for an image acquisition pipeline.

```text
Acquisition Thread → Queue → Worker Thread(s)
```

- **Producer**: The acquisition thread grabs images and pushes them into a queue.
- **Consumer**: The worker threads process images independently.

## Example Implementation Using a Custom Thread

!!! info
    You can use the grab loop thread provided by the InstantCamera (see the **grab_using_grab_loop_thread** sample). This is a custom implementation for demonstration purposes only.

```python
import threading
import queue
from pypylon import pylon

def process(image):
    print(image.shape)

image_queue = queue.Queue(maxsize=10)

# Producer thread
def grab_loop(camera):
    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
                image_queue.put(image)

# Consumer thread
def process_loop():
    while True:
        image = image_queue.get()
        process(image)
        image_queue.task_done()

with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing()

    grab_thread = threading.Thread(target=grab_loop, args=(camera,))
    processing_thread = threading.Thread(target=process_loop)

    grab_thread.start()
    processing_thread.start()

    grab_thread.join()
    image_queue.join()
```

## Queue Behavior and Backpressure

```text
Queue full → producer blocks → acquisition slows down
```

Strategies:

- Increase queue size.
- Drop frames manually.
- Use `LatestImageOnly`.

## Combining with Grab Strategies

- `LatestImageOnly`: Reduces backlog.
- `OneByOne`: Ensures completeness.

Best practice:

```text
LatestImageOnly + queue → responsive systems
OneByOne + logging → analysis systems
```

## Thread-Safety Considerations

- Avoid sharing mutable data without locks.
- Copy images before passing them to other threads, e.g., by using the `Array` function.
- Use `queue.Queue` for safe communication.

## CPU Utilization

Parallel processing has the following advantages:

- Better CPU usage
- Separation of concerns
- Scalable architectures

```text
Core 1 → Acquisition
Core 2 → Processing
Core 3 → AI
```

## When to Use Multiple Threads

**Use** threading in these situations:

- Processing is slower than acquisition.
- Multiple processing stages exist.
- Real-time responsiveness is required.

**Avoid** threading in these situations:

- Processing is negligible.
- System complexity must be minimal.

## Advanced Patterns (Overview)

### Multi-Stage Pipeline

A multi-stage pipeline splits image processing into independent steps that run concurrently and exchange data via queues.

```text
Grab → Preprocess → Analyze → Display
```

### Multi-Consumer Setup

```text
Producer → Queue → Multiple processing threads
```

## Conceptual Pipeline

```text
Camera → Queue → Processing → Results
```

## Key Takeaways

- Acquisition and processing should be decoupled.
- Use producer-consumer pattern for scalability.
- Queues provide thread-safe communication.
- Threading improves performance but increases complexity.
