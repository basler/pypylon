// ParametrizeCamera_Shading.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample demonstrates how to calculate and upload a gain shading
    set to a Basler runner line scan camera.

    This sample only applies to Basler runner cameras.
*/

// For use with Visual Studio >= 2005, disable deprecate warnings caused by the fopen function.
#define _CRT_SECURE_NO_WARNINGS

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// For DBL_MAX.
#include <float.h>
#include <errno.h>

#ifdef _MSC_VER
#pragma warning(push)
#pragma warning(disable: 4244)
#endif

// For file upload.
#include <GenApi/Filestream.h>

#ifdef _MSC_VER
#pragma warning(pop)
#endif

// Namespace for using pylon objects.
using namespace Pylon;

// Namespaces for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;
using namespace Basler_UniversalStreamParams;

// Namespace for using cout.
using namespace std;

////////////////////////////////////////////////////////////////////////////////

// Prototypes for functions used in 'main'.

void CreateShadingData( CBaslerUniversalInstantCamera& camera,
                        const char* pLocalFilename );
void UploadFile( CBaslerUniversalInstantCamera& camera,
                 const char* pCameraFilename,
                 const char* pLocalFilename );
void CheckShadingData( CBaslerUniversalInstantCamera& camera );

////////////////////////////////////////////////////////////////////////////////

// Name of the file where we will store the shading data on the local disk.
static const char LocalFilename[] = "ShadingData.bin";


#define USE_SHADING_SET_1   // Define which shading set we are going to use.

#if defined (USE_SHADING_SET_1)

// Name of the file in the camera where the shading data will be stored.
static const char CameraFilename[] = "UserGainShading1";

// Name of the shading set that corresponds to 'CameraFilename'.
static ShadingSetSelectorEnums ShadingSet = ShadingSetSelector_UserShadingSet1;

#elif defined (USE_SHADING_SET_2)

// Name of the file in the camera where shading data will be stored.
static const char CameraFilename[] = "UserGainShading2";

// Name of the shading set that corresponds to 'CameraFilename'.
static ShadingSetSelectorEnums ShadingSet = ShadingSetSelector_UserShadingSet2;

#else
#error No shading set defined!
#endif

////////////////////////////////////////////////////////////////////////////////

int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Only look for GigE cameras.
        CDeviceInfo info;
        info.SetDeviceClass( Pylon::BaslerGigEDeviceClass );

        // Create an instant camera object for the GigE camera found first.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice( info ) );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Register the standard configuration event handler for configuring single frame acquisition.
        // This replaces the default configuration as all event handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration( new CAcquireSingleFrameConfiguration(), RegistrationMode_ReplaceAll, Cleanup_Delete );

        // Open the camera.
        camera.Open();

        // Only line scan cameras support gain shading.
        if (camera.DeviceScanType.GetValue() == DeviceScanType_Linescan)
        {
            // Here, we assume that the conditions for exposure (illumination,
            // exposure time, etc.) have been set up to deliver images of
            // uniform intensity (gray value), but that the acquired images are not uniform.
            // We calculate the gain shading data so that the observed non-uniformity
            // will be compensated when the data are applied.
            // These data are saved to a local file.
            CreateShadingData( camera, LocalFilename );

            // Transfer calculated gain shading data from the local file to the camera.
            UploadFile( camera, CameraFilename, LocalFilename );

            // Test to what extent the non-uniformity has been compensated.
            CheckShadingData( camera );
        }
        else
        {
            cerr << "Only line scan cameras support gain shading." << endl;
        }

        // Close the camera.
        camera.Close();
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

////////////////////////////////////////////////////////////////////////////////
//
// In the following code, the format of the arrays containing intensities
// or coefficients is as follows:
//
//      If the pixel format is PixelFormat_Mono8:
//      ArraySize == Width
//      [Value_x0, Value_x1, Value_x2, ... , Value_x(Width - 1)]
//
//      If the pixel format is PixelFormat_RGB8Packed:
//      ArraySize ==  3 * Width
//      [ValueRed_x0,   ValueRed_x1,   ... , ValueRed_x(Width - 1),
//       ValueGreen_x0, ValueGreen_x1, ... , ValueGreen_x(Width - 1),
//       ValueBlue_x0,  ValueBlue_x1,  ... , ValueBlue_x(Width - 1)]
//
////////////////////////////////////////////////////////////////////////////////


