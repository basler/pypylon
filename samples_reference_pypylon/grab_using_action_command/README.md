# GigE Action Command Sample

## Description

This sample demonstrates how to use GigE Vision ACTION_CMD to trigger multiple cameras simultaneously. Action commands provide precise synchronization for multi-camera systems by broadcasting trigger signals to all cameras on the same network subnet at once, enabling applications requiring exact timing coordination.

## Equivalent C++ Sample

`samples_reference_c++/Grab_UsingActionCommand/`

## Prerequisites

- pypylon
- **Multiple GigE cameras** on the same network subnet
- GigE Vision transport layer support
- Network bandwidth sufficient for multiple cameras

**Note**: Action commands are **GigE-specific** and not available for USB cameras.

## Usage

```bash
python grab_using_action_command.py
```

## Key Features Demonstrated

### 1. **GigE Action Command System**
- ACTION_CMD broadcast triggering
- Multi-camera synchronization
- Network subnet-based grouping
- Precise timing coordination

### 2. **Action Command Configuration**
- **DeviceKey**: Random unique identifier for security
- **GroupKey**: Defines camera group (0x112233)
- **GroupMask**: Determines which cameras respond (0xFFFFFFFF)
- **TriggerSource**: Set to "Action1" or "Action0"

### 3. **Camera Discovery and Filtering**
- GigE-specific camera enumeration
- Subnet address filtering
- Maximum camera count limiting
- IP address validation

### 4. **Multi-Camera Management**
- InstantCameraArray equivalent functionality
- Camera context assignment
- Individual camera configuration
- Synchronized grabbing operations

### 5. **Network Considerations**
- Bandwidth management for multiple cameras
- Subnet-based camera grouping
- Interpacket delay configuration awareness
- Network topology optimization

## Code Highlights

### GigE Transport Layer Access
```python
def check_gige_support(self) -> bool:
    tl_factory = pylon.TlFactory.GetInstance()
    tl_infos = tl_factory.EnumerateTls()
    
    for tl_info in tl_infos:
        if "GigE" in tl_info.GetDeviceClass():
            return True
    return False
```

### Action Command Configuration
```python
class ActionCommandConfiguration:
    def __init__(self, device_key=None, group_key=0x112233, group_mask=0xFFFFFFFF):
        self.device_key = device_key or random.randint(1, 0xFFFFFFFF)
        self.group_key = group_key
        self.group_mask = group_mask
```

### Camera Action Setup
```python
def configure_camera_action_parameters(self, camera, config):
    # Set frame trigger mode
    camera.TriggerSelector.Value = "FrameStart"
    camera.TriggerMode.Value = "On"
    camera.TriggerSource.Value = "Action1"
    
    # Configure action parameters
    camera.ActionDeviceKey.Value = config.device_key
    camera.ActionGroupKey.Value = config.group_key
    camera.ActionGroupMask.Value = config.group_mask
```

### Action Command Issuing
```python
def issue_action_command(self):
    gige_tl = tl_factory.CreateTl(gige_tl_info)
    
    result = gige_tl.IssueActionCommand(
        self.action_config.device_key,
        self.action_config.group_key,
        self.action_config.group_mask,
        self.subnet
    )
```

## Sample Output

```
=== GigE Action Command Sample ===
This sample demonstrates simultaneous camera triggering
using GigE Vision ACTION_CMD functionality.

[CONFIG] Requirements:
   • Multiple GigE cameras on the same network subnet
   • GigE Vision transport layer support
   • Network bandwidth sufficient for multiple cameras

[SUCCESS] GigE transport layer found: Basler GigE
📡 Discovering GigE cameras...
[INFO] Found 2 GigE camera(s)
🌐 Primary subnet: 192.168.1.0
📷 Camera 1: Basler acA1920-40gm (192.168.1.10)
📷 Camera 2: Basler acA1920-40gm (192.168.1.11)
[SUCCESS] Using 2 camera(s) for action commands

[CONFIG] Creating camera instances...
   📷 Camera 0: Basler acA1920-40gm
      IP: 192.168.1.10
   📷 Camera 1: Basler acA1920-40gm
      IP: 192.168.1.11
[SUCCESS] Created 2 camera instances

[CONFIG] Configuring action trigger...
   ActionConfig(DeviceKey=0x1A2B3C4D, GroupKey=0x00112233, GroupMask=0xFFFFFFFF)
   📷 Configuring camera 0...
         DeviceKey: 0x1A2B3C4D
         GroupKey: 0x00112233
         GroupMask: 0xFFFFFFFF
      [SUCCESS] Camera 0 configured for action commands
[SUCCESS] All cameras configured for action triggering

==================================================
ACTION COMMAND TRIGGER 1/3
==================================================
[CONFIG] Starting grabbing on all cameras...
   📷 Camera 0: Started grabbing
   📷 Camera 1: Started grabbing
[SUCCESS] All cameras are grabbing (waiting for action command)

[ACTION] Issuing action command...
   [SUCCESS] Action command issued successfully

[CONFIG] Retrieving results from cameras...
   🖼️  Camera 0: Image retrieved
      📏 Size: 1920x1080
      [INFO] Frame ID: 1
      [STATS] Mean intensity: 127.5
   🖼️  Camera 1: Image retrieved
      📏 Size: 1920x1080
      [INFO] Frame ID: 1
      [STATS] Mean intensity: 128.2

[INFO] Trigger 1 Results:
   Successful captures: 2/2
```

