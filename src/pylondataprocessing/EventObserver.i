%rename(Recipe) Pylon::DataProcessing::CRecipe;
%rename(EventData) Pylon::DataProcessing::CEventData;
%rename(EventObserver) Pylon::DataProcessing::IEventObserver;
%feature("director") Pylon::DataProcessing::IEventObserver;

%rename(EventType) Pylon::DataProcessing::CEventData::eventType;
%rename(Description) Pylon::DataProcessing::CEventData::description;
%rename(EventClass) Pylon::DataProcessing::CEventData::eventClass;
%rename(EventSourceName) Pylon::DataProcessing::CEventData::eventSourceName;

// previous data processing version < v2.0.0 (pylon 7.4), in current versions 'events' is named 'pEvents'
%typemap(directorin) (const Pylon::DataProcessing::CEventData* events, size_t numEvents) (PyObject* listObject)
%{
  listObject = PyList_New(numEvents);
  for (size_t i = 0; i < numEvents; ++i)
  {
    PyObject* eventObject = SWIG_NewPointerObj(SWIG_as_voidptr(new Pylon::DataProcessing::CEventData(events[i])), SWIGTYPE_p_Pylon__DataProcessing__CEventData, SWIG_POINTER_OWN);
    PyList_SetItem(listObject, i, eventObject);
  }
  $input = listObject;
%}

%typemap(directorin) (const Pylon::DataProcessing::CEventData* pEvents, size_t numEvents) (PyObject* listObject)
%{
  listObject = PyList_New(numEvents);
  for (size_t i = 0; i < numEvents; ++i)
  {
    PyObject* eventObject = SWIG_NewPointerObj(SWIG_as_voidptr(new Pylon::DataProcessing::CEventData(pEvents[i])), SWIGTYPE_p_Pylon__DataProcessing__CEventData, SWIG_POINTER_OWN);
    PyList_SetItem(listObject, i, eventObject);
  }
  $input = listObject;
%}

%extend Pylon::DataProcessing::CEventData {
    %pythoncode %{
        def __str__(self):
            result = "EventType: {0}; Description = {1};  EventClass = {2}; EventSourceName = {3}".format(self.EventType, self.Description, self.EventClass, self.EventSourceName)
            return result
    %}
}

%include <pylondataprocessing/IEventObserver.h>;