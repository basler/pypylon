"""\
This unit test checks the Error type bindings introduced by src/pylondataprocessing/Error.i.

It covers construction, validity, the description accessors, preceding-error
access and the string representation.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest


@unittest.skipUnless(
    hasattr(pylondataprocessing, "Error"),
    "Error is not available in this DataProcessing SDK version",
)
class ErrorTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Construction / validity
    # ------------------------------------------------------------------

    def test_construction_default(self):
        """A default-constructed Error is invalid and has no description."""
        error = pylondataprocessing.Error()
        self.assertFalse(error.IsValid())
        self.assertEqual(error.GetDescription(), "")

    def test_construction_with_description(self):
        """Constructing an Error with a description makes it valid."""
        error = pylondataprocessing.Error("Error message")
        self.assertTrue(error.IsValid())
        self.assertEqual(error.GetDescription(), "Error message")

    # ------------------------------------------------------------------
    # Description accessors
    # ------------------------------------------------------------------

    def test_get_description_std_string(self):
        """GetDescriptionStdString returns the same text as GetDescription."""
        error = pylondataprocessing.Error("Error message")
        self.assertEqual(error.GetDescriptionStdString(), "Error message")

    def test_set_updates_description(self):
        """Set replaces the description and keeps the Error valid."""
        error = pylondataprocessing.Error("Error message")
        error.Set("changed")
        self.assertTrue(error.IsValid())
        self.assertEqual(error.GetDescription(), "changed")

    # ------------------------------------------------------------------
    # Preceding errors
    # ------------------------------------------------------------------

    def test_num_preceding_errors_default(self):
        """A freshly created Error has no preceding errors."""
        error = pylondataprocessing.Error("Error message")
        self.assertEqual(error.GetNumPrecedingErrors(), 0)

    def test_get_preceding_error_out_of_range(self):
        """GetPrecedingError raises when the index is out of range."""
        error = pylondataprocessing.Error("Error message")
        with self.assertRaises(genicam.InvalidArgumentException):
            error.GetPrecedingError(0)

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def test_str(self):
        """str(Error) returns the error description."""
        error = pylondataprocessing.Error("Error message")
        self.assertEqual(str(error), "Error message")


if __name__ == "__main__":
    unittest.main()



