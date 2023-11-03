from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

class VariantContainerTypeTestSuite(PylonDataProcessingTestCase):
    def test_presence(self):
        self.assertEqual(pylondataprocessing.VariantContainerType_None, 0)             
        self.assertEqual(pylondataprocessing.VariantContainerType_Array, 1)            
        self.assertEqual(pylondataprocessing.VariantContainerType_Unsupported, 2)           

if __name__ == "__main__":
    unittest.main()
