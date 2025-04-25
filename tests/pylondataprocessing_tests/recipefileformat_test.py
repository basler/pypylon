from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest

class RecipeFileFormatTestSuite(PylonDataProcessingTestCase):
    def test_presence(self):
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(3,1,0):
            self.assertEqual(pylondataprocessing.RecipeFileFormat_JsonDefault, 1)             
            self.assertEqual(pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData, 2)            

if __name__ == "__main__":
    unittest.main()
