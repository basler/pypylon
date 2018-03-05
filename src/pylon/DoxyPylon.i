
// File: index.xml

// File: class_pylon_1_1_avi_writer_fatal_exception.xml


%feature("docstring") Pylon::AviWriterFatalException "

Exception thrown if a fatal error occurs (e.g. access violations, ...) when
accessing an AVI video file.  

C++ includes: AviWriter.h
";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "

";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "
";

%feature("docstring") Pylon::AviWriterFatalException::AviWriterFatalException "
";

// File: class_pylon_1_1_base___callback1_body.xml


%feature("docstring") Pylon::Base_Callback1Body "
";

%feature("docstring") Pylon::Base_Callback1Body::~Base_Callback1Body "

destructor  
";

%feature("docstring") Pylon::Base_Callback1Body::clone "

deep copy  
";

// File: class_pylon_1_1_c_acquire_continuous_configuration.xml


%feature("docstring") Pylon::CAcquireContinuousConfiguration "

Changes the configuration of the camera to free-running continuous acquisition.  

The `CAcquireContinuousConfiguration` is the default configuration of the
Instant Camera class. The CAcquireContinuousConfiguration is automatically
registered when an Instant Camera object is created.  

This instant camera configuration is provided as header-only file. The code can
be copied and modified for creating own configuration classes.  

C++ includes: AcquireContinuousConfiguration.h
";

%feature("docstring") Pylon::CAcquireContinuousConfiguration::ApplyConfiguration "

Apply acquire continuous configuration.  
";

%feature("docstring") Pylon::CAcquireContinuousConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

// File: class_pylon_1_1_c_acquire_single_frame_configuration.xml


%feature("docstring") Pylon::CAcquireSingleFrameConfiguration "

An instant camera configuration for single frame acquisition, Use together with
CInstantCamera::GrabOne() only.  

The CAcquireSingleFrameConfiguration is provided as header-only file. The code
can be copied and modified for creating own configuration classes.  

note: Grabbing single images using Software Trigger
    (CSoftwareTriggerConfiguration) is recommended if you want to maximize frame
    rate. This is because the overhead per grabbed image is reduced compared to
    Single Frame Acquisition. The grabbing can be started using
    CInstantCamera::StartGrabbing(). Images are grabbed using the
    CInstantCamera::WaitForFrameTriggerReady(),
    CInstantCamera::ExecuteSoftwareTrigger() and
    CInstantCamera::RetrieveResult() methods instead of using
    CInstantCamera::GrabOne(). The grab can be stopped using
    CInstantCamera::StopGrabbing() when done.  

C++ includes: AcquireSingleFrameConfiguration.h
";

%feature("docstring") Pylon::CAcquireSingleFrameConfiguration::ApplyConfiguration "

Apply acquire single frame configuration.  
";

%feature("docstring") Pylon::CAcquireSingleFrameConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

// File: class_pylon_1_1_callback1.xml


%feature("docstring") Pylon::Callback1 "
";

%feature("docstring") Pylon::Callback1::~Callback1 "

destructor, destroying body  
";

%feature("docstring") Pylon::Callback1::Callback1 "

constructor, taking lifetime control of body  
";

%feature("docstring") Pylon::Callback1::Callback1 "

copy constructor doing deep copy  
";

// File: class_pylon_1_1_c_avi_writer.xml


%feature("docstring") Pylon::CAviWriter "

Supports writing AVI files.  

C++ includes: AviWriter.h
";

%feature("docstring") Pylon::CAviWriter::Open "

Opens an AVI file for writing.  

If a file with the same `filename` already exists, it will be overwritten.  

Parameters
----------
* `filename` :  
    Name and path of the image.  
* `framesPerSecondPlayback` :  
    The frame rate of the AVI file when shown in a media player.  
* `pixelType` :  
    The pixel type of the image in the AVI file.  
* `width` :  
    The number of pixels in a row.  
* `height` :  
    The number of rows of the image.  
* `orientation` :  
    The vertical orientation of the image data in the AVI file.  
* `pCompressionOptions` :  
    Compression can be enabled by passing compression options. See
    SAviCompressionOptions.  

pre:  

    *   The AVI file is closed.  
    *   The pixelType is either PixelType_Mono8, PixelType_BGR8packed or
        PixelType_BGRA8packed  
    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

Throws an exception if the AVI file cannot be opened. Throws an exception if the
preconditions are not met.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::IsOpen "

Returns the open state of the AVI file.  

Returns
-------
Returns true if open.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::~CAviWriter "

Destroys the AVI writer object.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::GetCountOfAddedImages "

Provides access to the number of images that have been added to the AVI file.  

Returns
-------
Returns the number of images that have been added to the AVI file. Returns 0 if
no AVI file has been written yet.  Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the AVI file without
prior conversion when Add() is called.  

Parameters
----------
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image data in the AVI file.  

Returns
-------
Returns true if the image is added to the AVI stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::CanAddWithoutConversion "

Can be used to check whether the given image is added to the AVI file without
prior conversion when Add() is called.  

Parameters
----------
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the image is added to the AVI stream without prior conversion
when Add() is called. Returns false if the image is automatically converted when
Add() is called. Returns false if the image cannot be added at all. See the
preconditions of Add() for more information.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::CAviWriter "

Creates an AVI writer object.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::GetImageDataBytesWritten "

Provides access to the number of image data bytes written to the AVI file.  

This value is updated with each call to AviWriter::Add().  

Depending on the used image format and codec, about 5 KB of header information
and padding bytes are written to the AVI file. Furthermore, 24 additional bytes
are needed per image for chunk header and index entry data.  

Returns
-------
Returns the number of image data bytes that have been written to the AVI file.
Returns 0 if no AVI File has been written yet. This size does not include the
sizes of the AVI file header and AVI file index.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CAviWriter::Add "

Adds the image to the AVI file. Converts the image to the correct format if
required.  

The image is automatically converted to the format passed when opening the file
if needed. The image is also converted if the stride of the passed image is not
aligned to 4 byte. The image is also converted if the orientation of the passed
image does mot match the value passed when opening the AVI file.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert other images with a CPylonBitmapImage object as target.
The CPylonBitmapImage object can then be added to the AVI file.  

Parameters
----------
* `image` :  
    The image to add, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `keyFrameSelection` :  
    Can be used to control key frame selection for compressed images if needed.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The pixel type of the image to add is a supported input format of the
        Pylon::CImageFormatConverter.  
    *   The width and height of the `image` match the values passed when opening
        the AVI file.  
    *   The total size of the AVI file must not exceed 2 GB. See
        CAviWriter::GetImageDataBytesWritten().  

Throws an exception if the image cannot be added.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::Add "

Adds the image to the AVI file. Converts the image to the correct format if
required.  

See Add( const Image&) for more details.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the image.  
* `bufferSize` :  
    The size of the buffer in byte.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each line.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  
* `keyFrameSelection` :  
    Can be used to control key frame selection for compressed images if needed.  

pre:  

    *   The file is open.  
    *   The image added is valid.  
    *   The pixel type of the image to add is a supported input format of the
        Pylon::CImageFormatConverter.  
    *   The width and height of the `image` match the values passed when opening
        the AVI file.  
    *   The total size of the AVI file must not exceed 2 GB. See
        CAviWriter::GetImageDataBytesWritten().  

Throws an exception if the image cannot be added.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CAviWriter::Close "

Closes the AVI file.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

// File: class_pylon_1_1_c_chunk_parser_1_1_c_buffer.xml

// File: class_pylon_1_1_c_camera_event_handler.xml


%feature("docstring") Pylon::CCameraEventHandler "

The camera event handler base class.  

C++ includes: CameraEventHandler.h
";

%feature("docstring") Pylon::CCameraEventHandler::DebugGetEventHandlerRegistrationCount "
";

%feature("docstring") Pylon::CCameraEventHandler::~CCameraEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CCameraEventHandler::CCameraEventHandler "

Create.  
";

%feature("docstring") Pylon::CCameraEventHandler::CCameraEventHandler "

Copy.  
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEventHandlerDeregistered "

This method is called when the camera event handler has been deregistered.  

The camera event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events.  

C++ exceptions from this call will be caught and ignored.  This method is called
inside the lock of the camera event handler registry.  
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEvent "

This method is called when a camera event has been received.  

Only very short processing tasks should be performed by this method. Otherwise,
the event notification will block the processing of images.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `userProvidedId` :  
    The ID passed when registering for the event. It can be used to distinguish
    between different events.  
* `pNode` :  
    The node identified by node name when registering.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  This method is called outside the lock of the camera object, outside
the lock of the node map, and inside the lock of the camera event handler
registry.  
";

%feature("docstring") Pylon::CCameraEventHandler::DestroyCameraEventHandler "

Destroys the camera event handler.  

C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CCameraEventHandler::OnCameraEventHandlerRegistered "

This method is called when the camera event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events.  

Exceptions from this call will propagate through.  This method is called inside
the lock of the camera event handler registry.  
";

// File: class_pylon_1_1_c_camera_pixel_type_mapper_t.xml


%feature("docstring") Pylon::CCameraPixelTypeMapperT "

A camera specific pixeltypemapper (maps device specific pixelformats contained
in the generated camera classes to pylon pixeltypes by their name).  

Use this mapper to convert a PixelTypeEnums or ChunkPixelFormatEnums enum values
to a Pylon_PixelType used for PixelTypeConverter creation. When passing the
symbolic name of the pixeltype you can use the static version
GetPylonPixelTypeByName. This function will do the lookup everytime you call it.
The non-static member function GetPylonPixelTypeFromPixelFormatEnum uses caching
to speed up subsequent calls.  

The template parameter EnumT is the enumeration type from the camera class
(typically Basler_GigECamera::PixelFormatEnums for GigE cameras or
Basler_IIDC1394CameraParams::PixelFormatEnums for 1394 cameras)  

C++ includes: PixelTypeMapper.h
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::SetPixelFormatEnumNode "

Lazy initialization of the object.  

Parameters
----------
* `pEnumT` :  
    Pointer to the enumeration node containing the PixelFormats.  

Call this function initialize the mapper when using the default c'tor.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::IsValid "

Checks the objects validity.  

Returns
-------
Returns true if the object is initialized properly.  

Essentially this function checks whether you've called SetPixelFormatEnumNode.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::~CCameraPixelTypeMapperT "
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeFromPixelFormatEnum "

Converts a enumeration node value to a Pylon::EPixelType enum.  

Parameters
----------
* `pixelFormatEnumValue` :  
    enumeration value to convert. You obtain this value by calling
    GENAPI_NAMESPACE::IEnumerationT::GetValue.  

Returns
-------
Returns the Pylon::EPixelType for a given pixelformat enum value defined in the
enum node passed in c'tor  

Converts a enumeration node value to a Pylon::EPixelType enum. You must have
initialized the mapper before you can call this function.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `pszSymbolicName` :  
    pointer to the symbolic name. Note: Symbolic names are case sensitive. You
    can obtain the symbolic name by calling
    GENAPI_NAMESPACE::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup soley by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `symbolicName` :  
    The symbolic name. Note: Symbolic names are case sensitive. You can obtain
    the symbolic name by calling GENAPI_NAMESPACE::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup solely by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::GetNameByPixelType "

Static function that returns a string representation of the given EPixelType.  

Parameters
----------
* `pixelType` :  
    The pixel type to return the name for.  
* `sfncVer` :  
    SFNC Version to use when doing the mapping. Some names have been changed in
    SFNC 2.0  

Returns
-------
Returns the pointer to a null terminated string representing the symbolic name
of the pixel type.  

Passing Pylon::PixelType_Mono16 will return \"Mono16\" will be returned. If the
pixel type is not known an empty string is returned.  

note: The returned name cannot be used to parameterize the pixel format of a
    camera device, because the camera's pixel format name can be different. The
    camera's pixel format name depends on the used standard feature naming
    convention (SFNC).  

(PixelType, SFNCVersion sfncVer = SFNCVersion_pre2_0)  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::CCameraPixelTypeMapperT "

Create an empty mapper. Before calling any non-static function.  
";

%feature("docstring") Pylon::CCameraPixelTypeMapperT::CCameraPixelTypeMapperT "

create a mapper by using the enum node passed.  
";

// File: class_pylon_1_1_c_chunk_parser.xml


%feature("docstring") Pylon::CChunkParser "

Low Level API: Base class for chunk parsers returned by camera objects.  

Part implementation of chunk parser of common functionality.  

C++ includes: ChunkParser.h
";

%feature("docstring") Pylon::CChunkParser::GetChunkDataNodeMap "
";

%feature("docstring") Pylon::CChunkParser::AttachBuffer "
";

%feature("docstring") Pylon::CChunkParser::UpdateBuffer "
";

%feature("docstring") Pylon::CChunkParser::Destroy "
";

%feature("docstring") Pylon::CChunkParser::DetachBuffer "
";

// File: class_pylon_1_1_c_configuration_event_handler.xml


%feature("docstring") Pylon::CConfigurationEventHandler "

The configuration event handler base class.  

C++ includes: ConfigurationEventHandler.h
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDestroy "

This method is called before the attached Pylon Device is destroyed.  

Camera DestroyDevice must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::CConfigurationEventHandler "

Create.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::CConfigurationEventHandler "

Copy.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnClosed "

This method is called after the attached Pylon Device has been closed.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnConfigurationDeregistered "

This method is called when the configuration event handler has been
deregistered.  

The configuration event handler is automatically deregistered when the Instant
Camera object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored.  This method is called
inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabError "

This method is called when an exception has been triggered during grabbing.  

An exception has been triggered by a grab thread. The grab will be stopped after
this event call.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `errorMessage` :  
    The message of the exception that signaled an error during grabbing.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnCameraDeviceRemoved "

This method is called when a camera device removal from the PC has been
detected.  

The Pylon Device attached to the Instant Camera is not operable after this
event. After it is made sure that no access to the Pylon Device or any of its
node maps is made anymore the Pylon Device should be destroyed using
InstantCamera::DeviceDestroy(). The access to the Pylon Device can be protected
using the lock provided by GetLock(), e.g. when accessing parameters.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object from an additional
thread.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStopped "

This method is called after a grab session has been stopped.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStart "

This method is called before a grab session is started.  

Camera StartGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnConfigurationRegistered "

This method is called when the configuration event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through.  This method is called inside
the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::DebugGetEventHandlerRegistrationCount "
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDetach "

This method is called before the attached Pylon Device is detached from the
Instant Camera object.  

The camera's Detach() method must not be called from here or from subsequent
calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStarted "

This method is called after a grab session has been started.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnAttach "

This method is called before a Pylon Device (Pylon::IPylonDevice) is attached by
calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnOpen "

This method is called before the attached Pylon Device is opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDestroyed "

This method is called after the attached Pylon Device has been destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnGrabStop "

This method is called before a grab session is stopped.  

Camera StopGrabbing must not be called from here or from subsequent calls to
avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnDetached "

This method is called after the attached Pylon Device has been detached from the
Instant Camera object.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::DestroyConfiguration "

Destroys the configuration event handler.  

C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::~CConfigurationEventHandler "

Destruct.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnAttached "

This method is called after a Pylon Device (Pylon::IPylonDevice) has been
attached by calling the Instant Camera object's Attach() method.  

This method can not be used for detecting that a camera device has been attached
to the PC. The camera's Attach() method must not be called from here or from
subsequent calls to avoid infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

%feature("docstring") Pylon::CConfigurationEventHandler::OnClose "

This method is called before the attached Pylon Device is closed.  

Camera Close must not be called from here or from subsequent calls to avoid
infinite recursion.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored. All event handlers are
notified.  

This method is called inside the lock of the camera object.  
";

// File: class_pylon_1_1_c_device_info.xml


%feature("docstring") Pylon::CDeviceInfo "

Holds information about an enumerated device.  

The device enumeration process creates a list of CDeviceInfo objects
(Pylon::DeviceInfoList_t). Each CDeviceInfo objects stores information about a
device. The information is retrieved during the device enumeration process
(ITransportLayer::EnumerateDevices resp. CTlFactory::EnumerateDevices)  

C++ includes: DeviceInfo.h
";

%feature("docstring") Pylon::CDeviceInfo::SetXMLSource "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::SetModelName "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceFactory "

Retrieves the identifier for the transport layer able to create this device.
This property is identified by Key::DeviceFactoryKey.  
";

%feature("docstring") Pylon::CDeviceInfo::IsModelNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetSerialNumber "

Retrieves the serial number if it supported by the underlying implementation
This property is identified by Key::SerialNumberKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetUserDefinedName "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceFactory "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsSerialNumberAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetXMLSource "

Retrieves the location where the XML file was loaded from. This property is
identified by Key::XMLSourceKey. You must use the DeviceInfo of an opened
IPylonDevice to retrieve this property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceFactoryAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::GetModelName "

Retrieves the model name of the device. This property is identified by
Key::ModelNameKey.  
";

%feature("docstring") Pylon::CDeviceInfo::GetUserDefinedName "

Retrieves the user-defined name if present. This property is identified by
Key::UserDefinedNameKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceVersion "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::IsDeviceVersionAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::IsUserDefinedNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::SetVendorName "

Sets the vendor name of the device. This property is identified by
Key::VendorNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::IsXMLSourceAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CDeviceInfo::SetDeviceClass "

Sets the device class device, e.g. Basler1394. This property is identified by
Key::DeviceClassKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::CDeviceInfo "
";

%feature("docstring") Pylon::CDeviceInfo::CDeviceInfo "
";

%feature("docstring") Pylon::CDeviceInfo::SetFriendlyName "

Sets the display friendly name of the device. This property is identified by
Key::FriendlyNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::SetFullName "

Sets the full name identifying the device. This property is identified by
Key::FullNameKey. This method overrides a method of a base class returning a
reference to CDeviceInfo  
";

%feature("docstring") Pylon::CDeviceInfo::SetSerialNumber "

Sets the above property.  
";

%feature("docstring") Pylon::CDeviceInfo::GetDeviceVersion "

Retrieves the version string of the device. This property is identified by
Key::DeviceVersionKey.  
";

%feature("docstring") Pylon::CDeviceInfo::SetPropertyValue "

Modifies a property value This method overrides a method of a base class
returning a reference to CDeviceInfo  
";

// File: class_pylon_1_1_c_event_grabber_proxy_t.xml


%feature("docstring") Pylon::CEventGrabberProxyT "

Low Level API: The event grabber class with parameter access methods.  

This is the base class for pylon event grabber providing access to configuration
parameters.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: EventGrabberProxy.h
";

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Implementation of the IEventGrabber interface 
*/

