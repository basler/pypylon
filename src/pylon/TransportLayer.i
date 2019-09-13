%rename (TransportLayer) Pylon::ITransportLayer;
%nodefaultdtor Pylon::ITransportLayer;
%extend Pylon::ITransportLayer
{
    PROP_GET(TlInfo)
    PROP_GET(NodeMap)

%pythoncode %{
    class InterfaceContext:
        def __init__(self, tl, iface_info):
            self.tl = tl
            self.iface_info = iface_info
            self.iface = None

        def __enter__(self):
            self.iface = self.tl.CreateInterface(self.iface_info)
            return self.iface

        def __exit__(self, type, value, traceback):
            self.tl.DestroyInterface(self.iface)

    def Interface(self, iface_info):
        return self.InterfaceContext(self, iface_info)

    class InterfaceNodeMapContext:
        def __init__(self, tl, iface_info):
            self.tl = tl
            self.iface_info = iface_info
            self.iface = None

        def __enter__(self):
            self.iface = self.tl.CreateInterface(self.iface_info)
            self.iface.Open()
            return self.iface.GetNodeMap()

        def __exit__(self, type, value, traceback):
            self.iface.Close()
            self.tl.DestroyInterface(self.iface)

    def InterfaceNodeMap(self, iface_info):
        return self.InterfaceNodeMapContext(self, iface_info)

%}

}

////////////////////////////////////////////////////////////////////////////////
//
// InterfaceInfoList output
//

%typemap(in, numinputs=0) (Pylon::InterfaceInfoList_t& list, bool addToList)
{
    $1 = new Pylon::InterfaceInfoList_t();
    $2 = false;
}

%typemap(argout,fragment="t_output_helper") Pylon::InterfaceInfoList_t &
{
    Py_DECREF($result);
    PyObject *tpl = PyTuple_New($1->size());
    for (unsigned int i = 0; i < $1->size(); i++)
    {
        CInterfaceInfo *ii = new CInterfaceInfo((*$1)[i]);
        PyObject *item = SWIG_NewPointerObj(
            SWIG_as_voidptr(ii),
            SWIGTYPE_p_Pylon__CInterfaceInfo,
            SWIG_POINTER_OWN
            );
        PyTuple_SetItem(tpl, i, item);
    }
    $result = tpl;
    delete $1;
}

%include <pylon/TransportLayer.h>;

%typemap(in) (Pylon::InterfaceInfoList_t& list, bool addToList);
%typemap(argout) Pylon::InterfaceInfoList_t&;
