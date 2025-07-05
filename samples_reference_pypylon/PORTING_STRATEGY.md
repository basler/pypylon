# pypylon Sample Porting Strategy

## Overview
This document outlines the systematic approach for porting all C++ samples from `samples_reference_c++` to Python equivalents in `samples_reference_pypylon`.

## Sample Categories & Priority

### Phase 1: Foundation Samples (Priority 1 - Immediate)
Essential samples that demonstrate core pypylon functionality:

1. **Grab** - Basic image acquisition
2. **Grab_Strategies** - Different grabbing strategies
3. **Grab_MultipleCameras** - Multi-camera handling
4. **ParametrizeCamera_LoadAndSave** - Configuration persistence

### Phase 2: Core Camera Operations (Priority 2 - High)
Samples demonstrating parameter control and camera configuration:

5. **ParametrizeCamera_GenericParameterAccess** - Generic parameter access
6. **ParametrizeCamera_NativeParameterAccess** - Native parameter access
7. **ParametrizeCamera_Configurations** - Camera configurations
8. **ParametrizeCamera_UserSets** - User set management
9. **ParametrizeCamera_AutoFunctions** - Auto function configuration
10. **DeviceRemovalHandling** - Device disconnection handling

### Phase 3: Advanced Grabbing (Priority 2 - High)
Advanced image acquisition patterns:

11. **Grab_CameraEvents** - Camera event handling
12. **Grab_ChunkImage** - Chunk data processing
13. **Grab_UsingGrabLoopThread** - Multi-threaded grabbing
14. **Grab_UsingSequencer** - Sequencer functionality
15. **Grab_UsingActionCommand** - Action command triggering
16. **Grab_UsingBufferFactory** - Custom buffer management
17. **Grab_UsingExposureEndEvent** - Exposure event handling

### Phase 4: Image Processing & Utilities (Priority 3 - Medium)
Image processing and utility functions:

18. **Utility_Image** - Image class usage
19. **Utility_ImageFormatConverter** - Format conversion
20. **Utility_ImageLoadAndSave** - Image file I/O
21. **Utility_ImageDecompressor** - Image decompression
22. **Utility_GrabVideo** - Video grabbing
23. **Utility_InstantInterface** - Instant interface usage

### Phase 5: Network & Specialized Features (Priority 3 - Medium)
GigE and specialized camera features:

24. **Grab_MultiCast** - Multicast streaming
25. **Utility_IpConfig** - IP configuration
26. **ParametrizeCamera_SerialCommunication** - Serial communication
27. **ParametrizeCamera_LookupTable** - LUT management
28. **ParametrizeCamera_Shading** - Shading correction
29. **ParametrizeCamera_Shading_Racer2** - Racer2-specific shading
30. **Utility_FFC** - Flat field correction

### Phase 6: Data Processing (Priority 4 - Lower)
Advanced data processing features (requires pylondataprocessing):

31. **barcode** - Barcode detection
32. **ocr** - OCR functionality
33. **region** - Region processing
34. **camera** - Camera data processing
35. **chunks** - Chunk data processing
36. **compositedatatypes** - Composite data types
37. **buildersrecipe** - Recipe building

### Phase 7: GUI & Specialized (Priority 5 - Lowest)
GUI and highly specialized samples:

38. **GUI_QtMultiCam** - Qt multi-camera GUI (may skip or replace with Tkinter/PyQt)

## Porting Guidelines

### Directory Structure
Each ported sample will have its own subdirectory with:
```
samples_reference_pypylon/
├── sample_name/
│   ├── README.md           # Sample description and usage
│   ├── sample_name.py      # Main Python script
│   ├── requirements.txt    # Python dependencies (if any)
│   └── assets/            # Any required assets (optional)
```

### Naming Convention
- C++ sample `Grab_UsingActionCommand` becomes `grab_using_action_command`
- Use snake_case for Python directory and file names
- Keep descriptive names that match the C++ functionality

### Code Style Guidelines
1. Follow PEP 8 Python style guidelines
2. Use type hints where appropriate
3. Include comprehensive docstrings
4. Add error handling and user feedback
5. Use context managers for resource management (cameras, etc.)
6. Include example output or expected behavior in comments

### README Template for Each Sample
```markdown
# Sample Name

## Description
Brief description of what this sample demonstrates.

## Equivalent C++ Sample
`samples_reference_c++/OriginalName/`

## Prerequisites
- pypylon
- Additional dependencies (if any)

## Usage
```python
python sample_name.py
```

## Key Features Demonstrated
- Feature 1
- Feature 2

## Notes
Any special considerations or limitations.
```

### Error Handling Strategy
- Wrap pylon operations in try-catch blocks
- Provide meaningful error messages
- Handle common scenarios (no camera found, disconnection, etc.)
- Include cleanup code in finally blocks or use context managers

### Testing Strategy
- Each sample should run without errors on emulated cameras
- Include validation for expected behavior
- Document any camera-specific requirements
- Test with different camera types where possible

## Implementation Phases

### Current Status: Phase 0 - Setup
- [x] Create directory structure
- [x] Define porting strategy
- [ ] Set up template files

### Phase 1 Implementation Plan
1. Start with **Grab** sample as it's the foundation
2. Identify pypylon API differences from C++
3. Establish patterns for common operations
4. Create reusable utility functions if needed

### Potential pypylon Extensions Needed
During porting, we may discover missing functionality in pypylon that exists in C++. Document these for potential implementation:

- Missing image processing utilities
- Advanced parameter access methods
- Specialized camera feature access
- Performance optimization features

## Success Criteria
- All samples run successfully with emulated cameras
- Clear documentation for each sample
- Proper error handling and user feedback
- Consistent code style across all samples
- Performance comparable to C++ where applicable
- Easy to understand for pypylon users 