/*
See Pylon::IEventGrabber for more details.  

*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CEventGrabberProxyT::GetEventGrabber "

Returns the pylon event grabber interface pointer.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::CEventGrabberProxyT "

Creates a CEventGrabberProxyT object that is not attached to a pylon stream
grabber. Use the Attach() method to attach the pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::CEventGrabberProxyT "

Creates a CEventGrabberProxyT object and attaches it to a pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::GetNodeMap "

Returns the set of camera parameters.  

Returns the GenApi node map used for accessing parameters provided by the
transport layer.  

Returns the associated stream grabber parameters.  

Returns
-------
Pointer to the GenApi node map holding the parameters  

If no parameters are available, NULL is returned.  

Returns
-------
NULL, if the transport layer doesn't provide parameters, a pointer to the
parameter node map otherwise.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::~CEventGrabberProxyT "

Destructor.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::GetWaitObject "

Returns the result event object.  

This object is associated with the result queue. The event is signaled when
queue is non-empty  
";

%feature("docstring") Pylon::CEventGrabberProxyT::IsOpen "

Retrieve whether the stream grabber is open.  

";

%feature("docstring") Pylon::CEventGrabberProxyT::Close "

Closes the stream grabber.  

Flushes the result queue and stops the thread.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::Attach "

Attach a pylon event grabber.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::IsAttached "

Checks if a pylon stream grabber is attached.  
";

%feature("docstring") Pylon::CEventGrabberProxyT::RetrieveEvent "


";

%feature("docstring") Pylon::CEventGrabberProxyT::Open "

Opens the stream grabber.  

";

// File: class_pylon_1_1_c_feature_persistence.xml


%feature("docstring") Pylon::CFeaturePersistence "

Utility class for saving and restoring camera features to and from a file or
string.  

note: When saving features, the behavior of cameras supporting sequencers
    depends on the current setting of the \"SequenceEnable\" (some GigE models)
    or \"SequencerConfigurationMode\" (USB only) features respectively.  

Only if the sequencer is in configuration mode, are the sequence sets exported.
Otherwise, the camera features are exported without sequence sets.  

C++ includes: FeaturePersistence.h
";

%feature("docstring") Pylon::CFeaturePersistence::SaveToString "

Saves the node map to the string. Sequence sets of a camera are automatically
saved, if SequenceEnable or SequencerConfigurationMode is enabled.  

Parameters
----------
* `Features` :  
    String containing the node map values  
* `pNodeMap` :  
    Pointer to the node map  

Throws an exception if saving fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::LoadFromString "

Loads the features from the string to the node map.  

Parameters
----------
* `Features` :  
    String containing the node map values.  
* `pNodeMap` :  
    Pointer to the node map.  
* `validate` :  
    If validate==true, all node values will be validated. In case of an error, a
    GenICam::RuntimeException will be thrown.  

Throws an exception if loading fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::Save "

Saves the node map to the file.  

Sequence sets of a camera are automatically saved if SequenceEnable or
SequencerConfigurationMode is enabled.  

Parameters
----------
* `FileName` :  
    Name of the file that contains the node map values  
* `pNodeMap` :  
    Pointer to the node map  

Throws an exception if saving fails.  
";

%feature("docstring") Pylon::CFeaturePersistence::Load "

Loads the features from the file to the node map.  

Parameters
----------
* `FileName` :  
    Name of the file that contains the node map values.  
* `pNodeMap` :  
    Pointer to the node map  
* `validate` :  
    If validate==true, all node values will be validated. In case of an error, a
    GenICam::RuntimeException will be thrown  

Throws an exception if loading fails.  
";

// File: class_pylon_1_1_c_grab_result_data.xml


%feature("docstring") Pylon::CGrabResultData "

Makes the data for one grabbed buffer available.  

C++ includes: GrabResultData.h
";

%feature("docstring") Pylon::CGrabResultData::~CGrabResultData "
";

%feature("docstring") Pylon::CGrabResultData::GetTimeStamp "

Get the camera specific tick count (camera device specific).  

This describes when the image exposure was started. Cameras that do not support
this feature return zero. If supported, this can be used to determine which
image AOIs were acquired simultaneously.  
";

%feature("docstring") Pylon::CGrabResultData::IsChunkDataAvailable "

Returns true if chunk data is available.  

This is the case if the chunk mode is enabled for the camera device. The
parameter CInstantCamera::ChunkNodeMapsEnable of the used Instant Camera object
is set to true (default setting). Chunk data node maps are supported by the
Transport Layer of the camera device.  
";

%feature("docstring") Pylon::CGrabResultData::GetErrorCode "

This method returns the error code if GrabSucceeded() returns false due to an
error.  
";

%feature("docstring") Pylon::CGrabResultData::GetImageNumber "

Get the number of the image. This number is incremented when an image is
retrieved using CInstantCamera::RetrieveResult().  

Always returns a number larger than 0. The counting starts with 1 and is reset
with every call to CInstantCamera::StartGrabbing().  
";

%feature("docstring") Pylon::CGrabResultData::GetNumberOfSkippedImages "

Get the number of skipped images before this image.  

This value can be larger than 0 if EGrabStrategy_LatestImageOnly grab strategy
or GrabStrategy_LatestImages grab strategy is used. Always returns a number
larger than or equal 0. This number does not include the number of images lost
in case of a buffer underrun in the driver.  
";

%feature("docstring") Pylon::CGrabResultData::GetPayloadType "

Get the current payload type.  
";

%feature("docstring") Pylon::CGrabResultData::GetCameraContext "

Get the context value assigned to the camera object. The context is attached to
the result when it is retrieved.  
";

%feature("docstring") Pylon::CGrabResultData::GetErrorDescription "

This method returns a description of the error if GrabSucceeded() returns false
due to an error.  
";

%feature("docstring") Pylon::CGrabResultData::HasCRC "

Checks if buffer has a CRC attached. This needs not be activated for the device.
See the PayloadCRC16 chunk.  
";

%feature("docstring") Pylon::CGrabResultData::GetID "

Get the ID of the grabbed image.  

Always returns a number larger than 0. The counting starts with 1 and is never
reset during the lifetime of the Instant Camera object.  
";

%feature("docstring") Pylon::CGrabResultData::GetPixelType "

Get the current pixel type.  
";

%feature("docstring") Pylon::CGrabResultData::GetStride "

Get the stride in byte.  
";

%feature("docstring") Pylon::CGrabResultData::CheckCRC "

Checks CRC sum of buffer, returns true if CRC sum is OK.  
";

%feature("docstring") Pylon::CGrabResultData::GetImageSize "

Get the size of the image in byte.  
";

%feature("docstring") Pylon::CGrabResultData::PYLON_DEPRECATED "

Deprecated: GetBlockID() should be used instead. Get the index of the grabbed
frame (camera device specific).  
";

%feature("docstring") Pylon::CGrabResultData::GrabSucceeded "

Returns true if an image has been grabbed successfully and false in the case of
an error.  
";

%feature("docstring") Pylon::CGrabResultData::GetChunkDataNodeMap "

Get the reference to the chunk data node map connected to the result.  

An empty node map is returned when the device does not support this feature or
when chunks are disabled.  
";

%feature("docstring") Pylon::CGrabResultData::GetBufferContext "

Get the context value assigned to the buffer. The context is set when
CInstamtCamera is using a custom buffer factory.  
";

%feature("docstring") Pylon::CGrabResultData::GetOffsetY "

Get the current starting row.  
";

%feature("docstring") Pylon::CGrabResultData::GetPaddingX "

Get the number of extra data at the end of each row in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetGrabResultDataImpl "
";

%feature("docstring") Pylon::CGrabResultData::GetOffsetX "

Get the current starting column.  
";

%feature("docstring") Pylon::CGrabResultData::GetWidth "

Get the current number of columns.  
";

%feature("docstring") Pylon::CGrabResultData::GetBlockID "

Get the block ID of the grabbed frame (camera device specific).  

par: IEEE 1394 Camera Devices
    The value of Block ID is always UINT64_MAX.  

par: GigE Camera Devices
    The sequence number starts with 1 and wraps at 65535. The value 0 has a
    special meaning and indicates that this feature is not supported by the
    camera.  

par: USB Camera Devices
    The sequence number starts with 0 and uses the full 64 Bit range.  

attention: A block ID with the value UINT64_MAX indicates that the block ID is
    invalid and must not be used.  
";

%feature("docstring") Pylon::CGrabResultData::GetPaddingY "

Get the number of extra data at the end of the image data in bytes.  
";

%feature("docstring") Pylon::CGrabResultData::GetHeight "

Get the current number of rows expressed as number of pixels.  
";

%feature("docstring") Pylon::CGrabResultData::GetBuffer "

Get the pointer to the buffer.  

If the chunk data feature is activated for the device, chunk data is appended to
the image data. When writing past the image section while performing image
processing, the chunk data will be corrupted.  
";

%feature("docstring") Pylon::CGrabResultData::GetPayloadSize "

Get the current payload size in bytes.  
";

// File: class_pylon_1_1_c_grab_result_image_t.xml


%feature("docstring") Pylon::CGrabResultImageT "

Low Level API: Adapts grab result to Pylon::IImage.  

C++ includes: ResultImage.h
";

%feature("docstring") Pylon::CGrabResultImageT::CGrabResultImageT "

Creates a grab result image object.  

Parameters
----------
* `grabResult` :  
    A grab result.  
* `isUnique` :  
    User provided info whether the buffer is referenced only by this grab
    result.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultImageT::GetPixelType "
";

%feature("docstring") Pylon::CGrabResultImageT::GetBuffer "
";

%feature("docstring") Pylon::CGrabResultImageT::GetBuffer "
";

%feature("docstring") Pylon::CGrabResultImageT::GetHeight "
";

%feature("docstring") Pylon::CGrabResultImageT::~CGrabResultImageT "

Destroys a grab result image object.  
";

%feature("docstring") Pylon::CGrabResultImageT::GetImageSize "
";

%feature("docstring") Pylon::CGrabResultImageT::GetWidth "
";

%feature("docstring") Pylon::CGrabResultImageT::IsUnique "
";

%feature("docstring") Pylon::CGrabResultImageT::GetStride "
";

%feature("docstring") Pylon::CGrabResultImageT::GetOrientation "
";

%feature("docstring") Pylon::CGrabResultImageT::GetPaddingX "
";

%feature("docstring") Pylon::CGrabResultImageT::IsValid "
";

// File: class_pylon_1_1_c_grab_result_ptr.xml


%feature("docstring") Pylon::CGrabResultPtr "

A smart pointer holding a reference to grab result data.  

This class is used for distributing the grab result data of a camera. It
controls the reuse and lifetime of the referenced buffer. When all smart
pointers referencing a buffer go out of scope the referenced buffer is reused or
destroyed. The data and the held buffer are still valid after the camera object
it originated from has been destroyed.  

attention: The grabbing will stop with an input queue underrun, when the grab
    results are never released, e.g. when put into a container.  

The CGrabResultPtr class provides a cast operator that allows passing the grab
result directly to functions or methods that take an const IImage& as parameter,
e.g. image saving functions or image format converter methods.  

attention: The returned reference to IImage is only valid as long the
    CGrabResultPtr object it came from is not destroyed.  

Instances of CGrabResultPtr referencing the same grab result can be used from
any thread context.  

C++ includes: GrabResultPtr.h
";

%feature("docstring") Pylon::CGrabResultPtr::CGrabResultPtr "

Creates a smart pointer.  

post: No grab result is referenced.  
";

%feature("docstring") Pylon::CGrabResultPtr::CGrabResultPtr "

Creates a copy of a smart pointer.  

Parameters
----------
* `rhs` :  
    Another smart pointer, source of the result data to reference.  

The data itself is not copied.  

post:  

    *   Another reference to the grab result of the source is held if it
        references a grab result.  
    *   No grab result is referenced if the source does not reference a grab
        result.  

Still valid after error.  
";

%feature("docstring") Pylon::CGrabResultPtr::Release "

The currently referenced data is released.  

post: The currently referenced data is released.  

Still valid after error.  
";

%feature("docstring") Pylon::CGrabResultPtr::IsValid "

Check whether data is referenced.  

Returns
-------
True if data is referenced.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultPtr::IsUnique "

Indicates that the held grab result data and buffer is only referenced by this
grab result.  

Returns
-------
Returns true if the held grab result data and buffer is only referenced by this
grab result. Returns false if the grab result is invalid.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultPtr::~CGrabResultPtr "

Destroys the smart pointer.  

post: The currently referenced data is released.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CGrabResultPtr::PylonPrivate::CGrabResultDataConverter "

Internal use only.  
";

// File: class_pylon_1_1_c_image_event_handler.xml


%feature("docstring") Pylon::CImageEventHandler "

The image event handler base class.  

C++ includes: ImageEventHandler.h
";

%feature("docstring") Pylon::CImageEventHandler::OnImageEventHandlerDeregistered "

This method is called when the image event handler has been deregistered.  

The image event handler is automatically deregistered when the Instant Camera
object is destroyed.  

Parameters
----------
* `camera` :  
    The source of the call.  

C++ exceptions from this call will be caught and ignored.  This method is called
inside the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::CImageEventHandler "

Create.  
";

%feature("docstring") Pylon::CImageEventHandler::CImageEventHandler "

Copy.  
";

%feature("docstring") Pylon::CImageEventHandler::DebugGetEventHandlerRegistrationCount "
";

%feature("docstring") Pylon::CImageEventHandler::DestroyImageEventHandler "

Destroys the image event handler.  

C++ exceptions from this call will be caught and ignored.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImageEventHandlerRegistered "

This method is called when the image event handler has been registered.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through.  This method is called inside
the lock of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImageGrabbed "

This method is called when an image has been grabbed.  

The grab result smart pointer passed does always reference a grab result data
object. The status of the grab needs to be checked before accessing the grab
result data. See CGrabResultData::GrabSucceeded(),
CGrabResultData::GetErrorCode() and CGrabResultData::GetErrorDescription() for
more information.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `grabResult` :  
    The grab result data.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called outside the lock of the camera object but inside the lock
of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::OnImagesSkipped "

This method is called when images have been skipped using the
GrabStrategy_LatestImageOnly strategy or the GrabStrategy_LatestImages strategy.  

Parameters
----------
* `camera` :  
    The source of the call.  
* `countOfSkippedImages` :  
    The number of images skipped. This `countOfSkippedImages` does not include
    the number of images lost in the case of a buffer under run in the driver.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called outside the lock of the camera object but inside the lock
of the image event handler registry.  
";

%feature("docstring") Pylon::CImageEventHandler::~CImageEventHandler "

Destruct.  
";

// File: class_pylon_1_1_c_image_format_converter.xml


%feature("docstring") Pylon::CImageFormatConverter "

Creates new images by converting a source image to another format.  

Supported input image formats defined by the pixel type:  

*   PixelType_Mono1packed  
*   PixelType_Mono2packed  
*   PixelType_Mono4packed  
*   PixelType_Mono8  
*   PixelType_Mono10  
*   PixelType_Mono10packed  
*   PixelType_Mono10p  
*   PixelType_Mono12  
*   PixelType_Mono12packed  
*   PixelType_Mono12p  
*   PixelType_Mono16  

*   PixelType_BayerGR8  
*   PixelType_BayerRG8  
*   PixelType_BayerGB8  
*   PixelType_BayerBG8  
*   PixelType_BayerGR10  
*   PixelType_BayerRG10  
*   PixelType_BayerGB10  
*   PixelType_BayerBG10  
*   PixelType_BayerGR12  
*   PixelType_BayerRG12  
*   PixelType_BayerGB12  
*   PixelType_BayerBG12  
*   PixelType_BayerGR12Packed  
*   PixelType_BayerRG12Packed  
*   PixelType_BayerGB12Packed  
*   PixelType_BayerBG12Packed  
*   PixelType_BayerGR10p  
*   PixelType_BayerRG10p  
*   PixelType_BayerGB10p  
*   PixelType_BayerBG10p  
*   PixelType_BayerGR12p  
*   PixelType_BayerRG12p  
*   PixelType_BayerGB12p  
*   PixelType_BayerBG12p  
*   PixelType_BayerGR16  
*   PixelType_BayerRG16  
*   PixelType_BayerGB16  
*   PixelType_BayerBG16  

*   PixelType_RGB8packed  
*   PixelType_BGR8packed  
*   PixelType_RGBA8packed  
*   PixelType_BGRA8packed  
*   PixelType_RGB10packed  
*   PixelType_BGR10packed  
*   PixelType_RGB12packed  
*   PixelType_BGR12packed  
*   PixelType_RGB12V1packed  
*   PixelType_RGB16packed  
*   PixelType_RGB8planar  
*   PixelType_RGB16planar  

*   PixelType_YUV422packed  
*   PixelType_YUV422_YUYV_Packed  

Supported output image formats defined by the pixel type:  

*   PixelType_BGRA8packed - This pixel type can be used in Windows bitmaps. See
    Pylon::SBGRA8Pixel.  
*   PixelType_BGR8packed - This pixel type can be used in Windows bitmaps. See
    Pylon::SBGR8Pixel.  
*   PixelType_RGB8packed - See Pylon::SRGB8Pixel.  
*   PixelType_RGB16packed - See Pylon::SRGB16Pixel.  
*   PixelType_RGB8planar  
*   PixelType_RGB16planar  
*   PixelType_Mono8  
*   PixelType_Mono16  

All input image formats can be converted to all output image formats.  

RGB, BGR and Bayer image formats are converted to monochrome formats by using
the following formula:  


YUV formats are converted to 16 bit bit depth in an intermediate conversion
step. This is why the output is always aligned at the most significant bit when
converting to 16 bit color output formats like PixelType_RGB16packed.  

par: Limitations:
    The last column of a YUV input image with odd width cannot be converted. The
    last column and the last row of a Bayer input image cannot be converted.  

The default treatment of rows and columns that cannot be converted due to their
location on edges, can be controlled using the
CImageFormatConverter::InconvertibleEdgeHandling parameter. See also the
Convert() method description.  

The CImageFormatConverter class is not thread-safe.  

C++ includes: ImageFormatConverter.h
";

%feature("docstring") Pylon::CImageFormatConverter::~CImageFormatConverter "

Destroys the image format converter.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsSupportedOutputFormat "

Returns true if the image format defined by the given pixel type is a supported
output format.  

Parameters
----------
* `destinationPixelType` :  
    The pixel type of the destination image.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::ImageHasDestinationFormat "

Checks to see if a conversion is required or if the source image already has the
desired format.  

Parameters
----------
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the source image already has the desired format.  

A conversion may even be required image format does not change e.g. if the gamma
conversion method is selected and the format describes a monochrome image.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::ImageHasDestinationFormat "

Checks to see if a conversion is required or if the source image already has the
desired format.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the image in the image buffer. The default value
    is usually ImageOrientation_TopDown.  

Returns
-------
Returns true if the source image already has the desired format. This is done
according to the current converter settings.  

A conversion may even be required image format does not change e.g. if the gamma
conversion method is selected and the format describes a monochrome image.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::CImageFormatConverter "

Creates an image format converter.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsSupportedInputFormat "

Returns true if the image format defined by the given pixel type is a supported
input format.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetNodeMap "

Provides access to the node map of the format converter.  

Returns
-------
Reference to the node map of the format converter.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::Initialize "

Optionally initializes the image format converter before conversion.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

*   Depending on parameter settings and the input format, data structures
    required for conversion are created, e.g. lookup tables.  
*   Initialization is done automatically when calling Convert() if needed. This
    may add a delay when converting the first image.  

pre:  

    *   The converter parameters are set up.  
    *   The `pixelTypeSource` must be supported by the converter.  

Lookup tables are created when using monochrome images as input and when the
gamma conversion method is selected or when the shift conversion method is
selected and the value of AdditionalLeftShift is not zero. The converter can be
reinitialized with other settings if required.  

Throws an exception if the passed pixel type does not represent a valid input
format. The converter object is still valid after error and can be initialized
again.  
";

%feature("docstring") Pylon::CImageFormatConverter::Uninitialize "

Destroys data structures required for conversion.  

This function can be called to free resources held by the format converter.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetBufferSizeForConversion "

Computes the size of the destination image buffer in byte.  

Parameters
----------
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
The size of the destination image when converting the given source image using
current converter settings.  

Throws an exception if the destination image size for the passed input cannot be
computed. The converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::GetBufferSizeForConversion "

Computes the size of the destination image buffer in byte.  

Parameters
----------
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  

Returns
-------
The size of the destination image when converting the source image using current
converter settings.  

pre:  

    *   The `sourceWidth` value must be >= 0 and < _I32_MAX.  
    *   The `sourceHeight` value must be >= 0 and < _I32_MAX.  

Throws an exception if the destination image size for the passed input cannot be
computed. The converter object is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::IsInitialized "

Returns information about the converter being initialized.  

Parameters
----------
* `sourcePixelType` :  
    The pixel type of the source image.  

The result depends on the converter settings.  

Returns
-------
True if initialized.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The IReusableImage::Reset() method of the destination image is called to set the
destination format. The image is converted to the destination image according to
the current converter settings. The padding area of a row in the destination
image is set to zero.  

The OutputPaddingX setting is ignored for images that do not support user
defined padding, e.g. CPylonBitmapImage. See also
IReusableImage::IsAdditionalPaddingSupported().  

Parameters
----------
* `destinationImage` :  
    The destination image, e.g. a CPylonImage or CPylonBitmapImage object. When
    passing a CPylonBitmapImage object the target format must be supported by
    the CPylonBitmapImage class.  
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre:  

    *   The source and destination images must be different images.  
    *   The source image must be valid.  
    *   The format of the source image must be supported by the converter.  
    *   The destination image must support the destination format.  
    *   The destination image must be able to provide a large enough buffer to
        hold the image.  

Throws an exception if the passed parameters are not valid. The converter object
is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The IReusableImage::Reset() method of the destination image is called to set the
destination format. The image is converted to the destination image according to
the current converter settings. The padding area of a row in the destination
image is set to zero.  

The OutputPaddingX setting is ignored for images that do not support user
defined padding, e.g. CPylonBitmapImage. See also
IReusableImage::IsAdditionalPaddingSupported().  

Parameters
----------
* `destinationImage` :  
    The destination image.  
* `pSourceBuffer` :  
    The pointer to the buffer of the source image.  
* `sourceBufferSizeBytes` :  
    The size of the buffer of the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the source image in the image buffer. The
    default value is usually ImageOrientation_TopDown.  

pre:  

    *   The pixel type must be valid.  
    *   The `sourceWidth` value must be >= 0 and < _I32_MAX.  
    *   The `sourceHeight` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The format of the input image represented by the given parameter must be
        supported by the converter.  
    *   The destination image must support the destination format.  
    *   The destination image must be able to provide a large enough buffer to
        hold the image.  
    *   The source image buffer and the destination image buffer must not be
        identical.  

Throws an exception if the passed parameters are not valid. The converter object
is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The image is converted to the destination image according to the current
converter settings. The padding area of a row in the destination image is set to
zero.  

Parameters
----------
* `pDestinationBuffer` :  
    The pointer to the buffer of the destination image.  
* `destinationBufferSizeBytes` :  
    The size of the buffer of the destination image.  
* `sourceImage` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre:  

    *   The format of the source image must be supported by the converter.  
    *   The destination image buffer must be large enough to hold the
        destination image.  
    *   The source image buffer and the destination image buffer must not be
        identical.  

Throws an exception if the passed parameters are not valid. The converter object
is still valid after error.  
";

%feature("docstring") Pylon::CImageFormatConverter::Convert "

Creates a new image by converting an image to a different format.  

The image is converted to the destination image according to the current
converter settings. The padding area of a row in the destination image is set to
zero.  

Parameters
----------
* `pDestinationBuffer` :  
    The pointer to the buffer of the destination image.  
* `destinationBufferSizeBytes` :  
    The size of the buffer of the destination image.  
* `pSourceBuffer` :  
    The pointer to the buffer of the source image.  
* `sourceBufferSizeBytes` :  
    The size of the buffer of the source image.  
* `sourcePixelType` :  
    The pixel type of the source image.  
* `sourceWidth` :  
    The number of pixels in a row in the source image.  
* `sourceHeight` :  
    The number of rows in the source image.  
* `sourcePaddingX` :  
    The number of extra data bytes at the end of each row. The default value is
    usually 0.  
* `sourceOrientation` :  
    The vertical orientation of the source image in the image buffer. The
    default value is usually ImageOrientation_TopDown.  

pre:  

    *   The parameters regarding the source buffer must describe a valid image.  
    *   The format of the input image represented by the given parameter must be
        supported by the converter.  
    *   If the destination image buffer must be large enough to hold the
        destination image.  
    *   The the source buffer can not be equal the destination buffer.  

Throws an exception if the passed parameters are not valid. The converter object
is still valid after error.  
";

// File: class_basler___image_format_converter_params_1_1_c_image_format_converter_params___params.xml


%feature("docstring") Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params "

Interface to image format converter parameters.  

C++ includes: _ImageFormatConverterParams.h
";

/*
 MonoConversion - Parameters for converting monochrome images. 
*/

