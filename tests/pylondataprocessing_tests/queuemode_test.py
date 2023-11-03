from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class QueueModeTestSuite(PylonDataProcessingTestCase):
    def test_presence(self):
        self.assertEqual(pylondataprocessing.QueueMode_Unlimited, 0)
        self.assertEqual(pylondataprocessing.QueueMode_DropOldest, 1)
        self.assertEqual(pylondataprocessing.QueueMode_DropNewest, 2)
        self.assertEqual(pylondataprocessing.QueueMode_Blocking, 3)         

if __name__ == "__main__":
    unittest.main()
