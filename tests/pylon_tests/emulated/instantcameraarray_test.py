from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class InstantCameraArrayTestSuite(PylonEmuTestCase):
    def test_constructor_empty(self):
        cameraArray = pylon.InstantCameraArray()
        self.assertEqual(0, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())
        # Test if no Camera is connected
        for cam in cameraArray:
            self.fail()

    def test_initialize(self):
        cameraArray = pylon.InstantCameraArray()
        self.assertEqual(0, cameraArray.GetSize())
        cameraArray.Initialize(self.num_dev)
        self.assertEqual(self.num_dev, cameraArray.GetSize())
        v = 0
        for cam in cameraArray:
            v += 1
        self.assertEqual(self.num_dev, v)

    def test_connect_cameras(self):
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        self.assertEqual(len(devices), self.num_dev)
        cameraArray = pylon.InstantCameraArray(self.num_dev)
        for i, cam in enumerate(cameraArray):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.Open()

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.StartGrabbing()

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertTrue(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.RetrieveResult(300)

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertTrue(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.StopGrabbing()

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertTrue(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.Close()

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertTrue(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

        cameraArray.DestroyDevice()

        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())

    def test_detach_cameras(self):

        cameraArray = pylon.InstantCameraArray(self.num_dev)
        devices = pylon.TlFactory.GetInstance().EnumerateDevices(self.device_filter)
        self.assertEqual(len(devices), self.num_dev)
        for i, cam in enumerate(cameraArray):
            self.assertEqual(devices[i].GetDeviceClass(), self.device_class)
            cam.Attach(pylon.TlFactory.GetInstance().CreateDevice(devices[i]))

        cameraArray.Open()
        cameraArray.StartGrabbing()
        cameraArray.DetachDevice()
        self.assertEqual(self.num_dev, cameraArray.GetSize())
        self.assertFalse(cameraArray.IsGrabbing())
        self.assertFalse(cameraArray.IsOpen())
        self.assertFalse(cameraArray.IsPylonDeviceAttached())
        self.assertFalse(cameraArray.IsCameraDeviceRemoved())


if __name__ == "__main__":
    unittest.main()