## Important Notes

### GigE-Only Feature
- Action commands are **exclusive to GigE cameras**
- USB cameras do not support action commands
- Requires GigE Vision transport layer

### Network Requirements
- All cameras must be on the **same subnet**
- Sufficient network bandwidth for multiple cameras
- Consider interpacket delays for bandwidth management
- Network switch recommendations for multi-camera setups

### Timing Precision
- Action commands provide **hardware-level synchronization**
- Much more precise than software triggers
- Typical synchronization: **microsecond accuracy**
- Depends on network latency and camera response

### Security Considerations
- **DeviceKey** acts as security token
- Only cameras with matching DeviceKey respond
- Prevents accidental triggering of wrong cameras
- GroupKey/GroupMask provide additional filtering

## Applications

### Stereoscopic Imaging
```python
# Configure cameras for stereo pair
left_camera.ActionDeviceKey.Value = device_key
right_camera.ActionDeviceKey.Value = device_key
left_camera.ActionGroupKey.Value = STEREO_GROUP
right_camera.ActionGroupKey.Value = STEREO_GROUP
```

### High-Speed Motion Capture
```python
# Configure multiple cameras for motion capture
for i, camera in enumerate(motion_cameras):
    camera.ActionDeviceKey.Value = device_key
    camera.ActionGroupKey.Value = MOTION_GROUP
    camera.ActionGroupMask.Value = 0xFFFFFFFF
```

### Industrial Inspection
```python
# Different groups for different inspection stations
camera1.ActionGroupKey.Value = STATION_A_GROUP
camera2.ActionGroupKey.Value = STATION_B_GROUP
# Trigger specific stations with different group keys
```

## Troubleshooting

### No GigE Cameras Found
```python
if not manager.discover_gige_cameras():
    print("Check:")
    print("- GigE cameras are connected")
    print("- Network configuration is correct")
    print("- Cameras are in same subnet")
```

### Action Command Issues
```python
# Common issues:
# 1. DeviceKey mismatch
# 2. GroupKey/GroupMask filtering
# 3. Network connectivity
# 4. Camera trigger configuration
```

### Network Bandwidth
```python
# For multiple cameras, consider:
# - Interpacket delays (GevSCPD)
# - Frame transmission delays (GevSCFTD)
# - Network switch capabilities
# - Cable quality and length
```

### Camera Synchronization
```python
# Verify synchronization:
# - Check frame timestamps
# - Compare grab result timing
# - Monitor network latency
# - Validate trigger sources
```

## Advanced Usage

### Custom Action Groups
```python
class ActionGroup:
    def __init__(self, group_key, cameras):
        self.group_key = group_key
        self.cameras = cameras
    
    def configure_cameras(self, device_key):
        for camera in self.cameras:
            camera.ActionDeviceKey.Value = device_key
            camera.ActionGroupKey.Value = self.group_key
```

### Conditional Triggering
```python
# Trigger only specific camera groups
def trigger_group(manager, group_key):
    manager.action_config.group_key = group_key
    manager.issue_action_command()
```

### Bandwidth Management
```python
# Configure interpacket delays
for camera in cameras:
    if hasattr(camera, 'GevSCPD'):
        camera.GevSCPD.Value = 1000  # Interpacket delay
    if hasattr(camera, 'GevSCFTD'):
        camera.GevSCFTD.Value = 0    # Frame transmission delay
```

### Multi-Subnet Support
```python
# Handle multiple subnets
def discover_multi_subnet_cameras():
    all_cameras = []
    for subnet in available_subnets:
        subnet_cameras = discover_cameras_in_subnet(subnet)
        all_cameras.extend(subnet_cameras)
    return all_cameras
```

## Performance Considerations

### Network Optimization
- Use dedicated network for camera traffic
- Configure appropriate MTU sizes
- Consider jumbo frames for high-resolution cameras
- Use managed switches with QoS support

### Camera Settings
- Optimize exposure times for simultaneous capture
- Configure appropriate pixel formats
- Set consistent frame rates across cameras
- Use hardware triggering when possible

### Timing Analysis
```python
# Measure action command timing
start_time = time.time()
manager.issue_action_command()
results = manager.retrieve_results()
end_time = time.time()
print(f"Action command cycle time: {(end_time - start_time)*1000:.2f}ms")
```

## Related Samples

- `grab_multiple_cameras/` - Basic multi-camera handling
- `grab_strategies/` - Different grabbing strategies
- `grab_camera_events/` - Camera event handling
- Network configuration samples for GigE cameras

## Technical Details

### Action Command Protocol
- Based on GigE Vision standard
- UDP broadcast message
- Contains DeviceKey, GroupKey, GroupMask, ActionTime
- Processed by camera firmware

### Response Timing
- Cameras respond within microseconds
- Network latency adds small delay
- Hardware trigger generation is immediate
- Software processing adds minimal overhead

### Scalability
- Supports many cameras on same subnet
- Limited by network bandwidth
- Broadcast nature scales well
- No per-camera overhead

This sample provides a comprehensive foundation for implementing synchronized multi-camera systems using GigE Vision action commands in pypylon applications. 