/*
*/

/*
 MonoConversion - Parameters for converting monochrome images. 
*/

/*
 MonoConversion - Parameters for converting monochrome images. 
*/

/*
 Root - Image Format Converter parameters. 
*/

/*
 Root - Image Format Converter parameters. 
*/

/*
 Root - Image Format Converter parameters. 
*/

/*
 Root - Image Format Converter parameters. 
*/

// File: class_pylon_1_1_c_image_persistence.xml


%feature("docstring") Pylon::CImagePersistence "

Contains static functions supporting loading and saving of images.  

C++ includes: ImagePersistence.h
";

%feature("docstring") Pylon::CImagePersistence::Save "

Saves the image to disk. Converts the image to a format that can be saved if
required.  

If required, the image is automatically converted to a new image and then saved.
See CanSaveWithoutConversion() for more information. An image with a bit depth
higher than 8 bit is stored with 16 bit bit depth if supported by the image file
format. In this case the pixel data is MSB aligned.  

If more control over the conversion is required then the CImageFormatConverter
class can be used to convert the input image before saving it.  

Parameters
----------
* `imageFileFormat` :  
    The file format to save the image in.  
* `filename` :  
    Name and path of the image.  
* `pBuffer` :  
    The pointer to the buffer of the image.  
* `bufferSize` :  
    The size of the buffer in byte.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  
* `pOptions` :  
    Additional options.  

pre:  

    *   The pixel type of the image to save must be a supported input format of
        the Pylon::CImageFormatConverter.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

Throws an exception if saving the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::Save "

Saves the image to disk. Converts the image to a format that can be if required.  

If required, the image is automatically converted to a new image and then saved.
See CanSaveWithoutConversion() for more information. An image with a bit depth
higher than 8 bit is stored with 16 bit bit depth if supported by the image file
format. In this case the pixel data is MSB aligned.  

If more control over the conversion is required then the CImageFormatConverter
class can be used to convert the input image before saving it.  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `filename` :  
    Name and path of the image.  
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `pOptions` :  
    Additional options.  

pre: The pixel type of the image to save must be a supported input format of the
    Pylon::CImageFormatConverter.  

Throws an exception if saving the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::LoadFromMemory "

Loads an image from memory.  

The orientation of loaded images is always ImageOrientation_TopDown. Currently
BMP, JPEG & PNG images are supported.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `image` :  
    The target image object, e.g. a CPylonImage or CPylonBitmapImage object.
    When passing a CPylonBitmapImage object the loaded format must be supported
    by the CPylonBitmapImage class.  

Throws an exception if the image cannot be loaded. The image buffer content is
undefined when the loading of the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::Load "

Loads an image from disk.  

The orientation of loaded images is always ImageOrientation_TopDown.  

Parameters
----------
* `filename` :  
    Name and path of the image.  
* `image` :  
    The target image object, e.g. a CPylonImage or CPylonBitmapImage object.
    When passing a CPylonBitmapImage object the loaded format must be supported
    by the CPylonBitmapImage class.  

Throws an exception if the image cannot be loaded. The image buffer content is
undefined when the loading of the image fails.  
";

%feature("docstring") Pylon::CImagePersistence::CanSaveWithoutConversion "

Can be used to check whether the given image can be saved without prior
conversion.  

See the CImagePersistence::CanSaveWithoutConversion( EImageFileFormat, const
IImage&) method documentation for a list of supported pixel formats.  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `pixelType` :  
    The pixel type of the image to save.  
* `width` :  
    The number of pixels in a row of the image to save.  
* `height` :  
    The number of rows of the image to save.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

Returns
-------
Returns true if the image can be saved without prior conversion.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CImagePersistence::CanSaveWithoutConversion "

Can be used to check whether the image can be saved without prior conversion.  

Supported formats for TIFF:  

*   PixelType_Mono8  
*   PixelType_Mono16  
*   PixelType_RGB8packed  
*   PixelType_RGB16packed  

Supported formats for BMP, JPEG and PNG:  

*   PixelType_Mono8  
*   PixelType_BGR8packed  
*   PixelType_BGRA8packed  

Parameters
----------
* `imageFileFormat` :  
    The target file format for the image to save.  
* `image` :  
    The image to save, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

Returns
-------
Returns true if the image can be saved without prior conversion.  

Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_image_persistence_options.xml


%feature("docstring") Pylon::CImagePersistenceOptions "

Used to pass options to CImagePersistence methods.  

C++ includes: ImagePersistence.h
";

%feature("docstring") Pylon::CImagePersistenceOptions::SetQuality "

Set the image quality options. Valid quality values range from 0 to 100.  
";

%feature("docstring") Pylon::CImagePersistenceOptions::CImagePersistenceOptions "
";

%feature("docstring") Pylon::CImagePersistenceOptions::GetQuality "

Returns the set quality level.  
";

// File: class_pylon_1_1_c_info_base.xml


%feature("docstring") Pylon::CInfoBase "

Base implementation for PYLON info container.  

Info container allow a generic access to implemented properties. All Properties
and their values can be accessed without knowing them in advance. It is possible
to enumerate all properties available and corresponding values. Properties and
values are represented as String_t. The normal usage is to have enumerators that
create the info objects and clients that read only.  

If the type of the info object is known before client can use specific accessor
function to retrieve the property values  

C++ includes: Info.h
";

%feature("docstring") Pylon::CInfoBase::IsFullNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::GetPropertyNames "
";

%feature("docstring") Pylon::CInfoBase::IsUserProvided "
";

%feature("docstring") Pylon::CInfoBase::GetPropertyValue "
";

%feature("docstring") Pylon::CInfoBase::GetDeviceClass "

Retrieves the device class device, e.g. Basler1394. This property is identified
by Key::DeviceClassKey.  
";

%feature("docstring") Pylon::CInfoBase::GetFullName "

Retrieves the full name identifying the device. This property is identified by
Key::FullNameKey.  
";

%feature("docstring") Pylon::CInfoBase::SetFullName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::GetPropertyAvailable "
";

%feature("docstring") Pylon::CInfoBase::SetPropertyValue "
";

%feature("docstring") Pylon::CInfoBase::GetFriendlyName "

Retrieves the human readable name of the device. This property is identified by
Key::FriendlyNameKey.  
";

%feature("docstring") Pylon::CInfoBase::GetVendorName "

Retrieves the vendor name of the device. This property is identified by
Key::VendorNameKey.  
";

%feature("docstring") Pylon::CInfoBase::SetDeviceClass "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::IsDeviceClassAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::SetFriendlyName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::SetVendorName "

Sets the above property.  
";

%feature("docstring") Pylon::CInfoBase::GetPropertyNotAvailable "
";

%feature("docstring") Pylon::CInfoBase::IsVendorNameAvailable "

Returns true if the above property is available.  
";

%feature("docstring") Pylon::CInfoBase::IsSubset "
";

%feature("docstring") Pylon::CInfoBase::IsFriendlyNameAvailable "

Returns true if the above property is available.  
";

// File: class_pylon_1_1_c_instant_camera.xml


%feature("docstring") Pylon::CInstantCamera "

Provides convenient access to a camera device.  

*   Establishes a single access point for accessing camera functionality.  
*   The class can be used off the shelf without any parameters. The camera uses
    a default configuration for the camera device. This can be overridden.  
*   Handles Pylon device lifetime. This can be overridden.  
*   Handles opening and closing of a Pylon device automatically.  
*   Handles chunk data parsing automatically returning the chunk data in the
    grab result.  
*   Handles event grabbing automatically providing a convenient interface for
    event callbacks. This can be overridden.  
*   Handles physical camera device removal.  
*   Handles the creation, reuse, and destruction of buffers.  
*   The grabbing can be done in the context of the caller or by using an
    additional grab loop thread.  
*   The Instant Camera class is extensible using derivation or by registering
    event handler objects.  

C++ includes: InstantCamera.h
";

%feature("docstring") Pylon::CInstantCamera::Close "

Closes the attached Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If the Pylon device is already closed, nothing is done.  
*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   The configuration event OnClose is fired. Possible C++ exceptions from event
    calls are caught and ignored. All event handlers are notified.  
*   The Pylon device is closed.  
*   The configuration event OnClosed is fired if the Pylon device has been
    closed successfully. Possible C++ exceptions from event calls are caught and
    ignored. All event handlers are notified.  

post: The Pylon device is closed.  

Does not throw C++ exceptions. Possible C++ exceptions are caught and ignored.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RegisterCameraEventHandler "

Adds an camera event handler to the list of registered camera event handler
objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered camera
    event handlers is cleared.  
*   If the pointer `pCameraEventHandler` is not NULL, it is appended to the list
    of camera event handlers.  

Parameters
----------
* `pCameraEventHandler` :  
    The receiver of camera events.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  
* `userProvidedId` :  
    This ID is passed as a parameter in CCameraEventHandler::OnCameraEvent and
    can be used to distinguish between different events. It is recommended to
    create an own application specific enum and use it's values as IDs.  
* `mode` :  
    Indicates how to register the new cameraEventHandler.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  
* `availability` :  
    If availability equals CameraEventAvailability_Mandatory, the camera must
    support the data node specified by node name. If not, an exception is thrown
    when the Instant Camera is open, the Instant Camera is opened, or an open
    Pylon device is attached.  

Internally, a GenApi node call back is registered for the node identified by
`nodeName`. This callback triggers a call to the
`CCameraEventHandler::OnCameraEvent()` method. That's why a Camera Event Handler
can be registered for any node of the camera node map to get informed about
changes.  

post: The cameraEventHandler is registered and called on camera events.  

Throws an exception if the availability is set to
CameraEventAvailability_Mandatory and the node with the name `nodeName` is not
available in the camera node map (see GetNodeMap()). Throws an exception fail if
the node callback registration fails. The event handler is not registered when
an C++ exception is thrown.  

This method is synchronized using the camera event handler lock. If the camera
is open, the lock provided by GetLock() and the camera node map lock are also
used for synchronization.  
";

%feature("docstring") Pylon::CInstantCamera::Attach "

Attaches a Pylon device to the Instant Camera.  

Parameters
----------
* `pDevice` :  
    The Pylon device to attach.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the Pylon device is destroyed
    when the Instant Camera object is destroyed.  

*   If a Pylon device is currently attached, it is destroyed (DestroyDevice())
    or removed (DetachDevice()) depending on the previously set cleanup
    procedure value.  
*   If the pDevice parameter is NULL, nothing more is done.  
*   The OnAttach configuration event is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The new Pylon device is attached.  
*   If the passed Pylon device is open, callbacks for camera events are
    registered at the camera node map. (This may fail)  
*   If the passed Pylon device is open, a device removal call back is
    registered. (This may fail)  
*   If the passed Pylon device is open, access modifiers (see
    IPylonDevice::Open()) are overtaken as camera parameters.  
*   The OnAttached configuration event is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

post:  

    *   If the passed pointer to the Pylon device is NULL, the Instant Camera
        object is in the \"no device attached\" state.  
    *   If the passed pointer to the Pylon device is not NULL, the passed Pylon
        device is attached.  
    *   If the set cleanup procedure equals Cleanup_Delete, the Pylon device is
        destroyed when the Instant Camera object is destroyed or a new device is
        attached.  
    *   If the passed Pylon device is open and the registration of callbacks
        fails, the Instant Camera object is in the \"no device attached\" state.  
    *   The opened-by-user flag is set, preventing closing of the Pylon device
        on StopGrabbing() when the attached Pylon device is already open.  

May throw an exception if the passed Pylon device is open. Does not throw C++
exceptions if the passed Pylon device is closed or NULL.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DetachDevice "

Detaches an attached Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   The configuration event OnDetach is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The Pylon device is detached.  
*   The configuration event OnDetached is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

Returns
-------
The attached Pylon device or NULL if nothing has been attached before.  

post:  

    *   No Pylon device is attached.  
    *   The ownership of the Pylon device goes to the caller who is responsible
        for destroying the Pylon device.  

Does not throw C++ exceptions. Possible C++ exceptions are caught and ignored.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsPylonDeviceAttached "

Returns the Pylon device attached state of the Instant Camera object.  

Returns
-------
True if a Pylon device is attached.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterImageEventHandler "

Removes an image event handler from the list of registered image event handler
objects.  

If the image event handler is not found, nothing is done.  

Parameters
----------
* `imageEventHandler` :  
    The registered receiver of configuration events.  

Returns
-------
True if successful  

post:  

    *   The imageEventHandler is deregistered.  
    *   If the image event handler has been registered by passing a pointer and
        the cleanup procedure is Cleanup_Delete, the event handler is deleted.  

Does not throw C++ exceptions.  

This method is synchronized using the internal image event handler registry
lock.  
";

%feature("docstring") Pylon::CInstantCamera::GetExtensionInterface "
";

%feature("docstring") Pylon::CInstantCamera::IsGrabbing "

Returns state of grabbing.  

The camera object is grabbing after a successful call to StartGrabbing() until
StopGrabbing() is called.  

Returns
-------
Returns true if still grabbing.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::WaitForFrameTriggerReady "

Actively waits until the the camera is ready to accept a frame trigger.  

The implementation selects 'FrameTriggerWait' for the
'AcquisitionStatusSelector' and waits until the 'AcquisitionStatus' is true. If
the above mentioned nodes are not available and the 'SoftwareTrigger' node is
readable, the implementation waits for SoftwareTrigger.IsDone().  

The WaitForFrameTriggerReady method does not work for A600 Firewire cameras.  

Parameters
----------
* `timeoutMs` :  
    The timeout in ms for active waiting.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the camera can execute a frame trigger.  

pre: The 'AcquisitionStatusSelector' node is writable and the
    'AcquisitionStatus' node is readable or the 'SoftwareTrigger' node is
    readable. This depends on the used camera model.  

Accessing the camera registers may fail.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::HasOwnership "

Returns the ownership of the attached Pylon device.  

Returns
-------
True if a Pylon device is attached and the Instant Camera object has been given
the ownership by passing the cleanup procedure Cleanup_Delete when calling
Attach().  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RegisterImageEventHandler "

Adds an image event handler to the list of registered image event handler
objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered image
    event handlers is cleared.  
*   If pointer `pImageEventHandler` is not NULL, it is appended to the list of
    image event handlers.  

Parameters
----------
* `pImageEventHandler` :  
    The receiver of image events.  
* `mode` :  
    Indicates how to register the new imageEventHandler.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  

post: The imageEventHandler is registered and called on image related events.  

Does not throw C++ exceptions, except when memory allocation fails.  

This method is synchronized using the internal image event handler registry
lock.  
";

%feature("docstring") Pylon::CInstantCamera::SetCameraContext "

Sets a context that is attached to each grab result of the camera object on
RetrieveResult(). This is useful when handling multiple cameras. It has nothing
in common with the context passed to the stream grabber when queuing a buffer.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsCameraLink "

Returns true if a Camera Link Pylon device is attached to the Instant Camera
object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetGrabResultWaitObject "

Provides access to a wait object indicating available grab results.  

Returns
-------
A wait object indicating available grab results.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetGrabStopWaitObject "

Provides access to a wait object indicating that the grabbing has stopped.  

Returns
-------
A wait object indicating that the grabbing has stopped.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GrabOne "

Grabs one image.  

The following code shows a simplified version of what is done (happy path):  


GrabOne() can be used to together with the CAcquireSingleFrameConfiguration.  

note: Using GrabOne is more efficient if the Pylon device is already open,
    otherwise the Pylon device is opened and closed for each call.  

    Grabbing single images using Software Trigger
    (CSoftwareTriggerConfiguration) is recommended if you want to maximize frame
    rate. This is because the overhead per grabbed image is reduced compared to
    Single Frame Acquisition. The grabbing can be started using StartGrabbing().
    Images are grabbed using the WaitForFrameTriggerReady(),
    ExecuteSoftwareTrigger() and RetrieveResult() methods instead of using
    GrabOne. The grab can be stopped using StopGrabbing() when done.  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
Returns true if the call successfully retrieved a grab result and the grab
succeeded (CGrabResultData::GrabSucceeded()).  

pre: Must meet the preconditions of start grabbing.  

post: Meets the postconditions of stop grabbing.  

The Instant Camera object is still valid after error. See StartGrabbing(),
RetrieveResult(), and StopGrabbing() . In the case of exceptions after
StartGrabbing() the grabbing is stopped using StopGrabbing().  
";

%feature("docstring") Pylon::CInstantCamera::GetInstantCameraNodeMap "

Provides access to the node map of the Instant Camera object.  

The node map of the camera device is made available by the GetNodeMap() method.  

Returns
-------
Reference to the node map of the Instant Camera object.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetSfncVersion "

Returns the SFNC version read from the camera node map.  

The SFNC version is read from the camera node map using the integer nodes
DeviceSFNCVersionMajor, DeviceSFNCVersionMinor, and DeviceSFNCVersionSubMinor.  

Returns
-------
The SFNC version used by the camera device. The returned SFNC version is 0.0.0
(Pylon::Sfnc_VersionUndefined) if no SFNC version information is provided by the
camera device.  

pre: A Pylon device is attached.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetCameraContext "

Returns the context that is attached to each grab result of the camera object.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetDeviceInfo "

Provides access to the device info object of the attached Pylon device or an
empty one.  

Returns
-------
The info object of the attached Pylon device or an empty one.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetNodeMap "

Provides access to the node map of the camera device.  

The Pylon device must be opened before reading ore writing any parameters of the
camera device. This can be done using the Open() method of the Instant Camera
class.  

Returns
-------
Reference to the node map of the camera device.  

pre: A Pylon device is attached.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::RegisterConfiguration "

