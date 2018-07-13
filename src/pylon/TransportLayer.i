%rename (TransportLayer) Pylon::ITransportLayer;
namespace Pylon
{
    typedef interfaceinfo_vector InterfaceInfoList_t;
}
%extend Pylon::ITransportLayer {
    public:
    PROP_GET(TlInfo)
    PROP_GET(NodeMap)
}
%include <pylon/TransportLayer.h>;

%pythoncode %{
    ITransportLayer = TransportLayer
%}
