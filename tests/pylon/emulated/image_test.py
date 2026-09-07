"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/Image.i,
covering the Image (IImage) abstract interface and the IImage alias.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class ImageTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Class identity / subclass hierarchy
    # ------------------------------------------------------------------

    def test_image_is_abstract_and_cannot_be_instantiated(self):
        """pylon.Image raises AttributeError when instantiated directly (abstract class)."""
        with self.assertRaises(AttributeError):
            pylon.Image()

    def test_iimage_is_alias_for_image(self):
        """pylon.IImage is a binding alias that resolves to the same class as pylon.Image."""
        self.assertIs(pylon.IImage, pylon.Image)

    def test_pylon_image_is_subclass_of_image(self):
        """PylonImage is a concrete subclass of Image."""
        self.assertTrue(issubclass(pylon.PylonImage, pylon.Image))

    def test_pylon_image_instance_is_instance_of_image(self):
        """A PylonImage object satisfies isinstance(obj, pylon.Image)."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 4, 4)
        self.assertIsInstance(image, pylon.Image)
        image.Release()

    # ------------------------------------------------------------------
    # IsValid
    # ------------------------------------------------------------------

    def test_is_valid_returns_false_for_default_constructed_image(self):
        """IsValid() returns False for a default-constructed (empty) image."""
        image = pylon.PylonImage()
        self.assertFalse(image.IsValid())

    def test_is_valid_returns_true_for_created_image(self):
        """IsValid() returns True after a successful PylonImage.Create()."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        self.assertTrue(image.IsValid())
        image.Release()

    # ------------------------------------------------------------------
    # IsUnique
    # ------------------------------------------------------------------

    def test_is_unique_true_when_sole_owner(self):
        """IsUnique() returns True when no other image object shares the buffer."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        self.assertTrue(image.IsUnique())
        image.Release()

    def test_is_unique_false_while_copy_exists_and_true_after_copy_released(self):
        """IsUnique() is False while a copy shares the buffer; True again after the copy is released."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        copy = pylon.PylonImage(image)

        self.assertFalse(image.IsUnique())
        self.assertFalse(copy.IsUnique())

        copy.Release()
        self.assertTrue(image.IsUnique())
        image.Release()

    # ------------------------------------------------------------------
    # Dimensions: GetWidth, GetHeight, GetPaddingX, GetPixelType,
    #             GetImageSize, GetOrientation
    # ------------------------------------------------------------------

    def test_dimension_accessors_match_creation_parameters(self):
        """GetWidth, GetHeight, GetPaddingX, GetPixelType, and GetImageSize reflect Create() arguments."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 320, 240)
        self.assertEqual(image.GetWidth(), 320)
        self.assertEqual(image.GetHeight(), 240)
        self.assertEqual(image.GetPaddingX(), 0)
        self.assertEqual(image.GetPixelType(), pylon.PixelType_Mono8)
        self.assertEqual(image.GetImageSize(), 320 * 240)
        image.Release()

    def test_get_image_size_accounts_for_padding(self):
        """GetImageSize() includes paddingX bytes in the per-row count."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48, 4)
        self.assertEqual(image.GetImageSize(), (64 + 4) * 48)
        image.Release()

    def test_get_orientation_default_is_top_down(self):
        """GetOrientation() returns ImageOrientation_TopDown for images created without explicit orientation."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        self.assertEqual(image.GetOrientation(), pylon.ImageOrientation_TopDown)
        image.Release()

    def test_get_orientation_bottom_up_when_specified(self):
        """GetOrientation() returns ImageOrientation_BottomUp when that orientation was requested."""
        image = pylon.PylonImage.Create(
            pylon.PixelType_Mono8, 64, 48, 0, pylon.ImageOrientation_BottomUp
        )
        self.assertEqual(image.GetOrientation(), pylon.ImageOrientation_BottomUp)
        image.Release()

    def test_dimension_accessors_return_zeros_for_invalid_image(self):
        """GetWidth, GetHeight, GetPaddingX, and GetImageSize all return 0 for an invalid image."""
        image = pylon.PylonImage()
        self.assertEqual(image.GetWidth(), 0)
        self.assertEqual(image.GetHeight(), 0)
        self.assertEqual(image.GetPaddingX(), 0)
        self.assertEqual(image.GetImageSize(), 0)

    # ------------------------------------------------------------------
    # GetStride
    # ------------------------------------------------------------------

    def test_get_stride_returns_ok_and_row_size_in_bytes_for_mono8(self):
        """GetStride() returns (True, width) for a Mono8 image with no padding."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        ok, stride = image.GetStride()
        self.assertTrue(ok)
        self.assertEqual(stride, 64)  # Mono8: 1 byte/pixel, no padding
        image.Release()

    def test_get_stride_includes_padding_bytes(self):
        """GetStride() includes paddingX in the reported stride."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48, 8)
        ok, stride = image.GetStride()
        self.assertTrue(ok)
        self.assertEqual(stride, 64 + 8)
        image.Release()

    # ------------------------------------------------------------------
    # GetBuffer
    # ------------------------------------------------------------------

    def test_get_buffer_returns_bytearray_with_length_equal_to_image_size(self):
        """GetBuffer() returns a bytearray whose length equals GetImageSize()."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48)
        buf = image.GetBuffer()
        self.assertIsInstance(buf, bytearray)
        self.assertEqual(len(buf), image.GetImageSize())
        image.Release()

    def test_get_buffer_on_invalid_image_returns_none(self):
        """GetBuffer() returns None for an invalid (default-constructed) image."""
        image = pylon.PylonImage()
        self.assertIsNone(image.GetBuffer())


if __name__ == "__main__":
    unittest.main()
