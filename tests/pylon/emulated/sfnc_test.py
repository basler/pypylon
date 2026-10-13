"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/SfncVersion.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest

class SfncTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Camera SFNC version
    # ------------------------------------------------------------------

    def test_sfnc_camera_version(self):
        """GetSfncVersion returns SFNC 2.5.0 for the emulated camera."""
        camera = self.create_first()
        camera.Open()
        sfnc = pylon.GetSfncVersion(camera.GetNodeMap())
        # Since pylon 12.4 the emulated camera reports SFNC version 2.5.0.
        self.assertEqual(sfnc, pylon.Sfnc_2_5_0)
        self.assertEqual("<VersionInfo 2.5.0>", str(sfnc))
        camera.Close()

    # ------------------------------------------------------------------
    # Exact version numbers encoded in each constant's name
    # ------------------------------------------------------------------

    def test_sfnc_version_undefined_is_0_0_0(self):
        """Sfnc_VersionUndefined has version 0.0.0."""
        v = pylon.Sfnc_VersionUndefined
        self.assertEqual(0, v.Major)
        self.assertEqual(0, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_1_2_1_is_1_2_1(self):
        """Sfnc_1_2_1 has version 1.2.1."""
        v = pylon.Sfnc_1_2_1
        self.assertEqual(1, v.Major)
        self.assertEqual(2, v.Minor)
        self.assertEqual(1, v.Subminor)

    def test_sfnc_1_3_0_is_1_3_0(self):
        """Sfnc_1_3_0 has version 1.3.0."""
        v = pylon.Sfnc_1_3_0
        self.assertEqual(1, v.Major)
        self.assertEqual(3, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_1_4_0_is_1_4_0(self):
        """Sfnc_1_4_0 has version 1.4.0."""
        v = pylon.Sfnc_1_4_0
        self.assertEqual(1, v.Major)
        self.assertEqual(4, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_1_5_0_is_1_5_0(self):
        """Sfnc_1_5_0 has version 1.5.0."""
        v = pylon.Sfnc_1_5_0
        self.assertEqual(1, v.Major)
        self.assertEqual(5, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_1_5_1_is_1_5_1(self):
        """Sfnc_1_5_1 has version 1.5.1."""
        v = pylon.Sfnc_1_5_1
        self.assertEqual(1, v.Major)
        self.assertEqual(5, v.Minor)
        self.assertEqual(1, v.Subminor)

    def test_sfnc_2_0_0_is_2_0_0(self):
        """Sfnc_2_0_0 has version 2.0.0."""
        v = pylon.Sfnc_2_0_0
        self.assertEqual(2, v.Major)
        self.assertEqual(0, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_2_1_0_is_2_1_0(self):
        """Sfnc_2_1_0 has version 2.1.0."""
        v = pylon.Sfnc_2_1_0
        self.assertEqual(2, v.Major)
        self.assertEqual(1, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_2_2_0_is_2_2_0(self):
        """Sfnc_2_2_0 has version 2.2.0."""
        v = pylon.Sfnc_2_2_0
        self.assertEqual(2, v.Major)
        self.assertEqual(2, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_2_3_0_is_2_3_0(self):
        """Sfnc_2_3_0 has version 2.3.0."""
        v = pylon.Sfnc_2_3_0
        self.assertEqual(2, v.Major)
        self.assertEqual(3, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_2_4_0_is_2_4_0(self):
        """Sfnc_2_4_0 has version 2.4.0."""
        v = pylon.Sfnc_2_4_0
        self.assertEqual(2, v.Major)
        self.assertEqual(4, v.Minor)
        self.assertEqual(0, v.Subminor)

    def test_sfnc_2_5_0_is_2_5_0(self):
        """Sfnc_2_5_0 has version 2.5.0."""
        v = pylon.Sfnc_2_5_0
        self.assertEqual(2, v.Major)
        self.assertEqual(5, v.Minor)
        self.assertEqual(0, v.Subminor)

    # ------------------------------------------------------------------
    # Constants are ordered strictly as expected
    # ------------------------------------------------------------------

    def test_sfnc_constants_ordering(self):
        """The Sfnc_* constants are strictly ascending in version order."""
        self.assertLess(pylon.Sfnc_VersionUndefined, pylon.Sfnc_1_2_1)
        self.assertLess(pylon.Sfnc_1_2_1,            pylon.Sfnc_1_3_0)
        self.assertLess(pylon.Sfnc_1_3_0,            pylon.Sfnc_1_4_0)
        self.assertLess(pylon.Sfnc_1_4_0,            pylon.Sfnc_1_5_0)
        self.assertLess(pylon.Sfnc_1_5_0,            pylon.Sfnc_1_5_1)
        self.assertLess(pylon.Sfnc_1_5_1,            pylon.Sfnc_2_0_0)
        self.assertLess(pylon.Sfnc_2_0_0,            pylon.Sfnc_2_1_0)
        self.assertLess(pylon.Sfnc_2_1_0,            pylon.Sfnc_2_2_0)
        self.assertLess(pylon.Sfnc_2_2_0,            pylon.Sfnc_2_3_0)
        self.assertLess(pylon.Sfnc_2_3_0,            pylon.Sfnc_2_4_0)
        self.assertLess(pylon.Sfnc_2_4_0,            pylon.Sfnc_2_5_0)


if __name__ == "__main__":
    unittest.main()