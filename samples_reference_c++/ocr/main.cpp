/*
    Sample demonstrating how to use the OCR Basic vTool (license required).
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
// The sample uses the std::vector and std::accumulate.
#include <vector>
#include <numeric>

// Namespaces for using pylon objects
using namespace Pylon;
using namespace Pylon::DataProcessing;

// Namespace for using cout
using namespace std;

// Number of images to be grabbed
static const uint32_t c_countOfImagesToGrab = 10;

bool getRejectionCharPositions(const Pylon::String_t& text, vector<size_t> &rejectionCharPositions)
{
    rejectionCharPositions.clear();

    size_t currentCharPos = 0;
    const string stdText(text.c_str());
    string::const_iterator it = stdText.cbegin();
    string::const_iterator itEnd = stdText.cend();

    // Check for UTF-8 rejection character (encoded as 0xEF 0xBF 0xBD).
    for (; it != itEnd; ++it)
    {
        if (*it == '\xEF' && (itEnd - it >= 3) && *(it + 1) == '\xBF' && *(it + 2) == '\xBD')
        {
            // Rejection character found.
            rejectionCharPositions.push_back(currentCharPos);
            it += 2; // Advance it to '\xBD'.
        }
        // Increment current character position.
        // Note: We assume here that all other characters are ASCII-encoded (a subset of UTF-8 using only one byte).
        currentCharPos++;
    }

    return (rejectionCharPositions.empty() == false);
}

int main(int /*argc*/, char* /*argv*/[])
{
#ifdef PYLON_WIN_BUILD
    // Change encoding of the output to UTF-8 to get correctly printed messages.
    SetConsoleOutputCP(CP_UTF8);
#endif

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

        // Create a recipe object representing a recipe file created using
        // the pylon Viewer Workbench.
        CRecipe recipe;

        // Load the recipe file.
        // Note: PYLON_DATAPROCESSING_OCR_RECIPE is a string
        // created by the CMake build files.
        recipe.Load(PYLON_DATAPROCESSING_OCR_RECIPE);

        // Set up correct image path to samples.
        // Note: PYLON_DATAPROCESSING_OCR_IMAGES_PATH is a string created by the CMake build files.
        recipe.GetParameters().Get(StringParameterName("ImageLoading/@vTool/SourcePath")).SetValue(PYLON_DATAPROCESSING_OCR_IMAGES_PATH);

        // This is where the output goes.
        recipe.RegisterAllOutputsObserver(&resultCollector, RegistrationMode_Append);

        // Start the processing.
        recipe.Start();

        // Flag to store mode change of OCRBasic vTool.
        bool useCharacterSetAll = false;

        for (uint32_t i = 0; i < c_countOfImagesToGrab; ++i)
        {
            if (resultCollector.GetWaitObject().Wait(5000))
            {
                CVariantContainer result = resultCollector.RetrieveResult();

                CVariant imageVariant = result["Image"];
                if (!imageVariant.HasError())
                {
                    CPylonImage image = imageVariant.ToImage();
                    // Access the image data.
                    cout << "SizeX: " << image.GetWidth() << endl;
                    cout << "SizeY: " << image.GetHeight() << endl;
                    const uint8_t* pImageBuffer = (uint8_t*)image.GetBuffer();
                    cout << "Gray value of first pixel: " << (uint32_t)pImageBuffer[0] << endl << endl;
#ifdef PYLON_WIN_BUILD
                    DisplayImage(1, image);
#endif
                }
                else
                {
                    cout << "An error occurred during processing (pin 'Image'): " << imageVariant.GetErrorDescription() << endl;
                }

                CVariant textArray = result["Texts"];
                if (!textArray.HasError())
                {
                    cout << "Texts:" << endl;
                    for(size_t index = 0; index < textArray.GetNumArrayValues(); ++index)
                    {
                        const Pylon::String_t text(textArray.GetArrayValue(index).ToString());
                        cout << index << " : " <<  text << endl;

                        // The texts read are UTF-8-encoded.
                        // Characters that couldn't be detected are replaced by a UTF-8 rejection character.
                        // Check for UTF-8 rejection character (encoded as 0xEF 0xBF 0xBD) in results.
                        vector<size_t> foundPositions;
                        if (getRejectionCharPositions(text, foundPositions) == true)
                        {
                            // Build a comma-seperated string from foundPositions list.
                            string foundPositionsString = to_string(foundPositions[0]);
                            for (auto it = foundPositions.cbegin() + 1; it != foundPositions.cend(); ++it)
                            {
                                foundPositionsString += ", ";
                                foundPositionsString += to_string(*it);
                            }

                            cout << "Characters at the following positions couldn't be detected: " << foundPositionsString << endl;
                        }
                    }
                }
                else
                {
                    cout << "An error occurred during processing (pin 'Texts'): " << textArray.GetErrorDescription() << std::endl;
                }
                cout << endl << endl << endl;
            }
            else
            {
                throw RUNTIME_EXCEPTION("Result timeout");
            }

            // Switch character set after first full image loop.
            if (   (i >= (c_countOfImagesToGrab / 2))
                && (useCharacterSetAll == false))
            {
                cout << "Switch to character set \"All\" to demonstrate correct OCR detection." << endl << endl << endl;
                recipe.GetParameters().Get(EnumParameterName("OcrBasic/@vTool/CharacterSet")).SetValue("All");

                useCharacterSetAll = true;
            }
        }

        // Stop the processing.
        recipe.Stop();
    }
    catch (const GenericException& e)
    {
        // Error handling
        cerr << "An exception occurred." << endl << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}
