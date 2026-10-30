[Previous](14-pypylon-multi-camera-systems.md) | [Contents](README.md) | [Next](16-pypylon-troubleshooting.md)

---

# Best Practices

This chapter summarizes proven recommendations for building robust, efficient, and maintainable pypylon applications in production environments.

## Resource Management

Always ensure that camera resources are acquired and released properly.

```Python
with pylon.InstantCamera(pylon.FirstFound) as camera:
    # use camera
```

Benefits:

- Automatic cleanup
- Exception safety
- Prevents resource leaks

## Device Identification

Never rely on device indices as they are not stable:

```Python
devices[0]
```

Use unique identifiers instead:

- Serial number
- User-defined name

See [Discovering and Selecting a Camera](05-pypylon-discovering-and-selecting-cameras.md) for details.

## Performance Optimization

### Use Appropriate Grab Strategy

- `LatestImageOnly` → low latency
- `OneByOne` → complete processing

### Reduce Data at Source

- Specify a [ROI](08-pypylon-configuring-camera-parameters.md#roi).
- Reduce resolution.
- Lower frame rate if possible.

### Avoid Unnecessary Copies

- Copy only when required.
- Reuse buffers when possible.

## Threading Design

### Separate Acquisition and Processing

````mermaid
flowchart LR
    camera["Camera"] --> queue["Queue"] --> processing["Processing"]
````

Benefits:

- Better CPU utilization
- Avoids blocking acquisition

### Use Producer–Consumer Pattern

- Acquisition thread pushes images.
- Processing threads consume them.

### Use Thread-Safe Queues

```Python
import queue
q = queue.Queue()
```

## Multi-Stage Pipelines

Structure complex applications as pipelines:

````mermaid
flowchart LR
    grab["Grab"] --> preprocess["Preprocess"] --> analyze["Analyze"] --> output["Output"]
````

Guidelines:

- Each stage has one responsibility.
- Communicate via queues.
- Allow independent scaling per stage.

## Error Handling

### Always Check Grab Success

```Python
if grab_result.GrabSucceeded():
    process(grab_result.Array)
else:
    log_error(grab_result.ErrorDescription)
```

### Catch and Log Exceptions

```Python
try:
    # acquisition code
    pass
except Exception as e:
    log_error(e)
```

### Implement Recovery Logic

````mermaid
flowchart LR
    Error --> StopGrabbing --> Retry --> Continue
````

## Shutdown Strategy

Implement clean shutdown mechanisms:

- Use `threading.Event`.
- Avoid blocking calls without timeout.
- Stop acquisition explicitly.

```Python
stop_event.set()
camera.StopGrabbing()
```

## OpenCV Integration Rules

- Run `imshow()` only in main thread.
- Avoid GUI in worker threads.

## System Monitoring

Track key metrics:

- Frame rate
- Processing latency
- Queue sizes
- CPU usage

## Configuration Management

- Store camera parameters externally.
- Avoid hardcoded values.
- Validate configuration at startup.

## Recommendations for Testing

- Test with real hardware.
- Simulate load conditions.
- Verify recovery behavior.

## Common Pitfalls

- Using image buffers after release
- Blocking queues indefinitely
- Ignoring synchronization requirements
- Mixing UI and worker threads

## Mental Model

````mermaid
flowchart BT
    system["Reliable System"]
    error["Error"] 
    performance["Performance"]
    architecture["Architecture"]
    
    architecture --> system
    error        --> system
    performance  --> system
````

## Key Takeaways

- Design for robustness from the start.
- Separate concerns (acquisition vs. processing).
- Validate every external interaction.
- Plan for failure and recovery.

---

[Previous](14-pypylon-multi-camera-systems.md) | [Contents](README.md) | [Next](16-pypylon-troubleshooting.md)
