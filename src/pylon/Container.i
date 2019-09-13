
namespace std
{
    %template(tlinfo_vector) std::vector<CTlInfo>;
    %template(interfaceinfo_vector) std::vector<CInterfaceInfo>;
    %template(deviceinfo_vector) std::vector<CDeviceInfo>;
}

namespace Pylon
{
    typedef tlinfo_vector TlInfoList_t;
    typedef interfaceinfo_vector InterfaceInfoList_t;
    typedef deviceinfo_vector DeviceInfoList_t;
}
