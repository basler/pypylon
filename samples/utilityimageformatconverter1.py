'''
    Note: Before getting started, Basler recommends reading the Programmer's Guide topic
    in the pylon C++ API documentation that gets installed with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the Migration topic in the pylon C++ API documentation.

    This sample illustrates how to use the image format
    converter class CImageFormatConverter.

    The image format converter accepts all image formats
    produced by Basler camera devices and it is able to
    convert these to a number of output formats.
    The conversion can be controlled by several parameters.
    See the converter class documentation for more details.
'''

from pypylon import pylon
from pypylon import genicam


def show_image(img, message):
    print(message)

    image_array = img.GetArray()
    print(image_array)



def grab_image():
    try:
        camera = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice())

        camera.Open()
        result = camera.GrabOne(100)
        camera.Close()
        return result
    except genicam.GenericException as e:
        print("Could not grab an image: ", e.GetDescription())


try:
    # The image format converter basics.
    # First the image format converter class must be created.
    converter = pylon.ImageFormatConverter()

    # Second the converter must be parameterized.
    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment = "MsbAligned"
    # or alternatively
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


    # Then it can be used to convert input images to
    # the target image format.

    # Grab an image
    image = grab_image()
    show_image(image, "Source Image")

    # Now we can check if conversion is required.
    if (converter.ImageHasDestinationFormat(image)):
        show_image(image, "No conversion needed.")
    else:
        # Convert the image. Note that there are more overloaded Convert methods avilable, e.g.
        # for converting the image from or to a user buffer.
        target_image = converter.Convert(image)
        show_image(target_image, "Converted image.")
except genicam.GenericException as e:
    print("An exception occurred. ", e.GetDescription())
