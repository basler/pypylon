%ignore SetVariantContainer;
%ignore SetInitialUpdate;
%ignore SetGrabResult;
%ignore Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>::Container;

%include <pylondataprocessing/SmartResult.h>

%template(SmartInstantCameraResult) Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr>;

// This converts the data type CVariantContainer to a python dictionary by applying a %typemap from pylondataprocessing.i
%extend Pylon::DataProcessing::SSmartInstantCameraResultT<Pylon::CGrabResultPtr> {
    CVariantContainer GetContainer()
    {
        return $self->Container;
    }
}

// This provides the added GetContainer as a property.
%pythoncode %{ SmartInstantCameraResult.Container = property(SmartInstantCameraResult.GetContainer) %}