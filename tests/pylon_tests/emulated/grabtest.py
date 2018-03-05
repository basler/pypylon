from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import numpy
import unittest


class GrabTestSuite(PylonEmuTestCase):
    def test_grabone(self):

        camera = self.create_first()
        camera.Open()
        camera.ExposureTimeAbs.SetValue(10000.0)
        self.assertEqual(10000, camera.ExposureTimeAbs.GetValue())
        result = camera.GrabOne(1000)
        self.assertEqual(9.5, numpy.mean(result.Array[0:20, 0]))
        camera.Close()

    def test_grab(self):
        countOfImagesToGrab = 5
        imageCounter = 0
        camera = self.create_first()
        camera.Open()
        camera.ExposureTimeAbs.SetValue(10000.0)
        self.assertEqual(10000, camera.ExposureTimeAbs.GetValue())
        camera.StartGrabbingMax(countOfImagesToGrab)
        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                imageCounter = imageCounter + 1
                self.assertEqual(1024, grabResult.Width)
                self.assertEqual(1040, grabResult.Height)
                img = grabResult.Array
            grabResult.Release()
        self.assertEqual(countOfImagesToGrab, imageCounter)
        camera.Close()

    def test_grab_multiple_cameras(self):
        twoCamsUsed = False
        # Number of images to be grabbed.
        countOfImagesToGrab = 10
        # Limits the amount of cameras used for grabbing.
        maxCamerasToUse = 2
        # Get the transport layer factory.
        tlFactory = pylon.TlFactory.GetInstance()
        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices(self.device_filter)
        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
        l = cameras.GetSize()
        self.assertEqual(2, l)  # Are 2 Cameras initialized
        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(tlFactory.CreateDevice(devices[i]))
        # Starts grabbing for all cameras
        cameras.StartGrabbing()
        # Grab c_countOfImagesToGrab from the cameras.
        for i in range(countOfImagesToGrab):
            if not cameras.IsGrabbing():
                break
            grabResult = cameras.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            cameraContextValue = grabResult.GetCameraContext()
            if (cameraContextValue == 1):
                twoCamsUsed = True
            # Now, the image data can be processed.
            self.assertEqual(True, grabResult.GrabSucceeded())
            img = grabResult.GetArray()
            first_line = img[0]
            prev = first_line[0]
            for pxl in first_line[1:]:
                self.assertEqual(pxl, (prev + 1) % 256)
                prev = pxl
        self.assertTrue(twoCamsUsed)  # Are 2 Cameras actually used


if __name__ == "__main__":
    unittest.main()
