# Auto Functions Sample

## Description
This sample illustrates how to use the Auto Functions feature of Basler cameras. Auto functions automatically adjust camera parameters like gain, exposure time, and white balance to optimize image quality based on the current scene.

Auto functions are particularly useful for:
- Adapting to changing lighting conditions
- Optimizing image quality automatically
- Reducing manual configuration effort
- Handling varying scene content

This sample shows how to:
- Use auto gain (once and continuous modes)
- Use auto exposure (once and continuous modes)
- Use auto white balance for color cameras
- Handle different SFNC (Standard Feature Naming Convention) versions
- Check camera capabilities (area scan vs line scan, color vs monochrome)

## Equivalent C++ Sample
`samples_reference_c++/ParametrizeCamera_AutoFunctions/`

## Prerequisites
- pypylon
- A Basler camera (or camera emulator)
- **IMPORTANT**: Remove lens cap and ensure adequate lighting

## Usage
```bash
python parametrize_camera_auto_functions.py
```

[WARNING] **IMPORTANT**: Make sure the camera lens cap is removed and there is adequate lighting for auto functions to work properly!

## Key Features Demonstrated

### 1. Auto Gain Functions
- **Auto Gain Once**: Adjusts gain once based on current image
- **Auto Gain Continuous**: Continuously adjusts gain as scene changes
- Monitors gain changes during adjustment process

### 2. Auto Exposure Functions
- **Auto Exposure Once**: Adjusts exposure time once based on current image
- **Auto Exposure Continuous**: Continuously adjusts exposure as lighting changes
- Monitors exposure time changes during adjustment process

### 3. Auto White Balance (Color Cameras Only)
- **Auto White Balance Once**: Adjusts color balance once based on current scene
- Works with Red, Green, and Blue balance ratios
- Only available on color cameras

### 4. Camera Type Detection
- **Area Scan Check**: Auto functions only work on area scan cameras
- **Color Detection**: Auto white balance only works on color cameras
- **SFNC Version Handling**: Uses appropriate parameters for different camera generations

### 5. Parameter Monitoring
- Real-time monitoring of parameter changes during auto functions
- Before/after value comparison
- Change delta calculation

## Sample Output
```
=== Auto Functions Sample ===
Using device: Basler acA1920-40gm
Device scan type: Areascan
SFNC Version: 2.0

==================================================
Auto Gain Once
==================================================
Initial gain: 12.00
Gain auto set to 'Once'
Waiting for auto gain to complete...
Final gain after auto adjustment: 8.50
Gain change: -3.50

==================================================
Auto Gain Continuous
==================================================
Initial gain: 8.50
Gain auto set to 'Continuous'
Monitoring gain for 3 seconds...
  Current gain: 8.50
  Current gain: 9.25
  Current gain: 10.00
  Current gain: 10.00
  Current gain: 10.00
  Current gain: 10.00
Gain auto turned off
Final gain: 10.00

==================================================
Auto Exposure Once
==================================================
Initial exposure time: 10000.0 µs
Exposure auto set to 'Once'
Waiting for auto exposure to complete...
Final exposure time: 15500.0 µs
Exposure change: +5500.0 µs

==================================================
Auto Exposure Continuous
==================================================
Initial exposure time: 15500.0 µs
Exposure auto set to 'Continuous'
Monitoring exposure for 3 seconds...
  Current exposure: 15500.0 µs
  Current exposure: 14200.0 µs
  Current exposure: 13800.0 µs
  Current exposure: 13500.0 µs
  Current exposure: 13500.0 µs
  Current exposure: 13500.0 µs
Exposure auto turned off
Final exposure time: 13500.0 µs

==================================================
Auto White Balance
==================================================
Setting initial balance ratio values...
  Red balance ratio set to: 4.00
  Green balance ratio set to: 2.00
  Blue balance ratio set to: 1.00

Balance white auto set to 'Once'
Waiting for auto white balance to complete...

Final balance ratio values:
  Red balance ratio: 2.85 (change: -1.15)
  Green balance ratio: 1.95 (change: -0.05)
  Blue balance ratio: 1.72 (change: +0.72)

Auto functions demonstration completed successfully!
```

## Code Highlights

### Auto Gain Once Implementation
```python
def auto_gain_once(camera: pylon.InstantCamera) -> None:
    if camera.GetSfncVersion() >= pylon.Sfnc_2_0_0:
        # SFNC 2.0+ (USB cameras)
        initial_gain = camera.Gain.Value
        camera.GainAuto.Value = "Once"
        
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        wait_for_auto_function_completion(camera, 3000)
        camera.StopGrabbing()
        
        final_gain = camera.Gain.Value
        print(f"Gain change: {final_gain - initial_gain:+.2f}")
    else:
        # SFNC 1.x (GigE cameras)
        initial_gain = camera.GainRaw.Value
        camera.GainAuto.Value = "Once"
        # ... similar process with GainRaw
```

