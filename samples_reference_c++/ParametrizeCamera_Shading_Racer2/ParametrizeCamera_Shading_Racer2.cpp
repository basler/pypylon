// ParametrizeCamera_Shading_Racer2.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample demonstrates how to create and use a DSNU or PRNU shading
    set with a Basler racer 2 line scan camera.

    This sample only applies to Basler racer 2 cameras.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

#ifdef PYLON_WIN_BUILD
// To show image window on Windows.
#include "pylon/PylonGUI.h"
#endif

// For sleeping
#include <chrono>
#include <thread>


#ifdef _MSC_VER
#pragma warning(push)
#pragma warning(disable: 4244)
#endif


#ifdef _MSC_VER
#pragma warning(pop)
#endif

// Namespace for using pylon objects.
using namespace Pylon;

// Namespaces for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using cout.
using namespace std;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 5;

////////////////////////////////////////////////////////////////////////////////

int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object for the first camera found.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Register the standard configuration event handler for configuring continuous frame acquisition.
        // This replaces the default configuration as all event handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CAcquireContinuousConfiguration(), RegistrationMode_ReplaceAll, Cleanup_Delete );

        // Open the camera.
        camera.Open();

        // Only line scan cameras support gain shading.
        if (camera.DeviceScanType.GetValue() == DeviceScanType_Linescan && camera.BslShadingCorrectionSelector.IsValid())
        {
            // Disable Reverse X and set ROI to Max.
            camera.Width.SetValue(camera.WidthMax.GetValue());
            camera.ReverseX.SetValue(false);

            // Here, we assume that the conditions for exposure (illumination,
            // exposure time, etc.) have been set up to deliver correct images
            // for the correction type selected (DSNU or PRNU). If you're not sure, refer to the camera
            // documentation.

            // Set camera to DSNU Shading, switch to User mode, and select shading set 1.
            camera.BslShadingCorrectionSelector.SetValue(BslShadingCorrectionSelector_DSNU);
            camera.BslShadingCorrectionMode.SetValue(BslShadingCorrectionMode_User);
            camera.BslShadingCorrectionSetIndex.SetValue(1);

            // Start acquiring Images.
            camera.StartGrabbing();

            // Start the shading set generation and wait for success. The camera will automatically grab 256 images and
            // create the shading data.
            camera.BslShadingCorrectionSetCreate.Execute();

            // Wait until the shading set generation has finished
            cout << "Generating shading correction data.";
            while(camera.BslShadingCorrectionSetCreateStatus.GetValue() == BslShadingCorrectionSetCreateStatus_Active)
            {
                cout << ".";
                std::this_thread::sleep_for(std::chrono::milliseconds(1));
            }
            cout << "done." << endl;
            // Stop grabbing.
            camera.StopGrabbing();

            // Now we have a camera with a valid shading set stored on index 1. Let's use it.
            // First check whether the shading set selected really works.
            if(camera.BslShadingCorrectionSetStatus.GetValue() == BslShadingCorrectionSetStatus_Ok)
            {
                cout << "Successfully loaded Shading Correction"  << endl;
                // Start the grabbing of c_countOfImagesToGrab images.
                camera.StartGrabbing( c_countOfImagesToGrab );

                // This smart pointer will receive the grab result data.
                CGrabResultPtr ptrGrabResult;

                // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
                // when c_countOfImagesToGrab images have been retrieved.
                while (camera.IsGrabbing())
                {
                    // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                    camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );

                    // Image grabbed successfully?
                    if (ptrGrabResult->GrabSucceeded())
                    {
                        // Access the image data.
                        cout << "SizeX: " << ptrGrabResult->GetWidth() << endl;
                        cout << "SizeY: " << ptrGrabResult->GetHeight() << endl;
                        const uint8_t* pImageBuffer = (uint8_t*) ptrGrabResult->GetBuffer();
                        cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << endl << endl;

#ifdef PYLON_WIN_BUILD
                        // Display the image grabbed.
                        Pylon::DisplayImage( 1, ptrGrabResult );
#endif
                    }
                    else
                    {
                        cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << endl;
                    }
                }
            }
            else
            {
                cout << "Shading Correction could not be loaded." << endl;
            }
        }
        else
        {
            cerr << "Only line scan cameras support gain shading." << endl;
        }

        // Close the camera.
        camera.Close();
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

