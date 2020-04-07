%nodefaultdtor GENAPI_NAMESPACE::INodeMap;
%nodefaultctor GENAPI_NAMESPACE::INodeMap;
namespace GENAPI_NAMESPACE {
    class IDeviceInfo;
}
%extend GENAPI_NAMESPACE::INodeMap {
    PROP_GET(DeviceName)
    //! gets the interface of the DeviceInfo
    IDeviceInfo *GetDeviceInfo()
    {
        IDeviceInfo *p_di;
        p_di = dynamic_cast<IDeviceInfo*>($self);
        if (NULL == p_di)
            throw LOGICAL_ERROR_EXCEPTION( "Nodemap has no deviceinfo" );
        return p_di;
    };

    PROP_GET(DeviceInfo)
%pythoncode %{
    def __getattr__(self, attribute):
        if attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            return self.GetNode(attribute)

    def __setattr__(self, attribute, val):
        if attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
        else:
            self.GetNode(attribute).SetValue(val)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        nodes = []
        try:
            nodes = self.GetNodeMap().GetNodes()
            features = filter(lambda n: n.GetNode().IsFeature(), nodes)
            l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        try:
            chunks = filter(lambda n: "ChunkData" in (f.Name for f in n.GetParents()), nodes)
            l.extend(x.GetNode().GetName() for x in chunks)
        except:
            pass
        return sorted(set(l))
%}
}
%include <GenApi/INodeMap.h>;
