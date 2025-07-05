// camera/main.cpp
/*
    Sample demonstrating how to use and parameterize the Camera vTool (no license required).
    Note: The Recipe Code Generator of the pylon Viewer allows you to generate
          sample code to use your vTool recipe in your development environment.
*/
// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#  include <pylon/PylonGUI.h>
#endif
// Extend the pylon API for using pylon data processing
#include <pylondataprocessing/PylonDataProcessingIncludes.h>
// The sample uses the std::list
#include <list>

// Namespaces for using pylon objects
using namespace Pylon;
using namespace Pylon::DataProcessing;

// Namespace for using cout
using namespace std;

// Number of images to be grabbed
static const uint32_t c_countOfImagesToGrab = 100;

// Declare a data class for one set of output data values.
class ResultData
{
public:
    ResultData()
        : hasError(false)
    {
    }

    CPylonImage image; // The image from the camera

    bool hasError;     // If something doesn't work as expected
                       // while processing data, this is set to true.

    String_t errorMessage; // Contains an error message if
                           // hasError has been set to true.
};


// MyOutputObserver is a helper object that shows how to handle output data
// provided via the IOutputObserver::OutputDataPush interface method.
// Also, MyOutputObserver shows how a thread-safe queue can be implemented
// for later processing while pulling the output data.
// Note: The pylon Viewer provides the Recipe Code Generator feature to generate
// the necessary code to handle the output data of your recipe, like this class.
// Note: Alternatively, you can use the CGenericOutputObserver. For more information,
// see the samples, e.g., the Barcode sample.
class MyOutputObserver : public IOutputObserver
{
public:
    MyOutputObserver()
        : m_waitObject(WaitObjectEx::Create())
    {
    }

    // Implements IOutputObserver::OutputDataPush.
    // This method is called when an output of the CRecipe pushes data out.
    // The call of the method can be performed by any thread of the thread pool of the recipe.
    void OutputDataPush(
        CRecipe& recipe,
        CVariantContainer valueContainer,
        const CUpdate& update,
        intptr_t userProvidedId) override
    {
        // The following variables are not used here:
        PYLON_UNUSED(recipe);
        PYLON_UNUSED(update);
        PYLON_UNUSED(userProvidedId);

        ResultData currentResultData;

        // Get the data provided by the recipe output pin "Image".
        // The value container is a dictionary/map-like type.
        // Look for the key in the dictionary.
        auto pos = valueContainer.find("Image");
        // We expect there to be an image
        // because this is the only output pin of this recipe.
        PYLON_ASSERT(pos != valueContainer.end());
        if (pos != valueContainer.end())
        {
            // Now we can use the value of the key/value pair.
            const CVariant& value = pos->second;
            if (!value.HasError())
            {
                currentResultData.image = value.ToImage();
            }
            else
            {
                currentResultData.hasError = true;
                currentResultData.errorMessage = value.GetErrorDescription();
            }
        }
        // Add data to the result queue in a thread-safe way.
        {
            AutoLock scopedLock(m_memberLock);
            m_queue.emplace_back(currentResultData);
        }

        // Signal that data is ready.
        m_waitObject.Signal();
    }

    // Get the wait object for waiting for data.
    const WaitObject& GetWaitObject()
    {
        return m_waitObject;
    }

    // Get one result data object from the queue.
    bool GetResultData(ResultData& resultDataOut)
    {
        AutoLock scopedLock(m_memberLock);
        if (m_queue.empty())
        {
            return false;
        }

        resultDataOut = std::move(m_queue.front());
        m_queue.pop_front();
        if (m_queue.empty())
        {
            m_waitObject.Reset();
        }
        return true;
    }

private:
    CLock m_memberLock;        // The member lock is required to ensure
                               // thread-safe access to the member variables.
    WaitObjectEx m_waitObject; // Signals that ResultData is available.
                               // It is set when m_queue is not empty.
    list<ResultData> m_queue;  // The queue of ResultData
};

int main(int /*argc*/, char* /*argv*/[])
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Enable the pylon camera emulator for grabbing images from disk
    // by setting the necessary environment variable.
#if defined(PYLON_WIN_BUILD)
    _putenv("PYLON_CAMEMU=1");
#elif defined(PYLON_UNIX_BUILD)
    setenv("PYLON_CAMEMU", "1", true);
