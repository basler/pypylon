"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylon/StaticDefectPixelCorrection.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class StaticDefectPixelCorrectionTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Surface API
    # ------------------------------------------------------------------

    def test_static_defect_pixel_correction_symbols_exist(self):
        """StaticDefectPixelCorrection and its list type constants are available."""
        self.assertTrue(hasattr(pylon, "StaticDefectPixelCorrection"))
        self.assertTrue(hasattr(pylon.StaticDefectPixelCorrection, "ListType_Factory"))
        self.assertTrue(hasattr(pylon.StaticDefectPixelCorrection, "ListType_User"))

    # ------------------------------------------------------------------
    # Get / Set / Normalize
    # ------------------------------------------------------------------

    def test_get_defect_pixel_list_returns_status_and_list(self):
        """GetDefectPixelList returns [success, pixel_list] with a Python list payload."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            result = pylon.StaticDefectPixelCorrection.GetDefectPixelList(
                camera.NodeMap,
                pylon.StaticDefectPixelCorrection.ListType_User,
            )

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], list)

    def test_set_defect_pixel_list_accepts_python_list(self):
        """SetDefectPixelList accepts Python (x, y[, type]) tuples and returns a status/list pair."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            try:
                result = pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(10, 20), (12, 25, 0)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )
            except pylon.RuntimeException as exc:
                self.skipTest(f"Static defect pixel list is not supported by this camera: {exc}")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], list)

    def test_normalize_pixel_list_accepts_and_returns_python_list(self):
        """NormalizePixelList accepts Python list input and returns [success, normalized_list]."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            try:
                result = pylon.StaticDefectPixelCorrection.NormalizePixelList(
                    camera.NodeMap,
                    [(11, 33, 0), (11, 33, 0), (3, 2, 0)],
                )
            except pylon.RuntimeException as exc:
                self.skipTest(f"Static defect pixel list is not supported by this camera: {exc}")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], list)

    # ------------------------------------------------------------------
    # staticdefectpixel_vector class
    # ------------------------------------------------------------------

    def test_staticdefectpixel_vector_construction_empty(self):
        """A newly constructed staticdefectpixel_vector has size 0 and reports empty."""
        vector = pylon.staticdefectpixel_vector()
        self.assertEqual(len(vector), 0)
        self.assertEqual(vector.size(), 0)
        self.assertTrue(vector.empty())

    def test_staticdefectpixel_vector_falsy_when_empty(self):
        """An empty staticdefectpixel_vector is falsy."""
        vector = pylon.staticdefectpixel_vector()
        self.assertFalse(bool(vector))

    def test_staticdefectpixel_vector_reserve_sets_capacity(self):
        """reserve(n) ensures capacity() is at least n."""
        vector = pylon.staticdefectpixel_vector()
        vector.reserve(10)
        self.assertGreaterEqual(vector.capacity(), 10)

    def test_staticdefectpixel_vector_resize_increases_size(self):
        """resize(n) makes size() equal to n."""
        vector = pylon.staticdefectpixel_vector()
        vector.resize(5)
        self.assertEqual(vector.size(), 5)
        self.assertEqual(len(vector), 5)

    def test_staticdefectpixel_vector_clear_resets_size(self):
        """clear() resets size to 0 and empty() to True."""
        vector = pylon.staticdefectpixel_vector()
        vector.resize(3)
        vector.clear()
        self.assertEqual(len(vector), 0)
        self.assertTrue(vector.empty())

    def test_staticdefectpixel_vector_swap_exchanges_contents(self):
        """swap() exchanges the sizes of two staticdefectpixel_vector instances."""
        vector_a = pylon.staticdefectpixel_vector()
        vector_b = pylon.staticdefectpixel_vector()
        vector_a.resize(4)
        vector_a.swap(vector_b)
        self.assertEqual(len(vector_a), 0)
        self.assertEqual(len(vector_b), 4)

    def test_staticdefectpixel_vector_iteration_over_empty(self):
        """Iterating an empty staticdefectpixel_vector yields no items."""
        vector = pylon.staticdefectpixel_vector()
        self.assertEqual(list(vector), [])

    # ------------------------------------------------------------------
    # StaticDefectPixel struct
    # ------------------------------------------------------------------

    def test_static_defect_pixel_construction_default_zeros(self):
        """A default-constructed StaticDefectPixel has X, Y, and Type all equal to 0."""
        pixel = pylon.StaticDefectPixel()
        self.assertEqual(pixel.X, 0)
        self.assertEqual(pixel.Y, 0)
        self.assertEqual(pixel.Type, 0)

    def test_static_defect_pixel_field_write_and_read(self):
        """StaticDefectPixel fields X, Y, and Type are writable and readable."""
        pixel = pylon.StaticDefectPixel()
        pixel.X = 1023
        pixel.Y = 767
        pixel.Type = pylon.StaticDefectPixelType_Reserved
        self.assertEqual(pixel.X, 1023)
        self.assertEqual(pixel.Y, 767)
        self.assertEqual(pixel.Type, pylon.StaticDefectPixelType_Reserved)

    # ------------------------------------------------------------------
    # Constants
    # ------------------------------------------------------------------

    def test_staticdefectpixeltype_reserved_is_zero(self):
        """StaticDefectPixelType_Reserved has the value 0."""
        self.assertEqual(pylon.StaticDefectPixelType_Reserved, 0)

    # ------------------------------------------------------------------
    # Typemap input validation
    # ------------------------------------------------------------------

    def test_typemap_rejects_non_list_input(self):
        """SetDefectPixelList raises TypeError when the pixel list argument is not a list."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(TypeError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    "not_a_list",
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_non_sequence_element(self):
        """SetDefectPixelList raises TypeError when a list element is not a tuple or list."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(TypeError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    ["not_a_tuple"],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_element_with_one_value(self):
        """SetDefectPixelList raises ValueError when a pixel entry has only one value."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(10,)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_element_with_four_values(self):
        """SetDefectPixelList raises ValueError when a pixel entry has four or more values."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(10, 20, 0, 99)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_x_above_max_uint16(self):
        """SetDefectPixelList raises ValueError when x exceeds the uint16 maximum (65535)."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(65536, 0)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_y_above_max_uint16(self):
        """SetDefectPixelList raises ValueError when y exceeds the uint16 maximum (65535)."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(0, 65536)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_negative_x(self):
        """SetDefectPixelList raises ValueError when x is negative."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(-1, 0)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_negative_y(self):
        """SetDefectPixelList raises ValueError when y is negative."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(ValueError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [(0, -1)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_rejects_non_integer_coordinate(self):
        """SetDefectPixelList raises TypeError when a coordinate is not an integer."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            with self.assertRaises(TypeError):
                pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [("a", 20)],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )

    def test_typemap_accepts_list_element(self):
        """SetDefectPixelList accepts a list [x, y] as a pixel entry in addition to a tuple."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            try:
                result = pylon.StaticDefectPixelCorrection.SetDefectPixelList(
                    camera.NodeMap,
                    [[10, 20]],
                    pylon.StaticDefectPixelCorrection.ListType_User,
                )
            except pylon.RuntimeException as exc:
                self.skipTest(f"Static defect pixel list is not supported by this camera: {exc}")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()

