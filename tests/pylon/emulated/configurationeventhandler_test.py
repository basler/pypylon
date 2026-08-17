"""\
This unit test checks the ConfigurationEventHandler class
introduced by `src/pylon/ConfigurationEventHandler.i`.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class TestConfigurationEventHandler(pylon.ConfigurationEventHandler):
    def __init__(self):
        super().__init__()
        self.attach_camera = None
        self.attached_camera = None
        self.detach_camera = None
        self.detached_camera = None
        self.destroy_camera = None
        self.destroyed_camera = None
        self.open_camera = None
        self.opened_camera = None
        self.close_camera = None
        self.closed_camera = None
        self.grab_start_camera = None
        self.grab_started_camera = None
        self.grab_stop_camera = None
        self.grab_stopped_camera = None
        self.grab_error_camera = None
        self.grab_error_message = None
        self.camera_device_removed_camera = None
        self.configuration_registered_camera = None
        self.configuration_deregistered_camera = None

    def OnAttach(self, camera):
        self.attach_camera = camera

    def OnAttached(self, camera):
        self.attached_camera = camera

    def OnDetach(self, camera):
        self.detach_camera = camera

    def OnDetached(self, camera):
        self.detached_camera = camera

    def OnDestroy(self, camera):
        self.destroy_camera = camera

    def OnDestroyed(self, camera):
        self.destroyed_camera = camera

    def OnOpen(self, camera):
        self.open_camera = camera

    def OnOpened(self, camera):
        self.opened_camera = camera

    def OnClose(self, camera):
        self.close_camera = camera

    def OnClosed(self, camera):
        self.closed_camera = camera

    def OnGrabStart(self, camera):
        self.grab_start_camera = camera

    def OnGrabStarted(self, camera):
        self.grab_started_camera = camera

    def OnGrabStop(self, camera):
        self.grab_stop_camera = camera

    def OnGrabStopped(self, camera):
        self.grab_stopped_camera = camera

    def OnGrabError(self, camera, errorMessage):
        self.grab_error_camera = camera
        self.grab_error_message = errorMessage

    def OnCameraDeviceRemoved(self, camera):
        self.camera_device_removed_camera = camera

    def OnConfigurationRegistered(self, camera):
        self.configuration_registered_camera = camera

    def OnConfigurationDeregistered(self, camera):
        self.configuration_deregistered_camera = camera


class ConfigurationEventHandlerTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid handler object."""
        handler = pylon.ConfigurationEventHandler()
        self.assertIsNotNone(handler)

    def test_copy_construction(self):
        """Copy construction produces a valid handler object."""
        original = pylon.ConfigurationEventHandler()
        handler_copy = pylon.ConfigurationEventHandler(original)
        self.assertIsNotNone(handler_copy)

    # ------------------------------------------------------------------
    # OnAttach / OnAttached
    # ------------------------------------------------------------------

    def test_on_attach_and_on_attached(self):
        """OnAttach and OnAttached are called with the correct camera when a device is attached."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                self.assertEqual(handler.attach_camera.CameraContext, 4711)
                self.assertEqual(handler.attached_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnDetach / OnDetached
    # ------------------------------------------------------------------

    def test_on_detach_and_on_detached(self):
        """OnDetach and OnDetached are called with the correct camera when the device is detached."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.DetachDevice()
                self.assertEqual(handler.detach_camera.CameraContext, 4711)
                self.assertEqual(handler.detached_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnDestroy / OnDestroyed
    # ------------------------------------------------------------------

    def test_on_destroy_and_on_destroyed(self):
        """OnDestroy and OnDestroyed are called with the correct camera when the device is destroyed."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.DestroyDevice()
                self.assertEqual(handler.destroy_camera.CameraContext, 4711)
                self.assertEqual(handler.destroyed_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnOpen / OnOpened
    # ------------------------------------------------------------------

    def test_on_open_and_on_opened(self):
        """OnOpen and OnOpened are called with the correct camera when the camera is opened."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.Open()
                self.assertEqual(handler.open_camera.CameraContext, 4711)
                self.assertEqual(handler.opened_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnClose / OnClosed
    # ------------------------------------------------------------------

    def test_on_close_and_on_closed(self):
        """OnClose and OnClosed are called with the correct camera when the camera is closed."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.Open()
                camera.Close()
                self.assertEqual(handler.close_camera.CameraContext, 4711)
                self.assertEqual(handler.closed_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnGrabStart / OnGrabStarted
    # ------------------------------------------------------------------

    def test_on_grab_start_and_on_grab_started(self):
        """OnGrabStart and OnGrabStarted are called with the correct camera when grabbing is started."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.Open()
                camera.StartGrabbing()
                self.assertEqual(handler.grab_start_camera.CameraContext, 4711)
                self.assertEqual(handler.grab_started_camera.CameraContext, 4711)
                camera.StopGrabbing()
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnGrabStop / OnGrabStopped
    # ------------------------------------------------------------------

    def test_on_grab_stop_and_on_grab_stopped(self):
        """OnGrabStop and OnGrabStopped are called with the correct camera when grabbing is stopped."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.Open()
                camera.StartGrabbing()
                camera.StopGrabbing()
                self.assertEqual(handler.grab_stop_camera.CameraContext, 4711)
                self.assertEqual(handler.grab_stopped_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnConfigurationRegistered
    # ------------------------------------------------------------------

    def test_on_configuration_registered(self):
        """OnConfigurationRegistered is called with the correct camera when the handler is registered."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                self.assertIsNotNone(handler.configuration_registered_camera)
                self.assertEqual(handler.configuration_registered_camera.CameraContext, 4711)
            finally:
                camera.DeregisterConfiguration(handler)

    # ------------------------------------------------------------------
    # OnConfigurationDeregistered
    # ------------------------------------------------------------------

    def test_on_configuration_deregistered(self):
        """OnConfigurationDeregistered is called with the correct camera when the handler is deregistered."""
        handler = TestConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.CameraContext = 4711
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            camera.DeregisterConfiguration(handler)
            self.assertIsNotNone(handler.configuration_deregistered_camera)
            self.assertEqual(handler.configuration_deregistered_camera.CameraContext, 4711)

    # ------------------------------------------------------------------
    # DestroyConfiguration
    # ------------------------------------------------------------------

    def test_destroy_configuration_called_for_cleanup_delete(self):
        """DestroyConfiguration is called when the handler is deregistered with Cleanup_Delete."""
        call_log = []

        class DestructionTrackingHandler(pylon.ConfigurationEventHandler):
            def __init__(self):
                super().__init__()

            def DestroyConfiguration(self):
                call_log.append(True)

        handler = DestructionTrackingHandler()
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            camera.DeregisterConfiguration(handler)
            self.assertEqual(len(call_log), 1)

    # ------------------------------------------------------------------
    # RegisterConfiguration with None (deregister all)
    # ------------------------------------------------------------------

    def test_register_configuration_none_cleanup_none(self):
        """RegisterConfiguration(None, ..., Cleanup_None) deregisters all handlers without error."""
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(pylon.ConfigurationEventHandler(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # Passing None as handler deregisters all currently registered configuration handlers.
            camera.RegisterConfiguration(None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)

    def test_register_configuration_none_cleanup_delete(self):
        """RegisterConfiguration(None, ..., Cleanup_Delete) deregisters all handlers without error."""
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(pylon.ConfigurationEventHandler(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # Passing None as handler deregisters all currently registered configuration handlers.
            camera.RegisterConfiguration(None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)

    # ------------------------------------------------------------------
    # Base class pass-through
    # ------------------------------------------------------------------

    def test_base_class_lifecycle_callbacks_do_not_raise(self):
        """Base class On* lifecycle methods execute without raising when a plain handler is registered."""
        handler = pylon.ConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.Open()
                camera.StartGrabbing()
                camera.StopGrabbing()
                camera.Close()
            finally:
                camera.DeregisterConfiguration(handler)

    def test_base_class_on_destroy_and_on_destroyed_do_not_raise(self):
        """Base class OnDestroy and OnDestroyed execute without raising when the device is destroyed."""
        handler = pylon.ConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.DestroyDevice()
            finally:
                camera.DeregisterConfiguration(handler)

    def test_base_class_on_detach_and_on_detached_do_not_raise(self):
        """Base class OnDetach and OnDetached execute without raising when the device is detached."""
        handler = pylon.ConfigurationEventHandler()
        with pylon.InstantCamera() as camera:
            camera.RegisterConfiguration(handler, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
            try:
                camera.Attach(self.get_camera_traits(), pylon.FirstFound)
                camera.DetachDevice()
            finally:
                camera.DeregisterConfiguration(handler)

    def test_base_class_on_camera_device_removed_does_not_raise(self):
        """Base class OnCameraDeviceRemoved is directly callable and does not raise."""
        handler = pylon.ConfigurationEventHandler()
        with self.create_first() as camera:
            handler.OnCameraDeviceRemoved(camera)

    def test_base_class_on_grab_error_does_not_raise(self):
        """Base class OnGrabError is directly callable and does not raise."""
        handler = pylon.ConfigurationEventHandler()
        with self.create_first() as camera:
            handler.OnGrabError(camera, "test error message")

if __name__ == "__main__":
    unittest.main()