Adds a configurator to the list of registered configurator objects.  

*   If mode equals RegistrationMode_ReplaceAll, the list of registered
    configurators is cleared.  
*   If pointer `pConfigurator` is not NULL, it is appended to the list of
    configurators.  

Parameters
----------
* `pConfigurator` :  
    The receiver of configuration events.  
* `mode` :  
    Indicates how to register the new configurator.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the passed event handler is
    deleted when no longer needed.  

post: The configurator is registered and called on configuration events.  

Does not throw C++ exceptions, except when memory allocation fails.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsBcon "

Returns true if a BCON Pylon device is attached to the Instant Camera object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::Open "

Opens the attached Pylon device.  

*   Opened by user flag is set, preventing closing of the device on
    StopGrabbing().  
*   If the Pylon device is already open, nothing more is done.  
*   The OnOpen configuration event is fired. The notification of event handlers
    stops when an event call triggers an exception.  
*   The Pylon device is opened.  
*   A device removal call back is registered at the Pylon device.  
*   Callbacks for camera events are registered at the camera node map.  
*   The OnOpened configuration event is fired if the Pylon device has been
    opened successfully. The notification of event handlers stops when an event
    call triggers an exception.  

pre: A Pylon device is attached.  

post:  

    *   The Pylon device is open.  
    *   Opened by user flag is set, preventing closing of the Pylon device on
        StopGrabbing().  

The Instant Camera object is still valid after error. The Pylon device open may
throw. Configuration event calls may throw. Callback registrations may throw.
The Pylon device is closed with Close() if the OnOpened event call triggers an
exception.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsGigE "

Returns true if a GigE Pylon device is attached to the Instant Camera object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::~CInstantCamera "

Destroys an Instant Camera object.  

Calls Attach( NULL) for destroying or removing a Pylon device depending on the
passed cleanup procedure.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCamera::RetrieveResult "

Retrieves a grab result according to the strategy, waits if it is not yet
available.  

*   The content of the passed grab result is released.  
*   If no Pylon device is attached or the grabbing is not started, the method
    returns immediately \"false\".  
*   Wait for a grab result if it is not yet available. The access to the camera
    is not locked during waiting. Camera events are handled.  
*   Only if camera events are used: Incoming camera events are handled.  
*   One grab result is retrieved per call according to the strategy applied.  
*   Only if chunk mode is used: The chunk data parsing is performed. The grab
    result data is updated using chunk data.  
*   The image event OnImagesSkipped is fired if grab results have been skipped
    according to the strategy. The notification of event handlers stops when an
    event call triggers an exception.  
*   The image event OnImageGrabbed is fired if a grab result becomes available.
    The notification of event handlers stops when an event call triggers an
    exception.  
*   Stops the grabbing by calling StopGrabbing() if the maximum number of images
    has been grabbed.  

It needs to be checked whether the grab represented by the grab result has been
successful, see CGrabResultData::GrabSucceeded().  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the call successfully retrieved a grab result, false otherwise.  

pre:  

    *   There is no other thread waiting for a result. This will be the case
        when the Instant Camera grab loop thread is used.  

post:  

    *   If a grab result has been retrieved, one image is removed from the
        output queue and is returned in the grabResult parameter.  
    *   If no grab result has been retrieved, an empty grab result is returned
        in the grabResult parameter.  
    *   If the maximum number of images has been grabbed, the grabbing is
        stopped.  
    *   If camera event handling is enabled and camera events were received, at
        least one or more camera event messages have been processed.  

The Instant Camera object is still valid after error. The grabbing is stopped if
an exception is thrown.  

This method is synchronized using the lock provided by GetLock() while not
waiting.  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterCameraEventHandler "

Removes a camera event handler from the list of registered camera event handler
objects.  

If the camera event handler is not found, nothing is done.  

Parameters
----------
* `cameraEventHandler` :  
    The registered receiver of camera events.  
* `nodeName` :  
    The name of the event data node updated on camera event, e.g.
    \"ExposureEndEventTimestamp\" for exposure end event.  

Returns
-------
True if successful  

post:  

    *   The cameraEventHandler is deregistered.  
    *   If the camera event handler has been registered by passing a pointer and
        the cleanup procedure is Cleanup_Delete, the event handler is deleted.  

Does not throw C++ exceptions.  

This method is synchronized using the camera event handler lock. If the camera
is open, the camera node map lock is also used for synchronization.  
";

%feature("docstring") Pylon::CInstantCamera::DestroyDevice "

Destroys the attached Pylon device.  

attention: The node maps, e.g. the camera node map, of the attached Pylon device
    must not be accessed anymore while destroying the Pylon device.  

*   If no Pylon device is attached, nothing is done.  
*   If the Pylon device is open, it is closed by calling Close().  
*   The configuration event OnDestroy is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The Pylon device is destroyed even if the cleanup procedure Cleanup_None has
    been passed when calling Attach() before.  
*   The configuration event OnDestroyed is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  

post: No Pylon device is attached.  

Does not throw C++ exceptions. Possible C++ exceptions are caught and ignored.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::ExecuteSoftwareTrigger "

Executes the software trigger command.  

The camera needs to be configured for software trigger mode. Additionally, the
camera needs to be ready to accept triggers. When triggering a frame this can be
checked using the WaitForFrameTriggerReady() method;  

note: The application has to make sure that the correct trigger is selected
    before calling ExecuteSoftwareTrigger(). This can be done via the camera's
    TriggerSelector node. The `Pylon::CSoftwareTriggerConfiguration` selects the
    correct trigger when the Instant Camera is opened.  

pre:  

    *   The grabbing is started.  
    *   The camera device supports software trigger.  
    *   The software trigger is available. This depends on the configuration of
        the camera device.  

Accessing the camera registers may fail. Throws an exception on timeout if
`timeoutHandling` is TimeoutHandling_ThrowException.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsOpen "

Returns the open state of the Pylon device.  Does not throw C++ exceptions.  

Returns
-------
Returns true if a Pylon device is attached and it is open.  This method is
synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsUsb "

Returns true if a USB Pylon device is attached to the Instant Camera object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::Is1394 "

Returns true if an IEEE 1394 Pylon device is attached to the Instant Camera
object.  

This method is provided for convenience only. The device type can also be
determined as shown in the following example.  


This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetEventGrabberNodeMap "

Provides access to the event grabber node map of the attached Pylon device.  

Returns
-------
Reference to the event grabber node map of the attached Pylon device or a
reference to the empty node map if event grabbing is not supported. The
GENAPI_NAMESPACE::INodeMap::GetNumNodes() method can be used to check whether
the node map is empty.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::CanWaitForFrameTriggerReady "

Checks to see whether the camera device can be queried whether it is ready to
accept the next frame trigger.  

If 'FrameTriggerWait' can be selected for 'AcquisitionStatusSelector' and
'AcquisitionStatus' is readable, the camera device can be queried whether it is
ready to accept the next frame trigger.  

If the nodes mentioned above are not available and the 'SoftwareTrigger' node is
readable, the camera device can be queried whether it is ready to accept the
next frame trigger.  

note: If a camera device can't be queried whether it is ready to accept the next
    frame trigger, the camera device is ready to accept the next trigger after
    the last image triggered has been grabbed, e.g. after you have retrieved the
    last image triggered using RetrieveResult(). Camera devices that can be
    queried whether they are ready to accept the next frame trigger, may not be
    ready for the next frame trigger after the last image triggered has been
    grabbed.  

Returns
-------
Returns true if the camera is open and the camera device can be queried whether
it is ready to accept the next frame trigger.  

post: The 'AcquisitionStatusSelector' is set to 'FrameTriggerWait' if writable.  

Accessing the camera registers may fail.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::IsCameraDeviceRemoved "

Returns the connection state of the camera device.  

The device removal is only detected while the Instant Camera and therefore the
attached Pylon device are open.  

The attached Pylon device is not operable anymore if the camera device has been
removed from the PC. After it is made sure that no access to the Pylon device or
any of its node maps is made anymore the Pylon device should be destroyed using
InstantCamera::DeviceDestroy(). The access to the Pylon device can be protected
using the lock provided by GetLock(), e.g. when accessing parameters.  

Returns
-------
True if the camera device removal from the PC has been detected.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::DeregisterConfiguration "

Removes a configurator from the list of registered configurator objects.  

If the configurator is not found, nothing is done.  

Parameters
----------
* `configurator` :  
    The registered receiver of configuration events.  

Returns
-------
True if successful  

post:  

    *   The configurator is deregistered.  
    *   If the configuration has been registered by passing a pointer and the
        cleanup procedure is Cleanup_Delete, the event handler is deleted.  

Does not throw C++ exceptions.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetQueuedBufferCount "

Deprecated: This method has been deprecated. Use the NumQueuedBuffers parameter
instead.  

Returns
-------
The number of buffers that are queued for grabbing.  
";

%feature("docstring") Pylon::CInstantCamera::GetCameraEventWaitObject "

Provides access to a wait object indicating available camera events.  

This wait object is Pylon device specific and changes when a new Pylon device is
attached to the camera.  

Returns
-------
A wait object indicating available camera events.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::CInstantCamera "

Creates an Instant Camera object with no attached Pylon device.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCamera::CInstantCamera "

Creates an Instant Camera object and calls Attach().  

See Attach() for more information.  

Parameters
----------
* `pDevice` :  
    The Pylon device to attach.  
* `cleanupProcedure` :  
    If cleanupProcedure equals Cleanup_Delete, the Pylon device is destroyed
    when the Instant Camera object is destroyed.  

May throw an exception if the passed Pylon device is open. Does not throw C++
exceptions if the passed Pylon device is closed or NULL.  
";

%feature("docstring") Pylon::CInstantCamera::StopGrabbing "

Stops the grabbing of images.  

*   Nothing is done if the Instant Camera is not currently grabbing.  
*   The configuration event OnGrabStop is fired. Possible C++ exceptions from
    event calls are caught and ignored. All event handlers are notified.  
*   The grabbing is stopped.  
*   All buffer queues of the Instant Camera are cleared.  
*   The OnGrabStopped configuration event is fired if the grab has been stopped
    successfully. Possible C++ exceptions from event calls are caught and
    ignored. All event handlers are notified.  
*   If the Instant Camera has been opened by StartGrabbing, it is closed by
    calling Close().  
*   Grab-specific parameters of the camera object are unlocked, e.g.
    MaxNumBuffers.  

post:  

    *   The grabbing is stopped.  
    *   If the Pylon device has been opened by StartGrabbing and no other camera
        object service requires it to be open, it is closed.  
    *   Grab specific parameters of the camera object are unlocked, e.g.
        MaxNumBuffers.  

Does not throw C++ exceptions. Possible C++ exceptions are caught and ignored.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::StartGrabbing "

Starts the grabbing of images.  

*   If a grab loop thread has been used in the last grab session, the grab loop
    thread context is joined with the caller's context.  
*   If the Pylon device is not already open, it is opened by calling Open().  
*   The configuration event OnGrabStart is fired. The notification of event
    handlers stops when an event call triggers an exception.  
*   Grab-specific parameters of the camera object are locked, e.g.
    MaxNumBuffers.  
*   If the camera device parameter ChunkModeActive is enabled, the Instant
    Camera chunk parsing support is initialized.  
*   If the Instant Camera parameter GrabCameraEvents is enabled, the Instant
    Camera event grabbing support is initialized.  
*   The grabbing is started.  
*   The configuration event OnGrabStarted is fired if the grab has been started
    successfully. The notification of event handlers stops when an event call
    triggers an exception.  
*   If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is started calling RetrieveResult( GrabLoopThreadTimeout,
    grabResult) in a loop.  

Parameters
----------
* `strategy` :  
    The grab strategy. See Pylon::EGrabStrategy for more information  
* `grabLoopType` :  
    If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is used to run the grab loop.  

pre:  

    *   A Pylon device is attached.  
    *   The stream grabber of the Pylon device is closed.  
    *   The grabbing is stopped.  
    *   The attached Pylon device supports grabbing.  
    *   Must not be called while holding the lock provided by GetLock() when
        using the grab loop thread.  

post:  

    *   The grabbing is started.  
    *   Grab-specific parameters of the camera object are locked, e.g.
        MaxNumBuffers.  
    *   If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional
        grab loop thread is running that calls RetrieveResult(
        GrabLoopThreadTimeout, grabResult) in a loop. Images are processed by
        registered image event handlers.  
    *   Operating the stream grabber from outside the camera object will result
        in undefined behavior.  

The Instant Camera object is still valid after error. Open() may throw.
Configuration event calls may throw. The grab implementation may throw. The
grabbing is stopped with StopGrabbing() if the OnGrabStarted event call triggers
an exception. Throws a C++ exception, if Upcoming Image grab strategy is used
together with USB camera devices.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::StartGrabbing "

Starts the grabbing for a maximum number of images.  

Extends the StartGrabbing(EStrategy, EGrabLoop) by a number of images to grab.
If the passed count of images has been reached, StopGrabbing is called
automatically. The images are counted according to the grab strategy. Skipped
images are not taken into account.  

The amount of allocated buffers is reduced to maxImages when grabbing fewer
images than according to the value of the `MaxNumBuffer`  parameter and the grab
strategy is GrabStrategy_OneByOne.  

Parameters
----------
* `maxImages` :  
    The count of images to grab. This value must be larger than zero.  
* `strategy` :  
    The grab strategy. See Pylon::InstantCamera::EStrategy for more information.  
* `grabLoopType` :  
    If grabLoopType equals GrabLoop_ProvidedByInstantCamera, an additional grab
    loop thread is used to run the grab loop.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetStreamGrabberNodeMap "

Provides access to the stream grabber node map of the attached Pylon device.  

Returns
-------
Reference to the stream grabber node map of the attached Pylon device or the
reference to the empty node map if grabbing is not supported. The
GENAPI_NAMESPACE::INodeMap::GetNumNodes() method can be used to check whether
the node map is empty.  

pre:  

    *   A Pylon device is attached.  
    *   The Pylon device is open.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::SetBufferFactory "

Sets an alternative buffer factory that is used for buffer allocation.  

This use of this method is optional and intended for advanced use cases only.  

If NULL is passed as buffer factory then the default buffer factory is used.
Buffers are allocated when StartGrabbing is called. A buffer factory must not be
deleted while it is attached to the camera object and it must not be deleted
until the last buffer is freed. To free all buffers the grab needs to be stopped
and all grab results must be released or destroyed.  

Parameters
----------
* `pFactory` :  
    A pointer to a buffer factory.  
* `cleanupProcedure` :  
    If ownership is cleanupProcedure Cleanup_Delete, the passed factory is
    destroyed when no longer needed.  

This method is synchronized using the lock provided by GetLock().  
";

%feature("docstring") Pylon::CInstantCamera::GetTLNodeMap "

Provides access to the transport layer node map of the attached Pylon device.  

Returns
-------
Reference to the transport layer node map of the attached Pylon device or the
reference to the empty node map if a transport layer node map is not supported.
The GENAPI_NAMESPACE::INodeMap::GetNumNodes() method can be used to check
whether the node map is empty.  

pre: A Pylon device is attached.  

The Instant Camera object is still valid after error.  

This method is synchronized using the lock provided by GetLock().  
";

// File: class_pylon_1_1_c_instant_camera_array.xml


%feature("docstring") Pylon::CInstantCameraArray "

Supports grabbing with multiple camera devices.  

The CInstantCameraArray class is not thread-safe.  

C++ includes: InstantCameraArray.h
";

%feature("docstring") Pylon::CInstantCameraArray::IsCameraDeviceRemoved "

Returns the connection state of the camera devices used by the Instant Cameras
in the array.  

The device removal is only detected if the Instant Cameras and therefore the
attached Pylon Devices are open.  

The Pylon Device is not operable after this event. After it is made sure that no
access to the Pylon Device or any of its node maps is made anymore the Pylon
Device should be destroyed using InstantCamera::DeviceDestroy(). The access to
the Pylon Device can be protected using the lock provided by GetLock(), e.g.
when accessing parameters.  

Returns
-------
True if the camera device removal from the PC for any camera in the array has
been detected.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::CInstantCameraArray "

Creates an Instant Camera Array of size 0.  

Initialize() can be used to adjust the size of the array.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::CInstantCameraArray "

Creates an Instant Camera Array.  

Calls Initialize() to adjust the size of the array.  

Parameters
----------
* `numberOfCameras` :  
    The number of cameras the array shall hold. Can be 0.  

The index operator can be used to access the individual cameras for attaching a
Pylon Device or for configuration.  

Example:  

Does not throw C++ exceptions, except when memory allocation fails.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsOpen "

Returns the open state of the cameras in the array.  Does not throw C++
exceptions.  

Returns
-------
Returns true if all cameras in the array are open. False is returned if the size
of the array is 0.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsGrabbing "

Returns state of grabbing.  

The camera array is grabbing after a successful call to StartGrabbing() until
StopGrabbing() has been called.  

Returns
-------
Returns true if still grabbing.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::RetrieveResult "

Retrieves a grab result according to the strategy, waits if it is not yet
available.  

*   The content of the passed grab result is released.  
*   If the grabbing is not started, the method returns immediately false.  
*   If GrabStrategy_UpcomingImage strategy: RetrieveResult is called for a
    camera. Cameras are processed using a round-robin strategy.  
*   If GrabStrategy_OneByOne, GrabStrategy_LatestImageOnly or
    GrabStrategy_LatestImages strategy: Pending images or camera events are
    retrieved. Cameras are processed using a round-robin strategy.  
*   If GrabStrategy_OneByOne, GrabStrategy_LatestImageOnly or
    GrabStrategy_LatestImages strategy: Wait for a grab result if it is not yet
    available. Camera events are handled.  

The camera array index is assigned to the context value of the instant camera
when Initialize() is called. This context value is attached to the result when
the result is retrieved and can be obtained using the grab result method
GrabResultData::GetCameraContext(). The context value can be used to associate
the result with the camera from where it originated.  

Parameters
----------
* `timeoutMs` :  
    A timeout value in ms for waiting for a grab result, or the INFINITE value.  
* `grabResult` :  
    Receives the grab result.  
* `timeoutHandling` :  
    If timeoutHandling equals TimeoutHandling_ThrowException, a timeout
    exception is thrown on timeout.  

Returns
-------
True if the call successfully retrieved a grab result, false otherwise.  

pre: The preconditions for calling StartGrabbing() are met for every camera in
    the array.  

post:  

    *   If successful, one image is removed from the output queue of a camera
        and is returned in the grabResult parameter.  
    *   If not successful, an empty grab result is returned in the grabResult
        parameter.  

The Instant Camera Array object is still valid after error. The grabbing is
stopped by calling StopGrabbing() if an exception is thrown.  
";

%feature("docstring") Pylon::CInstantCameraArray::DetachDevice "

Detaches all Pylon Devices that are attached to the Instant Cameras in the
array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   DetachDevice is called for all cameras, see CInstantCamera::DetachDevice()
    for more information.  

post:  

    *   No Pylon Devices are attached to the cameras in the array.  
    *   The ownership of the Pylon Devices goes to the caller who is responsible
        for destroying the Pylon Devices.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::~CInstantCameraArray "

Destroys the Instant Camera Array.  

If a grab is in progress, it is stopped by calling StopGrabbing().  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::StartGrabbing "

Starts the grabbing of images for all cameras.  

*   StartGrabbing is called for all cameras with the provided parameters, see
    CInstantCamera::StartGrabbing() for more information.  
*   The grabbing is started.  
*   The starting position for retrieving results is set to the first camera.  

Parameters
----------
* `strategy` :  
    The grab strategy, see Pylon::InstantCamera::EStrategy for more information.  
* `grabLoopType` :  
    Indicates using the internal grab thread of the camera.  

pre:  

    *   The size of the array is larger than 0.  
    *   All devices are attached.  
    *   The grabbing is stopped.  
    *   The preconditions for calling StartGrabbing() are met for every camera
        in the array.  

post: The grabbing is started.  

The camera objects may throw an exception. The grabbing is stopped calling
StopGrabbing() in this case.  
";

%feature("docstring") Pylon::CInstantCameraArray::Initialize "

Initializes the array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   All cameras of the array are destroyed.  
*   A new set of cameras is created. No Pylon Devices are attached.  
*   The camera context values are set to the index of the camera in the array
    using CInstantCamera::SetCameraContext.  

The index operator can be used to access the individual cameras for attaching a
Pylon Device or for configuration.  

