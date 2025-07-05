// Grab_UsingExposureEndEvent.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample shows how to use the Exposure End event to speed up image acquisition.
    For example, when a sensor exposure is finished, the camera can send an Exposure End event to the computer.
    The computer can receive the event before the image data of the finished exposure has been transferred completely.
    This avoids unnecessary delays, e.g., when an image object moves before the related image data transfer is complete.

    Note: This sample shows how to match incoming images using the camera.EventExposureEndFrameID
          and the ptrGrabResult->GetBlockID() values. For ace 2 camera models,
          camera.EventExposureEndFrameID and ptrGrabResult->GetBlockID() don't contain matching values.
          The ptrGrabResult->GetBlockID() equivalent is the chunk value represented by the camera.ChunkSelector FrameID.
          Please see the Grab_ChunkImage sample for more information about how to determine the
          correct chunk value to use instead of ptrGrabResult->GetBlockID().
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include files used by samples.
#include "../include/ConfigurationEventPrinter.h"

#include <iomanip>

#ifdef PYLON_UNIX_BUILD
#    include <sys/time.h>
#endif

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using cout.
using namespace std;

// Enumeration used for distinguishing different events.
enum MyEvents
{
    eMyExposureEndEvent,      // Triggered by a camera event.
    eMyImageReceivedEvent,    // Triggered by the receipt of an image.
    eMyMoveEvent,             // Triggered when the imaged item or the sensor head can be moved.
    eMyNoEvent                // Used as default setting.
};

// Names of possible events for printed output.
const char* MyEventNames[] =
{
    "ExposureEndEvent     ",
    "ImageReceived        ",
    "Move                 ",
    "NoEvent              "
};

// Used for logging received events without outputting the information on the screen
// because outputting will change the timing.
// This class is used for demonstration purposes only.
struct LogItem
{
    LogItem()
        : eventType( eMyNoEvent )
        , frameNumber( 0 )
    {
    }

    LogItem( MyEvents event, uint16_t frameNr )
        : eventType( event )
        , frameNumber( frameNr )
    {
        //Warning. The values measured may not be correct on older computer hardware.
#if defined(PYLON_WIN_BUILD)
        QueryPerformanceCounter( &time );
#elif defined(PYLON_UNIX_BUILD)
        struct timeval tv;

        gettimeofday( &tv, NULL );
        time = static_cast<unsigned long long>(tv.tv_sec) * 1000L + static_cast<unsigned long long>(tv.tv_usec) / 1000LL;
#endif
    }


#if defined(PYLON_WIN_BUILD)
    LARGE_INTEGER time; // Timestamps recorded.
#elif defined(PYLON_UNIX_BUILD)
    unsigned long long time; // Timestamps recorded.
#endif
    MyEvents eventType; // Type of the event received.
    uint16_t frameNumber; // Frame number of the event received.
};


// Helper function for printing a log.
// This function is used for demonstration purposes only.
void PrintLog( const std::vector<LogItem>& aLog )
{
#if defined(PYLON_WIN_BUILD)
    // Get the computer timer frequency.
    LARGE_INTEGER timerFrequency;
    QueryPerformanceFrequency( &timerFrequency );
#endif

    cout << std::endl << "Warning. The time values printed may not be correct on older computer hardware." << std::endl << std::endl;
    // Print the event information header.
    cout << "Time [ms]    " << "Event                 " << "Frame Number" << std::endl;
    cout << "------------ " << "--------------------- " << "-----------" << std::endl;

    // Print the logged information.
    size_t logSize = aLog.size();
    for (size_t i = 0; i < logSize; ++i)
    {
        // Calculate the time elapsed between the events.
        double time_ms = 0;
        if (i)
        {
#if defined(PYLON_WIN_BUILD)
            __int64 oldTicks = ((__int64) aLog[i - 1].time.HighPart << 32) + (__int64) aLog[i - 1].time.LowPart;
            __int64 newTicks = ((__int64) aLog[i].time.HighPart << 32) + (__int64) aLog[i].time.LowPart;
            long double timeDifference = (long double) (newTicks - oldTicks);
            long double ticksPerSecond = (long double) (((__int64) timerFrequency.HighPart << 32) + (__int64) timerFrequency.LowPart);
            time_ms = (timeDifference / ticksPerSecond) * 1000;
#elif defined(PYLON_UNIX_BUILD)
            time_ms = aLog[i].time - aLog[i - 1].time;
#endif
        }

        // Print the event information.
        cout << setw( 12 ) << fixed << setprecision( 4 ) << time_ms << " " << MyEventNames[aLog[i].eventType] << " " << aLog[i].frameNumber << std::endl;
    }
}


// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 20;


// Example handler for GigE camera events.
// Additional handling is required for GigE camera events because the event network packets may get lost, duplicated, or delayed in the network.
class CEventHandler : public CBaslerUniversalCameraEventHandler, public CBaslerUniversalImageEventHandler
{
public:
    CEventHandler()
        : m_nextExpectedFrameNumberImage( 0 )
        , m_nextExpectedFrameNumberExposureEnd( 0 )
        , m_nextFrameNumberForMove( 0 )
        , m_isGigE( false )
    {
        // Reserve space to log camera, image, and move events.
        m_log.reserve( c_countOfImagesToGrab * 3 );
    }

    void Initialize( int value, bool isGigE )
    {
        m_nextExpectedFrameNumberImage = value;
        m_nextExpectedFrameNumberExposureEnd = value;
        m_nextFrameNumberForMove = value;
        m_isGigE = isGigE;
    }

    // This method is called when a camera event has been received.
    virtual void OnCameraEvent( CBaslerUniversalInstantCamera& camera, intptr_t userProvidedId, GenApi::INode* /* pNode */ )
    {
        if (userProvidedId == eMyExposureEndEvent)
        {
            // An Exposure End event has been received.
            uint16_t frameNumber;
            if (camera.GetSfncVersion() < Sfnc_2_0_0)
            {
                frameNumber = (uint16_t) camera.ExposureEndEventFrameID.GetValue();
            }
            else
            {
                frameNumber = (uint16_t) camera.EventExposureEndFrameID.GetValue();
            }
            m_log.push_back( LogItem( eMyExposureEndEvent, frameNumber ) );

            if (GetIncrementedFrameNumber( frameNumber ) != m_nextExpectedFrameNumberExposureEnd)
            {
                // Check whether the imaged item or the sensor head can be moved.
                if (frameNumber == m_nextFrameNumberForMove)
                {
                    MoveImagedItemOrSensorHead();
                }

                // Check for missing Exposure End events.
                if (frameNumber != m_nextExpectedFrameNumberExposureEnd)
                {
                    throw RUNTIME_EXCEPTION( "An Exposure End event has been lost. Expected frame number is %d but got frame number %d.", m_nextExpectedFrameNumberExposureEnd, frameNumber );
                }
                IncrementFrameNumber( m_nextExpectedFrameNumberExposureEnd );
            }
        }
        else
        {
            PYLON_ASSERT2( false, "The sample has been modified and a new event has been registered. Add handler code above." );
        }
    }

    // This method is called when an image has been grabbed.
    virtual void OnImageGrabbed( CBaslerUniversalInstantCamera& /*camera*/, const CBaslerUniversalGrabResultPtr& ptrGrabResult )
    {
        // An image has been received.
        uint16_t frameNumber = (uint16_t) ptrGrabResult->GetBlockID();
        m_log.push_back( LogItem( eMyImageReceivedEvent, frameNumber ) );

        // Check whether the imaged item or the sensor head can be moved.
        // This will be the case if the Exposure End has been lost or if the Exposure End is received later than the image.
        if (frameNumber == m_nextFrameNumberForMove)
        {
            MoveImagedItemOrSensorHead();
        }

        // Check for missing images.
        if (frameNumber != m_nextExpectedFrameNumberImage)
        {
            throw RUNTIME_EXCEPTION( "An image has been lost. Expected frame number is %d but got frame number %d.", m_nextExpectedFrameNumberImage, frameNumber );
        }
        IncrementFrameNumber( m_nextExpectedFrameNumberImage );
    }

    void MoveImagedItemOrSensorHead()
    {
        // The imaged item or the sensor head can be moved now...
        // The camera may not be ready yet for a trigger at this point because the sensor is still being read out.
        // See the documentation of the CInstantCamera::WaitForFrameTriggerReady() method for more information.
        m_log.push_back( LogItem( eMyMoveEvent, m_nextFrameNumberForMove ) );
        IncrementFrameNumber( m_nextFrameNumberForMove );
    }

