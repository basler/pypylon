# Troubleshooting

This topic helps with diagnosing and resolving common issues encountered when working with pypylon and industrial cameras.

The focus is on practical debugging strategies and typical failure scenarios.

## Typical Symptoms and Causes

| Symptom                       | Possible Cause                                     |
| ----------------------------- | -------------------------------------------------- |
| No camera detected            | Driver missing, cable issue, SDK not installed     |
| Timeout in `RetrieveResult()` | Trigger misconfiguration, no signal, wrong timeout |
| Dropped frames                | Bandwidth limitation, slow processing              |
| Grab errors                   | Network instability, packet loss                   |
| Application freezes           | Blocking calls, deadlocks, queue overflow          |

## Camera Detection Issues

To resolve camera detection issues, you have two options:

- Check the hardware:
    - Verify cable connection.
    - Verify camera power.
    - Try a different USB port or Ethernet cable.

- Check the software:
    - Ensure that the pylon SDK is installed.
    - Verify that the drivers are loaded.
    - Test with the pylon Viewer.

## Timeout Problems

##### Typical Causes

- Trigger mode enabled but no trigger signal
- Exposure time too long
- Timeout value too low

##### Debugging Strategies

```Python
camera.TriggerMode
camera.TriggerSource
```

Disable triggering for testing:

```Python
camera.TriggerMode.Value = "Off"
```

## Grab Errors

##### Indicators

```Python
if not grab_result.GrabSucceeded():
    print(grab_result.ErrorDescription)
```

##### Typical Causes

- Network congestion (GigE)
- Insufficient bandwidth
- Unstable connection

## Image Corruption and Frame Loss

##### Typical Causes

- Packet loss (GigE cameras)
- CPU overload
- Insufficient buffers

##### Mitigation Strategies

- Enable jumbo frames.
- Increase `MaxNumBuffer`.
- Reduce ROI or frame rate.

## Performance Issues

##### Indicators

- Rising latency
- Increasing queue sizes
- Dropped frames

##### Debugging Strategies

- Measure frame rate.
- Monitor CPU usage.
- Inspect queue sizes.

## Threading Issues

##### Indicators

- Deadlocks due to blocking `queue.get()`
- Threads not stopping on shutdown

##### Fixes

- Use timeouts:<br>

    ```Python
    q.get(timeout=0.1)
    ```

- Use stop signals:<br>

    ```Python
    stop_event = threading.Event()
    ```

## OpenCV GUI Issues

##### Indicators

```PlainText
QObject::killTimer error
```

##### Typical Cause

- GUI functions executed in worker thread

##### Fix

- Run `cv2.imshow()` only in main thread.

## Network Issues (GigE)

##### Indicators

- Packet loss
- Frame drops

##### Mitigation Strategies

- Use dedicated network interface card (NIC)
- Enable jumbo frames.
- Adjust packet delay.

## Debugging Checklist

The first step is to identify which layer causes the issue.

```PlainText
Hardware → Transport → Driver → Application
```

Look for the following issue indicators:

- Is the camera detected?
- Does the pylon Viewer work?
- Have you configured `TriggerMode` correctly?
- Is the bandwidth sufficient?
- Is the CPU overloaded?
- Are queues blocking?

## Logging Recommendations

Use structured logging instead of print:

```Python
import logging
logging.exception("Camera error")
```

## Key Takeaways

- Most issues are related to configuration or timing.
- Always isolate hardware vs. software problems.
- Monitor system resources continuously.
- Use systematic debugging approach.