Parameters
----------
* `numberOfCameras` :  
    The number of cameras the array shall hold.  

Does not throw C++ exceptions, except when memory allocation fails.  
";

%feature("docstring") Pylon::CInstantCameraArray::IsPylonDeviceAttached "

Returns the attachment state of cameras in the array.  

Returns
-------
True if all cameras in the array have a Pylon Device attached. False is returned
if the size of the array is 0.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::StopGrabbing "

Stops the grabbing of images.  

The grabbing is stopped. StopGrabbing is called for all cameras. See
CInstantCamera::StopGrabbing() for more information.  

post: The grabbing is stopped.  

Does not throw C++ exceptions.  

Can be called while one other thread is polling RetrieveResult() in a
IsGrabbing()/RetrieveResult() loop to stop grabbing.  
";

%feature("docstring") Pylon::CInstantCameraArray::Open "

Opens all cameras in the array.  

Open is called for all cameras. See CInstantCamera::Open() for more information.  

pre:  

    *   The size of the array is larger than 0.  
    *   All devices are attached.  

post: The cameras are open.  

If one camera throws an exception, all cameras are closed by calling Close().  
";

%feature("docstring") Pylon::CInstantCameraArray::DestroyDevice "

Destroys the Pylon Devices that are attached to the Instant Cameras in the
array.  

attention: The node maps, e.g. the camera node map, of the attached Pylon Device
    must not be accessed anymore while destroying the Pylon Device.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   DestroyDevice is called for all cameras. See CInstantCamera::DestroyDevice()
    for more information.  

post: No Pylon Devices are attached to the cameras in the array.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::GetSize "

Returns the size of the array.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CInstantCameraArray::Close "

Closes all cameras in the array.  

*   If a grab is in progress, it is stopped by calling StopGrabbing().  
*   Close is called for all cameras, see CInstantCamera::Close() for more
    information.  

post: All cameras in the array are closed.  

Does not throw C++ exceptions.  
";

// File: class_basler___instant_camera_params_1_1_c_instant_camera_params___params.xml


%feature("docstring") Basler_InstantCameraParams::CInstantCameraParams_Params "

Interface to instant camera parameters.  

C++ includes: _InstantCameraParams.h
";

/*
 Root - Instant camera parameters. 
*/

/*
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 InternalGrabEngineThread - Parameters of the internal grab engine thread. 
*/

/*
 InternalGrabEngineThread - Parameters of the internal grab engine thread. 
*/

/*
 GrabLoopThread - Parameters of the optional grab loop  thread. 
*/

/*
 GrabLoopThread - Parameters of the optional grab loop  thread. 
*/

/*
 GrabLoopThread - Parameters of the optional grab loop  thread. 
*/

/*
 GrabLoopThread - Parameters of the optional grab loop  thread. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

/*
 Root - Instant camera parameters. 
*/

// File: class_pylon_1_1_c_interface_info.xml


%feature("docstring") Pylon::CInterfaceInfo "

Class used for storing information about an interface object provided by a
transport layer.  

Enumerating the available Transport Layer Interface objects returns a list of
CInterface objects (Pylon::InterfaceInfoList_t). A CInterfaceInfo object holds
information about the enumerated interface.  

C++ includes: InterfaceInfo.h
";

// File: class_pylon_1_1_c_node_map_proxy_t.xml


%feature("docstring") Pylon::CNodeMapProxyT "

Implementation Detail: This class wraps programming interfaces that are
generated from GenICam parameter description files to provide native parameter
access.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: NodeMapProxy.h
";

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Partial implementation of the INodeMap interface 
*/

/*
See GENAPI_NAMESPACE::INodeMap for more details  

*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CNodeMapProxyT::IsAttached "

Checks if a pylon node map is attached.  
";

%feature("docstring") Pylon::CNodeMapProxyT::GetNode "


";

%feature("docstring") Pylon::CNodeMapProxyT::Attach "

Attach a pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::~CNodeMapProxyT "

Destructor.  
";

%feature("docstring") Pylon::CNodeMapProxyT::Poll "


";

%feature("docstring") Pylon::CNodeMapProxyT::GetNodeMap "

Returns the pylon node map interface pointer.  
";

%feature("docstring") Pylon::CNodeMapProxyT::CNodeMapProxyT "

Creates a CNodeMapProxyT object that is not attached to a node map. Use the
Attach() method to attach the pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::CNodeMapProxyT "

Creates a CNodeMapProxyT object and attaches it to a pylon node map.  
";

%feature("docstring") Pylon::CNodeMapProxyT::GetNodes "


";

%feature("docstring") Pylon::CNodeMapProxyT::InvalidateNodes "


";

// File: class_pylon_1_1_t_list_1_1const__iterator.xml


%feature("docstring") Pylon::TList::const_iterator "
";

%feature("docstring") Pylon::TList::const_iterator::const_iterator "
";

// File: class_pylon_1_1_c_pixel_format_converter.xml


%feature("docstring") Pylon::CPixelFormatConverter "
";

%feature("docstring") Pylon::CPixelFormatConverter::SetOutputBitAlignment "
";

%feature("docstring") Pylon::CPixelFormatConverter::Convert "
";

%feature("docstring") Pylon::CPixelFormatConverter::IsInitialized "
";

%feature("docstring") Pylon::CPixelFormatConverter::Init "
";

// File: class_pylon_1_1_c_pixel_format_converter_mono_packed.xml


%feature("docstring") Pylon::CPixelFormatConverterMonoPacked "
";

%feature("docstring") Pylon::CPixelFormatConverterMonoPacked::PYLON_UTILITY_3_0_DEPRECATED "
";

// File: class_pylon_1_1_c_pixel_format_converter_mono_x_x.xml


%feature("docstring") Pylon::CPixelFormatConverterMonoXX "
";

// File: class_pylon_1_1_c_pixel_type_mapper.xml


%feature("docstring") Pylon::CPixelTypeMapper "

A simple pixeltypemapper (maps device specific pixelformats read from device-
node map to pylon pixeltypes by their name).  

Use this mapper to convert a device specifc Pylon::PixelFormat value to a
Pylon::EPixelType used for PixelFormatConverters. When passing the symbolic name
of the pixeltype you can use the static function
CPixelTypeMapper::GetPylonPixelTypeByName(). If you want to convert a nodeValue
you must first create a CPixelTypeMapper instance and pass the constructor a
pointer the PixelFormat node of the device you want the node value to be
converted. Then call CPixelTypeMapper::GetPylonPixelTypeFromNodeValue() to get
the corresponding Pylon::EPixelType.  

C++ includes: PixelTypeMapper.h
";

%feature("docstring") Pylon::CPixelTypeMapper::~CPixelTypeMapper "

default d'tor  
";

%feature("docstring") Pylon::CPixelTypeMapper::IsValid "

Checks the objects validity.  

Returns
-------
Returns true if the object is initialized properly.  

Essentially this function checks whether you've called SetPixelFormatEnumNode.  
";

%feature("docstring") Pylon::CPixelTypeMapper::SetPixelFormatEnumNode "

Lazy initialization of the object.  

Parameters
----------
* `pEnum` :  
    Pointer to the enumeration node containing the PixelFormats.  

Call this function initialize the mapper when using the default c'tor.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeFromNodeValue "

Converts a enumeration node value to a Pylon::EPixelType enum.  

Parameters
----------
* `nodeValue` :  
    node value to convert. You can obtain this value by calling
    GENAPI_NAMESPACE::IEnumeration::GetIntValue.  

Returns
-------
Returns the Pylon::EPixelType for a given pixelformat enum value defined in the
Enum passed in c'tor  

Converts a enumeration node value to a Pylon::EPixelType enum. You must have
initialized the mapper before you can call this function.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetNameByPixelType "

Static function that returns a string representation of the given EPixelType.  

Parameters
----------
* `pixelType` :  
    The pixel type to return the name for.  
* `sfncVer` :  
    SFNC Version to use when doing the mapping. Some names have been changed in
    SFNC 2.0  

Returns
-------
Returns the pointer to a null terminated string representing the symbolic name
of the pixel type.  

Passing Pylon::PixelType_Mono16 will return \"Mono16\" will be returned. If the
pixel type is not known an empty string is returned.  

note: The returned name cannot be used to parameterize the pixel format of a
    camera device, because the camera's pixel format name can be different. The
    camera's pixel format name depends on the used standard feature naming
    convention (SFNC).  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `pszSymbolicName` :  
    pointer to the symbolic name. Note: Symbolic names are case sensitive. You
    can obtain the symbolic name by calling
    GENAPI_NAMESPACE::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup soley by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CPixelTypeMapper::GetPylonPixelTypeByName "

Returns a Pylon::EPixelType for a given symbolic name.  

Parameters
----------
* `symbolicName` :  
    The symbolic name. Note: Symbolic names are case sensitive. You can obtain
    the symbolic name by calling GENAPI_NAMESPACE::IEnumEntry::GetSymbolic()  

Returns
-------
Returns the Pylon_PixelType for a given symbolic name.  

Static version which does the lookup solely by symbolic string comparison.
Passing \"Mono16\" will return Pylon::PixelType_Mono16. If the name is not found
Pylon::PixelType_Undefined will be returned.  
";

%feature("docstring") Pylon::CPixelTypeMapper::CPixelTypeMapper "

Create an empty mapper. Before calling any non-static function you must call
SetPixelFormatEnumNode to initialize the mapper.  
";

%feature("docstring") Pylon::CPixelTypeMapper::CPixelTypeMapper "

create and initialize a mapper by using the enum node passed.  
";

// File: class_pylon_1_1_c_pylon_bitmap_image.xml


%feature("docstring") Pylon::CPylonBitmapImage "

This class can be used to easily create Windows bitmaps for displaying images.  

*   Automatically handles the bitmap creation and lifetime.  
*   Provides methods for loading and saving an image in different file formats.  
*   Serves as target format for the `CImageFormatConverter` image format
    converter.  

par: Buffer Handling:
    The bitmap buffer that is automatically created by the CPylonBitmapImage
    class. The Release() method can be used to release a bitmap.  

The CPylonBitmapImage class is not thread-safe.  

C++ includes: PylonBitmapImage.h
";

%feature("docstring") Pylon::CPylonBitmapImage::GetPixelType "
";

%feature("docstring") Pylon::CPylonBitmapImage::~CPylonBitmapImage "

Destroys a pylon image object.  

attention: The bitmap handle must not be currently selected into a DC. Otherwise
    the bitmap is not freed.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CopyImage "

Copies the image data from a different image.  

The input image is automatically converted if needed to PixelType_Mono8 if
Pylon::IsMonoImage( pixelTypeSource) is true, otherwise it is converted to
PixelType_BGR8packed. The orientation of the image is changed to bottom up.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert other images with a CPylonBitmapImage object as target.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre: The preconditions of the Reset() method must be met.  

post:  

    *   The source image is automatically converted.  
    *   Creates an invalid image if the source image is invalid.  

Throws an exception when the bitmap could not be created. Throws an exception
when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CopyImage "

Sets an image from a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The preconditions of the Reset() method must be met.  

post: The source image is automatically converted. See CopyImage().  

Throws an exception when when the bitmap could not be created. Throws an
exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CPylonBitmapImage "

Creates an invalid image.  

See Pylon::IImage on how the properties of an invalid image are returned.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::CPylonBitmapImage "

Copies the image properties and creates a reference to the bitmap of the source
image.  

Parameters
----------
* `source` :  
    The source image.  

post:  

    *   Another reference to the source bitmap is created.  
    *   Creates an invalid image if the source image is invalid.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonBitmapImage::Create "

Creates an image and a Windows bitmap for it.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be supported, see IsSupportedPixelType().  
    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

Throws an exception when the parameters are invalid. Throws an exception when
the bitmap could not be created.  
";

%feature("docstring") Pylon::CPylonBitmapImage::GetOrientation "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetStride "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetWidth "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetHeight "
";

%feature("docstring") Pylon::CPylonBitmapImage::Detach "

Detach the windows bitmap.  

Returns
-------
Returns the handle of the windows bitmap or NULL if the image is invalid.  

pre: IsUnique() must return true. No other image must reference the bitmap.  

post:  

    *   The image is invalid.  
    *   The ownership of the bitmap goes to the caller who is responsible for
        deleting it.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonBitmapImage::Reset "

Resets the image properties and creates a new Windows bitmap if required.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be > 0 and < _I32_MAX.  
    *   The `height` value must be > 0 and < _I32_MAX.  

post:  

    *   If the previously referenced bitmap is also referenced by another pylon
        bitmap image, a new Windows bitmap is created.  
    *   If the previously referenced bitmap is able to hold an image with the
        given properties, a new Windows bitmap is created.  
    *   If no bitmap has been created before, a new Windows bitmap is created.  

Throws an exception when the preconditions are not met. Throws an exception when
no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::CPylonBitmapImage::IsValid "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsAdditionalPaddingSupported "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsUnique "
";

%feature("docstring") Pylon::CPylonBitmapImage::IsSupportedPixelType "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetPaddingX "
";

%feature("docstring") Pylon::CPylonBitmapImage::GetImageSize "
";

%feature("docstring") Pylon::CPylonBitmapImage::Release "
";

// File: class_pylon_1_1_c_pylon_device_proxy_t.xml


%feature("docstring") Pylon::CPylonDeviceProxyT "

Low Level API: The camera class for generic camera devices.  

This is the base class for pylon camera classes providing access to camera
parameters.  

See also: configuringcameras  

templateparam
-------------
* `TCameraParams` :  
    The camera specific parameter class (auto generated from camera xml file)  

C++ includes: PylonDeviceProxy.h
";

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Implementation of the IPylonDevice interface. 
*/

