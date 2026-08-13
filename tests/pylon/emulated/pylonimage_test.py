"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/PylonImage.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest
import os
import tempfile

_BARCODE_PNG = os.path.join(os.path.dirname(__file__), 'barcode01.png')
_BARCODE_WIDTH  = 1920
_BARCODE_HEIGHT = 1200
_BARCODE_PIXEL_TYPE = pylon.PixelType_Mono8
_BARCODE_FIRST_PIXEL = 143


def _make_mono8_image(width=64, height=48):
    """Return a valid Mono8 PylonImage filled with a saw-tooth byte pattern."""
    image_mono8 = pylon.PylonImage.Create(pylon.PixelType_Mono8, width, height)
    with image_mono8.GetArrayZeroCopy() as numpy_array:
        for y in range(image_mono8.Height):
            for x in range(image_mono8.Width):
                numpy_array[y, x] = (x + y) % 256
    return image_mono8


class PylonImageTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction / Create
    # ------------------------------------------------------------------

    def test_default_construction_produces_invalid_image(self):
        """Default-constructed PylonImage is invalid and all dimensions are zero."""
        image = pylon.PylonImage()
        self.assertFalse(image.IsValid())
        self.assertEqual(image.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(image.Width, 0)
        self.assertEqual(image.Height, 0)
        self.assertEqual(image.PaddingX, 0)
        self.assertEqual(image.ImageSize, 0)
        self.assertEqual(image.AllocatedBufferSize, 0)
        self.assertEqual(image.Orientation, pylon.ImageOrientation_TopDown)

    def test_default_construction_getter_methods_agree_with_properties(self):
        """Getter methods return the same values as the corresponding properties."""
        image = pylon.PylonImage()
        self.assertEqual(image.GetPixelType(), image.PixelType)
        self.assertEqual(image.GetWidth(), image.Width)
        self.assertEqual(image.GetHeight(), image.Height)
        self.assertEqual(image.GetPaddingX(), image.PaddingX)
        self.assertEqual(image.GetImageSize(), image.ImageSize)
        self.assertEqual(image.GetOrientation(), image.Orientation)
        self.assertEqual(image.GetAllocatedBufferSize(), image.AllocatedBufferSize)

    def test_create_produces_valid_image_with_correct_properties(self):
        """PylonImage.Create() produces a valid image with the requested dimensions."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 320, 240)
        self.assertTrue(image.IsValid())
        self.assertEqual(image.PixelType, pylon.PixelType_Mono8)
        self.assertEqual(image.Width, 320)
        self.assertEqual(image.Height, 240)
        self.assertEqual(image.PaddingX, 0)
        self.assertEqual(image.ImageSize, 320 * 240)
        self.assertEqual(image.Orientation, pylon.ImageOrientation_TopDown)

    def test_create_with_padding_sets_padding_x(self):
        """PylonImage.Create() with paddingX creates an image with that padding."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48, 4)
        self.assertEqual(image.PaddingX, 4)
        self.assertEqual(image.ImageSize, (64 + 4) * 48)

    def test_create_with_bottom_up_orientation(self):
        """PylonImage.Create() honours the ImageOrientation_BottomUp parameter."""
        image = pylon.PylonImage.Create(
            pylon.PixelType_Mono8, 64, 48, 0, pylon.ImageOrientation_BottomUp
        )
        self.assertEqual(image.Orientation, pylon.ImageOrientation_BottomUp)

    def test_copy_construction_produces_shallow_copy_sharing_the_buffer(self):
        """Copy constructor creates a shallow copy: properties are identical and the buffer is shared."""
        import numpy as np
        source = pylon.PylonImage.Create(pylon.PixelType_Mono8, 32, 16)
        with source.GetArrayZeroCopy() as view:
            view[:] = 42

        copy = pylon.PylonImage(source)

        # Properties match the source.
        self.assertTrue(copy.IsValid())
        self.assertEqual(copy.PixelType, source.PixelType)
        self.assertEqual(copy.Width, source.Width)
        self.assertEqual(copy.Height, source.Height)
        self.assertEqual(copy.PaddingX, source.PaddingX)
        self.assertEqual(copy.ImageSize, source.ImageSize)
        self.assertEqual(copy.Orientation, source.Orientation)

        # Both objects read the same pixel values.
        self.assertTrue(np.all(copy.Array == 42))

        # The buffer is shared: writing through the copy is immediately visible in the source.
        with copy.GetArrayZeroCopy() as view:
            view[:] = 99
        self.assertTrue(np.all(source.Array == 99))

        # IsUnique() returns False while both handles are alive.
        self.assertFalse(source.IsUnique())
        self.assertFalse(copy.IsUnique())

        # Releasing the copy hands sole ownership back to the source.
        copy.Release()
        self.assertTrue(source.IsUnique())

    def test_copy_construction_from_invalid_image_produces_invalid_copy(self):
        """Copy-constructing from an invalid (default) PylonImage produces another invalid image."""
        source = pylon.PylonImage()
        self.assertFalse(source.IsValid())

        copy = pylon.PylonImage(source)

        self.assertFalse(copy.IsValid())
        self.assertEqual(copy.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(copy.Width, 0)
        self.assertEqual(copy.Height, 0)

    # ------------------------------------------------------------------
    # IsValid / Release
    # ------------------------------------------------------------------

    def test_release_invalidates_image(self):
        """Release() makes IsValid() return False."""
        image = _make_mono8_image()
        self.assertTrue(image.IsValid())
        image.Release()
        self.assertFalse(image.IsValid())

    def test_context_manager_calls_release_on_exit(self):
        """The with-statement context manager calls Release() on exit."""
        image = _make_mono8_image()
        with image:
            self.assertTrue(image.IsValid())
        self.assertFalse(image.IsValid())

    def test_context_manager_calls_release_on_exception(self):
        """The context manager calls Release() even when an exception is raised inside."""
        image = _make_mono8_image()
        try:
            with image:
                raise RuntimeError("simulated error")
        except RuntimeError:
            pass
        self.assertFalse(image.IsValid())

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def test_reset_changes_image_dimensions(self):
        """Reset() updates pixel type, width and height of an existing image."""
        image = _make_mono8_image(64, 48)
        image.Reset(pylon.PixelType_Mono16, 128, 96)
        self.assertEqual(image.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(image.Width, 128)
        self.assertEqual(image.Height, 96)

    def test_reset_with_padding_sets_padding_x(self):
        """Reset() with explicit paddingX configures the padding correctly."""
        image = _make_mono8_image()
        # Five arguments are required to reach the paddingX overload; with four
        # arguments SWIG dispatches to Reset(pixelType, width, height, orientation).
        image.Reset(pylon.PixelType_Mono8, 32, 32, 8, pylon.ImageOrientation_TopDown)
        self.assertEqual(image.PaddingX, 8)

    # ------------------------------------------------------------------
    # GetBuffer / Buffer / GetMemoryView
    # ------------------------------------------------------------------

    def test_get_buffer_on_default_image_returns_none_or_empty(self):
        """GetBuffer() on a default-constructed (invalid) image returns None."""
        image = pylon.PylonImage()
        buf = image.GetBuffer()
        self.assertIsNone(buf)

    def test_buffer_property_and_get_buffer_agree(self):
        """Buffer property and GetBuffer() return the same bytes for a loaded image."""
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        self.assertEqual(image.Buffer[0], _BARCODE_FIRST_PIXEL)
        self.assertEqual(image.GetBuffer()[0], _BARCODE_FIRST_PIXEL)
        image.Release()

    def test_get_memory_view_exposes_writable_buffer(self):
        """GetMemoryView() returns a writable memory view over the image buffer."""
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        memory_view = image.GetMemoryView()
        self.assertEqual(memory_view[0], _BARCODE_FIRST_PIXEL)
        # Verify it is writable by modifying its first byte.
        memory_view[0] = 0
        self.assertEqual(image.GetBuffer()[0], 0)
        image.Release()

    # ------------------------------------------------------------------
    # GetStride
    # ------------------------------------------------------------------

    def test_get_stride_returns_ok_and_row_size_in_bytes(self):
        """GetStride() returns (True, width_in_bytes) for a non-packed Mono8 image."""
        image = _make_mono8_image(64, 48)
        ok, stride = image.GetStride()
        self.assertTrue(ok)
        self.assertEqual(stride, 64)

    def test_get_stride_with_padding_includes_padding_bytes(self):
        """GetStride() includes paddingX in the reported stride."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono8, 64, 48, 8)
        ok, stride = image.GetStride()
        self.assertTrue(ok)
        self.assertEqual(stride, 64 + 8)

    # ------------------------------------------------------------------
    # IsUnique
    # ------------------------------------------------------------------

    def test_is_unique_true_for_standalone_image(self):
        """IsUnique() returns True when no other image shares the buffer."""
        image = _make_mono8_image()
        self.assertTrue(image.IsUnique())

    # ------------------------------------------------------------------
    # IsSupportedPixelType / IsAdditionalPaddingSupported
    # ------------------------------------------------------------------

    def test_is_supported_pixel_type_true_for_mono8(self):
        """IsSupportedPixelType() returns True for PixelType_Mono8."""
        image = pylon.PylonImage()
        self.assertTrue(image.IsSupportedPixelType(pylon.PixelType_Mono8))

    def test_is_additional_padding_supported_always_true(self):
        """IsAdditionalPaddingSupported() always returns True for CPylonImage."""
        image = pylon.PylonImage()
        self.assertTrue(image.IsAdditionalPaddingSupported())

    # ------------------------------------------------------------------
    # IsUserBufferAttached / IsGrabResultBufferAttached
    # ------------------------------------------------------------------

    def test_is_user_buffer_attached_false_for_created_image(self):
        """IsUserBufferAttached() returns False when the image owns its buffer."""
        image = _make_mono8_image()
        self.assertFalse(image.IsUserBufferAttached())

    def test_is_grab_result_buffer_attached_false_for_created_image(self):
        """IsGrabResultBufferAttached() returns False for a buffer-owning PylonImage."""
        image = _make_mono8_image()
        self.assertFalse(image.IsGrabResultBufferAttached())

    def test_is_user_buffer_attached_true_after_attach_memory_view(self):
        """IsUserBufferAttached() returns True after AttachMemoryView()."""
        buf = bytearray(64 * 48)
        image = pylon.PylonImage()
        image.AttachMemoryView(memoryview(buf), pylon.PixelType_Mono8, 64, 48, 0)
        self.assertTrue(image.IsUserBufferAttached())

    # ------------------------------------------------------------------
    # ChangePixelType
    # ------------------------------------------------------------------

    def test_change_pixel_type_between_compatible_types(self):
        """ChangePixelType() swaps between two types with the same bit depth."""
        image = pylon.PylonImage.Create(pylon.PixelType_Mono10, 64, 48)
        image.ChangePixelType(pylon.PixelType_Mono12)
        self.assertEqual(image.PixelType, pylon.PixelType_Mono12)

    # ------------------------------------------------------------------
    # GetPlane
    # ------------------------------------------------------------------

    def test_get_plane_zero_on_non_planar_image_returns_same_dimensions(self):
        """GetPlane(0) on a non-planar image returns an image with the same width/height."""
        image = _make_mono8_image(64, 48)
        plane = image.GetPlane(0)
        self.assertEqual(plane.Width, 64)
        self.assertEqual(plane.Height, 48)
        self.assertEqual(plane.PixelType, pylon.PixelType_Mono8)

    # ------------------------------------------------------------------
    # GetAoi
    # ------------------------------------------------------------------

    def test_get_aoi_returns_image_with_correct_dimensions(self):
        """GetAoi() returns an image view with the requested AOI dimensions."""
        image = _make_mono8_image(128, 96)
        aoi = image.GetAoi(10, 11, 65, 48)
        self.assertEqual(aoi.Width, 65)
        self.assertEqual(aoi.Height, 48)
        self.assertEqual(aoi.PaddingX, 63)

    def test_get_aoi_first_row_matches_source_first_row(self):
        """GetAoi() row 0 pixel values equal the corresponding region in the source row 0.

        Note: Only row 0 is checked because the AOI image has non-zero PaddingX equal to
        (source_width - aoi_width), so GetArray() without explicit stride handling only
        produces correct results for the very first row.
        """
        import numpy as np
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        aoi = image.GetAoi(0, 0, 100, 100)
        source_row0 = image.GetArray()[0, :100]
        aoi_row0 = aoi.GetArray()[0, :100]
        np.testing.assert_array_equal(aoi_row0, source_row0)
        image.Release()

    # ------------------------------------------------------------------
    # CopyImage
    # ------------------------------------------------------------------

    def test_copy_image_produces_independent_copy(self):
        """CopyImage() creates an independent copy; modifying the source does not affect the copy."""
        source = _make_mono8_image(64, 48)
        # Write a sentinel value into the source via its writable memory view.
        source.GetMemoryView()[0] = 0xAA

        destination = pylon.PylonImage()
        destination.CopyImage(source)

        self.assertEqual(destination.Width, source.Width)
        self.assertEqual(destination.Height, source.Height)
        self.assertEqual(destination.PixelType, source.PixelType)
        self.assertEqual(destination.GetBuffer()[0], 0xAA)

        # Overwrite the source; the copy must remain unchanged.
        source.GetMemoryView()[0] = 0x00
        self.assertEqual(destination.GetBuffer()[0], 0xAA)

    def test_copy_image_with_new_padding_adjusts_padding(self):
        """CopyImage() overload with newPaddingX produces the requested padding."""
        source = _make_mono8_image(64, 48)
        destination = pylon.PylonImage()
        destination.CopyImage(source, 4)
        self.assertEqual(destination.PaddingX, 4)
        self.assertEqual(destination.Width, 64)

    # ------------------------------------------------------------------
    # AttachGrabResultBuffer
    # ------------------------------------------------------------------

    def test_attach_grab_result_buffer_makes_grab_result_buffer_attached(self):
        """AttachGrabResultBuffer() sets IsGrabResultBufferAttached() to True."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing(1)
            grab_result = camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            )
            self.assertTrue(grab_result.GrabSucceeded())
            image = pylon.PylonImage()
            image.AttachGrabResultBuffer(grab_result)
            self.assertTrue(image.IsGrabResultBufferAttached())
            self.assertTrue(image.IsValid())
            self.assertEqual(image.PixelType, grab_result.PixelType)
            self.assertEqual(image.Width, grab_result.Width)
            self.assertEqual(image.Height, grab_result.Height)

        def test_attach_grab_result_buffer_component_makes_grab_result_buffer_attached(self):
            """AttachGrabResultBuffer(index, grab_result) sets IsGrabResultBufferAttached() to True."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.StartGrabbing(1)
            grab_result = camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException
            )
            self.assertTrue(grab_result.GrabSucceeded())
            image = pylon.PylonImage()
            image.AttachGrabResultBuffer(0, grab_result)
            self.assertTrue(image.IsGrabResultBufferAttached())
            self.assertTrue(image.IsValid())
            self.assertEqual(image.PixelType, grab_result.PixelType)
            self.assertEqual(image.Width, grab_result.Width)
            self.assertEqual(image.Height, grab_result.Height)

    # ------------------------------------------------------------------
    # AttachMemoryView / AttachArray
    # ------------------------------------------------------------------

    def test_attach_memory_view_sets_properties_and_user_buffer_flag(self):
        """AttachMemoryView() attaches an external buffer and sets the image properties."""
        buf = bytearray(320 * 240)
        image = pylon.PylonImage()
        image.AttachMemoryView(memoryview(buf), pylon.PixelType_Mono8, 320, 240, 0)
        self.assertTrue(image.IsValid())
        self.assertTrue(image.IsUserBufferAttached())
        self.assertEqual(image.Width, 320)
        self.assertEqual(image.Height, 240)
        self.assertEqual(image.PixelType, pylon.PixelType_Mono8)

    def test_attach_bytes_object_sets_properties_and_user_buffer_flag(self):
        """AttachBytesObject() attaches a bytes buffer and sets the image properties."""
        buf = bytes(320 * 240)
        image = pylon.PylonImage()
        image.AttachBytesObject(buf, pylon.PixelType_Mono8, 320, 240, 0)
        self.assertTrue(image.IsValid())
        self.assertTrue(image.IsUserBufferAttached())
        self.assertEqual(image.Width, 320)
        self.assertEqual(image.Height, 240)
        self.assertEqual(image.PixelType, pylon.PixelType_Mono8)

    def test_attach_bytes_object_content_is_readable(self):
        """AttachBytesObject() exposes the bytes content through GetBuffer()."""
        pixel_data = bytes([i % 256 for i in range(64 * 48)])
        image = pylon.PylonImage()
        image.AttachBytesObject(pixel_data, pylon.PixelType_Mono8, 64, 48, 0)
        self.assertEqual(image.GetBuffer()[0], pixel_data[0])
        self.assertEqual(image.GetBuffer()[64 * 48 - 1], pixel_data[64 * 48 - 1])

    def test_attach_bytes_object_rejects_non_bytes_argument(self):
        """AttachBytesObject() raises RuntimeError when passed a non-bytes object."""
        image = pylon.PylonImage()
        with self.assertRaises(RuntimeError):
            image.AttachBytesObject("not bytes", pylon.PixelType_Mono8, 4, 4, 0)

    def test_attach_array_holds_reference_and_shares_buffer(self):
        """AttachArray() increments ref-count of the array and shares the buffer."""
        import numpy as np
        import sys
        image = pylon.PylonImage()
        array = np.zeros((480, 640), dtype=np.uint8)
        array[0, 0] = 42

        ref_count_before = sys.getrefcount(array)
        image.AttachArray(array, pylon.PixelType_Mono8)
        self.assertEqual(sys.getrefcount(array), ref_count_before + 1)

        # Buffer is shared, not copied.
        self.assertEqual(image.Array[0, 0], 42)

        del image
        self.assertEqual(sys.getrefcount(array), ref_count_before)

    # ------------------------------------------------------------------
    # Load / Save / CanSaveWithoutConversion
    # ------------------------------------------------------------------

    def test_load_populates_image_properties(self):
        """Load() fills in the pixel type, dimensions and image data from a PNG file."""
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        self.assertTrue(image.IsValid())
        self.assertEqual(image.PixelType, _BARCODE_PIXEL_TYPE)
        self.assertEqual(image.Width, _BARCODE_WIDTH)
        self.assertEqual(image.Height, _BARCODE_HEIGHT)
        self.assertEqual(image.PaddingX, 0)
        self.assertEqual(image.ImageSize, _BARCODE_WIDTH * _BARCODE_HEIGHT)
        self.assertEqual(image.AllocatedBufferSize, _BARCODE_WIDTH * _BARCODE_HEIGHT)
        self.assertEqual(image.Orientation, pylon.ImageOrientation_TopDown)
        image.Release()

    def test_save_and_reload_round_trip(self):
        """Save() writes a PNG that Load() can read back with identical content."""
        import numpy as np
        source = pylon.PylonImage()
        source.Load(_BARCODE_PNG)

        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temporary_file:
            temporary_path = temporary_file.name
        try:
            source.Save(pylon.ImageFileFormat_Png, temporary_path)
            reloaded = pylon.PylonImage()
            reloaded.Load(temporary_path)
            self.assertEqual(reloaded.Width, source.Width)
            self.assertEqual(reloaded.Height, source.Height)
            np.testing.assert_array_equal(reloaded.Array, source.Array)
            reloaded.Release()
        finally:
            os.unlink(temporary_path)
        source.Release()

    def test_can_save_without_conversion_true_for_mono8_png(self):
        """CanSaveWithoutConversion() returns True for a Mono8 image saved as PNG."""
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        self.assertTrue(image.CanSaveWithoutConversion(pylon.ImageFileFormat_Png))
        image.Release()

    # ------------------------------------------------------------------
    # GetImageFormat
    # ------------------------------------------------------------------

    def test_get_image_format_on_default_image_raises_value_error(self):
        """GetImageFormat() on an invalid (default-constructed) image raises ValueError."""
        with self.assertRaises(ValueError):
            pylon.PylonImage().GetImageFormat()

    def test_image_format_property_on_default_image_raises_value_error(self):
        """ImageFormat property on an invalid image raises ValueError."""
        with self.assertRaises(ValueError):
            _ = pylon.PylonImage().ImageFormat

    def test_get_image_format_returns_correct_shape_and_dtype_for_mono8(self):
        """GetImageFormat() returns (height, width) shape and uint8 dtype for Mono8."""
        import numpy as np
        image = _make_mono8_image(64, 48)
        shape, dtype, fmt = image.GetImageFormat()
        self.assertEqual(shape, (48, 64))
        self.assertEqual(dtype, np.uint8)

    def test_get_image_format_accepts_explicit_pixel_type_override(self):
        """GetImageFormat(pt) uses the supplied pixel type instead of the image's own type."""
        import numpy as np
        image = _make_mono8_image()
        shape, dtype, fmt = image.GetImageFormat(pylon.PixelType_Mono16)
        self.assertEqual(dtype, np.uint16)

    def test_get_image_format_supports_all_mapped_pixel_types(self):
        """GetImageFormat(pt) returns the expected shape/dtype/format for every supported mapped pixel type."""
        import numpy as np

        width = 7
        height = 5
        image = _make_mono8_image(width, height)

        cases = (
            # Mono/Bayer/Confidence/Coord3D-C, 8-bit
            (pylon.PixelType_Mono8, (height, width), np.uint8, "B"),
            (pylon.PixelType_BayerGR8, (height, width), np.uint8, "B"),
            (pylon.PixelType_BayerRG8, (height, width), np.uint8, "B"),
            (pylon.PixelType_BayerGB8, (height, width), np.uint8, "B"),
            (pylon.PixelType_BayerBG8, (height, width), np.uint8, "B"),
            (pylon.PixelType_Confidence8, (height, width), np.uint8, "B"),
            (pylon.PixelType_Coord3D_C8, (height, width), np.uint8, "B"),
            # Mono/Bayer, 10-bit
            (pylon.PixelType_Mono10, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGR10, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerRG10, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGB10, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerBG10, (height, width), np.uint16, "H"),
            # Mono/Bayer, 12-bit
            (pylon.PixelType_Mono12, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGR12, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerRG12, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGB12, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerBG12, (height, width), np.uint16, "H"),
            # Mono/Bayer/Confidence/Coord3D-C, 16-bit
            (pylon.PixelType_Mono16, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGR16, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerRG16, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerGB16, (height, width), np.uint16, "H"),
            (pylon.PixelType_BayerBG16, (height, width), np.uint16, "H"),
            (pylon.PixelType_Confidence16, (height, width), np.uint16, "H"),
            (pylon.PixelType_Coord3D_C16, (height, width), np.uint16, "H"),
            # RGB/BGR
            (pylon.PixelType_RGB8packed, (height, width, 3), np.uint8, "B"),
            (pylon.PixelType_BGR8packed, (height, width, 3), np.uint8, "B"),
            (pylon.PixelType_RGB12packed, (height, width, 3), np.uint16, "H"),
            (pylon.PixelType_BGR12packed, (height, width, 3), np.uint16, "H"),
            (pylon.PixelType_RGB10packed, (height, width, 3), np.uint16, "H"),
            (pylon.PixelType_BGR10packed, (height, width, 3), np.uint16, "H"),
            # YUV 4:2:2
            (pylon.PixelType_YUV422_YUYV_Packed, (height, width, 2), np.uint8, "B"),
            (pylon.PixelType_YUV422packed, (height, width, 2), np.uint8, "B"),
            # 32-bit float formats
            (pylon.PixelType_Coord3D_ABC32f, (height, width, 3), np.float32, "f"),
            (pylon.PixelType_Data32f, (height, width, 1), np.float32, "f"),
            # BiColor
            (pylon.PixelType_BiColorRGBG8, (height, width * 2), np.uint8, "B"),
            (pylon.PixelType_BiColorBGRG8, (height, width * 2), np.uint8, "B"),
            (pylon.PixelType_BiColorRGBG10, (height, width * 2), np.uint16, "H"),
            (pylon.PixelType_BiColorBGRG10, (height, width * 2), np.uint16, "H"),
            (pylon.PixelType_BiColorRGBG12, (height, width * 2), np.uint16, "H"),
            (pylon.PixelType_BiColorBGRG12, (height, width * 2), np.uint16, "H"),
        )

        for pixel_type, expected_shape, expected_dtype, expected_fmt in cases:
            with self.subTest(pixel_type=pixel_type):
                shape, dtype, fmt = image.GetImageFormat(pixel_type)
                self.assertEqual(shape, expected_shape)
                self.assertEqual(dtype, expected_dtype)
                self.assertEqual(fmt, expected_fmt)

    def test_get_image_format_raises_value_error_for_unsupported_pixel_type_override(self):
        """GetImageFormat(pt) raises ValueError for an unsupported pixel type."""
        image = _make_mono8_image()
        with self.assertRaises(ValueError):
            image.GetImageFormat(pylon.PixelType_Undefined)

    def test_get_image_format_raises_value_error_for_packed_pixel_type_override(self):
        """GetImageFormat(pt) raises ValueError when the supplied pixel type is packed."""
        image = _make_mono8_image()
        for packed_pixel_type in (pylon.PixelType_Mono12packed, pylon.PixelType_Mono12p):
            with self.subTest(pixel_type=packed_pixel_type):
                with self.assertRaises(ValueError):
                    image.GetImageFormat(packed_pixel_type)

    # ------------------------------------------------------------------
    # GetArray
    # ------------------------------------------------------------------

    def test_array_property_on_default_image_raises_value_error(self):
        """Array property on an invalid image raises ValueError."""
        with self.assertRaises(ValueError):
            _ = pylon.PylonImage().Array

    def test_get_array_returns_correct_shape_and_content(self):
        """GetArray() returns an ndarray shaped (height, width) with correct pixel values."""
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        array = image.GetArray()
        self.assertEqual(array.shape, (_BARCODE_HEIGHT, _BARCODE_WIDTH))
        self.assertEqual(array[0, 0], _BARCODE_FIRST_PIXEL)
        image.Release()

    def test_array_property_and_get_array_agree(self):
        """Array property and GetArray() return arrays with identical content."""
        import numpy as np
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        np.testing.assert_array_equal(image.Array, image.GetArray())
        image.Release()

    def test_get_array_raw_returns_uint8_flat_byte_array(self):
        """GetArray(raw=True) returns the raw image bytes as a flat uint8 array."""
        import numpy as np
        image = _make_mono8_image(64, 48)
        raw = image.GetArray(raw=True)
        self.assertEqual(raw.dtype, np.uint8)
        self.assertEqual(raw.size, 64 * 48)

    # ------------------------------------------------------------------
    # GetArrayZeroCopy
    # ------------------------------------------------------------------

    def test_get_array_zero_copy_shares_underlying_buffer(self):
        """GetArrayZeroCopy() yields an array that is a zero-copy view of the buffer."""
        import numpy as np
        image = pylon.PylonImage()
        image.Load(_BARCODE_PNG)
        with image.GetArrayZeroCopy() as zero_copy_array:
            self.assertEqual(zero_copy_array[0, 0], _BARCODE_FIRST_PIXEL)
            # Writing to the zero-copy array modifies the image buffer in-place.
            zero_copy_array[0, 0] = 0
        self.assertEqual(image.GetBuffer()[0], 0)
        image.Release()

    def test_get_array_zero_copy_raw_returns_uint8_view(self):
        """GetArrayZeroCopy(raw=True) yields a flat uint8 view of the image buffer."""
        import numpy as np
        image = _make_mono8_image(64, 48)
        with image.GetArrayZeroCopy(raw=True) as zero_copy_array:
            self.assertEqual(zero_copy_array.dtype, np.uint8)
            self.assertEqual(zero_copy_array.size, 64 * 48)

    # ------------------------------------------------------------------
    # Packed pixel format (Mono12p sawtooth) — ImageFormatConverter._Unpack
    # path exercised through GetArray / GetArrayZeroCopy
    # ------------------------------------------------------------------

    #: Dimensions for the synthetic Mono12p test image.
    #: Width must be even so each row packs into whole 3-byte groups.
    _PACKED_WIDTH  = 4
    _PACKED_HEIGHT = 2
    #: Value step for the sawtooth pattern; all values must fit in 12 bits.
    _PACKED_STEP   = 256

    @staticmethod
    def _pack_mono12p(pixel_values):
        """Pack a flat sequence of 12-bit integer values into a Mono12p byte buffer.

        Mono12p layout for each pair (p0, p1):
          byte 0 : p0[7:0]
          byte 1 : p0[11:8]  (lower nibble)  |  p1[3:0]  (upper nibble)
          byte 2 : p1[11:4]
        """
        packed = bytearray()
        for i in range(0, len(pixel_values), 2):
            p0 = int(pixel_values[i])     & 0xFFF
            p1 = int(pixel_values[i + 1]) & 0xFFF
            packed.append(p0 & 0xFF)
            packed.append(((p0 >> 8) & 0x0F) | ((p1 & 0x0F) << 4))
            packed.append((p1 >> 4) & 0xFF)
        return bytes(packed)

    def _make_mono12p_sawtooth_image(self):
        """Return (PylonImage, pixel_values_flat) for a synthetic Mono12p sawtooth test image.

        Pixel values increment by _PACKED_STEP and wrap at 4096 (12-bit range).
        Every value is distinct for the chosen image size.
        """
        num_pixels = self._PACKED_WIDTH * self._PACKED_HEIGHT
        pixel_values = [(i * self._PACKED_STEP) % 4096 for i in range(num_pixels)]
        packed = self._pack_mono12p(pixel_values)
        image = pylon.PylonImage()
        image.AttachMemoryView(
            memoryview(packed),
            pylon.PixelType_Mono12p,
            self._PACKED_WIDTH,
            self._PACKED_HEIGHT,
            0,
        )
        return image, pixel_values

    def test_packed_get_image_format_raises_value_error(self):
        """GetImageFormat() raises ValueError for a packed pixel type (Mono12p)."""
        image, _ = self._make_mono12p_sawtooth_image()
        with self.assertRaises(ValueError):
            image.GetImageFormat()

    def test_packed_get_array_returns_uint16_shaped_height_by_width(self):
        """GetArray() on a Mono12p image returns a uint16 ndarray shaped (height, width)."""
        import numpy as np
        image, _ = self._make_mono12p_sawtooth_image()
        result = image.GetArray()
        self.assertEqual(result.dtype, np.uint16)
        self.assertEqual(result.shape, (self._PACKED_HEIGHT, self._PACKED_WIDTH))

    def test_packed_get_array_decodes_sawtooth_pixel_values_correctly(self):
        """GetArray() on a Mono12p image decodes every pixel to its expected 12-bit value (LsbAligned)."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        result = image.GetArray()
        expected = np.array(pixel_values, dtype=np.uint16).reshape(
            self._PACKED_HEIGHT, self._PACKED_WIDTH
        )
        np.testing.assert_array_equal(result, expected)

    def test_packed_get_array_raw_returns_uint8_packed_buffer(self):
        """GetArray(raw=True) on a Mono12p image returns the raw packed bytes as a uint8 array."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        raw = image.GetArray(raw=True)
        self.assertEqual(raw.dtype, np.uint8)
        expected_size = self._PACKED_WIDTH * self._PACKED_HEIGHT * 3 // 2
        self.assertEqual(len(raw), expected_size)
        expected_bytes = np.frombuffer(self._pack_mono12p(pixel_values), dtype=np.uint8)
        np.testing.assert_array_equal(raw, expected_bytes)

    def test_packed_get_array_zero_copy_decodes_sawtooth_pixel_values_correctly(self):
        """GetArrayZeroCopy() on a Mono12p image unpacks via CPylonImage fallback and returns correct uint16 values."""
        import numpy as np
        image, pixel_values = self._make_mono12p_sawtooth_image()
        expected = np.array(pixel_values, dtype=np.uint16).reshape(
            self._PACKED_HEIGHT, self._PACKED_WIDTH
        )
        with image.GetArrayZeroCopy() as result:
            self.assertEqual(result.dtype, np.uint16)
            self.assertEqual(result.shape, (self._PACKED_HEIGHT, self._PACKED_WIDTH))
            np.testing.assert_array_equal(result, expected)



if __name__ == "__main__":
    unittest.main()
