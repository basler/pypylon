%rename(Recipe) Pylon::DataProcessing::CRecipe;
%rename(OutputObserver) Pylon::DataProcessing::IOutputObserver;

%ignore GetParameters;
%ignore GetInputTypeName;
%ignore GetOutputTypeName;
%ignore UnregisterOutputObserver;
%ignore RegisterOutputObserver;
%ignore TriggerUpdate;
%ignore TriggerUpdateAsync;

%ignore GetOutputNames;
%rename(GetOutputNames) GetOutputNames2;
%rename(UnregisterOutputObserver) UnregisterOutputObserver2;
%rename(RegisterOutputObserver) RegisterOutputObserver2;
%rename(TriggerUpdate) TriggerUpdate2;
%rename(TriggerUpdateAsync) TriggerUpdateAsync2;

#define CLock GENAPI_NAMESPACE::CLock

%typemap(typecheck,precedence=SWIG_TYPECHECK_CHAR)  (const void* pBuffer, size_t bufferSize)
   %{
       $1 = (PyBytes_Check($input) || PyByteArray_Check($input)) ? 1 : 0;
   %}

%typemap(in) (const void* pBuffer, size_t bufferSize)
    %{
        if (PyBytes_Check($input)) {
            $1 = PyBytes_AsString($input);
            $2 = PyBytes_Size($input);
        } else if (PyByteArray_Check($input)) {
            $1 = PyByteArray_AsString($input);
            $2 = PyByteArray_Size($input);
        } else {
            PyErr_SetString(
              PyExc_TypeError,
              "Invalid type of buffer (bytes and bytearray are supported)!."
            );
            SWIG_fail;
        }
    %}

%include <pylondataprocessing/Recipe.h>;

%extend Pylon::DataProcessing::CRecipe {

    void GetOutputNames2(StringList_t& result) const
    {
        $self->GetOutputNames(result);
    }
    
    void GetAllParameterNames(StringList_t& result)
    {
        result = $self->GetParameters().GetAllParameterNames();
    }
    
    bool ContainsParameter(const Pylon::String_t& fullname)
    {
        bool result = $self->GetParameters().Contains(fullname);
        return result;
    }

    GenApi::INode* GetParameter(const Pylon::String_t& fullname)
    {
        GenApi::INode* pNode = $self->GetParameters().Get(fullname).GetNode();
		return pNode;
    }
    
    void RegisterOutputObserver2(const StringList_t& outputFullNames, IOutputObserver* pObserver, ERegistrationMode mode, intptr_t userProvidedId = 0)
    {
        $self->RegisterOutputObserver(outputFullNames, pObserver, mode, userProvidedId);
    }
    
    bool UnregisterOutputObserver2(IOutputObserver* pObserver, intptr_t userProvidedId = 0)
    {
        bool result = $self->UnregisterOutputObserver(pObserver, userProvidedId);
        return result;
    }
    
    Pylon::DataProcessing::CUpdate TriggerUpdateAsync2(Pylon::DataProcessing::CVariantContainer inputCollection, Pylon::DataProcessing::IUpdateObserver* pObserver = nullptr, intptr_t userProvidedId = 0)
    {
        Pylon::DataProcessing::CUpdate result = self->TriggerUpdateAsync(inputCollection, pObserver, userProvidedId);
        return result;
    }
    
    Pylon::DataProcessing::CUpdate TriggerUpdate2(Pylon::DataProcessing::CVariantContainer inputCollection, unsigned int timeoutMs, Pylon::ETimeoutHandling timeoutHandling = Pylon::TimeoutHandling_ThrowException, Pylon::DataProcessing::IUpdateObserver* pObserver = nullptr, intptr_t userProvidedId = 0)
    {
        Pylon::DataProcessing::CUpdate result = self->TriggerUpdate(inputCollection, timeoutMs, timeoutHandling, pObserver, userProvidedId);
        return result;
    }

    %pythoncode %{
        def __getattr__(self, attribute):
            if attribute.startswith("_") or attribute in ("thisown", "this"):
                return object.__getattribute__(self, attribute)
            
            # Return type-specific enhanced wrapper with modern C++ API methods
            # Use pylon module's factory functions to ensure consistent types
            try:
                import pypylon.pylon as pylon
                wrapper = pylon.CreateParameterWrapperTyped(self.GetParameters().GetNodeMap(), attribute)
                if wrapper is None:
                    raise AttributeError(f"Parameter '{attribute}' not found or not available")
                return wrapper
            except Exception as e:
                raise AttributeError(f"Failed to access parameter '{attribute}': {str(e)}")
        
        def __setattr__(self, attribute, val):
            if attribute.startswith("_") or attribute in ("thisown", "this"):
                object.__setattr__(self, attribute, val)
            else:
                # Support setting parameter values directly via attribute access
                try:
                    import pypylon.pylon as pylon
                    wrapper = pylon.CreateParameterWrapperSafe(self.GetParameters().GetNodeMap(), attribute)
                    if wrapper and wrapper.IsWritable():
                        # Try to determine the appropriate setter based on value type
                        if isinstance(val, bool):
                            wrapper.SetValue(val)
                        elif isinstance(val, (int, float, str)):
                            wrapper.SetValue(val)
                        else:
                            wrapper.SetValue(str(val))
                    else:
                        if wrapper and not wrapper.IsWritable():
                            raise AttributeError(f"Parameter '{attribute}' is not writable")
                        else:
                            object.__setattr__(self, attribute, val)
                except Exception as e:
                    raise AttributeError(f"Failed to set parameter '{attribute}': {str(e)}") from e
        
        def __dir__(self):
            """Provide autocompletion support by listing all available parameters."""
            l = []
            l += [x for x in dir(type(self))]
            l += [x for x in self.__dict__.keys()]
            try:
                nodes = self.GetParameters().GetNodeMap().GetNodes()
                features = filter(lambda n: n.GetNode().IsFeature(), nodes)
                # Skip ICategory nodes as they are just organizational containers
                l += [x.GetNode().GetName() for x in features 
                      if x.GetNode().GetPrincipalInterfaceType() != genicam.intfICategory]
            except:
                pass
            return sorted(set(l))
        
        def GetParameter(self, name):
            """Get a parameter wrapper with extended methods."""
            import pypylon.pylon as pylon
            return pylon.CreateParameterWrapperSafe(self.GetParameters().GetNodeMap(), name)
        
        def HasParameter(self, name):
            """Check if a parameter exists and is valid."""
            try:
                import pypylon.pylon as pylon
                wrapper = pylon.CreateParameterWrapperSafe(self.GetParameters().GetNodeMap(), name)
                return wrapper is not None and wrapper.IsValid()
            except:
                return False
        
        def IsParameterWritable(self, name):
            """Check if a parameter is writable."""
            try:
                import pypylon.pylon as pylon
                wrapper = pylon.CreateParameterWrapperSafe(self.GetParameters().GetNodeMap(), name)
                return wrapper is not None and wrapper.IsWritable()
            except:
                return False
        
        def TrySetParameter(self, name, value):
            """Try to set a parameter value safely."""
            try:
                import pypylon.pylon as pylon
                wrapper = pylon.CreateParameterWrapperSafe(self.GetParameters().GetNodeMap(), name)
                if wrapper and wrapper.IsWritable():
                    wrapper.SetValue(value)
                    return True
                return False
            except:
                return False
    %}
}