### Auto Exposure Continuous Monitoring
```python
def auto_exposure_continuous(camera: pylon.InstantCamera) -> None:
    camera.ExposureAuto.Value = "Continuous"
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    
    # Monitor exposure changes for 3 seconds
    start_time = time.time()
    while time.time() - start_time < 3.0:
        current_exposure = camera.ExposureTime.Value
        print(f"  Current exposure: {current_exposure:.1f} µs")
        time.sleep(0.5)
    
    camera.ExposureAuto.Value = "Off"
    camera.StopGrabbing()
```

### Color Camera Detection
```python
def is_color_camera(camera: pylon.InstantCamera) -> bool:
    try:
        # Check for color pixel formats
        if hasattr(camera, 'PixelFormat'):
            pixel_format_entries = camera.PixelFormat.Symbolics
            color_formats = ['RGB', 'BGR', 'YUV', 'Bayer']
            for format_name in pixel_format_entries:
                for color_format in color_formats:
                    if color_format.lower() in format_name.lower():
                        return True
        
        # Alternative: check for balance ratio parameters
        if hasattr(camera, 'BalanceRatioSelector'):
            return True
            
        return False
    except Exception:
        return False
```

### Auto White Balance with Balance Ratios
```python
def auto_white_balance(camera: pylon.InstantCamera) -> None:
    # Set initial values for demonstration
    camera.BalanceRatioSelector.Value = "Red"
    initial_red = camera.BalanceRatio.Max
    camera.BalanceRatio.Value = initial_red
    
    camera.BalanceRatioSelector.Value = "Green"
    green_mid = camera.BalanceRatio.Min + (camera.BalanceRatio.Max - camera.BalanceRatio.Min) * 0.5
    camera.BalanceRatio.Value = green_mid
    
    camera.BalanceRatioSelector.Value = "Blue"
    initial_blue = camera.BalanceRatio.Min
    camera.BalanceRatio.Value = initial_blue
    
    # Perform auto white balance
    camera.BalanceWhiteAuto.Value = "Once"
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    wait_for_auto_function_completion(camera, 5000)
    camera.StopGrabbing()
```

## Auto Function Modes

### Once Mode
- Performs automatic adjustment once
- Analyzes current image and sets optimal value
- Value remains fixed after adjustment
- Good for stable lighting conditions

### Continuous Mode
- Continuously monitors and adjusts parameters
- Adapts to changing conditions in real-time
- Useful for varying lighting or scene content
- Can be turned off when desired values are reached

### Off Mode
- Disables automatic adjustment
- Parameters remain at manually set values
- Required for manual control

## Camera Type Support

### Area Scan Cameras
- [SUCCESS] **Supported**: All auto functions available
- Most common camera type
- Captures full frames

### Line Scan Cameras
- [ERROR] **Not Supported**: Auto functions not available
- Used for continuous imaging applications
- Different imaging characteristics

### Monochrome Cameras
- [SUCCESS] **Partial Support**: Auto gain and exposure only
- [ERROR] **No White Balance**: Color-specific feature

### Color Cameras
- [SUCCESS] **Full Support**: All auto functions available
- Auto white balance for color correction

## SFNC Version Differences

### SFNC 2.0+ (Typically USB Cameras)
- `Gain` (float parameter)
- `ExposureTime` (float parameter, in microseconds)
- `BalanceRatio` (float parameter)
- `UserSetDefault` (for default settings)

### SFNC 1.x (Typically GigE Cameras)
- `GainRaw` (integer parameter)
- `ExposureTimeRaw` (integer parameter)
- `BalanceRatioAbs` (float parameter)
- `UserSetDefaultSelector` (for default settings)

## Best Practices

1. **Lighting**: Ensure adequate and stable lighting for reliable auto function performance
2. **Scene Content**: Auto functions work best with varied scene content (not uniform surfaces)
3. **Lens Cap**: Always remove lens cap before running auto functions
4. **Timing**: Allow sufficient time for auto functions to complete
5. **Monitoring**: Monitor parameter changes to understand auto function behavior
6. **Manual Override**: Turn off auto functions when manual control is needed

## Troubleshooting

### Auto Functions Don't Work
- [SUCCESS] Check if lens cap is removed
- [SUCCESS] Ensure adequate lighting
- [SUCCESS] Verify camera is area scan type
- [SUCCESS] Check if parameters are available on your camera

### Timeout Errors
- [SUCCESS] Increase timeout values
- [SUCCESS] Improve lighting conditions
- [SUCCESS] Ensure scene has content for analysis

### Parameter Not Available
- [SUCCESS] Check camera documentation for supported features
- [SUCCESS] Verify SFNC version compatibility
- [SUCCESS] Some parameters may be camera-specific

## Related Samples
- `parametrize_camera_native_parameter_access` - Manual parameter control
- `parametrize_camera_configurations` - Configuration event handlers
- `grab` - Basic image acquisition for testing auto functions 