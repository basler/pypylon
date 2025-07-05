# pypylon Reference Samples

This directory contains Python equivalents of the C++ reference samples from `samples_reference_c++`, demonstrating comprehensive pypylon functionality and best practices.

## Sample Status Overview

All samples are currently in **BASE PORTED** state - they have been translated from C++ to Python but require review and testing before being marked as complete.

## Complete Sample Inventory

| Phase | Sample | C++ Original | Python Port | Status | Notes |
|-------|--------|--------------|-------------|--------|-------|
| **Phase 1: Foundation Samples** | | | | | |
| 1 | grab | Grab | grab | Base Ported | Basic image acquisition |
| 1 | grab_strategies | Grab_Strategies | grab_strategies | Base Ported | Different grabbing strategies |
| 1 | grab_multiple_cameras | Grab_MultipleCameras | grab_multiple_cameras | Base Ported | Multi-camera handling |
| 1 | parametrize_camera_load_and_save | ParametrizeCamera_LoadAndSave | parametrize_camera_load_and_save | Base Ported | Configuration persistence |
| **Phase 2: Core Camera Operations** | | | | | |
| 2 | parametrize_camera_generic_parameter_access | ParametrizeCamera_GenericParameterAccess | parametrize_camera_generic_parameter_access | Base Ported | Generic parameter access |
| 2 | parametrize_camera_native_parameter_access | ParametrizeCamera_NativeParameterAccess | parametrize_camera_native_parameter_access | Base Ported | Native parameter access |
| 2 | parametrize_camera_configurations | ParametrizeCamera_Configurations | parametrize_camera_configurations | Base Ported | Configuration event handlers |
| 2 | parametrize_camera_user_sets | ParametrizeCamera_UserSets | parametrize_camera_user_sets | Base Ported | User set management |
| 2 | parametrize_camera_auto_functions | ParametrizeCamera_AutoFunctions | parametrize_camera_auto_functions | Base Ported | Auto functions |
| 2 | device_removal_handling | DeviceRemovalHandling | device_removal_handling | Base Ported | Device disconnection handling |
| **Phase 3: Advanced Grabbing Features** | | | | | |
| 3 | grab_camera_events | Grab_CameraEvents | grab_camera_events | Base Ported | Camera event handling |
| 3 | grab_chunk_image | Grab_ChunkImage | grab_chunk_image | Base Ported | Chunk data processing |
| 3 | grab_using_grab_loop_thread | Grab_UsingGrabLoopThread | grab_using_grab_loop_thread | Base Ported | Multi-threaded grabbing |
| 3 | grab_using_sequencer | Grab_UsingSequencer | grab_using_sequencer | Base Ported | Sequencer functionality |
| 3 | grab_using_action_command | Grab_UsingActionCommand | grab_using_action_command | Base Ported | GigE action commands |
| 3 | grab_using_buffer_factory | Grab_UsingBufferFactory | grab_using_buffer_factory | Base Ported | Custom buffer management |
| 3 | grab_using_exposure_end_event | Grab_UsingExposureEndEvent | grab_using_exposure_end_event | Base Ported | Exposure end event handling |
| **Phase 4: Image Processing & Utilities** | | | | | |
| 4 | utility_image_format_converter | Utility_ImageFormatConverter | - | Not Started | Image format conversion |
| 4 | utility_image_load_and_save | Utility_ImageLoadAndSave | - | Not Started | Image loading/saving |
| 4 | utility_image | Utility_Image | - | Not Started | Image manipulation |
| 4 | utility_image_decompressor | Utility_ImageDecompressor | - | Not Started | Image decompression |
| 4 | utility_grab_video | Utility_GrabVideo | - | Not Started | Video grabbing |
| 4 | utility_instant_interface | Utility_InstantInterface | - | Not Started | Instant interface usage |
| 4 | utility_ffc | Utility_FFC | - | Not Started | Flat field correction |
| **Phase 5: Network Features** | | | | | |
| 5 | grab_multicast | Grab_MultiCast | - | Not Started | Multicast grabbing |
| 5 | utility_ip_config | Utility_IpConfig | - | Not Started | IP configuration |
| 5 | parametrize_camera_serial_communication | ParametrizeCamera_SerialCommunication | - | Not Started | Serial communication |
| **Phase 6: Specialized Camera Features** | | | | | |
| 6 | parametrize_camera_lookup_table | ParametrizeCamera_LookupTable | - | Not Started | Lookup table configuration |
| 6 | parametrize_camera_shading | ParametrizeCamera_Shading | - | Not Started | Shading correction |
| 6 | parametrize_camera_shading_racer2 | ParametrizeCamera_Shading_Racer2 | - | Not Started | Racer2 shading correction |
| **Phase 7: Data Processing & GUI** | | | | | |
| 7 | barcode_recognition | barcode | - | Not Started | Barcode recognition (requires license) |
| 7 | ocr_recognition | ocr | - | Not Started | OCR recognition (requires license) |
| 7 | camera_recipe | camera | - | Not Started | Camera-based recipe processing |
| 7 | builders_recipe | buildersrecipe | - | Not Started | Recipe builder pattern |
| 7 | composite_data_types | compositedatatypes | - | Not Started | Composite data type handling |
| 7 | region_processing | region | - | Not Started | Region-based processing |
| 7 | chunks_processing | chunks | - | Not Started | Chunk data processing |
| 7 | gui_qt_multicam | GUI_QtMultiCam | - | Not Started | Qt GUI for multiple cameras |

