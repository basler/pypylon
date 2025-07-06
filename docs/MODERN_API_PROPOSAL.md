# Modern C++ API Compatibility for pypylon

This document outlines the implementation of complete modern C++ API compatibility for pypylon, exactly matching the actual Pylon SDK patterns discovered by examining `/opt/pylon/include/pylon/`.

## Problem Statement

Current pypylon requires verbose API calls:
```python
geni.IsWritable(self.camera.ExposureTimeRaw.Node)
```

Modern C++ Pylon SDK provides:
```cpp
camera.ExposureTimeRaw.IsWritable()
```

**Goal**: Enable identical API in Python:
```python
self.camera.ExposureTimeRaw.IsWritable()
```

## Implementation: Exact SDK Pattern Matching

Based on examination of the actual Pylon SDK headers, we've implemented **exact interface matching** with the C++ SDK.

### Core Interfaces Implemented

#### 1. **IValueEx Interface** (Base for all parameters)
Matches: `/opt/pylon/include/pylon/Parameter.h`

```python
# All parameters inherit these methods
param.IsWritable()                                  # -> bool
param.IsReadable()                                  # -> bool  
param.IsValid()                                     # -> bool
param.GetInfo(EParameterInfo.ParameterInfo_Name)    # -> string
param.GetInfoOrDefault(info, "default")             # -> string
param.ToStringOrDefault("default")                  # -> string
```

#### 2. **IIntegerEx Interface** 
Matches: `/opt/pylon/include/pylon/IntegerParameter.h`

```python
# Integer parameters (ExposureTimeRaw, Width, Height, etc.)
param.TrySetValue(1000)                             # -> bool
param.GetValueOrDefault(500)                        # -> int64
param.TrySetValue(1000, EIntegerValueCorrection.IntegerValueCorrection_Nearest)  # -> bool
param.SetValue(1000, EIntegerValueCorrection.IntegerValueCorrection_Up)
param.GetValuePercentOfRange()                      # -> double
param.SetValuePercentOfRange(50.0)                  # Set to 50% of range
param.TrySetValuePercentOfRange(75.0)               # -> bool
param.SetToMaximum()                                # Set to max value
param.SetToMinimum()                                # Set to min value  
param.TrySetToMaximum()                             # -> bool
param.TrySetToMinimum()                             # -> bool
```

#### 3. **IEnumerationEx Interface**
Matches: `/opt/pylon/include/pylon/EnumParameter.h`

```python
# Enumeration parameters (PixelFormat, TriggerMode, etc.)
param.TrySetValue("Mono8")                          # -> bool
param.CanSetValue("RGB8")                           # -> bool
param.GetValueOrDefault("Unknown")                  # -> string
param.SetValue(["BayerGR8", "BayerRG8", "Mono8"])  # Set first available
param.TrySetValue(["BayerGR8", "BayerRG8", "Mono8"]) # -> bool
```

#### 4. **IBooleanEx Interface**
Matches: `/opt/pylon/include/pylon/BooleanParameter.h`

```python
# Boolean parameters (ReverseX, ReverseY, etc.)
param.TrySetValue(True)                             # -> bool
param.GetValueOrDefault(False)                      # -> bool
```

#### 5. **ICommandEx Interface**
Matches: `/opt/pylon/include/pylon/CommandParameter.h`

```python
# Command parameters (TriggerSoftware, UserSetLoad, etc.)
param.TryExecute()                                  # -> bool
param.IsDone()                                      # -> bool
```

#### 6. **IFloatEx Interface** (Additional implementation)
```python
# Float parameters (ExposureTime, Gain, etc.)
param.TrySetValue(1.5)                              # -> bool
param.GetValueOrDefault(1.0)                        # -> double
```

#### 7. **IStringEx Interface** (Additional implementation)
```python
# String parameters
param.TrySetValue("test")                           # -> bool
param.GetValueOrDefault("default")                  # -> string
```

