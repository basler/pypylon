// Grab_MultiCast.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample demonstrates how to open a camera in multicast mode
    and how to receive a multicast stream.

    Two instances of this application must be started simultaneously on different computers.
    The first application started on computer A acts as the controlling application and has full access to the GigE camera.
    The second instance started on computer B opens the camera in monitor mode.
    This instance is not able to control the camera but can receive multicast streams.

    To get the sample running, start this application first on computer A in control mode.
    After computer A has begun to receive frames, start the second instance of this
    application on computer B in monitor mode.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Include files used by samples.
#include "../include/ConfigurationEventPrinter.h"
#include "../include/ImageEventPrinter.h"

// Include file for _kbhit
#if defined(PYLON_WIN_BUILD)
#include <conio.h>
#elif defined(PYLON_UNIX_BUILD)
#    include <stdio.h>
#    include <termios.h>
#    include <unistd.h>
#    include <fcntl.h>
#endif

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;
using namespace Basler_UniversalStreamParams;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 100;


bool KeyPressed( void )
{
#if defined(PYLON_WIN_BUILD)
    return _kbhit() != 0;
#elif defined(PYLON_UNIX_BUILD)
    struct termios savedTermios;
    int savedFL;
    struct termios termios;
    int ch;

    tcgetattr( STDIN_FILENO, &savedTermios );
    savedFL = fcntl( STDIN_FILENO, F_GETFL, 0 );

    termios = savedTermios;
    termios.c_lflag &= ~(ICANON | ECHO);
    tcsetattr( STDIN_FILENO, TCSANOW, &termios );
    fcntl( STDIN_FILENO, F_SETFL, savedFL | O_NONBLOCK );

    ch = getchar();

    fcntl( STDIN_FILENO, F_SETFL, savedFL );
    tcsetattr( STDIN_FILENO, TCSANOW, &savedTermios );

    if (ch != EOF)
    {
        ungetc( ch, stdin );
    }

    return ch != EOF;
#endif
}

int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    char key;
    bool monitorMode = false;

    try
    {
        // Only look for GigE cameras.
        CDeviceInfo info;
        info.SetDeviceClass( Pylon::BaslerGigEDeviceClass );

        // Create an instant camera object for the GigE camera found first.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice( info ) );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Query the user for the mode to use.
        // Ask the user to launch the multicast controlling application or the multicast monitoring application.
        cout << "Start multicast sample in (c)ontrol or in (m)onitor mode? (c/m) "; cout.flush();

        do
        {
            cin.get( key );
            // Remove newline from stdin.
            cin.get();
        } while ((key != 'c') && (key != 'm') && (key != 'C') && (key != 'M'));

        monitorMode = (key == 'm') || (key == 'M');

        // The default configuration must be removed when monitor mode is selected
        // because the monitoring application is not allowed to modify any parameter settings.
        if (monitorMode)
        {
            camera.RegisterConfiguration( (CConfigurationEventHandler*) NULL, RegistrationMode_ReplaceAll, Cleanup_None );
        }

        // For demonstration purposes only, registers an event handler configuration to print out information about camera use.
        // The event handler configuration is appended to the registered software trigger configuration handler by setting 
        // registration mode to RegistrationMode_Append.
        camera.RegisterConfiguration( new CConfigurationEventPrinter, RegistrationMode_Append, Cleanup_Delete ); // Camera use.
        camera.RegisterImageEventHandler( new CImageEventPrinter, RegistrationMode_Append, Cleanup_Delete );     // Image grabbing.

        // Monitor mode selected.
        if (monitorMode)
        {
            // Set MonitorModeActive to true to act as monitor
            camera.MonitorModeActive = true;

            // Open the camera.
            camera.Open();

            // Select transmission type. If the camera is already controlled by another application
            // and configured for multicast, the active camera configuration can be used
            // (IP Address and Port will be set automatically).
            camera.GetStreamGrabberParams().TransmissionType = TransmissionType_UseCameraConfig;

            // Alternatively, the stream grabber could be explicitly set to "multicast"...
            // In this case, the IP Address and the IP port must also be set.
            //
            //camera.GetStreamGrabberParams().TransmissionType = TransmissionType_Multicast;
            //camera.GetStreamGrabberParams().DestinationAddr = "239.0.0.1";
            //camera.GetStreamGrabberParams().DestinationPort = 49152;

            if (camera.GetStreamGrabberParams().DestinationAddr.GetValue() != "0.0.0.0" &&
                 camera.GetStreamGrabberParams().DestinationPort.GetValue() != 0)
            {
                camera.StartGrabbing( c_countOfImagesToGrab );
            }
            else
            {
                cerr << endl << "Failed to open stream grabber (monitor mode): The acquisition is not yet started by the controlling application." << endl;
                cerr << endl << "Start the controlling application before starting the monitor application" << endl;
            }
        }
        // Controlling mode selected.
        else
        {
            // Open the camera.
            camera.Open();

            // Set transmission type to "multicast"...
            // In this case, the IP Address and the IP port must also be set.
            camera.GetStreamGrabberParams().TransmissionType = TransmissionType_Multicast;
            // camera.GetStreamGrabberParams().DestinationAddr = "239.0.0.1";    // These are default values.
            // camera.GetStreamGrabberParams().DestinationPort = 49152;

            // Maximize the image area of interest (Image AOI).
            camera.OffsetX.TrySetToMinimum();
            camera.OffsetY.TrySetToMinimum();
            camera.Width.SetToMaximum();
            camera.Height.SetToMaximum();

            // Set the pixel data format.
            camera.PixelFormat.SetValue( PixelFormat_Mono8 );

            camera.StartGrabbing();
        }

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        // when c_countOfImagesToGrab images have been retrieved in monitor mode
        // or when a key is pressed and the camera object is destroyed.
        while (!KeyPressed() && camera.IsGrabbing())
        {
            // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );

#ifdef PYLON_WIN_BUILD
            // Display the image
            Pylon::DisplayImage( 1, ptrGrabResult );
#endif

            // The grab result could now be processed here.
        }
    }
    catch (const GenericException& e)
    {
        // Error handling
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following three lines to disable wait on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}

