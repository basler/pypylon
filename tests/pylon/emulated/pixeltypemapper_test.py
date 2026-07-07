"""Unit tests for the PixelTypeMapper class-based API."""


from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class PixelTypeMapperTestSuite(PylonEmuTestCase):
    """Checks mapping between PixelType values and symbolic pixel format names."""
    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------
    def test_pixel_type_mapper_class_is_exposed(self):
        self.assertTrue(hasattr(pylon, "PixelTypeMapper"))

    def test_get_pixel_type_from_format_value_is_exposed(self):
        self.assertTrue(hasattr(pylon.PixelTypeMapper, "GetPylonPixelTypeByPixelFormatValue"))
        self.assertTrue(callable(pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue))

    def test_get_pixel_format_value_from_pixel_type_is_exposed(self):
        self.assertTrue(hasattr(pylon.PixelTypeMapper, "GetPixelFormatByPixelType"))
        self.assertTrue(callable(pylon.PixelTypeMapper.GetPixelFormatByPixelType))

    def test_sfnc_version_constants_are_available(self):
        self.assertTrue(hasattr(pylon, "Sfnc_1_5_0"))
        self.assertTrue(hasattr(pylon, "Sfnc_2_0_0"))
        self.assertTrue(hasattr(pylon, "Sfnc_2_1_0"))

    # -------------------------------------------------------------------------
    # Map pixel format values to pixel type (int)
    # -------------------------------------------------------------------------
    def test_get_pixel_type_from_format_value_returns_int(self):
        result = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(pylon.PixelType_Mono8)
        self.assertIsInstance(result, int)

    def test_get_pixel_type_from_format_value_recognizes_known_types(self):
        for pixel_type in (
            pylon.PixelType_Mono8,
            pylon.PixelType_Mono16,
            pylon.PixelType_RGB8packed,
            pylon.PixelType_BayerRG8,
        ):
            with self.subTest(pixel_type=pixel_type):
                result = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(pixel_type)
                self.assertEqual(result, pixel_type)

    def test_get_pixel_type_from_format_value_returns_undefined_for_invalid_value(self):
        result = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(0xDEADBEEF)
        self.assertEqual(result, pylon.PixelType_Undefined)

    def test_get_pixel_type_from_format_value_default_sfnc_is_2_0_0(self):
        result_default = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(pylon.PixelType_Mono8)
        result_explicit = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(
            pylon.PixelType_Mono8, pylon.Sfnc_2_0_0
        )
        self.assertEqual(result_default, result_explicit)

    def test_get_pixel_type_from_format_value_accepts_sfnc_versions(self):
        result_sfnc1 = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(
            pylon.PixelType_Mono8, pylon.Sfnc_1_5_0
        )
        result_sfnc2 = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(
            pylon.PixelType_Mono8, pylon.Sfnc_2_0_0
        )
        self.assertNotEqual(result_sfnc1, pylon.PixelType_Undefined)
        self.assertNotEqual(result_sfnc2, pylon.PixelType_Undefined)

    # -------------------------------------------------------------------------
    # Map pixel type (str) to pixel format value (int)
    # -------------------------------------------------------------------------
    def test_get_pixel_format_value_from_pixel_type_returns_string(self):
        result = pylon.PixelTypeMapper.GetPixelFormatByPixelType(pylon.PixelType_Mono8)
        self.assertIsInstance(result, str)

    def test_get_pixel_format_value_from_pixel_type_maps_known_types(self):
        expected = {
            pylon.PixelType_Mono8: "Mono8",
            pylon.PixelType_Mono16: "Mono16",
            pylon.PixelType_RGB8packed: "RGB8",
            pylon.PixelType_BayerRG8: "BayerRG8",
        }
        for pixel_type, expected_name in expected.items():
            with self.subTest(pixel_type=pixel_type):
                result = pylon.PixelTypeMapper.GetPixelFormatByPixelType(pixel_type)
                self.assertEqual(result, expected_name)

    def test_get_pixel_format_value_from_pixel_type_undefined_returns_empty_string(self):
        result = pylon.PixelTypeMapper.GetPixelFormatByPixelType(pylon.PixelType_Undefined)
        self.assertEqual(result, "")

    def test_get_pixel_format_value_from_pixel_type_invalid_returns_empty_string(self):
        result = pylon.PixelTypeMapper.GetPixelFormatByPixelType(0xDEADBEEF)
        self.assertEqual(result, "")

    # -------------------------------------------------------------------------
    # SFNC version behavior and round-trip
    # -------------------------------------------------------------------------
    def test_get_pixel_format_value_from_pixel_type_default_sfnc_is_2_0_0(self):
        result_default = pylon.PixelTypeMapper.GetPixelFormatByPixelType(pylon.PixelType_Mono8)
        result_explicit = pylon.PixelTypeMapper.GetPixelFormatByPixelType(
            pylon.PixelType_Mono8, pylon.Sfnc_2_0_0
        )
        self.assertEqual(result_default, result_explicit)

    def test_get_pixel_format_value_from_pixel_type_accepts_sfnc_versions(self):
        result_sfnc1 = pylon.PixelTypeMapper.GetPixelFormatByPixelType(
            pylon.PixelType_Mono8, pylon.Sfnc_1_5_0
        )
        result_sfnc2 = pylon.PixelTypeMapper.GetPixelFormatByPixelType(
            pylon.PixelType_Mono8, pylon.Sfnc_2_0_0
        )
        self.assertTrue(len(result_sfnc1) > 0)
        self.assertTrue(len(result_sfnc2) > 0)

    def test_round_trip_various_formats(self):
        test_formats = [
            (pylon.PixelType_Mono8, "Mono8"),
            (pylon.PixelType_Mono16, "Mono16"),
            (pylon.PixelType_RGB8packed, "RGB8"),
            (pylon.PixelType_BGR8packed, "BGR8"),
            (pylon.PixelType_BayerRG8, "BayerRG8"),
        ]

        for pixel_type, expected_name in test_formats:
            with self.subTest(pixel_type=pixel_type):
                name = pylon.PixelTypeMapper.GetPixelFormatByPixelType(pixel_type)
                self.assertEqual(name, expected_name)
                roundtrip_type = pylon.PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(pixel_type)
                self.assertEqual(roundtrip_type, pixel_type)

    def test_sfnc_versions_can_change_symbolic_name(self):
        self.assertEqual(
            pylon.PixelTypeMapper.GetPixelFormatByPixelType(
                pylon.PixelType_RGB8packed, pylon.Sfnc_1_5_0
            ),
            "RGB8Packed",
        )
        self.assertEqual(
            pylon.PixelTypeMapper.GetPixelFormatByPixelType(
                pylon.PixelType_RGB8packed, pylon.Sfnc_2_0_0
            ),
            "RGB8",
        )


if __name__ == "__main__":
    unittest.main()

