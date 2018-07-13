%rename (Device) Pylon::IDevice;
%include<pylon/Device.h>;
%pythoncode %{
    IDevice = Device
%}
