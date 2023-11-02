from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest

class UpdateTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.Update()
        testee2 = pylondataprocessing.Update()
        testee3 = pylondataprocessing.Update(testee2)
        self.assertFalse(testee1.IsValid())
        self.assertEqual(testee1.GetNumPrecedingUpdates(), 0)
        self.assertFalse(testee1.HasBeenTriggeredBy(testee2))
        #invalid updates, you can get valid updates only from a running recipe.
        self.assertTrue(testee1 == testee2)
        self.assertFalse(testee1 != testee2)
        self.assertFalse(testee1 < testee2)
        try:
            testee1.GetPrecedingUpdate(0)
        except genicam.RuntimeException as e:
            self.assertTrue(str(e).startswith("This update is invalid. Cannot get preceding updates."))

if __name__ == "__main__":
    unittest.main()
