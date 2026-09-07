"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/PixelTypeMapper.i.
"""

from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class PixelTypeMapperTestSuite(PylonEmuTestCase):
    """Checks mapping between PixelType values and symbolic pixel format names."""

    # -------------------------------------------------------------------------
    # Public interface
    # -------------------------------------------------------------------------
    def test_pixel_type_mapper_class_is_exposed(self):
        """The PixelTypeMapper class is available on the pylon module."""
        self.assertTrue(hasattr(pylon, "PixelTypeMapper"))

    def test_get_pylon_pixel_type_by_name_is_exposed(self):
        """The PixelTypeMapper method GetPylonPixelTypeByName is available."""
        self.assertTrue(hasattr(pylon.PixelTypeMapper, "GetPylonPixelTypeByName"))
        self.assertTrue(callable(pylon.PixelTypeMapper.GetPylonPixelTypeByName))

    def test_get_name_by_pixel_type_is_exposed(self):
        """The PixelTypeMapper method GetNameByPixelType is available."""
        self.assertTrue(hasattr(pylon.PixelTypeMapper, "GetNameByPixelType"))
        self.assertTrue(callable(pylon.PixelTypeMapper.GetNameByPixelType))

    def test_sfnc_version_constants_are_available(self):
        """The built-in SFNC version constants used by GetNameByPixelType are available."""
        self.assertTrue(hasattr(pylon, "Sfnc_VersionUndefined"))
        self.assertTrue(hasattr(pylon, "Sfnc_1_5_0"))
        self.assertTrue(hasattr(pylon, "Sfnc_2_0_0"))

    # -------------------------------------------------------------------------
    # GetPylonPixelTypeByName: symbolic name (str) -> pixel type (int)
    # -------------------------------------------------------------------------
    def test_get_pylon_pixel_type_by_name_returns_int(self):
        """The result type of GetPylonPixelTypeByName is int."""
        result = pylon.PixelTypeMapper.GetPylonPixelTypeByName("Mono8")
        self.assertIsInstance(result, int)

    def test_get_pylon_pixel_type_by_name_recognizes_known_names(self):
        """GetPylonPixelTypeByName recognizes known symbolic names."""
        expected = {
            "Mono8": pylon.PixelType_Mono8,
            "Mono16": pylon.PixelType_Mono16,
            "RGB8": pylon.PixelType_RGB8packed,
            "RGB8Packed": pylon.PixelType_RGB8packed,
            "BayerRG8": pylon.PixelType_BayerRG8,
        }
        for symbolic_name, expected_type in expected.items():
            with self.subTest(symbolic_name=symbolic_name):
                result = pylon.PixelTypeMapper.GetPylonPixelTypeByName(symbolic_name)
                self.assertEqual(result, expected_type)

    def test_get_pylon_pixel_type_by_name_returns_undefined_for_invalid_name(self):
        """GetPylonPixelTypeByName returns PixelType_Undefined for unknown names."""
        result = pylon.PixelTypeMapper.GetPylonPixelTypeByName("NotARealPixelFormat")
        self.assertEqual(result, pylon.PixelType_Undefined)

    # -------------------------------------------------------------------------
    # GetNameByPixelType: pixel type (int) -> symbolic name (str)
    # -------------------------------------------------------------------------
    def test_get_name_by_pixel_type_returns_string(self):
        """GetNameByPixelType returns a string."""
        result = pylon.PixelTypeMapper.GetNameByPixelType(pylon.PixelType_Mono8)
        self.assertIsInstance(result, str)

    def test_get_name_by_pixel_type_maps_known_types(self):
        """GetNameByPixelType maps known pixel types correctly."""
        expected = {
            pylon.PixelType_Mono8: "Mono8",
            pylon.PixelType_Mono16: "Mono16",
            pylon.PixelType_BayerRG8: "BayerRG8",
        }
        for pixel_type, expected_name in expected.items():
            with self.subTest(pixel_type=pixel_type):
                result = pylon.PixelTypeMapper.GetNameByPixelType(pixel_type)
                self.assertEqual(result, expected_name)

    def test_get_name_by_pixel_type_undefined_returns_empty_string(self):
        """GetNameByPixelType returns an empty string for PixelType_Undefined."""
        result = pylon.PixelTypeMapper.GetNameByPixelType(pylon.PixelType_Undefined)
        self.assertEqual(result, "")

    def test_get_name_by_pixel_type_default_sfnc_is_pre2_0(self):
        """GetNameByPixelType defaults to the pre-2.0 naming, matching the pylon API default."""
        result_default = pylon.PixelTypeMapper.GetNameByPixelType(pylon.PixelType_RGB8packed)
        result_explicit = pylon.PixelTypeMapper.GetNameByPixelType(
            pylon.PixelType_RGB8packed, pylon.Sfnc_VersionUndefined
        )
        self.assertEqual(result_default, result_explicit)
        self.assertEqual(result_default, "RGB8Packed")

    def test_sfnc_version_changes_symbolic_name(self):
        """GetNameByPixelType returns a different name depending on the SFNC version."""
        self.assertEqual(
            pylon.PixelTypeMapper.GetNameByPixelType(
                pylon.PixelType_RGB8packed, pylon.Sfnc_1_5_0
            ),
            "RGB8Packed",
        )
        self.assertEqual(
            pylon.PixelTypeMapper.GetNameByPixelType(
                pylon.PixelType_RGB8packed, pylon.Sfnc_2_0_0
            ),
            "RGB8",
        )

    def test_sfnc_version_accepts_camera_get_sfnc_version(self):
        """GetNameByPixelType accepts the VersionInfo returned by camera.GetSfncVersion()."""
        camera = self.create_first()
        camera.Open()
        try:
            sfnc_version = camera.GetSfncVersion()  # Sfnc_VersionUndefined for the emulated camera
            result = pylon.PixelTypeMapper.GetNameByPixelType(
                pylon.PixelType_RGB8packed, sfnc_version
            )
            self.assertEqual(result, "RGB8Packed")
        finally:
            camera.Close()

    # -------------------------------------------------------------------------
    # Round trip
    # -------------------------------------------------------------------------
    def test_round_trip_various_formats(self):
        """Names obtained from GetNameByPixelType map back with GetPylonPixelTypeByName."""
        test_formats = [
            (pylon.PixelType_Mono8, "Mono8"),
            (pylon.PixelType_Mono16, "Mono16"),
            (pylon.PixelType_BayerRG8, "BayerRG8"),
        ]

        for pixel_type, expected_name in test_formats:
            with self.subTest(pixel_type=pixel_type):
                name = pylon.PixelTypeMapper.GetNameByPixelType(pixel_type)
                self.assertEqual(name, expected_name)
                roundtrip_type = pylon.PixelTypeMapper.GetPylonPixelTypeByName(name)
                self.assertEqual(roundtrip_type, pixel_type)



if __name__ == "__main__":
    unittest.main()
