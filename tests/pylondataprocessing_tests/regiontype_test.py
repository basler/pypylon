from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest

class RegionTypeTestSuite(PylonDataProcessingTestCase):
    def test_presence(self):
        self.assertEqual(pylondataprocessing.RegionType_Undefined, -1)
        self.assertEqual(pylondataprocessing.RegionType_RLE32, 6291457)
        
    def test_IsValid(self):
        self.assertTrue(pylondataprocessing.IsValidRegionType(pylondataprocessing.RegionType_RLE32))
        self.assertFalse(pylondataprocessing.IsValidRegionType(pylondataprocessing.RegionType_Undefined))
        
    def test_BitPerRegionElement(self):
        self.assertEqual(pylondataprocessing.BitPerRegionElement(pylondataprocessing.RegionType_RLE32), 3 * 32)
        try:
            pylondataprocessing.BitPerRegionElement(pylondataprocessing.RegionType_Undefined)
        except genicam.InvalidArgumentException as e:
            self.assertTrue(str(e).startswith("Invalid region type passed."))

    def test_ComputeRegionSize(self):    
        self.assertEqual(pylondataprocessing.ComputeRegionSize(pylondataprocessing.RegionType_RLE32, 10), 3 * 4 * 10)
        try:
            pylondataprocessing.ComputeRegionSize(pylondataprocessing.RegionType_Undefined, 10)
        except genicam.InvalidArgumentException as e:
            self.assertTrue(str(e).startswith("Invalid region type passed."))
    
if __name__ == "__main__":
    unittest.main()
