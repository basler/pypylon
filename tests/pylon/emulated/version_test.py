"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/PylonVersionInfo.i
and version functions mapped by pylon.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class GetPylonVersionTestSuite(unittest.TestCase):

    # ------------------------------------------------------------------
    # GetPylonVersion / GetPylonVersionString
    # ------------------------------------------------------------------

    def test_get_pylon_version_returns_four_ints(self):
        """GetPylonVersion returns a tuple of four non-negative integers."""
        major, minor, subminor, build = pylon.GetPylonVersion()
        self.assertIsInstance(major, int)
        self.assertIsInstance(minor, int)
        self.assertIsInstance(subminor, int)
        self.assertIsInstance(build, int)

    def test_get_pylon_version_string_is_non_empty(self):
        """GetPylonVersionString returns a non-empty string."""
        version_string = pylon.GetPylonVersionString()
        self.assertGreater(len(version_string), 0)

    def test_get_pylon_version_consistent_with_version_string(self):
        """GetPylonVersion components appear in the GetPylonVersionString output."""
        major, minor, subminor, build = pylon.GetPylonVersion()
        version_string = pylon.GetPylonVersionString()
        self.assertIn(str(major), version_string)
        self.assertIn(str(minor), version_string)
        self.assertIn(str(subminor), version_string)


class VersionInfoTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction / accessors
    # ------------------------------------------------------------------

    def test_version_info_default_construction_matches_pylon_version(self):
        """Default VersionInfo() is initialized with the running pylon version."""
        major, minor, subminor, build = pylon.GetPylonVersion()
        version = pylon.VersionInfo()
        self.assertEqual(major, version.getMajor())
        self.assertEqual(minor, version.getMinor())
        self.assertEqual(subminor, version.getSubminor())
        self.assertEqual(build, version.getBuild())

    def test_version_info_three_param_construction(self):
        """VersionInfo(major, minor, subminor) stores the three parts and sets build to zero."""
        version = pylon.VersionInfo(2, 1, 3)
        self.assertEqual(2, version.getMajor())
        self.assertEqual(1, version.getMinor())
        self.assertEqual(3, version.getSubminor())
        self.assertEqual(0, version.getBuild())

    def test_version_info_four_param_construction(self):
        """VersionInfo(major, minor, subminor, build) stores all four parts."""
        version = pylon.VersionInfo(2, 1, 3, 1234)
        self.assertEqual(2, version.getMajor())
        self.assertEqual(1, version.getMinor())
        self.assertEqual(3, version.getSubminor())
        self.assertEqual(1234, version.getBuild())

    # ------------------------------------------------------------------
    # Properties (Major, Minor, Subminor, Build)
    # ------------------------------------------------------------------

    def test_version_info_properties_match_getters(self):
        """Major, Minor, Subminor, and Build properties return the same values as the get* methods."""
        version = pylon.VersionInfo(2, 1, 3, 1234)
        self.assertEqual(version.getMajor(), version.Major)
        self.assertEqual(version.getMinor(), version.Minor)
        self.assertEqual(version.getSubminor(), version.Subminor)
        self.assertEqual(version.getBuild(), version.Build)

    def test_version_info_properties_three_param(self):
        """Properties reflect the values passed to the three-param constructor."""
        version = pylon.VersionInfo(5, 3, 1)
        self.assertEqual(5, version.Major)
        self.assertEqual(3, version.Minor)
        self.assertEqual(1, version.Subminor)
        self.assertEqual(0, version.Build)

    # ------------------------------------------------------------------
    # Comparison operators
    # ------------------------------------------------------------------

    def test_version_info_greater_than(self):
        """VersionInfo > compares by major, then minor, then subminor."""
        self.assertGreater(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 1))
        self.assertGreater(pylon.VersionInfo(2, 3, 0), pylon.VersionInfo(2, 2, 9))
        self.assertGreater(pylon.VersionInfo(3, 0, 0), pylon.VersionInfo(2, 9, 9))

    def test_version_info_less_than(self):
        """VersionInfo < compares by major, then minor, then subminor."""
        self.assertLess(pylon.VersionInfo(2, 2, 1), pylon.VersionInfo(2, 2, 2))
        self.assertLess(pylon.VersionInfo(2, 2, 9), pylon.VersionInfo(2, 3, 0))
        self.assertLess(pylon.VersionInfo(2, 9, 9), pylon.VersionInfo(3, 0, 0))

    def test_version_info_equal(self):
        """VersionInfo == is true when major, minor, and subminor all match."""
        self.assertEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 2))

    def test_version_info_not_equal(self):
        """VersionInfo != is true when major, minor, or subminor differ."""
        self.assertNotEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 1))
        self.assertNotEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 1, 2))
        self.assertNotEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(1, 2, 2))

    def test_version_info_greater_or_equal(self):
        """VersionInfo >= is true when left is greater than or equal to right."""
        self.assertGreaterEqual(pylon.VersionInfo(2, 2, 3), pylon.VersionInfo(2, 2, 2))
        self.assertGreaterEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 2))

    def test_version_info_less_or_equal(self):
        """VersionInfo <= is true when left is less than or equal to right."""
        self.assertLessEqual(pylon.VersionInfo(2, 2, 1), pylon.VersionInfo(2, 2, 2))
        self.assertLessEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 2))

    # ------------------------------------------------------------------
    # Build number in comparisons
    # ------------------------------------------------------------------

    def test_version_info_four_param_build_used_in_comparison(self):
        """Four-param VersionInfo includes build in equality and ordering."""
        self.assertGreater(pylon.VersionInfo(2, 2, 2, 2), pylon.VersionInfo(2, 2, 2, 1))
        self.assertNotEqual(pylon.VersionInfo(2, 2, 2, 1), pylon.VersionInfo(2, 2, 2, 2))

    def test_version_info_three_param_build_ignored_in_comparison(self):
        """Three-param VersionInfo ignores build — equal to four-param with same major.minor.subminor."""
        # Three-param has checkBuild=False, so the build of the right-hand side is irrelevant.
        self.assertEqual(pylon.VersionInfo(2, 2, 2), pylon.VersionInfo(2, 2, 2, 1234))

    # ------------------------------------------------------------------
    # VersionInfo from camera / repr
    # ------------------------------------------------------------------

    def test_sfnc_version_accessors(self):
        """Camera emulator reports SFNC version 2.5.0 (since pylon 12.4)."""
        with self.create_first() as camera:
            version = camera.GetSfncVersion()
            self.assertEqual(2, version.getMajor())
            self.assertEqual(5, version.getMinor())
            self.assertEqual(0, version.getSubminor())
            self.assertEqual(0, version.getBuild())

    def test_version_info_repr(self):
        """VersionInfo repr formats as <VersionInfo major.minor.subminor>."""
        with self.create_first() as camera:
            version = camera.GetSfncVersion()
            self.assertEqual("<VersionInfo 2.5.0>", repr(version))


if __name__ == "__main__":
    unittest.main()
