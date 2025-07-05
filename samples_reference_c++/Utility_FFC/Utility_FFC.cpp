// Utility_FFC.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates how to use the Flat-Field Correction (FFC) with Basler boost V cameras.
    The goal of FFC is to create a more accurate and evenly-illuminated representation of the original image.
    This sample requires a lot of processing power and execution may take a long time in debug configurations.
*/

#pragma warning( disable : 4996 ) // Function call with parameters that may be unsafe. This call relies on the caller to check that the values passed are correct. To disable this warning, use -D_SCL_SECURE_NO_WARNINGS. See the Visual Studio documentation for how to use C++ Checked Iterators.

#define NOMINMAX

#include <algorithm>
#include <cmath>
#include <numeric>

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using cout.
using namespace std;

// The maximum number of images to be grabbed.
static const uint8_t numberOfMaxImagesToGrab = 5;

// Creates an image buffer based on the arithmetic mean of all images grabbed and creates a row of correction values for DSNU and PRNU coefficients calculation.
void processImages( CInstantCamera& camera, float& meanPixelVal, vector<float>& meanOfColumns, const size_t width, const size_t height )
{
    // Start the grabbing of numberOfMaxImagesToGrab images.
    camera.StartGrabbing( numberOfMaxImagesToGrab );

    // This smart pointer will receive the grab result data.
    CGrabResultPtr ptrGrabResult;

    cout << "Please wait. Images are being grabbed." << endl;
    uint8_t succeededGrabs = 0;

    CIntegerParameter bufferSize( camera.GetNodeMap(), "PayloadSize" );
    vector<float> bufferArray( static_cast<size_t>(bufferSize.GetValue()), 0.0f);

    // Camera.StopGrabbing() is called automatically by the RetrieveResult() method
    // when numberOfMaxImagesToGrab images have been retrieved.
    while (camera.IsGrabbing())
    {
        // Wait for an image and then retrieve it. A timeout of 5000 ms is used.
        camera.RetrieveResult( 5000, ptrGrabResult, TimeoutHandling_ThrowException );

        // Image grabbed successfully and expected image buffer size is equal to actual?
        if (ptrGrabResult->GrabSucceeded() && (bufferArray.size() == ptrGrabResult->GetPayloadSize()))
        {
            // Adds current buffer to all previously acquired (and summed) buffers.
            std::transform( bufferArray.begin(),
                            bufferArray.end(),
                            static_cast<const uint8_t*>(ptrGrabResult->GetBuffer()),
                            bufferArray.begin(),
                            plus<float>() );

            succeededGrabs++;
        }
        else
        {
            cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << endl;
        }
    }
    if (succeededGrabs > 0)
    {
        const float heightFloat = static_cast<float>(height);
        const float widthFloat = static_cast<float>(width);

        // Calculates a row (width) of sums of every column (height).
        for (unsigned int y = 0; y < height; ++y)
        {
            for (unsigned int x = 0; x < width; ++x)
            {
                size_t idx = (width * y) + x;
                meanOfColumns[x] += bufferArray[idx];
            }
        }

        // Division by succeededGrabs is neccessary because we summed the pixel values.
        // Division by height is neccessary for mean pixel value per column.
        const float divisor = static_cast<float>(succeededGrabs) + heightFloat;
        std::for_each( meanOfColumns.begin(), 
                       meanOfColumns.end(), 
                       [&divisor] ( float& n )
                       {
                           n /= divisor;
                       } );

        // Calculating mean pixel value of correction value row.
        meanPixelVal = std::accumulate( meanOfColumns.begin(), meanOfColumns.end(), 0.0f);
        meanPixelVal /= widthFloat;
    }
}

// Searching for FFC-compatible boost cameras in CXP transport layer (TL).
bool findBoostCam( CInstantCamera& camera )
{
    // Build a filter list containing each model name supported.
    const char* supportedModelNames[] = { "boA9344-70cc", 
                                          "boA9344-70cm", 
                                          "boA5120-150cc", 
                                          "boA5120-150cm", 
                                          "boA5120-230cc", 
                                          "boA5120-230cm" };
    
    DeviceInfoList filter;
    CDeviceInfo deviceInfo;

    // Find only CXP devices.
    deviceInfo.SetDeviceClass( Pylon::BaslerGenTlCxpDeviceClass );

    // Add each model name to the filter.
    for (const char* supportedModelName : supportedModelNames)
    {
        deviceInfo.SetModelName( supportedModelName );
        filter.push_back( deviceInfo );
    }

    // List of devices matching the filter.
    Pylon::DeviceInfoList_t deviceInfoList;

    CTlFactory::GetInstance().EnumerateDevices( deviceInfoList, filter );

    if (!deviceInfoList.empty())
    {
        // First FFC-compatible CXP device will be chosen.
        camera.Attach( CTlFactory::GetInstance().CreateDevice( deviceInfoList[0] ) );

        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;
        cout << "Devices found: " << deviceInfoList.size() << endl;

        if (camera.IsPylonDeviceAttached())
        {
            cout << "Starting FFC with device: " << deviceInfoList[0].GetModelName() << " (" << deviceInfoList[0].GetSerialNumber() << ")" << endl;
            return true;
        }
    }
    else
    {
        cout << "Devices found: " << deviceInfoList.size() << endl;
        cout << "Couldn't find any FFC-compatible CXP device." << endl;
    }

    return false;
}

