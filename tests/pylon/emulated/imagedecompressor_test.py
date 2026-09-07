"""\
This unit test checks the pypylon API exposed by `src/pylon/ImageDecompressor.i`.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import gc
import unittest

# These Mono8 decompression fixtures were copied from
# `tests/pylon/decompression_test.py` so this emulated suite stays
# self-contained while still using the same documented descriptor/payload pair.
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

COMPRESSED_PAYLOAD_MONO8 = (
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

EXPECTED_DECOMPRESSED_WIDTH = 32
EXPECTED_DECOMPRESSED_HEIGHT = 32
EXPECTED_DECOMPRESSED_OFFSETX = 16
EXPECTED_DECOMPRESSED_OFFSETY = 8


class ImageDecompressorTestSuite(PylonEmuTestCase):
    def _expected_image_decompressor_methods(self):
        return frozenset((
            "SetCompressionDescriptor",
            "GetCompressionMode",
            "GetCompressionInfo",
            "ComputeCompressionDescriptorHash",
            "GetCurrentCompressionDescriptorHash",
            "GetCompressionDescriptorHash",
            "DecompressImage",
            "HasCompressionDescriptor",
            "ResetCompressionDescriptor",
            "GetImageSizeForDecompression",
            "GetCompressionDescriptor",
            "GetCurrentCompressionDescriptor",
        ))

    def _expected_compression_info_fields(self):
        return frozenset((
            "hasCompressedImage",
            "compressionStatus",
            "lossy",
            "pixelType",
            "width",
            "height",
            "offsetX",
            "offsetY",
            "paddingX",
            "paddingY",
            "decompressedImageSize",
            "decompressedPayloadSize",
        ))

    def _make_configured_decompressor(self):
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        return decompressor

    def _assert_mono8_descriptor_hash(self, descriptor_hash):
        self.assertEqual(bytes(descriptor_hash), DESCRIPTOR_HASH_MONO8)

    def _make_populated_compression_info(self):
        info = pylon.CompressionInfo()
        info.hasCompressedImage = True
        info.compressionStatus = pylon.CompressionStatus_Ok
        info.lossy = True
        info.pixelType = pylon.PixelType_Mono8
        info.width = 640
        info.height = 480
        info.offsetX = 16
        info.offsetY = 32
        info.paddingX = 4
        info.paddingY = 2
        info.decompressedImageSize = 640 * 480
        info.decompressedPayloadSize = 640 * 480 + 128
        return info

    # ------------------------------------------------------------------
    # %rename + %ignore directives
    #     %rename(ImageDecompressor) Pylon::CImageDecompressor;
    #     %rename(CompressionInfo)   Pylon::CompressionInfo_t;
    # ------------------------------------------------------------------

    def test_renamed_classes_are_exposed(self):
        """ImageDecompressor.i exposes the renamed ImageDecompressor and CompressionInfo classes on pylon."""
        self.assertTrue(hasattr(pylon, "ImageDecompressor"))
        self.assertTrue(hasattr(pylon, "CompressionInfo"))
        self.assertIsInstance(pylon.ImageDecompressor, type)
        self.assertIsInstance(pylon.CompressionInfo, type)

    def test_original_names_are_hidden(self):
        """Neither the C-prefixed class names nor the enum type names are exposed on pylon."""
        self.assertFalse(hasattr(pylon, "CImageDecompressor"))
        self.assertFalse(hasattr(pylon, "CompressionInfo_t"))
        self.assertFalse(hasattr(pylon, "EEndianness"))
        self.assertFalse(hasattr(pylon, "ECompressionStatus"))
        self.assertFalse(hasattr(pylon, "ECompressionMode"))

    # ------------------------------------------------------------------
    # EEndianness / ECompressionStatus / ECompressionMode enums
    # from <pylon/ImageDecompressor.h>
    # ------------------------------------------------------------------

    def test_endianness_constants_are_exposed(self):
        """Every EEndianness enum member declared in pylon/ImageDecompressor.h is exposed on pylon as an int."""
        self.assertIsInstance(pylon.Endianness_Little, int)
        self.assertIsInstance(pylon.Endianness_Big, int)
        self.assertIsInstance(pylon.Endianness_Auto, int)

    def test_endianness_values_match_header_declaration(self):
        """Every Endianness_* constant has the integer value documented in pylon/ImageDecompressor.h."""
        self.assertEqual(pylon.Endianness_Little, 0)
        self.assertEqual(pylon.Endianness_Big, 1)
        self.assertEqual(pylon.Endianness_Auto, 2)

    def test_endianness_runtime_surface_matches_expected(self):
        """The set of pylon.Endianness_* attributes at runtime equals the exhaustive expected set."""
        runtime = frozenset(n for n in dir(pylon) if n.startswith("Endianness_"))
        expected = frozenset(("Endianness_Little", "Endianness_Big", "Endianness_Auto"))
        self.assertFalse(expected - runtime, "missing: %s" % sorted(expected - runtime))
        self.assertFalse(runtime - expected, "unexpected: %s" % sorted(runtime - expected))

    def test_compression_status_constants_are_exposed(self):
        """Every ECompressionStatus enum member is exposed on pylon as an int."""
        self.assertIsInstance(pylon.CompressionStatus_Ok, int)
        self.assertIsInstance(pylon.CompressionStatus_BufferOverflow, int)
        self.assertIsInstance(pylon.CompressionStatus_Error, int)

    def test_compression_status_values_match_header_declaration(self):
        """Every CompressionStatus_* constant has the integer value documented in pylon/ImageDecompressor.h."""
        self.assertEqual(pylon.CompressionStatus_Ok, 0)
        self.assertEqual(pylon.CompressionStatus_BufferOverflow, 1)
        self.assertEqual(pylon.CompressionStatus_Error, 2)

    def test_compression_status_runtime_surface_matches_expected(self):
        """The set of pylon.CompressionStatus_* attributes at runtime equals the exhaustive expected set."""
        runtime = frozenset(n for n in dir(pylon) if n.startswith("CompressionStatus_"))
        expected = frozenset((
            "CompressionStatus_Ok",
            "CompressionStatus_BufferOverflow",
            "CompressionStatus_Error",
        ))
        self.assertFalse(expected - runtime, "missing: %s" % sorted(expected - runtime))
        self.assertFalse(runtime - expected, "unexpected: %s" % sorted(runtime - expected))

    def test_compression_mode_constants_are_exposed(self):
        """Every ECompressionMode enum member is exposed on pylon as an int."""
        self.assertIsInstance(pylon.CompressionMode_Off, int)
        self.assertIsInstance(pylon.CompressionMode_BaslerLossless, int)
        self.assertIsInstance(pylon.CompressionMode_BaslerFixRatio, int)
        self.assertIsInstance(pylon.CompressionMode_JPEGFixQuality, int)

    def test_compression_mode_values_match_header_declaration(self):
        """Every CompressionMode_* constant has the integer value documented in pylon/ImageDecompressor.h."""
        self.assertEqual(pylon.CompressionMode_Off, 0)
        self.assertEqual(pylon.CompressionMode_BaslerLossless, 1)
        self.assertEqual(pylon.CompressionMode_BaslerFixRatio, 2)
        self.assertEqual(pylon.CompressionMode_JPEGFixQuality, 3)

    def test_compression_mode_runtime_surface_matches_expected(self):
        """The set of pylon.CompressionMode_* attributes at runtime equals the exhaustive expected set."""
        runtime = frozenset(n for n in dir(pylon) if n.startswith("CompressionMode_"))
        expected = frozenset((
            "CompressionMode_Off",
            "CompressionMode_BaslerLossless",
            "CompressionMode_BaslerFixRatio",
            "CompressionMode_JPEGFixQuality",
        ))
        self.assertFalse(expected - runtime, "missing: %s" % sorted(expected - runtime))
        self.assertFalse(runtime - expected, "unexpected: %s" % sorted(runtime - expected))

    def test_enum_values_are_pairwise_distinct_within_each_enum(self):
        """Within each enum, every mapped constant has a distinct integer value."""
        self.assertEqual(
            len({pylon.Endianness_Little, pylon.Endianness_Big, pylon.Endianness_Auto}),
            3,
        )
        self.assertEqual(
            len({
                pylon.CompressionStatus_Ok,
                pylon.CompressionStatus_BufferOverflow,
                pylon.CompressionStatus_Error,
            }),
            3,
        )
        self.assertEqual(
            len({
                pylon.CompressionMode_Off,
                pylon.CompressionMode_BaslerLossless,
                pylon.CompressionMode_BaslerFixRatio,
                pylon.CompressionMode_JPEGFixQuality,
            }),
            4,
        )

    # ------------------------------------------------------------------
    # ImageDecompressor construction
    # ------------------------------------------------------------------

    def test_image_decompressor_default_construction(self):
        """Default construction produces a usable ImageDecompressor that owns no descriptor yet."""
        decompressor = pylon.ImageDecompressor()
        self.assertIsInstance(decompressor, pylon.ImageDecompressor)
        self.assertFalse(decompressor.HasCompressionDescriptor())

    # ------------------------------------------------------------------
    # CImageDecompressor(const CImageDecompressor&) – copy constructor
    # ------------------------------------------------------------------

    def test_copy_construction_of_default_decompressor_has_no_descriptor(self):
        """Copy-constructing a default (unconfigured) ImageDecompressor yields a new instance with no descriptor."""
        original = pylon.ImageDecompressor()
        copy = pylon.ImageDecompressor(original)
        self.assertIsInstance(copy, pylon.ImageDecompressor)
        self.assertFalse(copy.HasCompressionDescriptor())

    def test_copy_construction_propagates_installed_descriptor(self):
        """Copy-constructing a configured ImageDecompressor yields a copy that also owns a compression descriptor."""
        original = self._make_configured_decompressor()
        copy = pylon.ImageDecompressor(original)
        self.assertIsInstance(copy, pylon.ImageDecompressor)
        self.assertTrue(copy.HasCompressionDescriptor())

    def test_copy_construction_preserves_descriptor_hash(self):
        """The descriptor hash of the copy equals the descriptor hash of the original."""
        original = self._make_configured_decompressor()
        copy = pylon.ImageDecompressor(original)
        self.assertEqual(
            bytes(copy.GetCurrentCompressionDescriptorHash()),
            bytes(original.GetCurrentCompressionDescriptorHash()),
        )

    def test_copy_construction_hash_matches_documented_mono8_fixture(self):
        """The copy's descriptor hash equals the documented Mono8 hash, confirming the descriptor was copied faithfully."""
        original = self._make_configured_decompressor()
        copy = pylon.ImageDecompressor(original)
        self._assert_mono8_descriptor_hash(copy.GetCurrentCompressionDescriptorHash())

    def test_copy_construction_produces_independent_instance(self):
        """Resetting the descriptor on the copy does not affect the original, and vice versa."""
        original = self._make_configured_decompressor()
        copy = pylon.ImageDecompressor(original)
        copy.ResetCompressionDescriptor()
        self.assertFalse(copy.HasCompressionDescriptor())
        self.assertTrue(original.HasCompressionDescriptor())

    # ------------------------------------------------------------------
    # CImageDecompressor(GenApi::INodeMap&) – node-map constructor
    # ------------------------------------------------------------------

    def test_nodemap_construction_accepts_instant_camera_nodemap(self):
        """ImageDecompressor(nodeMap) accepts an InstantCamera.NodeMap."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            if camera.ImageCompressionMode.IsWritable() and \
               camera.DeviceInfo.DeviceClass != pylon.BaslerCamEmuDeviceClass:
                camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
                pylon.ImageDecompressor(camera.NodeMap)
            else:
                try:
                    pylon.ImageDecompressor(camera.NodeMap)
                    self.fail("Expected RuntimeException was not raised")
                except pylon.RuntimeException as exc:
                    pass

    def test_nodemap_construction_raises_when_compression_is_disabled(self):
        """ImageDecompressor(nodeMap) raises RuntimeException when the camera has compression disabled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            try:
                camera.ImageCompressionMode.TrySetValue("Off")
                pylon.ImageDecompressor(camera.NodeMap)
                self.fail("Expected RuntimeException was not raised")
            except pylon.RuntimeException as exc:
                self.assertIn("Compression is disabled", str(exc))

    # ------------------------------------------------------------------
    # GetImageSizeForDecompression test
    # ------------------------------------------------------------------

    def test_nodemap_construction_accepts_instant_camera_nodemap(self):
        """ImageDecompressor provides GetImageSizeForDecompression."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            if camera.ImageCompressionMode.IsWritable() and \
                    camera.DeviceInfo.DeviceClass != pylon.BaslerCamEmuDeviceClass:
                camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
                image_size = pylon.ImageDecompressor.GetImageSizeForDecompression(camera.NodeMap)
                self.assertGreaterEqual(image_size, 0)
            else:
                try:
                    image_size = pylon.ImageDecompressor.GetImageSizeForDecompression(camera.NodeMap)
                    self.fail("Expected RuntimeException was not raised")
                except pylon.RuntimeException as exc:
                    pass

    # ------------------------------------------------------------------
    # ImageDecompressor construction and public-method surface
    # ------------------------------------------------------------------

    def test_image_decompressor_method_surface_matches_expected(self):
        """pylon.ImageDecompressor exposes exactly the expected set of public methods."""
        runtime = frozenset(
            name for name in dir(pylon.ImageDecompressor)
            if not name.startswith("_") and name != "thisown"
        )
        expected = self._expected_image_decompressor_methods()
        missing = expected - runtime
        unexpected = runtime - expected
        self.assertFalse(missing, "missing methods on ImageDecompressor: %s" % sorted(missing))
        self.assertFalse(unexpected, "unexpected methods on ImageDecompressor: %s" % sorted(unexpected))

    def test_image_decompressor_expected_methods_are_callable(self):
        """Every method advertised in the contract resolves to a callable on an ImageDecompressor instance."""
        decompressor = pylon.ImageDecompressor()
        for method_name in self._expected_image_decompressor_methods():
            with self.subTest(method=method_name):
                self.assertTrue(callable(getattr(decompressor, method_name)))

    # ------------------------------------------------------------------
    # ImageDecompressor.SetCompressionDescriptor (custom %extend overload
    # with extractByteLikePyObject helper)
    # ------------------------------------------------------------------

    def test_set_compression_descriptor_rejects_non_bytes_types(self):
        """SetCompressionDescriptor rejects non-bytes/bytearray inputs with an InvalidArgumentException."""
        decompressor = pylon.ImageDecompressor()
        for bad in ("astring", 123, 3.14, [1, 2, 3], None, (b"tuple",)):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(pylon.InvalidArgumentException):
                    decompressor.SetCompressionDescriptor(bad)

    def test_set_compression_descriptor_rejects_empty_buffer(self):
        """SetCompressionDescriptor rejects an empty buffer with an InvalidArgumentException."""
        decompressor = pylon.ImageDecompressor()
        for empty in (b"", bytearray()):
            with self.subTest(arg=repr(empty)):
                with self.assertRaises(pylon.InvalidArgumentException):
                    decompressor.SetCompressionDescriptor(empty)

    def test_set_compression_descriptor_rejects_malformed_descriptor(self):
        """SetCompressionDescriptor rejects non-empty but incompatible descriptor data with a RuntimeException."""
        decompressor = pylon.ImageDecompressor()
        for malformed in (b"garbage", bytearray(b"garbage"), b"\x00" * 16):
            with self.subTest(arg=repr(malformed)):
                with self.assertRaises(pylon.RuntimeException):
                    decompressor.SetCompressionDescriptor(malformed)

    def test_set_compression_descriptor_failure_leaves_state_unchanged(self):
        """A rejected SetCompressionDescriptor call on a fresh instance leaves HasCompressionDescriptor False."""
        decompressor = pylon.ImageDecompressor()
        with self.assertRaises(pylon.RuntimeException):
            decompressor.SetCompressionDescriptor(b"garbage")
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_set_compression_descriptor_installs_valid_descriptor(self):
        """SetCompressionDescriptor(valid_descriptor) flips HasCompressionDescriptor to True."""
        decompressor = pylon.ImageDecompressor()
        self.assertFalse(decompressor.HasCompressionDescriptor())
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        self.assertTrue(decompressor.HasCompressionDescriptor())

    def test_set_compression_descriptor_accepts_bytes_and_bytearray_for_valid_descriptor(self):
        """SetCompressionDescriptor installs the same descriptor from either bytes or bytearray inputs."""
        for descriptor in (COMPRESSION_DESCRIPTOR_MONO8, bytearray(COMPRESSION_DESCRIPTOR_MONO8)):
            with self.subTest(input_type=type(descriptor).__name__):
                decompressor = pylon.ImageDecompressor()
                decompressor.SetCompressionDescriptor(descriptor)
                self.assertTrue(decompressor.HasCompressionDescriptor())
                self._assert_mono8_descriptor_hash(
                    decompressor.GetCurrentCompressionDescriptorHash()
                )

    def test_set_compression_descriptor_is_idempotent_for_same_descriptor(self):
        """Installing the same valid descriptor twice leaves the decompressor in the installed state."""
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        self.assertTrue(decompressor.HasCompressionDescriptor())
        self._assert_mono8_descriptor_hash(decompressor.GetCurrentCompressionDescriptorHash())

    def test_set_compression_descriptor_failure_preserves_installed_descriptor(self):
        """A rejected SetCompressionDescriptor call does not clobber a previously installed descriptor."""
        decompressor = self._make_configured_decompressor()
        for bad in (None, b"", b"garbage" * 16):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises((pylon.InvalidArgumentException, pylon.RuntimeException)):
                    decompressor.SetCompressionDescriptor(bad)
                self.assertTrue(decompressor.HasCompressionDescriptor())
                self._assert_mono8_descriptor_hash(
                    decompressor.GetCurrentCompressionDescriptorHash()
                )

    # ------------------------------------------------------------------
    # SetCompressionDescriptor(GenApi::INodeMap&) – node-map overload
    # ------------------------------------------------------------------

    def test_set_compression_descriptor_from_nodemap_accepts_instant_camera_nodemap(self):
        """SetCompressionDescriptor(nodeMap) accepts an InstantCamera.NodeMap."""
        decompressor = pylon.ImageDecompressor()
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            if camera.ImageCompressionMode.IsWritable() and \
               camera.DeviceInfo.DeviceClass != pylon.BaslerCamEmuDeviceClass:
                camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
                decompressor.SetCompressionDescriptor(camera.NodeMap)
            else:
                try:
                    decompressor.SetCompressionDescriptor(camera.NodeMap)
                    self.fail("Expected RuntimeException was not raised")
                except pylon.RuntimeException as exc:
                    pass

    def test_set_compression_descriptor_from_nodemap_raises_when_compression_is_disabled(self):
        """SetCompressionDescriptor(nodeMap) raises RuntimeException when the camera has compression disabled."""
        decompressor = pylon.ImageDecompressor()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            try:
                camera.ImageCompressionMode.TrySetValue("Off")
                decompressor.SetCompressionDescriptor(camera.NodeMap)
                self.fail("Expected RuntimeException was not raised")
            except pylon.RuntimeException as exc:
                self.assertIn("Compression is disabled", str(exc))

    def test_set_compression_descriptor_from_nodemap_leaves_state_unchanged_on_failure(self):
        """A failed SetCompressionDescriptor(nodeMap) on a fresh instance leaves HasCompressionDescriptor False."""
        decompressor = pylon.ImageDecompressor()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.TrySetValue("Off")
            with self.assertRaises(pylon.RuntimeException):
                decompressor.SetCompressionDescriptor(camera.NodeMap)
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_set_compression_descriptor_from_nodemap_preserves_installed_descriptor_on_failure(self):
        """A failed SetCompressionDescriptor(nodeMap) does not clobber a previously installed descriptor."""
        decompressor = self._make_configured_decompressor()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.TrySetValue("Off")
            with self.assertRaises(pylon.RuntimeException):
                decompressor.SetCompressionDescriptor(camera.NodeMap)
        self.assertTrue(decompressor.HasCompressionDescriptor())
        self._assert_mono8_descriptor_hash(decompressor.GetCurrentCompressionDescriptorHash())

    # ------------------------------------------------------------------
    # ImageDecompressor.GetCompressionMode(nodeMap) – static node-map query
    # ------------------------------------------------------------------

    def test_get_compression_mode_returns_off_when_compression_is_disabled(self):
        """GetCompressionMode(nodeMap) returns CompressionMode_Off when compression is disabled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.TrySetValue("Off")
            result = pylon.ImageDecompressor.GetCompressionMode(camera.NodeMap)
            self.assertEqual(result, pylon.CompressionMode_Off)

    # ------------------------------------------------------------------
    # ImageDecompressor.ComputeCompressionDescriptorHash (pure hash over
    # the input buffer; no descriptor parsing required)
    # ------------------------------------------------------------------

    def test_compute_compression_descriptor_hash_rejects_non_bytes_types(self):
        """ComputeCompressionDescriptorHash rejects non-bytes/bytearray inputs with an InvalidArgumentException."""
        for bad in ("astring", 123, 3.14, [1, 2, 3], None):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(pylon.InvalidArgumentException):
                    pylon.ImageDecompressor.ComputeCompressionDescriptorHash(bad)

    def test_compute_compression_descriptor_hash_rejects_empty_buffer(self):
        """ComputeCompressionDescriptorHash rejects an empty buffer with an InvalidArgumentException."""
        decompressor = pylon.ImageDecompressor()
        with self.assertRaises(pylon.InvalidArgumentException):
            decompressor.ComputeCompressionDescriptorHash(b"")

    def test_compute_compression_descriptor_hash_returns_bytearray(self):
        """ComputeCompressionDescriptorHash returns a non-empty bytearray for any non-empty bytes input."""
        decompressor = pylon.ImageDecompressor()
        result = decompressor.ComputeCompressionDescriptorHash(b"some-descriptor-blob")
        self.assertIsInstance(result, bytearray)
        self.assertGreater(len(result), 0)

    def test_compute_compression_descriptor_hash_accepts_bytes_and_bytearray_identically(self):
        """ComputeCompressionDescriptorHash accepts both bytes and bytearray and hashes identical content identically."""
        decompressor = pylon.ImageDecompressor()
        payload = b"some-descriptor-blob"
        self.assertEqual(
            decompressor.ComputeCompressionDescriptorHash(payload),
            decompressor.ComputeCompressionDescriptorHash(bytearray(payload)),
        )

    def test_compute_compression_descriptor_hash_is_deterministic(self):
        """ComputeCompressionDescriptorHash returns the same value for identical inputs on repeated calls."""
        decompressor = pylon.ImageDecompressor()
        payload = b"some-descriptor-blob"
        self.assertEqual(
            decompressor.ComputeCompressionDescriptorHash(payload),
            decompressor.ComputeCompressionDescriptorHash(payload),
        )

    def test_compute_compression_descriptor_hash_differs_for_different_inputs(self):
        """ComputeCompressionDescriptorHash produces different hashes for different input buffers."""
        decompressor = pylon.ImageDecompressor()
        self.assertNotEqual(
            decompressor.ComputeCompressionDescriptorHash(b"input-A"),
            decompressor.ComputeCompressionDescriptorHash(b"input-B-that-is-longer"),
        )

    def test_compute_compression_descriptor_hash_matches_documented_mono8_fixture(self):
        """ComputeCompressionDescriptorHash of the Mono8 descriptor equals the documented hash value."""
        decompressor = pylon.ImageDecompressor()
        self._assert_mono8_descriptor_hash(
            decompressor.ComputeCompressionDescriptorHash(COMPRESSION_DESCRIPTOR_MONO8)
        )

    # ------------------------------------------------------------------
    # ImageDecompressor.GetCurrentCompressionDescriptorHash (no-arg variant;
    # requires a compression descriptor to have been set)
    # ------------------------------------------------------------------

    def test_get_current_compression_descriptor_hash_without_descriptor_raises(self):
        """GetCurrentCompressionDescriptorHash raises a RuntimeException when no descriptor has been set."""
        decompressor = pylon.ImageDecompressor()
        self.assertFalse(decompressor.HasCompressionDescriptor())
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCurrentCompressionDescriptorHash()

    def test_get_current_compression_descriptor_hash_after_set_returns_installed_hash(self):
        """GetCurrentCompressionDescriptorHash returns the documented hash after a valid descriptor has been installed."""
        decompressor = self._make_configured_decompressor()
        result = decompressor.GetCurrentCompressionDescriptorHash()
        self.assertIsInstance(result, bytearray)
        self._assert_mono8_descriptor_hash(result)

    def test_get_current_compression_descriptor_hash_matches_compute_hash(self):
        """After installing a descriptor, GetCurrentCompressionDescriptorHash and ComputeCompressionDescriptorHash agree."""
        decompressor = self._make_configured_decompressor()
        self.assertEqual(
            decompressor.GetCurrentCompressionDescriptorHash(),
            decompressor.ComputeCompressionDescriptorHash(COMPRESSION_DESCRIPTOR_MONO8),
        )

    # ------------------------------------------------------------------
    # ImageDecompressor.GetCompressionDescriptor(nodemap) (static)
    # ImageDecompressor.GetCurrentCompressionDescriptor() (instance; requires descriptor to be set)
    # ------------------------------------------------------------------

    def test_get_compression_descriptor_without_descriptor_raises(self):
        """GetCurrentCompressionDescriptor() raises a RuntimeException when no descriptor has been set."""
        decompressor = pylon.ImageDecompressor()
        self.assertFalse(decompressor.HasCompressionDescriptor())
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCurrentCompressionDescriptor()

    def test_get_compression_descriptor_returns_bytearray(self):
        """GetCurrentCompressionDescriptor() returns a non-empty bytearray after a valid descriptor has been installed."""
        decompressor = self._make_configured_decompressor()
        result = decompressor.GetCurrentCompressionDescriptor()
        self.assertIsInstance(result, bytearray)
        self.assertGreater(len(result), 0)

    def test_get_compression_descriptor_matches_installed_descriptor(self):
        """GetCurrentCompressionDescriptor() returns the exact bytes of the installed descriptor."""
        decompressor = self._make_configured_decompressor()
        result = decompressor.GetCurrentCompressionDescriptor()
        self.assertEqual(bytes(result), bytes(COMPRESSION_DESCRIPTOR_MONO8))

    def test_get_compression_descriptor_roundtrip(self):
        """A descriptor retrieved via GetCurrentCompressionDescriptor() can be reinstalled and yields the same hash."""
        original = self._make_configured_decompressor()
        retrieved = original.GetCurrentCompressionDescriptor()

        reinstalled = pylon.ImageDecompressor()
        reinstalled.SetCompressionDescriptor(retrieved)
        self.assertTrue(reinstalled.HasCompressionDescriptor())
        self.assertEqual(
            reinstalled.GetCurrentCompressionDescriptorHash(),
            original.GetCurrentCompressionDescriptorHash(),
        )

    def test_get_compression_descriptor_raises_after_reset(self):
        """GetCurrentCompressionDescriptor() raises again after ResetCompressionDescriptor has cleared the descriptor."""
        decompressor = self._make_configured_decompressor()
        decompressor.ResetCompressionDescriptor()
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCurrentCompressionDescriptor()

    def test_get_compression_descriptor_from_nodemap_raises_when_compression_is_disabled(self):
        """GetCompressionDescriptor(nodeMap) raises RuntimeException when compression is disabled in the camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.TrySetValue("Off")
            with self.assertRaises(pylon.RuntimeException):
                pylon.ImageDecompressor.GetCompressionDescriptor(camera.NodeMap)

    def test_get_compression_descriptor_from_nodemap_accepts_instant_camera_nodemap(self):
        """GetCompressionDescriptor(nodeMap) accepts an InstantCamera.NodeMap."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            if camera.ImageCompressionMode.IsWritable() and \
               camera.DeviceInfo.DeviceClass != pylon.BaslerCamEmuDeviceClass:
                camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
                result = pylon.ImageDecompressor.GetCompressionDescriptor(camera.NodeMap)
                self.assertIsInstance(result, bytearray)
                self.assertGreater(len(result), 0)
            else:
                try:
                    pylon.ImageDecompressor.GetCompressionDescriptor(camera.NodeMap)
                    self.fail("Expected RuntimeException was not raised")
                except pylon.RuntimeException:
                    pass

    def test_get_compression_descriptor_instance_and_nodemap_agree(self):
        """GetCurrentCompressionDescriptor() and GetCompressionDescriptor(nodeMap) return identical bytes when both are available."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            if not (camera.ImageCompressionMode.IsWritable() and
                    camera.DeviceInfo.DeviceClass != pylon.BaslerCamEmuDeviceClass):
                self.skipTest("Camera does not support compression; skipping nodemap vs instance comparison")
            camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
            decompressor = pylon.ImageDecompressor(camera.NodeMap)
            from_instance = decompressor.GetCurrentCompressionDescriptor()
            from_nodemap = pylon.ImageDecompressor.GetCompressionDescriptor(camera.NodeMap)
            self.assertEqual(bytes(from_instance), bytes(from_nodemap))

    # ------------------------------------------------------------------
    # ImageDecompressor.GetCompressionInfo (introspective, non-validating
    # call that returns a CompressionInfo for any byte-like input)
    # ------------------------------------------------------------------

    def test_get_compression_info_rejects_non_bytes_types(self):
        """GetCompressionInfo rejects non-bytes/bytearray inputs with an InvalidArgumentException."""
        decompressor = pylon.ImageDecompressor()
        for bad in ("astring", 123, 3.14, [1, 2, 3], None):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(TypeError):
                    decompressor.GetCompressionInfo(bad)

    def test_get_compression_info_returns_compression_info_for_uncompressed_buffer(self):
        """GetCompressionInfo returns a CompressionInfo with hasCompressedImage=False for arbitrary uncompressed bytes."""
        decompressor = pylon.ImageDecompressor()
        info = decompressor.GetCompressionInfo(b"\x00" * 128)
        self.assertIsInstance(info, pylon.CompressionInfo)
        self.assertFalse(info.hasCompressedImage)
        self.assertEqual(info.compressionStatus, pylon.CompressionStatus_Error)

    def test_get_compression_info_accepts_all_endianness_values(self):
        """GetCompressionInfo accepts every documented EEndianness value as the optional second argument."""
        decompressor = pylon.ImageDecompressor()
        self.assertIsInstance(
            decompressor.GetCompressionInfo(b"\x00" * 128, pylon.Endianness_Little),
            pylon.CompressionInfo,
        )
        self.assertIsInstance(
            decompressor.GetCompressionInfo(b"\x00" * 128, pylon.Endianness_Big),
            pylon.CompressionInfo,
        )
        self.assertIsInstance(
            decompressor.GetCompressionInfo(b"\x00" * 128, pylon.Endianness_Auto),
            pylon.CompressionInfo,
        )

    def test_get_compression_info_accepts_bytes_and_bytearray(self):
        """GetCompressionInfo accepts both bytes and bytearray inputs via the shared %typemap."""
        decompressor = pylon.ImageDecompressor()
        self.assertIsInstance(
            decompressor.GetCompressionInfo(b"\x00" * 64), pylon.CompressionInfo
        )
        self.assertIsInstance(
            decompressor.GetCompressionInfo(bytearray(64)), pylon.CompressionInfo
        )

    def test_get_compression_info_reports_compressed_payload_correctly(self):
        """GetCompressionInfo on the Mono8 compressed payload returns every documented image attribute."""
        decompressor = pylon.ImageDecompressor()
        info = decompressor.GetCompressionInfo(COMPRESSED_PAYLOAD_MONO8)
        self.assertTrue(info.hasCompressedImage)
        self.assertEqual(info.compressionStatus, pylon.CompressionStatus_Ok)
        self.assertFalse(info.lossy)
        self.assertEqual(info.pixelType, pylon.PixelType_Mono8)
        self.assertEqual(info.width,   EXPECTED_DECOMPRESSED_WIDTH)
        self.assertEqual(info.height,  EXPECTED_DECOMPRESSED_HEIGHT)
        self.assertEqual(info.offsetX, EXPECTED_DECOMPRESSED_OFFSETX)
        self.assertEqual(info.offsetY, EXPECTED_DECOMPRESSED_OFFSETY)
        self.assertEqual(
            info.decompressedImageSize,
            EXPECTED_DECOMPRESSED_WIDTH * EXPECTED_DECOMPRESSED_HEIGHT,
        )

    def test_get_compression_info_from_grab_result(self):
        """GetCompressionInfo from grab result can be read."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.Value = "BaslerCompressionBeyond"
            grab_result = camera.GrabOne(1000)
            self.assertTrue(grab_result.GrabSucceeded())
            compression_info_1 = pylon.ImageDecompressor.GetCompressionInfo(grab_result)
            compression_info_2 = pylon.ImageDecompressor.GetCompressionInfo(grab_result, pylon.Endianness_Auto)
            self.assertIsInstance(compression_info_1, pylon.CompressionInfo)
            self.assertIsInstance(compression_info_2, pylon.CompressionInfo)
            self.assertEqual(compression_info_1.to_dict(), compression_info_2.to_dict())

    # ------------------------------------------------------------------
    # ImageDecompressor.GetCompressionDescriptorHash (buffer variant;
    # requires parsable chunk data)
    # ------------------------------------------------------------------

    def test_get_compression_descriptor_hash_rejects_non_bytes_types(self):
        """GetCompressionDescriptorHash rejects non-bytes/bytearray inputs with an InvalidArgumentException."""
        decompressor = pylon.ImageDecompressor()
        for bad in ("astring", 123, 3.14, [1, 2, 3], None):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(pylon.InvalidArgumentException):
                    decompressor.GetCompressionDescriptorHash(bad)

    def test_get_compression_descriptor_hash_rejects_unparsable_chunk_data(self):
        """GetCompressionDescriptorHash raises a RuntimeException when the payload cannot be parsed as chunk data."""
        decompressor = pylon.ImageDecompressor()
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCompressionDescriptorHash(b"garbage-chunk-payload")

    def test_get_compression_descriptor_hash_accepts_endianness_argument(self):
        """GetCompressionDescriptorHash accepts every documented EEndianness value (although the emulator buffers still fail parsing)."""
        decompressor = pylon.ImageDecompressor()
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCompressionDescriptorHash(
                b"garbage-chunk-payload", pylon.Endianness_Little
            )
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCompressionDescriptorHash(
                b"garbage-chunk-payload", pylon.Endianness_Big
            )
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCompressionDescriptorHash(
                b"garbage-chunk-payload", pylon.Endianness_Auto
            )

    def test_get_compression_descriptor_hash_extracts_hash_from_compressed_payload(self):
        """GetCompressionDescriptorHash on the Mono8 compressed payload returns the documented descriptor hash."""
        decompressor = pylon.ImageDecompressor()
        result = decompressor.GetCompressionDescriptorHash(COMPRESSED_PAYLOAD_MONO8)
        self.assertIsInstance(result, bytearray)
        self._assert_mono8_descriptor_hash(result)

    def test_get_compression_descriptor_hash_from_grab_result_buffer(self):
        """GetCompressionDescriptorHash called with grab_result.Buffer returns a non-empty bytearray."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.ImageCompressionMode.TrySetValue("BaslerCompressionBeyond")
            with camera.GrabOne(1000) as grab_result:
                self.assertTrue(grab_result.GrabSucceeded())
                result = pylon.ImageDecompressor.GetCompressionDescriptorHash(grab_result.Buffer)
                self.assertIsInstance(result, bytearray)
                self.assertGreater(len(result), 0)

    # ------------------------------------------------------------------
    # ImageDecompressor.DecompressImage (two %extend overloads:
    #     (CGrabResultPtr) and (bytes-via-typemap))
    # ------------------------------------------------------------------

    def test_decompress_image_rejects_unsupported_argument_types(self):
        """DecompressImage rejects inputs that are neither a grab result nor a byte-like buffer with a TypeError."""
        decompressor = pylon.ImageDecompressor()
        for bad in ("astring", 123, 3.14, [1, 2, 3], None):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(TypeError):
                    decompressor.DecompressImage(bad)

    def test_decompress_image_bytes_variant_does_not_accept_endianness(self):
        """DecompressImage(bytes) does not expose an endianness overload; passing two arguments raises TypeError."""
        decompressor = pylon.ImageDecompressor()
        with self.assertRaises(TypeError):
            decompressor.DecompressImage(b"compressed-blob", pylon.Endianness_Auto)

    def test_decompress_image_bytes_variant_on_uncompressed_buffer_raises(self):
        """DecompressImage(bytes) raises a RuntimeException when the buffer contains no compressed payload."""
        decompressor = pylon.ImageDecompressor()
        for payload in (b"\x00" * 128, bytearray(128)):
            with self.subTest(arg=type(payload).__name__):
                with self.assertRaises(pylon.RuntimeException):
                    decompressor.DecompressImage(payload)

    def test_decompress_image_grab_variant_on_uncompressed_grab_raises(self):
        """DecompressImage(grab_result) raises a RuntimeException for an uncompressed emulator grab."""
        decompressor = pylon.ImageDecompressor()
        camera = pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound)
        with camera:
            grab = camera.GrabOne(1000)
            self.assertTrue(grab.GrabSucceeded())
            with self.assertRaises(pylon.RuntimeException):
                decompressor.DecompressImage(grab)

    def test_decompress_image_bytes_variant_success_returns_expected_image(self):
        """DecompressImage(compressed_payload) returns a valid PylonImage with the documented Mono8 dimensions after installing the descriptor."""
        decompressor = self._make_configured_decompressor()
        image = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        self.assertIsInstance(image, pylon.PylonImage)
        self.assertTrue(image.IsValid())
        self.assertEqual(image.Width,       EXPECTED_DECOMPRESSED_WIDTH)
        self.assertEqual(image.Height,      EXPECTED_DECOMPRESSED_HEIGHT)
        self.assertEqual(image.PixelType,   pylon.PixelType_Mono8)
        self.assertEqual(
            len(image.GetBuffer()),
            EXPECTED_DECOMPRESSED_WIDTH * EXPECTED_DECOMPRESSED_HEIGHT,
        )

    def test_decompress_image_bytes_variant_decodes_payload_pixel_perfect(self):
        """DecompressImage produces the documented (x+y) test pattern for every pixel of the Mono8 reference payload."""
        decompressor = self._make_configured_decompressor()
        image = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        buffer = image.GetBuffer()
        for y in range(EXPECTED_DECOMPRESSED_HEIGHT):
            for x in range(EXPECTED_DECOMPRESSED_WIDTH):
                self.assertEqual(
                    buffer[y * EXPECTED_DECOMPRESSED_WIDTH + x],
                    (x + y) & 0xFF,
                    "Pixel mismatch at (x=%d, y=%d)" % (x, y),
                )

    def test_decompress_image_returned_image_is_owned_by_python(self):
        """The %typemap(out) for Pylon::CPylonImage* transfers SWIG_POINTER_OWN to the returned PylonImage."""
        decompressor = self._make_configured_decompressor()
        image = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        self.assertTrue(image.thisown)

    def test_decompress_image_returned_image_outlives_decompressor(self):
        """A returned PylonImage remains usable after the producing ImageDecompressor is destroyed (ownership is independent)."""
        decompressor = self._make_configured_decompressor()
        image = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        del decompressor
        gc.collect()
        self.assertTrue(image.IsValid())
        buffer = image.GetBuffer()
        self.assertEqual(
            len(buffer),
            EXPECTED_DECOMPRESSED_WIDTH * EXPECTED_DECOMPRESSED_HEIGHT,
        )
        self.assertEqual(buffer[0], 0)
        last_x = EXPECTED_DECOMPRESSED_WIDTH - 1
        last_y = EXPECTED_DECOMPRESSED_HEIGHT - 1
        self.assertEqual(
            buffer[last_y * EXPECTED_DECOMPRESSED_WIDTH + last_x],
            (last_x + last_y) & 0xFF,
        )

    def test_decompress_image_returns_distinct_images_per_call(self):
        """Consecutive DecompressImage calls return independent PylonImage wrappers, each owning its own CPylonImage."""
        decompressor = self._make_configured_decompressor()
        first = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        second = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)
        self.assertIsNot(first, second)
        self.assertTrue(first.thisown)
        self.assertTrue(second.thisown)
        self.assertEqual(bytes(first.GetBuffer()), bytes(second.GetBuffer()))

    def test_decompress_image_grab_variant_success_path_requires_real_camera(self):
        """DecompressImage(grab_result) success path is only reachable with a compression-capable camera; covered in tests/pylon/usb/decompression_test.py."""
        # The Basler camera emulator does not produce compressed grabs, so
        # the (CGrabResultPtr) overload's success branch cannot be driven
        # from this emulated suite.  The failure path for this overload is
        # verified by test_decompress_image_grab_variant_on_uncompressed_grab_raises.
        self.skipTest(
            "emulator cannot produce compressed grab results; "
            "success path exercised in tests/pylon/usb/decompression_test.py"
        )

    # ------------------------------------------------------------------
    # ImageDecompressor.HasCompressionDescriptor / ResetCompressionDescriptor
    # ------------------------------------------------------------------

    def test_has_compression_descriptor_is_false_on_fresh_instance(self):
        """HasCompressionDescriptor returns False on a freshly constructed ImageDecompressor."""
        self.assertFalse(pylon.ImageDecompressor().HasCompressionDescriptor())

    def test_reset_compression_descriptor_is_idempotent_on_fresh_instance(self):
        """ResetCompressionDescriptor is a no-op on a fresh ImageDecompressor and leaves HasCompressionDescriptor False."""
        decompressor = pylon.ImageDecompressor()
        decompressor.ResetCompressionDescriptor()
        decompressor.ResetCompressionDescriptor()
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_reset_compression_descriptor_clears_installed_descriptor(self):
        """ResetCompressionDescriptor clears a previously installed descriptor and makes the current-hash query raise again."""
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        self.assertTrue(decompressor.HasCompressionDescriptor())
        decompressor.ResetCompressionDescriptor()
        self.assertFalse(decompressor.HasCompressionDescriptor())
        with self.assertRaises(pylon.RuntimeException):
            decompressor.GetCurrentCompressionDescriptorHash()

    def test_reset_compression_descriptor_is_idempotent_after_clearing(self):
        """ResetCompressionDescriptor called twice in a row after a successful install leaves the decompressor cleared."""
        decompressor = pylon.ImageDecompressor()
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        decompressor.ResetCompressionDescriptor()
        decompressor.ResetCompressionDescriptor()
        self.assertFalse(decompressor.HasCompressionDescriptor())

    def test_set_after_reset_reinstalls_descriptor(self):
        """SetCompressionDescriptor installs the descriptor again after ResetCompressionDescriptor has cleared it."""
        decompressor = self._make_configured_decompressor()
        decompressor.ResetCompressionDescriptor()
        self.assertFalse(decompressor.HasCompressionDescriptor())
        decompressor.SetCompressionDescriptor(COMPRESSION_DESCRIPTOR_MONO8)
        self.assertTrue(decompressor.HasCompressionDescriptor())
        self._assert_mono8_descriptor_hash(decompressor.GetCurrentCompressionDescriptorHash())

    # ------------------------------------------------------------------
    # ImageDecompressor.operator== (CImageDecompressor::operator==)
    # ------------------------------------------------------------------

    def test_equality_two_default_decompressors_are_equal(self):
        """Two default-constructed ImageDecompressors (no descriptor) compare equal."""
        a = pylon.ImageDecompressor()
        b = pylon.ImageDecompressor()
        self.assertTrue(a == b)
        self.assertFalse(a != b)

    def test_equality_decompressor_is_equal_to_itself(self):
        """An ImageDecompressor compares equal to itself regardless of whether it has a descriptor."""
        decompressor = self._make_configured_decompressor()
        self.assertTrue(decompressor == decompressor)

    def test_equality_copy_constructed_decompressor_is_equal_to_original(self):
        """A copy-constructed ImageDecompressor compares equal to the original."""
        original = self._make_configured_decompressor()
        copy = pylon.ImageDecompressor(original)
        self.assertTrue(original == copy)
        self.assertFalse(original != copy)

    def test_equality_configured_vs_default_decompressor_are_not_equal(self):
        """An ImageDecompressor with a descriptor is not equal to one without a descriptor."""
        configured = self._make_configured_decompressor()
        default = pylon.ImageDecompressor()
        self.assertFalse(configured == default)
        self.assertTrue(configured != default)

    def test_equality_after_reset_matches_default(self):
        """After ResetCompressionDescriptor, a formerly configured decompressor compares equal to a default one."""
        configured = self._make_configured_decompressor()
        default = pylon.ImageDecompressor()
        configured.ResetCompressionDescriptor()
        self.assertTrue(configured == default)

    # ------------------------------------------------------------------
    # CompressionInfo construction and field surface
    # ------------------------------------------------------------------

    def test_compression_info_default_construction(self):
        """Default construction produces a CompressionInfo with hasCompressedImage=False and an error status."""
        info = pylon.CompressionInfo()
        self.assertIsInstance(info, pylon.CompressionInfo)
        self.assertFalse(info.hasCompressedImage)
        self.assertEqual(info.compressionStatus, pylon.CompressionStatus_Error)

    def test_compression_info_exposes_every_expected_field(self):
        """Every field declared in Pylon::CompressionInfo_t is accessible on pylon.CompressionInfo."""
        info = pylon.CompressionInfo()
        for field_name in self._expected_compression_info_fields():
            with self.subTest(field=field_name):
                self.assertTrue(hasattr(info, field_name))

    def test_compression_info_fields_are_mutable(self):
        """Every public CompressionInfo field can be assigned and read back unchanged."""
        info = pylon.CompressionInfo()
        assignments = {
            "hasCompressedImage":       True,
            "compressionStatus":        pylon.CompressionStatus_Ok,
            "lossy":                    True,
            "pixelType":                pylon.PixelType_Mono8,
            "width":                    640,
            "height":                   480,
            "offsetX":                  16,
            "offsetY":                  32,
            "paddingX":                 4,
            "paddingY":                 2,
            "decompressedImageSize":    640 * 480,
            "decompressedPayloadSize":  640 * 480 + 128,
        }
        for field_name, value in assignments.items():
            with self.subTest(field=field_name):
                setattr(info, field_name, value)
                self.assertEqual(getattr(info, field_name), value)

    # ------------------------------------------------------------------
    # CompressionInfo.to_dict (added via %extend %pythoncode)
    # ------------------------------------------------------------------

    def test_compression_info_to_dict_returns_dict_with_expected_keys(self):
        """to_dict returns a dict whose keys equal the twelve documented CompressionInfo fields."""
        info = pylon.CompressionInfo()
        result = info.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(frozenset(result.keys()), self._expected_compression_info_fields())

    def test_compression_info_to_dict_values_mirror_attribute_values(self):
        """to_dict mirrors the live attribute values of the CompressionInfo instance."""
        info = pylon.CompressionInfo()
        info.width = 1280
        info.height = 720
        info.hasCompressedImage = True
        info.lossy = True
        result = info.to_dict()
        self.assertEqual(result["width"], 1280)
        self.assertEqual(result["height"], 720)
        self.assertTrue(result["hasCompressedImage"])
        self.assertTrue(result["lossy"])

    # ------------------------------------------------------------------
    # CompressionInfo.__repr__ (added via %extend %pythoncode)
    #
    # The wrapper pins the exact format:
    #     "<CompressionInfo " + repr(self.to_dict()) + ">"
    # Keep one formula test plus exact string checks for the default and a
    # populated instance so format regressions stay obvious.
    # ------------------------------------------------------------------

    def test_compression_info_repr_matches_wrapper_formula_exactly(self):
        """repr(CompressionInfo) equals '<CompressionInfo ' + repr(to_dict()) + '>' on every instance state."""
        default_info = pylon.CompressionInfo()
        populated_info = self._make_populated_compression_info()

        for label, info in (("default", default_info), ("populated", populated_info)):
            with self.subTest(instance=label):
                self.assertEqual(
                    repr(info),
                    "<CompressionInfo " + repr(info.to_dict()) + ">",
                )

    def test_compression_info_repr_default_instance_has_documented_string(self):
        """repr(default CompressionInfo) has the exact documented byte-for-byte string."""
        expected = (
            "<CompressionInfo {"
            "'hasCompressedImage': False, "
            "'compressionStatus': 2, "
            "'lossy': False, "
            "'pixelType': -1, "
            "'width': 0, "
            "'height': 0, "
            "'offsetX': 0, "
            "'offsetY': 0, "
            "'paddingX': 0, "
            "'paddingY': 0, "
            "'decompressedImageSize': 0, "
            "'decompressedPayloadSize': 0"
            "}>"
        )
        self.assertEqual(repr(pylon.CompressionInfo()), expected)

    def test_compression_info_repr_reflects_mutated_fields_in_exact_order(self):
        """repr(mutated CompressionInfo) has the exact documented string, with fields in to_dict insertion order."""
        info = self._make_populated_compression_info()

        expected = (
            "<CompressionInfo {"
            "'hasCompressedImage': True, "
            "'compressionStatus': 0, "
            "'lossy': True, "
            "'pixelType': %d, "
            "'width': 640, "
            "'height': 480, "
            "'offsetX': 16, "
            "'offsetY': 32, "
            "'paddingX': 4, "
            "'paddingY': 2, "
            "'decompressedImageSize': 307200, "
            "'decompressedPayloadSize': 307328"
            "}>"
        ) % pylon.PixelType_Mono8
        self.assertEqual(repr(info), expected)


    # ------------------------------------------------------------------
    # PylonImage.Array – numpy integration
    # ------------------------------------------------------------------

    def test_decompress_image_array_returns_numpy_array_with_correct_shape(self):
        """image.Array returns a 2-D numpy array whose shape matches (Width, Height) of the decompressed image."""
        try:
            import numpy as np
        except ImportError:
            self.skipTest("numpy is not installed")

        decompressor = self._make_configured_decompressor()
        image = decompressor.DecompressImage(COMPRESSED_PAYLOAD_MONO8)

        array = image.Array
        self.assertIsInstance(array, np.ndarray)
        self.assertEqual(array.shape, (image.Width, image.Height))


if __name__ == "__main__":
    unittest.main()
