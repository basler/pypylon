#    Note: Before getting started, Basler recommends reading the Programmer's Guide topic
#    in the pylon C++ API documentation that gets installed with pylon.
#    If you are upgrading to a higher major version of pylon, Basler also
#    strongly recommends reading the Migration topic in the pylon C++ API documentation.

#    This sample illustrates how to use the image format
#    converter class CImageFormatConverter.

#    The image format converter accepts all image formats
#    produced by Basler camera devices and it is able to
#    convert these to a number of output formats.
#    The conversion can be controlled by several parameters.
#    See the converter class documentation for more details.

from pypylon import pylon
from pypylon import genicam


# This is a helper function for showing an image on the screen if Windows is used,
# and for printing the first bytes of the image.
def show_image(image, message):
    print(message)
    pBytes = image.Array
    print("Bytes of the image: \n")
    print(pBytes)


try:
    # Create the converter and set parameters.
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_Mono8

    # Try to get a grab result for demonstration purposes.
    print("Waiting for an image to be grabbed.")
    try:
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        grabResult = camera.GrabOne(1000)
        show_image(grabResult, "Grabbed image.")
        targetImage = pylon.PylonImage.Create(pylon.PixelType_Mono8, grabResult.GetWidth(), grabResult.GetHeight());
        print(converter.IsSupportedOutputFormat(pylon.PixelType_Mono8))
        # Now we can check if conversion is required.
        if converter.ImageHasDestinationFormat(grabResult):
            # No conversion is needed. It can be skipped for saving processing
            # time.
            show_image(grabResult, "Grabbed image.")

        else:
            # Conversion is needed.
            show_image(grabResult, "Grabbed image.")

            show_image(targetImage, "Converted image.")

    except genicam.GenericException as e:
        print("Could not grab an image: ", e.GetDescription())
except genicam.GenericException as e:
    print("An exception occurred. ", e.GetDescription())
