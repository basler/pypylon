# Camera Sequencer Sample

## Description

This sample demonstrates how to use the camera sequencer feature for automated parameter changes during image acquisition. The sequencer allows the camera to automatically cycle through different parameter settings (sequence sets) for each captured image, enabling complex acquisition patterns without manual intervention.

## Equivalent C++ Sample

`samples_reference_c++/Grab_UsingSequencer/`

## Prerequisites

- pypylon
- Basler camera supporting sequencer functionality
- Camera with configurable sequence sets

## Usage

```bash
python grab_using_sequencer.py
```

## Key Features Demonstrated

### 1. **Sequencer Configuration**
- SFNC 2.0+ sequencer setup (USB cameras)
- SFNC 1.x sequencer setup (GigE cameras)
- Sequence set creation and parameter configuration
- Automatic parameter cycling

### 2. **Sequence Set Management**
- Multiple sequence sets with different parameters
- Height parameter variation (25%, 50%, 100%)
- Sequence set saving and restoration
- Automatic advancement between sets

### 3. **SFNC Version Compatibility**
- **SFNC 2.0+**: Uses `SequencerMode`, `SequencerConfigurationMode`, `SequencerSetSelector`
- **SFNC 1.x**: Uses `SequenceEnable`, `SequenceConfigurationMode`, `SequenceSetIndex`

### 4. **Parameter Management**
- Original parameter storage and restoration
- Base parameter configuration
- Sequencer-controlled parameter locking
- Safe configuration mode handling

### 5. **Acquisition Demonstration**
- Automated image capture with sequencer
- Sequence cycle tracking
- Image statistics per sequence set
- Interactive demonstration flow

## Code Highlights

### Sequencer Support Detection
```python
def check_sequencer_support(self) -> bool:
    self.is_sfnc_2_0_plus = self.camera.GetSfncVersion() >= pylon.Sfnc_2_0_0
    
    if self.is_sfnc_2_0_plus:
        # Check for SFNC 2.0+ sequencer
        return hasattr(self.camera, 'SequencerMode')
    else:
        # Check for SFNC 1.x sequencer
        return hasattr(self.camera, 'SequenceEnable')
```

### SFNC 2.0+ Configuration
```python
# Enable configuration mode
camera.SequencerConfigurationMode.Value = "On"

# Configure sequence sets
for i, seq_set in enumerate(sequence_sets):
    camera.SequencerSetSelector.Value = current_set
    camera.Height.SetValuePercentOfRange(seq_set.height_percent)
    camera.SequencerSetSave.Execute()

# Enable sequencer
camera.SequencerConfigurationMode.Value = "Off"
camera.SequencerMode.Value = "On"
```

### SFNC 1.x Configuration
```python
# Configure sequence advance
camera.SequenceAdvanceMode.Value = "Auto"
camera.SequenceSetTotalNumber.Value = len(sequence_sets)

# Configure sequence sets
for i, seq_set in enumerate(sequence_sets):
    camera.SequenceSetIndex.Value = i
    camera.Height.SetValuePercentOfRange(seq_set.height_percent)
    camera.SequenceSetStore.Execute()

# Enable sequence
camera.SequenceEnable.Value = True
```

### Sequence Set Definition
```python
class SequenceSetConfiguration:
    def __init__(self, set_index: int, name: str, height_percent: float):
        self.set_index = set_index
        self.name = name
        self.height_percent = height_percent
```

## Sample Output

```
=== Camera Sequencer Sample ===
Using device: Basler acA1920-40gm
Serial Number: 12345678

[SUCCESS] Sequencer supported (SFNC 2.0+)
[CONFIG] Original parameters stored: 1920x1080

[CONFIG] Creating sequence sets...
   📝 Added sequence set: SequenceSet 0: Quarter Height (Height: 25.0%)
   📝 Added sequence set: SequenceSet 1: Half Height (Height: 50.0%)
   📝 Added sequence set: SequenceSet 2: Full Height (Height: 100.0%)

[CONFIG] Configuring sequencer (SFNC 2.0+)...
   [INFO] Sequencer sets: initial=0, increment=1
   📝 Configuring sequence set 0: Quarter Height
     📏 Height set to 25.0%
     [SUCCESS] Sequence set 0 saved
   [SUCCESS] Sequencer enabled (SFNC 2.0+)

[START] Starting sequencer demonstration (9 images)...

🖼️  Image 1:
    📏 Size: 1920x270
    📝 Sequence Set: 0 (Quarter Height)
    [INFO] Frame ID: 1
    [STATS] Mean intensity: 127.5

🖼️  Image 2:
    📏 Size: 1920x540
    📝 Sequence Set: 1 (Half Height)
    [INFO] Frame ID: 2
    [STATS] Mean intensity: 128.2

🖼️  Image 3:
    📏 Size: 1920x1080
    📝 Sequence Set: 2 (Full Height)
    [INFO] Frame ID: 3
    [STATS] Mean intensity: 126.8
    🔄 Completed sequence cycle 1

[SUCCESS] Sequencer demonstration completed!
[INFO] Total images: 9
🔄 Sequence cycles: 3
```

