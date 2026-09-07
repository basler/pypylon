"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/PixelData.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


def _make_image(pixel_type, width, height, buffer):
    """Return a PylonImage backed by the supplied pixel buffer."""
    image = pylon.PylonImage()
    image.AttachMemoryView(memoryview(buffer), pixel_type, width, height, 0)
    return image


class PixelDataTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # API availability
    # ------------------------------------------------------------------

    def test_get_pixel_data_returns_pixel_data_value(self):
        """GetPixelData returns a PixelData value object instead of an opaque SWIG pointer."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 1, 1)

        pixel_data = image.GetPixelData(0, 0)

        self.assertIsInstance(pixel_data, pylon.PixelData)
        self.assertFalse(hasattr(pixel_data, "Data"))

    def test_pixel_data_type_constants_are_module_level_integers(self):
        """PixelDataType constants are available as Python integers on the pylon module."""
        self.assertIsInstance(pylon.PixelDataType_Unknown, int)
        self.assertIsInstance(pylon.PixelDataType_Mono, int)
        self.assertIsInstance(pylon.PixelDataType_YUV, int)
        self.assertIsInstance(pylon.PixelDataType_RGB, int)
        self.assertIsInstance(pylon.PixelDataType_RGBA, int)
        self.assertIsInstance(pylon.PixelDataType_BayerR, int)
        self.assertIsInstance(pylon.PixelDataType_BayerG, int)
        self.assertIsInstance(pylon.PixelDataType_BayerB, int)
        self.assertIsInstance(pylon.PixelDataType_BiColorRG, int)
        self.assertIsInstance(pylon.PixelDataType_BiColorBG, int)

    # ------------------------------------------------------------------
    # Mono pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_mono8_returns_value_and_metadata(self):
        """GetPixelData returns the expected Mono value, data type, and bit depth for Mono8."""
        image = _make_image(pylon.PixelType_Mono8, 2, 1, bytearray([12, 34]))

        pixel_data = image.GetPixelData(1, 0)

        self.assertEqual(pixel_data.PixelDataType, pylon.PixelDataType_Mono)
        self.assertEqual(pixel_data.BitDepth, 8)
        self.assertEqual(pixel_data.Mono, 34)

    def test_get_pixel_data_rejects_component_not_matching_data_type(self):
        """Reading an RGB component from mono PixelData names the actual data type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([12]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_Mono"):
            _ = pixel_data.R

    def test_pixel_data_value_survives_image_release(self):
        """PixelData remains readable after the source PylonImage has been released."""
        image = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([91]))
        pixel_data = image.GetPixelData(0, 0)

        image.Release()

        self.assertEqual(pixel_data.PixelDataType, pylon.PixelDataType_Mono)
        self.assertEqual(pixel_data.Mono, 91)

    # ------------------------------------------------------------------
    # RGB and BGR pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_rgb8packed_returns_logical_rgb_components(self):
        """GetPixelData returns the logical R, G, and B values for RGB8packed."""
        image = _make_image(pylon.PixelType_RGB8packed, 1, 1, bytearray([10, 20, 30]))

        pixel_data = image.GetPixelData(0, 0)

        self.assertEqual(pixel_data.PixelDataType, pylon.PixelDataType_RGB)
        self.assertEqual(pixel_data.BitDepth, 8)
        self.assertEqual(pixel_data.R, 10)
        self.assertEqual(pixel_data.G, 20)
        self.assertEqual(pixel_data.B, 30)

    def test_get_pixel_data_bgr8packed_normalizes_to_logical_rgb_components(self):
        """GetPixelData normalizes BGR8packed buffer order to logical R, G, and B values."""
        image = _make_image(pylon.PixelType_BGR8packed, 1, 1, bytearray([30, 20, 10]))

        pixel_data = image.GetPixelData(0, 0)

        self.assertEqual(pixel_data.PixelDataType, pylon.PixelDataType_RGB)
        self.assertEqual(pixel_data.R, 10)
        self.assertEqual(pixel_data.G, 20)
        self.assertEqual(pixel_data.B, 30)

    def test_get_pixel_data_rejects_alpha_for_rgb_pixel_data(self):
        """Reading alpha from non-alpha RGB PixelData names the actual type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_RGB8packed, 1, 1, bytearray([10, 20, 30]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_RGB"):
            _ = pixel_data.A

    # ------------------------------------------------------------------
    # Bayer pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_bayer_rg8_returns_component_matching_position(self):
        """GetPixelData returns the Bayer component selected by the BayerRG8 pixel position."""
        image = _make_image(
            pylon.PixelType_BayerRG8,
            2,
            2,
            bytearray([11, 22, 33, 44]),
        )

        red_pixel = image.GetPixelData(0, 0)
        first_green_pixel = image.GetPixelData(1, 0)
        second_green_pixel = image.GetPixelData(0, 1)
        blue_pixel = image.GetPixelData(1, 1)

        self.assertEqual(red_pixel.PixelDataType, pylon.PixelDataType_BayerR)
        self.assertEqual(red_pixel.BayerR, 11)
        self.assertEqual(first_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(first_green_pixel.BayerG, 22)
        self.assertEqual(second_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(second_green_pixel.BayerG, 33)
        self.assertEqual(blue_pixel.PixelDataType, pylon.PixelDataType_BayerB)
        self.assertEqual(blue_pixel.BayerB, 44)

    def test_get_pixel_data_bayer_bg8_returns_component_matching_position(self):
        """GetPixelData returns the Bayer component selected by the BayerBG8 pixel position."""
        image = _make_image(
            pylon.PixelType_BayerBG8,
            2,
            2,
            bytearray([11, 22, 33, 44]),
        )

        blue_pixel = image.GetPixelData(0, 0)
        first_green_pixel = image.GetPixelData(1, 0)
        second_green_pixel = image.GetPixelData(0, 1)
        red_pixel = image.GetPixelData(1, 1)

        self.assertEqual(blue_pixel.PixelDataType, pylon.PixelDataType_BayerB)
        self.assertEqual(blue_pixel.BayerB, 11)
        self.assertEqual(first_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(first_green_pixel.BayerG, 22)
        self.assertEqual(second_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(second_green_pixel.BayerG, 33)
        self.assertEqual(red_pixel.PixelDataType, pylon.PixelDataType_BayerR)
        self.assertEqual(red_pixel.BayerR, 44)

    def test_get_pixel_data_bayer_gb8_returns_component_matching_position(self):
        """GetPixelData returns the Bayer component selected by the BayerGB8 pixel position."""
        image = _make_image(
            pylon.PixelType_BayerGB8,
            2,
            2,
            bytearray([11, 22, 33, 44]),
        )

        first_green_pixel = image.GetPixelData(0, 0)
        blue_pixel = image.GetPixelData(1, 0)
        red_pixel = image.GetPixelData(0, 1)
        second_green_pixel = image.GetPixelData(1, 1)

        self.assertEqual(first_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(first_green_pixel.BayerG, 11)
        self.assertEqual(blue_pixel.PixelDataType, pylon.PixelDataType_BayerB)
        self.assertEqual(blue_pixel.BayerB, 22)
        self.assertEqual(red_pixel.PixelDataType, pylon.PixelDataType_BayerR)
        self.assertEqual(red_pixel.BayerR, 33)
        self.assertEqual(second_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(second_green_pixel.BayerG, 44)

    def test_get_pixel_data_bayer_gr8_returns_component_matching_position(self):
        """GetPixelData returns the Bayer component selected by the BayerGR8 pixel position."""
        image = _make_image(
            pylon.PixelType_BayerGR8,
            2,
            2,
            bytearray([11, 22, 33, 44]),
        )

        first_green_pixel = image.GetPixelData(0, 0)
        red_pixel = image.GetPixelData(1, 0)
        blue_pixel = image.GetPixelData(0, 1)
        second_green_pixel = image.GetPixelData(1, 1)

        self.assertEqual(first_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(first_green_pixel.BayerG, 11)
        self.assertEqual(red_pixel.PixelDataType, pylon.PixelDataType_BayerR)
        self.assertEqual(red_pixel.BayerR, 22)
        self.assertEqual(blue_pixel.PixelDataType, pylon.PixelDataType_BayerB)
        self.assertEqual(blue_pixel.BayerB, 33)
        self.assertEqual(second_green_pixel.PixelDataType, pylon.PixelDataType_BayerG)
        self.assertEqual(second_green_pixel.BayerG, 44)

    # ------------------------------------------------------------------
    # BiColor pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_bicolor_rgbg8_returns_red_green_and_blue_green_pairs(self):
        """GetPixelData returns BiColorRG and BiColorBG component pairs for BiColorRGBG8."""
        image = _make_image(pylon.PixelType_BiColorRGBG8, 2, 1, bytearray([10, 20, 30, 40]))

        red_green_pixel = image.GetPixelData(0, 0)
        blue_green_pixel = image.GetPixelData(1, 0)

        self.assertEqual(red_green_pixel.PixelDataType, pylon.PixelDataType_BiColorRG)
        self.assertEqual(red_green_pixel.BitDepth, 8)
        self.assertEqual(red_green_pixel.R, 10)
        self.assertEqual(red_green_pixel.G, 20)

        self.assertEqual(blue_green_pixel.PixelDataType, pylon.PixelDataType_BiColorBG)
        self.assertEqual(blue_green_pixel.BitDepth, 8)
        self.assertEqual(blue_green_pixel.B, 30)
        self.assertEqual(blue_green_pixel.G, 40)

    def test_get_pixel_data_bicolor_bgrg8_returns_blue_green_and_red_green_pairs(self):
        """GetPixelData returns BiColorBG and BiColorRG component pairs for BiColorBGRG8."""
        image = _make_image(pylon.PixelType_BiColorBGRG8, 2, 1, bytearray([10, 20, 30, 40]))

        blue_green_pixel = image.GetPixelData(0, 0)
        red_green_pixel = image.GetPixelData(1, 0)

        self.assertEqual(blue_green_pixel.PixelDataType, pylon.PixelDataType_BiColorBG)
        self.assertEqual(blue_green_pixel.BitDepth, 8)
        self.assertEqual(blue_green_pixel.B, 10)
        self.assertEqual(blue_green_pixel.G, 20)

        self.assertEqual(red_green_pixel.PixelDataType, pylon.PixelDataType_BiColorRG)
        self.assertEqual(red_green_pixel.R, 30)
        self.assertEqual(red_green_pixel.G, 40)

    def test_get_pixel_data_rejects_blue_for_red_green_bicolor_pixel_data(self):
        """Reading blue from a BiColorRG pixel names the actual data type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_BiColorRGBG8, 2, 1, bytearray([10, 20, 30, 40]))

        red_green_pixel = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_BiColorRG"):
            _ = red_green_pixel.B

    def test_get_pixel_data_rejects_red_for_blue_green_bicolor_pixel_data(self):
        """Reading red from a BiColorBG pixel names the actual data type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_BiColorRGBG8, 2, 1, bytearray([10, 20, 30, 40]))

        blue_green_pixel = image.GetPixelData(1, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_BiColorBG"):
            _ = blue_green_pixel.R

    # ------------------------------------------------------------------
    # RGBA pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_rgba8packed_returns_all_four_components(self):
        """GetPixelData returns R, G, B, and A values for RGBA8packed."""
        image = _make_image(pylon.PixelType_RGBA8packed, 1, 1, bytearray([11, 22, 33, 44]))

        pixel_data = image.GetPixelData(0, 0)

        self.assertEqual(pixel_data.PixelDataType, pylon.PixelDataType_RGBA)
        self.assertEqual(pixel_data.BitDepth, 8)
        self.assertEqual(pixel_data.R, 11)
        self.assertEqual(pixel_data.G, 22)
        self.assertEqual(pixel_data.B, 33)
        self.assertEqual(pixel_data.A, 44)

    def test_get_pixel_data_rejects_mono_from_rgba_pixel_data(self):
        """Reading Mono from RGBA PixelData names the actual type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_RGBA8packed, 1, 1, bytearray([11, 22, 33, 44]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_RGBA"):
            _ = pixel_data.Mono

    # ------------------------------------------------------------------
    # YUV pixel data
    # ------------------------------------------------------------------

    def test_get_pixel_data_yuv422packed_returns_yuv_components(self):
        """GetPixelData returns the expected Y, U, and V values for YUV422packed."""
        # YUV422packed layout: U0, Y0, V0, Y1 (two pixels share U/V chroma).
        image = _make_image(
            pylon.PixelType_YUV422packed,
            2,
            1,
            bytearray([128, 100, 64, 200]),
        )

        first_pixel = image.GetPixelData(0, 0)
        second_pixel = image.GetPixelData(1, 0)

        self.assertEqual(first_pixel.PixelDataType, pylon.PixelDataType_YUV)
        self.assertEqual(first_pixel.Y, 100)
        self.assertEqual(first_pixel.U, 128)
        self.assertEqual(first_pixel.V, 64)

        self.assertEqual(second_pixel.PixelDataType, pylon.PixelDataType_YUV)
        self.assertEqual(second_pixel.Y, 200)
        self.assertEqual(second_pixel.U, 128)
        self.assertEqual(second_pixel.V, 64)

    def test_get_pixel_data_rejects_mono_from_yuv_pixel_data(self):
        """Reading Mono from YUV PixelData names the actual type in LogicalErrorException."""
        image = _make_image(
            pylon.PixelType_YUV422packed,
            2,
            1,
            bytearray([128, 100, 64, 200]),
        )

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_YUV"):
            _ = pixel_data.Mono

    # ------------------------------------------------------------------
    # Copy construction
    # ------------------------------------------------------------------

    def test_pixel_data_copy_construction_preserves_value(self):
        """PixelData(other) produces an independent copy with the same type and channel value."""
        original = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([77])).GetPixelData(0, 0)

        copy = pylon.PixelData(original)

        self.assertEqual(copy.PixelDataType, pylon.PixelDataType_Mono)
        self.assertEqual(copy.Mono, 77)
        self.assertEqual(copy, original)

    # ------------------------------------------------------------------
    # Error message coverage
    # ------------------------------------------------------------------

    def test_get_pixel_data_rejects_mono_from_rgb_pixel_data_with_message(self):
        """Reading Mono from RGB PixelData names the actual type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_RGB8packed, 1, 1, bytearray([10, 20, 30]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_RGB"):
            _ = pixel_data.Mono

    def test_get_pixel_data_rejects_wrong_bayer_component_with_message(self):
        """Reading BayerR from a BayerB pixel names the actual type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_BayerRG8, 2, 2, bytearray([11, 22, 33, 44]))

        blue_pixel = image.GetPixelData(1, 1)

        self.assertEqual(blue_pixel.PixelDataType, pylon.PixelDataType_BayerB)
        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_BayerB"):
            _ = blue_pixel.BayerR

    def test_get_pixel_data_rejects_yuv_component_from_mono_pixel_data_with_message(self):
        """Reading Y from Mono PixelData names the actual type in LogicalErrorException."""
        image = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([42]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaisesRegex(pylon.LogicalErrorException, "actual type is PixelDataType_Mono"):
            _ = pixel_data.Y

    # ------------------------------------------------------------------
    # Class-level constants
    # ------------------------------------------------------------------

    def test_pixel_data_type_constants_accessible_on_class(self):
        """PixelDataType constants are accessible on the PixelData class and equal the module-level aliases."""
        self.assertEqual(pylon.PixelData.PixelDataType_Unknown, pylon.PixelDataType_Unknown)
        self.assertEqual(pylon.PixelData.PixelDataType_Mono, pylon.PixelDataType_Mono)
        self.assertEqual(pylon.PixelData.PixelDataType_YUV, pylon.PixelDataType_YUV)
        self.assertEqual(pylon.PixelData.PixelDataType_RGB, pylon.PixelDataType_RGB)
        self.assertEqual(pylon.PixelData.PixelDataType_RGBA, pylon.PixelDataType_RGBA)
        self.assertEqual(pylon.PixelData.PixelDataType_BayerR, pylon.PixelDataType_BayerR)
        self.assertEqual(pylon.PixelData.PixelDataType_BayerG, pylon.PixelDataType_BayerG)
        self.assertEqual(pylon.PixelData.PixelDataType_BayerB, pylon.PixelDataType_BayerB)
        self.assertEqual(pylon.PixelData.PixelDataType_BiColorRG, pylon.PixelDataType_BiColorRG)
        self.assertEqual(pylon.PixelData.PixelDataType_BiColorBG, pylon.PixelDataType_BiColorBG)

    # ------------------------------------------------------------------
    # Coordinate validation
    # ------------------------------------------------------------------

    def test_get_pixel_data_rejects_negative_coordinates(self):
        """GetPixelData rejects negative coordinates before calling the SDK."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 1, 1)

        with self.assertRaises(OverflowError):
            image.GetPixelData(-1, 0)

    def test_get_pixel_data_rejects_coordinates_outside_image(self):
        """GetPixelData raises the SDK exception for coordinates outside the image."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 1, 1)

        with self.assertRaises(pylon.InvalidArgumentException):
            image.GetPixelData(1, 0)

    # ------------------------------------------------------------------
    # Equality
    # ------------------------------------------------------------------

    def test_pixel_data_equal_for_same_type_and_value(self):
        """Two PixelData with the same type, bit depth, and value compare equal."""
        left = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([42])).GetPixelData(0, 0)
        right = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([42])).GetPixelData(0, 0)

        self.assertTrue(left == right)
        self.assertFalse(left != right)

    def test_pixel_data_not_equal_for_same_type_different_value(self):
        """PixelData with the same type but different value compare unequal."""
        left = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([42])).GetPixelData(0, 0)
        right = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([7])).GetPixelData(0, 0)

        self.assertFalse(left == right)
        self.assertTrue(left != right)

    def test_pixel_data_not_equal_for_different_pixel_data_type(self):
        """PixelData with different PixelDataType compare unequal."""
        mono = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([10])).GetPixelData(0, 0)
        rgb = _make_image(pylon.PixelType_RGB8packed, 1, 1, bytearray([10, 20, 30])).GetPixelData(0, 0)

        self.assertNotEqual(mono.PixelDataType, rgb.PixelDataType)
        self.assertFalse(mono == rgb)
        self.assertTrue(mono != rgb)

    def test_pixel_data_not_equal_to_none_or_foreign_types(self):
        """Comparing PixelData to None or an unrelated type is unequal without raising."""
        pixel_data = _make_image(pylon.PixelType_Mono8, 1, 1, bytearray([42])).GetPixelData(0, 0)

        for other in (None, 42, "PixelData"):
            self.assertFalse(pixel_data == other)
            self.assertTrue(pixel_data != other)


if __name__ == "__main__":
    unittest.main()