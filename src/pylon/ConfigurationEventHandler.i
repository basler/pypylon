%rename(InstantCamera) Pylon::CInstantCamera;
%rename(ConfigurationEventHandler) Pylon::CConfigurationEventHandler;
%feature("director") Pylon::CConfigurationEventHandler;

%ignore Pylon::CConfigurationEventHandler::DebugGetEventHandlerRegistrationCount;
%include <pylon/ConfigurationEventHandler.h>
