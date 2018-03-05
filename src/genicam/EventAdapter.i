%rename (EventAdapter) GENAPI_NAMESPACE::CEventAdapter;
%include <GenApi/EventAdapter.h>;
%pythoncode %{
    CEventAdapter = EventAdapter
%}