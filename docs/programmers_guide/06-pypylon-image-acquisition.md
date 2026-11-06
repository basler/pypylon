[Previous](05-pypylon-discovering-and-selecting-cameras.md) | [Contents](README.md) | [Next](07-pypylon-working-with-images.md)  

---

# Image Acquisition

This topic describes how to set up continuous image acquisition and offers advice on grab strategies.

## Continuous Acquisition

This sample illustrates how to set up continuous image acquisition using the `LatestImageOnly` [grab strategy](#grab-strategies).

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    while camera.IsGrabbing():
        with camera.RetrieveResult(5000) as grab_result:
            if grab_result.GrabSucceeded():
                image = grab_result.Array
```

## Grab Strategies

Grab strategies define how images are handled in the internal buffer queue when the camera produces frames faster than the application consumes them.

In simple terms, they answer the question of what should happen if new images arrive while the application is still processing older ones?

There are two common grab strategies:

- **LatestImageOnly:**
    - Only the newest image is kept.
    - Older frames may be discarded.
- **OneByOne:**
    - All frames are queued and processed in order.
    - No frames are dropped (unless buffers overflow).

The following points may help you to decide when to use which strategy:

- Use **LatestImageOnly** for:
    - Live display
    - GUIs
    - Low-latency systems
- Use **OneByOne** for:
    - Inspection systems
    - Recording
    - Deterministic processing

A detailed explanation of tradeoffs and internal behavior is provided in the [Performance Optimization](10-pypylon-performance-optimization.md) topic.

### Mental Model

````mermaid
flowchart LR
    camera["Camera produces frames: F1, F2, F3, F4"] --> strategy{"Grab strategy"}
    strategy -- LatestImageOnly --> latest["Keep the newest frame: F4"]
    strategy -- OneByOne --> ordered["Process frames in order: F1, F2, F3, F4"]

````

---

[Previous](05-pypylon-discovering-and-selecting-cameras.md) | [Contents](README.md) | [Next](07-pypylon-working-with-images.md)  