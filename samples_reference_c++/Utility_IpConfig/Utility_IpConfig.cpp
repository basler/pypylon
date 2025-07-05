// Utility_IpConfig.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample demonstrates how to configure the IP address of a camera.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#include <pylon/gige/GigETransportLayer.h>
#include <algorithm>
#include <iostream>
#include <cctype>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;



int main( int argc, char* argv[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonAutoInitTerm autoInitTerm;

    try
    {
        // Create GigE transport layer.
        CTlFactory& TlFactory = CTlFactory::GetInstance();
        IGigETransportLayer* pTl = dynamic_cast<IGigETransportLayer*>(TlFactory.CreateTl( Pylon::BaslerGigEDeviceClass ));
        if (pTl == NULL)
        {
            cerr << "Error: No GigE transport layer installed." << endl;
            cerr << "       Please install GigE support as it is required for this sample." << endl;
            return 1;
        }

        // Enumerate devices.
        DeviceInfoList_t lstDevices;
        pTl->EnumerateAllDevices( lstDevices );

        for (DeviceInfoList_t::const_iterator it = lstDevices.begin(); it != lstDevices.end(); ++it)
        {
            cout << "Using device: " << it->GetModelName() << endl;
        }

        cout << endl;

        // Check if enough parameters are given.
        if (argc < 3)
        {
            // Print usage information.
            cout << "Usage: Utility_IpConfig <MAC> <IP> [MASK] [GATEWAY]" << endl;
            cout << "       <MAC> is the MAC address without separators, e.g., 0030531596CF" << endl;
            cout << "       <IP> is one of the following:" << endl;
            cout << "            - AUTO to use Auto-IP (LLA)." << endl;
            cout << "            - DHCP to use DHCP." << endl;
            cout << "            - Everything else is interpreted as a new IP address in dotted notation, e.g., 192.168.1.1" << endl;
            cout << "       [MASK] is the network mask in dotted notation. This is optional. 255.255.255.0 is used as default." << endl;
            cout << "       [GATEWAY] is the gateway address in dotted notation. This is optional. 0.0.0.0 is used as default." << endl;
            cout << "Please note that this is a sample and no sanity checks are made." << endl;
            cout << endl;

            // Print header for information table.
            cout << left << setfill( ' ' );
            cout << endl;
            cout.width( 32 + 14 + 17 + 17 + 15 + 8 );
            cout << "Available Devices";
            cout.width( 15 );
            cout << "   supports " << endl;
            cout.width( 32 );
            cout << "Friendly Name";
            cout.width( 14 );
            cout << "MAC";
            cout.width( 17 );
            cout << "IP Address";
            cout.width( 17 );
            cout << "Subnet Mask";
            cout.width( 15 );
            cout << "Gateway";
            cout.width( 8 );
            cout << "Mode";
            cout.width( 4 );
            cout << "IP?";
            cout.width( 6 );
            cout << "DHCP?";
            cout.width( 5 );
            cout << "LLA?";
            cout << endl;

            // Print information table.
            for (DeviceInfoList_t::const_iterator it = lstDevices.begin(); it != lstDevices.end(); ++it)
            {
                // Determine current configuration mode.
                String_t activeMode;
                if (it->IsPersistentIpActive())
                {
                    activeMode = "Static";
                }
                else if (it->IsDhcpActive())
                {
                    activeMode = "DHCP";
                }
                else
                {
                    activeMode = "AutoIP";
                }

                cout.width( 32 );
                cout << it->GetFriendlyName();
                cout.width( 14 );
                cout << it->GetMacAddress();
                cout.width( 17 );
                cout << it->GetIpAddress();
                cout.width( 17 );
                cout << it->GetSubnetMask();
                cout.width( 15 );
                cout << it->GetDefaultGateway();
                cout.width( 8 );
                cout << activeMode;
                cout.width( 4 );
                cout << it->IsPersistentIpSupported();
                cout.width( 6 );
                cout << it->IsDhcpSupported();
                cout.width( 5 );
                cout << it->IsAutoIpSupported();
                cout << endl;
            }

            exitCode = 1;
        }
        else
        {
            // Read arguments. Note that sanity checks are skipped for clarity.
            String_t macAddress = argv[1];
            String_t ipAddress = argv[2];
            String_t subnetMask = "255.255.255.0";
            if (argc >= 4)
            {
                subnetMask = argv[3];
            }
            String_t defaultGateway = "0.0.0.0";
            if (argc >= 5)
            {
                defaultGateway = argv[4];
            }

            // Check if configuration mode is AUTO, DHCP, or IP address.
            bool isAuto = (strcmp( argv[2], "AUTO" ) == 0);
            bool isDhcp = (strcmp( argv[2], "DHCP" ) == 0);
            bool isStatic = !isAuto && !isDhcp;

            // Find the camera's user-defined name.
            String_t userDefinedName = "";
            for (DeviceInfoList_t::const_iterator it = lstDevices.begin(); it != lstDevices.end(); ++it)
            {
                if (macAddress == it->GetMacAddress())
                {
                    userDefinedName = it->GetUserDefinedName();
                }
            }

            // Set new IP configuration.
            bool setOk = pTl->BroadcastIpConfiguration( macAddress, isStatic, isDhcp,
                                                        ipAddress, subnetMask, defaultGateway, userDefinedName );

                                                    // Show result message.
            if (setOk)
            {
                pTl->RestartIpConfiguration( macAddress );
                cout << "Successfully changed IP configuration via broadcast for device " << macAddress << " to " << ipAddress << endl;
            }
            else
            {
                cout << "Failed to change IP configuration via broadcast for device " << macAddress << endl;
                cout << "This is not an error. The device may not support broadcast IP configuration." << endl;
            }
        }

        // Comment the following two lines to disable waiting on exit.
        cerr << endl << "Press enter to exit." << endl;
        while (cin.get() != '\n');

        // Release transport layer.
        TlFactory.ReleaseTl( pTl );
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
            << e.GetDescription() << endl;
        exitCode = 1;
    }

    return exitCode;
}
