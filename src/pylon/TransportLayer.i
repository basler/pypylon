%rename (TransportLayer) Pylon::ITransportLayer;
%nodefaultdtor Pylon::ITransportLayer;
%extend Pylon::ITransportLayer
{
    PROP_GET(TlInfo)
    PROP_GET(NodeMap)
}

%include <pylon/TransportLayer.h>;