**Summary:**
- **Total Samples**: 38 (100%)
- **Base Ported**: 17 (44.7%)
- **Not Started**: 21 (55.3%)
- **Reviewed & Tested**: 0 (0%)

## Sample Categories

### Basic Operations
| Sample | Description | Status |
|--------|-------------|--------|
| `grab/` | Basic image acquisition with error handling | Base Ported |
| `grab_strategies/` | Different grabbing strategies demonstration | Base Ported |
| `grab_multiple_cameras/` | Multi-camera handling with InstantCameraArray | Base Ported |

### Parameter Management
| Sample | Description | Status |
|--------|-------------|--------|
| `parametrize_camera_generic_parameter_access/` | String-based parameter access | Base Ported |
| `parametrize_camera_native_parameter_access/` | Direct property access | Base Ported |
| `parametrize_camera_configurations/` | Configuration event handlers | Base Ported |
| `parametrize_camera_user_sets/` | User set management | Base Ported |
| `parametrize_camera_auto_functions/` | Auto gain, exposure, white balance | Base Ported |
| `parametrize_camera_load_and_save/` | Configuration persistence | Base Ported |

### Advanced Grabbing
| Sample | Description | Status |
|--------|-------------|--------|
| `grab_camera_events/` | Camera event handling (exposure end, overrun) | Base Ported |
| `grab_chunk_image/` | Chunk data processing and validation | Base Ported |
| `grab_using_grab_loop_thread/` | Multi-threaded background grabbing | Base Ported |
| `grab_using_sequencer/` | Automated parameter sequences | Base Ported |
| `grab_using_action_command/` | GigE action command synchronization | Base Ported |
| `grab_using_buffer_factory/` | Custom buffer management | Base Ported |
| `grab_using_exposure_end_event/` | Exposure end event optimization | Base Ported |

### Device Management
| Sample | Description | Status |
|--------|-------------|--------|
| `device_removal_handling/` | Robust device disconnection handling | Base Ported |

## Key Features Demonstrated

### Foundation Features
- **Basic Image Acquisition**: Error handling, resource management, grab result processing
- **Grabbing Strategies**: OneByOne, LatestImageOnly, LatestImages, UpcomingImage
- **Multi-Camera Systems**: InstantCameraArray usage, camera context management
- **Configuration Persistence**: Saving/loading camera configurations with FeaturePersistence

