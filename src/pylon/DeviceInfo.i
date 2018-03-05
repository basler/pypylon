%rename(DeviceInfo) Pylon::CDeviceInfo;

#define ManufacturerInfoKey ManufacturerInfoKeyIGNORE=

%ignore ManufacturerInfoKeyIGNORE;
%ignore DeviceIdxKey;
%include <pylon/DeviceInfo.h>;

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}