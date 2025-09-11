%feature("director") Pylon::DataProcessing::CSmartResultEventHandlerT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT< Pylon::CGrabResultPtr > >;

%include <pylondataprocessing/SmartResultEventHandler.h>;

%template(SmartResultEventHandler) Pylon::DataProcessing::CSmartResultEventHandlerT< Pylon::CInstantCamera, Pylon::DataProcessing::SSmartInstantCameraResultT< Pylon::CGrabResultPtr > >;
