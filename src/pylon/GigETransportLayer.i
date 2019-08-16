%rename (GigETransportLayer) Pylon::IGigETransportLayer;
namespace Pylon
{
    typedef interfaceinfo_vector InterfaceInfoList_t;
}
%extend Pylon::IGigETransportLayer {
    public:
}
%include <pylon/gige/GigETransportLayer.h>;

%pythoncode %{
    IGigETransportLayer = GigETransportLayer
%}
