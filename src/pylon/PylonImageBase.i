
%rename(PylonImageBase) Pylon::CPylonImageBase;
%nodefaultctor Pylon::CPylonImageBase;
%nodefaultdtor Pylon::CPylonImageBase;

#ifndef PYLON_WIN_BUILD
%ignore Pylon::CPylonImageBase::Save;
%ignore Pylon::CPylonImageBase::Load;
%ignore Pylon::CPylonImageBase::CanSaveWithoutConversion;
#endif

%include <pylon/PylonImageBase.h>;
