# User Set Management Sample

## Description
This sample demonstrates how to use user configuration sets (user sets) and how to configure the camera to start up with user-defined settings. User sets allow you to save and restore complete camera configurations, providing a convenient way to store different camera setups for various scenarios.

This sample shows how to:
- Check if a camera supports user sets
- Save current camera settings to a user set
- Load settings from a user set
- Set a user set as the default startup configuration
- Handle different SFNC (Standard Feature Naming Convention) versions
- Restore original default settings

## Equivalent C++ Sample
`samples_reference_c++/ParametrizeCamera_UserSets/`

## Prerequisites
- pypylon
- A Basler camera (or camera emulator)

## Usage
```bash
python parametrize_camera_user_sets.py
```

[WARNING] **WARNING**: This sample will overwrite all current settings in user set 1!

## Key Features Demonstrated

### 1. User Set Support Detection
- Checks if camera supports user sets via `UserSetSelector` parameter
- Provides graceful handling for cameras without user set support

### 2. User Set Operations
- **Save**: Store current camera configuration to a user set
- **Load**: Restore camera configuration from a user set
- **Default**: Set which user set loads on camera startup

### 3. SFNC Version Handling
- **SFNC 2.0+** (USB cameras): Uses `UserSetDefault` parameter
- **SFNC 1.x** (GigE cameras): Uses `UserSetDefaultSelector` parameter
- Automatically detects and uses appropriate parameters

### 4. Parameter Configuration
- Demonstrates setting gain and exposure parameters
- Handles both float (SFNC 2.0+) and integer (SFNC 1.x) parameter types
- Disables auto functions before manual parameter setting

### 5. Default User Set Management
- Saves current default user set for restoration
- Sets custom user set as default
- Restores original default user set when done

## Sample Output
```
=== User Set Management Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678
Vendor: Basler AG

Current default user set (SFNC 2.0+): Default
Loading default settings...
Default settings loaded successfully
Configuring camera parameters...
  Turned off Gain Auto
  Turned off Exposure Auto
  Set Gain to minimum: 0.00
  Set ExposureTime to minimum: 20.0

Saving currently active settings to UserSet1...
ATTENTION: This will overwrite all settings previously saved in this user set.
Settings saved to UserSet1 successfully

Loading Default settings...
Default settings loaded successfully

Default settings
================
Gain          : 12.00
Exposure time : 10000.0

Loading UserSet1 settings...
UserSet1 settings loaded successfully

User set 1 settings
===================
Gain          : 0.00
Exposure time : 20.0

Setting UserSet1 as default user set...
Default user set set to: UserSet1
Restored default user set to: Default

User set management demonstration completed successfully!

Note: When the camera is power-cycled, it will start with the configured default user set.
```

## Code Highlights

### Checking User Set Support
```python
def check_user_set_support(camera: pylon.InstantCamera) -> bool:
    try:
        if hasattr(camera, 'UserSetSelector') and camera.UserSetSelector.IsWritable():
            return True
        else:
            print("The device doesn't support user sets.")
            return False
    except (genicam.GenericException, AttributeError):
        return False
```

### Saving to User Set
```python
def save_to_user_set(camera: pylon.InstantCamera, user_set: str) -> None:
    camera.UserSetSelector.Value = user_set
    camera.UserSetSave.Execute()
    print(f"Settings saved to {user_set} successfully")
```

### Loading from User Set
```python
def load_user_set(camera: pylon.InstantCamera, user_set: str) -> None:
    camera.UserSetSelector.Value = user_set
    camera.UserSetLoad.Execute()
    print(f"{user_set} settings loaded successfully")
```

### SFNC Version Handling
```python
if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
    # SFNC 2.0+ cameras (USB)
    camera.UserSetDefault.Value = user_set
    camera.Gain.Value = camera.Gain.Min
    camera.ExposureTime.Value = camera.ExposureTime.Min
else:
    # SFNC 1.x cameras (GigE)
    camera.UserSetDefaultSelector.Value = user_set
    camera.GainRaw.Value = camera.GainRaw.Min
    camera.ExposureTimeRaw.Value = camera.ExposureTimeRaw.Min
```

### Parameter Configuration with Auto Functions
```python
# Disable auto functions first
if hasattr(camera, 'GainAuto') and camera.GainAuto.IsWritable():
    camera.GainAuto.Value = "Off"

if hasattr(camera, 'ExposureAuto') and camera.ExposureAuto.IsWritable():
    camera.ExposureAuto.Value = "Off"

# Then set manual values
camera.Gain.Value = camera.Gain.Min
camera.ExposureTime.Value = camera.ExposureTime.Min
```

## User Set Types

### Standard User Sets
- **Default**: Factory default settings (read-only)
- **UserSet1**: First user-configurable set
- **UserSet2**: Second user-configurable set (if available)
- **UserSet3**: Third user-configurable set (if available)

### User Set Operations
1. **Select**: Choose which user set to work with
2. **Load**: Apply settings from selected user set to camera
3. **Save**: Store current camera settings to selected user set
4. **Set Default**: Configure which user set loads on startup

## Use Cases

1. **Multiple Scenarios**: Save different configurations for various lighting conditions
2. **Quick Setup**: Rapidly switch between predefined camera configurations
3. **Backup**: Save known-good configurations before experimenting
4. **Production**: Ensure consistent camera settings across multiple systems
5. **Recovery**: Restore settings if camera configuration gets corrupted

## Important Notes

[WARNING] **Warnings**:
- Saving to a user set overwrites all previous settings in that set
- Changes to default user set affect camera startup behavior
- Not all cameras support all user sets (UserSet2, UserSet3, etc.)

[IDEA] **Tips**:
- Always check user set support before attempting operations
- Save important configurations to user sets as backup
- Use meaningful user set selection for different scenarios
- Test user set configurations thoroughly before deployment

## Related Samples
- `parametrize_camera_load_and_save` - Feature persistence using .pfs files
- `parametrize_camera_native_parameter_access` - Direct parameter access
- `parametrize_camera_configurations` - Configuration event handlers 