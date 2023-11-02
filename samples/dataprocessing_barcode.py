# ===============================================================================
# pylon data processing
# Sample using the Barcode vTool (license required)
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

try:
    # This object is used for collecting the output data.
    resultCollector = pylondataprocessing.GenericOutputObserver()
    
    # Create a recipe representing a design created using
    # the pylon Viewer Workbench.
    recipe = pylondataprocessing.Recipe()
    
    # Load the recipe file.
    thisdir = os.path.dirname(__file__)
    recipefilename = os.path.join(thisdir, 'dataprocessing_barcode.precipe')
    recipe.Load(recipefilename)

    # Register the helper object for receiving all output data.
    recipe.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append);

    # Allocate the required resources. This includes the camera device.
    recipe.PreAllocateResources()

    # Tell the camemu camera device where the barcode images are located
    imagespath = os.path.join(thisdir, 'images', 'barcode')
    recipe.GetParameter("MyCamera/@CameraDevice/ImageFilename").SetValue(imagespath);

    # Start the processing. The recipe is triggered internally
    # by the camera vTool for each image.
    recipe.Start()

    for i in range(0, countOfImagesToGrab):
        if resultCollector.GetWaitObject().Wait(5000):
            # Get the recipe dependend dictionary; key is the pin name and the value is a variant object
            result = resultCollector.RetrieveResult()
            # Show some image information
            variant = result["Image"]
            if not variant.HasError():
                # Print result data
                pylonimage = variant.ToImage()
                print("SizeX: ", pylonimage.Width)
                print("SizeY: ", pylonimage.Height)
                img = pylonimage.Array
                print("Gray value of first pixel: ", img[0, 0])
                pylonimage.Release()
            else:
                print("Error: " + variant.GetErrorDescription())
            # Print the barcodes
            variant = result["Barcodes"]
            if not variant.HasError():
                # Print result data
                for barcodeIndex in range(0, variant.NumArrayValues):
                    print(variant.GetArrayValue(barcodeIndex).ToString())
            else:
                print("Error: " + variant.GetErrorDescription())
        else:
            print("Result timeout")
            break

    # Stop the processing.
    recipe.Stop()
    
    # Optionally, deallocate resources.
    recipe.DeallocateResources()
    
    # Unload the recipe and free all created vTools
    recipe.Unload()
    
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
