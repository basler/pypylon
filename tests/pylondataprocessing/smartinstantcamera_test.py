"""\
This unit test checks the SmartInstantCamera API of pylondataprocessing.

It exercises construction, loading recipes, opening, grabbing (with and without
a running recipe) and the SmartResult event handler.
A Basler Camera Emulation device is required (configured via PYLON_CAMEMU).
"""
import os
num = 1
if int(os.environ.get("PYLON_CAMEMU", 0)) < num:
    os.environ["PYLON_CAMEMU"] = "%d" % num
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest


def _cleanup_camera(camera):
    """Close, unload and destroy a SmartInstantCamera, ignoring all errors."""
    if camera is None:
        return
    camera.Close()  # never throws
    camera.Unload()  # never throws
    camera.DestroyDevice()  # never throws


class TSmartResultEventHandler(pylondataprocessing.SmartResultEventHandler):
    """Records results and errors delivered through the SmartResult event handler."""

    def __init__(self):
        pylondataprocessing.SmartResultEventHandler.__init__(self)
        self.Result = None
        self.Camera = None
        self.Message = None
        self.OnResultCallCount = 0
        self.OnDataProcessingErrorCallCount = 0

    def OnResult(self, camera, result):
        self.Result = result
        self.Camera = camera
        self.OnResultCallCount += 1

    def OnDataProcessingError(self, camera, message):
        self.Camera = camera
        self.Message = message
        self.OnDataProcessingErrorCallCount += 1


