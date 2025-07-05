// Utility_ImageLoadAndSave.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to load and save images.

    The CImagePersistence class provides static functions for
    loading and saving images. It uses the image
    class related interfaces IImage and IReusableImage of pylon.

    IImage can be used to access image properties and image buffer.
    Therefore, it is used when saving images. In addition to that images can also
    be saved by passing an image buffer and the corresponding properties.

    The IReusableImage interface extends the IImage interface to be able to reuse
    the resources of the image to represent a different image. The IReusableImage
    interface is used when loading images.

    The CPylonImage and CPylonBitmapImage image classes implement the
    IReusableImage interface. These classes can therefore be used as targets
    for loading images.

    The gab result smart pointer classes provide a cast operator to the IImage
    interface. This makes it possible to pass a grab result directly to the
    function that saves images to disk.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#include "../include/SampleImageCreator.h"

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using cout.
using namespace std;


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object with the camera device found first.
        CInstantCamera Camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << Camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Define some constants.
        const uint32_t cWidth = 640;
        const uint32_t cHeight = 480;

        // Saving images using the CImagePersistence class.
        {
            // Create a sample image.
            CPylonImage imageRGB16packed = SampleImageCreator::CreateMandelbrotFractal( PixelType_RGB16packed, cWidth, cHeight );

            // If required the image is automatically converted to a new image and then saved.
            // An image with a bit depth higher than 8 Bit is stored with 16 Bit bit depth
            // if supported by the image file format. In this case the pixel data is MSB aligned.
            // If more control over the conversion is required then the CImageFormatConverter class
            // can be used to convert the input image before saving it (not shown).
            CImagePersistence::Save( ImageFileFormat_Tiff, "MandelbrotFractal.tiff", imageRGB16packed );

            cout << "The image " << (CImagePersistence::CanSaveWithoutConversion( ImageFileFormat_Tiff, imageRGB16packed ) ? "can" : "can not")
                << " be saved without conversion as tiff." << endl;

#ifdef PYLON_WIN_BUILD
            // The CPylonImage and the CPylonBitmapImage classes provide a member function
            // for saving images for convenience. This function calls CImagePersistence::Save().
            imageRGB16packed.Save( ImageFileFormat_Bmp, "MandelbrotFractal.bmp" );

            // CanSaveWithoutConversion() can be used to check whether a conversion is performed when saving the image.
            cout << "The image " << (CImagePersistence::CanSaveWithoutConversion( ImageFileFormat_Bmp, imageRGB16packed ) ? "can" : "can not")
                << " be saved without conversion as bmp." << endl;
#endif

            // Additionally it is possible to save image data that is not held by an image class.
            // For demonstration purposes only, the buffer and the image properties from the sample image are used here.
            EPixelType pixelType = imageRGB16packed.GetPixelType();
            uint32_t width = imageRGB16packed.GetWidth();
            uint32_t height = imageRGB16packed.GetHeight();
            size_t paddingX = imageRGB16packed.GetPaddingX();
            EImageOrientation orientation = imageRGB16packed.GetOrientation();
            size_t bufferSize = imageRGB16packed.GetImageSize();
            void* buffer = imageRGB16packed.GetBuffer();

            CImagePersistence::Save(
                ImageFileFormat_Png,
                "MandelbrotFractal.png",
                buffer,
                bufferSize,
                pixelType,
                width,
                height,
                paddingX,
                orientation );
        }


        // Loading images.
        {
            // Create pylon images.
            CPylonImage imageRGB16packedFromTiff;
            CPylonImage imageBGR8packedFromBmp;

            // Load the tiff image directly via the ImageFile interface.
            CImagePersistence::Load( "MandelbrotFractal.tiff", imageRGB16packedFromTiff );
            cout << "The pixel type of the image is " << (imageRGB16packedFromTiff.GetPixelType() == PixelType_RGB16packed ? "" : "not ")
                << "RGB16packed." << endl;

#ifdef PYLON_WIN_BUILD
            // The CPylonImage and the CPylonBitmapImage classes provide a member function
            // for loading images for convenience. This function calls CImagePersistence::Load().
            imageBGR8packedFromBmp.Load( "MandelbrotFractal.bmp" );

            // The format of the loaded image from the bmp file is BGR8packed instead of the original RGB16packed format because
            // it had to be converted for saving it in the bmp format.
            cout << "The pixel type of the image is " << (imageBGR8packedFromBmp.GetPixelType() == PixelType_BGR8packed ? "" : "not ")
                << "BGR8packed." << endl;
#endif

        }

//JPEG handling is only supported on windows
#ifdef PYLON_WIN_BUILD
        // Selecting the image quality when saving in JPEG format.
        {
            // Create a sample image.
            CPylonImage imageRGB8packed = SampleImageCreator::CreateMandelbrotFractal( PixelType_RGB8packed, cWidth, cHeight );

            // The JPEG image quality can be adjusted in the range from 0 to 100.
            CImagePersistenceOptions additionalOptions;
            // Set the lowest quality value.
            additionalOptions.SetQuality( 0 );

            // Save the image.
            CImagePersistence::Save( ImageFileFormat_Jpeg, "MandelbrotFractal_0.jpg", imageRGB8packed, &additionalOptions );

            // Set the highest quality value.
            additionalOptions.SetQuality( 100 );

            // Save the image.
            CImagePersistence::Save( ImageFileFormat_Jpeg, "MandelbrotFractal_100.jpg", imageRGB8packed, &additionalOptions );
        }
#endif

        // Saving grabbed images.
        {
            // Try to get a grab result.
            cout << endl << "Waiting for an image to be grabbed." << endl;
            try
            {
                // This smart pointer will receive the grab result data.
                CGrabResultPtr ptrGrabResult;
                
                if (Camera.GrabOne( 1000, ptrGrabResult ))
                {
                    // The pylon grab result smart pointer classes provide a cast operator to the IImage
                    // interface. This makes it possible to pass a grab result directly to the
                    // function that saves an image to disk.
                    CImagePersistence::Save( ImageFileFormat_Png, "GrabbedImage.png", ptrGrabResult );
                }
            }
            catch (const GenericException& e)
            {

                cerr << "Could not grab an image: " << endl
                    << e.GetDescription() << endl;
            }
        }
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
            << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}
