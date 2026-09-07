"""\
This unit test checks representative PixelType bindings introduced by
src/pylon/PixelType.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class PixelTypeTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # %ignore directives
    # ------------------------------------------------------------------

    def test_ignored_names_are_not_exposed(self):
        """The names hidden with %ignore are not exposed on pylon."""
        self.assertFalse(hasattr(pylon, "IsValidRGB"))
        self.assertFalse(hasattr(pylon, "IsValidBGR"))
        self.assertFalse(hasattr(pylon, "PixelSize"))
        self.assertFalse(hasattr(pylon, "PixelType"))

    # ------------------------------------------------------------------
    # Public constants
    # ------------------------------------------------------------------

    def test_representative_pixel_type_constants_are_python_ints(self):
        """Representative PixelType_* constants are exposed as Python ints."""
        self.assertIsInstance(pylon.PixelType_Undefined, int)
        self.assertIsInstance(pylon.PixelType_Mono8, int)
        self.assertIsInstance(pylon.PixelType_Mono12p, int)
        self.assertIsInstance(pylon.PixelType_BayerRG8, int)
        self.assertIsInstance(pylon.PixelType_RGB8packed, int)
        self.assertIsInstance(pylon.PixelType_RGB8planar, int)
        self.assertIsInstance(pylon.PixelType_YCbCr420_8_YY_CbCr_Semiplanar, int)
        self.assertIsInstance(pylon.PixelType_BiColorRGBG10p, int)
        self.assertIsInstance(pylon.PixelType_Coord3D_ABC32f, int)
        self.assertIsInstance(pylon.PixelType_Data64f, int)

    def test_pixel_type_undefined_uses_public_sentinel_value(self):
        """PixelType_Undefined keeps the documented public value -1."""
        self.assertEqual(pylon.PixelType_Undefined, -1)

    def test_color_filter_constants_use_public_values(self):
        """The PCF_* constants expose the public enum values."""
        self.assertEqual(pylon.PCF_BayerRG, 0)
        self.assertEqual(pylon.PCF_BayerGB, 1)
        self.assertEqual(pylon.PCF_BayerGR, 2)
        self.assertEqual(pylon.PCF_BayerBG, 3)
        self.assertEqual(pylon.PCF_Undefined, 4)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def test_bit_queries_distinguish_storage_from_bit_depth(self):
        """BitPerPixel and BitDepth distinguish unpacked, packed, and lsb-packed Mono12."""
        self.assertEqual(pylon.BitPerPixel(pylon.PixelType_Mono12), 16)
        self.assertEqual(pylon.BitPerPixel(pylon.PixelType_Mono12packed), 12)
        self.assertEqual(pylon.BitPerPixel(pylon.PixelType_Mono12p), 12)

        self.assertEqual(pylon.BitDepth(pylon.PixelType_Mono12), 12)
        self.assertEqual(pylon.BitDepth(pylon.PixelType_Mono12packed), 12)
        self.assertEqual(pylon.BitDepth(pylon.PixelType_Mono12p), 12)

    def test_samples_per_pixel_match_common_formats(self):
        """SamplesPerPixel matches mono, Bayer, RGB, and Coord3D usage."""
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_Mono8), 1)
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_BayerRG8), 1)
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_RGB8packed), 3)
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_Coord3D_ABC32f), 3)

    def test_plane_queries_show_how_planar_formats_reduce_to_mono_planes(self):
        """PlaneCount and GetPlanePixelType show how planar formats are interpreted."""
        self.assertEqual(pylon.PlaneCount(pylon.PixelType_RGB8planar), 3)
        self.assertEqual(
            pylon.GetPlanePixelType(pylon.PixelType_RGB8planar),
            pylon.PixelType_Mono8,
        )

        self.assertEqual(pylon.PlaneCount(pylon.PixelType_Mono8), 1)
        self.assertEqual(
            pylon.GetPlanePixelType(pylon.PixelType_Mono8),
            pylon.PixelType_Mono8,
        )

        self.assertEqual(pylon.PlaneCount(pylon.PixelType_YUV420planar), 3)
        self.assertEqual(
            pylon.GetPlanePixelType(pylon.PixelType_YUV420planar),
            pylon.PixelType_Mono8,
        )

    def test_pixel_increment_matches_layout_examples(self):
        """Pixel increments reflect Bayer and YUV subsampling layouts."""
        self.assertEqual(pylon.GetPixelIncrementX(pylon.PixelType_BayerRG8), 2)
        self.assertEqual(pylon.GetPixelIncrementY(pylon.PixelType_BayerRG8), 2)

        self.assertEqual(pylon.GetPixelIncrementX(pylon.PixelType_YUV422packed), 2)
        self.assertEqual(pylon.GetPixelIncrementY(pylon.PixelType_YUV422packed), 1)

        self.assertEqual(pylon.GetPixelIncrementX(pylon.PixelType_YUV411packed), 4)
        self.assertEqual(pylon.GetPixelIncrementY(pylon.PixelType_YUV411packed), 1)

        self.assertEqual(pylon.GetPixelIncrementX(pylon.PixelType_Mono8), 1)
        self.assertEqual(pylon.GetPixelIncrementY(pylon.PixelType_Mono8), 1)

    def test_get_pixel_color_filter_depends_on_pattern_not_depth(self):
        """GetPixelColorFilter stays stable across Bayer layouts and returns undefined otherwise."""
        self.assertEqual(
            pylon.GetPixelColorFilter(pylon.PixelType_BayerRG8),
            pylon.PCF_BayerRG,
        )
        self.assertEqual(
            pylon.GetPixelColorFilter(pylon.PixelType_BayerRG12p),
            pylon.PCF_BayerRG,
        )
        self.assertEqual(
            pylon.GetPixelColorFilter(pylon.PixelType_BayerGB8),
            pylon.PCF_BayerGB,
        )
        self.assertEqual(
            pylon.GetPixelColorFilter(pylon.PixelType_Mono8),
            pylon.PCF_Undefined,
        )

    def test_invalid_queries_raise_for_unsupported_formats(self):
        """Unsupported query combinations raise InvalidArgumentException."""
        with self.assertRaises(pylon.InvalidArgumentException):
            pylon.BitPerPixel(pylon.PixelType_Undefined)

        with self.assertRaises(pylon.InvalidArgumentException):
            pylon.BitDepth(pylon.PixelType_Coord3D_ABC32f)

    # ------------------------------------------------------------------
    # Classification helpers
    # ------------------------------------------------------------------

    def test_mono_and_color_helpers_show_the_bayer_distinction(self):
        """Bayer counts as mono for sampling but as color for image interpretation."""
        self.assertTrue(pylon.IsMono(pylon.PixelType_Mono8))
        self.assertTrue(pylon.IsMonoImage(pylon.PixelType_Mono8))
        self.assertFalse(pylon.IsColorImage(pylon.PixelType_Mono8))

        self.assertTrue(pylon.IsMono(pylon.PixelType_BayerRG8))
        self.assertFalse(pylon.IsMonoImage(pylon.PixelType_BayerRG8))
        self.assertTrue(pylon.IsColorImage(pylon.PixelType_BayerRG8))
        self.assertTrue(pylon.IsBayer(pylon.PixelType_BayerRG8))

    def test_rgb_bgr_and_yuv_helpers_match_common_formats(self):
        """RGB, BGR, and YUV helpers match the expected image families."""
        self.assertFalse(pylon.IsMono(pylon.PixelType_RGB8packed))
        self.assertTrue(pylon.IsColorImage(pylon.PixelType_RGB8packed))
        self.assertTrue(pylon.IsRGB(pylon.PixelType_RGB8packed))
        self.assertFalse(pylon.IsBGR(pylon.PixelType_RGB8packed))

        self.assertTrue(pylon.IsBGR(pylon.PixelType_BGR8packed))
        self.assertTrue(pylon.IsYUV(pylon.PixelType_YUV422packed))

    def test_rgba_and_bgra_helpers_match_channel_order(self):
        """IsRGBA and IsBGRA follow the channel order in the pixel type name."""
        self.assertTrue(pylon.IsRGBA(pylon.PixelType_RGBA8packed))
        self.assertFalse(pylon.IsRGBA(pylon.PixelType_BGRA8packed))
        self.assertTrue(pylon.IsBGRA(pylon.PixelType_BGRA8packed))
        self.assertFalse(pylon.IsBGRA(pylon.PixelType_RGBA8packed))

    def test_packed_helpers_distinguish_real_packing_from_legacy_names(self):
        """Packed helpers treat Mono/Bayer V1/V2 encodings differently from RGB8packed-style names."""
        self.assertTrue(pylon.IsPacked(pylon.PixelType_Mono12packed))
        self.assertTrue(pylon.IsPacked(pylon.PixelType_Mono12p))
        self.assertTrue(pylon.IsMonoPacked(pylon.PixelType_Mono12packed))
        self.assertTrue(pylon.IsPackedInLsbFormat(pylon.PixelType_Mono12p))
        self.assertFalse(pylon.IsPackedInLsbFormat(pylon.PixelType_Mono12packed))

        self.assertTrue(pylon.IsBayerPacked(pylon.PixelType_BayerGR12Packed))
        self.assertFalse(pylon.IsBayerPacked(pylon.PixelType_BayerGR8))

        self.assertTrue(pylon.IsRGBPacked(pylon.PixelType_RGB12V1packed))
        self.assertFalse(pylon.IsRGBPacked(pylon.PixelType_RGB8packed))
        self.assertTrue(pylon.IsBGRPacked(pylon.PixelType_BGR10V1packed))
        self.assertTrue(pylon.IsBGRPacked(pylon.PixelType_BGR10V2packed))
        self.assertFalse(pylon.IsBGRPacked(pylon.PixelType_BGR8packed))
        self.assertFalse(pylon.IsPacked(pylon.PixelType_RGB8packed))

    def test_planar_and_semiplanar_helpers_match_layout(self):
        """Planar and semiplanar helpers describe the memory layout directly."""
        self.assertTrue(pylon.IsPlanar(pylon.PixelType_RGB8planar))
        self.assertTrue(pylon.IsPlanar(pylon.PixelType_YUV422planar))
        self.assertFalse(pylon.IsPlanar(pylon.PixelType_RGB8packed))

        self.assertTrue(
            pylon.IsYUVSemiplanar(
                pylon.PixelType_YCbCr420_8_YY_CbCr_Semiplanar
            )
        )
        self.assertFalse(pylon.IsYUVSemiplanar(pylon.PixelType_YUV422packed))

    def test_bi_color_helpers_cover_packed_and_unpacked_examples(self):
        """BiColor helpers distinguish the plain and lsb-packed variants."""
        self.assertTrue(pylon.IsBiColor(pylon.PixelType_BiColorRGBG10))
        self.assertTrue(pylon.IsBiColor(pylon.PixelType_BiColorRGBG10p))
        self.assertTrue(pylon.IsColorImage(pylon.PixelType_BiColorRGBG10))
        self.assertFalse(pylon.IsBiColorPacked(pylon.PixelType_BiColorRGBG10))
        self.assertTrue(pylon.IsBiColorPacked(pylon.PixelType_BiColorRGBG10p))
        self.assertEqual(pylon.BitDepth(pylon.PixelType_BiColorRGBG10p), 10)

    # ------------------------------------------------------------------
    # Specialized formats
    # ------------------------------------------------------------------

    def test_confidence_and_single_channel_coord3d_formats_keep_their_categories(self):
        """Confidence and single-channel Coord3D formats keep their expected classifications."""
        self.assertTrue(pylon.IsMono(pylon.PixelType_Confidence16))
        self.assertTrue(pylon.IsMonoImage(pylon.PixelType_Confidence16))
        self.assertEqual(pylon.BitDepth(pylon.PixelType_Confidence16), 16)

        self.assertTrue(pylon.IsMono(pylon.PixelType_Coord3D_C16))
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_Coord3D_C16), 1)
        self.assertEqual(pylon.BitDepth(pylon.PixelType_Coord3D_C16), 16)

    def test_float_specialized_formats_keep_their_expected_categories(self):
        """Float Coord3D and Data formats keep their documented classifications."""
        self.assertTrue(pylon.IsColorImage(pylon.PixelType_Coord3D_ABC32f))
        self.assertTrue(pylon.IsFloatingPoint(pylon.PixelType_Coord3D_ABC32f))
        self.assertEqual(pylon.SamplesPerPixel(pylon.PixelType_Coord3D_ABC32f), 3)
        self.assertEqual(pylon.BitPerPixel(pylon.PixelType_Coord3D_ABC32f), 96)

        self.assertTrue(pylon.IsMono(pylon.PixelType_Data64f))
        self.assertTrue(pylon.IsFloatingPoint(pylon.PixelType_Data64f))
        self.assertEqual(pylon.BitDepth(pylon.PixelType_Data64f), 64)

    # ------------------------------------------------------------------
    # Buffer geometry helpers
    # ------------------------------------------------------------------

    def test_compute_stride_returns_ok_flag_and_byte_count(self):
        """ComputeStride returns [True, stride_bytes] for valid pixel types."""
        ok, stride = pylon.ComputeStride(pylon.PixelType_Mono8, 640)
        self.assertTrue(ok)
        self.assertEqual(stride, 640)

        ok, stride = pylon.ComputeStride(pylon.PixelType_RGB8packed, 640)
        self.assertTrue(ok)
        self.assertEqual(stride, 1920)

    def test_compute_stride_includes_padding(self):
        """ComputeStride adds paddingX bytes to the result."""
        ok, stride_no_pad = pylon.ComputeStride(pylon.PixelType_Mono8, 640)
        ok, stride_padded = pylon.ComputeStride(pylon.PixelType_Mono8, 640, 4)
        self.assertTrue(ok)
        self.assertEqual(stride_padded, stride_no_pad + 4)

    def test_compute_padding_x_recovers_padding_from_stride(self):
        """ComputePaddingX inverts ComputeStride to recover the padding bytes."""
        _, stride = pylon.ComputeStride(pylon.PixelType_Mono8, 640, 4)
        padding = pylon.ComputePaddingX(stride, pylon.PixelType_Mono8, 640)
        self.assertEqual(padding, 4)

        _, stride_no_pad = pylon.ComputeStride(pylon.PixelType_Mono8, 640)
        self.assertEqual(pylon.ComputePaddingX(stride_no_pad, pylon.PixelType_Mono8, 640), 0)

    def test_compute_buffer_size_equals_stride_times_height(self):
        """ComputeBufferSize equals stride × height for simple and padded cases."""
        self.assertEqual(
            pylon.ComputeBufferSize(pylon.PixelType_Mono8, 640, 480),
            640 * 480,
        )
        self.assertEqual(
            pylon.ComputeBufferSize(pylon.PixelType_RGB8packed, 640, 480),
            1920 * 480,
        )
        _, padded_stride = pylon.ComputeStride(pylon.PixelType_Mono8, 640, 4)
        self.assertEqual(
            pylon.ComputeBufferSize(pylon.PixelType_Mono8, 640, 480, 4),
            padded_stride * 480,
        )


if __name__ == "__main__":
    unittest.main()
