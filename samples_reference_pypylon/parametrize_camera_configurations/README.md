# Configuration Event Handlers Sample

## Description
This sample demonstrates how to use configuration event handlers by applying standard configurations and registering custom configuration event handlers. Configuration event handlers are derived from the ConfigurationEventHandler base class and provide methods that are called when the state of the instant camera object changes.

This sample shows how to:
- Use standard configuration event handlers (Software Trigger, Single Frame Acquisition)
- Create custom configuration event handlers
- Register and deregister configuration handlers
- Use multiple configuration handlers together
- Handle different acquisition modes with appropriate configurations

## Equivalent C++ Sample
`samples_reference_c++/ParametrizeCamera_Configurations/`

## Prerequisites
- pypylon
- A Basler camera (or camera emulator)

## Usage
```bash
python parametrize_camera_configurations.py
```

## Key Features Demonstrated

### 1. Standard Configuration Handlers
- **SoftwareTriggerConfiguration**: Sets up software triggering mode
- **AcquireSingleFrameConfiguration**: Configures single frame acquisition
- Standard handlers automatically configure camera parameters in their `OnOpened()` method

### 2. Custom Configuration Handlers
- **CustomConfigurationEventHandler**: Demonstrates event handling methods
- **PixelFormatAndAoiConfiguration**: Custom handler for pixel format and AOI setup
- **SimpleImageEventHandler**: Example image event handler

### 3. Configuration Handler Methods
- **OnOpened()**: Called when camera is opened
- **OnClosed()**: Called when camera is closed
- **OnGrabStart()**: Called when grabbing starts
- **OnGrabStop()**: Called when grabbing stops

### 4. Registration Modes
- **RegistrationMode_ReplaceAll**: Replaces all existing handlers
- **RegistrationMode_Append**: Adds handler to existing handlers

### 5. Cleanup Modes
- **Cleanup_Delete**: Handler is automatically deleted when deregistered
- **Cleanup_None**: Handler must be manually managed

## Sample Output
```
=== Configuration Event Handlers Sample ===
Using device: Basler Camera

============================================================
Grab using continuous acquisition:
============================================================
[ContinuousAcquisition] OnOpened: Camera opened
[ContinuousAcquisition] OnGrabStart: Grabbing started
  Grabbed image: 1920x1200
  Grabbed image: 1920x1200
  Grabbed image: 1920x1200
[ContinuousAcquisition] OnGrabStop: Grabbing stopped
[ContinuousAcquisition] OnClosed: Camera closed

============================================================
Grab using software trigger mode:
============================================================
[SoftwareTrigger] OnOpened: Camera opened
[SoftwareTrigger] OnGrabStart: Grabbing started
  Triggered image: 1920x1200
  Triggered image: 1920x1200
  Triggered image: 1920x1200
[SoftwareTrigger] OnGrabStop: Grabbing stopped
[SoftwareTrigger] OnClosed: Camera closed

============================================================
Grab using single frame acquisition:
============================================================
[SingleFrame] OnOpened: Camera opened
  Single frame grabbed: 1920x1200
[SingleFrame] OnClosed: Camera closed
[SingleFrame] OnOpened: Camera opened
  Single frame 1: 1920x1200
  Single frame 2: 1920x1200
  Single frame 3: 1920x1200
[SingleFrame] OnClosed: Camera closed

============================================================
Grab using multiple configuration objects:
============================================================
[PixelFormatAndAoiConfiguration] Configuring pixel format and AOI...
[PixelFormatAndAoiConfiguration] Configuration applied successfully
[Temporary] OnOpened: Camera opened
[ImageEventHandler] Image grabbed successfully: 1920x1200
  Image with all configurations: 1920x1200
[ImageEventHandler] Image grabbed successfully: 1920x1200
  Image without temporary config: 1920x1200

Configuration event handlers demonstration completed successfully!
```

## Code Highlights