/*
See Pylon::IPylonDevice for more details.  

*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CPylonDeviceProxyT::GetDevice "

Returns the pylon device interface pointer.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroyEventAdapter "


Deletes an Event adapter  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::RegisterRemovalCallback "

Registers a surprise removal callback object.  


Parameters
----------
* `d` :  
    reference to a device callback object  

Returns
-------
A handle which must be used to deregister a callback It is recommended to use
one of the RegisterRemovalCallback() helper functions to register a callback.  

Example how to register a C function  

Example how to register a class member function  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::AccessMode "


";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetEventGrabber "

Returns a pointer to an event grabber.  

Event grabbers are used to handle events sent from a camera device.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetStreamGrabber "

Returns a pointer to a stream grabber.  

Stream grabbers (IStreamGrabber) are the objects used to grab images from a
camera device. A camera device might be able to send image data over more than
one logical channel called stream. A stream grabber grabs data from one single
stream.  

Parameters
----------
* `index` :  
    The number of the grabber to return  

Returns
-------
A pointer to a stream grabber, NULL if index is out of range  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CPylonDeviceProxyT "

Creates a camera object that is not attached to an pylon device. Use the
Attach() method to attach the device.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CPylonDeviceProxyT "

Creates a camera object and attaches a camera object to a pylon device that
takes the ownership over an pylon device.  

When having the ownership, the destructor of this camera object destroys the
pylon device the camera object is attached to. Otherwise, the pylon device
object remains valid when the camera object has been destroyed.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::Open "

Opens the stream grabber.  

";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroySelfReliantChunkParser "


Deletes a self-reliant chunk parser  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DestroyChunkParser "

Deletes a chunk parser.  


Parameters
----------
* `pChunkParser` :  
    Pointer to the chunk parser to be deleted  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::DeregisterRemovalCallback "

Deregisters a surprise removal callback object.  


Parameters
----------
* `h` :  
    Handle of the callback to be removed  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetTLNodeMap "

Returns the set of camera related transport layer parameters.  


Returns
-------
Pointer to the GenApi node holding the transport layer parameter. If there are
no transport layer parameters for the device, NULL is returned.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateSelfReliantChunkParser "


Creates a a self-reliant chunk parser, returns NULL if not supported  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetNodeMap "

Returns the set of camera parameters.  

Returns the GenApi node map used for accessing parameters provided by the
transport layer.  

Returns the associated stream grabber parameters.  

Returns
-------
Pointer to the GenApi node map holding the parameters  

If no parameters are available, NULL is returned.  

Returns
-------
NULL, if the transport layer doesn't provide parameters, a pointer to the
parameter node map otherwise.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::IsOpen "

Retrieve whether the stream grabber is open.  

";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateChunkParser "

Creates a chunk parser used to update those camera object members reflecting the
content of additional data chunks appended to the image data.  


Returns
-------
Pointer to the created chunk parser  

note: Don't try to delete a chunk parser pointer by calling free or delete.
    Instead, use the DestroyChunkParser() method  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetNumStreamGrabberChannels "


";

%feature("docstring") Pylon::CPylonDeviceProxyT::Close "

Closes the stream grabber.  

Flushes the result queue and stops the thread.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::IsAttached "

Checks if a pylon device is attached to the camera object.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::HasOwnership "

Checks if the camera object has the ownership of the pylon device.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::~CPylonDeviceProxyT "

Destructor.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::CreateEventAdapter "


Creates an Event adapter  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::Attach "

Attach the camera object to a pylon device.  

It is not allowed to call Attach when the camera object is already attached!  

When having the ownership, the destructor of this camera object destroys the
pylon device the camera object is attached to. Otherwise, the pylon device
object remains valid when the camera object has been destroyed.  
";

%feature("docstring") Pylon::CPylonDeviceProxyT::GetDeviceInfo "


";

// File: class_pylon_1_1_c_pylon_image.xml


%feature("docstring") Pylon::CPylonImage "

Describes an image.  

*   Automatically handles size and lifetime of the image buffer.  
*   Allows to take over a buffer of grab result which is preventing its reuse as
    long as required.  
*   Allows to connect user buffers or buffers provided by third party software
    packages.  
*   Provides methods for loading and saving an image in different file formats.  
*   Serves as the main target format for the image format converter
    `CImageFormatConverter`.  
*   Eases working with planar images.  
*   Eases extraction of AOIs, e.g. for thumbnail images of defects.  

par: Buffer Handling:
    The buffer that is automatically created by the CPylonImage class or a
    hosted grab result buffer are replaced by a larger buffer if required. The
    size of the allocated buffer is never decreased. Referenced user buffers are
    never automatically replaced by a larger buffer. Referenced grab result
    buffers are never reused. See the Reset() method for more details. The
    Release() method can be used to detach a user buffer, release a hosted grab
    result buffer or to free an allocated buffer.  

The CPylonImage class is not thread-safe.  

C++ includes: PylonImage.h
";

%feature("docstring") Pylon::CPylonImage::IsUserBufferAttached "

Returns true if the referenced buffer has been provided by the user.  
";

%feature("docstring") Pylon::CPylonImage::AttachGrabResultBuffer "

Attaches a grab result buffer.  

Parameters
----------
* `grabResult` :  
    The source image represented by a grab result.  

post:  

    *   The image properties are taken over from the grab result.  
    *   The grab result buffer is used by the image class.  
    *   Another reference to the grab result buffer is created. This prevents
        the buffer's reuse for grabbing.  
    *   Creates an invalid image if the `grabResult` is invalid.  
    *   Creates an invalid image if the grab was not successful. See
        CGrabResultData::GrabSucceeded().  

Throws an exception when no buffer with the required size could be allocated.
Throws an exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonImage::IsSupportedPixelType "
";

%feature("docstring") Pylon::CPylonImage::GetPixelType "
";

%feature("docstring") Pylon::CPylonImage::CPylonImage "

Creates an invalid image.  

See Pylon::IImage on how the properties of an invalid image are returned.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::CPylonImage "

Copies the image properties and creates a reference to the buffer of the source
image.  

Parameters
----------
* `source` :  
    The source image.  

post:  

    *   Another reference to the source image buffer is created.  
    *   Creates an invalid image if the source image is invalid.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::GetWidth "
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a different image.  

This method is used for making a full copy of an image. Calls the Reset() method
to set the same image properties as the source image and copies the image data.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  

pre: The preconditions of the Reset() method must be met.  

post:  

    *   The image contains a copy of the image data contained by the source
        image.  
    *   Creates an invalid image if the source image is invalid.  

Throws an exception when no buffer with the required size could be allocated.
Throws an exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a different image and changes the padding while
copying.  

This method is used for making a full copy of an image except for changing the
padding. Calls the Reset() method to set the same image properties as the source
image and copies the image data. This method is useful in combination with the
GetAoi() method.  

Parameters
----------
* `image` :  
    The source image, e.g. a CPylonImage, CPylonBitmapImage, or Grab Result
    Smart Pointer object.  
* `newPaddingX` :  
    The number of extra data bytes at the end of each row.  

pre:  

    *   The preconditions of the Reset() method must be met.  
    *   The rows of the source image must be byte aligned. This may not be the
        case for packed pixel types. See Pylon::IsPacked().  
    *   The rows of the newly created image must be byte aligned. This may not
        be the case for packed pixel types. See Pylon::IsPacked().  

post:  

    *   The image contains a copy of the image data contained by the source
        image.  
    *   The line padding is adjusted.  
    *   The byte aligned row padding area is set to zero.  
    *   Creates an invalid image if the source image is invalid.  

Throws an exception when no buffer with the required size could be allocated.
Throws an exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonImage::CopyImage "

Copies the image data from a provided buffer.  

This method is used for making a full copy of an image. Calls the Reset() method
to set the same image properties as the source image and copies the image data.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  
    *   The preconditions of the Reset() method must be met.  

post: A copy of the image contained by the source image buffer is made.  

Throws an exception when no buffer with the required size could be allocated.
Throws an exception when the preconditions of the Reset() method are not met.  
";

%feature("docstring") Pylon::CPylonImage::Reset "

Resets the image properties and allocates a new buffer if required.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   If a user buffer is referenced then this buffer must not be referenced
        by another pylon image. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced then this buffer must be large enough to
        hold the destination image. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  

post:  

    *   If the previously referenced buffer is a grab result buffer, a new
        buffer has been allocated.  
    *   If the previously referenced buffer is also referenced by another pylon
        image, a new buffer has been allocated.  
    *   If the previously referenced buffer is not large enough to hold an image
        with the given properties, a new buffer has been allocated.  
    *   If no buffer has been allocated before, a buffer has been allocated.  

Throws an exception when the preconditions are not met. Throws an exception when
no buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::CPylonImage::Reset "

Extends the Reset( EPixelType, uint32_t, uint32_t, EImageOrientation) method by
settable paddingX.  


Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   If a user buffer is referenced then this buffer must not be referenced
        by another pylon image. See the IsUnique() and IsUserBufferAttached()
        methods.  
    *   If a user buffer is referenced then this buffer must be large enough to
        hold the destination image. See the GetAllocatedBufferSize() and
        IsUserBufferAttached() methods.  

post:  

    *   If the previously referenced buffer is a grab result buffer, a new
        buffer has been allocated.  
    *   If the previously referenced buffer is also referenced by another pylon
        image, a new buffer has been allocated.  
    *   If the previously referenced buffer is not large enough to hold an image
        with the given properties, a new buffer has been allocated.  
    *   If no buffer has been allocated before, a buffer has been allocated.  

Throws an exception when the preconditions are not met. Throws an exception when
no buffer with the required size could be allocated.  

Parameters
----------
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
";

%feature("docstring") Pylon::CPylonImage::IsGrabResultBufferAttached "

Returns true if the referenced buffer has been provided by a grab result.  
";

%feature("docstring") Pylon::CPylonImage::AttachUserBuffer "

Attaches a user buffer.  

Parameters
----------
* `pBuffer` :  
    The pointer to the buffer of the source image.  
* `bufferSizeBytes` :  
    The size of the buffer of the source image.  
* `pixelType` :  
    The pixel type of the source image.  
* `width` :  
    The number of pixels in a row in the source image.  
* `height` :  
    The number of rows in the source image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  
    *   The pointer to the source buffer must not be NULL.  
    *   The source buffer must be large enough to hold the image described by
        the parameters.  

post:  

    *   The image properties are taken over from the passed parameters.  
    *   The user buffer is used by the image class.  
    *   The buffer must not be freed while being attached.  

Throws an exception if the preconditions are not met.  
";

%feature("docstring") Pylon::CPylonImage::GetAllocatedBufferSize "

Returns the size of the used buffer.  

This method is useful when working with so-called user buffers.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImage::Release "
";

%feature("docstring") Pylon::CPylonImage::IsAdditionalPaddingSupported "
";

%feature("docstring") Pylon::CPylonImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonImage::GetBuffer "
";

%feature("docstring") Pylon::CPylonImage::GetPaddingX "
";

%feature("docstring") Pylon::CPylonImage::IsUnique "
";

%feature("docstring") Pylon::CPylonImage::ChangePixelType "

Changes the pixel type of the image.  

Parameters
----------
* `pixelType` :  
    The new pixel type.  

pre:  

    *   Pylon::SamplesPerPixel( oldPixelType) == Pylon::SamplesPerPixel(
        newPixelType)  
    *   Pylon::BitPerPixel( oldPixelType) == Pylon::BitPerPixel( newPixelType)  

Throws an exception when the new pixel type properties do not match the existing
ones.  
";

%feature("docstring") Pylon::CPylonImage::GetPlane "

Creates a new pylon image for a plane of the image. No image data is copied.  

Use CopyImage( const IImage& image) to create a full copy.  


Parameters
----------
* `planeIndex` :  
    The zero based index of the plane.  

Returns
-------
A pylon image referencing a plane of the image.  

pre: The value of planeIndex < Pylon::PlaneCount( GetPixelType()).  

post:  

    *   A reference to the same buffer is created. No image data is copied.  
    *   The returned image has the Pylon::GetPlanePixelType( GetPixelType())
        pixel type.  
    *   If the image is not planar only index 0 is allowed. A call passing index
        0 returns a copy of the image. No image data is copied.  

Throws an exception when the plane index is out of range.  
";

%feature("docstring") Pylon::CPylonImage::GetImageSize "
";

%feature("docstring") Pylon::CPylonImage::IsValid "
";

%feature("docstring") Pylon::CPylonImage::GetHeight "
";

%feature("docstring") Pylon::CPylonImage::GetOrientation "
";

%feature("docstring") Pylon::CPylonImage::GetStride "
";

%feature("docstring") Pylon::CPylonImage::GetAoi "

Creates a new pylon image for an image area of interest (Image AOI) derived from
the image. No image data is copied.  

Use CopyImage( const IImage& image, size_t newPaddingX) to create a full copy
and to remove the additional padding.  


Parameters
----------
* `topLeftX` :  
    The x-coordinate of the top left corner of the image AOI in pixels.  
* `topLeftY` :  
    The y-coordinate of the top left corner of the image AOI in pixels.  
* `width` :  
    The width of the image AOI in pixels.  
* `height` :  
    The height of the image AOI in pixels.  

Returns
-------
A pylon image referencing an image AOI of the image.  

pre:  

    *   The image must be valid.  
    *   The image AOI is located inside the image.  
    *   The image is not in a planar format, see Pylon::IsPlanar(). Use
        GetPlane() first in this case.  
    *   The rows of the image must be byte aligned. This may not be the case for
        packed pixel types. See Pylon::IsPacked().  
    *   The x-coordinate must be byte aligned. This may not be the case for
        packed pixel types. See Pylon::IsPacked().  
    *   The `topLeftX` parameter must be divisible by the return value of
        Pylon::GetPixelIncrementX() for the image's pixel type.  
    *   The `topLeftY` parameter must be divisible by the return value of
        Pylon::GetPixelIncrementY() for the image's pixel type.  

post:  

    *   A reference to the same buffer is created. The image data is not copied.  
    *   The returned image uses the paddingX property to skip over image content
        outside of the image AOI.  

Throws an exception when the preconditions are not met.  
";

%feature("docstring") Pylon::CPylonImage::Create "

Creates an image and allocates a buffer for it.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

Throws an exception when the parameters are invalid. Throws an exception when no
buffer with the required size could be allocated.  
";

%feature("docstring") Pylon::CPylonImage::~CPylonImage "

Destroys a pylon image object.  

Does not throw C++ exceptions.  
";

// File: class_pylon_1_1_c_pylon_image_base.xml


%feature("docstring") Pylon::CPylonImageBase "

Provides basic functionality for pylon image classes.  

C++ includes: PylonImageBase.h
";

%feature("docstring") Pylon::CPylonImageBase::Save "

Saves the image to disk. Converts the image to a format that can be saved if
required.  

This is a convenience method that calls CImagePersistence::Save().  

If required, the image is automatically converted into a new image and saved
afterwards. See CImagePersistence::CanSaveWithoutConversion() for more
information. An image with a bit depth higher than 8 bit is stored with 16 bit
bit depth, if supported by the image file format. In this case the pixel data is
MSB aligned.  

If more control over the conversion is required, the CImageFormatConverter class
can be used to convert the input image before saving it.  

Parameters
----------
* `imageFileFormat` :  
    File format to save the image in.  
* `filename` :  
    Name and path of the image.  
* `pOptions` :  
    Additional options.  

pre: The pixel type of the image to be saved must be a supported input format of
    the Pylon::CImageFormatConverter.  

Throws an exception if the saving of the image fails.  
";

%feature("docstring") Pylon::CPylonImageBase::GetPixelData "

Retrieves the data of a pixel.  

note: This method is relativly slow. Do not use it for image processing tasks.  

Parameters
----------
* `posX` :  
    Horizontal position of the pixel. The first column has position 0.  
* `posY` :  
    Vertical position of the pixel. The first row has position 0.  

Returns
-------
Returns the data of a pixel for supported pixel types. For unsupported pixel
types pixel data of the SPixelData::PixelDataType_Unknown type is returned.  

pre:  

    *   The image must be valid.  
    *   The pixel position defined by `posX` and `posY` must be located inside
        the image area.  

Supported pixel types:  

*   PixelType_Mono1packed  
*   PixelType_Mono2packed  
*   PixelType_Mono4packed  
*   PixelType_Mono8  
*   PixelType_Mono8signed  
*   PixelType_Mono10  
*   PixelType_Mono10packed  
*   PixelType_Mono10p  
*   PixelType_Mono12  
*   PixelType_Mono12packed  
*   PixelType_Mono12p  
*   PixelType_Mono16  

*   PixelType_BayerGR8  
*   PixelType_BayerRG8  
*   PixelType_BayerGB8  
*   PixelType_BayerBG8  
*   PixelType_BayerGR10  
*   PixelType_BayerRG10  
*   PixelType_BayerGB10  
*   PixelType_BayerBG10  
*   PixelType_BayerGR12  
*   PixelType_BayerRG12  
*   PixelType_BayerGB12  
*   PixelType_BayerBG12  
*   PixelType_BayerGR12Packed  
*   PixelType_BayerRG12Packed  
*   PixelType_BayerGB12Packed  
*   PixelType_BayerBG12Packed  
*   PixelType_BayerGR10p  
*   PixelType_BayerRG10p  
*   PixelType_BayerGB10p  
*   PixelType_BayerBG10p  
*   PixelType_BayerGR12p  
*   PixelType_BayerRG12p  
*   PixelType_BayerGB12p  
*   PixelType_BayerBG12p  
*   PixelType_BayerGR16  
*   PixelType_BayerRG16  
*   PixelType_BayerGB16  
*   PixelType_BayerBG16  

*   PixelType_RGB8packed  
*   PixelType_BGR8packed  
*   PixelType_RGBA8packed  
*   PixelType_BGRA8packed  
*   PixelType_RGB10packed  
*   PixelType_BGR10packed  
*   PixelType_RGB12packed  
*   PixelType_BGR12packed  
*   PixelType_RGB12V1packed  
*   PixelType_RGB16packed  
*   PixelType_RGB8planar  
*   PixelType_RGB10planar  
*   PixelType_RGB12planar  
*   PixelType_RGB16planar  

*   PixelType_YUV422packed  
*   PixelType_YUV422_YUYV_Packed  

Throws an exception, if the preconditions are not met.  
";

%feature("docstring") Pylon::CPylonImageBase::CanSaveWithoutConversion "

Can be used to check whether the image can be saved without prior conversion.  

This is a convenience method that calls
CImagePersistence::CanSaveWithoutConversion().  

Parameters
----------
* `imageFileFormat` :  
    Target file format for the image to be saved.  

Returns
-------
Returns true, if the image can be saved without prior conversion.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::CPylonImageBase::Load "

Loads an image from a disk.  

This is a convenience method that calls CImagePersistence::Load()  

Parameters
----------
* `filename` :  
    Name and path of the image.  

pre: The image object must be able to hold the image format of the loaded image.  

Throws an exception if the image cannot be loaded. The image buffer content is
undefined when the loading of the image fails.  
";

// File: class_pylon_1_1_c_software_trigger_configuration.xml


%feature("docstring") Pylon::CSoftwareTriggerConfiguration "

Changes the configuration of the camera so that the acquisition of frames is
triggered by software trigger. Use together with
CInstantCamera::WaitForFrameTriggerReady() and
CInstantCamera::ExecuteSoftwareTrigger().  

The CSoftwareTriggerConfiguration is provided as header-only file. The code can
be copied and modified for creating own configuration classes.  

C++ includes: SoftwareTriggerConfiguration.h
";

%feature("docstring") Pylon::CSoftwareTriggerConfiguration::ApplyConfiguration "

Apply software trigger configuration.  
";

%feature("docstring") Pylon::CSoftwareTriggerConfiguration::OnOpened "

This method is called after the attached Pylon Device has been opened.  

Parameters
----------
* `camera` :  
    The source of the call.  

Exceptions from this call will propagate through. The notification of event
handlers stops when an exception is triggered.  

This method is called inside the lock of the camera object.  
";

// File: class_pylon_1_1_c_stream_grabber_proxy_t.xml


%feature("docstring") Pylon::CStreamGrabberProxyT "

Low Level API: The stream grabber class with parameter access methods.  

This is the base class for pylon stream grabber providing access to
configuration parameters.  

See also: configuringcameras  

templateparam
-------------
* `TParams` :  
    The specific parameter class (auto generated from the parameter xml file)  

C++ includes: StreamGrabberProxy.h
";

/*
 Construction 
*/

/*
 Some smart pointer functionality 
*/

/*
 Implementation of the IStreamGrabber interface 
*/

/*
See Pylon::IStreamGrabber for more details.  

*/

/*
 Assignment and copying is not supported 
*/

%feature("docstring") Pylon::CStreamGrabberProxyT::GetStreamGrabber "

Returns the pylon stream grabber interface pointer.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::GetNodeMap "

Returns the set of camera parameters.  

Returns the GenApi node map used for accessing parameters provided by the
transport layer.  

Returns the associated stream grabber parameters.  

Returns
-------
Pointer to the GenApi node map holding the parameters  

If no parameters are available, NULL is returned.  

Returns
-------
NULL, if the transport layer doesn't provide parameters, a pointer to the
parameter node map otherwise.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::RetrieveResult "

Retrieves a grab result from the output queue.  


Returns
-------
When result was available true is returned and and the first result is copied
into the grabresult. Otherwise the grabresult remains unchanged and false is
returned.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::Open "

Opens the stream grabber.  

";

%feature("docstring") Pylon::CStreamGrabberProxyT::RegisterBuffer "

Registers a buffer for subsequent use.  

Stream must be locked to register buffers The Buffer size may not exceed the
value specified when PrepareGrab was called.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CancelGrab "

Cancels pending requests.  

, resources remain allocated. Following, the results must be retrieved from the
Output Queue.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::QueueBuffer "

Enqueues a buffer in the input queue.  

PrepareGrab is required to queue buffers. The context is returned together with
the buffer and the grab result. It is not touched by the stream grabber. It is
illegal to queue a buffer a second time before it is fetched from the result
queue.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::~CStreamGrabberProxyT "

Destructor.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::Attach "

Attach a pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::FinishGrab "

Stops grabbing.  

Releases the resources and camera. Pending grab requests are canceled.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CStreamGrabberProxyT "

Creates a CStreamGrabberProxyT object that is not attached to a pylon stream
grabber. Use the Attach() method to attach the pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::CStreamGrabberProxyT "

Creates a CStreamGrabberProxyT object and attaches it to a pylon stream grabber.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::DeregisterBuffer "

Deregisters the buffer.  

Deregistering fails while the buffer is in use, so retrieve the buffer from the
output queue after grabbing.  

note: Do not delete buffers before they are deregistered.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::IsOpen "

Retrieve whether the stream grabber is open.  

";

%feature("docstring") Pylon::CStreamGrabberProxyT::GetWaitObject "

Returns the result event object.  

This object is associated with the result queue. The event is signaled when
queue is non-empty  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::Close "

Closes the stream grabber.  

Flushes the result queue and stops the thread.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::IsAttached "

Checks if a pylon stream grabber is attached.  
";

%feature("docstring") Pylon::CStreamGrabberProxyT::PrepareGrab "

Prepares grabbing.  

Allocates resources, synchronizes with the camera and locks critical parameter  
";

// File: class_pylon_1_1_c_tl_factory.xml


%feature("docstring") Pylon::CTlFactory "

the Transport Layer Factory  

Creates, Destroys and Enumerates transport layers as well as their devices.  

C++ includes: TlFactory.h
";

%feature("docstring") Pylon::CTlFactory::IsDeviceAccessible "
";

%feature("docstring") Pylon::CTlFactory::GetInstance "

Retrieve the transport layer factory singleton. Throws an exception when
Pylon::PylonInitialize() has not been called before.  
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "

creates a device from a device info object, see IDeviceFactory for more
information  
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "

creates a device from a device info object, injecting additional GenICam XML
definition strings  
";

%feature("docstring") Pylon::CTlFactory::CreateDevice "

This method is deprecated. Use CreateDevice receiving a CDeviceInfo object
containing the full name as property. example: IPylonDevice* device =
TlFactory.CreateDevice( CDeviceInfo().SetFullName( fullname)); creates a device
by its unique name (i.e. fullname)  
";

%feature("docstring") Pylon::CTlFactory::CreateTl "

Create a transport layer object from a TlInfo object.  
";

%feature("docstring") Pylon::CTlFactory::CreateTl "

Create a transport layer object specified by the transport layer's device class
identifier.  
";

%feature("docstring") Pylon::CTlFactory::EnumerateDevices "

returns a list of available devices, see IDeviceFactory for more information  
";

%feature("docstring") Pylon::CTlFactory::EnumerateDevices "

returns a list of available devices that match the filter, see IDeviceFactory
for more information  
";

%feature("docstring") Pylon::CTlFactory::DestroyDevice "

destroys a device  
";

%feature("docstring") Pylon::CTlFactory::CreateFirstDevice "

creates first found device from a device info object, see IDeviceFactory for
more information  
";

%feature("docstring") Pylon::CTlFactory::CreateFirstDevice "

creates first found device from a device info object, injecting additional
GenICam XML definition strings  
";

%feature("docstring") Pylon::CTlFactory::EnumerateTls "

Retrieve a list of available transport layers.  
";

%feature("docstring") Pylon::CTlFactory::ReleaseTl "

Destroys a transport layer object.  
";

// File: class_pylon_1_1_c_tl_info.xml


%feature("docstring") Pylon::CTlInfo "

Class used for storing the result of the transport layer enumeration process.  

Enumerating the available Transport Layer objects returns a list of CTlInfo
objects (Pylon::TlInfoList_t). A CTlInfo object holds information about the
enumerated transport layer.  

C++ includes: TlInfo.h
";

// File: class_pylon_1_1_device_info_list.xml


%feature("docstring") Pylon::DeviceInfoList "

STL std::vector like container for Pylon::CDeviceInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

%feature("docstring") Pylon::DeviceInfoList::DeviceInfoList "
";

// File: class_pylon_1_1_event_result.xml


%feature("docstring") Pylon::EventResult "

Low Level API: An event result.  

C++ includes: Result.h
";

%feature("docstring") Pylon::EventResult::Succeeded "
";

%feature("docstring") Pylon::EventResult::ErrorDescription "
";

%feature("docstring") Pylon::EventResult::ErrorCode "
";

%feature("docstring") Pylon::EventResult::EventResult "
";

// File: class_pylon_1_1_function___callback_body.xml


%feature("docstring") Pylon::Function_CallbackBody "
";

%feature("docstring") Pylon::Function_CallbackBody::clone "

virtual copy constructor  
";

%feature("docstring") Pylon::Function_CallbackBody::Function_CallbackBody "

Constructor.  
";

// File: class_pylon_1_1_grab_result.xml


%feature("docstring") Pylon::GrabResult "

Low Level API: A grab result that combines the used image buffer and status
information.  

Note that depending on the used interface technology, the specific camera and
the situation some of the attributes are not meaningful, e. g. timestamp in case
of an canceled grab.  

C++ includes: Result.h
";

%feature("docstring") Pylon::GrabResult::Context "

