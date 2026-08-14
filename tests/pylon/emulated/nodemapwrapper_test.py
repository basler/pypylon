from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon, genicam
import unittest


class NodeMapWrapperTestSuite(PylonEmuTestCase):
    def test_instantcamera_wrappers_present(self):
        """InstantCamera uses NodeMapWrapper for its parameters"""
        camera = self.create_first()
        camera.Open()

        self.assertIsInstance(camera.GetNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(camera.GetTLNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(camera.GetStreamGrabberNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(camera.GetEventGrabberNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(camera.GetInstantCameraNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(camera.NodeMap, pylon.NodeMapWrapper)
        self.assertIsInstance(camera.TLNodeMap, pylon.NodeMapWrapper)
        self.assertIsInstance(camera.StreamGrabberNodeMap, pylon.NodeMapWrapper)
        self.assertIsInstance(camera.EventGrabberNodeMap, pylon.NodeMapWrapper)
        self.assertIsInstance(camera.InstantCameraNodeMap, pylon.NodeMapWrapper)
        result = camera.GrabOne(1000)
        self.assertIsInstance(result.GetChunkDataNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(result.ChunkDataNodeMap, pylon.NodeMapWrapper)
        camera.Close()

    def test_format_converter_wrappers_present(self):
        """ImageFormatConverter uses NodeMapWrapper for its parameters"""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.GetNodeMap(), pylon.NodeMapWrapper)

    # ------------------------------------------------------------------
    # Tests that NodeMapWrapper.GetNode() maps INode* to Pylon C*Parameter
    # types instead of the raw genicam interface types returned by a plain
    # INodeMap.
    # ------------------------------------------------------------------

    def test_getnode_integer_returns_integer_parameter(self):
        """intfIInteger  ->  pylon.IntegerParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainRaw")
        self.assertIsInstance(node, pylon.IntegerParameter)
        camera.Close()

    def test_getnode_boolean_returns_boolean_parameter(self):
        """intfIBoolean  ->  pylon.BooleanParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("ReverseX")
        self.assertIsInstance(node, pylon.BooleanParameter)
        camera.Close()

    def test_getnode_command_returns_command_parameter(self):
        """intfICommand  ->  pylon.CommandParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("AcquisitionStart")
        self.assertIsInstance(node, pylon.CommandParameter)
        camera.Close()

    def test_getnode_float_returns_float_parameter(self):
        """intfIFloat  ->  pylon.FloatParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("Gain")
        self.assertIsInstance(node, pylon.FloatParameter)
        camera.Close()

    def test_getnode_string_returns_string_parameter(self):
        """intfIString  ->  pylon.StringParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("DeviceVendorName")
        self.assertIsInstance(node, pylon.StringParameter)
        camera.Close()

    def test_getnode_enumeration_returns_enum_parameter(self):
        """intfIEnumeration  ->  pylon.EnumParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainAuto")
        self.assertIsInstance(node, pylon.EnumParameter)
        camera.Close()

    def test_getnode_register_returns_array_parameter(self):
        """intfIRegister  ->  pylon.ArrayParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("BslImageCompressionBCBDescriptor")
        self.assertIsInstance(node, pylon.ArrayParameter)
        camera.Close()

    def test_getnode_category_returns_category_parameter(self):
        """intfICategory  ->  pylon.CategoryParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("Root")
        self.assertIsInstance(node, pylon.CategoryParameter)
        camera.Close()

    def test_getnode_enumentry_returns_enum_entry_parameter(self):
        """intfIEnumEntry  ->  pylon.EnumEntryParameter"""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("EnumEntry_GainAuto_Off")
        self.assertIsInstance(node, pylon.EnumEntryParameter)
        camera.Close()

    def test_camera_attribute_access_maps_to_parameter_types(self):
        """Attribute access via __getattr__ delegates to GetNode and returns
        Pylon *Parameter types for all mapped interface types."""
        camera = self.create_first()
        camera.Open()
        self.assertIsInstance(camera.GainRaw, pylon.IntegerParameter)
        self.assertIsInstance(camera.ReverseX, pylon.BooleanParameter)
        self.assertIsInstance(camera.AcquisitionStart, pylon.CommandParameter)
        self.assertIsInstance(camera.Gain, pylon.FloatParameter)
        self.assertIsInstance(camera.DeviceVendorName, pylon.StringParameter)
        self.assertIsInstance(camera.GainAuto, pylon.EnumParameter)
        self.assertIsInstance(camera.BslImageCompressionBCBDescriptor, pylon.ArrayParameter)
        camera.Close()

    def test_nodemap_attribute_access_maps_to_parameter_types(self):
        """Attribute access via __getattr__ delegates to GetNode and returns
        Pylon *Parameter types for all mapped interface types."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        self.assertIsInstance(nm.GainRaw, pylon.IntegerParameter)
        self.assertIsInstance(nm.ReverseX, pylon.BooleanParameter)
        self.assertIsInstance(nm.AcquisitionStart, pylon.CommandParameter)
        self.assertIsInstance(nm.Gain, pylon.FloatParameter)
        self.assertIsInstance(nm.DeviceVendorName, pylon.StringParameter)
        self.assertIsInstance(nm.GainAuto, pylon.EnumParameter)
        self.assertIsInstance(nm.BslImageCompressionBCBDescriptor, pylon.ArrayParameter)
        camera.Close()

    def test_getnodes_returns_pylon_parameter_types(self):
        """GetNodes() via NodeMapWrapper returns Pylon *Parameter types for
        the mapped interface types (Integer, Boolean, Command, Float, String,
        Enumeration, Register, EnumEntry, Category, Port) and genicam fallback
        types only for remaining unrecognised interface types."""
        camera = self.create_first()
        camera.Open()
        nodes = camera.GetNodeMap().GetNodes()

        # Build a name->node dict for easy lookup
        by_name = {n.GetNode().GetName(): n for n in nodes}

        # Mapped types -> Pylon *Parameter
        self.assertIsInstance(by_name["GainRaw"], pylon.IntegerParameter)
        self.assertIsInstance(by_name["ReverseX"], pylon.BooleanParameter)
        self.assertIsInstance(by_name["AcquisitionStart"], pylon.CommandParameter)
        self.assertIsInstance(by_name["Gain"], pylon.FloatParameter)
        self.assertIsInstance(by_name["DeviceVendorName"], pylon.StringParameter)
        self.assertIsInstance(by_name["GainAuto"], pylon.EnumParameter)
        self.assertIsInstance(by_name["BslImageCompressionBCBDescriptor"], pylon.ArrayParameter)

        # Fallback types -> genicam interface types (IPort etc.)
        # Category -> pylon.CategoryParameter (no longer a fallback)
        self.assertIsInstance(by_name["Root"], pylon.CategoryParameter)
        # EnumEntry -> pylon.EnumEntryParameter (no longer a fallback)
        self.assertIsInstance(by_name["EnumEntry_GainAuto_Off"], pylon.EnumEntryParameter)

        # EnumEntry -> pylon.EnumEntryParameter (note: try to avoid using the enum entry directly)
        self.assertIsInstance(by_name["EnumEntry_GainAuto_Off"], pylon.EnumEntryParameter)

        camera.Close()

    def test_parameter_types_not_returned_by_raw_genicam_nodemap(self):
        """Contrast test: a raw genicam INodeMap (not wrapped by NodeMapWrapper)
        returns plain genicam interface types for GetNode(), NOT Pylon *Parameter
        objects.  This confirms that NodeMapWrapper is responsible for the
        type upgrade."""
        camera = self.create_first()
        camera.Open()

        # camera.GetNodeMap() returns an NodeMapWrapper; call _Get() to obtain
        # the underlying raw INodeMap pointer and cast it back via SWIG so that
        # the genicam typemaps are in effect.
        raw_nm = camera.GetNodeMap()._Get()

        # Raw INodeMap.GetNode returns genicam interface types
        self.assertIsInstance(raw_nm.GetNode("GainRaw"), genicam.IInteger)
        self.assertIsInstance(raw_nm.GetNode("ReverseX"), genicam.IBoolean)
        self.assertIsInstance(raw_nm.GetNode("AcquisitionStart"), genicam.ICommand)
        self.assertIsInstance(raw_nm.GetNode("Gain"), genicam.IFloat)
        self.assertIsInstance(raw_nm.GetNode("DeviceVendorName"), genicam.IString)
        self.assertIsInstance(raw_nm.GetNode("GainAuto"), genicam.IEnumeration)

        # And NOT Pylon *Parameter objects
        self.assertNotIsInstance(raw_nm.GetNode("GainRaw"), pylon.IntegerParameter)
        self.assertNotIsInstance(raw_nm.GetNode("ReverseX"), pylon.BooleanParameter)
        self.assertNotIsInstance(raw_nm.GetNode("Gain"), pylon.FloatParameter)

        camera.Close()

    # ------------------------------------------------------------------
    # Tests that NodeMapWrapper correctly exposes IDeviceInfo methods,
    # delegating to the underlying INodeMap which also implements IDeviceInfo.
    # ------------------------------------------------------------------

    def test_ideviceinfo_get_device_info_returns_ideviceinfo(self):
        """GetDeviceInfo() on NodeMapWrapper returns a genicam.IDeviceInfo instance"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        di = nm.GetDeviceInfo()
        self.assertIsInstance(di, genicam.IDeviceInfo)
        camera.Close()

    def test_ideviceinfo_string_properties(self):
        """IDeviceInfo string properties are correctly delegated through NodeMapWrapper"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        self.assertEqual(nm.GetModelName(), "BaslerCamEmu")
        self.assertEqual(nm.GetVendorName(), "Basler")
        self.assertIsInstance(nm.GetToolTip(), str)
        self.assertIsInstance(nm.GetStandardNameSpace(), str)
        self.assertIsInstance(nm.GetProductGuid(), str)
        self.assertIsInstance(nm.GetVersionGuid(), str)

        # Values must also be consistent when accessed through wrapped node map GetDeviceInfo()
        di = nm._Get().GetDeviceInfo()
        self.assertEqual(di.GetModelName(), nm.GetModelName())
        self.assertEqual(di.GetVendorName(), nm.GetVendorName())
        self.assertEqual(di.GetToolTip(), nm.GetToolTip())
        self.assertEqual(di.GetStandardNameSpace(), nm.GetStandardNameSpace())
        self.assertEqual(di.GetProductGuid(), nm.GetProductGuid())
        self.assertEqual(di.GetVersionGuid(), nm.GetVersionGuid())

        camera.Close()

    def test_ideviceinfo_version_properties(self):
        """IDeviceInfo version structs are correctly delegated through NodeMapWrapper"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        # GetGenApiVersion returns (Version, build:int)
        genapi_ver, build = nm.GetGenApiVersion()
        self.assertIsInstance(genapi_ver, genicam.Version)
        self.assertIsInstance(build, int)
        self.assertGreater(genapi_ver.Major, 0)

        # GetSchemaVersion returns a Version struct
        schema_ver = nm.GetSchemaVersion()
        self.assertIsInstance(schema_ver, genicam.Version)
        self.assertGreater(schema_ver.Major, 0)

        # GetDeviceVersion returns a Version struct
        device_ver = nm.GetDeviceVersion()
        self.assertIsInstance(device_ver, genicam.Version)
        self.assertGreater(device_ver.Major, 0)

        # Values must match those returned through GetDeviceInfo()
        di = nm.GetDeviceInfo()
        di_genapi_ver, di_build = di.GetGenApiVersion()
        self.assertEqual(di_genapi_ver.Major,    genapi_ver.Major)
        self.assertEqual(di_genapi_ver.Minor,    genapi_ver.Minor)
        self.assertEqual(di_genapi_ver.SubMinor, genapi_ver.SubMinor)
        self.assertEqual(di_build, build)

        di_schema_ver = di.GetSchemaVersion()
        self.assertEqual(di_schema_ver.Major,    schema_ver.Major)
        self.assertEqual(di_schema_ver.Minor,    schema_ver.Minor)
        self.assertEqual(di_schema_ver.SubMinor, schema_ver.SubMinor)

        di_device_ver = di.GetDeviceVersion()
        self.assertEqual(di_device_ver.Major,    device_ver.Major)
        self.assertEqual(di_device_ver.Minor,    device_ver.Minor)
        self.assertEqual(di_device_ver.SubMinor, device_ver.SubMinor)

        camera.Close()

    # ------------------------------------------------------------------
    # Tests for GetNodeMapType() / NodeMapType property
    # ------------------------------------------------------------------

    def test_getnodemap_type_camera(self):
        """GetNodeMap() wrapper reports NodeMapType_Camera"""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        self.assertEqual(nm.GetNodeMapType(), pylon.NodeMapType_Camera)
        camera.Close()

    def test_nodemap_type_property_camera(self):
        """NodeMapType property equals NodeMapType_Camera for the camera nodemap"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().NodeMapType, pylon.NodeMapType_Camera)
        camera.Close()

    def test_getnodemap_type_stream_grabber(self):
        """GetStreamGrabberNodeMap() wrapper reports NodeMapType_StreamGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().GetNodeMapType(), pylon.NodeMapType_StreamGrabber)
        camera.Close()

    def test_nodemap_type_property_stream_grabber(self):
        """NodeMapType property equals NodeMapType_StreamGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().NodeMapType, pylon.NodeMapType_StreamGrabber)
        camera.Close()

    def test_getnodemap_type_transport_layer(self):
        """GetTLNodeMap() wrapper reports NodeMapType_DeviceTransportLayer"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().GetNodeMapType(), pylon.NodeMapType_DeviceTransportLayer)
        camera.Close()

    def test_nodemap_type_property_transport_layer(self):
        """NodeMapType property equals NodeMapType_DeviceTransportLayer"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().NodeMapType, pylon.NodeMapType_DeviceTransportLayer)
        camera.Close()

    def test_getnodemap_type_event_grabber(self):
        """GetEventGrabberNodeMap() wrapper reports NodeMapType_EventGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().GetNodeMapType(), pylon.NodeMapType_EventGrabber)
        camera.Close()

    def test_nodemap_type_property_event_grabber(self):
        """NodeMapType property equals NodeMapType_EventGrabber"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().NodeMapType, pylon.NodeMapType_EventGrabber)
        camera.Close()

    def test_getnodemap_type_instant_camera(self):
        """GetInstantCameraNodeMap() wrapper reports NodeMapType_InstantCamera"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().GetNodeMapType(), pylon.NodeMapType_InstantCamera)
        camera.Close()

    def test_nodemap_type_property_instant_camera(self):
        """NodeMapType property equals NodeMapType_InstantCamera"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().NodeMapType, pylon.NodeMapType_InstantCamera)
        camera.Close()

    def test_getnodemap_type_image_format_converter(self):
        """ImageFormatConverter nodemap wrapper reports NodeMapType_ImageFormatConverter"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().GetNodeMapType(), pylon.NodeMapType_ImageFormatConverter)

    def test_nodemap_type_property_image_format_converter(self):
        """NodeMapType property equals NodeMapType_ImageFormatConverter"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().NodeMapType, pylon.NodeMapType_ImageFormatConverter)

    def test_getnodemap_type_chunk_data(self):
        """ChunkDataNodeMap wrapper reports NodeMapType_ChunkData"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.GetChunkDataNodeMap().GetNodeMapType(), pylon.NodeMapType_ChunkData)
        camera.Close()

    def test_nodemap_type_property_chunk_data(self):
        """NodeMapType property equals NodeMapType_ChunkData for chunk-data nodemap"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.ChunkDataNodeMap.NodeMapType, pylon.NodeMapType_ChunkData)
        camera.Close()

    # ------------------------------------------------------------------
    # Tests for GetNodeMapTypeString() / NodeMapTypeString property
    # ------------------------------------------------------------------

    def test_getnodemap_type_string_camera(self):
        """GetNodeMapTypeString() returns 'Camera' for the camera nodemap"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().GetNodeMapTypeString(), "Camera")
        camera.Close()

    def test_nodemap_type_string_property_camera(self):
        """NodeMapTypeString property returns 'Camera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetNodeMap().NodeMapTypeString, "Camera")
        camera.Close()

    def test_getnodemap_type_string_stream_grabber(self):
        """GetNodeMapTypeString() returns 'StreamGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().GetNodeMapTypeString(), "StreamGrabber")
        camera.Close()

    def test_nodemap_type_string_property_stream_grabber(self):
        """NodeMapTypeString property returns 'StreamGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetStreamGrabberNodeMap().NodeMapTypeString, "StreamGrabber")
        camera.Close()

    def test_getnodemap_type_string_transport_layer(self):
        """GetNodeMapTypeString() returns 'DeviceTransportLayer'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().GetNodeMapTypeString(), "DeviceTransportLayer")
        camera.Close()

    def test_nodemap_type_string_property_transport_layer(self):
        """NodeMapTypeString property returns 'DeviceTransportLayer'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetTLNodeMap().NodeMapTypeString, "DeviceTransportLayer")
        camera.Close()

    def test_getnodemap_type_string_event_grabber(self):
        """GetNodeMapTypeString() returns 'EventGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().GetNodeMapTypeString(), "EventGrabber")
        camera.Close()

    def test_nodemap_type_string_property_event_grabber(self):
        """NodeMapTypeString property returns 'EventGrabber'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetEventGrabberNodeMap().NodeMapTypeString, "EventGrabber")
        camera.Close()

    def test_getnodemap_type_string_instant_camera(self):
        """GetNodeMapTypeString() returns 'InstantCamera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().GetNodeMapTypeString(), "InstantCamera")
        camera.Close()

    def test_nodemap_type_string_property_instant_camera(self):
        """NodeMapTypeString property returns 'InstantCamera'"""
        camera = self.create_first()
        camera.Open()
        self.assertEqual(camera.GetInstantCameraNodeMap().NodeMapTypeString, "InstantCamera")
        camera.Close()

    def test_getnodemap_type_string_image_format_converter(self):
        """GetNodeMapTypeString() returns 'ImageFormatConverter'"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().GetNodeMapTypeString(), "ImageFormatConverter")

    def test_nodemap_type_string_property_image_format_converter(self):
        """NodeMapTypeString property returns 'ImageFormatConverter'"""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(converter.GetNodeMap().NodeMapTypeString, "ImageFormatConverter")

    def test_getnodemap_type_string_chunk_data(self):
        """GetNodeMapTypeString() returns 'ChunkData'"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.GetChunkDataNodeMap().GetNodeMapTypeString(), "ChunkData")
        camera.Close()

    def test_nodemap_type_string_property_chunk_data(self):
        """NodeMapTypeString property returns 'ChunkData'"""
        camera = self.create_first()
        camera.Open()
        result = camera.GrabOne(1000)
        self.assertEqual(result.ChunkDataNodeMap.NodeMapTypeString, "ChunkData")
        camera.Close()

    # ------------------------------------------------------------------
    # PlaceholderParameter returned for non-existent nodes
    # ------------------------------------------------------------------

    def test_getnode_nonexistent_returns_placeholder(self):
        """GetNode for an absent node returns a PlaceholderParameter."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("ThisNodeDoesNotExist_XYZ")
        self.assertIsInstance(node, pylon.PlaceholderParameter)
        self.assertFalse(node.IsValid())
        camera.Close()

    def test_getnode_nonexistent_path_format(self):
        """PlaceholderParameter path is '<NodeMapTypeString>/<NodeName>'."""
        camera = self.create_first()
        camera.Open()
        absent = "ThisNodeDoesNotExist_XYZ"
        node = camera.GetNodeMap().GetNode(absent)
        path = node.GetPath()
        self.assertIn(absent, path)
        self.assertIn("/", path)
        nodemap_type, node_name = path.split("/", 1)
        self.assertEqual("Camera", nodemap_type)
        self.assertEqual(absent, node_name)
        camera.Close()

    def test_getnode_nonexistent_path_reflects_nodemap_type_camera(self):
        """Placeholder path prefix equals 'Camera' for the camera nodemap."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertTrue(node.GetPath().startswith("Camera/"))
        camera.Close()

    def test_getnode_nonexistent_path_reflects_nodemap_type_stream_grabber(self):
        """Placeholder path prefix equals 'StreamGrabber' for the stream-grabber nodemap."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetStreamGrabberNodeMap().GetNode("NoSuchNode")
        self.assertTrue(node.GetPath().startswith("StreamGrabber/"))
        camera.Close()

    def test_getnode_nonexistent_path_reflects_nodemap_type_transport_layer(self):
        """Placeholder path prefix equals 'DeviceTransportLayer' for the TL nodemap."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetTLNodeMap().GetNode("NoSuchNode")
        self.assertTrue(node.GetPath().startswith("DeviceTransportLayer/"))
        camera.Close()

    def test_getnode_nonexistent_path_property(self):
        """The Path property on a nodemap-sourced PlaceholderParameter equals GetPath()."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertEqual(node.GetPath(), node.Path)
        camera.Close()

    def test_getnode_nonexistent_placeholder_is_invalid(self):
        """A nodemap-sourced PlaceholderParameter is never valid."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertFalse(node.IsValid())
        self.assertFalse(node.IsReadable())
        self.assertFalse(node.IsWritable())
        self.assertEqual(genicam.NI, node.GetAccessMode())
        camera.Close()

    def test_getnode_nonexistent_set_value_raises_with_path(self):
        """SetValue on a nodemap-sourced PlaceholderParameter raises with the path in the message."""
        camera = self.create_first()
        camera.Open()
        absent = "NoSuchNode"
        node = camera.GetNodeMap().GetNode(absent)
        with self.assertRaises(pylon.LogicalErrorException) as ctx:
            node.SetValue(42)
        self.assertIn(absent, str(ctx.exception))
        camera.Close()

    def test_getnode_nonexistent_try_set_value_returns_false(self):
        """TrySetValue on a nodemap-sourced PlaceholderParameter returns False without raising."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertFalse(node.TrySetValue(42))
        self.assertFalse(node.TrySetValue("Off"))
        self.assertFalse(node.TrySetValue(True))
        camera.Close()

    def test_getnode_nonexistent_try_execute_returns_false(self):
        """TryExecute on a nodemap-sourced PlaceholderParameter returns False without raising."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertFalse(node.TryExecute())
        camera.Close()

    def test_getnode_nonexistent_try_set_to_maximum_returns_false(self):
        """TrySetToMaximum and TrySetToMinimum on a PlaceholderParameter return False."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertFalse(node.TrySetToMaximum())
        self.assertFalse(node.TrySetToMinimum())
        camera.Close()

    def test_getnode_nonexistent_get_value_or_default(self):
        """GetValueOrDefault on a nodemap-sourced PlaceholderParameter returns the default."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("NoSuchNode")
        self.assertEqual(99,      node.GetValueOrDefault(99))
        self.assertEqual("Off",   node.GetValueOrDefault("Off"))
        self.assertAlmostEqual(1.5, node.GetValueOrDefault(1.5))
        camera.Close()

    def test_getnode_nonexistent_to_string_or_default(self):
        """ToStringOrDefault on a nodemap-sourced PlaceholderParameter returns the default."""
        camera = self.create_first()
        camera.Open()
        node = camera.NoSuchNode
        self.assertEqual("default", node.ToStringOrDefault("default"))
        camera.Close()

    def test_getnode_existing_node_not_a_placeholder(self):
        """GetNode for an existing node never returns a PlaceholderParameter."""
        camera = self.create_first()
        camera.Open()
        node = camera.GetNodeMap().GetNode("GainRaw")
        self.assertNotIsInstance(node, pylon.PlaceholderParameter)
        self.assertTrue(node.IsValid())
        camera.Close()

    # ------------------------------------------------------------------
    # Tests for Contains()
    # ------------------------------------------------------------------

    def test_contains_returns_true_for_existing_node(self):
        """Contains() returns True for a node that exists in the nodemap."""
        camera = self.create_first()
        camera.Open()
        self.assertTrue(camera.GetNodeMap().Contains("GainRaw"))
        camera.Close()

    def test_contains_returns_false_for_missing_node(self):
        """Contains() returns False for a node that does not exist in the nodemap."""
        camera = self.create_first()
        camera.Open()
        self.assertFalse(camera.GetNodeMap().Contains("ThisNodeDoesNotExist_XYZ"))
        camera.Close()

    def test_to_parameter(self):
        """ToParameter wraps raw genicam nodes into the matching Pylon *Parameter type."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()

        # Standard value-bearing types
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainRaw").GetNode()), pylon.IntegerParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainRaw")),           pylon.IntegerParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("ReverseX")),          pylon.BooleanParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("AcquisitionStart")),  pylon.CommandParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("Gain")),              pylon.FloatParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("DeviceVendorName")),  pylon.StringParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("GainAuto")),          pylon.EnumParameter)

        # Special-purpose structural types
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("Root")),                   pylon.CategoryParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("EnumEntry_GainAuto_Off")), pylon.EnumEntryParameter)
        self.assertIsInstance(pylon.ToParameter(raw_nm.GetNode("Device")),                 pylon.PortParameter)

        camera.Close()

    def test_to_parameter_none_returns_placeholder_parameter(self):
        """ToParameter(None) returns a PlaceholderParameter (permanently-invalid sentinel)."""
        result = pylon.ToParameter(None)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, pylon.PlaceholderParameter)
        self.assertFalse(result.IsValid())

    def test_to_parameter_unknown_type_returns_placeholder_parameter(self):
        """ToParameter() with an unrecognised type returns a PlaceholderParameter."""
        result = pylon.ToParameter(42)
        self.assertIsInstance(result, pylon.PlaceholderParameter)
        self.assertFalse(result.IsValid())

    def test_to_parameter_base_parameter_is_specialised(self):
        """ToParameter() specialises a base Parameter into the correct subtype."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        base_param = pylon.Parameter(nm.GetNode("GainRaw").GetNode())
        result = pylon.ToParameter(base_param)
        self.assertIsInstance(result, pylon.IntegerParameter)

        camera.Close()

    def test_to_parameter_inode_falls_back_to_base_parameter_when_mapping_not_available(self):
        """ToParameter(INode) falls back to base Parameter when _node_to_specific finds no matching interface constant."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        inode = raw_nm.GetNode("GainRaw").GetNode()

        original_intf_iinteger = genicam.intfIInteger
        try:
            genicam.intfIInteger = -999999
            result = pylon.ToParameter(inode)
        finally:
            genicam.intfIInteger = original_intf_iinteger
            camera.Close()

        self.assertIsInstance(result, pylon.Parameter)
        self.assertNotIsInstance(result, pylon.IntegerParameter)
        self.assertTrue(result.IsValid())
        self.assertEqual(result.GetNode().GetName(), "GainRaw")

    def test_to_parameter_base_parameter_remains_base_when_mapping_not_available(self):
        """ToParameter(base Parameter) returns the same base object if _node_to_specific cannot specialise it."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        base_param = pylon.Parameter(raw_nm.GetNode("GainRaw").GetNode())

        original_intf_iinteger = genicam.intfIInteger
        try:
            genicam.intfIInteger = -999999
            result = pylon.ToParameter(base_param)
        finally:
            genicam.intfIInteger = original_intf_iinteger
            camera.Close()

        self.assertIs(result, base_param)
        self.assertIsInstance(result, pylon.Parameter)
        self.assertNotIsInstance(result, pylon.IntegerParameter)
        self.assertTrue(result.IsValid())

    def test_to_parameter_specific_parameter_kept_unchanged(self):
        """ToParameter() returns a specific Parameter subclass unchanged."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()

        int_param = pylon.IntegerParameter(nm.GetNode("GainRaw").GetNode())
        result = pylon.ToParameter(int_param)
        self.assertIs(result, int_param)

        camera.Close()

    def test_to_parameter_invalid_base_parameter_returned_as_is(self):
        """ToParameter() returns an invalid (unattached) base Parameter unchanged."""
        base_param = pylon.Parameter()
        result = pylon.ToParameter(base_param)
        self.assertIsInstance(result, pylon.Parameter)
        self.assertIs(result, base_param)

    def test_to_parameter_placeholder_parameter_returned_as_is(self):
        """ToParameter() returns a PlaceholderParameter unchanged."""
        placeholder = pylon.PlaceholderParameter("Camera/NoSuchNode")
        result = pylon.ToParameter(placeholder)
        self.assertIs(result, placeholder)

    def test_to_parameter_category_node(self):
        """ToParameter() wraps a category INode into a CategoryParameter."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        result = pylon.ToParameter(raw_nm.GetNode("Root"))
        self.assertIsInstance(result, pylon.CategoryParameter)
        camera.Close()

    def test_to_parameter_enum_entry_node(self):
        """ToParameter() wraps an enum-entry INode into an EnumEntryParameter."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        result = pylon.ToParameter(raw_nm.GetNode("EnumEntry_GainAuto_Off"))
        self.assertIsInstance(result, pylon.EnumEntryParameter)
        camera.Close()

    def test_to_parameter_port_node(self):
        """ToParameter() wraps a port INode into a PortParameter."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        result = pylon.ToParameter(raw_nm.GetNode("Device"))
        self.assertIsInstance(result, pylon.PortParameter)
        camera.Close()

    def test_to_parameter_register_node(self):
        """ToParameter() wraps a register INode into an ArrayParameter."""
        camera = self.create_first()
        camera.Open()
        raw_nm = camera.GetNodeMap()._Get()
        result = pylon.ToParameter(raw_nm.GetNode("BslImageCompressionBCBDescriptor"))
        self.assertIsInstance(result, pylon.ArrayParameter)
        camera.Close()

    def test_to_parameter_port_node_via_get_node(self):
        """ToParameter() reaches _node_to_specific's intfIPort branch.

        genicam's native INodeMap.GetNode()/GetNodes() auto-downcast any
        Port-interface node directly to genicam.IPort (never genicam.INode),
        so ToParameter() takes its separate isinstance(val, IPort) shortcut
        and never reaches _node_to_specific for such nodes (see
        test_to_parameter_port_node above). pylon's own Parameter.GetNode(),
        however, returns a plain, un-downcast INode whose
        GetPrincipalInterfaceType() is still intfIPort, which correctly
        dispatches through _node_to_specific.
        """
        camera = self.create_first()
        camera.Open()
        port_param = camera.GetNodeMap().GetNode("Device")
        self.assertIsInstance(port_param, pylon.PortParameter)
        node = port_param.GetNode()
        self.assertIsInstance(node, genicam.INode)
        self.assertNotIsInstance(node, genicam.IPort)
        self.assertEqual(node.GetPrincipalInterfaceType(), genicam.intfIPort)
        result = pylon.ToParameter(node)
        self.assertIsInstance(result, pylon.PortParameter)
        camera.Close()

    def test_to_parameter_matches_nodemap_wrapper_dispatch(self):
        """ToParameter and NodeMapWrapper.GetNode agree on the returned type for all key nodes."""
        camera = self.create_first()
        camera.Open()
        nm      = camera.GetNodeMap()
        raw_nm  = nm._Get()

        pairs = [
            ("GainRaw",                         pylon.IntegerParameter),
            ("ReverseX",                        pylon.BooleanParameter),
            ("AcquisitionStart",                pylon.CommandParameter),
            ("Gain",                            pylon.FloatParameter),
            ("DeviceVendorName",                pylon.StringParameter),
            ("GainAuto",                        pylon.EnumParameter),
            ("Root",                            pylon.CategoryParameter),
            ("EnumEntry_GainAuto_Off",          pylon.EnumEntryParameter),
            ("Device",                          pylon.PortParameter),
        ]
        for name, expected_type in pairs:
            with self.subTest(node=name):
                via_wrapper    = nm.GetNode(name)
                via_to_param   = pylon.ToParameter(raw_nm.GetNode(name))
                self.assertIsInstance(via_wrapper,  expected_type, f"wrapper mismatch for {name}")
                self.assertIsInstance(via_to_param, expected_type, f"ToParameter mismatch for {name}")

        camera.Close()

    # ------------------------------------------------------------------
    # Construction / abstract guard
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_construction_raises(self):
        """NodeMapWrapper cannot be instantiated directly — it is abstract."""
        with self.assertRaises(AttributeError):
            pylon.NodeMapWrapper()

    # ------------------------------------------------------------------
    # InvalidateNodes
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_invalidate_nodes(self):
        """InvalidateNodes() does not raise and the nodemap remains usable afterwards."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        nm.InvalidateNodes()
        self.assertTrue(nm.Contains("GainRaw"))
        camera.Close()

    # ------------------------------------------------------------------
    # Connect
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_connect(self):
        """Connect() attaches a custom CPortImpl to a named port in the nodemap."""
        class _SimplePort(genicam.CPortImpl):
            def __init__(self):
                genicam.CPortImpl.__init__(self)
                self._mem = bytearray(1024)
            def Read(self, address, length):
                return bytes(self._mem[address:address + length])
            def Write(self, address, data):
                self._mem[address:address + len(data)] = data
            def GetAccessMode(self):
                return genicam.RW

        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        port = _SimplePort()
        nm.Connect(port, "Device")
        camera.Close()

    # ------------------------------------------------------------------
    # NewNodeWriteConcatenator / ConcatenatedWrite
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_new_node_write_concatenator(self):
        """NewNodeWriteConcatenator() returns a non-None concatenator object."""
        camera = self.create_first()
        camera.Open()
        conc = camera.GetNodeMap().NewNodeWriteConcatenator()
        self.assertIsNotNone(conc)
        camera.Close()

    def test_nodemap_wrapper_concatenated_write(self):
        """ConcatenatedWrite() executes a concatenator without raising."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        conc = nm.NewNodeWriteConcatenator()
        nm.ConcatenatedWrite(conc)
        camera.Close()

    # ------------------------------------------------------------------
    # SetSuppressCallbackMode
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_set_suppress_callback_mode(self):
        """SetSuppressCallbackMode() accepts True and False without raising."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        nm.SetSuppressCallbackMode(True)
        nm.SetSuppressCallbackMode(False)
        camera.Close()

    # ------------------------------------------------------------------
    # GetDeviceName / DeviceName property
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_get_device_name(self):
        """GetDeviceName() returns a non-empty string."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        name = nm.GetDeviceName()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        camera.Close()

    def test_nodemap_wrapper_device_name_property(self):
        """DeviceName property matches GetDeviceName()."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        self.assertEqual(nm.GetDeviceName(), nm.DeviceName)
        camera.Close()

    # ------------------------------------------------------------------
    # Poll
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_poll(self):
        """Poll() accepts an elapsed-time argument without raising."""
        camera = self.create_first()
        camera.Open()
        camera.GetNodeMap().Poll(100)
        camera.Close()

    # ------------------------------------------------------------------
    # GetLock
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_get_lock(self):
        """GetLock() returns a non-None lock object."""
        camera = self.create_first()
        camera.Open()
        lock = camera.GetNodeMap().GetLock()
        self.assertIsNotNone(lock)
        camera.Close()

    # ------------------------------------------------------------------
    # GetNumNodes
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_get_num_nodes(self):
        """GetNumNodes() returns a positive integer."""
        camera = self.create_first()
        camera.Open()
        num = camera.GetNodeMap().GetNumNodes()
        self.assertIsInstance(num, int)
        self.assertGreater(num, 0)
        camera.Close()

    # ------------------------------------------------------------------
    # ParseSwissKnifes
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_parse_swiss_knifes(self):
        """ParseSwissKnifes() does not raise on a valid camera nodemap."""
        camera = self.create_first()
        camera.Open()
        camera.GetNodeMap().ParseSwissKnifes()
        camera.Close()

    # ------------------------------------------------------------------
    # __getattr__ early-exit branch
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_getattr_unknown_dunder_raises(self):
        """Accessing an unknown dunder attribute raises AttributeError."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        with self.assertRaises(AttributeError):
            getattr(nm, "__foobar__")
        camera.Close()

    # ------------------------------------------------------------------
    # __setattr__ deprecated assignment
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_setattr_deprecated_assignment(self):
        """Direct feature assignment emits DeprecationWarning and sets the value."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        with self.assertWarns(DeprecationWarning):
            nm.GainRaw = 200
        self.assertEqual(200, nm.GainRaw.Value)
        camera.Close()

    # ------------------------------------------------------------------
    # __dir__
    # ------------------------------------------------------------------

    def test_nodemap_wrapper_dir_returns_method_names(self):
        """dir(nodemap) returns a sorted list that includes NodeMapWrapper method names."""
        camera = self.create_first()
        camera.Open()
        nm = camera.GetNodeMap()
        listing = dir(nm)
        self.assertIsInstance(listing, list)
        self.assertEqual(listing, sorted(set(listing)))
        self.assertIn("GetNode", listing)
        self.assertIn("Contains", listing)
        self.assertIn("GetNumNodes", listing)
        camera.Close()

if __name__ == "__main__":
    unittest.main()
