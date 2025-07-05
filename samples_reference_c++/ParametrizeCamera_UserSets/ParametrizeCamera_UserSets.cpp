// ParametrizeCamera_UserSets.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    Demonstrates how to use user configuration sets (user sets) and how to configure the camera
    to start up with the user defined settings of user set 1.

    You can also configure your camera using the pylon Viewer and
    store your custom settings in a user set of your choice.

    Note: Different camera families implement different versions of the Standard Feature Naming Convention (SFNC).
    That's why the name and the type of the parameters used can be different.

    ATTENTION:
    Executing this sample will overwrite all current settings in user set 1.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

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
        // Create an instant camera object with the first found camera device.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Open the camera.
        camera.Open();

        // Check if the device supports user sets.
        if (!camera.UserSetSelector.IsWritable())
        {
            throw RUNTIME_EXCEPTION( "The device doesn't support user sets." );
        }

        // Used for USB cameras
        UserSetDefaultEnums oldDefaultUserSet = UserSetDefault_Default;
        // Used for GigE cameras
        UserSetDefaultSelectorEnums oldDefaultUserSetSelector = UserSetDefaultSelector_Default;

        // Remember the current default user set selector so we can restore it later when cleaning up.
        if (camera.UserSetDefault.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            oldDefaultUserSet = camera.UserSetDefault.GetValue();
        }
        else
        {
            oldDefaultUserSetSelector = camera.UserSetDefaultSelector.GetValue();
        }

        // Load default settings.
        cout << "Loading default settings" << endl;
        camera.UserSetSelector.SetValue( UserSetSelector_Default );
        camera.UserSetLoad.Execute();

        // Set gain and exposure time values.
        // The camera won't let you set specific values when related auto functions are active.
        // So we need to disable the related auto functions before setting the values.
        cout << "Turning off Gain Auto and Exposure Auto." << endl;

        if (camera.Gain.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            camera.GainAuto.TrySetValue( GainAuto_Off );
            camera.Gain.SetValue( camera.Gain.GetMin() );
            camera.ExposureAuto.TrySetValue( ExposureAuto_Off );
            camera.ExposureTime.SetValue( camera.ExposureTime.GetMin() );
        }
        else
        {
            camera.GainAuto.TrySetValue( GainAuto_Off );
            camera.GainRaw.SetValue( camera.GainRaw.GetMin() );
            camera.ExposureAuto.TrySetValue( ExposureAuto_Off );
            camera.ExposureTimeRaw.SetValue( camera.ExposureTimeRaw.GetMin() );
        }

        // Save to user set 1.
        //
        // ATTENTION:
        // This will overwrite all settings previously saved in user set 1.
        cout << "Saving currently active settings to user set 1." << endl;
        camera.UserSetSelector.SetValue( UserSetSelector_UserSet1 );
        camera.UserSetSave.Execute();

        // Show default settings.
        cout << endl << "Loading default settings." << endl;
        camera.UserSetSelector.SetValue( UserSetSelector_Default );
        camera.UserSetLoad.Execute();
        cout << "Default settings" << endl;
        cout << "================" << endl;
        if (camera.Gain.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            cout << "Gain          : " << camera.Gain.GetValue() << endl;
            cout << "Exposure time : " << camera.ExposureTime.GetValue() << endl;
        }
        else
        {
            cout << "Gain          : " << camera.GainRaw.GetValue() << endl;
            cout << "Exposure time : " << camera.ExposureTimeRaw.GetValue() << endl;
        }

        // Show user set 1 settings.
        cout << endl << "Loading user set 1 settings." << endl;
        camera.UserSetSelector.SetValue( UserSetSelector_UserSet1 );
        camera.UserSetLoad.Execute();
        cout << "User set 1 settings" << endl;
        cout << "===================" << endl;

        if (camera.Gain.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            cout << "Gain          : " << camera.Gain.GetValue() << endl;
            cout << "Exposure time : " << camera.ExposureTime.GetValue() << endl;
        }
        else
        {
            cout << "Gain          : " << camera.GainRaw.GetValue() << endl;
            cout << "Exposure time : " << camera.ExposureTimeRaw.GetValue() << endl;
        }

        // Set user set 1 as default user set:
        // When the camera wakes up it will be configured
        // with the settings from user set 1.
        if (camera.UserSetDefault.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            camera.UserSetDefault.SetValue( UserSetDefault_UserSet1 );

            // Restore the default user set selector.
            camera.UserSetDefault.SetValue( oldDefaultUserSet );
        }
        else
        {
            // Set user set 1 as default user set:
            // When the camera wakes up it will be configured
            // with the settings from user set 1.
            camera.UserSetDefaultSelector.SetValue( UserSetDefaultSelector_UserSet1 );

            // Restore the default user set selector.
            camera.UserSetDefaultSelector.SetValue( oldDefaultUserSetSelector );
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

