// region/main.cpp
/*
    Sample demonstrating how to handle region data using the Region Morphology vTool (license required).
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

using namespace std;

// Number of region entries
static const uint32_t c_countOfInputRegionEntries = 10;

static const uint32_t c_regionEntryStartPositionX = 15;
static const uint32_t c_regionEntryEndPositionX = c_regionEntryStartPositionX + 9;
static const uint32_t c_regionEntryStartPositionY = 21;


inline CPylonImage makeImage(const CRegion& region, const uint32_t referenceWidth = 640, const uint32_t referenceHeight = 480)
{
    // Create image and set all pixel values to 0.
    CPylonImage image;
    image.Reset(PixelType_Mono8, referenceWidth, referenceHeight);
    memset(image.GetBuffer(), 0, image.GetImageSize());

    // Iterate over all region entries and set the corresponding pixel values in the image to 255.
    SRegionEntryRLE32 const* pRegionData = reinterpret_cast<SRegionEntryRLE32 const*>(region.GetBufferConst());
    const size_t entriesCount = region.GetDataSize() / sizeof(SRegionEntryRLE32);
    for (size_t i = 0; i < entriesCount; i++)
    {
        if (static_cast<uint32_t>(pRegionData[i].Y) < referenceHeight &&
            pRegionData[i].Y >= 0 &&
            pRegionData[i].StartX >= 0 &&
            static_cast<uint32_t>(pRegionData[i].EndX) < referenceWidth)
        {
            memset(reinterpret_cast<char*>(image.GetBuffer()) + pRegionData[i].Y * referenceWidth + pRegionData[i].StartX, 255, pRegionData[i].EndX - pRegionData[i].StartX);
        }
    }
    return image;
}

int main(int /*argc*/, char* /*argv*/[])
{
    // The exit code of the sample application.
    int exitCode = 0;

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
        CRecipe recipe;

        // Load the recipe file.
        // Note: PYLON_DATAPROCESSING_REGION_RECIPE is a string
        // created by the CMake build files.
        recipe.Load(PYLON_DATAPROCESSING_REGION_RECIPE);

        // Register the helper object for receiving all output data.
        recipe.RegisterAllOutputsObserver(&resultCollector, RegistrationMode_Append);

        // Compute region size.
        const size_t dataSize = ComputeRegionSize(RegionType_RLE32, c_countOfInputRegionEntries);

        // Create region.
        CRegion inputRegion(RegionType_RLE32, dataSize, 640u, 480u, c_regionEntryStartPositionX, c_regionEntryStartPositionY,
                            c_regionEntryEndPositionX - c_regionEntryStartPositionX + 1, c_countOfInputRegionEntries);

        // Get pointer to the region buffer.
        SRegionEntryRLE32* pInputRegionData = reinterpret_cast<SRegionEntryRLE32*>(inputRegion.GetBuffer());

        // Create region data representing a 10 x 10 matrix. Every region entry is one line.
        for (size_t i = 0; i < c_countOfInputRegionEntries; i++)
        {
            pInputRegionData[i].StartX = static_cast<int32_t>(c_regionEntryStartPositionX);
            pInputRegionData[i].EndX = static_cast<int32_t>(c_regionEntryEndPositionX);
            pInputRegionData[i].Y = static_cast<int32_t>(i + c_regionEntryStartPositionY);
        }
#ifdef PYLON_WIN_BUILD
        DisplayImage(1, makeImage(inputRegion, inputRegion.GetReferenceWidth(), inputRegion.GetReferenceHeight()));
#endif

        // Note: If you don't know the size of the region when you create it or if you need to resize the region afterwards,
        // you can do it in the following way: inputRegion.Resize(ComputeRegionSize(RegionType_RLE32, 10))

        cout << "Input Region:" << endl << endl;

        // Access the region data.
        cout << "Reference Height:        " << inputRegion.GetReferenceHeight() << endl;
        cout << "Reference Width:         " << inputRegion.GetReferenceWidth() << endl;
        cout << "Bounding Box Top Left X: " << inputRegion.GetBoundingBoxTopLeftX() << endl;
        cout << "Bounding Box Top Left Y: " << inputRegion.GetBoundingBoxTopLeftY() << endl;
        cout << "Bounding Box Height:     " << inputRegion.GetBoundingBoxHeight() << endl;
        cout << "Bounding Box Width:      " << inputRegion.GetBoundingBoxWidth() << endl;
        cout << "Data Size:               " << inputRegion.GetDataSize() << endl;
        cout << endl << endl;

        // Start the processing.
        recipe.Start();

        // Trigger the recipe with region as input data.
        recipe.TriggerUpdate("Regions", inputRegion, 40);

        if (resultCollector.GetWaitObject().Wait(5000))
        {

            CVariantContainer result = resultCollector.RetrieveResult();
            CVariant regionVariantArray = result["Regions"];
            if (!regionVariantArray.HasError())
            {
                cout << "Output Regions:" << endl << endl;
                for (size_t index = 0; index < regionVariantArray.GetNumArrayValues(); ++index)
                {
                    CRegion outputRegion = regionVariantArray.GetArrayValue(index).ToRegion();
                    cout << "Region " << index << ": " << endl;

                    // Access the region data.
                    cout << "Reference Height:        " << outputRegion.GetReferenceHeight() << endl;
                    cout << "Reference Width:         " << outputRegion.GetReferenceWidth() << endl;
                    cout << "Bounding Box Top Left X: " << outputRegion.GetBoundingBoxTopLeftX() << endl;
                    cout << "Bounding Box Top Left Y: " << outputRegion.GetBoundingBoxTopLeftY() << endl;
                    cout << "Bounding Box Height:     " << outputRegion.GetBoundingBoxHeight() << endl;
                    cout << "Bounding Box Width:      " << outputRegion.GetBoundingBoxWidth() << endl;
                    cout << "Data Size:               " << outputRegion.GetDataSize() << endl;

                    if (outputRegion.GetRegionType() == RegionType_RLE32)
                    {
#ifdef PYLON_WIN_BUILD
                        DisplayImage(2, makeImage(outputRegion));
#endif
                        cout << "Region Entries:" << endl << endl;

                        // Get pointer to the buffer containing the output region data.
                        const SRegionEntryRLE32* pOutputRegionData = reinterpret_cast<const SRegionEntryRLE32*>(outputRegion.GetBufferConst());

                        // Iterate over all entries of the output region.
                        const size_t entriesCount = outputRegion.GetDataSize() / sizeof(SRegionEntryRLE32);
                        for (size_t i = 0; i < entriesCount; i++)
                        {
                            cout << "  Line:   " << pOutputRegionData[i].Y << endl;
                            cout << "  StartX: " << pOutputRegionData[i].StartX << endl;
                            cout << "  EndX:   " << pOutputRegionData[i].EndX << endl;
                            cout << endl;
                        }
                    }
                    cout << endl << endl;
                }
            }
            else
            {
                cout << "An error occurred during processing (pin 'Regions'): " << regionVariantArray.GetErrorDescription() << endl;
            }
        }
        else
        {
            throw RUNTIME_EXCEPTION("Result timeout");
        }

        // Stop the processing.
        recipe.Stop();
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
