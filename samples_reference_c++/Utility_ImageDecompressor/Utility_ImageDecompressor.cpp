// Utility_ImageDecompressor.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to enable the Compression Beyond feature in Basler cameras and
    how to decompress images using the CImageDecompressor class.
*/

#include <iomanip>
// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using cout.
using namespace std;


// This is a helper function for showing an image on the screen if Windows is used,
// and for printing the first bytes of the image.
void ShowImage( IImage& image, const char* message = NULL )
{
#ifdef PYLON_WIN_BUILD
    // Display the image.
    Pylon::DisplayImage( 1, image );
#endif

    if (message)
    {
        cout << endl << message << " ";
    }

    // Store state of cout.
    std::ios state( NULL );
    state.copyfmt( cout );

    const uint8_t* pBytes = reinterpret_cast<const uint8_t*>(image.GetBuffer());
    cout << endl << "First six bytes of the image: " << endl;
    for (unsigned int i = 0; i < 6; ++i)
    {
        cout << "0x" << hex << setfill( '0' ) << setw( 2 ) << unsigned( pBytes[i] ) << " ";
    }
    cout << endl;

    // Restore state of cout.
    cout.copyfmt( state );

    // Wait for key.
    cerr << endl << "Press enter to continue." << endl;
    while (cin.get() != '\n');
}


