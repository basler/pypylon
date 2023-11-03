from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class RegionEntryTestSuite(PylonDataProcessingTestCase):
    def test_init_RegionEntryRLE32(self):
        testee1 = pylondataprocessing.RegionEntryRLE32()
        self.assertEqual(testee1.StartX, 0.0)
        self.assertEqual(testee1.EndX, 0.0)
        self.assertEqual(testee1.Y, 0.0)
        testee2 = pylondataprocessing.RegionEntryRLE32(10, 30, 40)
        self.assertEqual(testee2.StartX, 10)
        self.assertEqual(testee2.EndX, 30)
        self.assertEqual(testee2.Y, 40)
        
    def test_str(self):
        testee = pylondataprocessing.RegionEntryRLE32(10, 30, 40)
        self.assertEqual(str(testee), "StartX = 10; EndX = 30; Y = 40")

if __name__ == "__main__":
    unittest.main()
