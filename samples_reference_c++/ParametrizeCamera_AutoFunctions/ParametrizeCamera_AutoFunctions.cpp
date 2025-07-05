// ParametrizeCamera_AutoFunctions.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    Note: Different camera families implement different versions of the Standard Feature Naming Convention (SFNC).
    That's why the name and the type of the parameters used can be different.

    This sample illustrates how to use the Auto Functions feature of Basler cameras.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>
#ifdef PYLON_WIN_BUILD
#    include <pylon/PylonGUI.h>
#endif

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using cout.
using namespace std;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Forward declarations for helper functions
bool IsColorCamera( CBaslerUniversalInstantCamera& camera );
void AutoGainOnce( CBaslerUniversalInstantCamera& camera );
void AutoGainContinuous( CBaslerUniversalInstantCamera& camera );
void AutoExposureOnce( CBaslerUniversalInstantCamera& camera );
void AutoExposureContinuous( CBaslerUniversalInstantCamera& camera );
void AutoWhiteBalance( CBaslerUniversalInstantCamera& camera );


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized.
    PylonInitialize();

    try
    {
        // Create an instant camera object with the first found camera device.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        // Register the standard event handler for configuring single frame acquisition.
        // This overrides the default configuration as all event handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        // Please note that the camera device auto functions do not require grabbing by single frame acquisition.
        // All available acquisition modes can be used.
        camera.RegisterConfiguration( new CAcquireSingleFrameConfiguration, RegistrationMode_ReplaceAll, Cleanup_Delete );

        // Open the camera.
        camera.Open();

        // Turn test image off.
        camera.TestImageSelector.TrySetValue( TestImageSelector_Off );
        camera.TestPattern.TrySetValue( TestPattern_Off );

        // Only area scan cameras support auto functions.
        if (camera.DeviceScanType.GetValue() == DeviceScanType_Areascan)
        {
            if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
            {
                // All area scan cameras support luminance control.
                // Carry out luminance control by using the "once" gain auto function.
                // For demonstration purposes only, set the gain to an initial value.
                camera.Gain.SetToMaximum();
                AutoGainOnce( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');


                // Carry out luminance control by using the "continuous" gain auto function.
                // For demonstration purposes only, set the gain to an initial value.
                camera.Gain.SetToMaximum();
                AutoGainContinuous( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');

                // For demonstration purposes only, set the exposure time to an initial value.
                camera.ExposureTime.SetToMinimum();

                // Carry out luminance control by using the "once" exposure auto function.
                AutoExposureOnce( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');

                // For demonstration purposes only, set the exposure time to an initial value.
                camera.ExposureTime.SetToMinimum();

                // Carry out luminance control by using the "continuous" exposure auto function.
                AutoExposureContinuous( camera );
            }
            else
            {
                // All area scan cameras support luminance control.
                // Carry out luminance control by using the "once" gain auto function.
                // For demonstration purposes only, set the gain to an initial value.
                camera.GainRaw.SetToMaximum();
                AutoGainOnce( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');


                // Carry out luminance control by using the "continuous" gain auto function.
                // For demonstration purposes only, set the gain to an initial value.
                camera.GainRaw.SetToMaximum();
                AutoGainContinuous( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');

                // For demonstration purposes only, set the exposure time to an initial value.
                camera.ExposureTimeRaw.SetToMinimum();

                // Carry out luminance control by using the "once" exposure auto function.
                AutoExposureOnce( camera );
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');

                // For demonstration purposes only, set the exposure time to an initial value.
                camera.ExposureTimeRaw.SetToMinimum();

                // Carry out luminance control by using the "continuous" exposure auto function.
                AutoExposureContinuous( camera );
            }

            // Only color cameras support the balance white auto function.
            if (IsColorCamera( camera ))
            {
                cerr << endl << "Press enter to continue." << endl;
                while (cin.get() != '\n');

                if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
                {
                    // For demonstration purposes only, set the initial balance ratio values:
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
                    camera.BalanceRatio.SetToMaximum();
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
                    camera.BalanceRatio.TrySetValuePercentOfRange( 50.0 );
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
                    camera.BalanceRatio.SetToMinimum();
                }
                else
                {
                    // For demonstration purposes only, set the initial balance ratio values:
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
                    camera.BalanceRatioAbs.SetToMaximum();
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
                    camera.BalanceRatioAbs.TrySetValuePercentOfRange( 50.0 );
                    camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
                    camera.BalanceRatioAbs.SetToMinimum();
                }

                // Carry out white balance using the balance white auto function.
                AutoWhiteBalance( camera );
            }
        }
        else
        {
            cerr << "Only area scan cameras support auto functions." << endl;
        }

        // Close camera.
        camera.Close();

    }
    catch (const TimeoutException& e)
    {
        // Auto functions did not finish in time.
        // Maybe the cap on the lens is still on or there is not enough light.
        cerr << "A timeout has occurred." << endl
            << e.GetDescription() << endl;
        cerr << "Please make sure you remove the cap from the camera lens before running this sample." << endl;
        exitCode = 0;
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


void AutoGainOnce( CBaslerUniversalInstantCamera& camera )
{
    // Check whether the gain auto function is available.
    if (!camera.GainAuto.IsWritable())
    {
        cout << "The camera does not support Gain Auto." << endl << endl;
        return;
    }

    // Maximize the grabbed image area of interest (Image AOI).
    camera.OffsetX.TrySetToMinimum();
    camera.OffsetY.TrySetToMinimum();
    camera.Width.SetToMaximum();
    camera.Height.SetToMaximum();

    if (camera.AutoFunctionROISelector.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the Auto Function ROI for luminance statistics.
        // We want to use ROI1 for gathering the statistics

        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( true );   // ROI 1 is used for brightness control
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( false );   // ROI 2 is not used for brightness control

        // Set the ROI (in this example the complete sensor is used)
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );  // configure ROI 1
        camera.AutoFunctionROIOffsetX.SetToMinimum();
        camera.AutoFunctionROIOffsetY.SetToMinimum();
        camera.AutoFunctionROIWidth.SetToMaximum();
        camera.AutoFunctionROIHeight.SetToMaximum();
    }
    else if (camera.AutoFunctionAOISelector.IsWritable())
    {
        // Set the Auto Function AOI for luminance statistics.
        // Currently, AutoFunctionAOISelector_AOI1 is predefined to gather
        // luminance statistics.
        camera.AutoFunctionAOISelector.SetValue( AutoFunctionAOISelector_AOI1 );
        camera.AutoFunctionAOIOffsetX.SetToMinimum();
        camera.AutoFunctionAOIOffsetY.SetToMinimum();
        camera.AutoFunctionAOIWidth.SetToMaximum();
        camera.AutoFunctionAOIHeight.SetToMaximum();
    }

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the target value for luminance control.
        // A value of 0.3 means that the target brightness is 30 % of the maximum brightness of the raw pixel value read out from the sensor.
        // A value of 0.4 means 40 % and so forth.
        camera.AutoTargetBrightness.SetValue( 0.3 );

        // We are going to try GainAuto = Once.

        cout << "Trying 'GainAuto = Once'." << endl;
        cout << "Initial Gain = " << camera.Gain.GetValue() << endl;

        // Set the gain ranges for luminance control.
        camera.AutoGainLowerLimit.SetToMinimum();
        camera.AutoGainUpperLimit.SetToMaximum();
    }
    else
    {
        // Set the target value for luminance control. The value is always expressed
        // as an 8 bit value regardless of the current pixel data output format,
        // i.e., 0 -> black, 255 -> white.
        camera.AutoTargetValue.TrySetValue( 80 );

        // We are going to try GainAuto = Once.

        cout << "Trying 'GainAuto = Once'." << endl;
        cout << "Initial Gain = " << camera.GainRaw.GetValue() << endl;

        // Set the gain ranges for luminance control.
        camera.AutoGainRawLowerLimit.SetToMinimum();
        camera.AutoGainRawUpperLimit.SetToMaximum();
    }

    camera.GainAuto.SetValue( GainAuto_Once );

    // When the "once" mode of operation is selected,
    // the parameter values are automatically adjusted until the related image property
    // reaches the target value. After the automatic parameter value adjustment is complete, the auto
    // function will automatically be set to "off" and the new parameter value will be applied to the
    // subsequently grabbed images.

    int n = 0;
    while (camera.GainAuto.GetValue() != GainAuto_Off)
    {
        CBaslerUniversalGrabResultPtr ptrGrabResult;
        camera.GrabOne( 5000, ptrGrabResult );
#ifdef PYLON_WIN_BUILD
        Pylon::DisplayImage( 1, ptrGrabResult );

        //For demonstration purposes only. Wait until the image is shown.
        WaitObject::Sleep( 100 );
#endif

        //Make sure the loop is exited.
        if (++n > 100)
        {
            throw TIMEOUT_EXCEPTION( "The adjustment of auto gain did not finish." );
        }
    }

    cout << "GainAuto went back to 'Off' after " << n << " frames." << endl;
    if (camera.Gain.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        cout << "Final Gain = " << camera.Gain.GetValue() << endl << endl;
    }
    else
    {
        cout << "Final Gain = " << camera.GainRaw.GetValue() << endl << endl;
    }
}


void AutoGainContinuous( CBaslerUniversalInstantCamera& camera )
{
    // Check whether the Gain Auto feature is available.
    if (!camera.GainAuto.IsWritable())
    {
        cout << "The camera does not support Gain Auto." << endl << endl;
        return;
    }

    // Maximize the grabbed image area of interest (Image AOI).
    camera.OffsetX.TrySetToMinimum();
    camera.OffsetY.TrySetToMinimum();
    camera.Width.SetToMaximum();
    camera.Height.SetToMaximum();

    if (camera.AutoFunctionROISelector.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the Auto Function ROI for luminance statistics.
        // We want to use ROI1 for gathering the statistics

        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( true );   // ROI 1 is used for brightness control
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( false );   // ROI 2 is not used for brightness control


        // Set the ROI (in this example the complete sensor is used)
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );  // configure ROI 1
        camera.AutoFunctionROIOffsetX.SetToMinimum();
        camera.AutoFunctionROIOffsetY.SetToMinimum();
        camera.AutoFunctionROIWidth.SetToMaximum();
        camera.AutoFunctionROIHeight.SetToMaximum();
    }
    else if (camera.AutoFunctionAOISelector.IsWritable())
    {
        // Set the Auto Function AOI for luminance statistics.
        // Currently, AutoFunctionAOISelector_AOI1 is predefined to gather
        // luminance statistics.
        camera.AutoFunctionAOISelector.SetValue( AutoFunctionAOISelector_AOI1 );
        camera.AutoFunctionAOIOffsetX.SetToMinimum();
        camera.AutoFunctionAOIOffsetY.SetToMinimum();
        camera.AutoFunctionAOIWidth.SetToMaximum();
        camera.AutoFunctionAOIHeight.SetToMaximum();
    }

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the target value for luminance control.
        // A value of 0.3 means that the target brightness is 30 % of the maximum brightness of the raw pixel value read out from the sensor.
        // A value of 0.4 means 40 % and so forth.
        camera.AutoTargetBrightness.SetValue( 0.3 );

        // We are trying GainAuto = Continuous.
        cout << "Trying 'GainAuto = Continuous'." << endl;
        cout << "Initial Gain = " << camera.Gain.GetValue() << endl;

        camera.GainAuto.SetValue( GainAuto_Continuous );
    }
    else
    {
        // Set the target value for luminance control. The value is always expressed
        // as an 8 bit value regardless of the current pixel data output format,
        // i.e., 0 -> black, 255 -> white.
        camera.AutoTargetValue.TrySetValue( 80 );

        // We are trying GainAuto = Continuous.
        cout << "Trying 'GainAuto = Continuous'." << endl;
        cout << "Initial Gain = " << camera.GainRaw.GetValue() << endl;

        camera.GainAuto.SetValue( GainAuto_Continuous );
    }

    // When "continuous" mode is selected, the parameter value is adjusted repeatedly while images are acquired.
    // Depending on the current frame rate, the automatic adjustments will usually be carried out for
    // every or every other image unless the camera's micro controller is kept busy by other tasks.
    // The repeated automatic adjustment will proceed until the "once" mode of operation is used or
    // until the auto function is set to "off", in which case the parameter value resulting from the latest
    // automatic adjustment will operate unless the value is manually adjusted.
    for (int n = 0; n < 20; ++n)            // For demonstration purposes, we will grab "only" 20 images.
    {
        CBaslerUniversalGrabResultPtr ptrGrabResult;
        camera.GrabOne( 5000, ptrGrabResult );
#ifdef PYLON_WIN_BUILD
        Pylon::DisplayImage( 1, ptrGrabResult );

        //For demonstration purposes only. Wait until the image is shown.
        WaitObject::Sleep( 100 );
#endif
    }
    camera.GainAuto.SetValue( GainAuto_Off ); // Switch off GainAuto.

    if (camera.Gain.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        cout << "Final Gain = " << camera.Gain.GetValue() << endl << endl;
    }
    else
    {
        cout << "Final Gain = " << camera.GainRaw.GetValue() << endl << endl;
    }
}


void AutoExposureOnce( CBaslerUniversalInstantCamera& camera )
{
    // Check whether auto exposure is available
    if (!camera.ExposureAuto.IsWritable())
    {
        cout << "The camera does not support Exposure Auto." << endl << endl;
        return;
    }

    // Maximize the grabbed area of interest (Image AOI).
    camera.OffsetX.TrySetToMinimum();
    camera.OffsetY.TrySetToMinimum();
    camera.Width.SetToMaximum();
    camera.Height.SetToMaximum();

    if (camera.AutoFunctionROISelector.IsWritable())
    {
        // Set the Auto Function ROI for luminance statistics.
        // We want to use ROI1 for gathering the statistics
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( true );   // ROI 1 is used for brightness control
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( false );   // ROI 2 is not used for brightness control

        // Set the ROI (in this example the complete sensor is used)
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );  // configure ROI 1
        camera.AutoFunctionROIOffsetX.SetToMinimum();
        camera.AutoFunctionROIOffsetY.SetToMinimum();
        camera.AutoFunctionROIWidth.SetToMaximum();
        camera.AutoFunctionROIHeight.SetToMaximum();
    }
    else if (camera.AutoFunctionAOISelector.IsWritable())
    {
        // Set the Auto Function AOI for luminance statistics.
        // Currently, AutoFunctionAOISelector_AOI1 is predefined to gather
        // luminance statistics.
        camera.AutoFunctionAOISelector.SetValue( AutoFunctionAOISelector_AOI1 );
        camera.AutoFunctionAOIOffsetX.SetToMinimum();
        camera.AutoFunctionAOIOffsetY.SetToMinimum();
        camera.AutoFunctionAOIWidth.SetToMaximum();
        camera.AutoFunctionAOIHeight.SetToMaximum();
    }

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the target value for luminance control.
        // A value of 0.3 means that the target brightness is 30 % of the maximum brightness of the raw pixel value read out from the sensor.
        // A value of 0.4 means 40 % and so forth.
        camera.AutoTargetBrightness.SetValue( 0.3 );

        // Try ExposureAuto = Once.
        cout << "Trying 'ExposureAuto = Once'." << endl;
        cout << "Initial exposure time = ";
        cout << camera.ExposureTime.GetValue() << " us" << endl;

        // Set the exposure time ranges for luminance control.
        camera.AutoExposureTimeLowerLimit.SetToMinimum();
        // Some cameras have a very high upper limit.
        // To avoid excessive execution times of the sample, we use 1000000 us (1 s) as the upper limit.
        // If you need longer exposure times, you can set this to the maximum value.
        camera.AutoExposureTimeUpperLimit.SetValue( 1 * 1000 * 1000, FloatValueCorrection_ClipToRange );

        camera.ExposureAuto.SetValue( ExposureAuto_Once );
    }
    else
    {
        // Set the target value for luminance control. The value is always expressed
        // as an 8 bit value regardless of the current pixel data output format,
        // i.e., 0 -> black, 255 -> white.
        camera.AutoTargetValue.SetValue( 80 );

        // Try ExposureAuto = Once.
        cout << "Trying 'ExposureAuto = Once'." << endl;
        cout << "Initial exposure time = ";
        cout << camera.ExposureTimeAbs.GetValue() << " us" << endl;

        // Set the exposure time ranges for luminance control.
        camera.AutoExposureTimeAbsLowerLimit.SetToMinimum();
        // Some cameras have a very high upper limit.
        // To avoid excessive execution times of the sample, we use 1000000 us (1 s) as the upper limit.
        // If you need longer exposure times, you can set this to the maximum value.
        camera.AutoExposureTimeAbsUpperLimit.SetValue( 1 * 1000 * 1000, FloatValueCorrection_ClipToRange );

        camera.ExposureAuto.SetValue( ExposureAuto_Once );
    }

    // When the "once" mode of operation is selected,
    // the parameter values are automatically adjusted until the related image property
    // reaches the target value. After the automatic parameter value adjustment is complete, the auto
    // function will automatically be set to "off", and the new parameter value will be applied to the
    // subsequently grabbed images.
    int n = 0;
    while (camera.ExposureAuto.GetValue() != ExposureAuto_Off)
    {
        CBaslerUniversalGrabResultPtr ptrGrabResult;
        camera.GrabOne( 5000, ptrGrabResult );
#ifdef PYLON_WIN_BUILD
        Pylon::DisplayImage( 1, ptrGrabResult );

        //For demonstration purposes only. Wait until the image is shown.
        WaitObject::Sleep( 100 );
#endif
        //Make sure the loop is exited.
        if (++n > 100)
        {
            throw TIMEOUT_EXCEPTION( "The adjustment of auto exposure did not finish." );
        }
    }

    cout << "ExposureAuto went back to 'Off' after " << n << " frames." << endl;
    cout << "Final exposure time = ";
    if (camera.ExposureTime.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        cout << camera.ExposureTime.GetValue() << " us" << endl << endl;
    }
    else
    {
        cout << camera.ExposureTimeAbs.GetValue() << " us" << endl << endl;
    }
}


