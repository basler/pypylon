from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest

class SmartInstantCameraResultResultTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.SmartInstantCameraResult()
        update = testee1.Update
        grabResult = testee1.GrabResult
        container = testee1.Container
        #GetContainer() is currently also available but not considered part of the official API.
        self.assertFalse(update.IsValid())
        self.assertFalse(grabResult.IsValid())
        self.assertTrue(isinstance(container, dict))
        testee1.Release()

if __name__ == "__main__":
    unittest.main()
