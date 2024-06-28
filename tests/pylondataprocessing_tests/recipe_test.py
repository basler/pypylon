import os
num = 1
if int(os.environ.get("PYLON_CAMEMU", 0)) < num:
    os.environ["PYLON_CAMEMU"] = "%d" % num
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
from pypylon import genicam
import unittest

# This is just a workaround for testing puposes
class TWaitObject:
    def __init__(self):
        self._rc = pylondataprocessing.GenericOutputObserver()
        
    def Wait(self, timeout):
        return self._rc.GetWaitObject().Wait(timeout)

    def Signal(self):
        self._rc.OutputDataPush(pylondataprocessing.Recipe(), {}, pylondataprocessing.Update(), 0)
    
    def Reset(self):
        self._rc.Clear()


class TOuputObserver(pylondataprocessing.OutputObserver):
    def __init__(self):
        pylondataprocessing.OutputObserver.__init__(self)
        self.Recipe = None
        self.Value = None
        self.Update = None
        self.UserProvidedID = None

    def OutputDataPush(self, recipe, value, update, userProvidedId):
        #print("OutputDataPush")
        self.Recipe = recipe  #Attention: recipe can only be used in this call, e.g. to get the RecipeContext
        self.Value = value #Value is converted from CVariantContainer to a dictionary and can be used anywhere
        self.Update = pylondataprocessing.Update(update) #Attention: recipe can only be used in this call, create a copy to move it somewhere else
        self.UserProvidedID = userProvidedId

class TUpdateObserver(pylondataprocessing.UpdateObserver):
    def __init__(self):
        pylondataprocessing.UpdateObserver.__init__(self)
        self.Recipe = None
        self.Update = None
        self.UserProvidedID = None
        self.WaitObject = TWaitObject()

    def UpdateDone(self, recipe, update, userProvidedId):
        #print("UpdateDone")
        self.Recipe = recipe #Attention: recipe can only be used in this call, e.g. to get the RecipeContext
        self.Update = pylondataprocessing.Update(update) #Attention: recipe can only be used in this call, create a copy to move it somewhere else
        self.UserProvidedID = userProvidedId
        self.WaitObject.Signal()

class TEventObserver(pylondataprocessing.EventObserver):
    def __init__(self):
        pylondataprocessing.EventObserver.__init__(self)
        self.Recipe = None
        self.Events = None
        self.WaitObject = TWaitObject()
    
    def OnEventSignaled(self, recipe, events):
        #print("OnEventSignaled")
        self.Recipe = recipe #Attention: recipe can only be used in this call, e.g. to get the RecipeContext
        self.Events = events #Value is converted to a list and can be used anywhere
        #print(events[0])
        self.WaitObject.Signal()
        return True; #superfluous in C++ API, has been removed in data processing version 2.0/pylon 7.5

