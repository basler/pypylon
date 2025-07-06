%rename (InstantCamera) Pylon::CInstantCamera;

%ignore IInstantCameraExtensions;
%ignore GetExtensionInterface;
%ignore CGrabResultDataFactory;
%ignore CreateDeviceSpecificGrabResultData;
%ignore CreateGrabResultData;

#define AutoLock GENAPI_NAMESPACE::AutoLock
#define CLock GENAPI_NAMESPACE::CLock

%rename(ConfigurationEventHandler) Pylon::CConfigurationEventHandler;
%rename(ImageEventHandler) Pylon::CImageEventHandler;
%rename(CameraEventHandler) Pylon::CCameraEventHandler;
%rename(StartGrabbingMax) StartGrabbing( size_t maxImages, EGrabStrategy strategy = GrabStrategy_OneByOne, EGrabLoop grabLoopType = GrabLoop_ProvidedByUser);

namespace Pylon {
     class CConfigurationEventHandler;
     class CImageEventHandler;
     class CCameraEventHandler;
};


%ignore CanWaitForFrameTriggerReady;

%extend Pylon::CInstantCamera {
    PROP_GET(QueuedBufferCount)
    PROP_GETSET(CameraContext)
    PROP_GET(DeviceInfo)
    PROP_GET(NodeMap)
    PROP_GET(TLNodeMap)
    PROP_GET(StreamGrabberNodeMap)
    PROP_GET(EventGrabberNodeMap)
    PROP_GET(InstantCameraNodeMap)
%pythoncode %{
    # Enhanced properties that return wrapped nodemaps
    @property
    def StreamGrabber(self):
        if self.IsOpen():
            return _StreamGrabberWrapper(self.GetStreamGrabberNodeMap())
        return None
    
    @property 
    def EventGrabber(self):
        if self.IsOpen():
            return _EventGrabberWrapper(self.GetEventGrabberNodeMap())
        return None
    
    @property
    def TransportLayer(self):
        return _TransportLayerWrapper(self.GetTLNodeMap())

    def __getattr__(self, attribute):
        if hasattr(InstantCameraParams_Params, attribute) or attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            # Return type-specific enhanced wrapper with modern C++ API methods
            wrapper = CreateParameterWrapperTyped(self.GetNodeMap(), attribute)
            if wrapper is None:
                raise AttributeError(f"Camera parameter '{attribute}' not found or not available")
            return wrapper

    def __setattr__(self, attribute, val):
        if hasattr(InstantCameraParams_Params, attribute) or attribute.startswith("_") or attribute == "this" or attribute == "thisown":
            object.__setattr__(self, attribute, val)
        else:
            # Support setting parameter values directly via attribute access
            try:
                wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), attribute)
                if wrapper and wrapper.IsWritable():
                    # Try to determine the appropriate setter based on value type
                    if isinstance(val, bool):
                        if hasattr(wrapper, 'SetValue') and hasattr(wrapper, 'GetValue'):
                            # Check if it's a boolean parameter by trying to get a boolean value
                            try:
                                wrapper.SetValue(val)
                            except:
                                # Fallback to string representation
                                wrapper.SetValue(str(val))
                    elif isinstance(val, int):
                        if hasattr(wrapper, 'SetValue'):
                            wrapper.SetValue(val)
                    elif isinstance(val, float):
                        if hasattr(wrapper, 'SetValue'):
                            wrapper.SetValue(val)
                    elif isinstance(val, str):
                        if hasattr(wrapper, 'SetValue'):
                            wrapper.SetValue(val)
                    else:
                        # Fallback to string representation
                        if hasattr(wrapper, 'SetValue'):
                            wrapper.SetValue(str(val))
                else:
                    if wrapper and not wrapper.IsWritable():
                        raise AttributeError(f"Camera parameter '{attribute}' is not writable")
                    else:
                        object.__setattr__(self, attribute, val)
            except RuntimeError as e:
                raise AttributeError(f"Failed to set camera parameter '{attribute}': {str(e)}") from e
            except Exception as e:
                # Fallback - try normal attribute setting
                object.__setattr__(self, attribute, val)

    def __dir__(self):
        """Provide autocompletion support by listing all available camera parameters."""
        l = []
        # Include built-in methods and properties from the class
        l += [x for x in dir(type(self))]
        l += [x for x in self.__dict__.keys()]
        
        # Include all camera parameters from the nodemap
        try:
            if hasattr(self, 'GetNodeMap'):
                nodemap = self.GetNodeMap()
                nodes = nodemap.GetNodes()
                features = filter(lambda n: n.GetNode().IsFeature(), nodes)
                l += [x.GetNode().GetName() for x in features]
        except:
            pass
            
        return sorted(set(l))
    
    # Helper methods for modern C++ style access
    def GetParameter(self, name):
        """Get a parameter wrapper with extended methods like TrySetValue, IsWritable, etc.
        
        Args:
            name (str): Name of the parameter to access
            
        Returns:
            Parameter wrapper with extended methods, or None if parameter doesn't exist
            
        Raises:
            RuntimeError: If parameter access fails with details about the failure
        """
        try:
            return CreateParameterWrapperSafe(self.GetNodeMap(), name)
        except RuntimeError as e:
            # Re-raise with method context
            raise RuntimeError(f"GetParameter('{name}') failed: {str(e)}") from e
    
    def HasParameter(self, name):
        """Check if a parameter exists and is valid.
        
        Args:
            name (str): Name of the parameter to check
            
        Returns:
            bool: True if parameter exists and is valid, False otherwise
        """
        try:
            wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), name)
            return wrapper is not None and wrapper.IsValid()
        except:
            return False
    
    def IsParameterWritable(self, name):
        """Check if a parameter is writable using modern C++ API style.
        
        Args:
            name (str): Name of the parameter to check
            
        Returns:
            bool: True if parameter exists and is writable, False otherwise
        """
        try:
            wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), name)
            return wrapper.IsWritable() if wrapper else False
        except:
            return False
    
    def IsParameterReadable(self, name):
        """Check if a parameter is readable using modern C++ API style.
        
        Args:
            name (str): Name of the parameter to check
            
        Returns:
            bool: True if parameter exists and is readable, False otherwise
        """
        try:
            wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), name)
            return wrapper.IsReadable() if wrapper else False
        except:
            return False
    
    def TrySetParameter(self, name, value):
        """Try to set a parameter value, returns True if successful.
        
        Args:
            name (str): Name of the parameter to set
            value: Value to set (int, float, str, bool)
            
        Returns:
            bool: True if parameter was set successfully, False otherwise
        """
        try:
            wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), name)
            if wrapper and hasattr(wrapper, 'TrySetValue'):
                return wrapper.TrySetValue(value)
            return False
        except:
            return False
    
    def GetParameterInfo(self, name):
        """Get detailed information about a parameter.
        
        Args:
            name (str): Name of the parameter
            
        Returns:
            dict: Parameter information including name, type, range, etc.
            
        Raises:
            RuntimeError: If parameter doesn't exist or access fails
        """
        try:
            wrapper = CreateParameterWrapperSafe(self.GetNodeMap(), name)
            if not wrapper:
                raise RuntimeError(f"Parameter '{name}' not found")
            
            info = {
                'name': name,
                'valid': wrapper.IsValid(),
                'readable': wrapper.IsReadable(),
                'writable': wrapper.IsWritable(),
            }
            
            # Add type-specific information
            if hasattr(wrapper, 'GetMin') and hasattr(wrapper, 'GetMax'):
                # Integer/Float parameter
                info.update({
                    'type': 'integer' if hasattr(wrapper, 'GetInc') else 'float',
                    'current_value': wrapper.GetValue() if wrapper.IsReadable() else None,
                    'min_value': wrapper.GetMin(),
                    'max_value': wrapper.GetMax(),
                })
                if hasattr(wrapper, 'GetInc'):
                    info['increment'] = wrapper.GetInc()
            elif hasattr(wrapper, 'CanSetValue'):
                # Enumeration parameter
                info.update({
                    'type': 'enumeration',
                    'current_value': wrapper.GetValue() if wrapper.IsReadable() else None,
                })
            elif hasattr(wrapper, 'TryExecute'):
                # Command parameter
                info.update({
                    'type': 'command',
                    'is_done': wrapper.IsDone() if hasattr(wrapper, 'IsDone') else None,
                })
            else:
                # Generic parameter
                info['type'] = 'generic'
                if wrapper.IsReadable():
                    try:
                        info['current_value'] = wrapper.GetValue()
                    except:
                        pass
            
            return info
            
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to get parameter info for '{name}': {str(e)}") from e

    def GetIntegerParameter(self, parameterName):
        """Get a parameter as PyIntegerEx type."""
        try:
            result = CreateIntegerParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not an integer parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get integer parameter '{parameterName}': {str(e)}")

    def GetEnumerationParameter(self, parameterName):
        """Get a parameter as PyEnumerationEx type."""
        try:
            result = CreateEnumerationParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not an enumeration parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get enumeration parameter '{parameterName}': {str(e)}")

    def GetBooleanParameter(self, parameterName):
        """Get a parameter as PyBooleanEx type."""
        try:
            result = CreateBooleanParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not a boolean parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get boolean parameter '{parameterName}': {str(e)}")

    def GetCommandParameter(self, parameterName):
        """Get a parameter as PyCommandEx type."""
        try:
            result = CreateCommandParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not a command parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get command parameter '{parameterName}': {str(e)}")

    def GetFloatParameter(self, parameterName):
        """Get a parameter as PyFloatEx type."""
        try:
            result = CreateFloatParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not a float parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get float parameter '{parameterName}': {str(e)}")

    def GetStringParameter(self, parameterName):
        """Get a parameter as PyStringEx type."""
        try:
            result = CreateStringParameter(self.GetNodeMap(), parameterName)
            if result is None:
                raise ValueError(f"Parameter '{parameterName}' not found or not a string parameter")
            return result
        except Exception as e:
            raise ValueError(f"Failed to get string parameter '{parameterName}': {str(e)}")
%}
}

%pythonprepend Pylon::CInstantCamera::RegisterConfiguration %{
    if cleanupProcedure == Cleanup_Delete:
        pConfigurator.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterImageEventHandler %{
    if cleanupProcedure == Cleanup_Delete:
        pImageEventHandler.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterCameraEventHandler %{
    assert(len(args) > 4)
    if args[4] == Cleanup_Delete:
        args[0].__disown__()
    elif args[4] == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}

// Include enum headers (always available in Pylon v7.0+)
%include <pylon/ECleanup.h>;
%include <pylon/ERegistrationMode.h>;
%include <pylon/ETimeoutHandling.h>;

%include <pylon/InstantCamera.h>;