Get the pointer the user provided context.  
";

%feature("docstring") Pylon::GrabResult::GetSizeX "

Get the actual number of columns in pixel.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetPixelType "

Get the actual pixel type.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::Buffer "

Get the pointer to the buffer.  
";

%feature("docstring") Pylon::GrabResult::GetTimeStamp "

Get the camera specific tick count.  

In case of GigE-Vision this describes when the image exposure was started.
Cameras that do not support this feature return zero. If supported this may be
used to determine which ROIs were acquired simultaneously.  

In case of FireWire this value describes the cycle time when the first packet
arrives.  
";

%feature("docstring") Pylon::GrabResult::GetPaddingY "

Get the number of extra data at the end of the image data in bytes.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::PYLON_DEPRECATED "

Deprecated: GetBlockID() should be used instead. Get the index of the grabbed
frame.  
";

%feature("docstring") Pylon::GrabResult::GetPayloadSize "

Get the actual payload size in bytes.  
";

%feature("docstring") Pylon::GrabResult::GetPaddingX "

Get the number of extra data at the end of each row in bytes.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetImage "

Provides an adapter from the grab result to Pylon::IImage interface.  

This returned adapter allows passing the grab result to saving functions or
image format converter.  

attention: The returned reference is only valid as long the grab result is not
    destroyed.  
";

%feature("docstring") Pylon::GrabResult::GrabResult "

Default constructor.  
";

%feature("docstring") Pylon::GrabResult::GetPayloadSize_t "

Get the actual payload size in bytes as size_t.  
";

%feature("docstring") Pylon::GrabResult::GetOffsetX "

Get the actual starting column.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::Handle "

Get the buffer handle.  
";

%feature("docstring") Pylon::GrabResult::Succeeded "

True if status is grabbed.  
";

%feature("docstring") Pylon::GrabResult::GetErrorDescription "

Get a description of the current error.  
";

%feature("docstring") Pylon::GrabResult::GetSizeY "

Get the actual number of rows in pixel.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetPayloadType "

Get the actual payload type.  
";

%feature("docstring") Pylon::GrabResult::GetErrorCode "

Get the current error code.  
";

%feature("docstring") Pylon::GrabResult::GetOffsetY "

Get the actual starting row.  

This is only defined in case of image data.  
";

%feature("docstring") Pylon::GrabResult::GetBlockID "

Get the block ID of the grabbed frame (camera device specific).  

par: IEEE 1394 Camera Devices
    The value of block ID is always UINT64_MAX.  

par: GigE Camera Devices
    The sequence number starts with 1 and wraps at 65535. The value 0 has a
    special meaning and indicates that this feature is not supported by the
    camera.  

par: USB Camera Devices
    The sequence number starts with 0 and uses the full 64 Bit range.  

attention: A block ID of value UINT64_MAX indicates that the Block ID is invalid
    and must not be used.  
";

%feature("docstring") Pylon::GrabResult::Status "

Get the grab status.  
";

// File: class_i_buffer_factory.xml


%feature("docstring") IBufferFactory "

Usable to create a custom buffer factory when needed.  

C++ includes: BufferFactory.h
";

// File: interface_i_chunk_parser.xml

// File: interface_i_device.xml

// File: interface_i_device_factory.xml

// File: interface_i_event_adapter.xml

// File: interface_i_event_grabber.xml

// File: interface_i_image.xml

// File: class_pylon_1_1_interface_info_list.xml


%feature("docstring") Pylon::InterfaceInfoList "

STL std::vector like container for Pylon::CInterfaceInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

%feature("docstring") Pylon::InterfaceInfoList::InterfaceInfoList "
";

// File: class_pylon_1_1_c_image_format_converter_1_1_i_output_pixel_format_enum.xml


%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum "
";

%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum::SetValue "
";

%feature("docstring") Pylon::CImageFormatConverter::IOutputPixelFormatEnum::GetValue "
";

// File: interface_i_properties.xml

// File: interface_i_pylon_device.xml

// File: interface_i_reusable_image.xml

// File: interface_i_self_reliant_chunk_parser.xml

// File: interface_i_stream_grabber.xml

// File: class_pylon_1_1_t_list_1_1iterator.xml


%feature("docstring") Pylon::TList::iterator "
";

%feature("docstring") Pylon::TList::iterator::iterator "
";

// File: interface_i_transport_layer.xml

// File: class_pylon_1_1_member___callback_body.xml


%feature("docstring") Pylon::Member_CallbackBody "
";

%feature("docstring") Pylon::Member_CallbackBody::Member_CallbackBody "

Constructor.  
";

%feature("docstring") Pylon::Member_CallbackBody::clone "

virtual copy constructor  
";

// File: class_pylon_1_1_pylon_auto_init_term.xml


%feature("docstring") Pylon::PylonAutoInitTerm "

Helper class to automagically call PylonInitialize and PylonTerminate in
constructor and destructor.  

  

C++ includes: PylonBase.h
";

%feature("docstring") Pylon::PylonAutoInitTerm::PylonAutoInitTerm "
";

%feature("docstring") Pylon::PylonAutoInitTerm::~PylonAutoInitTerm "
";

// File: struct_pylon_1_1_s_b_g_r8_pixel.xml


%feature("docstring") Pylon::SBGR8Pixel "

Describes the memory layout of a BGR8 pixel. This pixel is used in Windows
bitmaps.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_b_g_r_a8_pixel.xml


%feature("docstring") Pylon::SBGRA8Pixel "

Describes the memory layout of a BGRA8 pixel. This pixel is used in Windows
bitmaps.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_image_format.xml


%feature("docstring") Pylon::SImageFormat "
";

%feature("docstring") Pylon::SImageFormat::IsValid "
";

%feature("docstring") Pylon::SImageFormat::~SImageFormat "
";

%feature("docstring") Pylon::SImageFormat::SImageFormat "
";

%feature("docstring") Pylon::SImageFormat::SImageFormat "
";

// File: struct_pylon_1_1_s_output_image_format.xml


%feature("docstring") Pylon::SOutputImageFormat "
";

%feature("docstring") Pylon::SOutputImageFormat::IsValid "
";

%feature("docstring") Pylon::SOutputImageFormat::SOutputImageFormat "
";

%feature("docstring") Pylon::SOutputImageFormat::SOutputImageFormat "
";

%feature("docstring") Pylon::SOutputImageFormat::SOutputImageFormat "
";

%feature("docstring") Pylon::SOutputImageFormat::~SOutputImageFormat "
";

// File: struct_pylon_1_1_s_pixel_data.xml


%feature("docstring") Pylon::SPixelData "

Describes the data of one pixel.  

C++ includes: PixelData.h
";

%feature("docstring") Pylon::SPixelData::SPixelData "

Construct and clear.  
";

// File: struct_pylon_1_1_s_r_g_b16_pixel.xml


%feature("docstring") Pylon::SRGB16Pixel "

Describes the memory layout of a RGB16 pixel.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_r_g_b8_pixel.xml


%feature("docstring") Pylon::SRGB8Pixel "

Describes the memory layout of a RGB8 pixel.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_y_u_v422___u_y_v_y.xml


%feature("docstring") Pylon::SYUV422_UYVY "

Describes the memory layout of a YUV422_UYVY pixel with information about
brightness and chroma for two pixels.  

C++ includes: Pixel.h
";

// File: struct_pylon_1_1_s_y_u_v422___y_u_y_v.xml


%feature("docstring") Pylon::SYUV422_YUYV "

Describes the memory layout of a YUV422_YUYV pixel with information about
brightness and chroma for two pixels.  

C++ includes: Pixel.h
";

// File: class_pylon_1_1_tl_info_list.xml


%feature("docstring") Pylon::TlInfoList "

STL std::vector like container for Pylon::CTlInfo objects.  

C++ includes: Container.h
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

%feature("docstring") Pylon::TlInfoList::TlInfoList "
";

// File: class_pylon_1_1_t_list.xml


%feature("docstring") Pylon::TList "

STL std::vector like container class.  

Based on the GenICam::gcstring_vector class.  

C++ includes: Container.h
";

%feature("docstring") Pylon::TList::push_back "
";

%feature("docstring") Pylon::TList::max_size "
";

%feature("docstring") Pylon::TList::insert "
";

%feature("docstring") Pylon::TList::insert "
";

%feature("docstring") Pylon::TList::front "
";

%feature("docstring") Pylon::TList::front "
";

%feature("docstring") Pylon::TList::~TList "
";

%feature("docstring") Pylon::TList::back "
";

%feature("docstring") Pylon::TList::back "
";

%feature("docstring") Pylon::TList::reserve "
";

%feature("docstring") Pylon::TList::pop_back "
";

%feature("docstring") Pylon::TList::assign "
";

%feature("docstring") Pylon::TList::end "
";

%feature("docstring") Pylon::TList::end "
";

%feature("docstring") Pylon::TList::clear "
";

%feature("docstring") Pylon::TList::capacity "
";

%feature("docstring") Pylon::TList::empty "
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::TList "
";

%feature("docstring") Pylon::TList::erase "
";

%feature("docstring") Pylon::TList::erase "
";

%feature("docstring") Pylon::TList::at "
";

%feature("docstring") Pylon::TList::at "
";

%feature("docstring") Pylon::TList::begin "
";

%feature("docstring") Pylon::TList::begin "
";

%feature("docstring") Pylon::TList::size "
";

%feature("docstring") Pylon::TList::resize "
";

// File: class_t_params.xml


%feature("docstring") TParams "
";

// File: class_pylon_1_1_version_info.xml


%feature("docstring") Pylon::VersionInfo "

Holds a four-part version number consisting of major.minor.subminor.build.  

This class stores a four-part version number and provides comparison operators.
If you use the constructor with one parameter, the version info object will be
initialized with pylon base version numbers.  

You can also call the static getVersionString() method to retrieve a string
containing the complete version separated by dots.  

C++ includes: PylonVersionInfo.h
";

%feature("docstring") Pylon::VersionInfo::getSubminor "

Returns the subminor version number. For version 2.1.3.1234 the value 3 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::getVersionString "

Returns the complete version number as a string.  
";

%feature("docstring") Pylon::VersionInfo::getMajor "

Returns the major version number. For version 2.1.3.1234 the value 2 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::~VersionInfo "

The VersionInfo destructor.  
";

%feature("docstring") Pylon::VersionInfo::getBuild "

Returns the build number. For version 2.1.3.1234 the value 1234 would be
returned.  
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using pylon base version numbers. If checkBuild
is set to false, the build number will not be used in comparison operators.  
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using the version number parts passed.  
";

%feature("docstring") Pylon::VersionInfo::VersionInfo "

Constructs a version info object using the version number parts passed.  
";

%feature("docstring") Pylon::VersionInfo::getMinor "

Returns the minor version number. For version 2.1.3.1234 the value 1 would be
returned.  
";

// File: class_pylon_1_1_wait_object.xml


%feature("docstring") Pylon::WaitObject "

A platform independent wait object.  

Wait objects are used by the Pylon::IStreamGrabber and Pylon::IEventGrabber
interfaces to provide a platform independent mechanism for allowing an
application to wait for data buffers to be filled.  

For the Windows version of pylon, WaitObjects are wrappers for Win32 objects
that can be used with `WaitForSingleObject()` and `WaitForMultipleObjects()`.  

For the Linux version of pylon, WaitObjects are implemented based on file
descriptors. The wait operation is implemented using the `poll()` function.  

Although the class provides a default constructor, the default constructor
doesn't create a \"usable\" wait objects wrapping a handle resp. file
descriptor. Valid instances of Pylon::WaitObject cannot be created by the
application, instead the pylon libraries return fully created wait objects. The
Pylon::WaitObjectEx class can be used to create wait objects that can be
controlled by the application.  

The Pylon::WaitObject class provides access to the wrapped handle resp. file
descriptor. This allows to use to allow use pylon wait objects as input for
\"native\" APIs like `WaitForMultipleObjects()` (Windows), and `poll()` (Linux).  

Multiple Pylon::WaitObjects can be put in the Pylon::WaitObjects container class
allowing to wait \"simultaneously\" for multiple events.  

C++ includes: WaitObject.h
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Constructs an \"empty\" wait object, i.e., the wait object is not attached to a
platform dependent wait object (IsValid() == false).  

The Pylon::WaitObjectEx class can be used to create wait objects controllable by
an application.  
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Copy constructor (duplicates the wrapped handle/file descriptor).  
";

%feature("docstring") Pylon::WaitObject::WaitObject "

Constructor taking existing handle (duplicate=false -> take ownership like
std:auto_ptr).  

This method allows to wrap an existing windows handle that can be used with the
`WaitForSingleObject()` and `WaitForMultipleObjects` methods.  
";

%feature("docstring") Pylon::WaitObject::IsValid "

Checks if the wait object is valid.  

Don't call the Wait methods() for an invalid wait object. Wait objects returned
by the pylon libraries are valid.  

Returns
-------
true if the object contains a valid handle/file descriptor  
";

%feature("docstring") Pylon::WaitObject::WaitEx "

Wait for the object to be signaled (interruptible).  

Parameters
----------
* `timeout` :  
    timeout in ms  
* `bAlertable` :  
    When the bAlertable parameter is set to true, the function waits until
    either the timeout elapses, the object enters the signaled state, or the
    wait operation has been interrupted. For Windows, the wait operation is
    interrupted by queued APCs or I/O completion routines. For Linux, the wait
    operation can be interrupted by signals.  

Returns
-------
The returned Pylon::EWaitExResult value indicates the result of the wait
operation.  
";

%feature("docstring") Pylon::WaitObject::~WaitObject "

Destructor.  
";

%feature("docstring") Pylon::WaitObject::Wait "

Wait for the object to be signaled.  

Parameters
----------
* `timeout` :  
    timeout in ms  

Returns
-------
false when the timeout has been expired, true when the waiting was successful
before the timeout has been expired.  
";

%feature("docstring") Pylon::WaitObject::Sleep "

Suspend calling thread for specified time.  

Parameters
----------
* `ms` :  
    wait time in ms  
";

// File: class_pylon_1_1_wait_object_ex.xml


%feature("docstring") Pylon::WaitObjectEx "

A wait object that the user may signal.  

C++ includes: WaitObject.h
";

%feature("docstring") Pylon::WaitObjectEx::Signal "

Set the object to signaled state.  
";

%feature("docstring") Pylon::WaitObjectEx::Reset "

Reset the object to unsignaled state.  
";

%feature("docstring") Pylon::WaitObjectEx::Create "

Creates an event object (manual reset event).  
";

%feature("docstring") Pylon::WaitObjectEx::WaitObjectEx "

Constructs an \"empty\" wait object, i.e., the wait object is not attached to a
platform dependent wait object (IsValid() == false).  

Use the static WaitObjectEx::Create() method to create instances of the
WaitObjectEx class instead.  
";

// File: class_pylon_1_1_wait_objects.xml


%feature("docstring") Pylon::WaitObjects "

A set of wait objects.  

C++ includes: WaitObjects.h
";

%feature("docstring") Pylon::WaitObjects::WaitObjects "

Creates an empty wait object set.  
";

%feature("docstring") Pylon::WaitObjects::WaitObjects "

copy constructor  
";

%feature("docstring") Pylon::WaitObjects::Add "

Add an object to wait on and return the index of the added object.  

Calling Add from another thread during wait operations will cause undefined
behaviour.  
";

%feature("docstring") Pylon::WaitObjects::~WaitObjects "

destructor  
";

%feature("docstring") Pylon::WaitObjects::WaitForAny "

Wait for any one object to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  
* `*pIndex` :  
    (optional) pointer to buffer taking the index of the signaled object  

Returns
-------
true if any object was signaled.  
";

%feature("docstring") Pylon::WaitObjects::WaitForAnyEx "

Wait for any one object to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  
* `bAlertable` :  
    If true, the wait operation can be interrupted (Windows: APC; UNIX: signal)  
* `*pIndex` :  
    (optional) pointer to buffer taking the index of the signaled object  
";

%feature("docstring") Pylon::WaitObjects::WaitForAll "

Wait for all objects to get signaled.  

Parameters
----------
* `timeout` :  
    maximum wait period in milliseconds  

Returns
-------
true if all objects were signaled  
";

%feature("docstring") Pylon::WaitObjects::WaitForAllEx "

Wait for all objects to get signaled.  

Parameters
----------
* `bAlertable` :  
    If true, the wait operation can be interrupted (Windows: APC; UNIX: signal)  
* `timeout` :  
    maximum wait period in milliseconds  
";

%feature("docstring") Pylon::WaitObjects::RemoveAll "

Removes all added wait objects.  

Calling RemoveAll from another thread during wait operations will cause
undefined behaviour.  
";

// File: namespace_basler___image_format_converter_params.xml

// File: namespace_basler___instant_camera_params.xml

// File: namespace_g_e_n_a_p_i___n_a_m_e_s_p_a_c_e.xml

// File: namespacegtl.xml

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetInc "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::GetMin "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::SetValueFromList "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::IsReadable "
";

%feature("docstring") gtl::CorrectDoubleValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::SetValue "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::IsWritable "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::Execute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::CanExecute "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetValue "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::GetMax "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::IsAvailable "
";

%feature("docstring") gtl::CorrectIntValue "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

%feature("docstring") gtl::IsImplemented "
";

// File: namespace_pylon.xml

%feature("docstring") Pylon::Key::BitPerPixel "

Returns the bits needed to store a pixel.  

BitPerPixel(PixelType_Mono12) returns 16 and BitPerPixel(PixelType_Mono12packed)
returns 12 for example.  

Parameters
----------
* `pixelType` :  
    The pixel type.  

pre: The pixel type must be defined.  

Throws an exception when the pixel type is undefined.  
";

%feature("docstring") Pylon::Key::GetSfncVersion "

Helper function for getting the SFNC version from the camera device node map.  
";

%feature("docstring") Pylon::Key::IsPacked "

Returns true if the pixels of the given pixel type are not byte aligned.  
";

%feature("docstring") Pylon::Key::GetNodeMap "

Returns the set of camera parameters.  

Returns the GenApi node map used for accessing parameters provided by the
transport layer.  

Returns the associated stream grabber parameters.  

Returns
-------
Pointer to the GenApi node map holding the parameters  

If no parameters are available, NULL is returned.  

Returns
-------
NULL, if the transport layer doesn't provide parameters, a pointer to the
parameter node map otherwise.  
";

%feature("docstring") Pylon::Key::Sfnc_2_2_0 "

Constant for SFNC version 2.2.0.  
";

%feature("docstring") Pylon::Key::Close "

Closes the stream grabber.  

Flushes the result queue and stops the thread.  
";

%feature("docstring") Pylon::Key::Release "

Releases the image buffer and resets to an invalid image.  

post:  

    *   PixelType = PixelType_Undefined.  
    *   Width = 0.  
    *   Height = 0.  
    *   PaddingX = 0.  
    *   No buffer is allocated.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::Key::GetPylonVersion "

Returns the version number of pylon.  

It is possible to pass a NULL pointer for a version number category if the value
is not of interest.  
";

%feature("docstring") Pylon::Key::Sfnc_1_5_1 "

Constant for SFNC version 1.5.1.  
";

%feature("docstring") Pylon::Key::IsBGRA "

Returns true when the pixel type represents a BGRA format.  
";

%feature("docstring") Pylon::Key::CreateSelfReliantChunkParser "

Creates a a self-reliant chunk parser, returns NULL if not supported  
";

%feature("docstring") Pylon::Key::Open "

Opens the stream grabber.  
";

%feature("docstring") Pylon::Key::GetRTThreadPriority "

Indicates the current thread priority of a thread.  
";

%feature("docstring") Pylon::Key::EnumerateInterfaces "

Retrieves a list of available interfaces.  

note: This method is currently only supported by the pylon GenTL consumer
    transport layer prototype.  

The concept of interfaces is not supported by all transport layers. Depending on
the transport layer, an interface may represent a frame grabber board, a network
card, etc.  

By default, the list passed in will be cleared.  

If the transport layer doesn't support the interface concept,
EnumerateInterfaces() always returns 0.  

Parameters
----------
* `list` :  
    The list to be filled with interface info objects  
* `addToList` :  
    If true, found devices will be added to the list instead of deleting the
    list  

Returns
-------
Number of interfaces provided by the transport layer.  
";

%feature("docstring") Pylon::Key::PylonTerminate "

Frees up resources allocated by the pylon runtime system.  

