%rename (ImageEventHandler) Pylon::CImageEventHandler;
%feature("director") Pylon::CImageEventHandler;

%ignore Pylon::CImageEventHandler::DebugGetEventHandlerRegistrationCount;
%clear Pylon::CGrabResultPtr& grabResult;
%include <pylon/ImageEventHandler.h>

// =========================================
// = GrabResult smart ptr output

%typemap(in,numinputs=0) Pylon::CGrabResultPtr& grabResult {
  $1 = new CGrabResultPtr();
}

%typemap(argout) Pylon::CGrabResultPtr& grabResult{
  Py_DECREF($result);
  $result = SWIG_NewPointerObj(SWIG_as_voidptr($1), SWIGTYPE_p_Pylon__CGrabResultPtr, SWIG_POINTER_OWN );
  $1 = 0; // Now owned by $result, make sure it is not freed later on success
}

%typemap(freearg) Pylon::CGrabResultPtr& grabResult {
  delete $1;
}