### Creating Custom Configuration Handler
```python
class CustomConfigurationEventHandler(pylon.ConfigurationEventHandler):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    def OnOpened(self, camera: pylon.InstantCamera):
        print(f"[{self.name}] OnOpened: Camera opened")
        # Custom configuration logic here
    
    def OnClosed(self, camera: pylon.InstantCamera):
        print(f"[{self.name}] OnClosed: Camera closed")
```

### Registering Configuration Handlers
```python
# Register standard software trigger configuration
camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                            pylon.RegistrationMode_ReplaceAll, 
                            pylon.Cleanup_Delete)

# Add custom configuration handler
camera.RegisterConfiguration(CustomConfigurationEventHandler("MyHandler"), 
                            pylon.RegistrationMode_Append, 
                            pylon.Cleanup_Delete)
```

### Custom AOI and Pixel Format Configuration
```python
class PixelFormatAndAoiConfiguration(pylon.ConfigurationEventHandler):
    def OnOpened(self, camera: pylon.InstantCamera):
        # Set offsets to minimum
        if hasattr(camera, 'OffsetX') and camera.OffsetX.IsWritable():
            camera.OffsetX.Value = camera.OffsetX.Min
        
        # Maximize image size
        if hasattr(camera, 'Width') and camera.Width.IsWritable():
            camera.Width.Value = camera.Width.Max
        
        # Set pixel format
        if hasattr(camera, 'PixelFormat') and camera.PixelFormat.IsWritable():
            camera.PixelFormat.Value = "Mono8"
```

### Using Multiple Handlers
```python
# Register primary configuration
camera.RegisterConfiguration(pylon.AcquireSingleFrameConfiguration(), 
                            pylon.RegistrationMode_ReplaceAll, 
                            pylon.Cleanup_Delete)

# Add additional configuration
camera.RegisterConfiguration(PixelFormatAndAoiConfiguration(), 
                            pylon.RegistrationMode_Append, 
                            pylon.Cleanup_Delete)

# Add image event handler
camera.RegisterImageEventHandler(SimpleImageEventHandler(), 
                                pylon.RegistrationMode_Append, 
                                pylon.Cleanup_Delete)
```

### Deregistering Handlers
```python
# Register with Cleanup_None for manual management
handler = CustomConfigurationEventHandler("Temporary")
camera.RegisterConfiguration(handler, pylon.RegistrationMode_Append, pylon.Cleanup_None)

# Later deregister manually
camera.DeregisterConfiguration(handler)
del handler
```

## Configuration Handler Types

1. **Standard Handlers** (built into pypylon):
   - `SoftwareTriggerConfiguration()`: Software triggering setup
   - `AcquireSingleFrameConfiguration()`: Single frame acquisition
   - `ActionTriggerConfiguration()`: Action command triggering

2. **Custom Handlers**: Inherit from `ConfigurationEventHandler`
   - Override methods like `OnOpened()`, `OnClosed()`, etc.
   - Implement custom camera configuration logic

3. **Event Handlers**: Handle specific events
   - `ImageEventHandler`: Handle image grab events
   - `CameraEventHandler`: Handle camera parameter change events

## Benefits of Configuration Handlers

1. **Automatic Configuration**: Handlers automatically configure camera when opened
2. **Reusability**: Same handlers can be used across multiple cameras
3. **Modularity**: Different aspects of configuration can be separated
4. **Event-Driven**: Handlers respond to camera state changes
5. **Multiple Handlers**: Chain multiple handlers for complex configurations

## Notes
- Configuration handlers are called in the order they were registered
- Handlers with `Cleanup_Delete` are automatically deleted when deregistered
- Custom handlers should include proper error handling
- The `OnOpened()` method is the most commonly overridden method
- Handlers are executed within the camera's lock, so avoid blocking operations

## Related Samples
- `parametrize_camera_generic_parameter_access` - Generic parameter access
- `parametrize_camera_native_parameter_access` - Native parameter access
- `grab_strategies` - Different grabbing strategies with configuration handlers 