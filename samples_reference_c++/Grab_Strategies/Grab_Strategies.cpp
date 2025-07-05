// Grab_Strategies.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample shows the use of the different grab strategies.
    
    There are different strategies to grab images with the Instant Camera grab engine:
    * One By One: This strategy is the default grab strategy. Acquisitioned images are processed in their arrival order.
    * Latest Image Only: Differs from the One By One strategy by a single image output queue. Therefore, only the latest
    image is kept in the output output queue, all other grabbed images are skipped. 
    * Latest Images: Extends the above strategies by adjusting the size of output queue. If the output queue has a size of
    1, it is equal to the Latest Image Only strategy. Consequently, setting the output queue size to 
    CInstantCamera::MaxNumBuffer is equal to One by One.
    * Upcoming Image Grab: Ensures that the image grabbed is the next image received from the camera. When retrieving an 
    image, a buffer is queued into the input queue and then the call waits for the upcoming image. Subsequently, image data 
    is grabbed into the buffer and returned. Note: This strategy can't be used together with USB camera devices. 
    
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include files used by samples.
#include "../include/ConfigurationEventPrinter.h"
#include "../include/ImageEventPrinter.h"

// Namespace for using pylon objects.
using namespace Pylon;

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
        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Create an instant camera object for the camera device found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Register the standard configuration event handler for enabling software triggering.
        // The software trigger configuration handler replaces the default configuration
        // as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CSoftwareTriggerConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // For demonstration purposes only, registers an event handler configuration to print out information about camera use.
        // The event handler configuration is appended to the registered software trigger configuration handler by setting 
        // registration mode to RegistrationMode_Append.
        camera.RegisterConfiguration( new CConfigurationEventPrinter, RegistrationMode_Append, Cleanup_Delete );
        camera.RegisterImageEventHandler( new CImageEventPrinter, RegistrationMode_Append, Cleanup_Delete );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // The MaxNumBuffer parameter can be used to control the count of buffers
        // allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 15;

        // Open the camera.
        camera.Open();


        // Can the camera device be queried whether it is ready to accept the next frame trigger?
        if (camera.CanWaitForFrameTriggerReady())
        {
            cout << "Grab using the GrabStrategy_OneByOne default strategy:" << endl << endl;

            // The GrabStrategy_OneByOne strategy is used. The images are processed
            // in the order of their arrival.
            camera.StartGrabbing( GrabStrategy_OneByOne );

            // In the background, the grab engine thread retrieves the
            // image data and queues the buffers into the internal output queue.

            // Issue software triggers. For each call, wait up to 1000 ms until the camera is ready for triggering the next image.
            for (int i = 0; i < 3; ++i)
            {
                if (camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException ))
                {
                    camera.ExecuteSoftwareTrigger();
                }
            }

            // For demonstration purposes, wait for the last image to appear in the output queue.
            WaitObject::Sleep( 3 * 1000 );

            // Check that grab results are waiting.
            if (camera.GetGrabResultWaitObject().Wait( 0 ))
            {
                cout << endl << "Grab results wait in the output queue." << endl << endl;
            }

            // All triggered images are still waiting in the output queue
            // and are now retrieved.
            // The grabbing continues in the background, e.g. when using hardware trigger mode,
            // as long as the grab engine does not run out of buffers.
            int nBuffersInQueue = 0;
            while (camera.RetrieveResult( 0, ptrGrabResult, TimeoutHandling_Return ))
            {
                nBuffersInQueue++;
            }
            cout << "Retrieved " << nBuffersInQueue << " grab results from output queue." << endl << endl;

            //Stop the grabbing.
            camera.StopGrabbing();



            cout << endl << "Grab using strategy GrabStrategy_LatestImageOnly:" << endl << endl;

            // The GrabStrategy_LatestImageOnly strategy is used. The images are processed
            // in the order of their arrival but only the last received image
            // is kept in the output queue.
            // This strategy can be useful when the acquired images are only displayed on the screen.
            // If the processor has been busy for a while and images could not be displayed automatically
            // the latest image is displayed when processing time is available again.
            camera.StartGrabbing( GrabStrategy_LatestImageOnly );

            // Execute the software trigger, wait actively until the camera accepts the next frame trigger or until the timeout occurs.
            for (int i = 0; i < 3; ++i)
            {
                if (camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException ))
                {
                    camera.ExecuteSoftwareTrigger();
                }
            }

            // Wait for all images.
            WaitObject::Sleep( 3 * 1000 );

            // Check whether the grab result is waiting.
            if (camera.GetGrabResultWaitObject().Wait( 0 ))
            {
                cout << endl << "A grab result waits in the output queue." << endl << endl;
            }

            // Only the last received image is waiting in the internal output queue
            // and is now retrieved.
            // The grabbing continues in the background, e.g. when using the hardware trigger mode.
            nBuffersInQueue = 0;
            while (camera.RetrieveResult( 0, ptrGrabResult, TimeoutHandling_Return ))
            {
                cout << "Skipped " << ptrGrabResult->GetNumberOfSkippedImages() << " images." << endl;
                nBuffersInQueue++;
            }

            cout << "Retrieved " << nBuffersInQueue << " grab result from output queue." << endl << endl;

            //Stop the grabbing.
            camera.StopGrabbing();



            cout << endl << "Grab using strategy GrabStrategy_LatestImages:" << endl << endl;

            // The GrabStrategy_LatestImages strategy is used. The images are processed
            // in the order of their arrival, but only a number of the images received last
            // are kept in the output queue.

            // The size of the output queue can be adjusted.
            // When using this strategy the OutputQueueSize parameter can be changed during grabbing.
            camera.OutputQueueSize = 2;

            camera.StartGrabbing( GrabStrategy_LatestImages );

            // Execute the software trigger, wait actively until the camera accepts the next frame trigger or until the timeout occurs.
            for (int i = 0; i < 3; ++i)
            {
                if (camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException ))
                {
                    camera.ExecuteSoftwareTrigger();
                }
            }

            // Wait for all images.
            WaitObject::Sleep( 3 * 1000 );

            // Check whether the grab results are waiting.
            if (camera.GetGrabResultWaitObject().Wait( 0 ))
            {
                cout << endl << "Grab results wait in the output queue." << endl << endl;
            }

            // Only the images received last are waiting in the internal output queue
            // and are now retrieved.
            // The grabbing continues in the background, e.g. when using the hardware trigger mode.
            nBuffersInQueue = 0;
            while (camera.RetrieveResult( 0, ptrGrabResult, TimeoutHandling_Return ))
            {
                if (ptrGrabResult->GetNumberOfSkippedImages())
                {
                    cout << "Skipped " << ptrGrabResult->GetNumberOfSkippedImages() << " image." << endl;
                }
                nBuffersInQueue++;
            }

            cout << "Retrieved " << nBuffersInQueue << " grab results from output queue." << endl << endl;

            // When setting the output queue size to 1 this strategy is equivalent to the GrabStrategy_LatestImageOnly grab strategy.
            camera.OutputQueueSize = 1;

            // When setting the output queue size to CInstantCamera::MaxNumBuffer this strategy is equivalent to GrabStrategy_OneByOne.
            camera.OutputQueueSize = camera.MaxNumBuffer;

            //Stop the grabbing.
            camera.StopGrabbing();



            // The Upcoming Image grab strategy can't be used together with USB camera devices.
            // For more information, see the advanced topics section of the pylon Programmer's Guide.
            if (!camera.IsUsb())
            {
                cout << endl << "Grab using the GrabStrategy_UpcomingImage strategy:" << endl << endl;

                // Reconfigure the camera to use continuous acquisition.
                CAcquireContinuousConfiguration().OnOpened( camera );

                // The GrabStrategy_UpcomingImage strategy is used. A buffer for grabbing
                // is queued each time when RetrieveResult()
                // is called. The image data is grabbed into the buffer and returned.
                // This ensures that the image grabbed is the next image
                // received from the camera.
                // All images are still transported to the computer.
                camera.StartGrabbing( GrabStrategy_UpcomingImage );

                // Queues a buffer for grabbing and waits for the grab to finish.
                camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );

                // Sleep.
                WaitObject::Sleep( 1000 );

                // Check no grab result is waiting, because no buffers are queued for grabbing.
                if (!camera.GetGrabResultWaitObject().Wait( 0 ))
                {
                    cout << "No grab result waits in the output queue." << endl << endl;
                }

                //Stop the grabbing.
                camera.StopGrabbing();
            }
        }
        else
        {
            // See the documentation of CInstantCamera::CanWaitForFrameTriggerReady() for more information.
            cout << endl;
            cout << "This sample can only be used with cameras that can be queried whether they are ready to accept the next frame trigger.";
            cout << endl;
            cout << endl;
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
