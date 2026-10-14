# Discovering and Selecting Cameras

This topic explains the process of discovering and selecting cameras to work with.

Before an application can use a camera, it must first **discover** which cameras are available. This process is called **enumeration**.

## Enumerating Cameras

Unlike consumer cameras (e.g., webcams), industrial cameras aren't automatically tied to a single application. Instead the following is true:

- Multiple cameras may be connected at the same time.
- Cameras may be connected via different transport layers, e.g., USB, GigE, etc.
- Cameras may appear/disappear dynamically, e.g., due to hot-plugging or network changes.

Enumeration allows your application to achieve the following:

- Detect all cameras currently available.
- Identify them reliably.
- Select the correct camera for your task.

### Examples

```Python
factory = pylon.TlFactory.GetInstance()
```

The **transport layer factory** is the entry point into the pylon ecosystem. It's responsible for these tasks:

- Discovering cameras.
- Creating device instances.
- Abstracting the underlying transport layers, e.g., USB, GigE, etc.

Think of it as a *device manager*.

```Python
device_info_list = factory.EnumerateDevices()
```

This returns a list of device descriptors. Each entry contains metadata about a detected camera, such as:

- Model name
- Serial number (unique identifier)
- Interface type (USB, GigE, etc.)

```Python
for device_info in device_info_list:
    print(device_info.GetFriendlyName())
    print(device_info.GetSerialNumber())
```

### Mental Model

```PlainText
System Startup
     ↓
Transport Layers Scan for Devices
     ↓
Detected Camera List (Enumeration)
     ↓
Application selects a camera
```

## Selecting a Camera

You can select cameras by serial number or by using the index.

### Serial Number (Recommended)

This is the recommended method to select a camera.

```Python
serial_number = "123456"

for device_info in device_info_list:
    if device_info.GetSerialNumber() == serial_number:
        camera = pylon.InstantCamera(factory.CreateDevice(device_info))
```

### Index

```Python
device_info_list[0]
```

!!! info
     Using the index is discouraged as the order may change depending on the number of cameras connected.

## Use Cases

### Single Camera Systems

Use `pylon.InstantCamera(pylon.FirstFound)`.

Key characteristics:

- Sufficient for testing simple setups.
- For single camera use cases, you can let pylon find your camera by passing the required properties as a dictionary.
- Not recommended for multi-camera use cases.

```Python
camera = pylon.InstantCamera({pylon.SerialNumberKey : serial_number}, pylon.FirstFound)
```

### Multi-Camera Systems

Basler recommends enumerating the devices first. Afterwards, you can select the desired camera by its unique identifier, e.g., its serial number, to avoid the overhead of multiple device enumerations.

- Enumerate all cameras.
- Map cameras by serial number or user-defined name.

### Production Systems

- Store camera identifiers in configuration files.
- Validate presence at startup.
- Fail fast if expected camera is missing.

## Key Takeaways

Enumeration is essential because it makes your application:

- Robust to hardware changes
- Independent of connection order
- Scalable to multiple cameras

Without proper enumeration, systems become fragile and difficult to maintain.
---