// Helper function for printing the data stored in the CompressionInfo_t structure.
void printCompressionInfo( const CompressionInfo_t& info )
{
    string status;

    switch (info.compressionStatus)
    {
        case CompressionStatus_Ok:
            status = "Ok";
            break;

        case CompressionStatus_BufferOverflow:
            status = "Buffer overflow";
            break;

        case CompressionStatus_Error:
            status = "Error";
            break;
    }

    cout << endl << "Compression info:" << endl;
    cout << "hasCompressedImage      :" << (info.hasCompressedImage == true ? "Yes" : "No") << endl;
    cout << "compressionStatus       :" << status << endl;
    cout << "lossy                   :" << (info.lossy == true ? "Yes" : "No") << endl;
    cout << "width                   :" << info.width << endl;
    cout << "height                  :" << info.height << endl;
    cout << "pixelType               :" << CPixelTypeMapper::GetNameByPixelType( info.pixelType ) << endl;
    cout << "decompressedImageSize   :" << info.decompressedImageSize << endl;
    cout << "decompressedPayloadSize :" << info.decompressedPayloadSize << endl;
}


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create a target image.
        CPylonImage targetImage;

        // This smart pointer will receive the grab result data.
        CGrabResultPtr ptrGrabResult;

        // Create an instant camera object with the camera device found first.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Open the camera.
        camera.Open();

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Fetch the nodemap.
        INodeMap& nodemap = camera.GetNodeMap();

        // Check if the camera supports compression.
        if (camera.ImageCompressionMode.IsWritable())
        {
            // Remember the original compression mode.
            String_t oldCompressionMode = camera.ImageCompressionMode.ToString();
            cout << "Old compression mode: " << oldCompressionMode << endl;

            // Set the compression mode to BaslerCompressionBeyond if available.
            if (camera.ImageCompressionMode.CanSetValue( ImageCompressionMode_BaslerCompressionBeyond ))
            {
                camera.ImageCompressionMode.SetValue( ImageCompressionMode_BaslerCompressionBeyond );
                cout << "New compression mode: " << camera.ImageCompressionMode.ToString() << endl;
            }

            // After enabling the compression, we can read the compression rate option.
            String_t oldCompressionRateOption = camera.ImageCompressionRateOption.ToString();
            cout << "Old compression rate option: " << oldCompressionRateOption << endl;

            // Configure lossless compression.
            if (camera.ImageCompressionRateOption.CanSetValue( ImageCompressionRateOption_Lossless ))
            {
                camera.ImageCompressionRateOption.SetValue( ImageCompressionRateOption_Lossless );
                cout << "New compression rate option: " << camera.ImageCompressionRateOption.ToString() << endl;
            }

            // Create the decompressor and initialize it with the nodemap of the camera.
            CImageDecompressor decompressor( nodemap );

            // Wait for a new image.
            if (camera.GrabOne( 1000, ptrGrabResult ))
            {
                if (ptrGrabResult->GrabSucceeded())
                {
                    // Fetch compression info and check whether the image was compressed by the camera.
                    CompressionInfo_t info;
                    if (decompressor.GetCompressionInfo( info, ptrGrabResult ))
                    {
                        // Print content of CompressionInfo_t.
                        printCompressionInfo( info );

                        // Check if image is still compressed (could have been decompressed by a transport layer).
                        if (info.hasCompressedImage)
                        {
                            if (info.compressionStatus == CompressionStatus_Ok)
                            {
                                // Show compression ratio.
                                cout << endl << "Transferred payload \t:" << ptrGrabResult->GetPayloadSize() << endl;
                                cout << "Compression ratio \t:" << (static_cast<float>(ptrGrabResult->GetPayloadSize()) / static_cast<float>(info.decompressedPayloadSize) * 100.0f) << "%" << endl;

                                // Decompress the image.
                                decompressor.DecompressImage( targetImage, ptrGrabResult );

                                // Show the image.
                                ShowImage( targetImage, "Decompressed image." );
                            }
                            else
                            {
                                cout << "There was an error while the camera was compressing the image." << endl;
                            }
                        }
                        else
                        {
                            // No decompression is needed because it is already an uncompressed image.
                            // (This can happen if the transport layer supports transparent decompressing.)
                            ShowImage( ptrGrabResult, "Grabbed image." );
                        }
                    }
                    else
                    {
                        // No decompression is required because the image has never been compressed.
                        // (This can happen if compression was accidentally turned off after initializing the decompressor class.)
                        ShowImage( ptrGrabResult, "Grabbed image." );
                    }
                }
                else
                {
                    cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << endl;
                }
            }
            else
            {
                cout << "Error: Could not grab an image." << endl;
            }

            // Take another picture with lossy compression (if available).

            if (camera.ImageCompressionRateOption.IsWritable())
            {
                cout << endl << "--- Switching to Fix Ratio compression ---" << endl << endl << endl;

                if (camera.ImageCompressionRateOption.CanSetValue( ImageCompressionRateOption_FixRatio ))
                {
                    camera.ImageCompressionRateOption.SetValue( ImageCompressionRateOption_FixRatio );
                    cout << "New compression rate option: " << camera.ImageCompressionRateOption.ToString() << endl;
                }

                // After changing the compression parameters, the decompressor MUST be reconfigured.
                decompressor.SetCompressionDescriptor( nodemap );

                // Wait for a new image.
                if (camera.GrabOne( 1000, ptrGrabResult ))
                {
                    if (ptrGrabResult->GrabSucceeded())
                    {
                        // Fetch compression info and check whether the image was compressed by the camera.
                        CompressionInfo_t info;
                        if (decompressor.GetCompressionInfo( info, ptrGrabResult ))
                        {
                            // Print content of CompressionInfo_t.
                            printCompressionInfo( info );

                            // Check if image is still compressed (could have been decompressed by a transport layer).
                            if (info.hasCompressedImage)
                            {
                                if (info.compressionStatus == CompressionStatus_Ok)
                                {
                                    // Show compression ratio.
                                    cout << endl << "Transferred payload \t:" << ptrGrabResult->GetPayloadSize() << endl;
                                    cout << "Compression ratio \t:" << (static_cast<float>(ptrGrabResult->GetPayloadSize()) / static_cast<float>(info.decompressedPayloadSize) * 100.0f) << "%" << endl;

                                    // Decompress the image.
                                    decompressor.DecompressImage( targetImage, ptrGrabResult );

                                    // Show the image.
                                    ShowImage( targetImage, "Decompressed image." );
                                }
                                else
                                {
                                    cout << "There was an error while the camera was compressing the image." << endl;
                                }
                            }
                            else
                            {
                                // No decompression is needed because it is already an uncompressed image.
                                // (This can happen if the transport layer supports transparent decompressing.)
                                ShowImage( ptrGrabResult, "Grabbed image." );
                            }
                        }
                        else
                        {
                            // No decompression is required because the image has never been compressed.
                            // (This can happen if compression was accidentally turned off after initializing the decompressor class.)
                            ShowImage( ptrGrabResult, "Grabbed image." );
                        }
                    }
                    else
                    {
                        cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << endl;
                    }
                }
                else
                {
                    cout << "Error: Could not grab an image." << endl;
                }
            }

            // Restore original compression mode. Compression rate option must be restored first as the rate can't be changed
            // when compression itself is turned off.
            camera.ImageCompressionRateOption.SetValue( oldCompressionRateOption );
            camera.ImageCompressionMode.SetValue( oldCompressionMode );
        }
        else
        {
            cout << "This camera does not support compression." << endl;
        }

        camera.Close();
    }
    catch (const GenericException& e)
    {

        cerr << "Could not grab an image: " << endl
            << e.GetDescription() << endl;

        exitCode = 1;
    }

    // Release all pylon resources.
    PylonTerminate();

    // Wait for key.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    return exitCode;
}
