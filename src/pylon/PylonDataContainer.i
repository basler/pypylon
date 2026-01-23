%rename(PylonDataContainer) Pylon::CPylonDataContainer;

%ignore CPylonDataContainerImpl;
%ignore GetDataComponent;

%include <pylon/PylonVersionNumber.h>;
%include <pylon/PylonDataContainer.h>;

%extend Pylon::CPylonDataContainer {
    // To allow the instant camera to reuse the CGrabResultData
    // and prevent buffer underruns, you must release the PylonDataContainer and all its PylonDataComponent objects.
    void Release()
    {
        *($self) = Pylon::CPylonDataContainer();
    }

    // Access to get data components overloaded methods
    %pythoncode %{
    @deprecated("Use GetDataComponentByIndex instead.")
    def GetDataComponent(self, param):
        return self.GetDataComponentByIndex(param)
    %}

    const Pylon::CPylonDataComponent GetDataComponentByIndex(const size_t index) const {
        return $self->GetDataComponent(index);
    }

#if (PYLON_VERSION_MAJOR > 11) || (PYLON_VERSION_MAJOR == 11 && PYLON_VERSION_MINOR >= 3)

    const Pylon::PylonDataComponentList GetDataComponentByType(const Pylon::EComponentType componentType) const {
        return $self->GetDataComponent(componentType);
    }

#endif
};