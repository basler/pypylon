%rename (InstantCamera) Pylon::CInstantCamera;

%ignore IInstantCameraExtensions;
%ignore GetExtensionInterface;
%ignore CGrabResultDataFactory;
%ignore CreateDeviceSpecificGrabResultData;
%ignore CreateGrabResultData;
%ignore CInstantCameraParams_Params;
%ignore Basler_InstantCameraParams;

namespace Basler_InstantCameraParams
{
   class CInstantCameraParams_Params
   {
   };
}
namespace Pylon
{
   using namespace Basler_InstantCameraParams;
}

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

%pythoncode %{
    FirstFound = True
    Unambiguous = False
    BufferHandlingMode_Pool = "Pool"
    BufferHandlingMode_Stream = "Stream"
%}

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

    @staticmethod
    def _device_info_from_dict(d):
        di = DeviceInfo()
        di.update(d)
        return di

    def __getattr__(self, attribute):
        if attribute in ( "thisown","this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)
        else:
            return _LookupParameter(self.GetInstantCameraNodeMap(), self.GetNodeMap() if self.IsPylonDeviceAttached() else None, attribute)

    def __setattr__(self, attribute, val):
        if attribute in ( "thisown","this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
        else:
            type_attr = getattr(type(self), attribute, None)
            if isinstance(type_attr, property):
                type_attr.fset(self, val)
            else:
                warnings.warn(f"Setting a feature value by direct assignment is deprecated. Use <nodemap>.{attribute}.Value = {val}", DeprecationWarning, stacklevel=2)
                _LookupParameter(self.GetInstantCameraNodeMap(), self.GetNodeMap() if self.IsPylonDeviceAttached() else None, attribute).SetValue(val)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        try:
            nodes = self.GetInstantCameraNodeMap().GetNodes()
            features = filter(lambda n: n.GetNode().IsFeature(), nodes)
            l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        try:
            if self.IsPylonDeviceAttached():
                nodes = self.GetNodeMap().GetNodes()
                features = filter(lambda n: n.GetNode().IsFeature(), nodes)
                l.extend(x.GetNode().GetName() for x in features)
        except:
            pass
        return sorted(set(l))

    def __enter__(self):
        if self.IsPylonDeviceAttached():
            self.Open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.DestroyDevice() #automatically closes the camera and releases the device
        # unregister all configurations to avoid lifetime issues with event handlers that may be registered by the user.
        self.RegisterConfiguration(None, _pylon.RegistrationMode_ReplaceAll, _pylon.Cleanup_None)
        self.RegisterImageEventHandler(None, _pylon.RegistrationMode_ReplaceAll, _pylon.Cleanup_None)
        self.RegisterCameraEventHandler(None, "Dummy", 0, _pylon.RegistrationMode_ReplaceAll, _pylon.Cleanup_None)
        return False
%}
}

%pythonprepend Pylon::CInstantCamera::CInstantCamera %{
    # InstantCamera(firstFound: bool)
    if len(args) == 1 and isinstance(args[0], bool):
        _pylon.InstantCamera_swiginit(self, _pylon.new_InstantCamera())
        tlf = TlFactory.GetInstance()
        if args[0] == FirstFound:
            self.Attach(tlf.CreateFirstDevice())
        else:
            self.Attach(tlf.CreateDevice(DeviceInfo()))
        return
    # InstantCamera(di: DeviceInfo | dict, firstFound: bool)
    if len(args) == 2 and isinstance(args[1], bool):
        di_arg = args[0]
        first_found = args[1]
        if isinstance(di_arg, dict):
            di_arg = InstantCamera._device_info_from_dict(di_arg)
        _pylon.InstantCamera_swiginit(self, _pylon.new_InstantCamera())
        tlf = TlFactory.GetInstance()
        if first_found == FirstFound:
            self.Attach(tlf.CreateFirstDevice(di_arg))
        else:
            self.Attach(tlf.CreateDevice(di_arg))
        return
%}

%pythonprepend Pylon::CInstantCamera::Attach %{
    # Attach(firstFound: bool)
    if len(args) == 1 and isinstance(args[0], bool):
        tlf = TlFactory.GetInstance()
        if args[0] == FirstFound:
            _pylon.InstantCamera_Attach(self, tlf.CreateFirstDevice())
        else:
            _pylon.InstantCamera_Attach(self, tlf.CreateDevice(DeviceInfo()))
        return
    # Attach(di: DeviceInfo | dict, firstFound: bool)
    if len(args) == 2 and isinstance(args[1], bool):
        di_arg = args[0]
        first_found = args[1]
        if isinstance(di_arg, dict):
            di_arg = InstantCamera._device_info_from_dict(di_arg)
        tlf = TlFactory.GetInstance()
        if first_found == FirstFound:
            _pylon.InstantCamera_Attach(self, tlf.CreateFirstDevice(di_arg))
        else:
            _pylon.InstantCamera_Attach(self, tlf.CreateDevice(di_arg))
        return
%}

%pythonprepend Pylon::CInstantCamera::RegisterConfiguration %{
    if cleanupProcedure == Cleanup_Delete:
        if pConfigurator:
            pConfigurator.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterImageEventHandler %{
    if cleanupProcedure == Cleanup_Delete:
        if pImageEventHandler:
            pImageEventHandler.__disown__()
    elif cleanupProcedure == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::RegisterCameraEventHandler %{
    assert(len(args) > 4)
    if args[4] == Cleanup_Delete:
        if args[0]:
            args[0].__disown__()
    elif args[4] == Cleanup_None:
        # should we increment the pyhon refcount here??
        pass
%}
%pythonprepend Pylon::CInstantCamera::SetBufferFactory %{
    pFactory = args[0] if len(args) > 0 else None
    cleanupProcedure = args[1] if len(args) > 1 else Cleanup_None
    if len(args) == 1:
        args = (pFactory, Cleanup_None)
    if pFactory is not None and cleanupProcedure == Cleanup_Delete and hasattr(pFactory, "__disown__"):
        pFactory.__disown__()
%}
%pythonappend Pylon::CInstantCamera::SetBufferFactory %{
    pFactory = args[0] if len(args) > 0 else None
    cleanupProcedure = args[1] if len(args) > 1 else Cleanup_None
    if pFactory is None or cleanupProcedure == Cleanup_Delete:
        self.__dict__.pop("_buffer_factory_ref", None)
    elif cleanupProcedure == Cleanup_None:
        # Keep the factory alive as long as it is attached to this camera.
        self.__dict__["_buffer_factory_ref"] = pFactory
%}

%include <pylon/ECleanup.h>;
%include <pylon/ERegistrationMode.h>;
%include <pylon/ETimeoutHandling.h>;

// Per-method typemaps for nodemap getters – each wraps the returned
// GenApi::INodeMap& in an NodeMapWrapper carrying the correct ENodeMapType.
// These must appear before %include <pylon/InstantCamera.h> so SWIG uses them
// instead of the generic INodeMap& typemap defined in pylon.i.

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_Camera),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetTLNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_DeviceTransportLayer),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetStreamGrabberNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_StreamGrabber),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetEventGrabberNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_EventGrabber),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CInstantCamera::GetInstantCameraNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_InstantCamera),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/InstantCamera.h>;