//
// Grab a frame and store the intensitiy for the pixels in each column
// in 'Intensities'.
//
void AverageLines( CBaslerUniversalInstantCamera& camera,
                   uint32_t Width,         // Width of frame (number of pixels in each line).
                   uint32_t Height,        // Height of frame (number of lines in each frame).
                   uint32_t NumCoeffs,     // Number of coefficients.
                   double* Intensities )    // Destination array.
{
    for (uint32_t x = 0; x < NumCoeffs; x++)
    {
        Intensities[x] = 0.0;
    }

    cout << "Grab frame for averaging." << endl;

    CGrabResultPtr ptrGrabResult;
    camera.GrabOne( 5000, ptrGrabResult );
    uint8_t* Buffer = static_cast<uint8_t*>(ptrGrabResult->GetBuffer());

    if (NumCoeffs == 3 * Width)
    {
        //
        // RGB mode.
        //
        for (uint32_t x = 0; x < Width; x++)
        {
            for (uint32_t y = 0; y < Height; y++)
            {
                // Add intensities.
                uint32_t idx = 3 * (y * Width + x);
                Intensities[x] += Buffer[idx];
                Intensities[x + Width] += Buffer[idx + 1];
                Intensities[x + 2 * Width] += Buffer[idx + 2];
            }
        }
    }
    else
    {
        //
        // Mono mode.
        //
        for (uint32_t x = 0; x < Width; x++)
        {
            for (uint32_t y = 0; y < Height; y++)
            {
                // Add intensities.
                Intensities[x] += Buffer[y * Width + x];
            }
        }
    }
    double scale = 1.0 / double( Height );
    for (uint32_t x = 0; x < NumCoeffs; x++)
    {
        // Calculate average intensities.
        Intensities[x] *= scale;
    }
}

////////////////////////////////////////////////////////////////////////////////
//
// Take the average intensities from 'pDblCoeff'. Identify the minimum and maximum
// average intensity. For each intensity, calculate a multiplier so that
// the product of the multiplier and  the intensity equals the maximimum intensity (the
// multiplier for the maximum intensity is 1). Store the multipliers in 'pDblCoeff'.
//
void CalculateCoeffs( uint32_t  Width,         // Width of image (number of pixels in each line).
                      uint32_t  /*Height*/,    // Height of image (number of lines in each frame).
                      uint32_t  NumCoeffs,     // Number of shading coefficients.
                      double* pDblCoeff )      // In: averaged intensities.
                                               // Out: multiplier values.
{
    if (NumCoeffs == 3 * Width)
    {
        //
        // RGB mode.
        //
        double MinR = DBL_MAX;
        double MinG = DBL_MAX;
        double MinB = DBL_MAX;
        double MaxR = -DBL_MAX;
        double MaxG = -DBL_MAX;
        double MaxB = -DBL_MAX;

        for (uint32_t x = 0; x < Width; x++)
        {
            // Determine min and max intensity.
            if (pDblCoeff[x] < MinR)
            {
                MinR = pDblCoeff[x];
            }

            if (pDblCoeff[x] > MaxR)
            {
                MaxR = pDblCoeff[x];
            }

            if (pDblCoeff[x + Width] < MinG)
            {
                MinG = pDblCoeff[x + Width];
            }

            if (pDblCoeff[x + Width] > MaxG)
            {
                MaxG = pDblCoeff[x + Width];
            }

            if (pDblCoeff[x + 2 * Width] < MinB)
            {
                MinB = pDblCoeff[x + 2 * Width];
            }

            if (pDblCoeff[x + 2 * Width] > MaxB)
            {
                MaxB = pDblCoeff[x + 2 * Width];
            }
        }
        cout << "MaxR = " << (MaxR / MinR) << " * MinR" << endl;
        cout << "MaxG = " << (MaxG / MinG) << " * MinG" << endl;
        cout << "MaxB = " << (MaxB / MinB) << " * MinB" << endl;

        // Scale to maximum intensity.
        for (uint32_t x = 0; x < Width; x++)
        {
            pDblCoeff[x] = MaxR / pDblCoeff[x];
            pDblCoeff[x + Width] = MaxG / pDblCoeff[x + Width];
            pDblCoeff[x + 2 * Width] = MaxB / pDblCoeff[x + 2 * Width];
        }
    }
    else
    {
        //
        // Mono mode.
        //

        double Min = DBL_MAX;
        double Max = -DBL_MAX;
        for (uint32_t x = 0; x < Width; x++)
        {
            // Determine min and max intensity.
            if (pDblCoeff[x] < Min)
            {
                Min = pDblCoeff[x];
            }

            if (pDblCoeff[x] > Max)
            {
                Max = pDblCoeff[x];
            }
        }

        cout << "Max = " << (Max / Min) << " * Min" << endl;

        // Scale to maximum intensity.
        for (uint32_t x = 0; x < Width; x++)
        {
            pDblCoeff[x] = Max / pDblCoeff[x];
        }
    }
}

