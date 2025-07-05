// DeviceRemovalHandling.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample program demonstrates how to be informed about the removal of a camera device.
    It also shows how to reconnect to a removed device.

    Attention:
    If you build this sample in debug mode and run it using a GigE camera device, pylon will set the heartbeat
    timeout to 60 minutes. This is done to allow debugging and single-stepping without losing the camera
    connection due to missing heartbeats. However, with this setting, it would take 60 minutes for the
    application to notice that a GigE device has been disconnected.
    As a workaround, the heartbeat timeout is set to 1000 ms.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#include "../include/ConfigurationEventPrinter.h"

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;


// When using device-specific Instant Camera classes there are specific Configuration event handler classes available which can be used, for example
// Pylon::CBaslerUniversalConfigurationEventHandler.
//Example of a configuration event handler that handles device removal events.
class CSampleConfigurationEventHandler : public Pylon::CConfigurationEventHandler
{
public:
    // This method is called from a different thread when the camera device removal has been detected.
    void OnCameraDeviceRemoved( CInstantCamera& /*camera*/ )
    {
        // Print two new lines, just for improving printed output.
        cout << endl << endl;
        cout << "CSampleConfigurationEventHandler::OnCameraDeviceRemoved called." << std::endl;
    }
};

// Time to wait in quarters of seconds.
static const uint32_t c_loopCounterInitialValue = 60 * 4;

 int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Declare a local counter used for waiting.
        int loopCount = 0;

        // Get the transport layer factory.
        CTlFactory& tlFactory = CTlFactory::GetInstance();

        // Create an instant camera object with the camera device found first.
        CInstantCamera camera( tlFactory.CreateFirstDevice() );

        // Print the camera information.
        cout << "Using device : " << camera.GetDeviceInfo().GetModelName() << endl;
        cout << "Friendly Name: " << camera.GetDeviceInfo().GetFriendlyName() << endl;
        cout << "Full Name    : " << camera.GetDeviceInfo().GetFullName() << endl;
        cout << "SerialNumber : " << camera.GetDeviceInfo().GetSerialNumber() << endl;
        cout << endl;

        // For demonstration purposes only, register another configuration event handler that handles device removal.
        camera.RegisterConfiguration( new CSampleConfigurationEventHandler, RegistrationMode_Append, Cleanup_Delete );

        // For demonstration purposes only, add a sample configuration event handler to print out information
        // about camera use.
        camera.RegisterConfiguration( new CConfigurationEventPrinter, RegistrationMode_Append, Cleanup_Delete );

        // Open the camera. Camera device removal is only detected while the camera is open.
        camera.Open();

        // Now, try to detect that the camera has been removed:

        // Ask the user to disconnect a device
        loopCount = c_loopCounterInitialValue;
        cout << endl << "Please disconnect the device (timeout " << loopCount / 4 << "s) " << endl;

        /////////////////////////////////////////////////// don't single step beyond this line  (see comments above)

        // Before testing the callbacks, we manually set the heartbeat timeout to a short value when using GigE cameras.
        // Since for debug versions the heartbeat timeout has been set to 5 minutes, it would take up to 5 minutes
        // until detection of the device removal.
        CIntegerParameter heartbeat( camera.GetTLNodeMap(), "HeartbeatTimeout" );
        heartbeat.TrySetValue( 1000, IntegerValueCorrection_Nearest );  // set to 1000 ms timeout if writable

        try
        {
            // Get a camera parameter using generic parameter access.
            CIntegerParameter width( camera.GetNodeMap(), "Width" );

            // The following loop accesses the camera. It could also be a loop that is
            // grabbing images. The device removal is handled in the exception handler.
            while (loopCount > 0)
            {
                // Print a "." every few seconds to tell the user we're waiting for the callback.
                if (--loopCount % 4 == 0)
                {
                    cout << ".";
                    cout.flush();
                }
                WaitObject::Sleep( 250 );

                // Change the width value in the camera depending on the loop counter.
                // Any access to the camera like setting parameters or grabbing images
                // will fail throwing an exception if the camera has been disconnected.
                width.SetValue( width.GetMax() - (width.GetInc() * (loopCount % 2)) );
            }

        }
        catch (const GenericException& e)
        {
            // An exception occurred. Is it because the camera device has been physically removed?

            // Known issue: Wait until the system safely detects a possible removal.
            WaitObject::Sleep( 1000 );

            if (camera.IsCameraDeviceRemoved())
            {
                // The camera device has been removed. This caused the exception.
                cout << endl;
                cout << "The camera has been removed from the computer." << endl;
                cout << "The camera device removal triggered an expected exception:" << endl
                    << e.GetDescription() << endl;
            }
            else
            {
                // An unexpected error has occurred.
                
                // In this example it is handled by exiting the program.
                throw;
            }
        }

        if (!camera.IsCameraDeviceRemoved())
            cout << endl << "Timeout expired" << endl;

        /////////////////////////////////////////////////// Safe to use single stepping (see comments above).

        // Now try to find the detached camera after it has been attached again:

        // Create a device info object for remembering the camera properties.
        CDeviceInfo info;

        // Remember the camera properties that allow detecting the same camera again.
        info.SetDeviceClass( camera.GetDeviceInfo().GetDeviceClass() );
        info.SetSerialNumber( camera.GetDeviceInfo().GetSerialNumber() );

        // Destroy the Pylon Device representing the detached camera device.
        // It can't be used anymore.
        camera.DestroyDevice();

        // Ask the user to connect the same device.
        loopCount = c_loopCounterInitialValue;
        cout << endl << "Please connect the same device to the computer again (timeout " << loopCount / 4 << "s) " << endl;

        // Create a filter containing the CDeviceInfo object info which describes the properties of the device we are looking for.
        DeviceInfoList_t filter;
        filter.push_back( info );

        for (; loopCount > 0; --loopCount)
        {
            // Print a . every few seconds to tell the user we're waiting for the camera to be attached
            if (loopCount % 4 == 0)
            {
                cout << ".";
                cout.flush();
            }

            // Try to find the camera we are looking for.
            DeviceInfoList_t devices;
            if (tlFactory.EnumerateDevices( devices, filter ) > 0)
            {
                // Print two new lines, just for improving printed output.
                cout << endl << endl;

                // The camera has been found. Create and attach it to the Instant Camera object.
                camera.Attach( tlFactory.CreateDevice( devices[0] ) );
                //Exit waiting
                break;
            }

            WaitObject::Sleep( 250 );
        }

        // If the camera has been found.
        if (camera.IsPylonDeviceAttached())
        {
            // Print the camera information.
            cout << endl;
            cout << "Using device " << camera.GetDeviceInfo().GetModelName() << endl;
            cout << "Friendly Name: " << camera.GetDeviceInfo().GetFriendlyName() << endl;
            cout << "Full Name    : " << camera.GetDeviceInfo().GetFullName() << endl;
            cout << "SerialNumber : " << camera.GetDeviceInfo().GetSerialNumber() << endl;
            cout << endl;

            // All configuration objects and other event handler objects are still registered.
            // The configuration objects will parameterize the camera device and the instant
            // camera will be ready for operation again.

            // Open the camera.
            camera.Open();

            // Now the Instant Camera object can be used as before.
        }
        else // Timeout
        {
            cout << endl << "Timeout expired." << endl;
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
