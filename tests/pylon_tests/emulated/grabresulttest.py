from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import unittest


class GrabResultTestSuite(PylonEmuTestCase):
    def test_constructor(self):
        grabResult = pylon.GrabResult()
        self.assertFalse(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        self.assertRaises(genicam.RuntimeException, grabResult.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grabResult.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grabResult.GetArray)
        grabResult.Release()

    def test_emu_grabresult(self):
        camera = self.create_first()

        camera.Open()
        grabResult = camera.GrabOne(1000)
        camera.Close()

        self.assertTrue(grabResult.IsValid())
        self.assertTrue(grabResult.IsUnique())
        ((height, width), dtype, form) = grabResult.GetImageFormat()
        self.assertEqual(1040, height)
        self.assertEqual(1024, width)
        self.assertEqual("B", form)
        self.assertTrue(grabResult.GetArray()[0, 1] == 1)
        grabResult.Release()
        self.assertFalse(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        self.assertRaises(genicam.RuntimeException, grabResult.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grabResult.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grabResult.GetArray)

    def test_copy(self):
        camera = self.create_first()

        camera.Open()
        cameraGrab = camera.GrabOne(1000)
        camera.Close()

        # Create a copy of the GrabResult
        grabResult = pylon.GrabResult(cameraGrab)

        self.assertTrue(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        ((height, width), dtype, form) = grabResult.GetImageFormat()
        self.assertEqual(1040, height)
        self.assertEqual(1024, width)
        self.assertEqual("B", form)
        self.assertTrue(grabResult.GetArray()[0, 1] == 1)

        cameraGrab.Release()
        self.assertTrue(grabResult.IsValid())
        self.assertTrue(grabResult.IsUnique())
        ((height, width), dtype, form) = grabResult.GetImageFormat()
        self.assertEqual(1040, height)
        self.assertEqual(1024, width)
        self.assertEqual("B", form)
        self.assertTrue(grabResult.GetArray()[0, 1] == 1)

        grabResult.Release()
        self.assertFalse(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        self.assertRaises(genicam.RuntimeException, grabResult.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grabResult.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grabResult.GetArray)


if __name__ == "__main__":
    unittest.main()
