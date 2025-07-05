// Utility_Image.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to use the pylon image classes CPylonImage and CPylonBitmapImage.
    CPylonImage supports handling image buffers of the various existing pixel types.
    CPylonBitmapImage can be used to easily create Windows bitmaps for displaying images.

    Additionally, there are two image class related interfaces in pylon IImage and IReusableImage.
    IImage can be used to access image properties and image buffer.
    The IReusableImage interface extends the IImage interface to be able to reuse the
    resources of the image to represent a different image.
    Both CPylonImage and CPylonBitmapImage implement the IReusableImage interface.

    The pylon grab result class CGrabResultPtr provides a cast operator to the IImage
    interface. This eases the use of the grab result together with the image classes.
*/

#include <iomanip>
// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

#include "../include/SampleImageCreator.h"

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using cout.
using namespace std;


// This is a helper function for printing image properties.
void PrintImageProperties( IImage& image )
{
    cout
        << "Buffer: " << image.GetBuffer()
        << " Image Size: " << image.GetImageSize()
        << " Width: " << image.GetWidth()
        << " Height: " << image.GetHeight()
        << " Unique: " << image.IsUnique()
        << endl;
}


// This is a helper function for showing an image on the screen if Windows is used,
// and for printing the first bytes of the image.
void ShowImage( IImage& image, const char* message = NULL )
{
#ifdef PYLON_WIN_BUILD
    // Display the image.
    Pylon::DisplayImage( 1, image );
#endif

    if (message)
    {
        cout << endl << message << " ";
    }

    // store state of cout
    std::ios state( NULL );
    state.copyfmt( cout );

    const uint8_t* pBytes = reinterpret_cast<const uint8_t*>(image.GetBuffer());
    cout << endl << "First six bytes of the image: " << endl;
    for (unsigned int i = 0; i < 6; ++i)
    {
        cout << "0x" << hex << setfill( '0' ) << setw( 2 ) << unsigned( pBytes[i] ) << " ";
    }
    cout << endl;

    // restore state of cout
    cout.copyfmt( state );

    cerr << "Press enter to continue." << endl;
    while (cin.get() != '\n');
}


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
        const uint32_t cPadding = 10;
        const uint8_t cSampleGrayValue = 160;

        // The CPylonImage basics.
        {
            // Create a pylon image with the given properties.
            CPylonImage imageMono8( CPylonImage::Create( PixelType_Mono8, cWidth, cHeight ) );
            cout << "The properties of the newly created image." << endl;
            PrintImageProperties( imageMono8 );

            // The image class allocates a buffer large enough to hold the image.
            // We can use it for example to fill it with a test pattern.
            uint32_t width = imageMono8.GetWidth();
            uint32_t height = imageMono8.GetHeight();
            uint8_t* buffer = static_cast<uint8_t*>(imageMono8.GetBuffer());
            uint8_t* p = buffer;
            for (uint32_t y = 0; y < height; ++y)
            {
                for (uint32_t x = 0; x < width; ++x, ++p)
                {
                    *p = (uint8_t) ((x + y) % 256);
                }
            }

            // Show the image on the screen in a separate window.
            ShowImage( imageMono8, "Created image." );

            // If the pylon image object is copied or assigned then no image data copy is made.
            // All objects reference the same buffer now. The image properties have been copied though.
            // The IsUnique() method can be used to check whether a buffer is
            // referenced by multiple pylon image objects.
            CPylonImage sameImageMono8A( imageMono8 );
            CPylonImage sameImageMono8B = imageMono8;
            cout << endl << "After assignment multiple images reference the same data." << endl;
            PrintImageProperties( imageMono8 );
            PrintImageProperties( sameImageMono8A );
            PrintImageProperties( sameImageMono8B );

            // The CopyImage method can be used to create a full copy of an image.
            CPylonImage copiedImage;
            copiedImage.CopyImage( imageMono8 );
            cout << endl << "The properties of a full copy of the test image." << endl;
            PrintImageProperties( copiedImage );

            // The Release() method can be used to release any data.
            // The object sameImageMono8B is now empty.
            // No buffer is allocated.
            sameImageMono8B.Release();
            cout << endl << "Assigned to image object after releasing the image data." << endl;
            PrintImageProperties( sameImageMono8B );

            // A newly created image object is empty.
            CPylonImage reusedImage;
            cout << endl << "A newly created image object." << endl;
            PrintImageProperties( reusedImage );

            // The Reset() method can be used to reset the image properties
            // and allocate a new buffer if required.
            reusedImage.Reset( PixelType_Mono8, cWidth, cHeight );
            cout << "After resetting the image properties. A new Buffer is allocated." << endl;
            PrintImageProperties( reusedImage );

            // Reset() never decreases the allocated buffer size if the
            // new image fits into the current buffer.
            // The new image is smaller and therefore the buffer is reused.
            reusedImage.Reset( PixelType_Mono8, cWidth / 2, cHeight );
            cout << "After resetting the image properties to a smaller image. The buffer is reused." << endl;
            PrintImageProperties( reusedImage );

            // A new buffer is allocated because the old buffer is
            // too small for the new image.
            reusedImage.Reset( PixelType_Mono8, cWidth * 2, cHeight );
            cout << "After resetting the image properties to a larger image." << endl << "A new Buffer is allocated." << endl;
            PrintImageProperties( reusedImage );

            // The imageMono8 and sameImageMono8A objects still reference the
            // same image. Because of this the buffer referenced by sameImageMono8A
            // can't be reused. A new buffer is allocated.
            sameImageMono8A.Reset( PixelType_Mono8, cWidth, cHeight );
            cout << endl << "After resetting the image properties while the image data is referenced by another image. A new Buffer is allocated." << endl;
            PrintImageProperties( sameImageMono8A );

            // For advanced use cases additional line padding and the image orientation can be defined, too.
            sameImageMono8A.Reset( PixelType_Mono8, cWidth, cHeight, cPadding, ImageOrientation_TopDown );
            cout << endl << "After resetting the image properties with additional padding." << endl;
            PrintImageProperties( sameImageMono8A );

            // The image objects are destroyed here and the buffers are deleted.
            // An allocated image buffer is deleted if it is not referenced
            // anymore by a pylon image object.
        }


        // The CPylonImage and user buffers.
        {
            // Create pylon images.
            CPylonImage imageA;
            CPylonImage imageB;

            // Create a buffer for demonstration purposes. This could be a buffer of a 3rd party
            // image library.
            // This example uses a C++ library vector class for buffer allocation for automatic
            // deletion of the buffer.
            vector<uint8_t> buffer( (cWidth + cPadding) * cHeight, cSampleGrayValue );
            size_t bufferSize = buffer.size() * sizeof( buffer[0] );

            // Initializes the image object with the user buffer. Now the image object could be used to
            // interface with other pylon objects more easily, e.g. the image format converter.
            // The user buffer must not be deleted while it is attached to the pylon image object.
            imageA.AttachUserBuffer( &buffer[0], bufferSize, PixelType_Mono8, cWidth, cHeight, cPadding );
            cout << endl << "The properties of an image with an attached user buffer." << endl;
            PrintImageProperties( imageA );

            // The image can be assigned new properties as long as the image fits into the user buffer.
            imageA.Reset( PixelType_Mono8, cWidth / 2, cHeight );
            cout << "After resetting the image properties to a smaller image. The buffer is reused." << endl;
            PrintImageProperties( imageA );

            // This causes an exception because the attached user buffer is too small for the image.
            try
            {
                cout << "Try calling the Reset method when the user buffer is too small for the new image." << endl;
                imageA.Reset( PixelType_Mono8, cWidth * 2, cHeight );
            }
            catch (const GenericException& e)
            {
                cerr << "Expected exception: " << e.GetDescription() << endl;
            }

            // The CopyImage method can be used to create a full copy of the provided image.
            imageB.CopyImage( &buffer[0], bufferSize, PixelType_Mono8, cWidth, cHeight, cPadding );
            cout << endl << "The properties of an image after a full copy of a user buffer." << endl;
            PrintImageProperties( imageB );

            // The image objects are destroyed. The user must take care of the deletion of the user buffer.
        }


        // The CPylonImage and grab results.
        {
            // This smart pointer will receive the grab result data.
            CGrabResultPtr ptrGrabResult;

            // Try to get a grab result.
            cout << endl << "Waiting for an image to be grabbed." << endl;
            try
            {
                Camera.GrabOne( 1000, ptrGrabResult );
            }
            catch (const GenericException& e)
            {

                cerr << "Could not grab an image: " << endl
                    << e.GetDescription() << endl;
            }

            if (ptrGrabResult && ptrGrabResult->GrabSucceeded())
            {
                // Create a pylon image.
                CPylonImage image;

                // A pylon grab result class CGrabResultPtr provides a cast operator to IImage.
                // That's why it can be used like an image, e.g. to print its properties or
                // to show it on the screen.
                cout << endl << "The properties of the grabbed image." << endl;
                PrintImageProperties( ptrGrabResult );
                ShowImage( ptrGrabResult, "Grabbed image." );

                // Initializes the image object with the buffer from the grab result.
                // This prevents the reuse of the buffer for grabbing as long as it is
                // not released.
                // Please note that this is not relevant for this example because the
                // camera object has been destroyed already.
                image.AttachGrabResultBuffer( ptrGrabResult );
                cout << endl << "The properties of an image with an attached grab result." << endl;
                PrintImageProperties( image );

                // Get the grab result image properties for later use.
                EPixelType pixelType = ptrGrabResult->GetPixelType();
                uint32_t width = ptrGrabResult->GetWidth();
                uint32_t height = ptrGrabResult->GetHeight();

                // Now the grab result can be released. The grab result buffer is now
                // only held by the pylon image.
                ptrGrabResult.Release();
                cout << "After the grab result has been released." << endl;
                PrintImageProperties( image );

                // If a grab result is referenced then always a new buffer is allocated on reset.
                image.Reset( pixelType, width / 2, height );
                cout << endl << "After resetting the image properties while a grab result is referenced. A new Buffer is allocated." << endl;
                PrintImageProperties( image );
            }
        }


        // Loading and saving.
        // Please note that this is only a brief overview. Please look at the
        // Utility_ImageLoadAndSave sample for more information.
        {
            // Create pylon images.
            CPylonImage imageSaved;
            CPylonImage imageLoaded;

            // Create a sample image.
            imageSaved = SampleImageCreator::CreateJuliaFractal( PixelType_RGB8packed, cWidth, cHeight );

#ifdef PYLON_WIN_BUILD
            // Save the image. The image is automatically converted to
            // a format that can be saved if needed.
            imageSaved.Save( ImageFileFormat_Bmp, "JuliaFractal.bmp" );
#endif

#ifdef PYLON_WIN_BUILD
            // Load the image.
            imageLoaded.Load( "JuliaFractal.bmp" );
            cout << endl << "The properties of the loaded sample image." << endl;
            PrintImageProperties( imageLoaded );
            ShowImage( imageLoaded, "The loaded sample image is shown." );
#endif
        }


        // The GetAOI method.
        // This method can be used to create partial images derived from an image, e.g. thumbnail images for displaying
        // defects.
        {
            // Create pylon images.
            CPylonImage sampleImage;
            CPylonImage aoi;
            CPylonImage aoiFromAoi;

            // Create a sample image.
            sampleImage = SampleImageCreator::CreateJuliaFractal( PixelType_RGB8packed, cWidth, cHeight );
            cout << endl << "The properties of the sample image." << endl;
            PrintImageProperties( sampleImage );

            // Compute the coordinates of the area of interest.
            uint32_t topLeftX = cWidth / 4;
            uint32_t topLeftY = cHeight / 2;
            uint32_t width = cWidth / 4;
            uint32_t height = cHeight / 4;

            // Create a new pylon image containing the AOI.
            // No image data is copied. The same image buffer is referenced.
            // The buffer start is now the first pixel of the and the
            // padding property of the pylon image object is used to skip over the
            // part of a line outside of the AOI.
            aoi = sampleImage.GetAoi( topLeftX, topLeftY, width, height );
            cout << "After creating an AOI." << endl;
            PrintImageProperties( aoi );
            ShowImage( aoi, "AOI of the sample image." );

            // CopyImage( const IImage& image, size_t newPaddingX) can be used to create a
            // full copy and to remove the additional padding.
            CPylonImage copiedAoi;
            copiedAoi.CopyImage( aoi, 0 );
            cout << "The properties of a full copy of the AOI image." << endl;
            PrintImageProperties( copiedAoi );

            // GetAOI can be applied again for the AOI image.
            topLeftX = width / 4;
            topLeftY = height / 4;
            width = width / 2;
            height = height / 2;
            aoiFromAoi = aoi.GetAoi( topLeftX, topLeftY, width, height );

            // An AOI image is still valid if the source image object has been destroyed
            // or the image data has been released.
            aoi.Release();
            sampleImage.Release();

            // Show the image.
            cout << "After creating an AOI of an AOI." << endl;
            PrintImageProperties( aoiFromAoi );
            ShowImage( aoiFromAoi, "AOI of the AOI of the sample image." );

            // The AOI image still references the buffer of the source image.
            // It is the only object that references this buffer.
            // That's why the full buffer can be reused if needed.
            aoiFromAoi.Reset( PixelType_Mono8, cWidth, cHeight );
            cout << "After reusing the buffer of the sample image." << endl;
            PrintImageProperties( aoiFromAoi );
        }


        // The GetPlane method.
        // This method can be used to work with the planes of
        // an planar image.
        {
            // Create an image object.
            CPylonImage imageRGB8planar;

            // Create a sample image.
            imageRGB8planar = SampleImageCreator::CreateMandelbrotFractal( PixelType_RGB8planar, cWidth, cHeight );
            ShowImage( imageRGB8planar, "Sample image." );

            // Create images to access the planes of the planar image.
            // No image data is copied. The same image buffer is referenced.
            // The buffer start is the start of the plane and the pixel type
            // set to the corresponding pixel type of a plane.
            CPylonImage redPlane = imageRGB8planar.GetPlane( 0 );
            CPylonImage greenPlane = imageRGB8planar.GetPlane( 1 );
            CPylonImage bluePlane = imageRGB8planar.GetPlane( 2 );

            // Show the planes.
            ShowImage( redPlane, "Red plane of the sample image." );
            ShowImage( greenPlane, "Green plane of the sample image." );
            ShowImage( bluePlane, "Blue plane of the sample image." );

            // Now a plane can be modified. Here the red plane is set to zero.
            memset( redPlane.GetBuffer(), 0, greenPlane.GetImageSize() );

            // Show the image.
            ShowImage( imageRGB8planar, "Sample image with red set to zero." );
        }


        // The CPylonBitmapImage class.
        // This class can be used to easily create Windows bitmaps, e.g. for displaying.
        {
#ifdef PYLON_WIN_BUILD
            // Create a bitmap image
            CPylonBitmapImage bitmapImage;

            // Create a sample image.
            CPylonImage sampleImage;
            sampleImage = SampleImageCreator::CreateJuliaFractal( PixelType_RGB8packed, cWidth, cHeight );

            // The bitmap image class automatically converts input images to the
            // corresponding bitmap format.
            bitmapImage.CopyImage( sampleImage );
            cout << endl << "The properties of the bitmap image." << endl;
            PrintImageProperties( bitmapImage );
            ShowImage( bitmapImage, "The sample image is shown." );

            // If the pylon bitmap image object is copied or assigned then no image data copy is made.
            // All objects reference the same Windows bitmap now.
            // The IsUnique() method can be used to check whether the Windows bitmap is
            // referenced by multiple pylon image objects.
            CPylonBitmapImage sameBitmapImageA( bitmapImage );
            CPylonBitmapImage sameBitmapImageB = bitmapImage;
            cout << endl << "After assignment multiple images reference the same data." << endl;
            PrintImageProperties( bitmapImage );
            PrintImageProperties( sameBitmapImageA );
            PrintImageProperties( sameBitmapImageB );

            // The Release() method can be used to release any data.
            // The object sameBitmapImageB is now empty.
            // No bitmap is allocated.
            sameBitmapImageB.Release();
            cout << endl << "Assigned to image object after releasing the image data." << endl;
            PrintImageProperties( sameBitmapImageB );

            // The image format converter can be used to have more control over the conversion.
            // In this example a monochrome version of a sample image is created.
            // See the Utility_ImageFormatConverter sample for more details.
            CImageFormatConverter converter;
            converter.OutputPixelFormat = PixelType_Mono8;
            converter.Convert( bitmapImage, sampleImage );

            // Show the image.
            cout << endl << "The properties of the converted bitmap image." << endl;
            PrintImageProperties( bitmapImage );
            ShowImage( bitmapImage, "The to monochrome converted sample image is shown." );

            // Reset can be used to reuse the underlying windows bitmap if
            // the new image properties are equal to the old ones.
            // No additional program logic is needed for reusing a bitmap
            // until new image properties are required.
            bitmapImage.Reset( PixelType_Mono8, cWidth, cHeight );
            cout << endl << "The properties of the reused bitmap image with equal properties." << endl;
            PrintImageProperties( bitmapImage );

            // Now the new image properties are different. A new Windows
            // bitmap is created.
            bitmapImage.Reset( PixelType_Mono8, cWidth / 2, cHeight );
            cout << endl << "The properties of the newly allocated bitmap image with different properties." << endl;
            PrintImageProperties( bitmapImage );

            // The bitmap image class provides a cast operator for HBitmap.
            // The cast operator can be used for instance to provide the handle to Windows API functions.
            HBITMAP bitmap = bitmapImage;

            // The bitmap can also be detached to use it without the pylon image object.
            bitmap = bitmapImage.Detach();

            // The pylon bitmap image is now empty.
            cout << endl << "The image object after detaching the image data." << endl;
            PrintImageProperties( bitmapImage );

            // After detaching the bitmap must be deleted by the user.
            ::DeleteObject( bitmap );
#endif
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
