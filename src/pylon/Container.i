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

// Add converter to handle PylonDataComponentList correctly, available since pylon C++ SDK 11.3.0
//
%include <pylon/PylonVersionNumber.h>;

#if (PYLON_VERSION_MAJOR > 11) || (PYLON_VERSION_MAJOR == 11 && PYLON_VERSION_MINOR >= 3)

namespace std
{
    %template(pylondatacomponent_vector) std::vector<CPylonDataComponent>;
}

namespace Pylon
{
    typedef pylondatacomponent_vector PylonDataComponentList;
}

%typemap(out) Pylon::PylonDataComponentList {
    $result = PyList_New($1.size());
    for (size_t i = 0; i < $1.size(); ++i) {
        PyObject* component = SWIG_NewPointerObj(
            new Pylon::CPylonDataComponent($1[i]),
            SWIGTYPE_p_Pylon__CPylonDataComponent,
            SWIG_POINTER_OWN
        );
        PyList_SetItem($result, i, component);
    }
}

#endif