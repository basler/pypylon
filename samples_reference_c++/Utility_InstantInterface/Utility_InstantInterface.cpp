// Utility_InstantInterface.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to use CInstantInterface to access parameters of the interface.
    Using the Basler CXP-12 interface card as an example, the sample shows you how to access the Power-Over-CXP settings
    and monitor the power usage.
*/

// Include file to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use cout
#include <iostream>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonAutoInitTerm autoInitTerm;

    try
    {
        // Open the first interface on the CXP interface card.
        CInterfaceInfo info;
        info.SetDeviceClass( Pylon::BaslerGenTlCxpDeviceClass );

        CUniversalInstantInterface instantInterface( info );
        instantInterface.Open();
        cout << "Interface opened." << endl;

        cout << " ExternalPowerPresent: ";
        if( instantInterface.ExternalPowerPresent.GetValue() ) 
        {
            cout << "yes" << endl;

            cout << " Switching power OFF." << endl;
            instantInterface.CxpPoCxpTurnOff.Execute();
            WaitObject::Sleep( 1000 );

            cout << " Switching power ON." << endl;
            instantInterface.CxpPoCxpAuto.Execute();
            // wait for 5000 ms (5 s) to allow the camera to start up again
            WaitObject::Sleep( 5000 );

            cout << " Updating device list." << endl;
            instantInterface.DeviceUpdateList.Execute();

            double current = instantInterface.CxpPort0Current();
            double voltage = instantInterface.CxpPort0Voltage();
            double power = instantInterface.CxpPort0Power();
            cout << fixed;
            cout.precision( 2 );
            cout << "  Port 0 :" << endl;
            cout << "   Current " << current << " mA" << endl;
            cout << "   Voltage " << voltage << " V" << endl;
            cout << "   Power " << power << " W" << endl << endl;
        }
        else
        {
            cout << "no" << endl;
        }

        instantInterface.Close();
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

    // All pylon resources are automatically released when autoInitTerm goes out of scope.

    return exitCode;
}
