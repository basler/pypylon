from pylonusbtestcase import PylonTestCase
from pypylon import pylon
import unittest


class GrabTestSuite(PylonTestCase):
    # test from sample grabone
    def test_grabone(self):

        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        camera.ExposureTime.SetValue(camera.ExposureTime.Min)
        grabResult = camera.GrabOne(1000)
        self.assertEqual(camera.Width.Max, grabResult.Width)
        self.assertEqual(camera.Height.Max, grabResult.Height)
        camera.Close()

    # test from Grab sample
    def test_grab(self):
        countOfImagesToGrab = 5
        imageCounter = 0
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        camera.Open()

        camera.Width.Value = camera.Width.Max
        camera.Height.Value = camera.Height.Max
        camera.ExposureTime.SetValue(camera.ExposureTime.Min)

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
                self.assertEqual(camera.Width.Max, grabResult.Width)
                self.assertEqual(camera.Height.Max, grabResult.Height)
                img = grabResult.Array
            grabResult.Release()
        self.assertEqual(countOfImagesToGrab, imageCounter)
        camera.Close()

    def disabled_test_grab_multiple_cameras(self):
        twoCamsUsed = False
        # Number of images to be grabbed.
        countOfImagesToGrab = 10
        # Limits the amount of cameras used for grabbing.
        maxCamerasToUse = 2
        # Get the transport layer factory.
        tlFactory = pylon.TlFactory.GetInstance()
        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices()
        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
        l = cameras.GetSize()
        self.assertEqual(2, l)  # Are 2 Cameras initialized
        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))
            # Print the model name of the camera.
            print("Using device ", cam.GetDeviceInfo().GetModelName())
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
            self.assertEqual(0, img[0, 0])
        self.assertTrue(twoCamsUsed)  # Are 2 Cameras actually used


if __name__ == "__main__":
    unittest.main()