### Value Correction Enums (Exact SDK Match)

```python
from pypylon import pylon as py

# Matches EIntegerValueCorrection from SDK
py.EIntegerValueCorrection.IntegerValueCorrection_None     # No correction
py.EIntegerValueCorrection.IntegerValueCorrection_Up       # Round up  
py.EIntegerValueCorrection.IntegerValueCorrection_Down     # Round down
py.EIntegerValueCorrection.IntegerValueCorrection_Nearest  # Round to nearest

# Matches EParameterInfo from SDK  
py.EParameterInfo.ParameterInfo_Name                       # Parameter name
py.EParameterInfo.ParameterInfo_DisplayName                # Display name
py.EParameterInfo.ParameterInfo_ToolTip                    # Short description
py.EParameterInfo.ParameterInfo_Description                # Long description
```

## Key Implementation Features

### 1. **Type-Specific Parameter Wrappers**
- **Factory Function**: `CreateParameterWrapper(node)` automatically returns the correct type
- **Automatic Detection**: Based on dynamic casting (Integer, Float, Boolean, Enum, Command, String)
- **Fallback Handling**: Unknown types get base `PyValueEx` interface

### 2. **Enhanced InstantCamera Integration**
```python
# Automatic parameter wrapping
exposure = camera.ExposureTimeRaw  # Returns PyIntegerEx automatically
width = camera.Width               # Returns PyIntegerEx automatically  
pixel_format = camera.PixelFormat  # Returns PyEnumerationEx automatically

# Helper methods
camera.GetParameter("Width")           # Explicit parameter access
camera.HasParameter("CustomParam")    # Parameter existence check
camera.IsParameterWritable("Width")   # Writability check
camera.TrySetParameter("Width", 640)  # Safe parameter setting
```

### 3. **Improved Error Handling with Parameter Names**
**Problem Solved**: The original error "Node not existing" was unhelpful.

**Before:**
```
[ERROR] GenICam exception: Node not existing (file 'genicamPYTHON_wrap.cxx', line 16822)
```

**After:**
```python
# Helpful error messages with parameter names
try:
    param = camera.NonExistentParameter
except AttributeError as e:
    print(e)  # "Camera parameter access failed: Parameter 'NonExistentParameter' does not exist on this camera/device"

# Safe methods that don't throw exceptions
camera.HasParameter("FakeParam")           # Returns False
camera.IsParameterWritable("FakeParam")    # Returns False  
camera.TrySetParameter("FakeParam", 123)   # Returns False

# Detailed parameter information
try:
    info = camera.GetParameterInfo("FakeParam")
except RuntimeError as e:
    print(e)  # "Failed to get parameter info for 'FakeParam': Parameter 'FakeParam' does not exist on this camera/device"
```

**Error Handling Features:**
- **Parameter Names in Errors**: All error messages include the requested parameter name
- **Context-Aware Messages**: Different error types (missing, read-only, etc.) have specific messages
- **Safe Fallback Methods**: Try* and Has* methods that return False instead of throwing
- **Detailed Error Context**: Information about what operation failed and why

### 4. **Value Correction Algorithm** 
Exact implementation matching SDK logic:

```python
def CorrectIntegerValue(value, min_val, max_val, inc, correction):
    # Range clipping
    corrected = max(min_val, min(max_val, value))
    
    # Increment alignment
    if inc > 1:
        remainder = (corrected - min_val) % inc
        if remainder != 0:
            if correction == IntegerValueCorrection_Up:
                corrected += (inc - remainder)
            elif correction == IntegerValueCorrection_Down:
                corrected -= remainder  
            elif correction == IntegerValueCorrection_Nearest:
                if remainder <= inc // 2:
                    corrected -= remainder
                else:
                    corrected += (inc - remainder)
    
    return max(min_val, min(max_val, corrected))
```

## Complete Usage Examples

