
%ignore CSimpleMutex;
%ignore ITransportLayer;
%ignore TlMap;
%ignore ImplicitTlRefs;

%nodefaultctor Pylon::CTlFactory;
%rename(TlFactory) Pylon::CTlFactory;

////////////////////////////////////////////////////////////////////////////////
//
// TlInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::TlInfoList_t & {
  $1 = new Pylon::TlInfoList_t();
}

%typemap(argout,fragment="t_output_helper") Pylon::TlInfoList_t & {
  Py_DECREF($result);
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CTlInfo *ti = new CTlInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(ti),
        SWIGTYPE_p_Pylon__CTlInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}


////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::DeviceInfoList_t & {
  $1 = new DeviceInfoList_t();
}

%typemap(argout,fragment="t_output_helper") Pylon::DeviceInfoList_t & {
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
// DeviceInfoList intput
//
// needed for EnumerateDevices(
//     DeviceInfoList_t& list,
//     const DeviceInfoList_t& filter,
//     bool addToList = false
//     );
//

// Type check to make overloading work
%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER)
const Pylon::DeviceInfoList_t&
{
    // We need a list
    $1 = PyList_Check($input) ? 1 : 0;
}

// Convert a python list of wrapped DeviceInfos to a DeviceInfoList_t
%typemap(in, numinputs=1, noblock=1)
const Pylon::DeviceInfoList_t&
(Pylon::DeviceInfoList_t di_list)
{
    if (PyList_Check($input))
    {
        Py_ssize_t size = PyList_Size($input);
        for (Py_ssize_t i = 0; i < size; i++)
        {
            // python object possibly wrapping a DeviceInfo
            PyObject *o = PyList_GetItem($input,i);
            // pointer to wrapped DeviceInfo
            void *w = 0;
            if (!SWIG_IsOK(
                    SWIG_ConvertPtr(o, &w, SWIGTYPE_p_Pylon__CDeviceInfo, 0)
                    )
                )
            {
                PyErr_SetString(
                    PyExc_TypeError,
                    "list must contain DeviceInfo objects"
                    );
                return NULL;
            }
            di_list.push_back(*reinterpret_cast<Pylon::CDeviceInfo*>(w));
        }
        $1 = &di_list;
    }
    else
    {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
    }
}



%include <pylon/TlFactory.h>;

// now that the local typemaps are no longer needed, clear them.

%typemap(in) Pylon::TlInfoList_t&;
%typemap(argout) Pylon::TlInfoList_t&;
%typemap(in) Pylon::DeviceInfoList_t&;
%typemap(argout) Pylon::DeviceInfoList_t&;
%typemap(argout) const Pylon::DeviceInfoList_t&;
%typemap(typecheck) const Pylon::DeviceInfoList_t&;
%typemap(in) const Pylon::DeviceInfoList_t&;