////////////////////////////////////////////////////////////////////////////////

bool SupportsRGB( CBaslerUniversalInstantCamera& camera );


// 'CreateShadingData' assumes that the conditions for exposure (illumination,
// exposure time, etc.) have been set up to deliver images of
// uniform intensity (gray value), but that the acquired images are not uniform.
// We calculate the gain shading data so that the observed non-uniformity
// will be compensated when the data are applied.
// These data are saved to a local file.

void CreateShadingData( CBaslerUniversalInstantCamera& camera, const char* pLocalFilename )
{
    //
    // Prepare camera for grab.
    //

    uint32_t Width = (uint32_t) camera.Width.GetValue();
    uint32_t Height = (uint32_t) camera.Height.GetValue();
    int32_t BytesPerPixel = 1;
    if (SupportsRGB( camera ))
    {
        camera.PixelFormat.SetValue( PixelFormat_RGB8Packed );
        BytesPerPixel = 3;
    }
    else
    {
        camera.PixelFormat.SetValue( PixelFormat_Mono8 );
    }

    // Disable gain shading for calculation.
    camera.ShadingSelector.SetValue( ShadingSelector_GainShading );
    camera.ShadingEnable.SetValue( false );

    //
    // Grab and average images into 'pDblCoeff'.
    //

    uint32_t NumCoeffs = BytesPerPixel * Width;
    double* pDblCoeff = new double[NumCoeffs];
    AverageLines( camera, Width, Height, NumCoeffs, pDblCoeff );

    //
    // Calculate gain shading data.
    //

    // Convert averaged intensities to multipliers.
    CalculateCoeffs( Width, Height, NumCoeffs, pDblCoeff );

    // Convert multipliers to camera format.
    uint32_t* pCoeffs = new uint32_t[NumCoeffs];
    for (uint32_t x = 0; x < NumCoeffs; x++)
    {
        // The multipliers are expressed as 32 bit fixed point
        // numbers with 16 bits before and 16 bits after
        // the decimal point.
        uint32_t coeff = uint32_t( pDblCoeff[x] * (1 << 16) );

        // Currently, the maximum multiplier is limited to 3.99998
        // (max register value == 0x0003FFFF).

        if (coeff > 0x0003FFFF)
        {
            static bool PrintMessage = true;
            if (PrintMessage)
            {
                PrintMessage = false;
                cout << "Gain shading had to be clipped." << endl;
            }
            coeff = 0x0003FFFF;
        }

        pCoeffs[x] = coeff;
    }

    delete[] pDblCoeff;

    //
    // Write data to file.
    //
    FILE* fp = fopen( pLocalFilename, "wb" );
    if (fp == NULL)
    {
        RUNTIME_EXCEPTION( "Can not open file '%s'\n", pLocalFilename );
    }

    // Header for gain shading file.
    struct ShadingHeader_t
    {
        unsigned char  version;
        unsigned char  type;
        unsigned char  sensorType;
        unsigned char  lineType;
        unsigned short width;
        unsigned short reserved;
    };

    // Constants used in header.
    static const unsigned char ShadingVersion_1 = 0x5a;
    static const unsigned char ShadingType_Gain = 0xc3;
    static const unsigned char ShadingSensorType_Line = 0x02;
    static const unsigned char ShadingLineType_Single = 0x01;
    static const unsigned char ShadingLineType_Tri = 0x03;

        // Construct header.
    ShadingHeader_t h;
    h.version = ShadingVersion_1;
    h.type = ShadingType_Gain;
    h.sensorType = ShadingSensorType_Line;
    h.lineType = BytesPerPixel == 3 ? ShadingLineType_Tri : ShadingLineType_Single;
    h.width = uint16_t( Width );
    h.reserved = 0;

        // Write shading data to local file.
    fwrite( &h, sizeof( h ), 1, fp );
    fwrite( pCoeffs, sizeof( uint32_t ), NumCoeffs, fp );
    fclose( fp );
    delete[] pCoeffs;
}

