# ===============================================================================
# pylon data processing
# sample using and parameterizing the Camera vTool(no license required)
# ===============================================================================
import os
num = 2
os.environ["PYLON_CAMEMU"] = "%d" % num
from pypylon import pylondataprocessing
from pypylon import pylon
from pypylon import genicam

import sys

# Number of images to be grabbed.
countOfImagesToGrab = 100

# The exit code of the sample application.
exitCode = 0

try:
    # This object is used for collecting the output data.
    resultCollector = pylondataprocessing.GenericOutputObserver()
    
    # Create a recipe representing a design created using
    # the pylon Viewer Workbench.
    recipe = pylondataprocessing.Recipe()
    
    # Load the recipe file.
    thisdir = os.path.dirname(__file__)
    recipefilename = os.path.join(thisdir, 'dataprocessing_camera.precipe')
    recipe.Load(recipefilename)
    
    # For demonstration purposes only
    # Let's check the Pylon::CDeviceInfo properties of the camera we are going to use.
    # Basler recommends using the DeviceClass and the UserDefinedName to identify a camera.
    # The UserDefinedName is taken from the DeviceUserID parameter that you can set in the pylon Viewer's Features pane.
    # Note: USB cameras must be disconnected and reconnected or reset to provide the new DeviceUserID.
    # This is due to restrictions defined by the USB standard.
    print("Properties used for selecting a camera device")
    devicePropertySelector = recipe.GetParameter("MyCamera/@vTool/DevicePropertySelector")
    if (genicam.IsWritable(devicePropertySelector)):
        deviceKey = recipe.GetParameter("MyCamera/@vTool/DevicePropertyKey");
        deviceValue = recipe.GetParameter("MyCamera/@vTool/DevicePropertyValue");
        for i in range(devicePropertySelector.Min, devicePropertySelector.Max):
            devicePropertySelector.SetValue(i);
            print(deviceKey.GetValue() + "=" + deviceValue.GetValue())
    else:
        print("The first camera device found is used.")

    # For demonstration purposes only
    # Print available parameters.
    print()
    print(recipe.GetAllParameterNames())

    # Allocate the required resources. This includes the camera device.
    recipe.PreAllocateResources()

    # For demonstration purposes only
    print()
    print("Selected camera device:")
    parameter = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceModelName");
    print("ModelName=" + (parameter.ToString() if genicam.IsReadable(parameter) else "N/A"))
    parameter = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceSerialNumber");
    print("SerialNumber=" + (parameter.ToString() if genicam.IsReadable(parameter) else "N/A"))
    parameter = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceVendorName");
    print("VendorName=" + (parameter.ToString() if genicam.IsReadable(parameter) else "N/A"))
    parameter = recipe.GetParameter("MyCamera/@vTool/SelectedDeviceUserDefinedName");
    print("UserDefinedName=" + (parameter.ToString() if genicam.IsReadable(parameter) else "N/A"))
    # StringParameterName is the type of the parameter.
    # MyCamera is the name of the vTool.
    # Use @vTool if you want to access the vTool parameters.
    # Use @CameraInstance if you want to access the parameters of the CInstantCamera object used internally.
    # Use @DeviceTransportLayer if you want to access the transport layer parameters.
    # Use @CameraDevice if you want to access the camera device parameters.
    # Use @StreamGrabber0 if you want to access the camera device parameters.
    # SelectedDeviceUserDefinedName is the name of the parameter.

    # For demonstration purposes only
    # Print available parameters after allocating resources. Now we can access the camera parameters.
    print()
    print(recipe.GetAllParameterNames())
    
    # For demonstration purposes only
    # Print available output names.
    print()
    print(recipe.GetOutputNames())

    # Register the helper object for receiving all output data.
    recipe.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append);

    # Start the processing. The recipe is triggered internally
    # by the camera vTool for each image.
    recipe.Start()
    
    testImage1 = True
    testImageSelector = recipe.GetParameter("MyCamera/@CameraDevice/TestImageSelector|MyCamera/@CameraDevice/TestPattern");
    for i in range(0, countOfImagesToGrab):
        if resultCollector.GetWaitObject().Wait(5000):
            # Get the recipe dependend dictionary; key is the pin name and the value is a variant object
            result = resultCollector.RetrieveResult()
            variant = result["Image"]
            if not variant.HasError():
                # Print result data
                pylonimage = variant.ToImage()
                print("SizeX: ", pylonimage.Width)
                print("SizeY: ", pylonimage.Height)
                img = pylonimage.Array
                print("Gray value of first pixel: ", img[0, 0])
                pylonimage.Release()
                # Change a parameter
                if (i % 10 == 0):
                    testImage1 = not testImage1;
                    testImageSelector.SetValue("Testimage1" if testImage1 else "Testimage2")
            else:
                print("Error: " + variant.GetErrorDescription())
        else:
            print("Result timeout")
            break

    # Stop the processing.
    recipe.Stop()
    
    # Optionally, deallocate resources.
    recipe.DeallocateResources()
    
    # Unload the recipe and free all created vTools
    recipe.Unload()
    
except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1
except Exception as e:
    print("An unexpected exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)
