%rename (EventPort) GENAPI_NAMESPACE::CEventPort;
%include <GenApi/EventPort.h>;
%pythoncode %{
    CEventPort = EventPort
%}
