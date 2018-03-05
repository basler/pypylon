from pypylon import pylon
from pypylon import genicam
import numpy

IMAGES_TO_GRAB = 50000
exitCode = 0

while True:
    camera = pylon.InstantCamera(
        pylon.TlFactory.GetInstance().CreateFirstDevice())

    camera.Open()

    # Print the model name of the camera.
    print("Using device ", camera.GetDeviceInfo().GetModelName())

    camera.MaxNumBuffer = 2
    try:
        camera.Gain = camera.Gain.Max
    except genicam.LogicalErrorException:
        camera.GainRaw = camera.GainRaw.Max
    camera.Width = camera.Width.Max
    camera.Height = camera.Height.Max
    # camera.ExposureTime = camera.ExposureTime.Min
    camera.PixelFormat = "Mono12"

    # Start the grabbing of IMAGES_TO_GRAB images.
    # The camera device is parameterized with a default configuration which
    # sets up free-running continuous acquisition.
    camera.StartGrabbingMax(IMAGES_TO_GRAB)

    # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    # when IMAGES_TO_GRAB images have been retrieved.
    try:
        while camera.IsGrabbing():
            result = camera.RetrieveResult(
                5000,
                pylon.TimeoutHandling_ThrowException)
            print(result.GrabSucceeded())
            # Image grabbed successfully?
            if result.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", result.Width)
                print("SizeY: ", result.Height)
                print(pylon.IsPacked(result.PixelType))
                print("Mean Gray value:", numpy.mean(result.Array[0:20, 0]))
                # Display the grabbed image.
                # pylon.DisplayImage(1, result)
                result.Release()

            else:
                print("Error: ", result.GetErrorCode(), result.GetErrorDescription())

    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.", e.GetDescription())

    camera.Close()
