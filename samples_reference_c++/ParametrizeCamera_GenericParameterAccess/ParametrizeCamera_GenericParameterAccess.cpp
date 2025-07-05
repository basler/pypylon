// ParametrizeCamera_GenericParameterAccess.cpp
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

    The nodes are linked together by different relationships as explained in the
    GenICam standard document available at www.GenICam.org. The complete set of
    nodes is stored in a data structure called Node Map.
    At runtime, a Node Map is instantiated from an XML description.

    This sample shows the 'generic' approach for configuring a camera
    using the GenApi nodemaps represented by the GenApi::INodeMap interface.

    The names and types of the parameter nodes can be found in the Basler pylon Programmer's Guide
    and API Reference, in the camera User's Manual, in the camera's document about
    Register Structure and Access Methodes (if applicable), and by using the pylon Viewer tool.

    See also the ParametrizeCamera_NativeParameterAccess sample for the 'native'
    approach for configuring a camera.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

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
        // Create an instant camera object with the camera found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        INodeMap& nodemap = camera.GetNodeMap();

        // Open the camera for accessing the parameters.
        camera.Open();

        // Get camera device information.
        cout << "Camera Device Information" << endl
            << "=========================" << endl;
        cout << "Vendor           : "
            << CStringParameter( nodemap, "DeviceVendorName" ).GetValue() << endl;
        cout << "Model            : "
            << CStringParameter( nodemap, "DeviceModelName" ).GetValue() << endl;
        cout << "Firmware version : "
            << CStringParameter( nodemap, "DeviceFirmwareVersion" ).GetValue() << endl << endl;

       // Camera settings.
        cout << "Camera Device Settings" << endl
            << "======================" << endl;


       // Set the AOI:

       // Get the integer nodes describing the AOI.
        CIntegerParameter offsetX( nodemap, "OffsetX" );
        CIntegerParameter offsetY( nodemap, "OffsetY" );
        CIntegerParameter width( nodemap, "Width" );
        CIntegerParameter height( nodemap, "Height" );

        // On some cameras, the offsets are read-only.
        // Therefore, we must use "Try" functions that only perform the action
        // when parameters are writable. Otherwise, we would get an exception.
        offsetX.TrySetToMinimum();
        offsetY.TrySetToMinimum();

        // Some properties have restrictions.
        // We use API functions that automatically perform value corrections.
        // Alternatively, you can use GetInc() / GetMin() / GetMax() to make sure you set a valid value.
        width.SetValue( 202, IntegerValueCorrection_Nearest );
        height.SetValue( 101, IntegerValueCorrection_Nearest );

        cout << "OffsetX          : " << offsetX.GetValue() << endl;
        cout << "OffsetY          : " << offsetY.GetValue() << endl;
        cout << "Width            : " << width.GetValue() << endl;
        cout << "Height           : " << height.GetValue() << endl;



        // Access the PixelFormat enumeration type node.
        CEnumParameter pixelFormat( nodemap, "PixelFormat" );

        // Remember the current pixel format.
        String_t oldPixelFormat = pixelFormat.GetValue();
        cout << "Old PixelFormat  : " << oldPixelFormat << endl;

        // Set the pixel format to Mono8 if available.
        if (pixelFormat.CanSetValue( "Mono8" ))
        {
            pixelFormat.SetValue( "Mono8" );
            cout << "New PixelFormat  : " << pixelFormat.GetValue() << endl;
        }


        // Set the new gain to 50% ->  Min + ((Max-Min) / 2).
        //
        // Note: Some newer camera models may have auto functions enabled.
        //       To be able to set the gain value to a specific value
        //       the Gain Auto function must be disabled first.
        // Access the enumeration type node GainAuto.
        // We use a "Try" function that only performs the action if the parameter is writable.
        CEnumParameter gainAuto( nodemap, "GainAuto" );
        gainAuto.TrySetValue( "Off" );


        // Check to see which Standard Feature Naming Convention (SFNC) is used by the camera device.
        if (camera.GetSfncVersion() >= Sfnc_2_0_0)
        {
            // Access the Gain float type node. This node is available for USB camera devices.
            // USB camera devices are compliant to SFNC version 2.0.
            CFloatParameter gain( nodemap, "Gain" );
            if (gain.TrySetValuePercentOfRange( 50.0 ))
            {
                cout << "Gain (50%)       : " << gain.GetValue() << " (Min: " << gain.GetMin() << "; Max: " << gain.GetMax() << ")" << endl;
            }
        }
        else
        {
            // Access the GainRaw integer type node. This node is available for GigE camera devices.
            CIntegerParameter gainRaw( nodemap, "GainRaw" );
            if (gainRaw.TrySetValuePercentOfRange( 50.0 ))
            {
                cout << "Gain (50%)       : " << gainRaw.GetValue() << " (Min: " << gainRaw.GetMin() << "; Max: " << gainRaw.GetMax() << "; Inc: " << gainRaw.GetInc() << ")" << endl;
            }
        }


        // Restore the old pixel format.
        pixelFormat.SetValue( oldPixelFormat );

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

