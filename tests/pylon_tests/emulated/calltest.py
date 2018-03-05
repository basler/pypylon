from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class CallTestSuite(PylonEmuTestCase):
    # Tests that you can set the GainRaw parameter of the camera
    def test_gain_raw(self):
        cam = self.create_first()
        cam.Open()

        # Set GainRaw to min value (192)
        cam.GainRaw.Value = cam.GainRaw.Min
        self.assertEqual(192, cam.GainRaw.Value)

        # Set GainRaw to max value (1023)
        cam.GainRaw.Value = cam.GainRaw.Max
        self.assertEqual(1023, cam.GainRaw.Value)

        # Set GainRaw to 500
        cam.GainRaw.Value = 500
        self.assertEqual(500, cam.GainRaw.Value)

        cam.Close()

    # Tests that you can set the Height parameter of the camera
    def test_height(self):
        cam = self.create_first()
        cam.Open()

        cam.Height.Value = cam.Height.Min
        self.assertEqual(1, cam.Height.Value)

        cam.Height.Value = cam.Height.Max
        self.assertEqual(4096, cam.Height.Value)

        cam.Height.Value = 500
        self.assertEqual(500, cam.Height.Value)

        cam.Close()

    # Tests that you can set the Width parameter of the camera
    def test_width(self):
        cam = self.create_first()
        cam.Open()

        cam.Width.Value = cam.Width.Min
        self.assertEqual(1, cam.Width.Value)

        cam.Width.Value = cam.Width.Max
        self.assertEqual(4096, cam.Width.Value)

        cam.Width.Value = 500
        self.assertEqual(500, cam.Width.Value)
        cam.Close()

    # Tests that you can set the ExposureTimeRaw parameter of the camera
    def test_exposure_time_raw(self):
        cam = self.create_first()
        cam.Open()

        cam.ExposureTimeRaw.Value = cam.ExposureTimeRaw.Min
        self.assertEqual(100, cam.ExposureTimeRaw.Value)

        cam.ExposureTimeRaw.Value = cam.ExposureTimeRaw.Max
        self.assertEqual(3000000, cam.ExposureTimeRaw.Value)

        cam.ExposureTimeRaw.Value = 1000
        self.assertEqual(1000, cam.ExposureTimeRaw.Value)

        cam.Close()

    # Tests that an emulated camera has no hardware interface
    def test_has_hardware_interface(self):
        cam = self.create_first()
        cam.Open()

        self.assertFalse(cam.Is1394())
        self.assertFalse(cam.IsUsb())
        self.assertFalse(cam.IsCameraLink())
        self.assertFalse(cam.IsGigE())

        cam.Close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
