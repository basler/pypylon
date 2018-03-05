%rename(InstantCameraArray) Pylon::CInstantCameraArray;

%pythonprepend Pylon::CInstantCameraArray::operator[]( size_t index) %{
    if index >= self.GetSize():
        raise IndexError
%}
%ignore Pylon::CInstantCameraArray::operator[]( size_t index) const;
%rename(__getitem__) Pylon::CInstantCameraArray::operator[]( size_t index);


%include <pylon/InstantCameraArray.h>;