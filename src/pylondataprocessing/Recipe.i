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
}
