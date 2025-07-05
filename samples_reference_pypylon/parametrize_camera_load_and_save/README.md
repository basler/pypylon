# Camera Configuration Load and Save Sample

## Description

This sample application demonstrates how to save or load the features of a camera to or from a file. This functionality is essential for:

- **Backing up camera configurations**: Save current settings before making changes
- **Sharing camera settings**: Transfer configurations between identical cameras
- **Restoring settings**: Recover configurations after firmware updates
- **Standardizing setups**: Create consistent camera configurations across multiple systems

The FeaturePersistence class provides static methods for saving and loading camera parameters to/from a .pfs (Pylon Feature Stream) file. This file format stores all accessible camera parameters in a standardized format.

## Equivalent C++ Sample

`samples_reference_c++/ParametrizeCamera_LoadAndSave/`

## Prerequisites

- pypylon
- A compatible camera (physical or emulated)

## Usage

```bash
python parametrize_camera_load_and_save.py
```

## Key Features Demonstrated

- Saving camera configurations to .pfs files
- Loading camera configurations from .pfs files
- Parameter validation during loading
- Error handling for file operations
- Demonstration of configuration persistence effectiveness

## Sample Output

```
=== Camera Configuration Load and Save Sample ===
This sample demonstrates how to save and load camera configurations using pypylon.
Press Ctrl+C to stop the application.

Camera Information:
  Model: acA1920-40gm
  Serial: 12345678
  Vendor: Basler

=== Saving Camera Configuration ===
Saving camera's node map to file: NodeMap.pfs
Configuration saved successfully (2847 bytes)

=== Modifying Camera Parameters ===
Making some parameter changes for demonstration...
  Changed Width from 1920 to 1820
  Changed Height from 1200 to 1100
  Changed ExposureTime from 10000.0 to 15000.0

=== Loading Camera Configuration ===
Reading file back to camera's node map: NodeMap.pfs
Configuration loaded successfully
All parameter values validated

=== Configuration Persistence Demonstration Complete ===
The camera configuration has been saved to and loaded from 'NodeMap.pfs'
Original settings have been restored.

Cleaning up: Removing 'NodeMap.pfs'

Application finished.
Press Enter to exit...
```

## Code Highlights

### Saving Configuration
```python
def save_camera_configuration(camera: pylon.InstantCamera, filename: str) -> bool:
    # Save the content of the camera's node map to the file
    pylon.FeaturePersistence.Save(filename, camera.GetNodeMap())
    return True
```

### Loading Configuration
```python
def load_camera_configuration(camera: pylon.InstantCamera, filename: str, validate: bool = True) -> bool:
    # Load the content of the file back to the camera's node map
    # The validate parameter enables validation of all node values
    pylon.FeaturePersistence.Load(filename, camera.GetNodeMap(), validate)
    return True
```

### Safe Parameter Modification
```python
# Check if parameter exists and is writable before modifying
if hasattr(camera, 'Width') and camera.Width.IsWritable():
    original_width = camera.Width.Value
    new_width = max(camera.Width.Min, original_width - 100)
    camera.Width.Value = new_width
```

## File Format

The .pfs (Pylon Feature Stream) file format is a text-based format that stores:
- All readable camera parameters
- Parameter values and their types
- Device information and metadata
- GenICam node map structure

Example .pfs content:
```
# {05D8C294-F295-4dfb-9D01-096BD04049F4}
# GenApi persistence file (version 3.1.0)
# Device = Basler acA1920-40gm
Width	1920
Height	1200
ExposureTime	10000.0
PixelFormat	Mono8
...
```

## Notes

- The sample automatically cleans up the created configuration file
- Parameter validation is enabled by default when loading configurations
- Only writable parameters are saved and can be restored
- Some parameters may be read-only depending on camera state
- The configuration includes all accessible camera features

## Best Practices

### Configuration Management
- Use descriptive filenames (e.g., `high_speed_config.pfs`, `quality_config.pfs`)
- Store configurations in a dedicated directory
- Version control your configuration files
- Document what each configuration is optimized for

### Error Handling
```python
try:
    pylon.FeaturePersistence.Save(filename, camera.GetNodeMap())
except Exception as e:
    print(f"Failed to save configuration: {e}")
```

### Validation
- Always use validation when loading configurations in production
- Validation ensures parameter values are within acceptable ranges
- Disable validation only for debugging or when loading partial configurations

## Use Cases

1. **Production Line Setup**: Standardize camera settings across multiple inspection stations
2. **Quality Control**: Switch between different inspection configurations
3. **Maintenance**: Backup configurations before firmware updates
4. **Development**: Share optimal settings between team members
5. **Troubleshooting**: Quickly restore known-good configurations

## Compatibility

- Configuration files are compatible between cameras of the same model
- Some parameters may not transfer between different camera models
- GenICam standard ensures basic compatibility across vendors
- Always test loaded configurations on target hardware

## Error Handling

The sample includes comprehensive error handling for:
- Missing camera devices
- File I/O operations
- Parameter access violations
- Invalid parameter values
- GenICam exceptions

## Security Considerations

- .pfs files contain all camera parameters, including sensitive settings
- Store configuration files securely if they contain proprietary settings
- Validate configurations from untrusted sources before loading
- Consider encrypting configuration files for sensitive applications 