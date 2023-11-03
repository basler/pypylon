from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
import unittest

#note the variant container is converted to a python dictionary when using a Recipe 
#TODO: solve SWIG problems and remove the VariantContainer
class VariantContainerTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee = pylondataprocessing.VariantContainer()

if __name__ == "__main__":
    unittest.main()