class RecipeTestSuite(PylonDataProcessingTestCase):
    def test_flow(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'recipe_test.precipe')
        #
        # create
        testee = pylondataprocessing.Recipe()
        self.assertFalse(testee.IsLoaded())
        self.assertFalse(testee.IsStarted())
        self.assertFalse(testee.HasInput("Image"))
        self.assertFalse(testee.HasOutput("Image"))
        #
        # unregister event observer
        testEventObserver = TEventObserver()
        testee.RegisterEventObserver(testEventObserver)
        #
        # recipe context
        testee.SetRecipeContext(85)
        self.assertEqual(testee.GetRecipeContext(), 85)
        self.assertEqual(testee.RecipeContext, 85)
        #
        # load
        testee.Load(recipefilename)
        self.assertTrue(testee.IsLoaded())
        self.assertFalse(testee.IsStarted())
        self.assertTrue(testee.HasInput("Image"))
        self.assertTrue(testee.HasOutput("Image"))
        self.assertEqual(testee.GetInputType("Image"), pylondataprocessing.VariantDataType_PylonImage)
        self.assertEqual(testee.GetOutputType("Image"), pylondataprocessing.VariantDataType_PylonImage)
        #
        # parameters
        self.assertTrue(testee.ContainsParameter("ImageLoading/@vTool/SourcePath"))
        self.assertFalse(testee.ContainsParameter("ImageLoading/@vTool/TestNotThere"))
        allParameterNames = testee.GetAllParameterNames()
        self.assertTrue("ImageLoading/@vTool/SourcePath" in allParameterNames)
        testee.GetParameter("ImageLoading/@vTool/SourcePath").SetValue(thisdir);
        #
        # check get output names
        outputNameList = testee.GetOutputNames()
        self.assertEqual(len(outputNameList), 5)
        self.assertTrue(type(outputNameList) is tuple)
        #
        # preallocate
        testee.PreAllocateResources()
        resultCollector = pylondataprocessing.GenericOutputObserver()
        #
        # resgister output sink
        testee.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append, 85)
        #
        # unregister output sink
        self.assertTrue(testee.UnregisterOutputObserver(resultCollector, 85))
        self.assertFalse(testee.UnregisterOutputObserver(resultCollector, 85))
        #
        # resgister output sink v2
        testee.RegisterOutputObserver(["Image", "ImageLoader", "ImagePath", "RunCount"], resultCollector, pylon.RegistrationMode_Append, 85)
        # start
        testee.Start()
        self.assertTrue(testee.IsLoaded())
        self.assertTrue(testee.IsStarted())
        #
        # result 1
        self.assertTrue(resultCollector.GetWaitObject().Wait(5000))
        fullresult1 = resultCollector.RetrieveFullResult()
        self.assertTrue(fullresult1.Update.IsValid())
        self.assertEqual(fullresult1.UserProvidedID, 85)
        self.assertTrue(fullresult1.Container["Image"].ToImage().IsValid())
        self.assertTrue(fullresult1.Container["ImageLoader"].ToImage().IsValid())
        self.assertEqual(fullresult1.Container["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
        self.assertTrue(fullresult1.Container["RunCount"].ToInt64(), 1)
        #
        # result 2
        self.assertTrue(resultCollector.GetWaitObject().Wait(5000))
        fullresult2 = resultCollector.RetrieveFullResult()
        self.assertTrue(fullresult1.Update < fullresult2.Update)
        self.assertTrue(fullresult1.Update != fullresult2.Update)
        self.assertTrue(fullresult2.Update.IsValid())
        self.assertEqual(fullresult2.UserProvidedID, 85)
        self.assertTrue(fullresult2.Container["Image"].ToImage().IsValid())
        self.assertTrue(fullresult2.Container["ImageLoader"].ToImage().IsValid())
        self.assertEqual(fullresult2.Container["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
        self.assertTrue(fullresult2.Container["RunCount"].ToInt64(), 1)
        #
        # result 3
        self.assertTrue(resultCollector.GetWaitObject().Wait(5000))
        result = resultCollector.RetrieveResult()
        self.assertTrue(result["Image"].ToImage().IsValid())
        self.assertTrue(result["ImageLoader"].ToImage().IsValid())
        self.assertEqual(result["ImagePath"].DataType, pylondataprocessing.VariantDataType_String)
        self.assertTrue(result["RunCount"].ToInt64(), 1)
        #
        # loader vTool stopped, it is configured to trigger updates for 3 images
        self.assertFalse(resultCollector.GetWaitObject().Wait(100))
        self.assertTrue(testee.CanTriggerUpdate())
        #
        # unregister output sink
        self.assertTrue(testee.UnregisterOutputObserver(resultCollector, 85))
        #
        # TriggerUpdateAsync
        testOutputObserver = TOuputObserver()
        testUpdateObserver = TUpdateObserver()
        testee.RegisterOutputObserver(["ImageConverter2"], testOutputObserver, pylon.RegistrationMode_Append, 83)
        testee.RegisterOutputObserver(["ImageConverter2"], resultCollector, pylon.RegistrationMode_Append, 83)
        update1 = testee.TriggerUpdateAsync({"Image" : result["Image"]}, testUpdateObserver, 47)
        self.assertTrue(resultCollector.GetWaitObject().Wait(5000))
        self.assertTrue(testUpdateObserver.WaitObject.Wait(5000)) #the update may finish later, this depends on the recipe
        self.assertTrue(testee.UnregisterOutputObserver(resultCollector, 83))
        self.assertTrue(testee.UnregisterOutputObserver(testOutputObserver, 83))
        self.assertEqual(testUpdateObserver.UserProvidedID, 47)
        self.assertEqual(testOutputObserver.UserProvidedID, 83)
        self.assertTrue(update1 == testUpdateObserver.Update)
        self.assertTrue(update1 == testOutputObserver.Update)
        self.assertTrue(testOutputObserver.Value["ImageConverter2"].ToImage().IsValid())
        #
        # TriggerUpdate
        testOutputObserver = TOuputObserver()
        testUpdateObserver = TUpdateObserver()
        testee.RegisterOutputObserver(["ImageConverter2"], testOutputObserver, pylon.RegistrationMode_Append, 83)
        update1 = testee.TriggerUpdate({"Image" : result["Image"]}, 1000, pylon.TimeoutHandling_ThrowException, testUpdateObserver, 48)
        self.assertTrue(testUpdateObserver.WaitObject.Wait(5000)) #the update may finish later, this depends on the recipe
        self.assertEqual(testUpdateObserver.UserProvidedID, 48)
        self.assertEqual(testOutputObserver.UserProvidedID, 83)
        self.assertTrue(update1 == testUpdateObserver.Update)
        self.assertTrue(update1 == testOutputObserver.Update)
        self.assertTrue(testOutputObserver.Value["ImageConverter2"].ToImage().IsValid())
        #
        # stop
        testee.Stop()
        self.assertTrue(testee.IsLoaded())
        self.assertFalse(testee.IsStarted())
        testee.Stop(100)
        #
        # deallocate
        testee.DeallocateResources()
        #
        # unload
        testee.Unload()
        self.assertFalse(testee.IsLoaded())
        self.assertFalse(testee.IsStarted())
        self.assertFalse(testee.HasInput("Image"))
        self.assertFalse(testee.HasOutput("Image"))
        #
        # unregister event observer
        testee.UnregisterEventObserver()

    def test_loadfrombinary(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'recipe_test.precipe')
        with open(recipefilename, mode='rb') as file:
            fileContent = file.read()
        testee = pylondataprocessing.Recipe()
        testee.LoadFromBinary(fileContent)
        self.assertTrue(testee.IsLoaded())
        testee.Unload()
        self.assertFalse(testee.IsLoaded())
        testee.LoadFromBinary(fileContent, thisdir)
        self.assertTrue(testee.IsLoaded())
        testee.Unload()
        self.assertFalse(testee.IsLoaded())

    def test_eventobserver(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'recipe_eventobserver_test.precipe')
        testee = pylondataprocessing.Recipe()
        testEventObserver = TEventObserver()
        testee.RegisterEventObserver(testEventObserver)
        testee.Load(recipefilename)
        testee.Start()
        self.assertTrue(testee.ContainsParameter("Camera/@CameraDevice/FirePnPCallback"))
        #trigger a camera vTool error
        testee.GetParameter("Camera/@CameraDevice/FirePnPCallback").Execute()
        self.assertTrue(testEventObserver.WaitObject.Wait(500))
        self.assertEqual(len(testEventObserver.Events), 1)
        self.assertEqual(testEventObserver.Events[0].EventType, 1)
        self.assertEqual(testEventObserver.Events[0].EventSourceName, "Camera")
        testEventObserver.WaitObject.Reset()
        testee.Stop()
        self.assertTrue(testEventObserver.WaitObject.Wait(500))
        self.assertEqual(len(testEventObserver.Events), 1)
        self.assertEqual(testEventObserver.Events[0].EventType, 2)
        self.assertEqual(testEventObserver.Events[0].EventSourceName, "Camera")
        self.assertTrue(testEventObserver.WaitObject.Wait(500))
        testee.Unload()

if __name__ == "__main__":
    unittest.main()
