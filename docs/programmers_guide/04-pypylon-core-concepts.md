# Core Concepts

## Acquisition Lifecycle

```PlainText
Camera → Transport → Buffer Queue → Application
                         ↑
                   RetrieveResult()
```

### Mental Model

- Camera runs asynchronously.
- Python retrieves synchronously.
- Buffers decouple both domains.

## Blocking Behavior

Slow processing may lead to backlog and dropped frames. You can specify a suitable timeout value for `RetrieveResult()` to avoid waiting indefinitely for a grab result.

```PlainText
RetrieveResult() → Waits until frame or timeout
```

## GenICam Nodes

### What is a GenICam Node?

A **GenICam node** represents a single configurable feature or property of a camera. Nodes are defined in the GenICam standard, which provides a uniform way for accessing camera functionality independent of the hardware vendor.

Each node behaves like a strongly-typed parameter and exposes various information:

- Name (e.g., `ExposureTime`)
- Data type (e.g., Float, Integer, Enumeration, etc.)
- Access rights (read-only or read/write)
- Valid value ranges or options

In pypylon, nodes are accessed as attributes of the camera object and provide methods like the following:

```Python
exposure_time = camera.ExposureTime   # Read exposure time in microseconds.
camera.ExposureTime.Value = 3000  # Value is in microseconds. Check Increment and ValueRange for valid values.
```

### Common Node Types

| Parameter   | Example                      | Description                                              |
| ----------- | ---------------------------- | -------------------------------------------------------- |
| Float       | `ExposureTime`               | Continuous values that map to discrete hardware settings |
| Integer     | `Width`                      | Discrete values                                          |
| Enumeration | `TriggerMode`                | Predefined string values                                 |
| Boolean     | `AcquisitionFrameRateEnable` | True/False                                               |
| Command     | `ExecuteSoftwareTrigger`     | Executes an action                                       |

Understanding nodes is essential because **all camera configuration in pypylon is performed through them**.

### pylon Parameters

pylon parameters wrap GenICam nodes and provide an extended consistent interface for reading and writing values. They also handle type conversion, range checking, and access mode handling.

If a node is not found, the `pylon.PlaceholderParameter` is returned, which allows your code to handle missing nodes gracefully. This is often a scenario in setups where different camera models or firmware versions may have different available features.

```Python
var = camera.NotThere.GetValueOrDefault(1)
camera.NotThere.TrySetValue(3000)
```

!!! info "Setting Parameters"
      To change certain parameters, acquisition must be stopped first:

      ```Python
      camera.StopGrabbing()
      camera.Width.Value = 640
      camera.StartGrabbing()
      ```
