%rename(PylonDataContainer) Pylon::CPylonDataContainer;

%ignore CPylonDataContainerImpl;

%include <pylon/PylonDataContainer.h>;
%extend Pylon::CPylonDataContainer {
    // To allow the instant camera to reuse the CGrabResultData
    // and prevent buffer underruns, you must release the PylonDataContainer and all its PylonDataComponent objects.
    void Release()
    {
        *($self) = Pylon::CPylonDataContainer();
    }
};