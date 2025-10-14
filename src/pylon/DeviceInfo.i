%rename(DeviceInfo) Pylon::CDeviceInfo;

%include <pylon/PylonVersionNumber.h>

%ignore DeviceIdxKey;
%include <pylon/DeviceInfo.h>;

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}

