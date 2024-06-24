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
        camera.Width.Value = 1024
        camera.Height.Value = 1040
        camera.PixelFormat.Value = "Mono8"
        grabResult = camera.GrabOne(1000)
        camera.Close()

        self.assertTrue(grabResult.IsValid())
        self.assertTrue(grabResult.IsUnique())
        ((height, width), dtype, form) = grabResult.GetImageFormat()
        self.assertEqual(1040, height)
        self.assertEqual(1024, width)
        self.assertEqual("B", form)
        actual = list(grabResult.Array[0:20, 0])
        expected = [actual[0] + i for i in range(20)]
        self.assertEqual(actual, expected)

        self.assertEqual(grabResult.GetDataComponentCount(), 1)
        self.assertEqual(grabResult.DataComponentCount, 1)
        container = grabResult.DataContainer;
        self.assertEqual(container.DataComponentCount, 1)
        container.Release()
        container = grabResult.GetDataContainer();
        self.assertEqual(container.DataComponentCount, 1)
        container.Release()
        component = grabResult.GetDataComponent(0)
        self.assertEqual(component.Width, 1024)
        component.Release()

        grabResult.Release()
        self.assertFalse(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        self.assertRaises(genicam.RuntimeException, grabResult.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grabResult.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grabResult.GetArray)

    def test_copy(self):
        camera = self.create_first()

        camera.Open()
        camera.Width.Value = 1024
        camera.Height.Value = 1040
        camera.PixelFormat.Value = "Mono8"
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
        actual = list(grabResult.Array[0:20, 0])
        expected = [actual[0] + i for i in range(20)]
        self.assertEqual(actual, expected)

        cameraGrab.Release()
        self.assertTrue(grabResult.IsValid())
        self.assertTrue(grabResult.IsUnique())
        ((height, width), dtype, form) = grabResult.GetImageFormat()
        self.assertEqual(1040, height)
        self.assertEqual(1024, width)
        self.assertEqual("B", form)
        actual = list(grabResult.Array[0:20, 0])
        expected = [actual[0] + i for i in range(20)]
        self.assertEqual(actual, expected)

        grabResult.Release()
        self.assertFalse(grabResult.IsValid())
        self.assertFalse(grabResult.IsUnique())
        self.assertRaises(genicam.RuntimeException, grabResult.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grabResult.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grabResult.GetArray)

    def test_zerocopy_access(self):
        camera = self.create_first()

        camera.Open()
        camera.Width.Value = 1024
        camera.Height.Value = 1040
        camera.PixelFormat.Value = "Mono8"
        cameraGrab = camera.GrabOne(1000)
        camera.Close()

        self.assertTrue(cameraGrab.IsValid())
        with cameraGrab.GetArrayZeroCopy() as zc:
            self.assertTrue(zc.shape[0] == 1040)
            self.assertTrue(zc.shape[1] == 1024)

    def test_zerocopy_access_exception(self):
        camera = self.create_first()

        camera.Open()
        camera.Width.Value = 1024
        camera.Height.Value = 1040
        camera.PixelFormat.Value = "Mono8"
        cameraGrab = camera.GrabOne(1000)
        camera.Close()

        self.assertTrue(cameraGrab.IsValid())
        with self.assertRaises(RuntimeError) as context:
            with cameraGrab.GetArrayZeroCopy() as zc:
                self.assertTrue(zc.shape[0] == 1040)
                self.assertTrue(zc.shape[1] == 1024)
                external_ref = zc
        self.assertEqual(str(context.exception), "Please remove any references to the array before leaving context manager scope!!!")

if __name__ == "__main__":
    unittest.main()
