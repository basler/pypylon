%rename (InstantCameraParams_Params) Basler_InstantCameraParams::CInstantCameraParams_Params;
#define GenApi GENAPI_NAMESPACE
%ignore Basler_InstantCameraParams::CInstantCameraParams_Params::CInstantCameraParams_Params(void);
%ignore Basler_InstantCameraParams::CInstantCameraParams_Params::~CInstantCameraParams_Params(void);
%ignore Basler_InstantCameraParams::CInstantCameraParams_Params::_Initialize(GenApi::INodeMap*);
%ignore Basler_InstantCameraParams::CInstantCameraParams_Params::_GetVendorName(void);
%ignore Basler_InstantCameraParams::CInstantCameraParams_Params::_GetModelName(void);

%define GENICAM_PROP(name)
    %rename(_##name) name;

    %pythoncode %{
        def _Get_## name(self):
           return self._ ## name
        def _Set_ ## name(self, value):
           self._ ## name.SetValue(value)
        name = property(_Get_ ## name, _Set_ ## name )
    %}

%enddef
%extend Basler_InstantCameraParams::CInstantCameraParams_Params {
    GENICAM_PROP(MaxNumBuffer);
    GENICAM_PROP(MaxNumQueuedBuffer);
    GENICAM_PROP(MaxNumGrabResults);
    GENICAM_PROP(ChunkNodeMapsEnable);
    GENICAM_PROP(StaticChunkNodeMapPoolSize);
    GENICAM_PROP(GrabCameraEvents);
    GENICAM_PROP(MonitorModeActive);
    GENICAM_PROP(InternalGrabEngineThreadPriorityOverride);
    GENICAM_PROP(InternalGrabEngineThreadPriority);
    GENICAM_PROP(GrabLoopThreadUseTimeout);
    GENICAM_PROP(GrabLoopThreadTimeout);
    GENICAM_PROP(GrabLoopThreadPriorityOverride);
    GENICAM_PROP(GrabLoopThreadPriority);
    GENICAM_PROP(NumQueuedBuffers);
    GENICAM_PROP(NumReadyBuffers);
    GENICAM_PROP(NumEmptyBuffers);
    GENICAM_PROP(OutputQueueSize);
}
%include <pylon/_InstantCameraParams.h>;

%pythoncode %{
    CInstantCameraParams_Params = InstantCameraParams_Params
%}