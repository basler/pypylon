// Grab_UsingBufferFactory.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample demonstrates how to use a user-provided buffer factory.
    Using a buffer factory is optional and intended for advanced use cases only.
    A buffer factory is only necessary if you want to grab into externally supplied buffers.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#include <pylon/PylonGUI.h>
#endif

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

// Number of images to be grabbed.
static const uint32_t c_countOfImagesToGrab = 5;


// A user-provided buffer factory.
class MyBufferFactory : public IBufferFactory
{
public:
    MyBufferFactory()
        : m_lastBufferContext( 1000 )
    {
    }

    virtual ~MyBufferFactory()
    {
    }


    // Will be called when the Instant Camera object needs to allocate a buffer.
    // Return the buffer and context data in the output parameters.
    // In case of an error, new() will throw an exception
    // which will be forwarded to the caller to indicate an error.
    // Warning: This method can be called by different threads.
    virtual void AllocateBuffer( size_t bufferSize, void** pCreatedBuffer, intptr_t& bufferContext )
    {
        try
        {
            // Allocate buffer for pixel data.
            // If you already have a buffer allocated by your image processing library, you can use this instead.
            // In this case, you must modify the delete code (see below) accordingly.
            *pCreatedBuffer = new uint8_t[bufferSize];
            // The context information is never changed by the Instant Camera and can be used
            // by the buffer factory to manage the buffers.
            // The context information can be retrieved from a grab result by calling
            // ptrGrabResult->GetBufferContext();
            bufferContext = ++m_lastBufferContext;

            cout << "Created buffer " << bufferContext << ", " << *pCreatedBuffer << endl;
        }
        catch (const std::exception&)
        {
            // In case of an error you must free the memory you may have already allocated.
            if (*pCreatedBuffer != NULL)
            {
                uint8_t* p = reinterpret_cast<uint8_t*>(pCreatedBuffer);
                delete[] p;
                *pCreatedBuffer = NULL;
            }

            // Rethrow exception.
            // AllocateBuffer can also just return with *pCreatedBuffer = NULL to indicate
            // that no buffer is available at the moment.
            throw;
        }
    }


    // Frees a previously allocated buffer.
    // Warning: This method can be called by different threads.
    virtual void FreeBuffer( void* pCreatedBuffer, intptr_t bufferContext )
    {
        uint8_t* p = reinterpret_cast<uint8_t*>(pCreatedBuffer);
        delete[] p;
        cout << "Freed buffer " << bufferContext << ", " << pCreatedBuffer << endl;
    }


    // Destroys the buffer factory.
    // This will be used when you pass the ownership of the buffer factory instance to pylon
    // by defining Cleanup_Delete. pylon will call this function to destroy the instance
    // of the buffer factory. If you don't pass the ownership to pylon (Cleanup_None),
    // this method will be ignored.
    virtual void DestroyBufferFactory()
    {
        delete this;
    }


protected:

    unsigned long m_lastBufferContext;
};


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // The buffer factory must be created first because objects on the
        // stack are destroyed in reverse order of creation.
        // The buffer factory must exist longer than the Instant Camera object
        // in this sample.
        MyBufferFactory myFactory;

        // Create an instant camera object with the camera device found first.
        CInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Use our own implementation of a buffer factory.
        // Since we control the lifetime of the factory object, we pass Cleanup_None.
        camera.SetBufferFactory( &myFactory, Cleanup_None );

        // The parameter MaxNumBuffer can be used to control the count of buffers
        // allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5;

        // If the 'BufferHandlingMode_Stream' is used, make sure to set
        // camera.MaxNumQueuedBuffer to a value smaller than or equal to the value
        // of camera.MaxNumBuffer.
        // Note: The USB3 Vision and GenTL transport layers do not support the
        // 'BufferHandlingMode_Stream' mode.

        // Start the grabbing of c_countOfImagesToGrab images.
        // The camera device is parameterized with a default configuration which
        // sets up free-running continuous acquisition.
        camera.StartGrabbing( c_countOfImagesToGrab );

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        // when c_countOfImagesToGrab images have been retrieved.
        while (camera.IsGrabbing())
        {
            // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );

            // Image grabbed successfully?
            if (ptrGrabResult->GrabSucceeded())
            {
                // Access the image data.
                cout << "Context: " << ptrGrabResult->GetBufferContext() << endl;
                cout << "SizeX: " << ptrGrabResult->GetWidth() << endl;
                cout << "SizeY: " << ptrGrabResult->GetHeight() << endl;
                const uint8_t* pImageBuffer = (uint8_t*) ptrGrabResult->GetBuffer();
                cout << "First value of pixel data: " << (uint32_t) pImageBuffer[0] << endl << endl;

#ifdef PYLON_WIN_BUILD
                // Display the grabbed image.
                Pylon::DisplayImage( 1, ptrGrabResult );
#endif
            }
            else
            {
                cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription();
            }
        }
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
