%rename(GenericOutputObserverResult) Pylon::DataProcessing::SGenericOutputObserverResult;
%rename(GenericOutputObserver) Pylon::DataProcessing::CGenericOutputObserver;
%ignore SGenericOutputObserverResult::Container;

%include <pylondataprocessing/GenericOutputObserver.h>;

%extend Pylon::DataProcessing::SGenericOutputObserverResult {
    CVariantContainer GetContainer()
    {
        return $self->Container;
    }
}

%pythoncode %{ GenericOutputObserverResult.Container = property(GenericOutputObserverResult.GetContainer) %}