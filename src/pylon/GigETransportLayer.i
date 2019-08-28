%rename (GigETransportLayer) Pylon::IGigETransportLayer;
%nodefaultdtor Pylon::IGigETransportLayer;

////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList output for EnumerateAllDevices
//

%typemap(in, numinputs=0) (Pylon::DeviceInfoList_t&, bool addToList)
{
    $1 = new Pylon::DeviceInfoList_t();
    $2 = false;
}

%typemap(argout, fragment="t_output_helper") Pylon::DeviceInfoList_t&
{
  Py_DECREF($result);
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CDeviceInfo *di = new CDeviceInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(di),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}

// ensure the above typemap will not be applied to const references
%typemap(argout, noblock=1) const Pylon::DeviceInfoList_t & {}

////////////////////////////////////////////////////////////////////////////////
//
// CDeviceInfo output for AnnounceRemoteDevice
//

%typemap(in, numinputs=0) Pylon::CDeviceInfo*
{
    $1 = new Pylon::CDeviceInfo();
}

%typemap(argout) Pylon::CDeviceInfo*
{
    Py_DECREF($result);
    PyObject *tpl = PyTuple_New(2);
    PyTuple_SetItem(tpl, 0, $result);
    PyObject *di = SWIG_NewPointerObj(
        SWIG_as_voidptr($1),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, 1, di);
    // do NOT delete $1, since 'di' took ownership of it
    $result = tpl;
}

////////////////////////////////////////////////////////////////////////////////

// Ignore original 'AnnounceRemoteDevice' and create an overload for it in
// order to get easier type mapping.

%ignore Pylon::IGigETransportLayer::AnnounceRemoteDevice(
    const String_t& IpAddress,
    CDeviceInfo* pInfo=NULL
    );

%extend Pylon::IGigETransportLayer {
    // Create an overload for 'AnnounceRemoteDevice' for easier type mapping.
    bool AnnounceRemoteDevice(CDeviceInfo* pInfo, const String_t& IpAddress)
    {
        return $self->AnnounceRemoteDevice(IpAddress, pInfo);
    }
}


%include <pylon/gige/GigETransportLayer.h>;

////////////////////////////////////////////////////////////////////////////////
// now that the local typemaps are no longer needed, clear them.

%typemap(in) (Pylon::DeviceInfoList_t&, bool addToList);
%typemap(argout) Pylon::DeviceInfoList_t&;
%typemap(argout) const Pylon::DeviceInfoList_t&;
%typemap(in) Pylon::CDeviceInfo*;
%typemap(argout) Pylon::CDeviceInfo*;
