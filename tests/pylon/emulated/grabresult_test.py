"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/GrabResultData.i and src/pylon/GrabResultPtr.i, covering every
public method and property of GrabResult (CGrabResultPtr) and the
GrabResultData (CGrabResultData) interface accessible through it.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import unittest


SIZE_MAX = 18446744073709551615

class GrabResultTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Enums
    # ------------------------------------------------------------------

    def test_enum_presence(self):
        """Test that all enum value ported from C++ are present."""
        self.assertEqual(pylon.PayloadType_Undefined, -1)
        self.assertEqual(pylon.PayloadType_Image, 0)
        self.assertEqual(pylon.PayloadType_RawData, 1)
        self.assertEqual(pylon.PayloadType_File, 2)
        self.assertEqual(pylon.PayloadType_ChunkData, 3)
        self.assertEqual(pylon.PayloadType_GenDC, 4)
        self.assertEqual(pylon.PayloadType_DeviceSpecific, 0x8000)

    # ------------------------------------------------------------------
    # GrabResult construction / validity / smart pointer (GrabResultPtr.h)
    # ------------------------------------------------------------------

    def test_default_construction_is_invalid(self):
        """Default-constructed GrabResult is invalid, not unique, and raises on data access."""
        grab_result = pylon.GrabResult()
        self.assertFalse(grab_result.IsValid())
        self.assertFalse(grab_result.IsUnique())
        self.assertFalse(bool(grab_result))
        self.assertRaises(genicam.RuntimeException, grab_result.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grab_result.GetImageBuffer)
        self.assertRaises(genicam.RuntimeException, grab_result.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grab_result.GetArray)
        self.assertRaises(genicam.RuntimeException, grab_result.GetMemoryView)
        self.assertRaises(genicam.RuntimeException, grab_result.GetImageMemoryView)
        grab_result.Release()

    def test_grab_result_is_valid_and_unique_after_grab(self):
        """A GrabResult from GrabOne is valid and the sole holder of the buffer."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)
        self.assertTrue(grab_result.IsValid())
        self.assertTrue(grab_result.IsUnique())
        self.assertTrue(bool(grab_result))
        grab_result.Release()

    def test_copy_construction_shares_buffer_reference(self):
        """Copying a GrabResult shares the buffer; IsUnique reflects the reference count."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            original = camera.GrabOne(1000)

        copy = pylon.GrabResult(original)

        # Both references are valid; neither is unique
        self.assertTrue(original.IsValid())
        self.assertTrue(copy.IsValid())
        self.assertFalse(original.IsUnique())
        self.assertFalse(copy.IsUnique())

        # Releasing original leaves copy as the sole reference
        original.Release()
        self.assertFalse(original.IsValid())
        self.assertTrue(copy.IsValid())
        self.assertTrue(copy.IsUnique())

        # Releasing copy fully invalidates the result
        copy.Release()
        self.assertFalse(copy.IsValid())

    def test_release_invalidates_and_raises_on_subsequent_access(self):
        """Release invalidates the GrabResult; buffer and image access raise RuntimeException afterwards."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)

        grab_result.Release()
        self.assertFalse(grab_result.IsValid())
        self.assertFalse(grab_result.IsUnique())
        self.assertFalse(bool(grab_result))
        self.assertRaises(genicam.RuntimeException, grab_result.GetBuffer)
        self.assertRaises(genicam.RuntimeException, grab_result.GetImageFormat)
        self.assertRaises(genicam.RuntimeException, grab_result.GetArray)

    # ------------------------------------------------------------------
    # Context manager (__enter__ / __exit__)
    # ------------------------------------------------------------------

    def test_context_manager_entry_returns_self(self):
        """__enter__ returns the GrabResult itself so it can be used directly in a with-block."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)

        with grab_result as result_in_context:
            self.assertIs(result_in_context, grab_result)
            self.assertTrue(grab_result.IsValid())

    def test_context_manager_exit_releases_grab_result(self):
        """__exit__ releases the GrabResult; it is invalid after leaving the with-block."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)

        with grab_result:
            self.assertTrue(grab_result.IsValid())
        self.assertFalse(grab_result.IsValid())

    # ------------------------------------------------------------------
    # Grab success and error state (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_grab_succeeded_true_for_emulated_grab(self):
        """GrabSucceeded returns True for a successful emulated image grab."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)
        self.assertTrue(grab_result.GrabSucceeded())
        grab_result.Release()

    def test_error_code_and_description_are_zero_on_success(self):
        """ErrorCode is 0 and ErrorDescription is empty when the grab succeeded."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)
            camera.ForceFailedBufferCount.Value = 1
            camera.ForceFailedBuffer.Execute()
            grab_result_with_error = camera.GrabOne(1000)

        # Method access
        self.assertTrue(grab_result.GrabSucceeded())
        self.assertEqual(grab_result.GetErrorCode(), 0)
        self.assertEqual(grab_result.GetErrorDescription(), "")
        # Property access (preferred style)
        self.assertEqual(grab_result.ErrorCode, 0)
        self.assertEqual(grab_result.ErrorDescription, "")
        grab_result.Release()

        # Test the result with error
        self.assertFalse(grab_result_with_error.GrabSucceeded())
        self.assertEqual(grab_result_with_error.ErrorCode, 0) # not set when using ForceFailedBuffer, but other than 0 in all error cases
        self.assertEqual(grab_result_with_error.ErrorDescription, "The buffer was incompletely grabbed.")
        grab_result_with_error.Release()

    # ------------------------------------------------------------------
    # Image dimensions: Width, Height, OffsetX, OffsetY (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_image_dimensions_match_camera_roi_settings(self):
        """Width and Height reflect the camera ROI settings at the time of grab."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.OffsetX.Value = 1
            camera.OffsetY.Value = 2
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetWidth(), 64)
        self.assertEqual(grab_result.GetHeight(), 48)
        self.assertEqual(grab_result.GetOffsetX(), 1)
        self.assertEqual(grab_result.GetOffsetY(), 2)
        # Property access (preferred style)
        self.assertEqual(grab_result.Width, 64)
        self.assertEqual(grab_result.Height, 48)
        self.assertEqual(grab_result.OffsetX, 1)
        self.assertEqual(grab_result.OffsetY, 2)
        grab_result.Release()

    def test_padding_is_zero_for_standard_emulated_image(self):
        """PaddingX and PaddingY are zero for a standard unpadded emulated image."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetPaddingX(), 0)
        self.assertEqual(grab_result.GetPaddingY(), 0)
        # Property access (preferred style)
        self.assertEqual(grab_result.PaddingX, 0)
        self.assertEqual(grab_result.PaddingY, 0)
        grab_result.Release()

    def test_get_stride_returns_valid_stride_for_mono8(self):
        """GetStride returns (True, width) for a Mono8 image with no padding."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        success, stride = grab_result.GetStride()
        self.assertTrue(success)
        self.assertEqual(stride, 64)  # Mono8: 1 byte per pixel, no padding
        grab_result.Release()

    # ------------------------------------------------------------------
    # Pixel type and payload type (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_pixel_type_matches_mono8_camera_format(self):
        """PixelType is PixelType_Mono8 when the camera is configured for Mono8."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetPixelType(), pylon.PixelType_Mono8)
        # Property access (preferred style)
        self.assertEqual(grab_result.PixelType, pylon.PixelType_Mono8)
        grab_result.Release()

    def test_pixel_type_matches_mono16_camera_format(self):
        """PixelType is PixelType_Mono16 when the camera is configured for Mono16."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono16"
            grab_result = camera.GrabOne(1000)
        self.assertEqual(grab_result.PixelType, pylon.PixelType_Mono16)
        grab_result.Release()

    def test_payload_type_is_image_for_standard_grab(self):
        """PayloadType is PayloadType_Image for a standard image grab."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetPayloadType(), pylon.PayloadType_Image)
        # Property access (preferred style)
        self.assertEqual(grab_result.PayloadType, pylon.PayloadType_Image)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Payload size, buffer size and image size (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_payload_and_image_size_equal_width_times_height_for_mono8(self):
        """PayloadSize and ImageSize both equal width * height bytes for Mono8."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        expected_size = 64 * 48
        # Method access
        self.assertEqual(grab_result.GetPayloadSize(), expected_size)
        self.assertEqual(grab_result.GetImageSize(), expected_size)
        self.assertGreaterEqual(grab_result.GetBufferSize(), expected_size)
        # Property access (preferred style)
        self.assertEqual(grab_result.PayloadSize, expected_size)
        self.assertEqual(grab_result.ImageSize, expected_size)
        self.assertGreaterEqual(grab_result.BufferSize, expected_size)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Identifiers: BlockID, TimeStamp, ID, ImageNumber,
    #              NumberOfSkippedImages (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_block_id_increases_across_consecutive_grabs(self):
        """BlockID increases with each grabbed frame."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            first = camera.GrabOne(1000)
            second = camera.GrabOne(1000)

        # Method access
        self.assertGreaterEqual(second.GetBlockID(), first.GetBlockID())
        # Property access (preferred style)
        self.assertGreaterEqual(second.BlockID, first.BlockID)
        # CamEmu reports "invalid value", currently
        self.assertEqual(second.BlockID, SIZE_MAX)
        first.Release()
        second.Release()

    def test_timestamp_increases_monotonically_across_grabs(self):
        """TimeStamp is non-decreasing across consecutive grabs."""
        with pylon.InstantCamera(pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            first = camera.GrabOne(1000)
            second = camera.GrabOne(1000)
            if camera.DeviceInfo.DeviceClass == pylon.BaslerCamEmuDeviceClass:
                # CamEmu reports 0 timestamp for all frames, currently
                self.assertEqual(second.TimeStamp, 0)

        # Method access
        self.assertLessEqual(first.GetTimeStamp(), second.GetTimeStamp())
        # Property access (preferred style)
        self.assertLessEqual(first.TimeStamp, second.TimeStamp)
        first.Release()
        second.Release()

    def test_id_is_positive_and_increases_across_grabs(self):
        """ID is always greater than 0 and increases with each retrieved result."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            with camera.GrabOne(1000) as result:
                pass # ID 1
            first = camera.GrabOne(1000)
            second = camera.GrabOne(1000)
        # Method access
        self.assertEqual(first.GetID(), 2)
        self.assertEqual(second.GetID(), 3)
        # Property access (preferred style)
        self.assertEqual(first.ID, 2)
        self.assertEqual(second.ID, 3)
        first.Release()
        second.Release()

    def test_image_number_is_positive_and_increases_across_grabs(self):
        """ImageNumber is always greater than 0 and increments with each RetrieveResult call."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.StartGrabbingMax(2)
            first = camera.RetrieveResult(1000)
            second = camera.RetrieveResult(1000)
        # Method access
        self.assertEqual(first.GetImageNumber(), 1)
        self.assertEqual(second.GetImageNumber(), 2)
        # Property access (preferred style)
        self.assertEqual(first.ImageNumber, 1)
        self.assertEqual(second.ImageNumber, 2)
        first.Release()
        second.Release()

    def test_number_of_skipped_images_is_zero_for_one_by_one_strategy(self):
        """NumberOfSkippedImages is 0 with the default OneByOne grab strategy."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetNumberOfSkippedImages(), 0)
        # Property access (preferred style)
        self.assertEqual(grab_result.NumberOfSkippedImages, 0)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Context values: CameraContext, BufferContext (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_camera_context_is_zero_by_default(self):
        """CameraContext is 0 when no custom context has been assigned to the camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetCameraContext(), 0)
        # Property access (preferred style)
        self.assertEqual(grab_result.CameraContext, 0)
        grab_result.Release()

    def test_buffer_context_is_an_integer(self):
        """GetBufferContext returns an integer context value associated with the buffer."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertIsInstance(grab_result.GetBufferContext(), int)
        # Property access (preferred style)
        self.assertIsInstance(grab_result.BufferContext, int)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Raw buffer access: GetBuffer, GetImageBuffer (GrabResultData.i)
    # ------------------------------------------------------------------

    def test_get_buffer_returns_bytearray_of_payload_size(self):
        """GetBuffer returns a bytearray whose length equals PayloadSize."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        buffer = grab_result.GetBuffer()
        self.assertIsInstance(buffer, bytearray)
        self.assertEqual(len(buffer), grab_result.PayloadSize)
        # Buffer property is equivalent
        self.assertEqual(grab_result.Buffer, buffer)
        grab_result.Release()

    def test_get_image_buffer_returns_bytearray_of_image_size(self):
        """GetImageBuffer returns a bytearray whose length equals ImageSize."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        image_buffer = grab_result.GetImageBuffer()
        self.assertIsInstance(image_buffer, bytearray)
        self.assertEqual(len(image_buffer), grab_result.ImageSize)
        grab_result.Release()

    def test_get_memory_view_returns_writable_view_of_payload(self):
        """GetMemoryView returns a writable memoryview spanning the full payload."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        memory_view = grab_result.GetMemoryView()
        self.assertIsInstance(memory_view, memoryview)
        self.assertEqual(len(memory_view), grab_result.PayloadSize)
        self.assertFalse(memory_view.readonly)
        memory_view.release()
        grab_result.Release()

    def test_get_image_memory_view_returns_writable_view_of_image(self):
        """GetImageMemoryView returns a writable memoryview spanning the image data only."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        image_memory_view = grab_result.GetImageMemoryView()
        self.assertIsInstance(image_memory_view, memoryview)
        self.assertEqual(len(image_memory_view), grab_result.ImageSize)
        self.assertFalse(image_memory_view.readonly)
        image_memory_view.release()
        grab_result.Release()

    # ------------------------------------------------------------------
    # NumPy image format: GetImageFormat (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_get_image_format_mono8_returns_2d_uint8_shape(self):
        """GetImageFormat for Mono8 returns ((height, width), uint8, 'B')."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        (height, width), dtype, format_char = grab_result.GetImageFormat()
        self.assertEqual(height, 48)
        self.assertEqual(width, 64)
        self.assertEqual(format_char, "B")
        self.assertEqual(dtype, numpy.uint8)
        grab_result.Release()

    def test_get_image_format_mono16_returns_2d_uint16_shape(self):
        """GetImageFormat for Mono16 returns ((height, width), uint16, 'H')."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono16"
            grab_result = camera.GrabOne(1000)
        (height, width), dtype, format_char = grab_result.GetImageFormat()
        self.assertEqual(height, 48)
        self.assertEqual(width, 64)
        self.assertEqual(format_char, "H")
        self.assertEqual(dtype, numpy.uint16)
        grab_result.Release()

    def test_get_image_format_with_explicit_pixel_type_override(self):
        """GetImageFormat(pt) uses the supplied pixel type instead of the result's pixel type."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        # Override the pixel type interpretation to Mono16
        (height, width), dtype, format_char = grab_result.GetImageFormat(pylon.PixelType_Mono16)
        self.assertEqual(format_char, "H")
        grab_result.Release()

    def test_get_image_format_raises_for_packed_pixel_format(self):
        """GetImageFormat raises ValueError when the pixel type is a packed format."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        self.assertRaises(ValueError, grab_result.GetImageFormat, pylon.PixelType_Mono12packed)
        grab_result.Release()

    # ------------------------------------------------------------------
    # NumPy array access: GetArray, Array property (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_get_array_returns_correct_shape_and_dtype_for_mono8(self):
        """GetArray returns a 2-D uint8 ndarray with shape (height, width) for Mono8."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64))
        self.assertEqual(array.dtype, numpy.uint8)
        grab_result.Release()

    def test_get_array_returns_correct_shape_and_dtype_for_mono16(self):
        """GetArray returns a 2-D uint16 ndarray with shape (height, width) for Mono16."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono16"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64))
        self.assertEqual(array.dtype, numpy.uint16)
        grab_result.Release()

    def test_array_property_matches_get_array_result(self):
        """The Array property returns the same data as GetArray()."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        numpy.testing.assert_array_equal(grab_result.Array, grab_result.GetArray())
        grab_result.Release()

    def test_get_array_raw_wraps_full_payload_as_1d_uint8(self):
        """GetArray(raw=True) returns a 1-D uint8 array spanning the entire payload."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        raw_array = grab_result.GetArray(raw=True)
        self.assertEqual(raw_array.size, grab_result.PayloadSize)
        self.assertEqual(raw_array.dtype, numpy.uint8)
        grab_result.Release()

    def test_emulated_image_contains_column_ramp_pattern(self):
        """The emulated camera produces a column ramp: pixel values increase by 1 across each row."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 1024
            camera.Height.Value = 1040
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        row = list(grab_result.Array[0, 0:20])
        expected = [row[0] + i for i in range(20)]
        self.assertEqual(row, expected)
        grab_result.Release()

    # ------------------------------------------------------------------
    # NumPy zero-copy access: GetArrayZeroCopy (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_get_array_zero_copy_yields_correct_shape(self):
        """GetArrayZeroCopy yields a numpy array with the correct (height, width) shape."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        with grab_result.GetArrayZeroCopy() as zero_copy_array:
            self.assertEqual(zero_copy_array.shape[0], 48)
            self.assertEqual(zero_copy_array.shape[1], 64)
        grab_result.Release()

    def test_get_array_zero_copy_raises_when_external_reference_is_held(self):
        """GetArrayZeroCopy raises RuntimeError when an external reference escapes the context."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        with self.assertRaises(RuntimeError) as context_manager:
            with grab_result.GetArrayZeroCopy() as zero_copy_array:
                external_reference = zero_copy_array  # noqa: F841 – intentional ref hold
        self.assertEqual(
            str(context_manager.exception),
            "Please remove any references to the array before leaving context manager scope!!!",
        )
        grab_result.Release()

    # ------------------------------------------------------------------
    # Data container and components (GrabResultData.h / GrabResultData.i)
    # ------------------------------------------------------------------

    def test_data_component_count_is_one_for_standard_image(self):
        """DataComponentCount is 1 for a standard single-image grab result."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        # Method access
        self.assertEqual(grab_result.GetDataComponentCount(), 1)
        # Property access (preferred style)
        self.assertEqual(grab_result.DataComponentCount, 1)
        grab_result.Release()

    def test_get_data_container_has_one_component(self):
        """GetDataContainer and the DataContainer property both return a container with one component."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)

        container_via_method = grab_result.GetDataContainer()
        self.assertEqual(container_via_method.DataComponentCount, 1)
        container_via_method.Release()

        container_via_property = grab_result.DataContainer
        self.assertEqual(container_via_property.DataComponentCount, 1)
        container_via_property.Release()

        grab_result.Release()

    def test_get_data_component_by_index_returns_component_matching_image(self):
        """GetDataComponentByIndex(0) returns a component with the correct image dimensions."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        component = grab_result.GetDataComponentByIndex(0)
        self.assertEqual(component.Width, 64)
        self.assertEqual(component.Height, 48)
        component.Release()
        grab_result.Release()

    def test_get_data_component_by_type_returns_list_when_available(self):
        """GetDataComponentByType returns a component list when the pylon version supports it."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        if hasattr(grab_result, "GetDataComponentByType"):
            component_list = grab_result.GetDataComponentByType(
                pylon.ComponentType_Intensity
            )
            self.assertIsNotNone(component_list)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Chunk data: IsChunkDataAvailable, ChunkDataNodeMap, HasCRC, CheckCRC,
    #             GetChunkNode, __getattr__, __setattr__, __dir__
    #             (GrabResultData.h / GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_chunk_data_not_available_without_chunk_mode(self):
        """IsChunkDataAvailable returns False when chunk mode is not enabled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        self.assertFalse(grab_result.IsChunkDataAvailable())
        grab_result.Release()

    def test_chunk_data_node_map_accessible_via_method_and_property(self):
        """GetChunkDataNodeMap and the ChunkDataNodeMap property both return a node map object."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        self.assertIsInstance(grab_result.GetChunkDataNodeMap(), pylon.NodeMapWrapper)
        self.assertIsInstance(grab_result.ChunkDataNodeMap, pylon.NodeMapWrapper)
        grab_result.Release()

    def test_has_crc_is_false_without_crc_chunk(self):
        """HasCRC returns False when no CRC chunk is present in the result."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        self.assertFalse(grab_result.HasCRC())
        grab_result.Release()

    def test_chunk_node_access_when_chunk_mode_enabled(self):
        """When chunk mode is on, IsChunkDataAvailable is True and chunk nodes are accessible."""
        with pylon.InstantCamera(pylon.FirstFound) as camera: # NOT using the camemu explicitly here
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            if not camera.ChunkSelector.IsWritable():
                self.skipTest("Chunk mode not supported by this emulated device")
            camera.ChunkModeActive.Value = True
            if camera.ChunkSelector.TrySetValue("Timestamp"):
                camera.ChunkEnable.SetValue(True)
            if camera.ChunkSelector.TrySetValue("PayloadCRC16"):
                camera.ChunkEnable.SetValue(True)
            grab_result = camera.GrabOne(1000)

        self.assertTrue(grab_result.IsChunkDataAvailable())
        chunk_node = grab_result.GetChunkNode("ChunkTimestamp")  # not recommended
        self.assertEqual(chunk_node.Value, grab_result.ChunkTimestamp.Value)
        # CheckCRC is valid when HasCRC reports True
        if grab_result.HasCRC():
            self.assertEqual(grab_result.CheckCRC(), True)
        grab_result.Release()

    def test_getattr_raises_for_unknown_attribute_without_chunks(self):
        """__getattr__ raises AttributeError when the attribute is not a method, property, or chunk node."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        with self.assertRaises(AttributeError):
            _ = grab_result.this_attribute_does_not_exist
        grab_result.Release()

    def test_setattr_raises_for_unknown_attribute_without_chunks(self):
        """__setattr__ raises AttributeError when assigning an unknown attribute without chunk data."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        with self.assertRaises(AttributeError):
            grab_result.this_attribute_does_not_exist = 42
        grab_result.Release()

    # ------------------------------------------------------------------
    # GetFirstImageDataComponent (GrabResultData.h / pylon 2605+)
    # ------------------------------------------------------------------

    def test_get_first_image_data_component_returns_valid_intensity_component(self):
        """GetFirstImageDataComponent() returns a valid Intensity component for a standard image grab."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        component = grab_result.GetFirstImageDataComponent()
        self.assertTrue(component.IsValid())
        self.assertEqual(component.ComponentType, pylon.ComponentType_Intensity)
        self.assertEqual(component.Width, 64)
        self.assertEqual(component.Height, 48)
        component.Release()
        grab_result.Release()

    def test_get_first_image_data_component_throw_true_succeeds_when_found(self):
        """GetFirstImageDataComponent(True) succeeds without raising when an image component exists."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        component = grab_result.GetFirstImageDataComponent(True)
        self.assertTrue(component.IsValid())
        self.assertEqual(component.ComponentType, pylon.ComponentType_Intensity)
        component.Release()
        grab_result.Release()

    def test_get_first_image_data_component_throw_false_returns_invalid_when_no_result(self):
        """GetFirstImageDataComponent(False) returns an invalid component when the grab result has no image data."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            camera.ForceFailedBufferCount.Value = 1
            camera.ForceFailedBuffer.Execute()
            grab_result = camera.GrabOne(1000)
        self.assertFalse(grab_result.GrabSucceeded())
        component = grab_result.GetFirstImageDataComponent(False)
        self.assertFalse(component.IsValid())
        component.Release()
        grab_result.Release()

    def test_get_first_image_data_component_matches_grab_result_image_dimensions(self):
        """The component returned by GetFirstImageDataComponent() has the same dimensions as the grab result."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 128
            camera.Height.Value = 96
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        component = grab_result.GetFirstImageDataComponent()
        self.assertEqual(component.Width, grab_result.Width)
        self.assertEqual(component.Height, grab_result.Height)
        self.assertEqual(component.PixelType, grab_result.PixelType)
        self.assertEqual(component.OffsetX, grab_result.OffsetX)
        self.assertEqual(component.OffsetY, grab_result.OffsetY)
        component.Release()
        grab_result.Release()

    # ------------------------------------------------------------------
    # Payload size and image size: Mono16 (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_payload_size_is_two_bytes_per_pixel_for_mono16(self):
        """PayloadSize and ImageSize both equal width * height * 2 bytes for Mono16."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono16"
            grab_result = camera.GrabOne(1000)
        expected_size = 64 * 48 * 2
        self.assertEqual(grab_result.PayloadSize, expected_size)
        self.assertEqual(grab_result.ImageSize, expected_size)
        grab_result.Release()

    # ------------------------------------------------------------------
    # GetStride: multi-channel format (GrabResultData.i)
    # ------------------------------------------------------------------

    def test_get_stride_returns_bytes_per_row_for_rgb8_packed(self):
        """GetStride for RGB8Packed returns (True, width * 3) because each pixel is 3 bytes."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "RGB8Packed"
            grab_result = camera.GrabOne(1000)
        success, stride = grab_result.GetStride()
        self.assertTrue(success)
        self.assertEqual(stride, 64 * 3)  # RGB8Packed: 3 bytes per pixel, no padding
        grab_result.Release()

    # ------------------------------------------------------------------
    # Multi-channel and Bayer pixel formats (GrabResultPtr.i / numpy)
    # ------------------------------------------------------------------

    def test_get_array_returns_3d_shape_for_rgb8_packed(self):
        """GetArray returns a 3-D (height, width, 3) uint8 ndarray for RGB8Packed."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "RGB8Packed"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64, 3))
        self.assertEqual(array.dtype, numpy.uint8)
        grab_result.Release()

    def test_get_array_returns_3d_shape_for_bgr8_packed(self):
        """GetArray returns a 3-D (height, width, 3) uint8 ndarray for BGR8Packed."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "BGR8Packed"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64, 3))
        self.assertEqual(array.dtype, numpy.uint8)
        grab_result.Release()

    def test_get_image_format_rgb8_packed_returns_3d_shape(self):
        """GetImageFormat for RGB8Packed returns ((height, width, 3), uint8, 'B')."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "RGB8Packed"
            grab_result = camera.GrabOne(1000)
        shape, dtype, format_char = grab_result.GetImageFormat()
        self.assertEqual(shape, (48, 64, 3))
        self.assertEqual(dtype, numpy.uint8)
        self.assertEqual(format_char, "B")
        grab_result.Release()

    def test_get_array_returns_2d_uint8_for_bayer_rg8(self):
        """GetArray for BayerRG8 returns a 2-D uint8 ndarray (single plane, not demosaiced)."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "BayerRG8"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64))
        self.assertEqual(array.dtype, numpy.uint8)
        grab_result.Release()

    def test_get_array_returns_2d_uint16_for_bayer_rg16(self):
        """GetArray for BayerRG16 returns a 2-D uint16 ndarray (single plane, not demosaiced)."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "BayerRG16"
            grab_result = camera.GrabOne(1000)
        array = grab_result.GetArray()
        self.assertEqual(array.shape, (48, 64))
        self.assertEqual(array.dtype, numpy.uint16)
        grab_result.Release()

    # ------------------------------------------------------------------
    # NumPy zero-copy raw access (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_get_array_zero_copy_raw_returns_1d_uint8_payload(self):
        """GetArrayZeroCopy(raw=True) yields a 1-D uint8 array of length PayloadSize."""
        import numpy
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        with grab_result.GetArrayZeroCopy(raw=True) as raw_array:
            self.assertEqual(raw_array.ndim, 1)
            self.assertEqual(raw_array.dtype, numpy.uint8)
            self.assertEqual(raw_array.size, grab_result.PayloadSize)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Context manager: exception propagation (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_context_manager_releases_on_exception(self):
        """__exit__ releases the GrabResult even when an exception is raised inside the with-block."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(1000)

        try:
            with grab_result:
                self.assertTrue(grab_result.IsValid())
                raise ValueError("intentional test error")
        except ValueError:
            pass

        self.assertFalse(grab_result.IsValid())

    # ------------------------------------------------------------------
    # GrabResult smart pointer: simultaneous references (GrabResultPtr.h)
    # ------------------------------------------------------------------

    def test_multiple_grab_results_held_simultaneously_are_all_valid(self):
        """Multiple GrabResults grabbed without releasing earlier ones are all independently valid."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            first = camera.GrabOne(1000)
            second = camera.GrabOne(1000)
            third = camera.GrabOne(1000)

        self.assertTrue(first.IsValid())
        self.assertTrue(second.IsValid())
        self.assertTrue(third.IsValid())
        # All IDs must be distinct
        self.assertNotEqual(first.ID, second.ID)
        self.assertNotEqual(second.ID, third.ID)
        first.Release()
        second.Release()
        third.Release()

    # ------------------------------------------------------------------
    # Context values: custom CameraContext (GrabResultData.h)
    # ------------------------------------------------------------------

    def test_camera_context_reflects_set_camera_context(self):
        """CameraContext in the grab result equals the value set via SetCameraContext."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.SetCameraContext(42)
            grab_result = camera.GrabOne(1000)
        self.assertEqual(grab_result.CameraContext, 42)
        self.assertEqual(grab_result.GetCameraContext(), 42)
        grab_result.Release()

    # ------------------------------------------------------------------
    # Introspection: __dir__ (GrabResultPtr.i)
    # ------------------------------------------------------------------

    def test_dir_includes_public_methods_and_properties(self):
        """dir(grab_result) lists the public properties and methods exposed by the binding."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.Width.Value = 64
            camera.Height.Value = 48
            camera.PixelFormat.Value = "Mono8"
            grab_result = camera.GrabOne(1000)
        names = dir(grab_result)
        for expected in ("Width", "Height", "Array", "GetArray", "GrabSucceeded", "PayloadType"):
            self.assertIn(expected, names)
        grab_result.Release()


if __name__ == "__main__":
    unittest.main()