## Important Notes

### SFNC Version Differences
- **USB Cameras (SFNC 2.0+)**: More complex configuration with paths and triggers
- **GigE Cameras (SFNC 1.x)**: Simpler configuration with automatic advance
- **Parameter Names**: Different parameter names between versions

### Parameter Locking
- Parameters under sequencer control are locked when sequencer is enabled
- Must disable sequencer to change configuration
- Always restore original parameters after use

### Sequence Advancement
- **SFNC 2.0+**: Uses trigger sources (FrameStart, ExposureStart)
- **SFNC 1.x**: Uses automatic advance mode
- Sequences loop back to first set after last set

### Configuration Mode
- Must enable configuration mode before setup
- Disable configuration mode before enabling sequencer
- Some cameras don't support configuration mode

## Applications

### Exposure Bracketing
```python
# Create sequence sets with different exposure times
sequence_sets = [
    SequenceSetConfiguration(0, "Short Exposure", exposure_time=1000),
    SequenceSetConfiguration(1, "Medium Exposure", exposure_time=5000),
    SequenceSetConfiguration(2, "Long Exposure", exposure_time=10000)
]
```

### Multi-Resolution Capture
```python
# Different resolution sequence sets
sequence_sets = [
    SequenceSetConfiguration(0, "Low Res", height_percent=25.0),
    SequenceSetConfiguration(1, "Med Res", height_percent=50.0),
    SequenceSetConfiguration(2, "High Res", height_percent=100.0)
]
```

### Parameter Sweeps
- Automated testing of different parameter combinations
- Quality optimization workflows
- Calibration procedures

## Troubleshooting

### Sequencer Not Supported
```python
if not sequencer.check_sequencer_support():
    print("Camera doesn't support sequencer")
    # Use manual parameter changes instead
```

### Configuration Errors
```python
# Always disable sequencer before configuration
sequencer.disable_sequencer()
# Configure parameters
# Enable sequencer after configuration
```

### Parameter Locking
```python
# Parameters may be locked when sequencer is active
try:
    camera.Height.Value = new_height
except genicam.AccessException:
    print("Parameter locked by sequencer")
```

### Sequence Set Limits
- Check maximum number of sequence sets
- Verify parameter ranges for each set
- Handle sequence set storage limitations

## Advanced Usage

### Custom Parameters
```python
class CustomSequenceSet(SequenceSetConfiguration):
    def __init__(self, set_index, name, **params):
        super().__init__(set_index, name, 100.0)
        self.exposure_time = params.get('exposure_time')
        self.gain = params.get('gain')
        self.offset = params.get('offset')
```

### Dynamic Sequence Generation
```python
def create_exposure_sweep(start_time, end_time, steps):
    sequence_sets = []
    for i in range(steps):
        exposure = start_time + (end_time - start_time) * i / (steps - 1)
        seq_set = SequenceSetConfiguration(i, f"Exposure_{i}", 100.0)
        seq_set.exposure_time = exposure
        sequence_sets.append(seq_set)
    return sequence_sets
```

### Conditional Sequences
```python
# Use sequencer paths for conditional advancement
camera.SequencerPathSelector.Value = 0  # Condition A
camera.SequencerSetNext.Value = set_a
camera.SequencerPathSelector.Value = 1  # Condition B  
camera.SequencerSetNext.Value = set_b
```

## Related Samples

- `grab_strategies/` - Basic grabbing strategies
- `parametrize_camera_auto_functions/` - Automatic camera parameter control
- `grab_camera_events/` - Camera event handling with sequencer

## Technical Details

### Sequence Flow
```
Sequence Set 0 → Sequence Set 1 → Sequence Set 2 → Sequence Set 0 (loop)
```

### Memory Usage
- Sequence sets stored in camera memory
- Limited number of sets depending on camera
- Parameters cached until sequencer disabled

### Timing Considerations
- Parameter changes occur between frames
- Minimal delay for parameter switching
- Synchronization with trigger sources

This sample provides a comprehensive foundation for implementing automated parameter changes using camera sequencer functionality in pypylon applications. 