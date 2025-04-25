from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest
import os

cameraVToolUuid = "846bca11-6bf2-4895-88c4-fe038f5a659c".upper()
formatConverterVToolUuid = "4049ea56-3827-4faf-9478-c3ba02e4a0cb".upper()

class BuildersRecipeTestSuite(PylonDataProcessingTestCase):
    def test_init(self):
        testee = pylondataprocessing.BuildersRecipe()
        self.assertFalse(testee.IsStarted())
        self.assertTrue(testee.IsLoaded())
        vToolIDs = testee.GetAvailableVToolTypeIDs()
        self.assertTrue(len(vToolIDs) > 1)
        self.assertTrue(cameraVToolUuid in vToolIDs)
        self.assertTrue(formatConverterVToolUuid in vToolIDs)
        self.assertEqual(testee.GetVToolDisplayNameForTypeID(cameraVToolUuid), "Camera")
        self.assertEqual(testee.GetVToolDisplayNameForTypeID(formatConverterVToolUuid), "Image Format Converter")
        testee.AddVTool("MyCamera", cameraVToolUuid);
        self.assertTrue(testee.HasVTool("MyCamera"));
        self.assertFalse(testee.HasVTool("MyCameraNotThereTest"));
        testee.AddVTool("MyConverter", formatConverterVToolUuid);
        self.assertTrue(testee.HasVTool("MyConverter"));
        vToolIdentifier = testee.AddVTool(cameraVToolUuid); #name automatically provided
        self.assertTrue(testee.HasVTool(vToolIdentifier));
        testee.RenameVTool(vToolIdentifier, vToolIdentifier + "NewName")
        self.assertTrue(testee.HasVTool(vToolIdentifier + "NewName"));
        testee.RemoveVTool(vToolIdentifier + "NewName")
        self.assertFalse(testee.HasVTool(vToolIdentifier + "NewName"));
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2,0,0):
            # This is the latest version
            testee.AddOutput("OriginalImage", pylondataprocessing.VariantDataType_PylonImage)
            testee.AddOutput("ConvertedImage", pylondataprocessing.VariantDataType_PylonImage)
            testee.AddOutput("ConvertedImage2", pylondataprocessing.VariantDataType_PylonImage)
        else:
            testee.AddOutput("OriginalImage", "Pylon::DataProcessing::Core::IImage")
            testee.AddOutput("ConvertedImage", "Pylon::DataProcessing::Core::IImage")
            testee.AddOutput("ConvertedImage2", "Pylon::DataProcessing::Core::IImage")
        testee.RenameOutput("ConvertedImage2", "ConvertedImage3")
        self.assertTrue("ConvertedImage3" in testee.GetOutputNames())
        testee.RemoveOutput("ConvertedImage3")
        self.assertFalse("ConvertedImage3" in testee.GetOutputNames())
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2,0,0):
            # This is the latest version
            outputName = testee.AddOutput(pylondataprocessing.VariantDataType_PylonImage)
        else:
            outputName = testee.AddOutput("Pylon::DataProcessing::Core::IImage")
        self.assertTrue(outputName in testee.GetOutputNames())
        testee.RemoveOutput(outputName)
        vToolIdentifiers = testee.GetVToolIdentifiers()
        self.assertTrue("MyCamera" in vToolIdentifiers)
        self.assertTrue("MyConverter" in vToolIdentifiers)
        self.assertEqual(len(vToolIdentifiers), 2)
        self.assertEqual(testee.GetVToolTypeID("MyCamera"), cameraVToolUuid)
        self.assertEqual(testee.GetVToolTypeID("MyConverter"), formatConverterVToolUuid)
        testee.AddConnection("camera_to_converter", "MyCamera.Image", "MyConverter.Image")
        testee.AddConnection("converter_to_output", "MyConverter.Image", "<RecipeOutput>.ConvertedImage", pylondataprocessing.QueueMode_Blocking, 1)
        testee.AddConnection("camera_to_output", "MyCamera.Image", "<RecipeOutput>.OriginalImage")
        connectionIDs = testee.GetConnectionIdentifiers()
        self.assertEqual(len(connectionIDs), 3)
        self.assertTrue("camera_to_converter" in connectionIDs)
        self.assertTrue("converter_to_output" in connectionIDs)
        self.assertTrue("camera_to_output" in connectionIDs)
        self.assertEqual(testee.GetConnectionQueueMode("converter_to_output"), pylondataprocessing.QueueMode_Blocking)
        testee.SetConnectionQueueMode("converter_to_output", pylondataprocessing.QueueMode_Unlimited)
        self.assertEqual(testee.GetConnectionQueueMode("converter_to_output"), pylondataprocessing.QueueMode_Unlimited)
        self.assertEqual(testee.GetConnectionSource("converter_to_output"), "MyConverter.Image")
        self.assertEqual(testee.GetConnectionDestination("converter_to_output"), "<RecipeOutput>.ConvertedImage")
        testee.RenameConnection("converter_to_output", "converter_to_output2");
        self.assertTrue(testee.HasConnection("converter_to_output2"))
        self.assertFalse(testee.HasConnection("converter_to_output"))
        testee.RemoveConnection("converter_to_output2")
        connectionName = testee.AddConnection("MyConverter.Image", "<RecipeOutput>.ConvertedImage", pylondataprocessing.QueueMode_Blocking, 1)
        self.assertTrue(testee.HasConnection(connectionName))
        self.assertEqual(testee.GetConnectionQueueMode(connectionName), pylondataprocessing.QueueMode_Blocking)
        self.assertEqual(testee.GetConnectionMaxQueueSize(connectionName), 1)
        testee.SetConnectionMaxQueueSize(connectionName, 2)
        self.assertEqual(testee.GetConnectionMaxQueueSize(connectionName), 2)
        testee.SetConnectionSettings(connectionName, pylondataprocessing.QueueMode_Unlimited, 3)
        self.assertEqual(testee.GetConnectionQueueMode(connectionName), pylondataprocessing.QueueMode_Unlimited)
        self.assertEqual(testee.GetConnectionMaxQueueSize(connectionName), 3)
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2,0,0):
            # This is the latest version
            testee.AddInput("A", pylondataprocessing.VariantDataType_PylonImage)
        else:
            testee.AddInput("A", "Pylon::DataProcessing::Core::IImage")
        self.assertTrue("A" in testee.GetInputNames())
        testee.RenameInput("A", "B")
        self.assertTrue("B" in testee.GetInputNames())
        testee.RemoveInput("B")
        self.assertFalse("B" in testee.GetInputNames())
        inputName = None
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2,0,0):
            # This is the latest version
            inputName = testee.AddInput(pylondataprocessing.VariantDataType_PylonImage)
        else:
            inputName = testee.AddInput("Pylon::DataProcessing::Core::IImage")
        self.assertTrue(inputName in testee.GetInputNames())
        testee.RemoveInput(inputName)
        self.assertFalse(inputName in testee.GetInputNames())
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'builders_test_save_846bca11_tmp.precipe')
        testee.Save(recipefilename)
        testee2 = pylondataprocessing.Recipe()
        testee2.Load(recipefilename)
        testee2.Unload()
        os.remove(recipefilename)
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(3,1,0):
            testee.SaveAs(pylondataprocessing.RecipeFileFormat_JsonDefault, recipefilename)
            testee2 = pylondataprocessing.Recipe()
            testee2.Load(recipefilename)
            testee2.Unload()
            os.remove(recipefilename)
            testee.SaveAs(pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData, recipefilename)
            testee2 = pylondataprocessing.Recipe()
            testee2.Load(recipefilename)
            testee2.Unload()
            os.remove(recipefilename)
        testee.ResetToEmpty()
 
if __name__ == "__main__":
    unittest.main()
