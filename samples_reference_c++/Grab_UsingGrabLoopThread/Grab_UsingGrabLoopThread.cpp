// Grab_UsingGrabLoopThread.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to grab and process images using the grab loop thread
    provided by the Instant Camera class.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

// Include files used by samples.
#include "../include/ConfigurationEventPrinter.h"
#include "../include/ImageEventPrinter.h"

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

//Example of an image event handler.
class CSampleImageEventHandler : public CImageEventHandler
{
public:
    virtual void OnImageGrabbed( CInstantCamera& /*camera*/, const CGrabResultPtr& ptrGrabResult )
    {
        cout << "CSampleImageEventHandler::OnImageGrabbed called." << std::endl;

#ifdef PYLON_WIN_BUILD
        // Display the image
        Pylon::DisplayImage( 1, ptrGrabResult );
#endif
    }
};

int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object for the camera device found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Register the standard configuration event handler for enabling software triggering.
        // The software trigger configuration handler replaces the default configuration
        // as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CSoftwareTriggerConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // For demonstration purposes only, registers an event handler configuration to print out information about camera use.
        // The event handler configuration is appended to the registered software trigger configuration handler by setting 
        // registration mode to RegistrationMode_Append.
        camera.RegisterConfiguration( new CConfigurationEventPrinter, RegistrationMode_Append, Cleanup_Delete );

        // The image event printer serves as sample image processing.
        // When using the grab loop thread provided by the Instant Camera object, an image event handler processing the grab
        // results must be created and registered.
        camera.RegisterImageEventHandler( new CImageEventPrinter, RegistrationMode_Append, Cleanup_Delete );

        // For demonstration purposes only, register another image event handler.
        camera.RegisterImageEventHandler( new CSampleImageEventHandler, RegistrationMode_Append, Cleanup_Delete );

        // Open the camera device.
        camera.Open();

        // Can the camera device be queried whether it is ready to accept the next frame trigger?
        if (camera.CanWaitForFrameTriggerReady())
        {
            // Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
            // to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
            // The GrabStrategy_OneByOne default grab strategy is used.
            camera.StartGrabbing( GrabStrategy_OneByOne, GrabLoop_ProvidedByInstantCamera );

            // Wait for user input to trigger the camera or exit the program.
            // The grabbing is stopped, the device is closed and destroyed automatically when the camera object goes out of scope.

            bool runLoop = true;
            while (runLoop)
            {
                cout << endl << "Enter \"t\" to trigger the camera or \"e\" to exit and press enter? (t/e) "; cout.flush();

                string userInput;
                getline(cin, userInput);

                for (size_t i = 0; i < userInput.size(); ++i)
                {
                    char key = userInput[i];
                    if ((key == 't' || key == 'T'))
                    {
                        // Execute the software trigger. Wait up to 1000 ms for the camera to be ready for trigger.
                        if (camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException ))
                        {
                            camera.ExecuteSoftwareTrigger();
                        }
                    }
                    else if ((key == 'e') || (key == 'E'))
                    {
                        runLoop = false;
                        break;
                    }
                }

                // Wait some time to allow the OnImageGrabbed handler print its output,
                // so the printed text on the console is in the expected order.
                WaitObject::Sleep( 250 );
            }
        }
        else
        {
            // See the documentation of CInstantCamera::CanWaitForFrameTriggerReady() for more information.
            cout << endl << "This sample can only be used with cameras that can be queried whether they are ready to accept the next frame trigger." << endl;
        }
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}

