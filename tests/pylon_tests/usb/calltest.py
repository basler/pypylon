from pylonusbtestcase import PylonTestCase
from pypylon import pylon
import unittest


class CallTestSuite(PylonTestCase):
    # Tests that you can set the Gain parameter of the camera
    def test_gain(self):
        cam = self.create_first()
        cam.Open()

        # Set Gain to min value
        cam.Gain.Value = cam.Gain.Min
        self.assertEqual(cam.Gain.Min, cam.Gain.Value)

        # Set Gain to max value
        cam.Gain.Value = cam.Gain.Max
        self.assertEqual(cam.Gain.Max, cam.Gain.Value)

        cam.Close()

    # Tests that you can set the Height parameter of the camera
    def test_height(self):
        cam = self.create_first()
        cam.Open()

        cam.Height.Value = cam.Height.Min
        self.assertEqual(cam.Height.Min, cam.Height.Value)

        cam.Height.Value = cam.Height.Max
        self.assertEqual(cam.Height.Max, cam.Height.Value)

        cam.Height.Value = 500
        self.assertEqual(500, cam.Height.Value)

        cam.Close()

    # Tests that you can set the Width parameter of the camera
    def test_width(self):
        cam = self.create_first()
        cam.Open()

        cam.Width.Value = cam.Width.Min
        self.assertEqual(cam.Width.Min, cam.Width.Value)

        cam.Width.Value = cam.Width.Max
        self.assertEqual(cam.Width.Max, cam.Width.Value)

    # Tests that you can set the ExposureTime parameter of the camera
    def test_exposure_time(self):
        cam = self.create_first()
        cam.Open()

        cam.ExposureTime.Value = cam.ExposureTime.Min
        self.assertEqual(cam.ExposureTime.Min, cam.ExposureTime.Value)

        cam.ExposureTime.Value = cam.ExposureTime.Max
        self.assertEqual(cam.ExposureTime.Max, cam.ExposureTime.Value)

        cam.ExposureTime.Value = 1000
        self.assertEqual(1000, cam.ExposureTime.Value)

        cam.Close()

    # Tests that a usb camera only has a usb hardware interface
    def test_hardware_interface(self):
        cam = self.create_first()
        cam.Open()

        self.assertFalse(cam.Is1394())
        self.assertTrue(cam.IsUsb())
        self.assertFalse(cam.IsCameraLink())
        self.assertFalse(cam.IsGigE())

        cam.Close()


if __name__ == "__main__":
    unittest.main()
