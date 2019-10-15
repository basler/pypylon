%rename (InstantCameraParams_Params) Basler_InstantCameraParams::CInstantCameraParams_Params;
%ignore CInstantCameraParams_ParamsData;

%extend Basler_InstantCameraParams::CInstantCameraParams_Params
{
    GENICAM_EX_PROP(MaxNumBuffer,               GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(MaxNumQueuedBuffer,         GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(MaxNumGrabResults,          GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(ChunkNodeMapsEnable,        GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(StaticChunkNodeMapPoolSize, GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(GrabCameraEvents,           GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(MonitorModeActive,          GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(GrabLoopThreadUseTimeout,   GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(GrabLoopThreadTimeout,      GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(NumQueuedBuffers,           GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(NumReadyBuffers,            GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(NumEmptyBuffers,            GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(OutputQueueSize,            GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(InternalGrabEngineThreadPriorityOverride,   GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(InternalGrabEngineThreadPriority,           GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(GrabLoopThreadPriorityOverride,             GENAPI_NAMESPACE::IBoolean);
    GENICAM_EX_PROP(GrabLoopThreadPriority,                     GENAPI_NAMESPACE::IInteger);
}

%include <pylon/_InstantCameraParams.h>;
