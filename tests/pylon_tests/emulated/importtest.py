from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest


class ImportTestSuite(PylonEmuTestCase):
    # These are only "mounted" into the pylon namespace. So we ensure these are available here also
    def test_import_exceptions(self):
        from pypylon.pylon import GenericException;
        from pypylon.pylon import InvalidArgumentException;
        from pypylon.pylon import BadAllocException;
        from pypylon.pylon import OutOfRangeException;
        from pypylon.pylon import PropertyException;
        from pypylon.pylon import RuntimeException;
        from pypylon.pylon import LogicalErrorException;
        from pypylon.pylon import AccessException;
        from pypylon.pylon import TimeoutException;
        from pypylon.pylon import DynamicCastException;


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
