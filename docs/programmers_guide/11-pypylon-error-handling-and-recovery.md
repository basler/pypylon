# Error Handling and Recovery

This topic explains why error handling is important.

Industrial camera systems operate in environments where failures are not only possible but expected. Unlike typical desktop applications, these systems often run continuously for hours and even days and interact with external hardware. Because of this, error handling is not optional but a core aspect of system design.

Typical sources of errors include:

- Network interruptions, especially when using GigE cameras
- USB disconnects
- Missing or unstable trigger signals
- CPU overload or slow image processing
- Bandwidth limitations
- Invalid or state-dependent camera configuration

The following visualizations illustrate why error handling is important:

```PlainText
System starts → runs normally → transient failure occurs
```

**Without** proper handling:

```PlainText
Unhandled exception → application crashes → acquisition stops
```

**With** proper handling:

```PlainText
Failure → detect → recover → continue
```

The goal is not to prevent every possible failure. The goal is to make failures visible, controlled, and recoverable.


## Types of Errors in pypylon

Different error types require different handling strategies.

### Grab Errors

A grab error means that a grab result was returned but that the image itself is not valid.

```Python
with camera.RetrieveResult(2000) as grab_result:
    if grab_result.GrabSucceeded():
        image = grab_result.Array
    else:
        print(grab_result.ErrorCode)
        print(grab_result.ErrorDescription)
```

Typical causes:

- Packet loss during GigE connections
- Insufficient bandwidth
- Temporary transport layer problems
- Camera or driver instability

This kind of error usually affects only a single frame. The application can usually log the problem, skip the frame, and continue acquisition.

### Timeout Errors

A timeout occurs while `RetrieveResult()` waits for an image but no image arrives within the timeout configured.

```Python
with camera.RetrieveResult(
    1000,
    pylon.TimeoutHandling_ThrowException
) as grab_result:
    image = grab_result.Array
```

Typical causes:

- Trigger mode is enabled but no trigger signal arrives
- Camera isn't grabbing
- Exposure time longer than expected
- Timeout value too short
- Inconsistent camera configuration

Timeouts are especially common in triggered systems. A timeout doesn't always mean that the camera is broken. It often means that the application is waiting for an event that never happened.

### Runtime Exceptions

Runtime exceptions indicate problems beyond the acquisition of a single frame.

Examples include:

- Camera unplugged
- Network connection lost
- Device reset
- Invalid camera state
- Invalid parameter access

```Python
try:
    # acquisition code
    pass
except Exception as e:
    print("Camera error:", e)
```

These errors usually require recovery logic, such as stopping acquisition, waiting, re-enumerating cameras, or reopening the device.

## Error Handling Strategies

A robust system usually combines multiple strategies.

### Per-Frame Handling

Use this when the camera is still running but individual frames may fail.

```Python
with camera.RetrieveResult(2000) as grab_result:
    if grab_result.GrabSucceeded():
        process(grab_result.Array)
    else:
        log_error(grab_result.ErrorDescription)
```

This approach is useful when occasional frame loss is acceptable. It keeps the acquisition loop alive and avoids stopping the whole system for one bad image.

Typical use cases:

- Live display
- Monitoring systems
- Non-critical image streams

### Exception Handling

Use `try`/`except` around operations that may fail at runtime.

```Python
try:
    with camera.RetrieveResult(
        2000,
        pylon.TimeoutHandling_ThrowException
    ) as grab_result:
        if grab_result.GrabSucceeded():
            process(grab_result.Array)

except Exception as e:
    print("Error:", e)
```

This prevents the application from crashing immediately. However, catching the exception alone isn't enough. The application must also decide whether to continue, retry, reset acquisition, or shut down safely.

### Recovery Loop Pattern

A recovery loop combines error detection with automatic recovery. The following code sample shows the recommended pattern for constructing a recovery loop.

```Python
import time

with pylon.InstantCamera(pylon.FirstFound) as camera:
    while True:
        try:
            if not camera.IsGrabbing():
                camera.StartGrabbing()

            with camera.RetrieveResult(
                2000,
                pylon.TimeoutHandling_ThrowException
            ) as grab_result:

                if grab_result.GrabSucceeded():
                    image = grab_result.Array
                    process(image)
                else:
                    log_error(grab_result.ErrorDescription)

        except Exception as e:
            log_error(f"Acquisition error: {e}")

            if camera.IsGrabbing():
                camera.StopGrabbing()

            time.sleep(0.5)
```

This is the sequence of events when using a recovery loop:

1. Acquisition runs normally.
2. An error occurs.
3. An exception is raised.
4. The exception handler logs the problem.
5. `StopGrabbing()` resets the acquisition pipeline.
6. The application waits briefly.
7. The loop retries acquisition.

This pattern allows a system to recover from temporary failures without manual intervention.

Internal buffers or the grabbing state may no longer represent a clean acquisition pipeline after an acquisition error.

```PlainText
Error → uncertain acquisition state → reset required
```

That's why calling `StopGrabbing()` is an essential part of the recovery loop. It helps with the following:

- Stopping the current acquisition operation
- Releasing or recycling internal buffers
- Preparing the camera for a clean restart

This doesn't solve every possible hardware failure but it's often the first safe recovery step.

## Camera Disconnect Handling

A physical disconnect is one of the most common real-world failure cases.

```PlainText
Camera unplugged → communication lost → exception
```

A robust application should assume that hardware can disappear at any time.

A typical recovery sequence is shown here:

```PlainText
Detect error
   ↓
Stop acquisition
   ↓
Wait briefly
   ↓
Re-enumerate cameras if needed
   ↓
Reconnect or report fatal failure
```

For production systems, reconnect logic is often implemented at a higher level than the basic grab loop.

## Resource Safety

Using `with` for grab results is essential.

```Python
with camera.RetrieveResult(...) as grab_result:
    image = grab_result.Array
```

This ensures that the grab result is released even if an exception occurs inside the block.

Without proper cleanup an acquisition may stall:

```PlainText
Unreleased grab results → buffers unavailable → acquisition stalls
```

This is why all examples in this guide use context managers for grab results.

## Logging Instead of Printing

For examples, `print()` is simple and readable. In production, using the Python `logging` module is preferable.

```Python
import logging

logging.exception("Camera acquisition failed")
```

Logging provides timestamps, severity levels, persistent files, and better diagnostics for long-running systems.

## Recoverable vs. Fatal Errors

Not all errors should be handled the same way.

| Error                              | Typical Handling                     |
| ---------------------------------- | ------------------------------------ |
| Single failed frame                | Log and continue                     |
| Timeout in trigger mode            | Check trigger configuration or retry |
| Temporary bandwidth issue          | Log, reduce load, continue           |
| Camera disconnected                | Stop, re-enumerate, reconnect        |
| Missing required camera at startup | Fail fast                            |
| Invalid configuration              | Stop and report error                |

A production application should clearly distinguish between errors that can be retried and errors that require operator intervention.

## Key Takeaways

- Errors are normal in industrial environments.
- Handle both frame-level errors and system-level exceptions.
- Consider using timeouts and specify appropriate length.
- Use `with` to guarantee resource cleanup.
- Implement recovery loops for unattended systems.
- Use logging and clear error classification in production.

A well-designed error handling strategy ensures stable, autonomous camera applications.
