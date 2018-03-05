
%ignore CSimpleMutex;
%ignore ITransportLayer;
%ignore IDeviceFactory;
%ignore TlMap;
%ignore ImplicitTlRefs;

%nodefaultctor Pylon::CTlFactory;
%rename(TlFactory) Pylon::CTlFactory;
%include <pylon/TlFactory.h>;