int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object with the first camera device found.
        CInstantCamera camera;

        // This sample only works with these cameras.
        if (!findBoostCam( camera ))
        {
            cerr << "Couldn't find supported device." << endl;
            PylonTerminate();

            exitCode = 1;
            return exitCode;
        }

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl;

        // Open the camera.
        camera.Open();

        INodeMap& nodemap = camera.GetNodeMap();

        //  Prepare camera settings to get the optimum images.
        CEnumParameter pixelFormat( nodemap, "PixelFormat" );
        CIntegerParameter width( nodemap, "Width" );
        CIntegerParameter height( nodemap, "Height" );
        CFloatParameter exposureTime( nodemap, "ExposureTime" );

        pixelFormat.TrySetValue( "Mono8" ); // FFC formula works only with Mono8 images.
        width.SetToMaximum();
        height.SetToMaximum();

        cout << "Pixel format: " << pixelFormat.GetValue() << endl;
        cout << "Image width: " << width.GetValue() << endl;
        cout << "Image height: " << height.GetValue() << endl;

        unsigned int inputExposureTime = 0;
        cout << "Enter a valid exposure time between " << exposureTime.GetMin() 
             << " and " << exposureTime.GetMax() << " [us] for a dark image." << endl;

        cin >> inputExposureTime;

        cout << "Exposure time for dark image is: " << inputExposureTime << " us" << endl;
        exposureTime.SetValue( inputExposureTime, FloatValueCorrection_ClipToRange );

        // Mean values over every column (height).
        vector<float> dx( static_cast<size_t>(width.GetValue()), 0.0f );
        // Mean pixel value over all dark images.
        float dMeanFloat = 0.0f;
        // With exposure time for dark images, processes the mean image buffer to calculate dx and dmean.
        processImages( camera, dMeanFloat, dx, static_cast<size_t>(width.GetValue()), static_cast<size_t>(height.GetValue()) );

        cout << "Enter a valid exposure time between " << exposureTime.GetMin() 
             << " and " << exposureTime.GetMax() << " [us] for a bright image." << endl;

        cin >> inputExposureTime;

        cout << "Exposure time for bright image is: " << inputExposureTime << " us" << endl;
        exposureTime.SetValue( inputExposureTime, FloatValueCorrection_ClipToRange );

        // Mean values over every column (height).
        vector<float> gx( static_cast<size_t>(width.GetValue()), 0.0f );
        // Mean pixel value over all bright images.
        float gMeanFloat = 0.0f;
        // With exposure time for bright images, processes the mean image buffer to calculate gx and gmean.
        processImages( camera, gMeanFloat, gx, static_cast<size_t>(width.GetValue()), static_cast<size_t>(height.GetValue()) );

        // Calculate Dark Signal Non-Uniformity (DSNU) coefficients.
        vector<uint8_t> dsnuCoefficients( dx.size(), 0 );
        for (unsigned i = 0; i < dsnuCoefficients.size(); ++i)
        {
            uint8_t ui8ValOverHeight = static_cast<uint8_t>(round( dx.at( i ) ));
            ui8ValOverHeight = std::max( static_cast<uint8_t>(0), ui8ValOverHeight );
            ui8ValOverHeight = std::min( ui8ValOverHeight, static_cast<uint8_t>(127) );
            dsnuCoefficients[i] = ui8ValOverHeight;
        }

        // Calculate Photo Response Non-Uniformity (PRNU) coefficients.
        vector<uint16_t> prnuCoefficients( gx.size(), 0 );
        for (unsigned i = 0; i < prnuCoefficients.size(); ++i)
        {
            float floatTmpVal = 128.0f * gMeanFloat / (gx.at( i ) - dx.at( i ) + 1.0f);
            uint16_t ui16TmpVal = static_cast<uint16_t>(round( floatTmpVal ));
            ui16TmpVal = std::max( static_cast<uint16_t>(0), ui16TmpVal );
            ui16TmpVal = std::min( ui16TmpVal, static_cast<uint16_t>(511) );
            prnuCoefficients[i] = ui16TmpVal;
        }

        if (dMeanFloat > 40.0f)
        {
            cout << ("It looks like the mean dark image isn't dark enough because the dmean value is a little bit high.") << endl;
        }

        if (gMeanFloat < 150.0f)
        {
            cout << ("It looks like the mean bright image is too dark because the gmean value is a little bit low.") << endl;

        }

        if (gMeanFloat > 210.0f)
        {
            cout << ("It looks like the mean bright image is too bright because the gmean value is a little bit high.") << endl;
        }

        CIntegerParameter FFCCoeffX( nodemap, "BslFlatFieldCorrectionCoeffX" );
        CIntegerParameter FFCCoeffDSNU( nodemap, "BslFlatFieldCorrectionCoeffDSNU" );
        CIntegerParameter FFCCoeffPRNU( nodemap, "BslFlatFieldCorrectionCoeffPRNU" );

        // Writing DSNU and PRNU coefficients to camera in column i.
        for (unsigned i = 0; i < gx.size(); ++i)
        {
            FFCCoeffX.SetValue( i, IntegerValueCorrection_Nearest );
            FFCCoeffDSNU.SetValue( dsnuCoefficients[i], IntegerValueCorrection_Nearest );
            FFCCoeffPRNU.SetValue( prnuCoefficients[i], IntegerValueCorrection_Nearest );
        }
        
        int64_t dMean = static_cast<int64_t>(round( dMeanFloat ));
        dMean = std::max( static_cast<int64_t>(0), dMean );
        dMean = std::min( dMean, static_cast<int64_t>(127) );

        // Saves mean dark image pixel value.
        CIntegerParameter FFCDMean( nodemap, "BslFlatFieldCorrectionDMean" ); 
        FFCDMean.SetValue( dMean );

        // Saves current flat-field correction values to flash memory.
        CCommandParameter FFCSaveToFlash( nodemap, "BslFlatFieldCorrectionSaveToFlash" );
        FFCSaveToFlash.Execute();
    }
    catch (const GenericException& e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
            << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cout << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources.
    PylonTerminate();

    return exitCode;
}
