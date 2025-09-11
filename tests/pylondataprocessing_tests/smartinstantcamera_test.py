import os
num = 1
if int(os.environ.get("PYLON_CAMEMU", 0)) < num:
    os.environ["PYLON_CAMEMU"] = "%d" % num
from pylondataprocessingtestcase import PylonDataProcessingTestCase
from pypylon import genicam
from pypylon import pylon
from pypylon import pylondataprocessing
import unittest

class TSmartResultEventHandler(pylondataprocessing.SmartResultEventHandler):
    def __init__(self):
        pylondataprocessing.SmartResultEventHandler.__init__(self)
        self.Result = None
        self.Camera = None
        self.Message = None
        self.OnResultCallCount = 0
        self.OnDataProcessingErrorCallCount = 0

    def OnResult(self, camera, result):
        print("OnResult")
        self.Result = result
        self.camera = camera
        self.OnResultCallCount += 1

    def OnDataProcessingError(self, camera, message):
        print("OnDataProcessingError")
        self.camera = camera
        self.Message = message
        self.OnDataProcessingErrorCallCount += 1
    

class SmartInstantCameraTestSuite(PylonDataProcessingTestCase):

    def get_filter(self):
        device_class = "BaslerCamEmu"
        di = pylon.DeviceInfo()
        di.SetDeviceClass(device_class)
        return di


    def test_init(self):
        testee1 = pylondataprocessing.SmartInstantCamera()
        smartresulthandler = TSmartResultEventHandler()
        
        # Load the recipe file.
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')

        # Create an instant camera object with the camera device found first.
        camera = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)
        camera.Open()

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer.Value = 5

        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(3)
        
        camera.RegisterSmartResultEventHandler(smartresulthandler, pylon.RegistrationMode_Append, pylon.Cleanup_None)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            
            # Image grabbed successfully?
            if result.GrabResult.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", result.GrabResult.Width)
                print("SizeY: ", result.GrabResult.Height)
                img = result.GrabResult.Array
                print("Gray value of first pixel: ", img[0, 0])
                # Print the barcodes
                variant = result.Container["Barcodes"]
                if not variant.HasError():
                    # Print result data
                    for barcodeIndex in range(0, variant.NumArrayValues):
                        print(variant.GetArrayValue(barcodeIndex).ToString())
                else:
                    print("Error: " + variant.GetErrorDescription())
                # Print the data matrix codes
                variant = result.Container["DataMatrixCodes"]
                if not variant.HasError():
                    # Print result data
                    for barcodeIndex in range(0, variant.NumArrayValues):
                        print(variant.GetArrayValue(barcodeIndex).ToString())
                else:
                    print("Error: " + variant.GetErrorDescription())
            else:
                print("Error: ", result.GrabResult.ErrorCode, result.GrabResult.ErrorDescription)
            result.Release()
        camera.Close()

if __name__ == "__main__":
    unittest.main()