void AutoExposureContinuous( CBaslerUniversalInstantCamera& camera )
{
    // Check whether the Exposure Auto feature is available.
    if (!camera.ExposureAuto.IsWritable())
    {
        cout << "The camera does not support Exposure Auto." << endl << endl;
        return;
    }

    // Maximize the grabbed area of interest (Image AOI).
    camera.OffsetX.TrySetToMinimum();
    camera.OffsetY.TrySetToMinimum();
    camera.Width.SetToMaximum();
    camera.Height.SetToMaximum();

    if (camera.AutoFunctionROISelector.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the Auto Function ROI for luminance statistics.
        // We want to use ROI1 for gathering the statistics

        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( true );   // ROI 1 is used for brightness control
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIUseBrightness.TrySetValue( false );   // ROI 2 is not used for brightness control

        // Set the ROI (in this example the complete sensor is used)
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );  // configure ROI 1
        camera.AutoFunctionROIOffsetX.SetToMinimum();
        camera.AutoFunctionROIOffsetY.SetToMinimum();
        camera.AutoFunctionROIWidth.SetToMaximum();
        camera.AutoFunctionROIHeight.SetToMaximum();
    }
    else if (camera.AutoFunctionAOISelector.IsWritable())
    {
        // Set the Auto Function AOI for luminance statistics.
        // Currently, AutoFunctionAOISelector_AOI1 is predefined to gather
        // luminance statistics.
        camera.AutoFunctionAOISelector.SetValue( AutoFunctionAOISelector_AOI1 );
        camera.AutoFunctionAOIOffsetX.SetToMinimum();
        camera.AutoFunctionAOIOffsetY.SetToMinimum();
        camera.AutoFunctionAOIWidth.SetToMaximum();
        camera.AutoFunctionAOIHeight.SetToMaximum();
    }

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the target value for luminance control.
        // A value of 0.3 means that the target brightness is 30 % of the maximum brightness of the raw pixel value read out from the sensor.
        // A value of 0.4 means 40 % and so forth.
        camera.AutoTargetBrightness.SetValue( 0.3 );

        cout << "Trying 'ExposureAuto = Continuous'." << endl;
        cout << "Initial exposure time = ";
        cout << camera.ExposureTime.GetValue() << " us" << endl;

        camera.ExposureAuto.SetValue( ExposureAuto_Continuous );
    }
    else
    {
        // Set the target value for luminance control. The value is always expressed
        // as an 8 bit value regardless of the current pixel data output format,
        // i.e., 0 -> black, 255 -> white.
        camera.AutoTargetValue.SetValue( 80 );

        cout << "Trying 'ExposureAuto = Continuous'." << endl;
        cout << "Initial exposure time = ";
        cout << camera.ExposureTimeAbs.GetValue() << " us" << endl;

        camera.ExposureAuto.SetValue( ExposureAuto_Continuous );
    }

    // When "continuous" mode is selected, the parameter value is adjusted repeatedly while images are acquired.
    // Depending on the current frame rate, the automatic adjustments will usually be carried out for
    // every or every other image, unless the camera's microcontroller is kept busy by other tasks.
    // The repeated automatic adjustment will proceed until the "once" mode of operation is used or
    // until the auto function is set to "off", in which case the parameter value resulting from the latest
    // automatic adjustment will operate unless the value is manually adjusted.
    for (int n = 0; n < 20; ++n)    // For demonstration purposes, we will use only 20 images.
    {
        CBaslerUniversalGrabResultPtr ptrGrabResult;
        camera.GrabOne( 5000, ptrGrabResult );
#ifdef PYLON_WIN_BUILD
        Pylon::DisplayImage( 1, ptrGrabResult );

        //For demonstration purposes only. Wait until the image is shown.
        WaitObject::Sleep( 100 );
#endif
    }
    camera.ExposureAuto.SetValue( ExposureAuto_Off ); // Switch off Exposure Auto.

    cout << "Final exposure time = ";
    if (camera.ExposureTime.IsReadable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        cout << camera.ExposureTime.GetValue() << " us" << endl << endl;
    }
    else
    {
        cout << camera.ExposureTimeAbs.GetValue() << " us" << endl << endl;
    }
}


