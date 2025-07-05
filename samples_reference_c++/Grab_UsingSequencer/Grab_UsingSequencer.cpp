// Grab_UsingSequencer.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample shows how to grab images using the sequencer feature of a camera.
    Three sequence sets are used for image acquisition. Each sequence set
    uses a different image height.
*/

// Include files to use the pylon API
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

using namespace Pylon;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using cout
using namespace std;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 10;


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object with the first found camera device.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Register the standard configuration event handler for enabling software triggering.
        // The software trigger configuration handler replaces the default configuration
        // as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CSoftwareTriggerConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // Open the camera.
        camera.Open();

        if (camera.SequencerMode.IsWritable() || camera.SequenceEnable.IsWritable())
        {
            if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
            {
                // Disable the sequencer before changing parameters.
                // The parameters under control of the sequencer are locked
                // when the sequencer is enabled. For a list of parameters
                // controlled by the sequencer, see the Basler Product Documentation or the camera user's manual.
                camera.SequencerMode.SetValue( SequencerMode_Off );
                camera.SequencerConfigurationMode.SetValue( SequencerConfigurationMode_Off );

                // Maximize the grabbed image area of interest (Image AOI).
                camera.OffsetX.TrySetToMinimum();
                camera.OffsetY.TrySetToMinimum();
                camera.Width.SetToMaximum();
                camera.Height.SetToMaximum();

                // Set the pixel data format.
                // This parameter may be locked when the sequencer is enabled.
                camera.PixelFormat.SetValue( PixelFormat_Mono8 );

                // Set up sequence sets.

                // Set up sequence sets and turn sequencer configuration mode on.
                camera.SequencerConfigurationMode.SetValue( SequencerConfigurationMode_On );

                const int64_t initialSet = camera.SequencerSetSelector.GetMin();
                const int64_t incSet = camera.SequencerSetSelector.GetInc();
                int64_t curSet = initialSet;

                // Set the parameters for step 0; quarter height image.
                camera.SequencerSetSelector.SetValue( initialSet );
                { // valid for all sets
                    // reset on software signal 1;
                    camera.SequencerPathSelector.SetValue( 0 );
                    camera.SequencerSetNext.SetValue( initialSet );
                    camera.SequencerTriggerSource.SetValue( SequencerTriggerSource_SoftwareSignal1 );
                    // advance on Frame Start or Exposure Start (depends on camera family)
                    camera.SequencerPathSelector.SetValue( 1 );
                    const char* sequencerTrigger[] = { "FrameStart", "ExposureStart", NULL };
                    camera.SequencerTriggerSource.SetValue( sequencerTrigger );
                }
                camera.SequencerSetNext.SetValue( curSet + incSet );
                // quarter height
                camera.Height.SetValuePercentOfRange( 25.0 );
                camera.SequencerSetSave.Execute();

                // Set the parameters for step 1; half height image.
                curSet += incSet;
                camera.SequencerSetSelector.SetValue( curSet );
                // advance on Frame Start to next set
                camera.SequencerSetNext.SetValue( curSet + incSet );
                // half height
                camera.Height.SetValuePercentOfRange( 50.0 );
                camera.SequencerSetSave.Execute();

                // Set the parameters for step 2; full height image.
                curSet += incSet;
                camera.SequencerSetSelector.SetValue( curSet );
                // advance on Frame End to initial set,
                camera.SequencerSetNext.SetValue( initialSet ); // terminates sequence definition
                // full height
                camera.Height.SetValuePercentOfRange( 100.0 );
                camera.SequencerSetSave.Execute();
                // Enable the sequencer feature.
                // From here on you can't change the sequencer settings anymore.
                camera.SequencerConfigurationMode.SetValue( SequencerConfigurationMode_Off );
                camera.SequencerMode.SetValue( SequencerMode_On );
            }
            else
            {
                // Disable the sequencer before changing parameters.
                // The parameters under control of the sequencer are locked
                // when the sequencer is enabled. For a list of parameters
                // controlled by the sequencer, see the Basler Product Documentation or the camera user's manual.
                camera.SequenceEnable.SetValue( false );
                camera.SequenceConfigurationMode.TrySetValue( SequenceConfigurationMode_Off );

                // Maximize the grabbed image area of interest (Image AOI).
                camera.OffsetX.TrySetToMinimum();
                camera.OffsetY.TrySetToMinimum();
                camera.Width.SetToMaximum();
                camera.Height.SetToMaximum();

                // Set the pixel data format.
                // This parameter may be locked when the sequencer is enabled.
                camera.PixelFormat.SetValue( PixelFormat_Mono8 );

                // Set up sequence sets.

                // Turn configuration mode on if available.
                // Not supported by all cameras.
                camera.SequenceConfigurationMode.TrySetValue( SequenceConfigurationMode_On );

                // Configure how the sequence will advance.
                // 'Auto' refers to the auto sequence advance mode.
                // The advance from one sequence set to the next will occur automatically with each image acquired.
                // After the end of the sequence set cycle was reached a new sequence set cycle will start.
                camera.SequenceAdvanceMode = SequenceAdvanceMode_Auto;

                // Our sequence sets relate to three steps (0..2).
                // In each step we will increase the height of the Image AOI by one increment.
                camera.SequenceSetTotalNumber = 3;

                // Set the parameters for step 0; quarter height image.
                camera.SequenceSetIndex = 0;
                camera.Height.SetValuePercentOfRange( 25.0 );
                camera.SequenceSetStore.Execute();

                // Set the parameters for step 1; half height image.
                camera.SequenceSetIndex = 1;
                camera.Height.SetValuePercentOfRange( 50.0 );
                camera.SequenceSetStore.Execute();

                // Set the parameters for step 2; full height image.
                camera.SequenceSetIndex = 2;
                camera.Height.SetValuePercentOfRange( 100.0 );
                camera.SequenceSetStore.Execute();

                // Turn configuration mode off if available.
                // Not supported by all cameras.
                camera.SequenceConfigurationMode.TrySetValue( SequenceConfigurationMode_Off );

                // Enable the sequencer feature.
                // From here on you can't change the sequencer settings anymore.
                camera.SequenceEnable.SetValue( true );
            }


            // Start the grabbing of c_countOfImagesToGrab images.
            camera.StartGrabbing( c_countOfImagesToGrab );

            // This smart pointer will receive the grab result data.
            CGrabResultPtr grabResult;

            // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
            // when c_countOfImagesToGrab images have been retrieved.
            while (camera.IsGrabbing())
            {
                // Execute the software trigger. Wait up to 1000 ms for the camera to be ready for trigger.
                if (camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException ))
                {
                    camera.ExecuteSoftwareTrigger();

                    // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
                    camera.RetrieveResult( 5000, grabResult, TimeoutHandling_ThrowException );

                    // Image grabbed successfully?
                    if (grabResult->GrabSucceeded())
                    {
#ifdef PYLON_WIN_BUILD
                    // Display the grabbed image.
                        Pylon::DisplayImage( 1, grabResult );
#endif

                    // Access the image data.
                        cout << "SizeX: " << grabResult->GetWidth() << endl;
                        cout << "SizeY: " << grabResult->GetHeight() << endl;
                        const uint8_t* pImageBuffer = (uint8_t*) grabResult->GetBuffer();
                        cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << endl << endl;
                    }
                    else
                    {
                        cout << "Error: " << std::hex << grabResult->GetErrorCode() << std::dec << " " << grabResult->GetErrorDescription() << endl;
                    }
                }

                // Wait for user input.
                cerr << endl << "Press enter to continue." << endl << endl;
                while (camera.IsGrabbing() && cin.get() != '\n');
            }

            // Disable the sequencer.
            if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
            {
                camera.SequencerMode.SetValue( SequencerMode_Off );
            }
            else
            {
                camera.SequenceEnable.SetValue( false );
            }
			camera.SequenceConfigurationMode.TrySetValue( SequenceConfigurationMode_Off );
        }
        else
        {
            cout << "The sequencer feature is not available for this camera." << endl;
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
