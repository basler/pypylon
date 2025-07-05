// Utility_ImageFormatConverter.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to use the image format
    converter class CImageFormatConverter.

    The image format converter accepts all image formats
    produced by Basler camera devices and it is able to
    convert these to a number of output formats.
    The conversion can be controlled by several parameters.
    See the converter class documentation for more details.
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

        // The image format converter basics.
        {
            // First the image format converter class must be created.
            CImageFormatConverter converter;

            // Second the converter must be parameterized.
            converter.OutputPixelFormat = PixelType_Mono16;
            converter.OutputBitAlignment = OutputBitAlignment_MsbAligned;

            // Try to set MaxNumThreads to maximum supported value.
            // Values larger than 1 will enable multithreaded image format conversion.
            
            // Set to 1 to disable multithreaded image format conversion.
            //converter.MaxNumThreads = 1;

            // Set to maximum value to enable all available cores for multithreaded image format conversion.
            converter.MaxNumThreads.TrySetToMaximum();

            // Then it can be used to convert input images to
            // the target image format.

            // Create a sample image.
            CPylonImage imageRGB8packed = SampleImageCreator::CreateMandelbrotFractal( PixelType_RGB8packed, cWidth, cHeight );
            ShowImage( imageRGB8packed, "Source image." );

            // Create a target image
            CPylonImage targetImage;

            // Convert the image. Note that there are more overloaded Convert methods available, e.g.
            // for converting the image from or to a user buffer.
            converter.Convert( targetImage, imageRGB8packed );
            ShowImage( targetImage, "Converted image." );
        }


        // Checking if conversion is needed.
        {
            // Create a target image.
            CPylonImage targetImage;

            // Create the converter and set parameters.
            CImageFormatConverter converter;
            converter.OutputPixelFormat = PixelType_Mono8;

            // Try to get a grab result for demonstration purposes.
            cout << endl << "Waiting for an image to be grabbed." << endl;
            try
            {
                // This smart pointer will receive the grab result data.
                CGrabResultPtr ptrGrabResult;
                
                if (Camera.GrabOne( 1000, ptrGrabResult ))
                {
                    // Now we can check if conversion is required.
                    if (converter.ImageHasDestinationFormat( ptrGrabResult ))
                    {
                        // No conversion is needed. It can be skipped for saving processing
                        // time.
                        ShowImage( ptrGrabResult, "Grabbed image." );
                    }
                    else
                    {
                        // Conversion is needed.
                        ShowImage( ptrGrabResult, "Grabbed image." );
                        converter.Convert( targetImage, ptrGrabResult );
                        ShowImage( targetImage, "Converted image." );
                    }
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
