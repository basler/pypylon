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
                [],
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


if __name__ == "__main__":
    unittest.main()

