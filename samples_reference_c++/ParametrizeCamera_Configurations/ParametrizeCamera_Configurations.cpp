// ParametrizeCamera_Configurations.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    The instant camera allows to install event handlers for configuration purposes
    and for handling the grab results. This is very useful for handling standard
    camera setups and image processing tasks.

    This sample shows how to use configuration event handlers by applying the standard
    configurations and registering sample configuration event handlers.

    Configuration event handlers are derived from the CConfigurationEventHandler base class.
    CConfigurationEventHandler provides virtual methods that can be overridden. If the
    configuration event handler is registered these methods are called when the state of the
    instant camera objects changes, e.g. when the camera object is opened or closed.

    The standard configuration event handlers override the OnOpened method. The overridden method
    parametrizes the camera.

    Device specific camera classes, e.g. for GigE cameras, provide specialized
    event handler base classes, e.g. CBaslerGigEConfigurationEventHandler.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include files used by samples.
#include "../include/ImageEventPrinter.h"
#include "../include/ConfigurationEventPrinter.h"
#include "../include/PixelFormatAndAoiConfiguration.h"

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 3;


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object with the first camera device found.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // For demonstration purposes only, register an image event handler.
        // printing out information about the grabbed images.
        camera.RegisterImageEventHandler( new CImageEventPrinter, RegistrationMode_Append, Cleanup_Delete );

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;



        cout << "Grab using continuous acquisition:" << endl << endl;

        // Register the standard configuration event handler for setting up the camera for continuous acquisition.
        // By setting the registration mode to RegistrationMode_ReplaceAll, the new configuration handler replaces the
        // default configuration handler that has been automatically registered when creating the
        // instant camera object.
        // The handler is automatically deleted when deregistered or when the registry is cleared if Cleanup_Delete is specified.
        camera.RegisterConfiguration( new CAcquireContinuousConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // The camera's Open() method calls the configuration handler's OnOpened() method that
        // applies the required parameter modifications.
        camera.Open();

        // The registered configuration event handler has done its parametrization now.
        // Additional parameters could be set here.

        // Grab some images for demonstration.
        camera.StartGrabbing( c_countOfImagesToGrab );
        while (camera.IsGrabbing())
        {
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );
        }

        // Close the camera.
        camera.Close();



        cout << "Grab using software trigger mode:" << endl << endl;

        // Register the standard configuration event handler for setting up the camera for software
        // triggering.
        // The current configuration is replaced by the software trigger configuration by setting the
        // registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CSoftwareTriggerConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // StartGrabbing() calls the camera's Open() automatically if the camera is not open yet.
        // The Open method calls the configuration handler's OnOpened() method that
        // sets the required parameters for enabling software triggering.

        // Grab some images for demonstration.
        camera.StartGrabbing( c_countOfImagesToGrab );
        while (camera.IsGrabbing())
        {
            // Execute the software trigger. The call waits up to 1000 ms for the camera
            // to be ready to be triggered.
            camera.WaitForFrameTriggerReady( 1000, TimeoutHandling_ThrowException );
            camera.ExecuteSoftwareTrigger();
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );
        }
        // StopGrabbing() is called from RetrieveResult if the number of images
        // to grab has been reached. Since the camera was opened by StartGrabbing()
        // it is closed by StopGrabbing().

        // The CSoftwareTriggerConfiguration, like all standard configurations, is provided as a header file.
        // The source code can be copied and modified to meet application specific needs, e.g.
        // the CSoftwareTriggerConfiguration class could easily be changed into a hardware trigger configuration.



        cout << "Grab using single frame acquisition:" << endl << endl;

        // Register the standard configuration event handler for configuring single frame acquisition.
        // The previous configuration is removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CAcquireSingleFrameConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // GrabOne calls StartGrabbing and StopGrabbing internally.
        // As seen above Open() is called by StartGrabbing and
        // the OnOpened() method of the CAcquireSingleFrameConfiguration handler is called.
        camera.GrabOne( 5000, ptrGrabResult );

        // To continuously grab single images it is much more efficient to open the camera before grabbing.
        // Note: The software trigger mode (see above) should be used for grabbing single images if you want to maximize frame rate.

        // Now, the camera parameters are applied in the OnOpened method of the configuration object.
        camera.Open();

        // Additional parameters could be set here.

        // Grab some images for demonstration.
        camera.GrabOne( 5000, ptrGrabResult );
        camera.GrabOne( 5000, ptrGrabResult );
        camera.GrabOne( 5000, ptrGrabResult );

        // Close the camera.
        camera.Close();



        cout << "Grab using multiple configuration objects:" << endl << endl;

        // Register the standard event handler for configuring single frame acquisition.
        // The current configuration is replaced by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CAcquireSingleFrameConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // Register an additional configuration handler to set the image format and adjust the AOI.
        // By setting the registration mode to RegistrationMode_Append, the configuration handler is added instead of replacing
        // the already registered configuration handler.
        camera.RegisterConfiguration( new CPixelFormatAndAoiConfiguration, RegistrationMode_Append, Cleanup_Delete );

        // Create an event printer on the heap.
        CConfigurationEventPrinter* pEventPrinterObject = new CConfigurationEventPrinter;
        // Register the handler object and define Cleanup_None so that it is not deleted by the camera object.
        // It must be ensured, that the configuration handler "lives" at least until the handler is deregistered!
        camera.RegisterConfiguration( pEventPrinterObject, RegistrationMode_Append, Cleanup_None );

        // Grab an image for demonstration. Configuration events are printed.
        cout << endl << "Grab, configuration events are printed:" << endl << endl;
        camera.GrabOne( 5000, ptrGrabResult );

        // Deregister the event handler.
        camera.DeregisterConfiguration( pEventPrinterObject );
        // The event handler can now be deleted.
        delete pEventPrinterObject;
        pEventPrinterObject = NULL;

        // Grab an image for demonstration. Configuration events are not printed.
        cout << endl << "Grab, configuration events are not printed:" << endl << endl;
        camera.GrabOne( 5000, ptrGrabResult );
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
