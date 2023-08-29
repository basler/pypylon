from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class VersionInfoTestSuite(PylonEmuTestCase):
    # Tests that you can get proper version info
    def test_version_get(self):
        cam = self.create_first()
        cam.Open()

        v = cam.GetSfncVersion()

        # camemu has sfnc version 0.0.0.0
        self.assertEqual(0, v.getMajor())
        self.assertEqual(0, v.getMinor())
        self.assertEqual(0, v.getSubminor())
        self.assertEqual(0, v.getBuild())

        cam.Close()

    # Tests that you can compare version info
    def test_version_compare(self):
        v0 = pylon.VersionInfo(2, 2, 2)
        v1 = pylon.VersionInfo(2, 2, 1)
        v0_1 = pylon.VersionInfo(2, 2, 2)

        self.assertGreater(v0, v1)
        self.assertLess(v1, v0)
        self.assertEqual(v0, v0_1)

    # Tests that version info has repr
    def test_version_repr(self):
        cam = self.create_first()
        cam.Open()

        v = cam.GetSfncVersion()
        sfnc_version_repr = v.__repr__()
        self.assertEqual("<VersionInfo 0.0.0>", sfnc_version_repr)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
