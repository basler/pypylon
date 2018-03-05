
namespace std
{
    %template(deviceinfo_vector) std::vector<CDeviceInfo>;
    %template(tlinfo_vector) std::vector<CTlInfo>;
}

namespace Pylon
{
    typedef tlinfo_vector TlInfoList_t;
    typedef deviceinfo_vector DeviceInfoList_t;
}
