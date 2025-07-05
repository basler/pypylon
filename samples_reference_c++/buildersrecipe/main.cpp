/*
    Sample using the builder's recipe
    Note: The Recipe Code Generator of the pylon Viewer allows you to generate
          sample code to use your vTool recipe in your development environment.
*/
// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Extend the pylon API for using pylon data processing.
#include <pylondataprocessing/PylonDataProcessingIncludes.h>

// Namespaces for using pylon objects
using namespace Pylon;
using namespace Pylon::DataProcessing;

// Namespace for using cout
using namespace std;

int main(int /*argc*/, char* /*argv*/[])
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Enable the pylon camera emulator to provide images from disk
    // by setting the necessary environment variable.
#if defined(PYLON_WIN_BUILD)
    _putenv("PYLON_CAMEMU=1");
#elif defined(PYLON_UNIX_BUILD)
    setenv("PYLON_CAMEMU", "1", true);
#endif

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    const Pylon::String_t cameraVToolUuid = "846bca11-6bf2-4895-88c4-fe038f5a659c";
    const Pylon::String_t formatConverterVToolUuid = "4049ea56-3827-4faf-9478-c3ba02e4a0cb";
    try
    {
        // Create a new builder's recipe.
        CBuildersRecipe recipe;

        // Use GetAvailableVToolTypeIDs() to retrieve a list of all available vTool types.
        Pylon::StringList_t vToolTypes;
        cout << "Available vTool types: " << recipe.GetAvailableVToolTypeIDs(vToolTypes) << '\n';
        for (const auto& type : vToolTypes)
        {
            // GetVToolDisplayNameForTypeID() returns the display name for a given vTool type.
            cout << "Type ID: '" << type << "' : Display Name: '" << recipe.GetVToolDisplayNameForTypeID(type) << "'\n";
        }

        // Use AddVTool to add vTools to the recipe.
        recipe.AddVTool("MyCamera", cameraVToolUuid);
        assert(recipe.HasVTool("MyCamera"));
        recipe.AddVTool("MyConverter", formatConverterVToolUuid);
        assert(recipe.HasVTool("MyConverter"));

        // Use GetVToolNames() to retrieve a list of all vTools that are currently in the recipe.
        Pylon::StringList_t vToolNames;
        cout << "vTools in recipe: " << recipe.GetVToolIdentifiers(vToolNames) << '\n';
        for (const auto& name : vToolNames)
        {
            // Use GetVToolTypeID() to get the vTool type of a specific vTool instance.
            cout << "vTool Name '" << name << "' : type: '" << recipe.GetVToolTypeID(name) << "'\n";
        }

        // Use AddOutput() to add outputs to your recipe.
        recipe.AddOutput("OriginalImage", VariantDataType_PylonImage);
        recipe.AddOutput("ConvertedImage", VariantDataType_PylonImage);

        // Use AddConnection() to create connections between vTool pins and/or the inputs or outputs of the recipe.
        recipe.AddConnection("camera_to_converter", "MyCamera.Image", "MyConverter.Image");
        recipe.AddConnection("converter_to_output", "MyConverter.Image", "<RecipeOutput>.ConvertedImage");
        recipe.AddConnection("camera_to_output", "MyCamera.Image", "<RecipeOutput>.OriginalImage");

        // Use GetConnectionNames() to retrieve a list of all connections that are currently in the recipe.
        Pylon::StringList_t connectionNames;
        cout << "Connections in recipe: " << recipe.GetConnectionIdentifiers(connectionNames) << '\n';
        for (const auto& name : connectionNames)
        {
            cout << "Connection Name '" << name << "'\n";
        }

        // Now, we can run the recipe as usual.
        recipe.Start();

        // Comment the following two lines to disable waiting on exit.
        cerr << endl << "Press enter to exit." << endl;
        while (cin.get() != '\n')
            ;

        recipe.Stop();
    }
    catch (GenICam::GenericException& e)
    {
        cout << "Caught a GenICam exception. Message: " << e.what() << '\n';
    }
    catch(...)
    {
        cout << "Caught an unknown exception.\n";
    }
    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}
