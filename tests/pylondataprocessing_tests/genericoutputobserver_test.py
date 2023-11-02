from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import genicam
import unittest

class GenericOutputObserverTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee1 = pylondataprocessing.GenericOutputObserverResult()
        self.assertEqual(testee1.Update, pylondataprocessing.Update())
        self.assertEqual(testee1.UserProvidedID, 0)
        self.assertTrue(type(testee1.Container) is dict)
        self.assertTrue(type(testee1.GetContainer()) is dict) #do not use
        
        testee2 = pylondataprocessing.GenericOutputObserver()
        self.assertFalse(testee2.GetWaitObject().Wait(0))
        self.assertEqual(testee2.GetNumResults(), 0)
        self.assertTrue(type(testee2.RetrieveFullResult().Container) is dict)
        self.assertTrue(type(testee2.RetrieveResult()) is dict)
        self.assertEqual(len(testee2.RetrieveFullResult().Container), 0)
        self.assertEqual(len(testee2.RetrieveResult()), 0)
        testee2.Clear()
        
    def test_push(self):
        inputData = {"Image" : pylondataprocessing.Variant(pylondataprocessing.VariantDataType_PylonImage)}
        testee1 = pylondataprocessing.GenericOutputObserver()
        testee1.OutputDataPush(pylondataprocessing.Recipe(), inputData, pylondataprocessing.Update(), 892);
        self.assertTrue(testee1.GetWaitObject().Wait(0))
        self.assertEqual(testee1.GetNumResults(), 1)
        testee2 = testee1.RetrieveFullResult()
        self.assertFalse(testee1.GetWaitObject().Wait(0))
        self.assertEqual(testee1.GetNumResults(), 0)
        self.assertTrue(type(testee2.Container) is dict)
        self.assertEqual(len(testee2.Container), 1)
        self.assertEqual(testee2.UserProvidedID, 892)
        self.assertFalse(testee2.Update.IsValid())
        testee1.OutputDataPush(pylondataprocessing.Recipe(), inputData, pylondataprocessing.Update(), 892);
        self.assertTrue(testee1.GetWaitObject().Wait(0))
        self.assertEqual(testee1.GetNumResults(), 1)
        testee3 = testee1.RetrieveResult()
        self.assertFalse(testee1.GetWaitObject().Wait(0))
        self.assertEqual(testee1.GetNumResults(), 0)
        self.assertEqual(testee3, inputData)
        testee1.OutputDataPush(pylondataprocessing.Recipe(), inputData, pylondataprocessing.Update(), 892);
        self.assertTrue(testee1.GetWaitObject().Wait(0))
        self.assertTrue(testee1.WaitObject.Wait(0))
        self.assertEqual(testee1.GetNumResults(), 1)
        self.assertEqual(testee1.NumResults, 1)
        testee1.Clear()
        self.assertFalse(testee1.GetWaitObject().Wait(0))
        self.assertEqual(testee1.GetNumResults(), 0)
        
if __name__ == "__main__":
    unittest.main()
    