#endif

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // This object is used for collecting the output data.
        // If placed on the stack it must be created before the recipe
        // so that it is destroyed after the recipe.
        MyOutputObserver resultCollector;

        // Create a recipe representing a design created using
        // the pylon Viewer Workbench.
        CRecipe recipe;

        // Load the recipe file.
        // Note: PYLON_DATAPROCESSING_CAMERA_RECIPE is a string
        // created by the CMake build files.
        recipe.Load(PYLON_DATAPROCESSING_CAMERA_RECIPE);

        // For demonstration purposes only
        // Let's check the Pylon::CDeviceInfo properties of the camera we are going to use.
        // Basler recommends using the DeviceClass and the UserDefinedName to identify a camera.
        // The UserDefinedName is taken from the DeviceUserID parameter that you can set in the pylon Viewer's Features pane.
        // Note: USB cameras must be disconnected and reconnected or reset to provide the new DeviceUserID.
        // This is due to restrictions defined by the USB standard.
        cout << "Properties used for selecting a camera device" << endl;
        CIntegerParameter devicePropertySelector = 
            recipe.GetParameters().Get(IntegerParameterName("MyCamera/@vTool/DevicePropertySelector"));
        if (devicePropertySelector.IsWritable())
        {
            CStringParameter deviceKey = recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/DevicePropertyKey"));
            CStringParameter deviceValue = recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/DevicePropertyValue"));
            for (int64_t i = devicePropertySelector.GetMin(); i <= devicePropertySelector.GetMax(); ++i)
            {
                devicePropertySelector.SetValue(i);
                cout << deviceKey.GetValue() << "=" << deviceValue.GetValue() << endl;
            }
        }
        else
        {
            cout << "The first camera device found is used." << endl;
        }

        // For demonstration purposes only
        // Print available parameters.
        {
            cout << "Parameter names before allocating resources" << endl;
            StringList_t parameterNames = recipe.GetParameters().GetAllParameterNames();
            for (const auto& name : parameterNames)
            {
                cout << name << endl;
            }
        }

        // Allocate the required resources. This includes the camera device.
        recipe.PreAllocateResources();

        // For demonstration purposes only
        cout << "Selected camera device:" << endl;
        cout << "ModelName=" << recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/SelectedDeviceModelName")).GetValueOrDefault("N/A") << std::endl;
        cout << "SerialNumber=" << recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/SelectedDeviceSerialNumber")).GetValueOrDefault("N/A") << std::endl;
        cout << "VendorName=" << recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/SelectedDeviceVendorName")).GetValueOrDefault("N/A") << std::endl;
        cout << "UserDefinedName=" << recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/SelectedDeviceUserDefinedName")).GetValueOrDefault("N/A") << std::endl;
        // StringParameterName is the type of the parameter.
        // MyCamera is the name of the vTool.
        // Use @vTool if you want to access the vTool parameters.
        // Use @CameraInstance if you want to access the parameters of the CInstantCamera object used internally.
        // Use @DeviceTransportLayer if you want to access the transport layer parameters.
        // Use @CameraDevice if you want to access the camera device parameters.
        // Use @StreamGrabber0 if you want to access the camera device parameters.
        // SelectedDeviceUserDefinedName is the name of the parameter.

        // For demonstration purposes only
        // Print available parameters after allocating resources. Now we can access the camera parameters.
        {
            cout << "Parameter names after allocating resources" << endl;
            StringList_t parameterNames = recipe.GetParameters().GetAllParameterNames();
            for (const auto& name : parameterNames)
            {
                cout << name << endl;
            }
        }


        // For demonstration purposes only
        // Print available output names.
        StringList_t outputNames;
        recipe.GetOutputNames(outputNames);
        for (const auto& outputName : outputNames)
        {
            cout << "Output found: " << outputName << std::endl;
        }

        // Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(&resultCollector, RegistrationMode_Append);

        // Start the processing. The recipe is triggered internally
        // by the camera vTool for each image.
        recipe.Start();

        int count = 0;
        bool testImage1 = true;
        CEnumParameter testImageSelector = recipe.GetParameters().Get(EnumParameterName("MyCamera/@CameraDevice/TestImageSelector|MyCamera/@CameraDevice/TestPattern"));
        for (uint32_t i = 0; i < c_countOfImagesToGrab; ++i)
        {
            if (resultCollector.GetWaitObject().Wait(5000))
            {
                ResultData result;
                resultCollector.GetResultData(result);
                if (!result.hasError)
                {
                    // Access the image data.
                    cout << "SizeX: " << result.image.GetWidth() << endl;
                    cout << "SizeY: " << result.image.GetHeight() << endl;
                    const uint8_t* pImageBuffer = (uint8_t*)result.image.GetBuffer();
                    cout << "Gray value of first pixel: " << (uint32_t)pImageBuffer[0] << endl << endl;

#ifdef PYLON_WIN_BUILD
                    DisplayImage(1, result.image);
#endif
                }
                else
                {
                    cout << "An error occurred in processing: " << result.errorMessage << endl;
                }

                ++count;

                // Now let's change a parameter every 10 images
                // while grabbing is active.
                if (0 == count % 10)
                {
                    testImage1 = !testImage1;
                    if (testImage1)
                    {
                        testImageSelector.SetValue("Testimage1");
                    }
                    else
                    {
                        testImageSelector.SetValue("Testimage2");
                    }
                }
            }
            else
            {
                throw RUNTIME_EXCEPTION("Result timeout");
            }
        }

        // Stop the processing.
        recipe.Stop();

        // Optionally, deallocate resources.
        recipe.DeallocateResources();
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n')
        ;

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}
