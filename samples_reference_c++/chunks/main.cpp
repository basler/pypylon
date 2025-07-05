// chunks/main.cpp
/*
    Sample demonstrating how to receive chunks and events from the Camera vTool (no license required).
    Note: The Recipe Code Generator of the pylon Viewer allows you to generate
          sample code to use your vTool recipe in your development environment.
*/
// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

#ifdef PYLON_WIN_BUILD
#  include <pylon/PylonGUI.h>
#endif
// Extend the pylon API for using pylon data processing.
#include <pylondataprocessing/PylonDataProcessingIncludes.h>

// Namespaces for using pylon objects
using namespace Pylon;
using namespace Pylon::DataProcessing;

// Namespace for using cout
using namespace std;

// Number of images to be grabbed
static const uint32_t c_countOfImagesToGrab = 100;



int main(int /*argc*/, char* /*argv*/[])
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Enable the pylon camera emulator for grabbing images from disk
    // by setting the necessary environment variable.
    // NOTE: Currently, the pylon camera emulator doesn't support chunks or events.
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
        // If placed on the stack, it must be created before the recipe
        // so that it is destroyed after the recipe.
        CGenericOutputObserver resultCollector;

        // Create a recipe representing a design created using
        // the pylon Viewer Workbench.
        CBuildersRecipe recipe;

        // Load the recipe file.
        // Note: PYLON_DATAPROCESSING_CHUNKS_RECIPE is a string
        // created by the CMake build files.
        recipe.Load(PYLON_DATAPROCESSING_CHUNKS_RECIPE);

        // Add event output pins for end of exposure events
        // (see the Basler Product Documentation for details).
        // These settings may already have been configured in the recipe.
        const auto eventConfiguration = {
                "EoxTimestamp.Type=Integer.EventName=ExposureEnd.ValueName=EventExposureEndTimestamp",
                "FrameID.Type=Integer.EventName=ExposureEnd.ValueName=EventExposureEndFrameID"
        };
        uint32_t eventIndex = 0;
        for (auto c : eventConfiguration)
        {
            if (recipe.GetParameters().Get(CommandParameterName("MyCamera/@vTool/EventPinAdd")).TryExecute())
            {
                if (recipe.GetParameters().Get(IntegerParameterName("MyCamera/@vTool/EventPinSelector"))
                            .TrySetValue(eventIndex) &&
                    recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/EventPinConfiguration"))
                            .TrySetValue(c))
                {
                    cout << "Configured event output " << "'" << c << "'" << endl;
                }
                ++eventIndex;
            }
        }

        // Enable output of Timestamp, Exposure Time, and Line Status All chunks
        // (see the Basler Product Documentation for details).
        // These settings may already have been configured in the recipe.
        const auto chunkConfiguration = {
                "ExposureTime.Type=Float.ValueName=ChunkExposureTime",
                "Timestamp.Type=Integer.ValueName=ChunkTimestamp",
                "LineStatusAll.Type=Integer.ValueName=ChunkLineStatusAll"
        };
        int index = 0;
        for (auto c : chunkConfiguration)
        {
            if (recipe.GetParameters().Get(CommandParameterName("MyCamera/@vTool/ChunkPinAdd")).TryExecute())
            {
                if (recipe.GetParameters().Get(IntegerParameterName("MyCamera/@vTool/ChunkPinSelector"))
                            .TrySetValue(index) &&
                    recipe.GetParameters().Get(StringParameterName("MyCamera/@vTool/ChunkPinValue")).TrySetValue(c))
                {
                    cout << "Configured chunk output " << "'" << c << "'" << endl;
                }
                ++index;
            }
        }

        // Allocate the required resources. This includes the camera device.
        recipe.PreAllocateResources();

        // This is where the output goes.
        recipe.RegisterAllOutputsObserver(&resultCollector, RegistrationMode_Append);

        // Configure camera after allocation.

        // Enable available chunks.
        {
            int chunkCount = 0;
            bool chunksAvailable = recipe.GetParameters().Get(
                    BooleanParameterName("MyCamera/@CameraDevice/ChunkModeActive")).TrySetValue(true);
            cout << "Chunk mode is " << (chunksAvailable ? "" : "not ") << "available" << endl;
            CEnumParameter chunkSelector = recipe.GetParameters().Get(
                    EnumParameterName("MyCamera/@CameraDevice/ChunkSelector"));
            CBooleanParameter chunkEnable = recipe.GetParameters().Get(
                    BooleanParameterName("MyCamera/@CameraDevice/ChunkEnable"));
            if (chunkSelector.IsValid())
            {
                GenApi::node_vector chunkEntries;

                StringList_t chunkNames;
                chunkSelector.GetSettableValues(chunkNames);
                for (const auto &name: chunkNames)
                {
                    if (chunkSelector.TrySetValue(name))
                    {
                        if (chunkEnable.TrySetValue(true))
                        {
                            ++chunkCount;
                            cout << "Enable chunk " << "'" << name.c_str() << "'" << endl;
                        }
                    };
                }
            }

            if (chunkCount == 0)
            {
                cout << "WARNING: Chunks are not supported by selected camera." << endl;
            }

        }



        // Turn Exposure End event notification on.
        if (recipe.GetParameters().Get(EnumParameterName("MyCamera/@CameraDevice/EventSelector"))
            .TrySetValue("ExposureEnd"))
        {
            if (recipe.GetParameters().Get(EnumParameterName("MyCamera/@CameraDevice/EventNotification"))
            .TrySetValue("On"))
            {
                cout << "Configured event notification for ExposureEnd event" << endl;
            }
        }


        recipe.AddOutput("EoxTimestamp", VariantDataType_Int64);
        recipe.AddOutput("FrameID", VariantDataType_Int64);
        recipe.AddOutput("ExposureTime", VariantDataType_Float);
        recipe.AddOutput("Timestamp", VariantDataType_Int64);
        recipe.AddOutput("LineStatusAll", VariantDataType_Int64);
        recipe.AddConnection("camera_to_eoxtimestamp", "MyCamera.EoxTimestamp", "<RecipeOutput>.EoxTimestamp");
        recipe.AddConnection("camera_to_frameid", "MyCamera.FrameID", "<RecipeOutput>.FrameID");
        recipe.AddConnection("camera_to_exposuretime", "MyCamera.ExposureTime", "<RecipeOutput>.ExposureTime");
        recipe.AddConnection("camera_to_timestamp", "MyCamera.Timestamp", "<RecipeOutput>.Timestamp");
        recipe.AddConnection("camera_to_linestatusall", "MyCamera.LineStatusAll", "<RecipeOutput>.LineStatusAll");

        // For demonstration purposes only
        // Print available output names.
        StringList_t outputNames;
        recipe.GetOutputNames(outputNames);
        for (const auto &outputName: outputNames)
        {
            cout << "Output found: " << outputName << endl;
        }

        // Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(&resultCollector, RegistrationMode_Append);

        // Start the processing. The recipe is started and the 
        // Camera vTool sends chunk and event data for each image.
        recipe.Start();

        CEnumParameter testImageSelector = recipe.GetParameters().Get(
                EnumParameterName("MyCamera/@CameraDevice/TestImageSelector|MyCamera/@CameraDevice/TestPattern"));
        for (uint32_t i = 0; i < c_countOfImagesToGrab; ++i)
        {
            if (resultCollector.GetWaitObject().Wait(5000))
            {
                CVariantContainer result = resultCollector.RetrieveResult();

                CVariant imageVariant = result["Image"];
                if (!imageVariant.HasError() && imageVariant.CanConvert(EVariantDataType::VariantDataType_PylonImage))
                {
                    CPylonImage image = imageVariant.ToImage();
                    // Access the image data.
                    cout << "SizeX: " << image.GetWidth() << endl;
                    cout << "SizeY: " << image.GetHeight() << endl;
                    const uint8_t* pImageBuffer = (uint8_t*)image.GetBuffer();
                    cout << "Gray value of first pixel: " << (uint32_t)pImageBuffer[0] <<  endl;
#ifdef PYLON_WIN_BUILD
                    DisplayImage(1, image);
#endif
                }

                CVariant timestamp= result["Timestamp"];
                if (timestamp.HasError() == false &&
                    timestamp.CanConvert(EVariantDataType::VariantDataType_UInt64))
                {
                    cout << "Timestamp    : " << timestamp.ToUInt64() << endl;
                }
                CVariant lineStatusAll = result["LineStatusAll"];
                if (lineStatusAll.HasError() == false &&
                    lineStatusAll.CanConvert(EVariantDataType::VariantDataType_UInt64))
                {
                    cout << "LineStatusAll: " << lineStatusAll.ToUInt64() << endl;
                }
                CVariant exposureTime = result["ExposureTime"];
                if (exposureTime.HasError() == false &&
                    exposureTime.CanConvert(EVariantDataType::VariantDataType_Float))
                {
                    cout << "ExposureTime : " << exposureTime.ToDouble() << endl;
                }
                CVariant frameID = result["FrameID"];
                if (frameID.HasError() == false && frameID.CanConvert(VariantDataType_UInt64))
                {
                    cout << "End of Exposure Event FrameID   : " << frameID.ToUInt64() << endl;
                }
                CVariant eoxTimestamp = result["EoxTimestamp"];
                if (eoxTimestamp.HasError() == false &&
                    eoxTimestamp.CanConvert(EVariantDataType::VariantDataType_UInt64))
                {
                    cout << "End of Exposure Event Timestamp : " << eoxTimestamp.ToUInt64() << endl;
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
