%rename (EventAdapterGEV) GENAPI_NAMESPACE::CEventAdapterGEV;
%ignore GVCP_REQUEST_HEADER;
%ignore GVCP_EVENT_ITEM_BASIC;
%ignore GVCP_EVENT_ITEM;
%ignore GVCP_EVENT_REQUEST;
%ignore GVCP_EVENTDATA_REQUEST;
%ignore GVCP_EVENT_ITEM_EXTENDED_ID;
%ignore GVCP_EVENT_REQUEST_EXTENDED_ID;
%ignore GVCP_EVENTDATA_REQUEST_EXTENDED_ID;
%ignore GVCP_MESSAGE_TAGS;
%ignore DeliverEventMessage;

//TODO fix for Linux
#define _MSC_VER
%include <GenApi/EventAdapterGEV.h>;
#undef _MSC_VER

%pythoncode %{
    CEventAdapterGEV = EventAdapterGEV
%}