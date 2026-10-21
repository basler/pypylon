"""\
This unit test checks the BuildersRecipe API of pylondataprocessing.

It builds a recipe programmatically: adding, renaming and removing vTools,
outputs, inputs and connections, and saving/loading the result.
"""
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import pylondataprocessing
from pypylon import pylon
import unittest
import json
import os
import tempfile

CAMERA_VTOOL_UUID = "846bca11-6bf2-4895-88c4-fe038f5a659c".upper()
FORMAT_CONVERTER_VTOOL_UUID = "4049ea56-3827-4faf-9478-c3ba02e4a0cb".upper()


class BuildersRecipeTestSuite(PylonDataProcessingTestCase):

    # ------------------------------------------------------------------
    # Building a recipe from scratch
    # ------------------------------------------------------------------

    def test_init(self):
        """A BuildersRecipe can add, rename and remove vTools, outputs, inputs and connections."""
        with pylondataprocessing.BuildersRecipe() as recipe:
            self.assertFalse(recipe.IsStarted())
            self.assertTrue(recipe.IsLoaded())
            vtool_type_ids = recipe.GetAvailableVToolTypeIDs()
            self.assertTrue(len(vtool_type_ids) > 1)
            self.assertTrue(CAMERA_VTOOL_UUID in vtool_type_ids)
            self.assertTrue(FORMAT_CONVERTER_VTOOL_UUID in vtool_type_ids)
            self.assertEqual(recipe.GetVToolDisplayNameForTypeID(CAMERA_VTOOL_UUID), "Camera")
            self.assertEqual(
                recipe.GetVToolDisplayNameForTypeID(FORMAT_CONVERTER_VTOOL_UUID), "Image Format Converter")

            # vTools
            recipe.AddVTool("MyCamera", CAMERA_VTOOL_UUID)
            self.assertTrue(recipe.HasVTool("MyCamera"))
            self.assertFalse(recipe.HasVTool("MyCameraNotThereTest"))
            recipe.AddVTool("MyConverter", FORMAT_CONVERTER_VTOOL_UUID)
            self.assertTrue(recipe.HasVTool("MyConverter"))
            vtool_identifier = recipe.AddVTool(CAMERA_VTOOL_UUID)  # name automatically provided
            self.assertTrue(recipe.HasVTool(vtool_identifier))
            recipe.RenameVTool(vtool_identifier, vtool_identifier + "NewName")
            self.assertTrue(recipe.HasVTool(vtool_identifier + "NewName"))
            recipe.RemoveVTool(vtool_identifier + "NewName")
            self.assertFalse(recipe.HasVTool(vtool_identifier + "NewName"))

            # Outputs
            if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2, 0, 0):
                # This is the latest version.
                recipe.AddOutput("OriginalImage", pylondataprocessing.VariantDataType_PylonImage)
                recipe.AddOutput("ConvertedImage", pylondataprocessing.VariantDataType_PylonImage)
                recipe.AddOutput("ConvertedImage2", pylondataprocessing.VariantDataType_PylonImage)
            else:
                recipe.AddOutput("OriginalImage", "Pylon::DataProcessing::Core::IImage")
                recipe.AddOutput("ConvertedImage", "Pylon::DataProcessing::Core::IImage")
                recipe.AddOutput("ConvertedImage2", "Pylon::DataProcessing::Core::IImage")
            recipe.RenameOutput("ConvertedImage2", "ConvertedImage3")
            self.assertTrue("ConvertedImage3" in recipe.GetOutputNames())
            recipe.RemoveOutput("ConvertedImage3")
            self.assertFalse("ConvertedImage3" in recipe.GetOutputNames())
            if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2, 0, 0):
                # This is the latest version.
                output_name = recipe.AddOutput(pylondataprocessing.VariantDataType_PylonImage)
            else:
                output_name = recipe.AddOutput("Pylon::DataProcessing::Core::IImage")
            self.assertTrue(output_name in recipe.GetOutputNames())
            recipe.RemoveOutput(output_name)
            vtool_identifiers = recipe.GetVToolIdentifiers()
            self.assertTrue("MyCamera" in vtool_identifiers)
            self.assertTrue("MyConverter" in vtool_identifiers)
            self.assertEqual(len(vtool_identifiers), 2)
            self.assertEqual(recipe.GetVToolTypeID("MyCamera"), CAMERA_VTOOL_UUID)
            self.assertEqual(recipe.GetVToolTypeID("MyConverter"), FORMAT_CONVERTER_VTOOL_UUID)

            # Connections
            recipe.AddConnection("camera_to_converter", "MyCamera.Image", "MyConverter.Image")
            recipe.AddConnection(
                "converter_to_output", "MyConverter.Image", "<RecipeOutput>.ConvertedImage",
                pylondataprocessing.QueueMode_Blocking, 1)
            recipe.AddConnection("camera_to_output", "MyCamera.Image", "<RecipeOutput>.OriginalImage")
            connection_identifiers = recipe.GetConnectionIdentifiers()
            self.assertEqual(len(connection_identifiers), 3)
            self.assertTrue("camera_to_converter" in connection_identifiers)
            self.assertTrue("converter_to_output" in connection_identifiers)
            self.assertTrue("camera_to_output" in connection_identifiers)
            self.assertEqual(
                recipe.GetConnectionQueueMode("converter_to_output"), pylondataprocessing.QueueMode_Blocking)
            recipe.SetConnectionQueueMode("converter_to_output", pylondataprocessing.QueueMode_Unlimited)
            self.assertEqual(
                recipe.GetConnectionQueueMode("converter_to_output"), pylondataprocessing.QueueMode_Unlimited)
            self.assertEqual(recipe.GetConnectionSource("converter_to_output"), "MyConverter.Image")
            self.assertEqual(recipe.GetConnectionDestination("converter_to_output"), "<RecipeOutput>.ConvertedImage")
            recipe.RenameConnection("converter_to_output", "converter_to_output2")
            self.assertTrue(recipe.HasConnection("converter_to_output2"))
            self.assertFalse(recipe.HasConnection("converter_to_output"))
            recipe.RemoveConnection("converter_to_output2")
            connection_name = recipe.AddConnection(
                "MyConverter.Image", "<RecipeOutput>.ConvertedImage", pylondataprocessing.QueueMode_Blocking, 1)
            self.assertTrue(recipe.HasConnection(connection_name))
            self.assertEqual(recipe.GetConnectionQueueMode(connection_name), pylondataprocessing.QueueMode_Blocking)
            self.assertEqual(recipe.GetConnectionMaxQueueSize(connection_name), 1)
            recipe.SetConnectionMaxQueueSize(connection_name, 2)
            self.assertEqual(recipe.GetConnectionMaxQueueSize(connection_name), 2)
            recipe.SetConnectionSettings(connection_name, pylondataprocessing.QueueMode_Unlimited, 3)
            self.assertEqual(recipe.GetConnectionQueueMode(connection_name), pylondataprocessing.QueueMode_Unlimited)
            self.assertEqual(recipe.GetConnectionMaxQueueSize(connection_name), 3)

            # Inputs
            if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2, 0, 0):
                # This is the latest version.
                recipe.AddInput("A", pylondataprocessing.VariantDataType_PylonImage)
            else:
                recipe.AddInput("A", "Pylon::DataProcessing::Core::IImage")
            self.assertTrue("A" in recipe.GetInputNames())
            recipe.RenameInput("A", "B")
            self.assertTrue("B" in recipe.GetInputNames())
            recipe.RemoveInput("B")
            self.assertFalse("B" in recipe.GetInputNames())
            if pylondataprocessing.GetVersion() >= pylon.VersionInfo(2, 0, 0):
                # This is the latest version.
                input_name = recipe.AddInput(pylondataprocessing.VariantDataType_PylonImage)
            else:
                input_name = recipe.AddInput("Pylon::DataProcessing::Core::IImage")
            self.assertTrue(input_name in recipe.GetInputNames())
            recipe.RemoveInput(input_name)
            self.assertFalse(input_name in recipe.GetInputNames())

        # Save / load round-trip
        this_dir = os.path.dirname(__file__)
        recipe_filename = os.path.join(this_dir, 'builders_test_save_846bca11_tmp.precipe')
        recipe.Save(recipe_filename)
        loaded_recipe = pylondataprocessing.Recipe()
        loaded_recipe.Load(recipe_filename)
        loaded_recipe.Unload()
        os.remove(recipe_filename)
        if pylondataprocessing.GetVersion() >= pylon.VersionInfo(3, 1, 0):
            recipe.SaveAs(pylondataprocessing.RecipeFileFormat_JsonDefault, recipe_filename)
            loaded_recipe = pylondataprocessing.Recipe()
            loaded_recipe.Load(recipe_filename)
            loaded_recipe.Unload()
            os.remove(recipe_filename)
            recipe.SaveAs(pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData, recipe_filename)
            loaded_recipe = pylondataprocessing.Recipe()
            loaded_recipe.Load(recipe_filename)
            loaded_recipe.Unload()
            os.remove(recipe_filename)
        recipe.ResetToEmpty()

    # ------------------------------------------------------------------
    # SaveAs overloads
    # ------------------------------------------------------------------

    @unittest.skipUnless(
        pylondataprocessing.GetVersion() >= pylon.VersionInfo(3, 1, 0),
        "SaveAs requires data processing 3.1+",
    )
    def test_save_as_without_detail_level(self):
        """The original two-argument SaveAs overload preserves recipe outputs."""
        with tempfile.TemporaryDirectory() as directory:
            recipe_filename = os.path.join(directory, "default.precipe")
            with pylondataprocessing.BuildersRecipe() as recipe:
                recipe.AddOutput("Image", pylondataprocessing.VariantDataType_PylonImage)
                for file_format in (
                    pylondataprocessing.RecipeFileFormat_JsonDefault,
                    pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData,
                ):
                    with self.subTest(file_format=file_format):
                        recipe.SaveAs(file_format, recipe_filename)
                        with pylondataprocessing.Recipe() as loaded_recipe:
                            loaded_recipe.Load(recipe_filename)
                            self.assertIn("Image", loaded_recipe.GetOutputNames())

    @unittest.skipUnless(
        pylondataprocessing.GetVersion() >= pylon.VersionInfo(6, 0, 0),
        "SaveAs with a detail level requires data processing 6.0+",
    )
    def test_save_as_with_detail_level(self):
        """Both file formats persist the requested detail level and remain loadable."""
        with tempfile.TemporaryDirectory() as directory:
            recipe_filename = os.path.join(directory, "detail.precipe")
            with pylondataprocessing.BuildersRecipe() as recipe:
                recipe.AddOutput("Image", pylondataprocessing.VariantDataType_PylonImage)
                for file_format in (
                    pylondataprocessing.RecipeFileFormat_JsonDefault,
                    pylondataprocessing.RecipeFileFormat_JsonCompressedBinaryData,
                ):
                    for detail_level, expected_detail_level in (
                        (pylondataprocessing.Detail_Complete, "Complete"),
                        (pylondataprocessing.Detail_Lean, "Lean"),
                    ):
                        with self.subTest(file_format=file_format, detail_level=detail_level):
                            recipe.SaveAs(file_format, recipe_filename, detail_level)
                            with open(recipe_filename, encoding="utf-8-sig") as recipe_file:
                                saved_recipe = json.load(recipe_file)
                            self.assertEqual(
                                saved_recipe["PylonMetaData"]["DetailLevel"], expected_detail_level
                            )
                            with pylondataprocessing.Recipe() as loaded_recipe:
                                loaded_recipe.Load(recipe_filename)
                                self.assertIn("Image", loaded_recipe.GetOutputNames())

    def test_typed_parameter_methods_are_exposed(self):
        """BuildersRecipe inherits typed parameter access methods from Recipe."""
        recipe = pylondataprocessing.BuildersRecipe()
        self.assertTrue(hasattr(recipe, "ContainsParameter"))
        self.assertTrue(hasattr(recipe, "GetParameter"))


if __name__ == "__main__":
    unittest.main()
