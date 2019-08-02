%rename(DeviceInfo) Pylon::CDeviceInfo;

%ignore DeviceIdxKey;
%include <pylon/DeviceInfo.h>;

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}