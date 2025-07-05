// Grab_UsingActionCommand.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample shows how to issue a GigE Vision ACTION_CMD to multiple cameras.
    By using an action command multiple cameras can be triggered at the same time
    compared to software triggering, which must be triggered individually.

    To make the configuration of multiple cameras easier this sample uses the CInstantCameraArray class.
    It also uses a CActionTriggerConfiguration to set up the basic action command features.
*/

#include <time.h>   // for time
#include <stdlib.h> // for rand & srand

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#   include <pylon/PylonGUI.h>
#endif

#include <pylon/BaslerUniversalInstantCameraArray.h>
#include <pylon/Info.h>
#include <pylon/gige/GigETransportLayer.h>
#include <pylon/gige/ActionTriggerConfiguration.h>
#include <pylon/gige/BaslerGigEDeviceInfo.h>


// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

// Limits the amount of cameras used for grabbing.
// It is important to manage the available bandwidth when grabbing with multiple
// cameras. This applies, for instance, if two GigE cameras are connected to the
// same network adapter via a switch. To manage the bandwidth, the GevSCPD
// interpacket delay parameter and the GevSCFTD transmission delay parameter can
// be set for each GigE camera device. The "Controlling Packet Transmission Timing
// with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
// Application Note (AW000649xx000) provides more information about this topic.
static const uint32_t c_maxCamerasToUse = 2;


