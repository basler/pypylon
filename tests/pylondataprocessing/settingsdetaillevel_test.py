"""\
This unit test checks the enum bindings introduced by SettingsDetailLevel.i.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest


class SettingsDetailLevelTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Enum values
    # ------------------------------------------------------------------

    @unittest.skipUnless(
        pylondataprocessing.GetVersion() >= pylon.VersionInfo(6, 0, 0),
        "SettingsDetailLevel requires data processing 6.0+",
    )
    def test_values(self):
        """Settings detail levels expose their documented integer values."""
        self.assertEqual(pylondataprocessing.Detail_Unknown, -1)
        self.assertEqual(pylondataprocessing.Detail_Complete, 0)
        self.assertEqual(pylondataprocessing.Detail_Lean, 1)


if __name__ == "__main__":
    unittest.main()