### Basic Parameter Access
```python
from pypylon import pylon as py

camera = py.InstantCamera()
camera.Open()

# Modern C++ API style - exact SDK match
exposure = camera.ExposureTimeRaw
print(f"Writable: {exposure.IsWritable()}")
print(f"Current: {exposure.GetValue()}")
print(f"Range: {exposure.GetMin()} - {exposure.GetMax()}")
```

### Safe Parameter Operations
```python
# Safe setting with error handling
if exposure.TrySetValue(10000):
    print("✓ Set exposure successfully")
else:
    print("✗ Failed to set exposure")

# Value correction
if exposure.TrySetValue(9999, py.EIntegerValueCorrection.IntegerValueCorrection_Nearest):
    print(f"✓ Set exposure with correction: {exposure.GetValue()}")
```

### Range Operations
```python
# Percentage-based setting
exposure.SetValuePercentOfRange(25.0)  # Set to 25% of range
print(f"Current range percentage: {exposure.GetValuePercentOfRange():.1f}%")

# Min/max operations
if exposure.TrySetToMinimum():
    print(f"✓ Set to minimum: {exposure.GetValue()}")
```

### Enumeration Operations
```python
pixel_format = camera.PixelFormat

# Check available values
formats = ["Mono8", "Mono12", "RGB8", "BayerGR8"]
for fmt in formats:
    if pixel_format.CanSetValue(fmt):
        print(f"✓ {fmt} is available")

# Safe setting
if pixel_format.TrySetValue("Mono8"):
    print("✓ Changed to Mono8")
```

### Command Operations
```python
if hasattr(camera, 'TriggerSoftware'):
    trigger = camera.TriggerSoftware
    if trigger.TryExecute():
        print("✓ Software trigger executed")
```

### Error Handling Examples
```python
# Old API - vague error
try:
    node = camera.GetNodeMap().GetNode("FakeParam")
    value = node.GetValue()  # "Node not existing" - unhelpful!
except:
    pass

# New API - helpful error with parameter name
try:
    param = camera.FakeParam
except AttributeError as e:
    print(e)  # "Camera parameter access failed: Parameter 'FakeParam' does not exist on this camera/device"

# Safe methods - no exceptions
if camera.HasParameter("FakeParam"):        # Returns False
    value = camera.FakeParam.GetValue()
else:
    print("Parameter 'FakeParam' not available")

# Try setting with helpful feedback
if not camera.TrySetParameter("Width", 1000):
    print("Failed to set Width - parameter may not exist or not be writable")
```

## Backward Compatibility

**Complete backward compatibility** is maintained:

```python
# Old API still works
width_node = camera.GetNodeMap().GetNode("Width")
old_writable = geni.IsWritable(width_node)

# New API works alongside
width_param = camera.Width  
new_writable = width_param.IsWritable()

# Mixed usage is fine
assert old_writable == new_writable
```

## Benefits Summary

✅ **100% SDK Compatibility**: Exact interface matching with Pylon C++ SDK  
✅ **Type Safety**: Automatic type-specific parameter wrappers  
✅ **Error Safety**: Try* methods for safe operations  
✅ **Range Operations**: Percentage, min/max, value correction  
✅ **Full Backward Compatibility**: Existing code continues to work  
✅ **Enhanced Error Handling**: Robust parameter validation with helpful messages  
✅ **Modern API**: Clean, intuitive parameter access  

## Implementation Files

1. **`src/pylon/NodeWrapper.i`** - Core extended parameter classes
2. **`src/pylon/InstantCamera.i`** - Enhanced camera integration  
3. **`samples/modern_api_demo.py`** - Comprehensive demonstration
4. **`samples/error_handling_demo.py`** - Focused error handling demonstration
5. **`docs/MODERN_API_PROPOSAL.md`** - This documentation

This implementation provides **complete API parity** with the modern Pylon C++ SDK while maintaining full backward compatibility with existing pypylon code. 