int main( int /*argc*/, char* /*argv*/[] )
{
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Get the GigE transport layer.
        // We'll need it later to issue the action commands.
        CTlFactory& tlFactory = CTlFactory::GetInstance();
        IGigETransportLayer* pTL = dynamic_cast<IGigETransportLayer*>(tlFactory.CreateTl( BaslerGigEDeviceClass ));
        if (pTL == NULL)
        {
            throw RUNTIME_EXCEPTION( "No GigE transport layer available." );
        }


        // In this sample we use the transport layer directly to enumerate cameras.
        // By calling EnumerateDevices on the TL we get get only GigE cameras.
        // You could also accomplish this by using a filter and
        // let the Transport Layer Factory enumerate.
        DeviceInfoList_t allDeviceInfos;
        if (pTL->EnumerateDevices( allDeviceInfos ) == 0)
        {
            throw RUNTIME_EXCEPTION( "No GigE cameras present." );
        }

        // Only use cameras in the same subnet as the first one.
        DeviceInfoList_t usableDeviceInfos;
        usableDeviceInfos.push_back( allDeviceInfos[0] );
        const String_t subnet( allDeviceInfos[0].GetSubnetAddress() );

        // Start with index 1 as we have already added the first one above.
        // We will also limit the number of cameras to c_maxCamerasToUse.
        for (size_t i = 1; i < allDeviceInfos.size() && usableDeviceInfos.size() < c_maxCamerasToUse; ++i)
        {
            if (subnet == allDeviceInfos[i].GetSubnetAddress())
            {
                // Add this deviceInfo to the ones we will be using.
                usableDeviceInfos.push_back( allDeviceInfos[i] );
            }
            else
            {
                cerr << "Camera will not be used because it is in a different subnet "
                    << subnet << "!" << endl;
            }
        }

        // In this sample we'll use an CBaslerGigEInstantCameraArray to access multiple cameras.
        CBaslerUniversalInstantCameraArray cameras( usableDeviceInfos.size() );

        // Seed the random number generator and generate a random device key value.
        srand( (unsigned) time( NULL ) );
        const uint32_t DeviceKey = rand();

        // For this sample we configure all cameras to be in the same group.
        const uint32_t GroupKey = 0x112233;

        // For the following sample we use the CActionTriggerConfiguration to configure the camera.
        // It will set the DeviceKey, GroupKey and GroupMask features. It will also
        // configure the camera FrameTrigger and set the TriggerSource to the action command.
        // You can look at the implementation of CActionTriggerConfiguration in <pylon/gige/ActionTriggerConfiguration.h>
        // to see which features are set.

        // Create all GigE cameras and attach them to the InstantCameras in the array.
        for (size_t i = 0; i < cameras.GetSize(); ++i)
        {
            cameras[i].Attach( tlFactory.CreateDevice( usableDeviceInfos[i] ) );
            // We'll use the CActionTriggerConfiguration, which will set up the cameras to wait for an action command.
            cameras[i].RegisterConfiguration( new CActionTriggerConfiguration( DeviceKey, GroupKey, AllGroupMask ), RegistrationMode_Append, Cleanup_Delete );
            // Set the context. This will help us later to correlate the grab result to a camera in the array.
            cameras[i].SetCameraContext( i );

            const CBaslerGigEDeviceInfo& di = cameras[i].GetDeviceInfo();

            // Print the model name of the camera.
            cout << "Using device    : " << di.GetModelName() << endl;
            cout << "Using camera nr.: " << i << endl;
            cout << "IP Address      : " << di.GetIpAddress() << endl << endl;
        }

        // Open all cameras.
        // This will apply the CActionTriggerConfiguration specified above.
        cameras.Open();

        //////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////////////////////////////
        // Use an Action Command to Trigger Multiple Cameras at the Same Time.
        //////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////////////////////////////

        cout << endl << "Issuing an action command." << endl;

        // Starts grabbing for all cameras.
        // The cameras won't transmit any image data, because they are configured to wait for an action command.
        cameras.StartGrabbing();

        // Now we issue the action command to all devices in the subnet.
        // The devices with a matching DeviceKey, GroupKey and valid GroupMask will grab an image.
        pTL->IssueActionCommand( DeviceKey, GroupKey, AllGroupMask, subnet );

        // This smart pointer will receive the grab result data.
        CBaslerUniversalGrabResultPtr ptrGrabResult;

        // Retrieve images from all cameras.
        const int DefaultTimeout_ms = 5000;
        for (size_t i = 0; i < usableDeviceInfos.size() && cameras.IsGrabbing(); ++i)
        {
            // CInstantCameraArray::RetrieveResult will return grab results in the order they arrive.
            cameras.RetrieveResult( DefaultTimeout_ms, ptrGrabResult, TimeoutHandling_ThrowException );

            // When the cameras in the array are created the camera context value
            // is set to the index of the camera in the array.
            // The camera context is a user-settable value.
            // This value is attached to each grab result and can be used
            // to determine the camera that produced the grab result.
            intptr_t cameraIndex = ptrGrabResult->GetCameraContext();


            // Image grabbed successfully?
            if (ptrGrabResult->GrabSucceeded())
            {
#ifdef PYLON_WIN_BUILD
                // Show the image acquired by each camera in the window related to the camera.
                // DisplayImage supports up to 32 image windows.
                if (cameraIndex <= 31)
                    Pylon::DisplayImage( cameraIndex, ptrGrabResult );
#endif
                // Print the index and the model name of the camera.
                cout << "Camera " << cameraIndex << ": " << cameras[cameraIndex].GetDeviceInfo().GetModelName() <<
                    " (" << cameras[cameraIndex].GetDeviceInfo().GetIpAddress() << ")" << endl;

                // You could process the image here by accessing the image buffer.
                cout << "GrabSucceeded: " << ptrGrabResult->GrabSucceeded() << endl;
                const uint8_t* pImageBuffer = (uint8_t*) ptrGrabResult->GetBuffer();
                cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << endl << endl;
            }
            else
            {
                // If a buffer has been incompletely grabbed, the network bandwidth is possibly insufficient for transferring
                // multiple images simultaneously. See note above c_maxCamerasToUse.
                cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << endl;
            }
        }

        // In case you want to trigger again you should wait for the camera
        // to become trigger-ready before issuing the next action command.
        // To avoid overtriggering you should call cameras[0].WaitForFrameTriggerReady
        // (see Grab_UsingGrabLoopThread sample for details).

        cameras.StopGrabbing();

        // Close all cameras.
        cameras.Close();
    }
    catch (const GenericException& e)
    {
        // Error handling
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


