from pypylon import pylon, genicam
import unittest


COMPRESSION_DESCRIPTOR_MONO8 = (
    b"\x01\x00\x01\x00\x01\x00\x00\x00\x08\x00\x0a\x00\x02\x00\x01\x00"
    + b"\x04\x00\x01\x00\x87\x65\x44\x33\x32\x22\x11\x11\x11\x10\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x11\x11\x11\x12\x22"
    + b"\x33\x34\x45\x66"
)

DESCRIPTOR_HASH_MONO8 = b"\x96\x84\xad\xed"

TEST_PAYLOAD_MONO8 = (
    b"\x00\x49\x00\x49\x00\x49\x00\x49"
    + b"\x00\x49\x00\x49\x00\x49\x00\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x52\x49\x52\x49\x52\x49\x52\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x12\x49\x12\x49\x12\x49\x12\x49"
    + b"\x52\x49\x00\x00\x52\x49\x00\x00"
    + b"\x52\x49\x00\x00\x52\x49\x00\x00"
    + b"\x52\x49\x00\x00\x52\x49\x00\x00"
    + b"\x52\x49\x00\x00\x52\x49\x00\x00"
    + b"\x1f\x20\x21\x22\x23\x24\x25\x26"
    + b"\x27\x28\x29\x2a\x2b\x2c\x2d\x2e"
    + b"\x2f\x30\x31\x32\x33\x34\x35\x36"
    + b"\x37\x38\x39\x3a\x3b\x3c\x3d\x3e"
    + b"\x00\x00\x00\x00\x90\x01\x00\x00"
    + b"\x01\x00\x08\x01\x20\x00\x00\x00"
    + b"\x20\x00\x00\x00\x10\x00\x00\x00"
    + b"\x08\x00\x00\x00\x00\x00\x00\x00"
    + b"\x96\x84\xad\xed\x00\x02\x00\x00"
    + b"\xea\x9a\x90\x2f\xd8\x01\x00\x00"
)

TEST_IMAGE_WIDTH = 32
TEST_IMAGE_HEIGHT = 32
TEST_IMAGE_OFFSET_X = 16
TEST_IMAGE_OFFSET_Y = 8


class DecompressionTestSuite(unittest.TestCase):
    def test_constructor(self):
        decompressor = pylon.ImageDecompressor()
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_set_compression_descriptor(self):
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        self.assertTrue(decompressor.HasCompressionDescriptor())

        decompressor.ResetCompressionDescriptor()
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_get_compression_info(self):
        decompressor = pylon.ImageDecompressor()
        info = decompressor.GetCompressionInfo(TEST_PAYLOAD_MONO8)
        self.assertEqual(info.hasCompressedImage, True)
        self.assertEqual(info.compressionStatus, pylon.CompressionStatus_Ok)
        self.assertEqual(info.lossy, False)
        self.assertEqual(info.pixelType, pylon.PixelType_Mono8)
        self.assertEqual(info.width, TEST_IMAGE_WIDTH)
        self.assertEqual(info.height, TEST_IMAGE_HEIGHT)
        self.assertEqual(info.offsetX, TEST_IMAGE_OFFSET_X)
        self.assertEqual(info.offsetY, TEST_IMAGE_OFFSET_Y)
        self.assertEqual(info.paddingX, 0)
        self.assertEqual(info.paddingY, 0)
        self.assertEqual(
            info.decompressedImageSize, TEST_IMAGE_WIDTH * TEST_IMAGE_HEIGHT * 1
        )
        self.assertGreater(info.decompressedPayloadSize, info.decompressedImageSize)

    def test_decompress_image(self):
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)

        image = decompressor.DecompressImage(TEST_PAYLOAD_MONO8)

        buffer = image.GetBuffer()
        self.assertEqual(len(buffer), TEST_IMAGE_WIDTH * TEST_IMAGE_HEIGHT)

        for y in range(TEST_IMAGE_HEIGHT):
            row = buffer[y * TEST_IMAGE_WIDTH : (y + 1) * TEST_IMAGE_WIDTH]
            for x, val in enumerate(row):
                self.assertEqual(val, x + y, "Mismatch in {}/{}".format(y, x))

    def test_hash(self):
        decompressor = pylon.ImageDecompressor()

        # test computing hash from binary representation of descriptor
        descriptor_hash = decompressor.ComputeCompressionDescriptorHash(
            COMPRESSION_DESCRIPTOR_MONO8
        )
        self.assertEqual(descriptor_hash, DESCRIPTOR_HASH_MONO8)

        # test extracting hash from loaded descriptor
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        descriptor_hash = decompressor.GetCurrentCompressionDescriptorHash()
        self.assertEqual(descriptor_hash, DESCRIPTOR_HASH_MONO8)

        decompressor.ResetCompressionDescriptor()
        self.assertRaises(
            genicam.RuntimeException, decompressor.GetCurrentCompressionDescriptorHash
        )

        # test extracting hash from payload
        descriptor_hash = decompressor.GetCompressionDescriptorHash(TEST_PAYLOAD_MONO8)
        self.assertEqual(descriptor_hash, DESCRIPTOR_HASH_MONO8)

    def test_numpy(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest("numpy is not installed")

        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)

        image = decompressor.DecompressImage(TEST_PAYLOAD_MONO8)

        array = image.Array
        self.assertEqual(array.shape, (image.Width, image.Height))


if __name__ == "__main__":
    unittest.main()
