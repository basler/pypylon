# Generic Parameter Access Sample

## Description
This sample demonstrates the 'generic' approach for configuring a camera using the GenApi nodemaps represented by the INodeMap interface. The generic approach uses string-based parameter names to access camera parameters through the node map.

This sample shows how to:
- Access camera device information using generic parameter access
- Set Area of Interest (AOI) parameters with value correction
- Handle pixel format changes
- Configure gain settings with auto-function handling
- Use "Try" functions for parameters that may be read-only
- Handle different SFNC (Standard Feature Naming Convention) versions

## Equivalent C++ Sample
`samples_reference_c++/ParametrizeCamera_GenericParameterAccess/`

## Prerequisites
- pypylon
- A Basler camera (or camera emulator)

## Usage
```bash
python parametrize_camera_generic_parameter_access.py
```

## Key Features Demonstrated

### 1. Generic Parameter Access
- Uses string-based parameter names: `CStringParameter(nodemap, "DeviceVendorName")`
- Accesses parameters through the node map interface
- Similar to C++ pylon API approach

### 2. Parameter Types
- **String parameters**: Device vendor, model, firmware version
- **Integer parameters**: Width, height, offsets, GainRaw
- **Float parameters**: Gain (for SFNC 2.0+ cameras)
- **Enumeration parameters**: PixelFormat, GainAuto

### 3. Safe Parameter Handling
- Uses `TrySetToMinimum()` for potentially read-only parameters
- Uses `TrySetValue()` for conditional parameter setting
- Implements value correction with `IntegerValueCorrection_Nearest`

### 4. SFNC Version Handling
- Detects SFNC version using `camera.GetSfncVersion()`
- Uses appropriate parameters for different camera generations:
  - SFNC 2.0+: `Gain` (float parameter)
  - SFNC 1.x: `GainRaw` (integer parameter)

### 5. Area of Interest (AOI) Configuration
- Sets offset parameters to minimum values
- Configures width and height with automatic value correction
- Handles parameter restrictions gracefully

## Sample Output
```
=== Generic Parameter Access Sample ===
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

Generic parameter access demonstration completed successfully!
```

## Code Highlights

### Generic Parameter Creation
```python
# Create generic parameter objects using string names
vendor_name = pylon.CStringParameter(nodemap, "DeviceVendorName")
width = pylon.CIntegerParameter(nodemap, "Width")
pixel_format = pylon.CEnumParameter(nodemap, "PixelFormat")
```

### Safe Parameter Setting
```python
# Use Try functions for potentially read-only parameters
offset_x.TrySetToMinimum()
gain_auto.TrySetValue("Off")

# Use value correction for parameters with restrictions
width.SetValue(202, pylon.IntegerValueCorrection_Nearest)
```

### SFNC Version Detection
```python
if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
    gain = pylon.CFloatParameter(nodemap, "Gain")
else:
    gain_raw = pylon.CIntegerParameter(nodemap, "GainRaw")
```

## Notes
- The generic approach is more flexible but requires knowledge of exact parameter names
- Parameter names can be found in the camera documentation or using pylon Viewer
- Always use try-catch blocks for parameter access as not all parameters are available on all cameras
- The sample includes comprehensive error handling for missing parameters
- Some parameters may be read-only depending on camera state and configuration

## Related Samples
- `parametrize_camera_native_parameter_access` - Native parameter access approach
- `parametrize_camera_configurations` - Configuration event handlers
- `parametrize_camera_user_sets` - User set management 