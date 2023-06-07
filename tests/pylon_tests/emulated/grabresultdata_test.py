from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class GrabResultDataTestSuite(PylonEmuTestCase):
    def test_emu_grabresultdata(self):
        camera = self.create_first()

        camera.Open()
        grabResult = camera.GrabOne(1000)
        camera.Close()

        self.assertTrue(grabResult.GrabSucceeded())
        self.assertEqual(0, grabResult.GetErrorCode())
        self.assertEqual(pylon.PayloadType_Image, grabResult.GetPayloadType())
        self.assertEqual(pylon.PixelType_Mono8, grabResult.GetPixelType())
        self.assertEqual(1024, grabResult.GetWidth())
        self.assertEqual(1040, grabResult.GetHeight())

        self.assertEqual(0, grabResult.GetOffsetX())
        self.assertEqual(0, grabResult.GetOffsetY())
        self.assertEqual(0, grabResult.GetPaddingX())
        self.assertEqual(0, grabResult.GetPaddingY())
        self.assertEqual(1024 * 1040, grabResult.GetImageSize())


if __name__ == "__main__":
    unittest.main()
