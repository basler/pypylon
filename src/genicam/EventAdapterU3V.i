%rename (EventAdapterU3V) GENAPI_NAMESPACE::CEventAdapterU3V;
%ignore U3V_COMMAND_HEADER;
%ignore U3V_EVENT_DATA;
%ignore U3V_EVENT_MESSAGE;

//TODO fix for Linux
#define _MSC_VER
%include <GenApi/EventAdapterU3V.h>;
#undef _MSC_VER

%pythoncode %{
    CEventAdapterU3V = EventAdapterU3V
%}
