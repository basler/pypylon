# ===============================================================================
#    This sample illustrates how to grab and process data using the CInstantCamera class.
#    The data is grabbed and processed asynchronously, i.e.,
#    while the application is processing a buffer, the acquisition of the next buffer is done
#    in parallel.
#
#    Utilizes the API for accessing GenICam Generic Data Container (GenDC).
#    This will allow the use of, e.g., Basler blaze 3D cameras.
# ===============================================================================
from pypylon import pylon
from pypylon import genicam

import sys

# Number of results to be grabbed.
countOfResultsToGrab = 100

# The exit code of the sample application.
exitCode = 0

try:
    # Create an instant camera object with the camera device found first.
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
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

    # Start the grabbing of c_countOfImagesToGrab grab results.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(countOfResultsToGrab)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when c_countOfImagesToGrab grab results have been retrieved.
    while camera.IsGrabbing():
        # Wait for grabbed data and then retrieve it. A timeout of 5000 ms is used.
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        # Data grabbed successfully?
        if grabResult.GrabSucceeded():
            # Get the grab result as a PylonDataContainer, e.g. when working with 3D cameras.
            pylonDataContainer = grabResult.GetDataContainer();
            print("Component Count: ", pylonDataContainer.DataComponentCount);
            # Access data components if the component type indicates image data
            for componentIndex in range(pylonDataContainer.DataComponentCount):
                pylonDataComponent = pylonDataContainer.GetDataComponent(componentIndex);
                if pylonDataComponent.ComponentType == pylon.ComponentType_Intensity:
                    # Access the component data.
                    print("PixelType: ", pylonDataComponent.PixelType)
                    print("SizeX: ", pylonDataComponent.Width)
                    print("SizeY: ", pylonDataComponent.Height)
                    print("OffsetX: ", pylonDataComponent.OffsetX)
                    print("OffsetY: ", pylonDataComponent.OffsetY)
                    print("PaddingX: ", pylonDataComponent.PaddingX)
                    print("DataSize: ", pylonDataComponent.DataSize)
                    print("TimeStamp: ", pylonDataComponent.TimeStamp)
                    img = pylonDataComponent.Array
                    print("Gray value of first pixel: ", img[0, 0])
                pylonDataComponent.Release()
            pylonDataContainer.Release()
        else:
            print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
        grabResult.Release()
    camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)
