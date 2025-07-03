%rename(PylonImageBase) Pylon::CPylonImageBase;
%nodefaultctor Pylon::CPylonImageBase;
%nodefaultdtor Pylon::CPylonImageBase;

// Suppress abstract class warnings
%ignore Pylon::CPylonImageBase::CPylonImageBase;
%ignore Pylon::CPylonImageBase::~CPylonImageBase;

%include <pylon/PylonImageBase.h>;
