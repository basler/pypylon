%rename (InstantCamera) Pylon::CInstantCamera;

%ignore IInstantCameraExtensions;
%ignore GetExtensionInterface;
%ignore CGrabResultDataFactory;
%ignore CreateDeviceSpecificGrabResultData;
%ignore CreateGrabResultData;

#define AutoLock GENAPI_NAMESPACE::AutoLock
#define CLock GENAPI_NAMESPACE::CLock

%rename(ConfigurationEventHandler) Pylon::CConfigurationEventHandler;
%rename(ImageEventHandler) Pylon::CImageEventHandler;
%rename(CameraEventHandler) Pylon::CCameraEventHandler;
%rename(StartGrabbingMax) StartGrabbing( size_t maxImages, EGrabStrategy strategy = GrabStrategy_OneByOne, EGrabLoop grabLoopType = GrabLoop_ProvidedByUser);

namespace Pylon {
     class CConfigurationEventHandler;
     class CImageEventHandler;
     class CCameraEventHandler;
};


%ignore CanWaitForFrameTriggerReady;

%extend Pylon::CInstantCamera {
    PROP_GET(QueuedBufferCount)
    PROP_GETSET(CameraContext)
    PROP_GET(DeviceInfo)
    PROP_GET(NodeMap)
    PROP_GET(TLNodeMap)
    PROP_GET(StreamGrabberNodeMap)
    PROP_GET(EventGrabberNodeMap)
    PROP_GET(InstantCameraNodeMap)
%pythoncode %{
    StreamGrabber = property(lambda self: self.GetStreamGrabberNodeMap() if self.IsOpen() else None)
    EventGrabber = property(lambda self: self.GetEventGrabberNodeMap() if self.IsOpen() else None)
    TransportLayer = property(lambda self: self.GetTLNodeMap())

    def __getattr__(self, attribute):
        if hasattr(InstantCameraParams_Params, attribute) or attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            return self.GetNodeMap().GetNode(attribute)

    def __setattr__(self, attribute, val):
        if hasattr(InstantCameraParams_Params, attribute) or attribute in ( "thisown","this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
        else:
            self.GetNodeMap().GetNode(attribute).SetValue(val)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        try:
            nodes = self.GetNodeMap().GetNodes()
            features = filter(lambda n: n.GetNode().IsFeature(), nodes)
            l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        return sorted(set(l))
%}
}

%pythonprepend Pylon::CInstantCamera::RegisterConfiguration %{
    if cleanupProcedure == Cleanup_Delete:
        pConfigurator.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterImageEventHandler %{
    if cleanupProcedure == Cleanup_Delete:
        pImageEventHandler.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterCameraEventHandler %{
    assert(len(args) > 4)
    if args[4] == Cleanup_Delete:
        args[0].__disown__()
    elif args[4] == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}

%include <pylon/InstantCamera.h>;
