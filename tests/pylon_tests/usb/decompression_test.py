import unittest

from numpy.testing import assert_array_equal

from pylonusbtestcase import PylonTestCase
from pypylon import pylon, genicam


class GrabTestSuite(PylonTestCase):
    def setUp(self):
        super().setUp()

        self.camera = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice()
        )
        self.camera.Open()
        self.camera.ExposureTime.SetValue(self.camera.ExposureTime.Min)

        self.camera.PixelFormat = "Mono8"
        self.camera.TestPattern = "Testimage1"

        self.camera.ImageCompressionMode = "Off"
        with self.camera.GrabOne(10000) as compressed_image:
            self.reference_array = compressed_image.Array

        try:
            self.camera.ImageCompressionMode = "BaslerCompressionBeyond"
        except (genicam.RuntimeException, genicam.InvalidArgumentException):
            self.camera.Close()
            self.skipTest("camera does not support baser compression beyond")

        self.camera.ImageCompressionRateOption = "Lossless"
        self.camera.BslImageCompressionRatio = 100.0

    def tearDown(self):
        self.camera.Close()
        super().tearDown()

    def test_grab_compressed(self):
        decompressor = pylon.ImageDecompressor()

        descriptor = self.camera.BslImageCompressionBCBDescriptor.GetAll()
        decompressor.SetCompressionDescriptor(descriptor)

        with self.camera.GrabOne(10000) as compressed_image:
            payload = compressed_image.GetBuffer()
            decompressed_image = decompressor.DecompressImage(payload)
            decompressed_array = decompressed_image.Array

        assert_array_equal(self.reference_array, decompressed_array)

        self.camera.Close()

    def test_decompress_image(self):
        decompressor = pylon.ImageDecompressor()

        descriptor = self.camera.BslImageCompressionBCBDescriptor.GetAll()
        decompressor.SetCompressionDescriptor(descriptor)

        with self.camera.GrabOne(10000) as compressed_image:
            decompressed_image = decompressor.DecompressImage(compressed_image)
            decompressed_array = decompressed_image.Array

        assert_array_equal(self.reference_array, decompressed_array)

        self.camera.Close()


if __name__ == "__main__":
    unittest.main()
