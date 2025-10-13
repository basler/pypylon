# ===============================================================================
#    This sample illustrates how to grab and process images using
#    the SmartInstantCamera class.
#
#    The SmartInstantCamera class convenient access to a camera device
#    and pylon data processing using a recipe as appended processing stage.
#    Extends the Instant Camera class.
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
    # Load the recipe file.
    thisdir = os.path.dirname(__file__)
    recipefilename = os.path.join(thisdir, 'dataprocessing_smartcamera.precipe')

    # Create an instant camera object with the camera device found first.
    camera = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(), recipefilename)
    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    # demonstrate some feature access
    new_width = camera.Width.Value - camera.Width.Inc
    if new_width >= camera.Width.Min:
        camera.Width.Value = new_width

    # The parameter MaxNumBuffer can be used to control the count of buffers
    # allocated for grabbing. The default value of this parameter is 10.
    camera.MaxNumBuffer.Value = 5

    # Start the grabbing of c_countOfImagesToGrab images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfImagesToGrab)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab images have been retrieved.
    while camera.IsGrabbing():
        # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        
        # Image grabbed successfully?
        if result.GrabResult.GrabSucceeded():
            # Access the image data.
            print("SizeX: ", result.GrabResult.Width)
            print("SizeY: ", result.GrabResult.Height)
            img = result.GrabResult.Array
            print("Gray value of first pixel: ", img[0, 0])

            # Iterate over all output pins in the container.
            # Container is a dictionary. Key is of type string and the value of type Variant.
            print("Processing recipe outputs:")
            for key, variant in result.Container.items():
                # Key contains the name of the recipe output pin.
                print(f"Output pin '{key}':")
                if not variant.HasError():
                    # Print result data.
                    # Check if variant is an array.
                    if variant.IsArray():
                        print(f"  Array with {variant.GetNumArrayValues()} items:")
                        data_array = variant.ToData() #ToData returns the data inside the variant as corresponding python type.
                        for i, item in enumerate(data_array):
                            if variant.GetDataType() == pylondataprocessing.VariantDataType_Region:
                                print(f"    [{i}] Region with {item.GetDataSize()} bytes")
                            elif variant.GetDataType() == pylondataprocessing.VariantDataType_PylonImage:
                                print(f"    [{i}] Image {item.GetWidth()}x{item.GetHeight()}")
                            else:
                                print(f"    [{i}] Data: {item}")
                    else:
                        data = variant.ToData() #ToData returns the data inside the variant as corresponding python type.
                        if variant.GetDataType() == pylondataprocessing.VariantDataType_Region:
                            print(f"  Region with {data.GetDataSize()} bytes")
                        elif variant.GetDataType() == pylondataprocessing.VariantDataType_PylonImage:
                            print(f"  Image {data.GetWidth()}x{data.GetHeight()}")
                        else:
                            print(f"  Data: {data}")
                else:
                    print(f"  Error: {variant.GetErrorDescription()}")
        else:
            print("Error: ", result.GrabResult.ErrorCode, result.GrabResult.ErrorDescription)

        result.Release()
    camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)