class SmartInstantCameraTestSuite(PylonDataProcessingTestCase):

    def get_filter(self):
        """Return a device-info filter that selects the Basler Camera Emulation device class."""
        device_class = "BaslerCamEmu"
        device_info = pylon.DeviceInfo()
        device_info.SetDeviceClass(device_class)
        return device_info

    # ------------------------------------------------------------------
    # Construction / recipe filename
    # ------------------------------------------------------------------

    def test_constructor(self):
        """SmartInstantCamera supports default, device and device-plus-recipe construction."""
        camera = None
        camera_with_device = None
        camera_with_recipe = None
        try:
            # CSmartInstantCameraT()
            camera = pylondataprocessing.SmartInstantCamera()
            self.assertEqual(camera.GetRecipeFilename(), "")
            self.assertFalse(camera.IsLoaded())
            self.assertFalse(camera.IsOpen())
            self.assertFalse(camera.IsGrabbing())
            self.assertFalse(camera.IsPylonDeviceAttached())
            # CSmartInstantCameraT(IPylonDevice* pDevice, ECleanup cleanupProcedure = Cleanup_Delete)
            camera_with_device = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
            self.assertEqual(camera_with_device.GetRecipeFilename(), "")
            self.assertFalse(camera_with_device.IsLoaded())
            self.assertFalse(camera_with_device.IsOpen())
            self.assertFalse(camera_with_device.IsGrabbing())
            self.assertTrue(camera_with_device.IsPylonDeviceAttached())
            # CSmartInstantCameraT(IPylonDevice* pDevice, const String_t& filename, ECleanup cleanupProcedure = Cleanup_Delete)
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera_with_recipe = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            self.assertEqual(camera_with_recipe.GetRecipeFilename(), recipe_filename)
            self.assertFalse(camera_with_recipe.IsLoaded())
            self.assertFalse(camera_with_recipe.IsOpen())
            self.assertFalse(camera_with_recipe.IsGrabbing())
            self.assertTrue(camera_with_recipe.IsPylonDeviceAttached())
        finally:
            _cleanup_camera(camera)
            _cleanup_camera(camera_with_device)
            _cleanup_camera(camera_with_recipe)

    def test_set_recipe_filename(self):
        """SetRecipeFilename stores the recipe path on the camera."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera()
            self.assertEqual(camera.GetRecipeFilename(), "")
            camera.SetRecipeFilename(recipe_filename)
            self.assertEqual(camera.GetRecipeFilename(), recipe_filename)
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # Loading recipes
    # ------------------------------------------------------------------

    def test_load(self):
        """Load loads a recipe without setting the recipe filename."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera()
            self.assertEqual(camera.GetRecipeFilename(), "")
            self.assertFalse(camera.IsLoaded())
            camera.Load(recipe_filename)
            self.assertTrue(camera.IsLoaded())
            self.assertEqual(camera.GetRecipeFilename(), "")
        finally:
            _cleanup_camera(camera)

    def test_load_from_binary(self):
        """LoadFromBinary loads a recipe from in-memory file content."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            with open(recipe_filename, mode='rb') as file:
                file_content = file.read()
            camera = pylondataprocessing.SmartInstantCamera()
            self.assertFalse(camera.IsLoaded())
            camera.LoadFromBinary(file_content)
            self.assertTrue(camera.IsLoaded())
            camera.Unload()
            self.assertFalse(camera.IsLoaded())
            camera.LoadFromBinary(file_content, this_dir)
            self.assertTrue(camera.IsLoaded())
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # Open / resources
    # ------------------------------------------------------------------

    def test_open(self):
        """Open and Close toggle the open state of the camera."""
        camera = None
        try:
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
            camera.Open()
            self.assertTrue(camera.IsOpen())
            camera.Close()
            self.assertFalse(camera.IsOpen())
        finally:
            _cleanup_camera(camera)

    def test_preallocate_resources(self):
        """PreAllocateResources and DeallocateResources allocate and free vTool resources."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_preallocate_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
            camera.Load(recipe_filename)
            self.assertFalse(camera.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())
            camera.PreAllocateResources()
            self.assertTrue(camera.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())
            camera.DeallocateResources()
            self.assertFalse(camera.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # Grabbing
    # ------------------------------------------------------------------

    def test_start_grabbing(self):
        """The various StartGrabbing overloads grab the requested number of images."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)

            camera.Open()
            camera.StartGrabbingMax(3, pylon.GrabStrategy_OneByOne)
            num_grabbed = 0
            while camera.IsGrabbing():
                num_grabbed += 1
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(result.GrabResult.GrabSucceeded())
                self.assertEqual(num_grabbed, result.GrabResult.ImageNumber)
            self.assertFalse(camera.IsGrabbing())
            camera.Close()

            camera.Open()
            # StartGrabbing for an amount of images while starting the recipe.
            camera.StartGrabbingMax(
                True, 3, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            self.assertTrue(camera.IsLoaded())
            self.assertTrue(camera.IsOpen())
            self.assertTrue(camera.IsGrabbing())
            self.assertTrue(camera.IsPylonDeviceAttached())
            num_grabbed = 0
            while camera.IsGrabbing():
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                num_grabbed += 1
                self.assertTrue(result.GrabResult.GrabSucceeded())
                self.assertEqual(num_grabbed, result.GrabResult.ImageNumber)
            self.assertFalse(camera.IsGrabbing())
            camera.Close()
            self.assertEqual(num_grabbed, 3)
            self.assertFalse(camera.IsLoaded())
            self.assertFalse(camera.IsOpen())
            self.assertFalse(camera.IsGrabbing())
            self.assertTrue(camera.IsPylonDeviceAttached())

            camera.Open()
            camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser)
            num_grabbed = 0
            while camera.IsGrabbing() and num_grabbed < 5:
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(result.GrabResult.GrabSucceeded())
                num_grabbed += 1
                self.assertEqual(num_grabbed, result.GrabResult.ImageNumber)
            camera.StopGrabbing()
            self.assertFalse(camera.IsGrabbing())
            camera.Close()

            camera.Open()
            camera.StartGrabbing(
                True, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            num_grabbed = 0
            while camera.IsGrabbing() and num_grabbed < 5:
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(result.GrabResult.GrabSucceeded())
                num_grabbed += 1
                self.assertEqual(num_grabbed, result.GrabResult.ImageNumber)
            camera.StopGrabbing(1000)
            self.assertFalse(camera.IsGrabbing())
            camera.Close()
        finally:
            _cleanup_camera(camera)

    def test_retrieve_result(self):
        """RetrieveResult returns a populated container while a recipe is running."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            camera.Load(recipe_filename)

            camera.Open()
            camera.StartGrabbing(
                True, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            num_grabbed = 0
            while camera.IsGrabbing() and num_grabbed < 5:
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(result.GrabResult.GrabSucceeded())
                self.assertTrue(len(result.GetContainer()) > 0)
                num_grabbed += 1
                self.assertEqual(num_grabbed, result.GrabResult.ImageNumber)
            camera.StopGrabbing(1000)
        finally:
            _cleanup_camera(camera)

    def test_grab_one(self):
        """GrabOne grabs a single image with and without a running recipe."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)

            grab_result = camera.GrabOne(1000)
            # Got valid data.
            self.assertTrue(grab_result.IsValid())
            self.assertTrue(grab_result.GrabSucceeded())
            # Grabbing is stopped afterwards.
            self.assertFalse(camera.IsGrabbing())

            # Test with running recipe.
            smart_grab_result = camera.GrabOne(True, 1000)
            # Got valid data.
            self.assertTrue(len(smart_grab_result.GetContainer()) > 0)
            self.assertTrue(smart_grab_result.GrabResult.IsValid())
            self.assertTrue(smart_grab_result.GrabResult.GrabSucceeded())
            # Grabbing is stopped afterwards.
            self.assertFalse(camera.IsGrabbing())

            # Test without running recipe.
            smart_grab_result = camera.GrabOne(False, 1000)
            # Got valid data.
            self.assertTrue(len(smart_grab_result.GetContainer()) == 0)
            self.assertTrue(smart_grab_result.GrabResult.IsValid())
            self.assertTrue(smart_grab_result.GrabResult.GrabSucceeded())
            # Grabbing is stopped afterwards.
            self.assertFalse(camera.IsGrabbing())
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # SmartResult event handler
    # ------------------------------------------------------------------

    def test_register_smart_result_event_handler(self):
        """A registered SmartResult event handler receives results until it is deregistered."""
        camera = None
        smart_result_handler = TSmartResultEventHandler()
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            camera.Open()
            camera.SetCameraContext(1234)

            # Grab with registered event handler.
            camera.RegisterSmartResultEventHandler(
                smart_result_handler, pylon.RegistrationMode_Append, pylon.Cleanup_None)
            camera.StartGrabbingMax(
                True, 3, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            num_grabbed = 0
            while camera.IsGrabbing():
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                num_grabbed += 1
                self.assertTrue(result.GrabResult.GrabSucceeded())
                self.assertEqual(smart_result_handler.Result.Container, result.Container)
                self.assertEqual(smart_result_handler.Result.GrabResult.ImageNumber, result.GrabResult.ImageNumber)
                self.assertEqual(smart_result_handler.Camera.CameraContext, 1234)
                self.assertEqual(smart_result_handler.Message, None)
            self.assertEqual(num_grabbed, 3)
            self.assertFalse(camera.IsGrabbing())
            self.assertEqual(smart_result_handler.OnResultCallCount, 3)
            self.assertEqual(smart_result_handler.OnDataProcessingErrorCallCount, 0)

            # Grab with deregistered event handler.
            num_grabbed = 0
            self.assertTrue(camera.DeregisterSmartResultEventHandler(smart_result_handler))
            self.assertFalse(camera.DeregisterSmartResultEventHandler(smart_result_handler))
            camera.StartGrabbingMax(
                True, 3, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            while camera.IsGrabbing():
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                self.assertTrue(result.GrabResult.GrabSucceeded())
                num_grabbed += 1
            self.assertEqual(num_grabbed, 3)
            self.assertFalse(camera.IsGrabbing())
            self.assertEqual(smart_result_handler.OnResultCallCount, 3)
            self.assertEqual(smart_result_handler.OnDataProcessingErrorCallCount, 0)
            camera.Close()
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # RegisterSmartResultEventHandler with None (deregister all)
    # ------------------------------------------------------------------

    def test_register_smart_result_event_handler_none_cleanup_none(self):
        """RegisterSmartResultEventHandler(None, ..., Cleanup_None) deregisters all handlers without error."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            camera.RegisterSmartResultEventHandler(pylondataprocessing.SmartResultEventHandler(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # Passing None as handler deregisters all currently registered SmartResult event handlers.
            camera.RegisterSmartResultEventHandler(None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
        finally:
            _cleanup_camera(camera)

    def test_register_smart_result_event_handler_none_cleanup_delete(self):
        """RegisterSmartResultEventHandler(None, ..., Cleanup_Delete) deregisters all handlers without error."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            camera.RegisterSmartResultEventHandler(pylondataprocessing.SmartResultEventHandler(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            # Passing None as handler deregisters all currently registered SmartResult event handlers.
            camera.RegisterSmartResultEventHandler(None, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
        finally:
            _cleanup_camera(camera)

    # ------------------------------------------------------------------
    # Wait objects
    # ------------------------------------------------------------------

    def test_wait_object(self):
        """GetGrabStopWaitObject signals when grabbing stops."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)

            camera.StartGrabbingMax(
                True, 10, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByInstantCamera)
            self.assertTrue(camera.GetGrabStopWaitObject().Wait(15000))
            self.assertFalse(camera.IsGrabbing())

            camera.StartGrabbing(
                True, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByInstantCamera)
            self.assertFalse(camera.GetGrabStopWaitObject().Wait(0))
            self.assertTrue(camera.IsGrabbing())
            camera.StopGrabbing()
        finally:
            _cleanup_camera(camera)

    def test_get_smart_result_wait_object(self):
        """GetSmartResultWaitObject signals when a smart result is available after a software trigger."""
        camera = None
        try:
            this_dir = os.path.dirname(__file__)
            recipe_filename = os.path.join(this_dir, 'smartinstantcamera_test.precipe')
            camera = pylondataprocessing.SmartInstantCamera(
                pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipe_filename)
            camera.RegisterConfiguration(
                pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
            camera.Open()
            camera.StartGrabbingMax(
                True, 5, pylon.GrabStrategy_OneByOne,
                pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
            while camera.IsGrabbing():
                camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException)
                camera.ExecuteSoftwareTrigger()
                camera.GetSmartResultWaitObject().Wait(5000)
                result = camera.RetrieveResult(5000, pylon.TimeoutHandling_Return)
                self.assertTrue(result.GrabResult.IsValid())
                self.assertTrue(result.GrabResult.GrabSucceeded())
                self.assertTrue(result.Update.IsValid())
                self.assertTrue(len(result.Container) == 4)
        finally:
            _cleanup_camera(camera)


if __name__ == "__main__":
    unittest.main()