////////////////////////////////////////////////////////////////////////////////

// Copy data from a local file to a file in the camera.
void UploadFile( CBaslerUniversalInstantCamera& camera,
                 const char* pCameraFilename,
                 const char* pLocalFilename )
{

    // Open local file.
    FILE* fp = fopen( pLocalFilename, "rb" );
    if (fp == NULL)
    {
        RUNTIME_EXCEPTION( "Can not open file '%s'\n", pLocalFilename );
    }

    // Determine file size.
    fseek( fp, 0, SEEK_END );
    size_t Size = ftell( fp );
    rewind( fp );

    if (Size == 0)
    {
        fclose( fp );
        return;
    }

    // Read data from local file into pBuf.
    char* pBuf = new char[Size];
    size_t read = fread( pBuf, 1, Size, fp );
    fclose( fp );
    if (read != Size)
    {
        RUNTIME_EXCEPTION( "Failed to read from file '%s'\n", pLocalFilename );
    }

    // Transfer data to camera.
    GenApi::ODevFileStream stream( &camera.GetNodeMap(), pCameraFilename );
    stream.write( pBuf, streamsize( Size ) );
    stream.close();

    delete[] pBuf;
}



////////////////////////////////////////////////////////////////////////////////
// Check the success of 'CreateShadingData' and 'UploadFile' by
//     - activating and enabling the uploaded shading data file
//     - grabbing one image
//     - calculating the multipliers again, expecting them to be close to 1.0
void CheckShadingData( CBaslerUniversalInstantCamera& camera )
{
    uint32_t Width = (uint32_t) camera.Width.GetValue();
    uint32_t Height = (uint32_t) camera.Height.GetValue();
    int32_t BytesPerPixel = 1;
    if (SupportsRGB( camera ))
    {
        BytesPerPixel = 3;
    }

    //
    // Activate and enable the gain shading set that was just uploaded.
    //

    camera.ShadingSelector.SetValue( ShadingSelector_GainShading );
    camera.ShadingSetSelector.SetValue( ShadingSet );
    camera.ShadingSetActivate.Execute();
    camera.ShadingEnable.SetValue( true );

    //
    // Grab image and calculate multipliers just to print the new Max/Min ratio.
    //

    uint32_t NumCoeffs = BytesPerPixel * Width;
    double* pDblCoeff = new double[NumCoeffs];
    AverageLines( camera,
                  Width,
                  Height,
                  NumCoeffs,
                  pDblCoeff );
    cout << endl << "After applying shading correction:" << endl;
    CalculateCoeffs( Width, Height, NumCoeffs, pDblCoeff );
    delete[] pDblCoeff;
}

////////////////////////////////////////////////////////////////////////////////
// Check whether camera supports RGB pixel formats.
bool SupportsRGB( CBaslerUniversalInstantCamera& camera )
{
    GenApi::NodeList_t Entries;
    camera.PixelFormat.GetEntries( Entries );
    bool Result = false;

    for (size_t i = 0; i < Entries.size(); i++)
    {
        GenApi::INode* pNode = Entries[i];
        if (IsAvailable( pNode->GetAccessMode() ))
        {
            GenApi::IEnumEntry* pEnum = dynamic_cast<GenApi::IEnumEntry*>(pNode);
            const GenICam::gcstring sym( pEnum->GetSymbolic() );
            if (sym.find( GenICam::gcstring( "RGB" ) ) != string::npos)
            {
                Result = true;
                break;
            }
        }
    }
    return Result;
}