    void PrintLog()
    {
        ::PrintLog( m_log );
    }

private:
    void IncrementFrameNumber( uint16_t& frameNumber )
    {
        frameNumber = GetIncrementedFrameNumber( frameNumber );
    }

    uint16_t GetIncrementedFrameNumber( uint16_t frameNumber )
    {
        ++frameNumber;

        if (m_isGigE)
        {
            if (frameNumber == 0)
            {
                // Zero is not a valid frame number.
                ++frameNumber;
            }
        }


        return frameNumber;
    }

    uint16_t m_nextExpectedFrameNumberImage;
    uint16_t m_nextExpectedFrameNumberExposureEnd;
    uint16_t m_nextFrameNumberForMove;

    bool m_isGigE;

    std::vector<LogItem> m_log;
};



int main( int /*argc*/, char* /*argv*/[] )
{
    // Exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create the event handler.
        CEventHandler eventHandler;

        // Create an instant camera object with the first camera device found.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Camera models behave differently regarding IDs and counters. Set initial values.
        if (camera.IsGigE())
        {
            eventHandler.Initialize( 1, true );
        }
        else
        {
            eventHandler.Initialize( 0, false );
        }


        // For demonstration purposes only, add sample configuration event handlers to print information
        // about camera use and image grabbing.
        camera.RegisterConfiguration( new CConfigurationEventPrinter, RegistrationMode_Append, Cleanup_Delete ); // Camera use.

        // Register the event handler.
        camera.RegisterImageEventHandler( &eventHandler, RegistrationMode_Append, Cleanup_None );

        // Camera event processing must be enabled first. The default is off.
        camera.GrabCameraEvents = true;

        // Open the camera to configure parameters.
        camera.Open();

        // Check whether the device supports events.
        if (!camera.EventSelector.IsWritable())
        {
            throw RUNTIME_EXCEPTION( "The device doesn't support events." );
        }

        if (camera.GetSfncVersion() < Sfnc_2_0_0)
        {
            camera.RegisterCameraEventHandler( &eventHandler, "ExposureEndEventData", eMyExposureEndEvent, RegistrationMode_ReplaceAll, Cleanup_None );
        }
        else
        {
            camera.RegisterCameraEventHandler( &eventHandler, "EventExposureEndData", eMyExposureEndEvent, RegistrationMode_ReplaceAll, Cleanup_None );
        }


        // Enable the sending of Exposure End events.
        // Select the event to be received.
        if (camera.EventSelector.TrySetValue( EventSelector_ExposureEnd ))
        {   // Enable it.
            if (!camera.EventNotification.TrySetValue( EventNotification_On ))
            {
                // scout-f, scout-g, and aviator GigE cameras use a different value.
                camera.EventNotification.SetValue( EventNotification_GenICamEvent );
            }
        }


        // Start grabbing of c_countOfImagesToGrab images.
        // The camera device is operated in a default configuration that
        // sets up free-running continuous acquisition.
        camera.StartGrabbing( c_countOfImagesToGrab );

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        // when c_countOfImagesToGrab images have been retrieved.
        while (camera.IsGrabbing())
        {
            // Retrieve grab results and notify the camera event and image event handlers.
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );
            // Nothing to do here with the grab result The grab results are handled by the registered event handlers.
        }

        // Disable the sending of Exposure End events.
        if (camera.EventSelector.TrySetValue( EventSelector_ExposureEnd ))
        {
            camera.EventNotification.SetValue( EventNotification_Off );
        }

        // Disable the sending of Frame Start Overtrigger events.
        if (camera.EventSelector.TrySetValue( EventSelector_FrameStartOvertrigger ))
        {
            camera.EventNotification.SetValue( EventNotification_Off );
        }

        if (camera.EventSelector.TrySetValue( EventSelector_EventOverrun ))
        {

            // Disable sending Event Overrun events.
            camera.EventSelector.SetValue( EventSelector_EventOverrun );
            camera.EventNotification.SetValue( EventNotification_Off );
        }

        // Print the recorded log showing the timing of events and images.
        eventHandler.PrintLog();
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