### Parameter Management
- **Generic Access**: String-based parameter access using GenApi nodemap
- **Native Access**: Direct property access for type safety and IDE support
- **Configuration Handlers**: Event-driven camera setup and configuration
- **User Sets**: Complete camera configuration management and default settings
- **Auto Functions**: Automatic gain, exposure, and white balance control
- **SFNC Compatibility**: Support for different SFNC versions (1.x vs 2.0+)

### Advanced Grabbing
- **Camera Events**: Exposure end, event overrun, and other camera-generated events
- **Chunk Data**: Accessing metadata embedded in images (timestamps, counters, CRC)
- **Multi-Threading**: Background grabbing with grab loop threads
- **Sequencer**: Automated parameter changes during acquisition
- **Action Commands**: Synchronized multi-camera triggering for GigE cameras
- **Buffer Management**: Custom buffer allocation and external library integration
- **Exposure Events**: Optimized workflows using exposure end notifications

### Device Management
- **Robust Connectivity**: Automatic reconnection, status monitoring, thread-safe operations
- **Error Recovery**: Comprehensive error handling and graceful degradation
- **Resource Management**: Proper cleanup and resource lifecycle management

## Sample Structure

Each sample follows a consistent structure:

```
sample_name/
├── sample_name.py          # Main implementation
└── README.md              # Comprehensive documentation
```

### Documentation Features
- **Detailed explanations** of concepts and implementation
- **Code highlights** with key snippets
- **Sample output** showing expected results
- **Troubleshooting guides** for common issues
- **Advanced usage patterns** for complex scenarios
- **Related samples** for further learning

## Learning Path

### Beginner Path
1. Start with `grab/` for basic concepts
2. Learn different strategies with `grab_strategies/`
3. Explore parameter access with `parametrize_camera_native_parameter_access/`
4. Understand configuration with `parametrize_camera_load_and_save/`

### Intermediate Path
5. Multi-camera systems with `grab_multiple_cameras/`
6. Auto functions with `parametrize_camera_auto_functions/`
7. Event handling with `grab_camera_events/`
8. Chunk data with `grab_chunk_image/`

### Advanced Path
9. Multi-threading with `grab_using_grab_loop_thread/`
10. Sequencer automation with `grab_using_sequencer/`
11. Action commands with `grab_using_action_command/`
12. Custom buffers with `grab_using_buffer_factory/`
13. Timing optimization with `grab_using_exposure_end_event/`

## Best Practices Demonstrated

### Error Handling
- Comprehensive exception handling for GenericException and general exceptions
- Graceful degradation when features are not available
- Resource cleanup in finally blocks

### Type Safety
- Type hints throughout all implementations
- Proper use of Optional types for nullable values
- Clear parameter and return type specifications

### Resource Management
- Proper camera opening/closing patterns
- Grab result release management
- Memory cleanup and garbage collection

### Performance Optimization
- Efficient grabbing strategies selection
- Buffer management for high-throughput applications
- Multi-threading for concurrent operations

### Cross-Platform Compatibility
- Support for both Windows and Linux
- Proper handling of different camera types (GigE vs USB)
- SFNC version compatibility

## Running Samples

### Prerequisites
```bash
pip install pypylon numpy
```

### Basic Usage
```bash
cd samples_reference_pypylon/grab/
python grab.py
```

### With Emulated Cameras
Most samples support emulated cameras for testing without hardware:
```bash
# The samples automatically detect and use emulated cameras when available
python grab.py
```

## Related Resources

- **Original C++ Samples**: `samples_reference_c++/`
- **Porting Strategy**: `PORTING_STRATEGY.md`
- **pypylon Documentation**: [pypylon GitHub](https://github.com/basler/pypylon)
- **Basler Product Documentation**: Camera-specific feature documentation

## Future Phases

The remaining phases will cover:

- **Phase 4**: Image Processing (Utility_* samples)
- **Phase 5**: Network Features (GigE-specific functionality)
- **Phase 6**: Data Processing (pylondataprocessing samples)
- **Phase 7**: GUI and Integration (Qt samples and special features)

---

*This reference sample collection provides a comprehensive foundation for pypylon development, demonstrating professional coding practices and advanced camera control techniques.* 