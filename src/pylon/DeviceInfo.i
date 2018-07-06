%rename(DeviceInfo) Pylon::CDeviceInfo;

#define ManufacturerInfoKey ManufacturerInfoKeyIGNORE=

%ignore ManufacturerInfoKeyIGNORE;
%ignore DeviceIdxKey;
%include <DeviceInfo.h>;

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}