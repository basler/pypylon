%rename (EventAdapterGeneric) GENAPI_NAMESPACE::CEventAdapterGeneric;
%include <GenApi/EventAdapterGeneric.h>;
%pythoncode %{
    CEventAdapterGeneric = EventAdapterGeneric
%}