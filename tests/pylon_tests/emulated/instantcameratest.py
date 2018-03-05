from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import numpy
import unittest


class InstantCameraTestSuite(PylonEmuTestCase):
    def test_open_device(self):
        cam = pylon.InstantCamera()
        self.assertFalse(cam.IsOpen())
        cam = self.create_first()
        cam.Open()
        self.assertTrue(cam.IsOpen())
        cam.Close()
        self.assertFalse(cam.IsOpen())

    def test_attach(self):
        cam = pylon.InstantCamera()
        self.assertFalse(cam.IsPylonDeviceAttached())
        dev = pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        cam.Attach(dev)
        cam.Open()
        self.assertTrue(cam.IsPylonDeviceAttached())
        cam.DetachDevice()
        self.assertFalse(cam.IsPylonDeviceAttached())

    def test_destroy_device(self):
        cam = self.create_first()
        cam.Open()
        cam.DestroyDevice()
        self.assertFalse(cam.IsPylonDeviceAttached())
        self.assertFalse(cam.IsOpen())

    def test_grab_one(self):
        cam = self.create_first()
        cam.Open()
        self.assertTrue(cam.GrabOne(1000))
        result = cam.GrabOne(1000)
        self.assertEqual(9.5, numpy.mean(result.Array[0:20, 0]))
        cam.Close()

    def test_grabbing(self):
        cam = self.create_first()
        cam.Open()
        self.assertFalse(cam.IsGrabbing())
        cam.StartGrabbing()
        self.assertTrue(cam.IsGrabbing())
        i = 0
        while (i < 10):
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                self.assertEqual(1024, grabResult.Width)
                self.assertEqual(1040, grabResult.Height)
                img = grabResult.Array
            grabResult.Release()
            self.assertTrue(cam.IsGrabbing())
            i = i + 1
        cam.StopGrabbing()
        self.assertFalse(cam.IsGrabbing())
        cam.Close()

    def test_has_hardware_interface(self):
        cam = self.create_first()
        cam.Open()
        self.assertFalse(cam.Is1394())
        self.assertFalse(cam.IsUsb())
        self.assertFalse(cam.IsCameraLink())
        self.assertFalse(cam.IsGigE())

        cam.Close()

        #######################################################
        # Can't test Eventhandlers with Emulated Cameras      #
        # Can't test Softwaretrigger with Emulated Cameras    #
        #######################################################


if __name__ == "__main__":
    unittest.main()
