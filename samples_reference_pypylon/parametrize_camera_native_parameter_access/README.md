# Native Parameter Access Sample

## Description
This sample demonstrates the 'native' approach for configuring a camera using direct property access to camera parameters. The native approach allows direct access to camera parameters as properties of the InstantCamera object, making it the easiest way to access parameters.

This sample shows how to:
- Access camera device information using native parameter access
- Set Area of Interest (AOI) parameters with proper bounds checking
- Handle pixel format changes using direct property access
- Configure gain settings with auto-function handling
- Handle different SFNC (Standard Feature Naming Convention) versions
- Perform safe parameter access with error handling

## Equivalent C++ Sample
`samples_reference_c++/ParametrizeCamera_NativeParameterAccess/`

## Prerequisites
- pypylon
- A Basler camera (or camera emulator)

## Usage
```bash
python parametrize_camera_native_parameter_access.py
```

## Key Features Demonstrated

### 1. Native Parameter Access
- Direct property access: `camera.Width.Value`, `camera.Height.Value`
- No need for string-based parameter names
- More intuitive and IDE-friendly approach

### 2. Parameter Properties
- **Value**: Get/set parameter values directly
- **Min/Max**: Access parameter bounds
- **Inc**: Get parameter increment values
- **IsWritable()**: Check if parameter can be modified

### 3. Safe Parameter Handling
- Checks parameter availability with `hasattr()`
- Validates parameter writability with `IsWritable()`
- Implements proper bounds checking and increment handling
- Comprehensive error handling for missing parameters

### 4. SFNC Version Handling
- Detects SFNC version using `camera.GetSfncVersion()`
- Uses appropriate parameters for different camera generations:
  - SFNC 2.0+: `Gain` (float parameter)
  - SFNC 1.x: `GainRaw` (integer parameter)

### 5. Area of Interest (AOI) Configuration
- Direct property access for Width, Height, OffsetX, OffsetY
- Automatic value correction for parameter restrictions
- Proper increment handling for parameters with step requirements

## Sample Output
```
=== Native Parameter Access Sample ===
Using device: Basler Camera

Camera Device Information
=========================
Vendor           : Basler AG
Model            : Basler Camera
Firmware version : 1.0.0

Camera Device Settings
======================
OffsetX          : 0
OffsetY          : 0
Width            : 202
Height           : 101
Old PixelFormat  : RGB8
New PixelFormat  : Mono8
Gain (50%)       : 12.50 (Min: 0.00; Max: 25.00)

Native parameter access demonstration completed successfully!
```

## Code Highlights

### Direct Property Access
```python
# Access parameters directly as properties
vendor_name = camera.DeviceVendorName.Value
width = camera.Width.Value
pixel_format = camera.PixelFormat.Value
```

### Safe Parameter Modification
```python
# Check if parameter exists and is writable
if hasattr(camera, 'Width') and camera.Width.IsWritable():
    # Calculate valid value within bounds
    desired_width = 202
    min_width = camera.Width.Min
    max_width = camera.Width.Max
    inc_width = camera.Width.Inc
    
    # Adjust to valid value respecting increment
    if inc_width > 1:
        desired_width = min_width + ((desired_width - min_width) // inc_width) * inc_width
    
    camera.Width.Value = desired_width
```

### SFNC Version Detection
```python
if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
    # Use float Gain parameter for newer cameras
    gain_50_percent = camera.Gain.Min + (camera.Gain.Max - camera.Gain.Min) * 0.5
    camera.Gain.Value = gain_50_percent
else:
    # Use integer GainRaw parameter for older cameras
    gain_50_percent = camera.GainRaw.Min + ((camera.GainRaw.Max - camera.GainRaw.Min) // 2)
    camera.GainRaw.Value = gain_50_percent
```

### Parameter Bounds Checking
```python
# Ensure value is within valid range
if desired_value < camera.Parameter.Min:
    desired_value = camera.Parameter.Min
elif desired_value > camera.Parameter.Max:
    desired_value = camera.Parameter.Max

# Adjust for increment requirements
if camera.Parameter.Inc > 1:
    desired_value = camera.Parameter.Min + ((desired_value - camera.Parameter.Min) // camera.Parameter.Inc) * camera.Parameter.Inc
```

## Advantages of Native Parameter Access

1. **Simplicity**: Direct property access is more intuitive than string-based generic access
2. **IDE Support**: Auto-completion and type checking work better with property access
3. **Performance**: Direct access is typically faster than string-based lookups
4. **Type Safety**: Properties provide better type information
5. **Discoverability**: Available parameters can be discovered through IDE introspection

## Notes
- Native parameter access is the recommended approach for pypylon
- Not all cameras support all parameters - always check availability
- Some parameters may be read-only depending on camera state
- Parameter names follow the GenICam standard naming convention
- The sample includes comprehensive error handling for robustness

## Related Samples
- `parametrize_camera_generic_parameter_access` - Generic parameter access using string names
- `parametrize_camera_configurations` - Configuration event handlers
- `parametrize_camera_user_sets` - User set management 