void AutoWhiteBalance( CBaslerUniversalInstantCamera& camera )
{
    // Check whether the Balance White Auto feature is available.
    if (!camera.BalanceWhiteAuto.IsWritable())
    {
        cout << "The camera does not support Balance White Auto." << endl << endl;
        return;
    }

    // Maximize the grabbed area of interest (Image AOI).
    camera.OffsetX.TrySetToMinimum();
    camera.OffsetY.TrySetToMinimum();
    camera.Width.SetToMaximum();
    camera.Height.SetToMaximum();

    if (camera.AutoFunctionROISelector.IsWritable()) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        // Set the Auto Function ROI for white balance.
        // We want to use ROI2
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI1 );
        camera.AutoFunctionROIUseWhiteBalance.SetValue( false );   // ROI 1 is not used for white balance
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIUseWhiteBalance.SetValue( true );   // ROI 2 is used for white balance

        // Set the Auto Function AOI for white balance statistics.
        // Currently, AutoFunctionROISelector_ROI2 is predefined to gather
        // white balance statistics.
        camera.AutoFunctionROISelector.SetValue( AutoFunctionROISelector_ROI2 );
        camera.AutoFunctionROIOffsetX.SetToMinimum();
        camera.AutoFunctionROIOffsetY.SetToMinimum();
        camera.AutoFunctionROIWidth.SetToMaximum();
        camera.AutoFunctionROIHeight.SetToMaximum();
    }
    else if (camera.AutoFunctionAOISelector.IsWritable())
    {
        // Set the Auto Function AOI for luminance statistics.
        // Currently, AutoFunctionAOISelector_AOI1 is predefined to gather
        // luminance statistics.
        camera.AutoFunctionAOISelector.SetValue( AutoFunctionAOISelector_AOI1 );
        camera.AutoFunctionAOIOffsetX.SetToMinimum();
        camera.AutoFunctionAOIOffsetY.SetToMinimum();
        camera.AutoFunctionAOIWidth.SetToMaximum();
        camera.AutoFunctionAOIHeight.SetToMaximum();
    }

    cout << "Trying 'BalanceWhiteAuto = Once'." << endl;
    cout << "Initial balance ratio: ";

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
        cout << "R = " << camera.BalanceRatio.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
        cout << "G = " << camera.BalanceRatio.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
        cout << "B = " << camera.BalanceRatio.GetValue() << endl;
    }
    else
    {
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
        cout << "R = " << camera.BalanceRatioAbs.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
        cout << "G = " << camera.BalanceRatioAbs.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
        cout << "B = " << camera.BalanceRatioAbs.GetValue() << endl;
    }

    camera.BalanceWhiteAuto.SetValue( BalanceWhiteAuto_Once );

    // When the "once" mode of operation is selected,
    // the parameter values are automatically adjusted until the related image property
    // reaches the target value. After the automatic parameter value adjustment is complete, the auto
    // function will automatically be set to "off" and the new parameter value will be applied to the
    // subsequently grabbed images.
    int n = 0;
    while (camera.BalanceWhiteAuto.GetValue() != BalanceWhiteAuto_Off)
    {
        CBaslerUniversalGrabResultPtr ptrGrabResult;
        camera.GrabOne( 5000, ptrGrabResult );
#ifdef PYLON_WIN_BUILD
        Pylon::DisplayImage( 1, ptrGrabResult );

        //For demonstration purposes only. Wait until the image is shown.
        WaitObject::Sleep( 100 );
#endif

        //Make sure the loop is exited.
        if (++n > 100)
        {
            throw TIMEOUT_EXCEPTION( "The adjustment of auto white balance did not finish." );
        }
    }

    cout << "BalanceWhiteAuto went back to 'Off' after ";
    cout << n << " frames." << endl;
    cout << "Final balance ratio: ";

    if (camera.GetSfncVersion() >= Sfnc_2_0_0) // Cameras based on SFNC 2.0 or later, e.g., USB cameras
    {
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
        cout << "R = " << camera.BalanceRatio.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
        cout << "G = " << camera.BalanceRatio.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
        cout << "B = " << camera.BalanceRatio.GetValue() << endl;
    }
    else
    {
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Red );
        cout << "R = " << camera.BalanceRatioAbs.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Green );
        cout << "G = " << camera.BalanceRatioAbs.GetValue() << "   ";
        camera.BalanceRatioSelector.SetValue( BalanceRatioSelector_Blue );
        cout << "B = " << camera.BalanceRatioAbs.GetValue() << endl;
    }
}


bool IsColorCamera( CBaslerUniversalInstantCamera& camera )
{
    StringList_t settableValues;
    camera.PixelFormat.GetSettableValues( settableValues );
    bool result = false;

    for (size_t i = 0; i < settableValues.size(); i++)
    {
        if (settableValues[i].find( String_t( "Bayer" ) ) != String_t::_npos())
        {
            result = true;
            break;
        }
    }
    return result;
}
