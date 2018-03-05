from pylongigetestcase import PylonTestCase
from pypylon import pylon
import unittest


class CallTestSuite(PylonTestCase):
    # Tests that you can set the GainRaw parameter of the camera
    def test_Gain(self):
        cam = self.create_first()
        cam.Open()

        # Set GainRaw to min value (192)
        cam.GainRaw.Value = cam.GainRaw.Max
        self.assertEqual(cam.GainRaw.Max, cam.GainRaw.Max)

        # Set GainRaw to max value (1023)
        cam.GainRaw.Value = cam.GainRaw.Max
        self.assertEqual(cam.GainRaw.Max, cam.GainRaw.Value)

        cam.Close()

    # Tests that you can set the Height parameter of the camera
    def test_Height(self):
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
    def test_Width(self):
        cam = self.create_first()
        cam.Open()

        cam.Width.Value = cam.Width.Min
        self.assertEqual(cam.Width.Min, cam.Width.Value)

        cam.Width.Value = cam.Width.Max
        self.assertEqual(cam.Width.Max, cam.Width.Value)

    # Tests that an emulated camera has no hardware interface
    def test_hasHardwareInterface(self):
        cam = self.create_first()
        cam.Open()

        self.assertFalse(cam.Is1394())
        self.assertFalse(cam.IsUsb())
        self.assertFalse(cam.IsCameraLink())
        self.assertTrue(cam.IsGigE())

        cam.Close()


if __name__ == "__main__":
    unittest.main()