Call this function before terminating the application. Don't use any pylon
methods or pylon objects after having called PylonTerminate().  

PylonInitialize/PylonTerminate is reference counted. For every call of
PylonInitialize, a call to PylonTerminate is required. The last call to
PylonTerminate will free up all resources.  
";

%feature("docstring") Pylon::Key::IsYUV "

Returns true when the pixel type represents a YUV format.  
";

%feature("docstring") Pylon::Key::CreateDeviceInfo "

Creates and returns an 'empty' Device Info object appropriate for the transport
layer.  

Device Info objects returned by the CreateDeviceInfo() method are used to create
devices from device info objects that are not the result of a device enumeration
process but are provided by the user. The user is responsible for filling in the
fields of the Device Info object that are needed to identify and create a
device.  

Example: To open a GigE device for which the IP address is known, the user lets
the Transport Layer object create a Device Info object, specifies the IP address
and passes the device info object to the CreateDevice() method.  
";

%feature("docstring") Pylon::Key::DeregisterBuffer "

Deregisters the buffer.  

Deregistering fails while the buffer is in use, so retrieve the buffer from the
output queue after grabbing.  

note: Do not delete buffers before they are deregistered.  
";

%feature("docstring") Pylon::Key::CancelGrab "

Cancels pending requests.  

, resources remain allocated. Following, the results must be retrieved from the
Output Queue.  
";

%feature("docstring") Pylon::Key::Sfnc_1_4_0 "

Constant for SFNC version 1.4.0.  
";

%feature("docstring") Pylon::Key::IsBayerPacked "

Returns true if the pixel type is Bayer and the pixel values are not byte
aligned.  
";

%feature("docstring") Pylon::Key::QueueBuffer "

Enqueues a buffer in the input queue.  

PrepareGrab is required to queue buffers. The context is returned together with
the buffer and the grab result. It is not touched by the stream grabber. It is
illegal to queue a buffer a second time before it is fetched from the result
queue.  
";

%feature("docstring") Pylon::Key::SamplesPerPixel "

Returns the number of measured values per pixel.  

SamplesPerPixel(PixelType_Mono8) returns 1 and
SamplesPerPixel(PixelType_RGB8packed) returns 3 for example.  

Parameters
----------
* `pixelType` :  
    The pixel type.  

pre: The pixel type must be defined. The pixel type is not
    PixelType_YUV411packed.  

Throws an exception when the pixel type is undefined.  
";

%feature("docstring") Pylon::Key::RegisterBuffer "

Registers a buffer for subsequent use.  

Stream must be locked to register buffers The Buffer size may not exceed the
value specified when PrepareGrab was called.  
";

%feature("docstring") Pylon::Key::DeregisterRemovalCallback "

Deregisters a surprise removal callback object.  

Parameters
----------
* `h` :  
    Handle of the callback to be removed  
";

%feature("docstring") Pylon::Key::Sfnc_2_0_0 "

Constant for SFNC version 2.0.0. This version or a later version is used by USB
camera devices.  
";

%feature("docstring") Pylon::Key::GetPixelIncrementY "

Returns the minimum step size expressed in pixels for extracting an AOI.  
";

%feature("docstring") Pylon::Key::IsMono "

Returns true when a given pixel is monochrome, e.g. PixelType_Mono8 or
PixelType_BayerGR8.  
";

%feature("docstring") Pylon::Key::BitDepth "

Returns the bit depth of a value of the pixel in bits.  

This may be less than the size needed to store the pixel.
BitDepth(PixelType_Mono12) returns 12, BitDepth(PixelType_Mono12packed) returns
12, and BitDepth(PixelType_RGB8packed) returns 8 for example.  

Parameters
----------
* `pixelType` :  
    The pixel type.  

pre: The pixel type must be valid.  

Throws an exception when the pixel type is undefined.  
";

%feature("docstring") Pylon::Key::RegisterRemovalCallback "

Registers a surprise removal callback object.  

Parameters
----------
* `d` :  
    reference to a device callback object  

Returns
-------
A handle which must be used to deregister a callback It is recommended to use
one of the RegisterRemovalCallback() helper functions to register a callback.  

Example how to register a C function  

Example how to register a class member function  
";

%feature("docstring") Pylon::Key::RegisterRemovalCallback "

Low Level API: Register a C-function as a removal callback.  

See also: Pylon::IPylonDevice::RegisterRemovalCallback()  

Parameters
----------
* `pDevice` :  
    Pointer to the device that generates callbacks  
* `f` :  
    The function to be called  
";

%feature("docstring") Pylon::Key::RegisterRemovalCallback "

Low Level API: Register a C++-member function as removal callback.  

See also: Pylon::IPylonDevice::RegisterRemovalCallback()  

Parameters
----------
* `pDevice` :  
    Pointer to the device that generates callbacks  
* `c` :  
    The client object  
* `m` :  
    The member function to be called  
";

%feature("docstring") Pylon::Key::PYLON_BASE_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::PYLON_BASE_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::PYLON_BASE_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::PYLON_BASE_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::CreateChunkParser "

Creates a chunk parser used to update those camera object members reflecting the
content of additional data chunks appended to the image data.  

Returns
-------
Pointer to the created chunk parser  

note: Don't try to delete a chunk parser pointer by calling free or delete.
    Instead, use the DestroyChunkParser() method  
";

%feature("docstring") Pylon::Key::PYLON_DEPRECATED "
";

%feature("docstring") Pylon::Key::PYLON_DEPRECATED "
";

%feature("docstring") Pylon::Key::FinishGrab "

Stops grabbing.  

Releases the resources and camera. Pending grab requests are canceled.  
";

%feature("docstring") Pylon::Key::Reset "

Resets the image properties and provides a buffer to hold the image.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The IsSupportedPixelType() method returns true.  
    *   The `width` value must be >= 0 and < _I32_MAX.  
    *   The `height` value must be >= 0 and < _I32_MAX.  

post:  

    *   The properties of the image are changed.  
    *   A buffer large enough to hold the image is provided.  

Throws an exception when the preconditions are not met. Throws an exception when
no buffer with the required size can be provided, e.g. by allocation. The
original representation is preserved on error.  
";

%feature("docstring") Pylon::Key::Reset "

Resets the image properties including user defined PaddingX and provides a
buffer to hold the image.  

Extends the Reset(EPixelType, uint32_t, uint32_t) method with user provided
padding.  

Parameters
----------
* `pixelType` :  
    The pixel type of the new image.  
* `width` :  
    The number of pixels in a row in the new image.  
* `height` :  
    The number of rows in the new image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row.  
* `orientation` :  
    The vertical orientation of the image in the image buffer.  

pre:  

    *   The preconditions of the Reset() method without paddingX parameter
        apply.  
    *   The IsAdditionalPaddingSupported() method returns true.  
";

%feature("docstring") Pylon::Key::IsMonoImage "

Returns true when an image using the given pixel type is monochrome, e.g.
PixelType_Mono8.  
";

%feature("docstring") Pylon::Key::IsRGBA "

Returns true when the pixel type represents an RGBA format.  
";

%feature("docstring") Pylon::Key::ComputePaddingX "

Computes the padding value from row stride in byte.  

Parameters
----------
* `strideBytes` :  
    The stride in byte.  
* `pixelType` :  
    The pixel type.  
* `width` :  
    The number of pixels in a row.  

Returns
-------
Returns the paddingX value for the given stride value (byte aligned).  

pre:  

    *   The value of `strideBytes` must be large enough to contain a line
        described by `pixelType` and `width`.  
    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and <= _I32_MAX.  

Throws an exception when the preconditions are not met.  
";

%feature("docstring") Pylon::Key::IsSupportedPixelType "

Can be used to check whether the pixel type is supported.  

Returns
-------
Returns true if the pixel type is supported.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::Key::ComputeStride "

Computes the stride in byte.  

The stride indicates the number of bytes between the beginning of one row in an
image and the beginning of the next row. For planar pixel types the returned
value represents the stride of a plane.  

The stride in bytes cannot be computed for packed image format when the stride
is not byte aligned and paddingX == 0. If paddingX is larger than zero and the
stride without padding is not byte aligned then the rest of the partially filled
byte is considered as padding, e.g. pixelType = PixelType_Mono12packed, width =
5, paddingX = 10 results in a stride of 18 Bytes (stride without padding is 5 *
BitPerPixel( PixelType_Mono12packed) = 5 * 12 = 60 Bits = 7.5 Bytes).  

See also Pylon::IsPacked().  

Parameters
----------
* `strideBytes` :  
    The stride in byte if it can be computed.  
* `pixelType` :  
    The pixel type.  
* `width` :  
    The number of pixels in a row.  
* `paddingX` :  
    The number of additional bytes at the end of a row (byte aligned).  

Returns
-------
Returns true if the stride can be computed.  

pre: The `width` value must be >= 0 and <= _I32_MAX.  

Throws an exception when the preconditions are not met.  
";

%feature("docstring") Pylon::Key::IsPlanar "

Returns true if images of the pixel type are divided into multiple planes.  
";

%feature("docstring") Pylon::Key::IsBayer "

Returns true when the pixel type represents a Bayer format.  
";

%feature("docstring") Pylon::Key::GetRTThreadPriorityCapabilities "

Queries the range of allowed thread priorities.  
";

%feature("docstring") Pylon::Key::Sfnc_VersionUndefined "

Constant for undefined SFNC version.  
";

%feature("docstring") Pylon::Key::IsRGBPacked "

Returns true if the pixel type is RGB and the pixel values are not byte aligned.  
";

%feature("docstring") Pylon::Key::GetTLNodeMap "

Returns the set of camera related transport layer parameters.  

Returns
-------
Pointer to the GenApi node holding the transport layer parameter. If there are
no transport layer parameters for the device, NULL is returned.  
";

%feature("docstring") Pylon::Key::Sfnc_1_3_0 "

Constant for SFNC version 1.3.0.  
";

%feature("docstring") Pylon::Key::PylonInitialize "

Initializes the pylon runtime system.  

You must call PylonInitialize before calling any other pylon functions. When
finished you must call PylonTerminate to free up all resources used by pylon.  

You can use the helperclass PylonAutoInitTerm to let the compiler call
PylonInitialze and PylonTerminate.  

Just create a local object on the stack in your main function and the
constructor and destructor will call the functions. See PylonAutoInitTerm for a
sample.  

PylonInitialize/PylonTerminate is reference counted. For every call of
PylonInitialize, a call to PylonTerminate is required. The last call to
PylonTerminate will free up all resources.  
";

%feature("docstring") Pylon::Key::Destroy "

Makes the object to destroy itself.  

This is an alternative to destroying it via the IPylonDevice interface. It is
used when the device has been destroyed already.  
";

%feature("docstring") Pylon::Key::IsMonoPacked "

Returns true if the pixel type is Mono and the pixel values are not byte
aligned.  
";

%feature("docstring") Pylon::Key::ComputeBufferSize "

Computes the buffer size in byte.  

Parameters
----------
* `pixelType` :  
    The pixel type.  
* `width` :  
    The number of pixels in a row.  
* `height` :  
    The number of rows in an image.  
* `paddingX` :  
    The number of extra data bytes at the end of each row (byte aligned).  

Returns
-------
The buffer size in byte.  

pre:  

    *   The pixel type must be valid.  
    *   The `width` value must be >= 0 and <= _I32_MAX.  
    *   The `height` value must be >= 0 and <= _I32_MAX.  

Throws an exception when the preconditions are not met.  
";

%feature("docstring") Pylon::Key::GetPylonVersionString "

Returns the version number of pylon as string.  
";

%feature("docstring") Pylon::Key::IsBGRPacked "

Returns true if the pixel type is BGR and the pixel values are not byte aligned.  
";

%feature("docstring") Pylon::Key::GetCurrentThreadIdentifier "

Get current running thread id.  

This wrapper method return the id of the current running thread.  
";

%feature("docstring") Pylon::Key::PrepareGrab "

Prepares grabbing.  

Allocates resources, synchronizes with the camera and locks critical parameter  
";

%feature("docstring") Pylon::Key::DestroyEventAdapter "

Deletes an Event adapter  
";

%feature("docstring") Pylon::Key::make_FunctionCallback "
";

%feature("docstring") Pylon::Key::IsRGB "

Returns true when the pixel type represents an RGB or RGBA format.  
";

%feature("docstring") Pylon::Key::make_MemberFunctionCallback "
";

%feature("docstring") Pylon::Key::CreateEventAdapter "

Creates an Event adapter  
";

%feature("docstring") Pylon::Key::Sfnc_2_1_0 "

Constant for SFNC version 2.1.0.  
";

%feature("docstring") Pylon::Key::SetRTThreadPriority "

Allows to set the realtime thread priority of a thread.  

Typically a thread that receives image data should be set to realtime thread
priorities to reduce jitter and delays. Be aware that such a realtime thread
shouldn't perform time consuming tasks (like image processing). A realtime
thread that is continuously working can cause the whole operating system to be
blocked!  
";

%feature("docstring") Pylon::Key::GetPlanePixelType "

Returns the pixel type of a plane.  
";

%feature("docstring") Pylon::Key::PlaneCount "

Returns number of planes in the image composed of the pixel type.  
";

%feature("docstring") Pylon::Key::RetrieveResult "

Retrieves a grab result from the output queue.  

Returns
-------
When result was available true is returned and and the first result is copied
into the grabresult. Otherwise the grabresult remains unchanged and false is
returned.  
";

%feature("docstring") Pylon::Key::IsOpen "

Retrieve whether the stream grabber is open.  
";

%feature("docstring") Pylon::Key::IsBGR "

Returns true when the pixel type represents a BGR or BGRA format.  
";

%feature("docstring") Pylon::Key::Sfnc_1_2_1 "

Constant for SFNC version 1.2.1.  
";

%feature("docstring") Pylon::Key::IsAdditionalPaddingSupported "

Can be used to check whether the value of PaddingX can be defined by the user.  

Returns
-------
Returns true if the value of PaddingX can be defined by the user.  

Does not throw C++ exceptions.  
";

%feature("docstring") Pylon::Key::DestroyChunkParser "

Deletes a chunk parser.  

Parameters
----------
* `pChunkParser` :  
    Pointer to the chunk parser to be deleted  
";

%feature("docstring") Pylon::Key::GetPixelIncrementX "

Returns the minimum step size expressed in pixels for extracting an AOI.  
";

%feature("docstring") Pylon::Key::DestroySelfReliantChunkParser "

Deletes a self-reliant chunk parser  
";

%feature("docstring") Pylon::Key::IsPackedInLsbFormat "

Returns true if the pixel type is packed in lsb packed format. For lsb packed
format, the data is filled lsb first in the lowest address byte (byte 0)
starting with the first pixel and continued in the lsb of byte 1 (and so on).
See the camera User's Manual or the Pixel Format Naming Convention (PFNC) of the
GenICam standard group for more information.  
";

%feature("docstring") Pylon::Key::GetPixelColorFilter "

Returns the Bayer color filter type.  
";

%feature("docstring") Pylon::Key::GetEventGrabber "

Returns a pointer to an event grabber.  

Event grabbers are used to handle events sent from a camera device.  
";

%feature("docstring") Pylon::Key::PYLON_UTILITY_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::PYLON_UTILITY_3_0_DEPRECATED "
";

%feature("docstring") Pylon::Key::GetCurrentThreadHandle "

Get current running thread handle.  

This wrapper method return the handle of the current running thread.  
";

%feature("docstring") Pylon::Key::GetWaitObject "

Returns the result event object.  

This object is associated with the result queue. The event is signaled when
queue is non-empty  
";

%feature("docstring") Pylon::Key::GetStreamGrabber "

Returns a pointer to a stream grabber.  

Stream grabbers (IStreamGrabber) are the objects used to grab images from a
camera device. A camera device might be able to send image data over more than
one logical channel called stream. A stream grabber grabs data from one single
stream.  

Parameters
----------
* `index` :  
    The number of the grabber to return  

Returns
-------
A pointer to a stream grabber, NULL if index is out of range  
";

%feature("docstring") Pylon::Key::Sfnc_1_5_0 "

Constant for SFNC version 1.5.0.  
";

// File: namespace_pylon_1_1_key.xml

%feature("docstring") Pylon::Key::ManufacturerInfoKey "

Identifies the manufacturer info.  
";

// File: namespace_pylon_1_1_pylon_private.xml

// File: ___image_format_converter_params_8h.xml

// File: ___instant_camera_params_8h.xml

// File: _acquire_continuous_configuration_8h.xml

// File: _acquire_single_frame_configuration_8h.xml

// File: _avi_compression_options_8h.xml

// File: _avi_writer_8h.xml

// File: _buffer_factory_8h.xml

// File: _callback_8h.xml

// File: _camera_event_handler_8h.xml

// File: _chunk_parser_8h.xml

// File: _configuration_event_handler_8h.xml

// File: _container_8h.xml

// File: _device_8h.xml

// File: _device_access_mode_8h.xml

// File: _device_class_8h.xml

// File: _device_factory_8h.xml

// File: _device_info_8h.xml

// File: _event_adapter_8h.xml

// File: _event_grabber_8h.xml

// File: _event_grabber_proxy_8h.xml

// File: _feature_persistence_8h.xml

// File: _grab_result_data_8h.xml

// File: _grab_result_ptr_8h.xml

// File: gtl_8h.xml

// File: gtlgen_8h.xml

// File: gtlstatic_8h.xml

// File: _image_8h.xml

// File: _image_event_handler_8h.xml

// File: _image_format_8h.xml

// File: _image_format_converter_8h.xml

// File: _image_persistence_8h.xml

// File: _info_8h.xml

// File: _instant_camera_8h.xml

// File: _instant_camera_array_8h.xml

// File: _interface_info_8h.xml

// File: _node_map_proxy_8h.xml

// File: _payload_type_8h.xml

// File: _pixel_8h.xml

// File: _pixel_data_8h.xml

// File: _pixel_format_converter_8h.xml

// File: _pixel_format_converter_bayer_8h.xml

// File: _pixel_format_converter_bayer16_8h.xml

// File: _pixel_format_converter_gamma_8h.xml

// File: _pixel_format_converter_gamma_packed_8h.xml

// File: _pixel_format_converter_mono_packed_8h.xml

// File: _pixel_format_converter_mono_x_x_8h.xml

// File: _pixel_format_converter_r_g_b_8h.xml

// File: _pixel_format_converter_truncate_8h.xml

// File: _pixel_format_converter_truncate_packed_8h.xml

// File: _pixel_format_converter_y_u_v422_8h.xml

// File: _pixel_type_8h.xml

// File: _pixel_type_mapper_8h.xml

// File: _platform_8h.xml

// File: _pylon_base_8h.xml

// File: _pylon_bitmap_image_8h.xml

// File: _pylon_device_proxy_8h.xml

// File: _pylon_g_u_i_8h.xml

// File: _pylon_g_u_i_includes_8h.xml

// File: _pylon_image_8h.xml

// File: _pylon_image_base_8h.xml

// File: _pylon_includes_8h.xml

// File: _pylon_linkage_8h.xml

// File: _pylon_utility_8h.xml

// File: _pylon_utility_includes_8h.xml

// File: _pylon_version_8h.xml

// File: _pylon_version_info_8h.xml

// File: _pylon_version_number_8h.xml

// File: _result_8h.xml

// File: _result_image_8h.xml

// File: _reusable_image_8h.xml

// File: _sfnc_version_8h.xml

// File: _software_trigger_configuration_8h.xml

// File: stdinclude_8h.xml

// File: _stream_grabber_8h.xml

// File: _stream_grabber_proxy_8h.xml

// File: _thread_priority_8h.xml

// File: _tl_factory_8h.xml

// File: _tl_info_8h.xml

// File: _transport_layer_8h.xml

// File: _type_mappings_8h.xml

// File: _wait_object_8h.xml

// File: _wait_objects_8h.xml

// File: _xml_file_provider_8h.xml

// File: group___pylon___instant_camera_api_generic.xml

// File: group___pylon___image_handling_support.xml

// File: group___pylon___transport_layer.xml

// File: dir_a9acf0e9773b052fcedd0b44a055946b.xml

// File: dir_b2c3bdeda402f0da6e3083aff1b68a31.xml

// File: dir_f8a07b22e547eb943772dc99a1be8120.xml

// File: dir_7b7f5717394725475e38cdf3cbd3c0c1.xml

// File: dir_5fc5c320b869e08468826ac0c3c212c5.xml

