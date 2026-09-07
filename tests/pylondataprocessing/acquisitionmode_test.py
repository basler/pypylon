"""\
This unit test checks all of the mapped pypylon API introduced by
src/pylondataprocessing/AcquisitionMode.i.

Note: pylondataprocessing is not supported on macOS — these tests are collected
only on platforms where the module is available.
"""
import os
num = 1
if int(os.environ.get("PYLON_CAMEMU", 0)) < num:
    os.environ["PYLON_CAMEMU"] = "%d" % num
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest


class AcquisitionModeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    def test_acquisition_mode_unchanged_exists(self):
        """AcquisitionMode_Unchanged is accessible and is an integer."""
        self.assertIsInstance(pylondataprocessing.AcquisitionMode_Unchanged, int)

    def test_acquisition_mode_constants_are_distinct(self):
        """All AcquisitionMode constants have distinct integer values."""
        constants = [
            pylondataprocessing.AcquisitionMode_Unchanged,
        ]
        self.assertEqual(len(constants), len(set(constants)))

    # ------------------------------------------------------------------
    # API integration — Start() with explicit AcquisitionMode
    # ------------------------------------------------------------------

    def test_recipe_start_with_acquisition_mode_unchanged(self):
        """Recipe.Start(AcquisitionMode_Unchanged) does not raise."""
        recipe_filename = os.path.join(
            os.path.dirname(__file__), "recipe_test.precipe"
        )
        recipe = pylondataprocessing.Recipe()
        recipe.Load(recipe_filename)
        recipe.Start(pylondataprocessing.AcquisitionMode_Unchanged)
        recipe.Stop()


if __name__ == "__main__":
    unittest.main()
