"""\
This unit test checks the mapped pypylon InstantCamera API introduced by
src/pylon/InstantCamera.i.  Tests are usage-centric: each test method exercises
a coherent group of related methods so that the overall number of tests stays
manageable while still covering every public method and property.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import ctypes
import gc
import numpy
import queue
import random
import threading
import time
import unittest
import weakref


class _Holder:
    def __init__(self, size):
        self.buffer = bytearray(size)

    @property
    def ptr(self):
        return ctypes.addressof((ctypes.c_ubyte * len(self.buffer)).from_buffer(self.buffer))


class _CudaLikeOwner:
    def __init__(self, ptr, size):
        self.nbytes = size
        self.__cuda_array_interface__ = {
            "shape": (size,),
            "typestr": "|u1",
            "data": (ptr, False),
            "version": 3,
        }


class _TrackedBufferFactory:
    def __init__(self, test_case):
        self.test_case = test_case
        self.allocated = {}
        self.allocated_contexts = []
        self.freed_contexts = []
        self.free_keepalive_seen = []
        self.lock = threading.Lock()
        self.factory = pylon.PythonBufferFactory(self.allocate, self.free)

    def allocate(self, size):
        buf = (ctypes.c_ubyte * size)()
        ptr = ctypes.addressof(buf)
        with self.lock:
            self.allocated[ptr] = buf
            self.allocated_contexts.append(ptr)
        return ptr, buf, ptr, size

    def free(self, ptr, context, keep_alive):
        with self.lock:
            self.test_case.assertIn(ptr, self.allocated)
            self.test_case.assertEqual(ptr, context)
            self.freed_contexts.append(context)
            self.free_keepalive_seen.append(keep_alive is not None)
            self.allocated.pop(ptr)

    def assert_all_freed_once(self):
        with self.lock:
            self.test_case.assertEqual(sorted(self.allocated_contexts), sorted(self.freed_contexts))
            self.test_case.assertEqual(len(set(self.freed_contexts)), len(self.freed_contexts))
            self.test_case.assertEqual({}, self.allocated)
            self.test_case.assertTrue(all(self.free_keepalive_seen))


class InstantCameraTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Enums
    # ------------------------------------------------------------------

    def test_enum_presence(self):
        """Test that all enum value ported from C++ are present."""
        self.assertEqual(pylon.GrabStrategy_OneByOne, 0)
        self.assertEqual(pylon.GrabStrategy_LatestImageOnly, 1)
        self.assertEqual(pylon.GrabStrategy_LatestImages, 2)
        self.assertEqual(pylon.GrabStrategy_UpcomingImage, 3)

        self.assertEqual(pylon.GrabLoop_ProvidedByInstantCamera, 0)
        self.assertEqual(pylon.GrabLoop_ProvidedByUser, 1)

        self.assertEqual(pylon.CameraEventAvailability_Mandatory, 0)
        self.assertEqual(pylon.CameraEventAvailability_Optional, 1)

        self.assertEqual(pylon.RegistrationMode_Append, 0)
        self.assertEqual(pylon.RegistrationMode_ReplaceAll, 1)

        self.assertEqual(pylon.TimeoutHandling_Return, 0)
        self.assertEqual(pylon.TimeoutHandling_ThrowException, 1)

        self.assertEqual(pylon.BufferHandlingMode_Pool, "Pool")
        self.assertEqual(pylon.BufferHandlingMode_Stream, "Stream")

    # ------------------------------------------------------------------
    # Construction / Attach / Detach / Destroy
    # ------------------------------------------------------------------

    def test_default_construction_and_attach_detach_cycle(self):
        """Default-constructed camera has no device; attach, detach, and destroy work correctly."""
        camera = pylon.InstantCamera()
        self.assertFalse(camera.IsPylonDeviceAttached())
        self.assertFalse(camera.IsOpen())
        self.assertFalse(camera.IsGrabbing())
        self.assertFalse(camera.HasOwnership())

        # Attach a device created via TlFactory
        device = pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        camera.Attach(device, pylon.Cleanup_Delete)
        self.assertTrue(camera.HasOwnership())
        self.assertTrue(camera.IsPylonDeviceAttached())

        # DestroyDevice returns the device and resets the camera
        camera.DestroyDevice()
        self.assertFalse(camera.IsPylonDeviceAttached())
        self.assertFalse(camera.IsOpen())
        self.assertFalse(camera.HasOwnership())

        # Attach a device created via TlFactory
        device = pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        camera.Attach(device, pylon.Cleanup_None)
        self.assertFalse(camera.HasOwnership())
        self.assertTrue(camera.IsPylonDeviceAttached())

        # Detach returns the device and resets the camera
        device = camera.DetachDevice()
        pylon.TlFactory.GetInstance().DestroyDevice(device)
        self.assertFalse(camera.IsPylonDeviceAttached())
        self.assertFalse(camera.IsOpen())
        self.assertFalse(camera.HasOwnership())

    def test_destroy_device_closes_and_detaches(self):
        """DestroyDevice closes an open camera and removes the attached device."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertTrue(camera.IsOpen())
            camera.DestroyDevice()
            self.assertFalse(camera.IsPylonDeviceAttached())
            self.assertFalse(camera.IsOpen())

    # ------------------------------------------------------------------
    # Constructor overloads: FirstFound / Unambiguous / DeviceInfo / dict
    # ------------------------------------------------------------------

    def test_constructor_first_found(self):
        """InstantCamera(FirstFound) attaches a device, can open and grab."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertTrue(camera.IsOpen())
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_constructor_device_info_first_found(self):
        """InstantCamera(DeviceInfo, FirstFound) filters by device class and attaches."""
        device_info = pylon.DeviceInfo()
        device_info.SetDeviceClass(self.device_class)
        with pylon.InstantCamera(device_info, pylon.FirstFound) as camera:
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(camera.DeviceInfo.DeviceClass, self.device_class)
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_constructor_device_info_unambiguous(self):
        """InstantCamera(DeviceInfo, Unambiguous) attaches an exact device by serial number."""
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        device_info = devices[0]
        with pylon.InstantCamera(device_info, pylon.Unambiguous) as camera:
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(
                camera.DeviceInfo.SerialNumber,
                device_info.SerialNumber,
            )
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_constructor_dict_first_found_and_unambiguous(self):
        """InstantCamera(dict, FirstFound/Unambiguous) converts dict to DeviceInfo transparently."""
        # FirstFound with dict
        with pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound) as camera:
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(camera.DeviceInfo.DeviceClass, self.device_class)
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

        # Unambiguous with dict
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        serial = devices[0].SerialNumber
        with pylon.InstantCamera(
            {"DeviceClass": self.device_class, "SerialNumber": serial},
            pylon.Unambiguous,
        ) as camera:
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(camera.DeviceInfo.SerialNumber, serial)

    # ------------------------------------------------------------------
    # Attach overloads: FirstFound / DeviceInfo / dict
    # ------------------------------------------------------------------

    def test_attach_first_found(self):
        """Attach(FirstFound) creates and attaches the first available device."""
        with pylon.InstantCamera() as camera:
            camera.Attach(pylon.FirstFound)
            self.assertTrue(camera.IsPylonDeviceAttached())
            camera.Open()
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

    def test_attach_device_info_first_found_and_unambiguous(self):
        """Attach(DeviceInfo/dict, FirstFound/Unambiguous) work like the constructor counterparts."""
        with pylon.InstantCamera() as camera:
            # DeviceInfo + FirstFound
            device_info = pylon.DeviceInfo()
            device_info.SetDeviceClass(self.device_class)
            camera.Attach(device_info, pylon.FirstFound)
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(camera.DeviceInfo.DeviceClass, self.device_class)
            camera.DestroyDevice()

            # DeviceInfo + Unambiguous
            devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
            camera.Attach(devices[0], pylon.Unambiguous)
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(
                camera.DeviceInfo.SerialNumber,
                devices[0].SerialNumber,
            )
            camera.DestroyDevice()

            # dict + FirstFound
            camera.Attach({"DeviceClass": self.device_class}, pylon.FirstFound)
            self.assertTrue(camera.IsPylonDeviceAttached())
            camera.DestroyDevice()

            # dict + Unambiguous
            serial = devices[0].SerialNumber
            camera.Attach(
                {"DeviceClass": self.device_class, "SerialNumber": serial},
                pylon.Unambiguous,
            )
            self.assertTrue(camera.IsPylonDeviceAttached())
            self.assertEqual(camera.DeviceInfo.SerialNumber, serial)

    # ------------------------------------------------------------------
    # Open / Close lifecycle
    # ------------------------------------------------------------------

    def test_open_close_lifecycle(self):
        """Open and Close control the device connection; both are idempotent."""
        camera = pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound)
        camera.Open()
        self.assertTrue(camera.IsOpen())

        # Open again is a no-op
        camera.Open()
        self.assertTrue(camera.IsOpen())

        camera.Close()
        self.assertFalse(camera.IsOpen())

        # Close again is a no-op
        camera.Close()
        self.assertFalse(camera.IsOpen())

        # Re-open after close
        camera.Open()
        self.assertTrue(camera.IsOpen())
        camera.Close()
        camera.DestroyDevice()

    # ------------------------------------------------------------------
    # with-statement (context manager)
    # ------------------------------------------------------------------

    def test_context_manager_opens_and_destroys(self):
        """The with-statement opens the device on entry and destroys it on exit."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertTrue(camera.IsOpen())
            self.assertTrue(camera.IsPylonDeviceAttached())
        self.assertFalse(camera.IsOpen())
        self.assertFalse(camera.IsPylonDeviceAttached())

    def test_context_manager_no_device_does_not_raise(self):
        """with InstantCamera() when no device is attached does not raise."""
        with pylon.InstantCamera() as camera:
            self.assertFalse(camera.IsPylonDeviceAttached())
            self.assertFalse(camera.IsOpen())

    def test_context_manager_destroys_on_exception(self):
        """The with-statement destroys the device even when an exception is raised."""
        camera_ref = None
        try:
            with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
                camera_ref = camera
                raise RuntimeError("test error")
        except RuntimeError:
            pass
        self.assertIsNotNone(camera_ref)
        self.assertFalse(camera_ref.IsPylonDeviceAttached())
        self.assertFalse(camera_ref.IsOpen())

    def test_context_manager_with_device_info_and_dict(self):
        """The with-statement works with DeviceInfo and dict constructor overloads."""
        device_info = pylon.DeviceInfo()
        device_info.DeviceClass = self.device_class
        with pylon.InstantCamera(device_info, pylon.FirstFound) as camera:
            self.assertTrue(camera.IsOpen())
        self.assertFalse(camera.IsPylonDeviceAttached())

        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        with pylon.InstantCamera(devices[0], pylon.Unambiguous) as camera:
            self.assertTrue(camera.IsOpen())
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())

        with pylon.InstantCamera({"DeviceClass": self.device_class}, pylon.FirstFound) as camera:
            self.assertTrue(camera.IsOpen())
        self.assertFalse(camera.IsPylonDeviceAttached())

    # ------------------------------------------------------------------
    # GrabOne
    # ------------------------------------------------------------------

    def test_grab_one(self):
        """GrabOne grabs a single image with valid result data."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            result = camera.GrabOne(1000)
            self.assertTrue(result.GrabSucceeded())
            self.assertGreater(result.Width, 0)
            self.assertGreater(result.Height, 0)
            self.assertIsNotNone(result.Array)
            result.Release()
            result = camera.GrabOne(1000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabSucceeded())

    def test_grab_one_image_data_is_valid(self):
        """GrabOne result contains expected pixel data (emulator produces ramp pattern)."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            result = camera.GrabOne(1000)
            actual = list(result.Array[0:20, 0])
            expected = [actual[0] + i for i in range(20)]
            self.assertEqual(actual, expected)

    def test_multiple_grab_one_calls(self):
        """GrabOne can be called multiple times in succession on an open camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            for _ in range(5):
                result = camera.GrabOne(1000)
                self.assertTrue(result.GrabSucceeded())
                self.assertGreater(result.Width, 0)

    # ------------------------------------------------------------------
    # StartGrabbing / RetrieveResult / StopGrabbing / IsGrabbing
    # ------------------------------------------------------------------

    def test_start_stop_grabbing_lifecycle(self):
        """StartGrabbing, RetrieveResult, StopGrabbing control the grab lifecycle."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertFalse(camera.IsGrabbing())

            camera.StartGrabbing()
            self.assertTrue(camera.IsGrabbing())

            for _ in range(5):
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(grab_result.GrabSucceeded())
                self.assertGreater(grab_result.Width, 0)
                self.assertGreater(grab_result.Height, 0)
                grab_result.Release()

            self.assertTrue(camera.IsGrabbing())
            camera.StopGrabbing()
            self.assertFalse(camera.IsGrabbing())

            # StopGrabbing is idempotent
            camera.StopGrabbing()
            self.assertFalse(camera.IsGrabbing())

    def test_start_grabbing_max_images(self):
        """StartGrabbingMax stops automatically after the specified image count."""
        max_images = 7
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbingMax(max_images)
            count = 0
            while camera.IsGrabbing():
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grab_result.GrabSucceeded():
                    count += 1
                grab_result.Release()
            self.assertEqual(max_images, count)
            self.assertFalse(camera.IsGrabbing())

    def test_close_stops_grabbing(self):
        """Closing the camera while grabbing implicitly stops the grab."""
        camera = pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound)
        camera.Open()
        camera.StartGrabbing()
        self.assertTrue(camera.IsGrabbing())
        camera.Close()
        self.assertFalse(camera.IsGrabbing())
        self.assertFalse(camera.IsOpen())
        camera.DestroyDevice()

    # ------------------------------------------------------------------
    # Grab result data
    # ------------------------------------------------------------------

    def test_grab_result_properties(self):
        """Grab result exposes width, height, pixel type, buffer, and error information."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.PixelFormat.Value = "Mono8"
            camera.StartGrabbingMax(1)
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(grab_result.GrabSucceeded())

            # Image geometry
            self.assertGreater(grab_result.Width, 0)
            self.assertGreater(grab_result.Height, 0)
            self.assertEqual(0, grab_result.OffsetX)
            self.assertEqual(0, grab_result.OffsetY)
            self.assertGreater(grab_result.PayloadSize, 0)

            # Pixel type is defined
            pixel_type = grab_result.PixelType
            self.assertNotEqual(pixel_type, pylon.PixelType_Undefined)

            # Error info on success
            self.assertEqual(0, grab_result.ErrorCode)
            self.assertEqual("", grab_result.ErrorDescription)

            # Image number and block ID
            self.assertEqual(1, grab_result.ImageNumber)
            self.assertEqual(1, grab_result.ID)

            # Stride – GetStride() returns (ok, stride_bytes)
            ok, stride = grab_result.GetStride()
            self.assertTrue(ok)
            # This computation is only valid for Mono8
            self.assertEqual(stride, grab_result.Width + grab_result.PaddingX)

            grab_result.Release()

    # ------------------------------------------------------------------
    # CameraContext
    # ------------------------------------------------------------------

    def test_camera_context(self):
        """CameraContext attaches a user value to each grab result."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # Default context is 0
            self.assertEqual(0, camera.CameraContext)

            camera.CameraContext = 4712
            self.assertEqual(4712, camera.CameraContext)

            camera.SetCameraContext(1247)
            self.assertEqual(1247, camera.GetCameraContext())

            grab_result = camera.GrabOne(1000)
            self.assertTrue(grab_result.GrabSucceeded())
            self.assertEqual(1247, grab_result.CameraContext)

    # ------------------------------------------------------------------
    # DeviceInfo
    # ------------------------------------------------------------------

    def test_device_info(self):
        """DeviceInfo provides device metadata; empty DeviceInfo when no device is attached."""
        # No device attached → empty DeviceInfo
        camera = pylon.InstantCamera()
        device_info = camera.DeviceInfo
        self.assertIsNotNone(device_info)

        # With device attached → populated DeviceInfo
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # use property (recommended)
            device_info = camera.DeviceInfo
            device_class = device_info.DeviceClass
            self.assertTrue(len(device_class) > 0)
            self.assertEqual(device_class, self.device_class)

            # alternative variant using the method
            device_info = camera.GetDeviceInfo()
            device_class = device_info.DeviceClass
            self.assertTrue(len(device_class) > 0)
            self.assertEqual(device_class, self.device_class)

    # ------------------------------------------------------------------
    # Node map access properties
    # ------------------------------------------------------------------

    def test_node_map_properties(self):
        """NodeMap, TLNodeMap, StreamGrabberNodeMap, EventGrabberNodeMap, and InstantCameraNodeMap are accessible."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # Camera node map
            node_map = camera.NodeMap
            self.assertIsInstance(node_map, pylon.NodeMapWrapper)

            # Transport layer node map
            device_transport_layer_node_map = camera.TLNodeMap
            self.assertIsInstance(device_transport_layer_node_map, pylon.NodeMapWrapper)

            # Stream grabber node map (available when open)
            stream_grabber_node_map = camera.StreamGrabberNodeMap
            self.assertIsInstance(stream_grabber_node_map, pylon.NodeMapWrapper)

            # Event grabber node map
            event_grabber_node_map = camera.EventGrabberNodeMap
            self.assertIsInstance(event_grabber_node_map, pylon.NodeMapWrapper)

            # InstantCamera node map (always available)
            instant_camera_node_map = camera.InstantCameraNodeMap
            self.assertIsInstance(instant_camera_node_map, pylon.NodeMapWrapper)

            # Get the node maps using the getter methods
            node_map = camera.GetNodeMap()
            device_transport_layer_node_map = camera.GetTLNodeMap()
            self.assertIsInstance(device_transport_layer_node_map, pylon.NodeMapWrapper)
            stream_grabber_node_map = camera.GetStreamGrabberNodeMap()
            self.assertIsInstance(stream_grabber_node_map, pylon.NodeMapWrapper)
            event_grabber_node_map = camera.GetEventGrabberNodeMap()
            self.assertIsInstance(event_grabber_node_map, pylon.NodeMapWrapper)
            instant_camera_node_map = camera.GetInstantCameraNodeMap()
            self.assertIsInstance(instant_camera_node_map, pylon.NodeMapWrapper)

    def test_node_map_shortcut_properties(self):
        """StreamGrabber, EventGrabber, and TransportLayer shortcut properties work."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertIsInstance(camera.StreamGrabber, pylon.NodeMapWrapper)
            self.assertIsInstance(camera.EventGrabber, pylon.NodeMapWrapper)
            self.assertIsInstance(camera.TransportLayer, pylon.NodeMapWrapper)

        # When not open, StreamGrabber and EventGrabber return None
        camera2 = pylon.InstantCamera()
        self.assertIsNone(camera2.StreamGrabber)
        self.assertIsNone(camera2.EventGrabber)

    # ------------------------------------------------------------------
    # InstantCamera parameters (MaxNumBuffer, OutputQueueSize, etc.)
    # ------------------------------------------------------------------

    def test_instant_camera_parameters(self):
        """InstantCamera parameters can be read and written via the parameter API."""
        # Parameters that are only writable when the camera is closed (not open)
        camera = pylon.InstantCamera()
        device = pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        camera.Attach(device, pylon.Cleanup_Delete)

        camera.GrabCameraEvents.Value = True
        self.assertEqual(True, camera.GrabCameraEvents.Value)
        camera.GrabCameraEvents.Value = False

        camera.MonitorModeActive.Value = True
        self.assertEqual(True, camera.MonitorModeActive.Value)
        camera.MonitorModeActive.Value = False

        camera.Open()

        # AcquisitionStartStopExecutionEnable
        camera.AcquisitionStartStopExecutionEnable.Value = False
        self.assertEqual(False, camera.AcquisitionStartStopExecutionEnable.Value)
        camera.AcquisitionStartStopExecutionEnable.Value = True
        self.assertEqual(True, camera.AcquisitionStartStopExecutionEnable.Value)

        # BufferHandlingMode
        self.assertEqual(pylon.BufferHandlingMode_Pool, camera.BufferHandlingMode.Value)
        camera.BufferHandlingMode.Value = pylon.BufferHandlingMode_Stream
        self.assertEqual(pylon.BufferHandlingMode_Stream, camera.BufferHandlingMode.Value)
        camera.BufferHandlingMode.Value = pylon.BufferHandlingMode_Pool

        # ChunkNodeMapsEnable
        camera.ChunkNodeMapsEnable.Value = False
        self.assertEqual(False, camera.ChunkNodeMapsEnable.Value)
        camera.ChunkNodeMapsEnable.Value = True
        self.assertEqual(True, camera.ChunkNodeMapsEnable.Value)

        # ClearBufferModeEnable
        camera.ClearBufferModeEnable.Value = True
        self.assertEqual(True, camera.ClearBufferModeEnable.Value)
        camera.ClearBufferModeEnable.Value = False
        self.assertEqual(False, camera.ClearBufferModeEnable.Value)

        # GrabLoopThreadPriorityOverride and GrabLoopThreadPriority
        camera.GrabLoopThreadPriorityOverride.Value = True
        self.assertEqual(True, camera.GrabLoopThreadPriorityOverride.Value)
        camera.GrabLoopThreadPriority.SetToMinimum()
        self.assertEqual(camera.GrabLoopThreadPriority.Min, camera.GrabLoopThreadPriority.Value)
        camera.GrabLoopThreadPriorityOverride.Value = False
        self.assertEqual(False, camera.GrabLoopThreadPriorityOverride.Value)

        # GrabLoopThreadUseTimeout and GrabLoopThreadTimeout
        camera.GrabLoopThreadUseTimeout.Value = True
        self.assertEqual(True, camera.GrabLoopThreadUseTimeout.Value)
        camera.GrabLoopThreadTimeout.Value = 10000
        self.assertEqual(10000, camera.GrabLoopThreadTimeout.Value)
        camera.GrabLoopThreadUseTimeout.Value = False
        self.assertEqual(False, camera.GrabLoopThreadUseTimeout.Value)

        # InternalGrabEngineThreadPriorityOverride and InternalGrabEngineThreadPriority
        camera.InternalGrabEngineThreadPriorityOverride.Value = True
        self.assertEqual(True, camera.InternalGrabEngineThreadPriorityOverride.Value)
        camera.InternalGrabEngineThreadPriority.SetToMinimum()
        self.assertEqual(camera.InternalGrabEngineThreadPriority.Min, camera.InternalGrabEngineThreadPriority.Value)
        camera.InternalGrabEngineThreadPriorityOverride.Value = False
        self.assertEqual(False, camera.InternalGrabEngineThreadPriorityOverride.Value)

        # MaxNumBuffer
        original_max = camera.MaxNumBuffer.Value
        camera.MaxNumBuffer.Value = 20
        self.assertEqual(20, camera.MaxNumBuffer.Value)
        camera.MaxNumBuffer.Value = original_max

        # MaxNumGrabResults
        camera.MaxNumGrabResults.Value = 100
        self.assertEqual(100, camera.MaxNumGrabResults.Value)

        # MaxNumQueuedBuffer
        camera.MaxNumQueuedBuffer.Value = 3
        self.assertEqual(3, camera.MaxNumQueuedBuffer.Value)

        # MigrationModeActive – read-only at runtime, just verify it is readable
        self.assertIsInstance(camera.MigrationModeActive.Value, bool)

        # NumEmptyBuffers, NumReadyBuffers, NumQueuedBuffers – read-only, zero when not grabbing
        self.assertEqual(0, camera.NumEmptyBuffers.Value)
        self.assertEqual(0, camera.NumReadyBuffers.Value)
        self.assertEqual(0, camera.NumQueuedBuffers.Value)

        # OutputQueueSize – writable before grabbing
        camera.OutputQueueSize.Value = 8
        self.assertEqual(8, camera.OutputQueueSize.Value)

        # StaticChunkNodeMapPoolSize
        camera.StaticChunkNodeMapPoolSize.Value = 10
        self.assertEqual(10, camera.StaticChunkNodeMapPoolSize.Value)
        camera.StaticChunkNodeMapPoolSize.Value = 0
        self.assertEqual(0, camera.StaticChunkNodeMapPoolSize.Value)

        # UseExtendedIdIfAvailable
        camera.UseExtendedIdIfAvailable.Value = False
        self.assertEqual(False, camera.UseExtendedIdIfAvailable.Value)
        camera.UseExtendedIdIfAvailable.Value = True
        self.assertEqual(True, camera.UseExtendedIdIfAvailable.Value)

        camera.DestroyDevice()

    def test_queue_params_during_grabbing(self):
        """NumEmptyBuffers, NumReadyBuffers, NumQueuedBuffers are readable during grabbing."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # Before grabbing, queue counters are zero
            self.assertEqual(0, camera.NumEmptyBuffers.Value)
            self.assertEqual(0, camera.NumReadyBuffers.Value)
            self.assertEqual(0, camera.NumQueuedBuffers.Value)

            camera.StartGrabbing()
            # During grabbing, buffers are queued
            self.assertGreaterEqual(camera.NumQueuedBuffers.Value, 0)

            # Retrieve one result and check counters are still readable
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(grab_result.GrabSucceeded())
            grab_result.Release()

            camera.StopGrabbing()
            # After stop, counters return to zero
            self.assertEqual(0, camera.NumQueuedBuffers.Value)

    def test_queued_buffer_count_property(self):
        """QueuedBufferCount property returns the number of queued buffers."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertEqual(0, camera.QueuedBufferCount)
            camera.StartGrabbing()
            self.assertGreater(camera.QueuedBufferCount, 0)
            self.assertGreater(camera.GetQueuedBufferCount(), 0)
            camera.StopGrabbing()
            self.assertEqual(0, camera.QueuedBufferCount)

    # ------------------------------------------------------------------
    # Grab strategies
    # ------------------------------------------------------------------

    def test_grab_strategy_one_by_one(self):
        """GrabStrategy_OneByOne delivers images in order with sequential IDs."""
        max_images = 5
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.CameraContext = 42
            camera.StartGrabbingMax(max_images, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser)
            count = 0
            while camera.IsGrabbing():
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                if grab_result.GrabSucceeded():
                    count += 1
                    self.assertEqual(count, grab_result.ImageNumber)
                    self.assertEqual(count, grab_result.ID)
                    self.assertEqual(42, grab_result.CameraContext)
                grab_result.Release()
            self.assertEqual(max_images, count)

    def test_grab_strategy_latest_image_only(self):
        """GrabStrategy_LatestImageOnly can be used for continuous grabbing."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, pylon.GrabLoop_ProvidedByUser)
            self.assertTrue(camera.IsGrabbing())
            for _ in range(3):
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(grab_result.GrabSucceeded())
                grab_result.Release()
            camera.StopGrabbing()

    def test_grab_strategy_latest_images(self):
        """GrabStrategy_LatestImages maintains a configurable output queue."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.OutputQueueSize.Value = 3
            camera.StartGrabbing(pylon.GrabStrategy_LatestImages)
            self.assertTrue(camera.IsGrabbing())
            for _ in range(3):
                grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(grab_result.GrabSucceeded())
                grab_result.Release()
            camera.StopGrabbing()

    # ------------------------------------------------------------------
    # Hardware interface type helpers
    # ------------------------------------------------------------------

    def test_hardware_interface_type_queries(self):
        """IsUsb, IsGigE, IsCameraLink, IsCxp return False for emulated cameras; also safe without a device."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertFalse(camera.IsUsb())
            self.assertFalse(camera.IsGigE())
            self.assertFalse(camera.IsCameraLink())
            self.assertFalse(camera.IsCxp())

        # Also safe without a device attached
        empty_camera = pylon.InstantCamera()
        self.assertFalse(empty_camera.IsUsb())
        self.assertFalse(empty_camera.IsGigE())
        self.assertFalse(empty_camera.IsCameraLink())
        self.assertFalse(empty_camera.IsCxp())

    # ------------------------------------------------------------------
    # SFNC version
    # ------------------------------------------------------------------

    def test_sfnc_version(self):
        """GetSfncVersion returns a VersionInfo when a device is attached and open."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            sfnc_version = camera.GetSfncVersion()
            self.assertIsNotNone(sfnc_version)

    # ------------------------------------------------------------------
    # IsCameraDeviceRemoved
    # ------------------------------------------------------------------

    def test_camera_device_removed(self):
        """IsCameraDeviceRemoved returns False for a normally connected or empty camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self.assertFalse(camera.IsCameraDeviceRemoved())
            camera.FirePnPCallback.Execute()
            self.assertTrue(camera.IsCameraDeviceRemoved())

        empty_camera = pylon.InstantCamera()
        self.assertFalse(empty_camera.IsCameraDeviceRemoved())

    # ------------------------------------------------------------------
    # WaitForFrameTriggerReady / CanWaitForFrameTriggerReady
    # ------------------------------------------------------------------

    def test_can_wait_for_frame_trigger_ready(self):
        """CanWaitForFrameTriggerReady reports trigger readiness capability."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            pylon.SoftwareTriggerConfiguration.ApplyConfiguration(camera.NodeMap)
            self.assertTrue(camera.CanWaitForFrameTriggerReady())
            camera.StartGrabbing()
            self.assertTrue(camera.WaitForFrameTriggerReady(1000))
            camera.ExecuteSoftwareTrigger()
            result = camera.RetrieveResult(1000)
            self.assertTrue(result.GrabSucceeded())

    # ------------------------------------------------------------------
    # dir() integration and __getattr__
    # ------------------------------------------------------------------

    def test_dir_includes_camera_and_instant_camera_features(self):
        """dir(camera) includes InstantCamera parameters and camera device features when open."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            attributes = dir(camera)
            # InstantCamera node map parameters
            self.assertIn("MaxNumBuffer", attributes)
            self.assertIn("OutputQueueSize", attributes)

    def test_direct_parameter_access_via_attribute(self):
        """Camera parameters are accessible as attributes (e.g. camera.Width) when the device is open."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            # The emulator should expose Width and Height
            width = camera.Width
            self.assertTrue(width.IsReadable())
            self.assertGreater(width.Value, 0)

    # ------------------------------------------------------------------
    # Event handler registration (ConfigurationEventHandler, ImageEventHandler)
    # ------------------------------------------------------------------

    def test_register_deregister_configuration_event_handler(self):
        """RegisterConfiguration and DeregisterConfiguration manage configuration event handlers."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            handler = pylon.ConfigurationEventHandler()

            camera.RegisterConfiguration(
                handler, pylon.RegistrationMode_Append, pylon.Cleanup_None
            )
            self.assertTrue(camera.DeregisterConfiguration(handler))
            # Deregistering again returns False
            self.assertFalse(camera.DeregisterConfiguration(handler))

    def test_register_deregister_image_event_handler(self):
        """RegisterImageEventHandler and DeregisterImageEventHandler manage image event handlers."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            handler = pylon.ImageEventHandler()

            camera.RegisterImageEventHandler(
                handler, pylon.RegistrationMode_Append, pylon.Cleanup_None
            )
            self.assertTrue(camera.DeregisterImageEventHandler(handler))
            # Deregistering again returns False
            self.assertFalse(camera.DeregisterImageEventHandler(handler))


    def test_register_deregister_camera_event_handler(self):
        """RegisterImageEventHandler and DeregisterImageEventHandler manage image event handlers."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            handler = pylon.CameraEventHandler()

            camera.RegisterCameraEventHandler(
                handler,
                "Width",
                1234,
                pylon.RegistrationMode_Append,
                pylon.Cleanup_None,
                pylon.CameraEventAvailability_Mandatory
            )
            self.assertTrue(camera.DeregisterCameraEventHandler(handler, "Width"))
            # Deregistering again returns False
            self.assertFalse(camera.DeregisterCameraEventHandler(handler, "Width"))

    # ------------------------------------------------------------------
    # Grab loop thread (GrabLoop_ProvidedByInstantCamera)
    # ------------------------------------------------------------------

    def test_grab_loop_provided_by_instant_camera(self):
        """StartGrabbing with GrabLoop_ProvidedByInstantCamera runs a background grab loop."""
        grabbed_images = []

        class CountingImageHandler(pylon.ImageEventHandler):
            def OnImageGrabbed(self, camera, grab_result):
                if grab_result.GrabSucceeded():
                    grabbed_images.append(grab_result.ImageNumber)

        max_images = 5
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.RegisterImageEventHandler(
                CountingImageHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete
            )
            camera.StartGrabbingMax(
                max_images, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera
            )

            # Wait for the grab to finish
            camera.GetGrabStopWaitObject().Wait(max_images * 5000)
            self.assertFalse(camera.IsGrabbing())
            self.assertEqual(max_images, len(grabbed_images))

    # ------------------------------------------------------------------
    # WaitObjects (GrabStopWaitObject / GrabResultWaitObject)
    # ------------------------------------------------------------------

    def test_grab_stop_and_result_wait_objects(self):
        """GetGrabStopWaitObject, GetCameraEventWaitObject and GetGrabResultWaitObject reflect the grab state."""
        with pylon.InstantCamera() as camera:
            camera.Attach(self.get_camera_traits(), pylon.FirstFound)
            camera.GrabCameraEvents.Value = True
            camera.Open()

            # Before grabbing, stop is signaled and result is not
            self.assertTrue(camera.GetGrabStopWaitObject().Wait(0))
            self.assertFalse(camera.GetGrabResultWaitObject().Wait(0))
            self.assertFalse(camera.GetCameraEventWaitObject().Wait(0))

            camera.StartGrabbing()
            # During grabbing, stop is not signaled
            self.assertFalse(camera.GetGrabStopWaitObject().Wait(0))

            camera.StopGrabbing()
            # After stopping, stop is signaled
            self.assertTrue(camera.GetGrabStopWaitObject().Wait(0))

    # ------------------------------------------------------------------
    # RetrieveResult when not grabbing
    # ------------------------------------------------------------------

    def test_retrieve_result_when_not_grabbing(self):
        """RetrieveResult returns immediately when the camera is not grabbing."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            got_result = camera.RetrieveResult(1, pylon.TimeoutHandling_Return)
            self.assertFalse(got_result.IsValid())

    # ------------------------------------------------------------------
    # No-device error cases
    # ------------------------------------------------------------------

    def test_operations_without_device_raise_or_are_safe(self):
        """Methods on a camera with no device attached either raise or are safely no-ops."""
        camera = pylon.InstantCamera()

        # Open requires attached device
        with self.assertRaises(Exception):
            camera.Open()

        # IsOpen, IsGrabbing are safe
        self.assertFalse(camera.IsOpen())
        self.assertFalse(camera.IsGrabbing())

        # StopGrabbing is idempotent
        camera.StopGrabbing()

        # DestroyDevice on empty camera is a no-op
        camera.DestroyDevice()

        # StartGrabbing requires a device
        with self.assertRaises(Exception):
            camera.StartGrabbing()

        # GrabOne requires a device
        with self.assertRaises(Exception):
            camera.GrabOne(10)

        # DetachDevice returns None when nothing is attached
        device = camera.DetachDevice()
        self.assertEqual(device, None)

        # CameraContext is accessible even without a device
        self.assertEqual(0, camera.CameraContext)
        camera.CameraContext = 567
        self.assertEqual(567, camera.CameraContext)

        # InstantCameraNodeMap is always available
        ic_node_map = camera.InstantCameraNodeMap
        self.assertIsNotNone(ic_node_map)

        # GetGrabStopWaitObject and GetGrabResultWaitObject are accessible
        self.assertTrue(camera.GetGrabStopWaitObject().Wait(0))
        self.assertFalse(camera.GetGrabResultWaitObject().Wait(0))

    # ------------------------------------------------------------------
    # Backwards compatability
    # ------------------------------------------------------------------

    def test_backwards_compatibility_direct_assignment(self):
        """Setting a parameter value using direct assignment instead of using the .Value property."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.MaxNumBuffer = 10
            self.assertEqual(camera.MaxNumBuffer.Value, 10)
            camera.MaxNumBuffer = 9
            self.assertEqual(camera.MaxNumBuffer.Value, 9)


    def test_backwards_compatibility_use_genicam_type(self):
        """Using a parameter as property resulting in a returned genicam type instead of a parameter type."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            root = camera.Root

    # ------------------------------------------------------------------
    # Python buffer factory
    # ------------------------------------------------------------------

    def _create_first_or_skip(self):
        try:
            return self.create_first()
        except Exception as exc:
            self.skipTest("CamEmu camera not available in this environment: %s" % exc)

    def test_set_python_buffer_factory(self):
        """SetBufferFactory with a Python callback allocates and frees buffers correctly."""
        cam = self.create_first()
        cam.Open()

        tracked = _TrackedBufferFactory(self)
        cam.SetBufferFactory(tracked.factory, pylon.Cleanup_None)

        cam.StartGrabbing()
        contexts = []
        while len(contexts) < 5:
            with cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grabResult:
                self.assertTrue(grabResult.GrabSucceeded())
                contexts.append(grabResult.BufferContext)
                with grabResult.GetArrayZeroCopy() as array:
                    self.assertEqual(array.ctypes.data, grabResult.BufferContext)
                    self.assertEqual(array.shape[0], grabResult.Height)
                    self.assertEqual(array.shape[1], grabResult.Width)
        cam.StopGrabbing()

        cam.SetBufferFactory(None)
        cam.Close()

        self.assertGreater(len(contexts), 0)
        self.assertTrue(set(contexts).issubset(set(tracked.allocated_contexts)))
        tracked.assert_all_freed_once()

    def test_set_python_buffer_factory_gendc_zero_copy(self):
        """Python buffer factory supplies GenDC payload bytes; component zero-copy views work."""
        cam = self.create_first()
        cam.Open()

        tracked = _TrackedBufferFactory(self)
        cam.SetBufferFactory(tracked.factory, pylon.Cleanup_None)

        try:
            cam.GenDC.Value = True
        except Exception as exc:
            cam.Close()
            self.skipTest("GenDC is not supported on this emulator: %s" % exc)

        cam.StartGrabbing()
        try:
            with cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                self.assertTrue(grab_result.GrabSucceeded())
                self.assertEqual(grab_result.PayloadType, pylon.PayloadType_GenDC)
                self.assertIn(grab_result.BufferContext, tracked.allocated_contexts)

                with grab_result.GetFirstImageDataComponent() as component:
                    self.assertTrue(component.IsValid())
                    with component.GetArrayZeroCopy() as image:
                        self.assertGreater(image.shape[0], 0)
                        self.assertGreater(image.shape[1], 0)
        finally:
            cam.StopGrabbing()

        cam.SetBufferFactory(None)
        cam.Close()
        tracked.assert_all_freed_once()

    def test_set_python_buffer_factory_default_keeps_factory_reference(self):
        """SetBufferFactory keeps the factory alive when Cleanup_None is used (default)."""
        cam = self.create_first()
        cam.Open()

        def alloc_cb(size):
            holder = _Holder(size)
            return (holder.ptr, holder, 0, len(holder.buffer))

        factory = pylon.PythonBufferFactory(alloc_cb)
        cam.SetBufferFactory(factory)
        self.assertIs(cam.__dict__.get("_buffer_factory_ref"), factory)

        cam.SetBufferFactory(None)
        self.assertNotIn("_buffer_factory_ref", cam.__dict__)
        cam.Close()

    def test_python_buffer_factory_debug_lifetime(self):
        """PythonBufferFactory debug helpers keep allocator objects alive until free."""
        callbacks = []
        holder_refs = []

        def allocate(size):
            holder = _Holder(size)
            holder_refs.append(weakref.ref(holder))
            return (holder.ptr, holder, 1234, len(holder.buffer))

        def free(ptr, context, keepalive):
            callbacks.append((ptr, context, keepalive is not None))

        factory = pylon.PythonBufferFactory(allocate, free)
        ptr, context = factory.DebugAllocateBuffer(128)
        self.assertEqual(context, 1234)
        self.assertTrue(holder_refs[0]() is not None)
        self.assertTrue(pylon.LookupBufferKeepAlive(ptr) is not None)

        gc.collect()
        self.assertTrue(holder_refs[0]() is not None)

        factory.DebugFreeBuffer(ptr, context)
        self.assertEqual(len(callbacks), 1)
        self.assertEqual(callbacks[0][0], ptr)
        self.assertEqual(callbacks[0][1], context)
        self.assertTrue(callbacks[0][2])
        self.assertTrue(pylon.LookupBufferKeepAlive(ptr) is None)

        gc.collect()
        self.assertTrue(holder_refs[0]() is None)

    def test_python_buffer_factory_capacity_guard(self):
        """PythonBufferFactory rejects allocations when keepalive capacity is too small."""
        def allocate(size):
            holder = _Holder(size)
            return (holder.ptr, holder, 1, size - 1)

        factory = pylon.PythonBufferFactory(allocate)
        with self.assertRaises(genicam.InvalidArgumentException):
            factory.DebugAllocateBuffer(1024)

    def test_python_buffer_factory_destroy_callback(self):
        """DestroyBufferFactory invokes the optional destroy callback."""
        destroyed = []

        def allocate(size):
            holder = _Holder(size)
            return (holder.ptr, holder, 0, len(holder.buffer))

        def destroy():
            destroyed.append(True)

        factory = pylon.PythonBufferFactory(allocate, None, destroy)
        factory.thisown = 0
        factory.DestroyBufferFactory()
        self.assertEqual(destroyed, [True])

    def test_python_buffer_factory_cuda_owner_proxy_shape(self):
        """_PylonOwnerView reshapes CUDA owner interfaces for grab-result views."""
        owner = _CudaLikeOwner(0x1234, 4096)
        proxy = pylon._PylonOwnerView(
            owner,
            pylon.GrabResult(),
            shape=(32, 32),
            dtype=numpy.uint8,
            strides=(32, 1),
            nbytes=1024,
        )

        interface = proxy.__cuda_array_interface__
        self.assertEqual(interface["shape"], (32, 32))
        self.assertEqual(interface["typestr"], numpy.dtype(numpy.uint8).str)
        self.assertEqual(interface["strides"], (32, 1))
        self.assertEqual(interface["data"][0], 0x1234)
        self.assertIs(proxy._owner, owner)

    def test_arrayview_backpressure_when_held(self):
        """GetArray(copy=False) keeps a grab buffer reserved until the view is released."""
        cam = self._create_first_or_skip()
        cam.Open()
        try:
            try:
                cam.MaxNumBuffer.Value = 1
            except Exception as exc:
                self.skipTest("MaxNumBuffer is not configurable: %s" % exc)

            cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

            held = []
            with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
                held.append(result.GetArray(copy=False))

            with self.assertRaises(genicam.TimeoutException):
                cam.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)

            held.clear()
            gc.collect()

            with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
        finally:
            if cam.IsGrabbing():
                cam.StopGrabbing()
            cam.Close()

    def test_arrayview_cross_thread_handoff_releases_buffer(self):
        """Zero-copy array views handed to another thread release buffers when dropped."""
        cam = self._create_first_or_skip()
        cam.Open()
        tracked = _TrackedBufferFactory(self)
        worker_errors = queue.Queue()
        release_event = threading.Event()

        try:
            try:
                cam.MaxNumBuffer.Value = 1
            except Exception as exc:
                self.skipTest("MaxNumBuffer is not configurable: %s" % exc)

            cam.SetBufferFactory(tracked.factory, pylon.Cleanup_None)
            cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

            frame_queue = queue.Queue()

            def worker():
                frame = None
                try:
                    frame = frame_queue.get(timeout=2)
                    self.assertEqual(frame.shape[0], 1040)
                    self.assertEqual(frame.shape[1], 1024)
                    release_event.wait(timeout=2)
                except Exception as exc:
                    worker_errors.put(exc)
                finally:
                    del frame
                    gc.collect()

            thread = threading.Thread(target=worker)
            thread.start()

            with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
                frame_queue.put(result.GetArray(copy=False))

            with self.assertRaises(genicam.TimeoutException):
                cam.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)

            self.assertEqual([], tracked.freed_contexts)
            release_event.set()
            thread.join(timeout=3)
            self.assertFalse(thread.is_alive())
            if not worker_errors.empty():
                raise worker_errors.get()

            gc.collect()
            with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
        finally:
            release_event.set()
            if cam.IsGrabbing():
                cam.StopGrabbing()
            cam.SetBufferFactory(None)
            cam.Close()

        tracked.assert_all_freed_once()

    def test_set_buffer_factory_waits_for_cross_thread_owner_view_release(self):
        """SetBufferFactory(None) waits until cross-thread owner views are released."""
        cam = self._create_first_or_skip()
        cam.Open()
        tracked = _TrackedBufferFactory(self)
        worker_errors = queue.Queue()
        release_event = threading.Event()

        try:
            cam.SetBufferFactory(tracked.factory, pylon.Cleanup_None)
            cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

            owner_queue = queue.Queue()

            def worker():
                owner_view = None
                try:
                    owner_view = owner_queue.get(timeout=2)
                    self.assertEqual(owner_view.shape[0], 1040)
                    self.assertEqual(owner_view.shape[1], 1024)
                    release_event.wait(timeout=2)
                except Exception as exc:
                    worker_errors.put(exc)
                finally:
                    del owner_view
                    gc.collect()

            thread = threading.Thread(target=worker)
            thread.start()

            with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                self.assertTrue(result.GrabSucceeded())
                held_context = result.BufferContext
                owner_queue.put(result.GetBufferOwnerView())

            cam.StopGrabbing()
            self.assertNotIn(held_context, tracked.freed_contexts)

            release_event.set()
            thread.join(timeout=3)
            self.assertFalse(thread.is_alive())
            if not worker_errors.empty():
                raise worker_errors.get()

            gc.collect()
            cam.SetBufferFactory(None)
            cam.Close()
        finally:
            release_event.set()
            if cam.IsGrabbing():
                cam.StopGrabbing()
            if cam.IsOpen():
                cam.SetBufferFactory(None)
                cam.Close()

        tracked.assert_all_freed_once()

    def test_arrayview_randomized_cross_thread_backpressure_stress(self):
        """Randomized cross-thread zero-copy handoff stress test with limited buffers."""
        cam = self._create_first_or_skip()
        cam.Open()
        tracked = _TrackedBufferFactory(self)
        rng = random.Random(1701)
        worker_errors = queue.Queue()
        release_events = []
        threads = []

        try:
            try:
                cam.MaxNumBuffer.Value = 2
            except Exception as exc:
                self.skipTest("MaxNumBuffer is not configurable: %s" % exc)

            cam.SetBufferFactory(tracked.factory, pylon.Cleanup_None)
            cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

            for _round_idx in range(8):
                frame_queue = queue.Queue()
                release_events = [threading.Event(), threading.Event()]
                threads = []
                held_contexts = []

                def worker(worker_idx):
                    frame = None
                    try:
                        frame = frame_queue.get(timeout=2)
                        self.assertEqual(frame.shape[0], 1040)
                        self.assertEqual(frame.shape[1], 1024)
                        time.sleep(rng.uniform(0.001, 0.01))
                        release_events[worker_idx].wait(timeout=3)
                        time.sleep(rng.uniform(0.001, 0.01))
                    except Exception as exc:
                        worker_errors.put(exc)
                    finally:
                        del frame
                        gc.collect()

                for worker_idx in range(2):
                    thread = threading.Thread(target=worker, args=(worker_idx,))
                    thread.start()
                    threads.append(thread)

                for _ in range(2):
                    with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                        self.assertTrue(result.GrabSucceeded())
                        held_contexts.append(result.BufferContext)
                        frame_queue.put(result.GetArray(copy=False))

                with self.assertRaises(genicam.TimeoutException):
                    cam.RetrieveResult(120, pylon.TimeoutHandling_ThrowException)

                for context in held_contexts:
                    self.assertNotIn(context, tracked.freed_contexts)

                release_order = [0, 1]
                rng.shuffle(release_order)
                release_events[release_order[0]].set()
                time.sleep(rng.uniform(0.001, 0.02))
                release_events[release_order[1]].set()

                for thread in threads:
                    thread.join(timeout=3)
                    self.assertFalse(thread.is_alive())

                if not worker_errors.empty():
                    raise worker_errors.get()

                gc.collect()
                with cam.RetrieveResult(2000, pylon.TimeoutHandling_ThrowException) as result:
                    self.assertTrue(result.GrabSucceeded())

            cam.StopGrabbing()
            cam.SetBufferFactory(None)
            cam.Close()
        finally:
            for event in release_events:
                event.set()
            for thread in threads:
                thread.join(timeout=1)
            if cam.IsGrabbing():
                cam.StopGrabbing()
            if cam.IsOpen():
                cam.SetBufferFactory(None)
                cam.Close()

        tracked.assert_all_freed_once()

if __name__ == "__main__":
    unittest.main()
