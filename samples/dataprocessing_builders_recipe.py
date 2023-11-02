# ===============================================================================
# pylon data processing
# Sample using the builder's recipe
# ===============================================================================
import os
num = 2
os.environ["PYLON_CAMEMU"] = "%d" % num
from pypylon import pylondataprocessing
from pypylon import pylon
from pypylon import genicam

import sys

# Number of images to be grabbed.
countOfImagesToGrab = 100

# The exit code of the sample application.
exitCode = 0

cameraVToolUuid = "846bca11-6bf2-4895-88c4-fe038f5a659c";
formatConverterVToolUuid = "4049ea56-3827-4faf-9478-c3ba02e4a0cb";

try:
    # This object is used for collecting the output data.
    resultCollector = pylondataprocessing.GenericOutputObserver()

    # Create a new builder's recipe.
    recipe = pylondataprocessing.BuildersRecipe()

    print("Available vTool types:")
    print(recipe.GetAvailableVToolTypeIDs())
    
    # Use AddVTool to add vTools to the recipe.
    recipe.AddVTool("MyCamera", cameraVToolUuid)
    recipe.AddVTool("MyConverter", formatConverterVToolUuid)

    # Use GetVToolNames() to retrieve a list of all vTools that are currently in the recipe.    
    print("vTools in recipe:")
    vToolIdentifiers = recipe.GetVToolIdentifiers()
    print(vToolIdentifiers)
    for identifier in vToolIdentifiers:
        print("vTool Name '{0}' : type: '{1}'\n".format(identifier, recipe.GetVToolTypeID(identifier)))

    # Use AddOutput() to add outputs to your recipe.
    recipe.AddOutput("OriginalImage", "Pylon::DataProcessing::Core::IImage");
    recipe.AddOutput("ConvertedImage", "Pylon::DataProcessing::Core::IImage");

    # Use AddConnection() to create connections between vTool pins and/or the inputs or outputs of the recipe.
    recipe.AddConnection("camera_to_converter", "MyCamera.Image", "MyConverter.Image");
    recipe.AddConnection("converter_to_output", "MyConverter.Image", "<RecipeOutput>.ConvertedImage");
    recipe.AddConnection("camera_to_output", "MyCamera.Image", "<RecipeOutput>.OriginalImage");

    # Use GetConnectionNames() to retrieve a list of all connections that are currently in the recipe.
    print("Connections in recipe:")
    print(recipe.GetConnectionIdentifiers())

    # Register the helper object for receiving all output data.
    recipe.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append);

    # Change the output format of the image format converter
    recipe.GetParameter("MyConverter/@vTool/OutputPixelFormat").SetValue("BGR8Packed")

    # Now, we can run the recipe as usual.
    recipe.Start();

    for i in range(0, countOfImagesToGrab):
        if resultCollector.GetWaitObject().Wait(5000):
            # Get the recipe dependend dictionary; key is the pin name and the value is a variant object
            result = resultCollector.RetrieveResult()
            # Show some image information
            variant = result["OriginalImage"]
            if not variant.HasError():
                # Print result data
                print("OriginalImage")
                pylonimage = variant.ToImage()
                print("SizeX: ", pylonimage.Width)
                print("SizeY: ", pylonimage.Height)
                img = pylonimage.Array
                print("Pixel Type", pylonimage.PixelType)
                pylonimage.Release()
            else:
                print("Error: " + variant.GetErrorDescription())
            variant = result["ConvertedImage"]
            if not variant.HasError():
                # Print result data
                print("ConvertedImage")
                pylonimage = variant.ToImage()
                print("SizeX: ", pylonimage.Width)
                print("SizeY: ", pylonimage.Height)
                img = pylonimage.Array
                print("Pixel Type", pylonimage.PixelType)
                pylonimage.Release()
                print()
            else:
                print("Error: " + variant.GetErrorDescription())
        else:
            print("Result timeout")
            break

    # Stop the processing.
    recipe.Stop()

    # Release everything.
    recipe.ResetToEmpty();
    
except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1
except Exception as e:
    print("An unexpected exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)
