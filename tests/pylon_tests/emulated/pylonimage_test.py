from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import unittest
import os

class PylonImageTestSuite(PylonEmuTestCase):

    def test_empty_pylon_image(self):
        testee = pylon.PylonImage()
        self.assertEqual(testee.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(testee.IsValid(), False)
        self.assertEqual(testee.Width, 0)
        self.assertEqual(testee.Height, 0)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.ImageSize, 0)
        self.assertEqual(testee.AllocatedBufferSize, 0)
        self.assertEqual(testee.Orientation, pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.GetPixelType(), pylon.PixelType_Undefined)
        self.assertEqual(testee.GetWidth(), 0)
        self.assertEqual(testee.GetHeight(), 0)
        self.assertEqual(testee.GetPaddingX(), 0)
        self.assertEqual(testee.GetImageSize(), 0)
        self.assertEqual(testee.GetOrientation(), pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.GetAllocatedBufferSize(), 0)
        try:
            testee.ImageFormat
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            testee.GetImageFormat()
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        try:
            testee.Array
        except ValueError:
            pass
        else:
            self.fail("Exception not raised.")
        testee.Buffer

    def test_container_load(self):
        testee = pylon.PylonImage()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'barcode01.png')
        testee.Load(filename)
        self.assertEqual(testee.PixelType, pylon.PixelType_Mono8)
        self.assertEqual(testee.IsValid(), True)
        self.assertEqual(testee.Width, 1920)
        self.assertEqual(testee.Height, 1200)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.ImageSize, 1920 * 1200)
        self.assertEqual(testee.AllocatedBufferSize, 1920 * 1200)
        self.assertEqual(testee.Orientation, pylon.ImageOrientation_TopDown)
        self.assertEqual(testee.Array[0,0], 143)
        self.assertEqual(testee.GetBuffer()[0], 143)
        self.assertEqual(testee.GetMemoryView()[0], 143)
        testee.Release()

    def test_container_load_zero_copy(self):
        testee = pylon.PylonImage()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'barcode01.png')
        testee.Load(filename)
        with testee.GetArrayZeroCopy() as zc:
            self.assertEqual(zc[0,0], 143)
        testee.Release()

    def test_attacharray(self):
        import numpy as np
        import sys

        img = pylon.PylonImage()
        arr = np.random.randint(0, 256, (480, 640), dtype=np.uint8)

        arr_refcount_0 = sys.getrefcount(arr)
        img.AttachArray(arr, pylon.PixelType_Mono8)
        # check proper refcounting attach
        self.assertEqual( sys.getrefcount(arr) , arr_refcount_0 + 1)

        # check that img and array have same content
        self.assertEqual(np.all(arr == img.Array), True)

        del img
        # check proper refcounting free
        self.assertEqual( sys.getrefcount(arr), arr_refcount_0)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
