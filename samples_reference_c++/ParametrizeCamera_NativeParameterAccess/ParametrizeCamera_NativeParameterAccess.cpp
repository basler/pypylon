// ParametrizeCamera_NativeParameterAccess.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    For camera configuration and for accessing other parameters, the pylon API
    uses the technologies defined by the GenICam standard hosted by the
    European Machine Vision Association (EMVA). The GenICam specification
    (http://www.GenICam.org) defines a format for camera description files.
    These files describe the configuration interface of GenICam compliant cameras.
    The description files are written in XML (eXtensible Markup Language) and
    describe camera registers, their interdependencies, and all other
    information needed to access high-level features such as Gain,
    Exposure Time, or Image Format by means of low-level register read and
    write operations.

    The elements of a camera description file are represented as software
    objects called Nodes. For example, a node can represent a single camera
    register, a camera parameter such as Gain, a set of available parameter
    values, etc. Each node implements the GenApi::INode interface.

    Using the code generators provided by GenICam's GenApi module,
    a programming interface is created from a camera description file.
    Thereby, a member is provided for each parameter that is available for the camera device.
    The programming interface is exported by the device-specific Instant Camera classes.
    This is the easiest way to access parameters.

    This sample shows the 'native' approach for configuring a camera
    using device-specific instant camera classes.

    See also the ParametrizeCamera_GenericParameterAccess sample for the 'generic'
    approach for configuring a camera.
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

        // Open the camera for accessing the parameters.
        camera.Open();

        // Get camera device information.
        cout << "Camera Device Information" << endl
            << "=========================" << endl;
        cout << "Vendor           : "
            << camera.DeviceVendorName.GetValue() << endl;
        cout << "Model            : "
            << camera.DeviceModelName.GetValue() << endl;
        cout << "Firmware version : "
            << camera.DeviceFirmwareVersion.GetValue() << endl << endl;

       // Camera settings.
        cout << "Camera Device Settings" << endl
            << "======================" << endl;



       // Set the AOI:

       // On some cameras, the offsets are read-only.
       // Therefore, we must use "Try" functions that only perform the action
       // when parameters are writable. Otherwise, we would get an exception.
        camera.OffsetX.TrySetToMinimum();
        camera.OffsetY.TrySetToMinimum();

        // Some properties have restrictions.
        // We use API functions that automatically perform value corrections.
        // Alternatively, you can use GetInc() / GetMin() / GetMax() to make sure you set a valid value.
        camera.Width.SetValue( 202, IntegerValueCorrection_Nearest );
        camera.Height.SetValue( 101, IntegerValueCorrection_Nearest );

        cout << "OffsetX          : " << camera.OffsetX.GetValue() << endl;
        cout << "OffsetY          : " << camera.OffsetY.GetValue() << endl;
        cout << "Width            : " << camera.Width.GetValue() << endl;
        cout << "Height           : " << camera.Height.GetValue() << endl;


        // Remember the current pixel format.
        PixelFormatEnums oldPixelFormat = camera.PixelFormat.GetValue();
        cout << "Old PixelFormat  : " << camera.PixelFormat.ToString() << " (" << oldPixelFormat << ")" << endl;

        // Set pixel format to Mono8 if available.
        if (camera.PixelFormat.CanSetValue( PixelFormat_Mono8 ))
        {
            camera.PixelFormat.SetValue( PixelFormat_Mono8 );
            cout << "New PixelFormat  : " << camera.PixelFormat.ToString() << " (" << camera.PixelFormat.GetValue() << ")" << endl;
        }

        // Set the new gain to 50% ->  Min + ((Max-Min) / 2).
        //
        // Note: Some newer camera models may have auto functions enabled.
        //       To be able to set the gain value to a specific value
        //       the Gain Auto function must be disabled first.
        // Access the enumeration type node GainAuto.
        // We use a "Try" function that only performs the action if the parameter is writable.
        camera.GainAuto.TrySetValue( GainAuto_Off );

        if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
        {
            if (camera.Gain.TrySetValuePercentOfRange( 50.0 ))
            {
                cout << "Gain (50%)       : " << camera.Gain.GetValue() << " (Min: " << camera.Gain.GetMin() << "; Max: " << camera.Gain.GetMax() << ")" << endl;
            }
        }
        else
        {
            if (camera.GainRaw.TrySetValuePercentOfRange( 50.0 ))
            {
                cout << "Gain (50%)       : " << camera.GainRaw.GetValue() << " (Min: " << camera.GainRaw.GetMin() << "; Max: " << camera.GainRaw.GetMax() << "; Inc: " << camera.GainRaw.GetInc() << ")" << endl;
            }
        }


        // Restore the old pixel format.
        camera.PixelFormat.SetValue( oldPixelFormat );

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

    // Comment the following two lines to disable waiting on exit
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}

