%rename (Device) Pylon::IDevice;
%include<Device.h>;
%pythoncode %{
    IDevice = Device
%}
