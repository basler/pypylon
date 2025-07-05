// ParametrizeCamera_LookupTable.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample program demonstrates the use of the Luminance Lookup Table feature.
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

        cout << "Opening camera...";

        // Open the camera.
        camera.Open();

        cout << "done" << endl;

        cout << "Writing LUT....";

        // Select the lookup table using the LUTSelector.
        camera.LUTSelector.SetValue( LUTSelector_Luminance );

        // Some cameras have 10 bit and others have 12 bit lookup tables, so determine
        // the type of the lookup table for the current device.
        const int nValues = (int) camera.LUTIndex.GetMax() + 1;
        int inc;
        if (nValues == 4096) // 12 bit LUT.
            inc = 8;
        else if (nValues == 1024) // 10 bit LUT.
            inc = 2;
        else
        {
            throw RUNTIME_EXCEPTION( "Type of LUT is not supported by this sample." );
        }

        // Use LUTIndex and LUTValue parameter to access the lookup table values.
        // The following lookup table causes an inversion of the sensor values.

        for (int i = 0; i < nValues; i += inc)
        {
            camera.LUTIndex.SetValue( i );
            camera.LUTValue.SetValue( nValues - 1 - i );
        }

        cout << "done" << endl;

        // Enable the lookup table.
        camera.LUTEnable.SetValue( true );

        // Grab and process images here.
        // ...

        // Disable the lookup table.
        camera.LUTEnable.SetValue( false );

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

