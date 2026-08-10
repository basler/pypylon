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
        """Reading alpha from non-alpha RGB PixelData raises LogicalErrorException."""
        image = _make_image(pylon.PixelType_RGB8packed, 1, 1, bytearray([10, 20, 30]))

        pixel_data = image.GetPixelData(0, 0)

        with self.assertRaises(pylon.LogicalErrorException):
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


if __name__ == "__main__":
    unittest.main()


