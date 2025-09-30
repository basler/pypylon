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

    def test_constructor(self):
        # CSmartInstantCameraT()
        testee = pylondataprocessing.SmartInstantCamera()
        self.assertEqual(testee.GetRecipeFilename(), "")
        self.assertFalse(testee.IsLoaded())
        # CSmartInstantCameraT(IPylonDevice* pDevice, ECleanup cleanupProcedure = Cleanup_Delete)
        testee1 = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
        self.assertEqual(testee1.GetRecipeFilename(), "")
        self.assertFalse(testee1.IsLoaded())
        # CSmartInstantCameraT(IPylonDevice* pDevice, const String_t& filename , ECleanup cleanupProcedure = Cleanup_Delete)
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee2 = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)
        self.assertEqual(testee2.GetRecipeFilename(), recipefilename)
        self.assertFalse(testee2.IsLoaded())

    def test_setrecipefilename(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera()
        self.assertEqual(testee.GetRecipeFilename(), "")
        testee.SetRecipeFilename(recipefilename)
        self.assertEqual(testee.GetRecipeFilename(), recipefilename)

    def test_load(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera()
        self.assertEqual(testee.GetRecipeFilename(), "")
        self.assertFalse(testee.IsLoaded())
        testee.Load(recipefilename)
        self.assertTrue(testee.IsLoaded())
        self.assertEqual(testee.GetRecipeFilename(), "")

    def test_loadfrombinary(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        with open(recipefilename, mode='rb') as file:
            fileContent = file.read()
        testee = pylondataprocessing.SmartInstantCamera()
        self.assertFalse(testee.IsLoaded())
        testee.LoadFromBinary(fileContent)
        self.assertTrue(testee.IsLoaded())
        testee.Unload()
        self.assertFalse(testee.IsLoaded())
        testee.LoadFromBinary(fileContent, thisdir)
        self.assertTrue(testee.IsLoaded())
        testee.Unload()
        self.assertFalse(testee.IsLoaded())

    def test_open(self):
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
        testee.Open()
        self.assertTrue(testee.IsOpen())
        testee.Close()
        self.assertFalse(testee.IsOpen())

    def test_preallocateresources(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_preallocate_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
        testee.Load(recipefilename)
        self.assertFalse(testee.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())
        testee.PreAllocateResources()
        self.assertTrue(testee.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())
        testee.DeallocateResources()
        self.assertFalse(testee.GetParameter("TestImageGenerator/@vTool/Allocated").GetValue())

    def test_startgrabbing(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)

        testee.Open()
        testee.StartGrabbingMax(3, pylon.GrabStrategy_OneByOne)
        while testee.IsGrabbing():
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
        self.assertFalse(testee.IsGrabbing())
        testee.Close()

        testee.Open()
        # StartGrabbing for an amount of images with starting the recipe
        testee.StartGrabbingMax(True, 3, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser, pylon.GrabLoop_ProvidedByUser)
        while testee.IsGrabbing():
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
        self.assertFalse(testee.IsGrabbing())
        testee.Close()

        testee.Open()
        testee.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser)
        numgrabbed = 0
        while testee.IsGrabbing() and numgrabbed<5:
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
            numgrabbed += 1
        testee.StopGrabbing()
        self.assertFalse(testee.IsGrabbing())
        testee.Close()

        testee.Open()
        testee.StartGrabbing(True, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser, pylon.GrabLoop_ProvidedByUser)
        numgrabbed = 0
        while testee.IsGrabbing() and numgrabbed<5:
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
            numgrabbed += 1
        testee.StopGrabbing(1000)
        self.assertFalse(testee.IsGrabbing())
        testee.Close()

    def test_retrieveresult(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)
        testee.Load(recipefilename)

        testee.Open()
        testee.StartGrabbing(True, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser, pylon.GrabLoop_ProvidedByUser)
        numgrabbed = 0
        while testee.IsGrabbing() and numgrabbed<5:
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
            self.assertTrue(len(result.GetContainer())>0)
            numgrabbed += 1
        testee.StopGrabbing(1000)

    def test_grabone(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)

        grabResult = testee.GrabOne(1000)
        # got valid data
        self.assertTrue(grabResult.IsValid())
        self.assertTrue(grabResult.GrabSucceeded())
        # grabbing is stopped afterwards
        self.assertFalse(testee.IsGrabbing())

        # test with running recipe
        smartGrabResult = testee.GrabOne(True, 1000)
        # got valid data
        self.assertTrue(len(smartGrabResult.GetContainer())>0)
        self.assertTrue(smartGrabResult.GrabResult.IsValid())
        self.assertTrue(smartGrabResult.GrabResult.GrabSucceeded())
        # grabbing is stopped afterwards
        self.assertFalse(testee.IsGrabbing())

        # test without running recipe
        smartGrabResult = testee.GrabOne(False, 1000)
        # got valid data
        self.assertTrue(len(smartGrabResult.GetContainer())==0)
        self.assertTrue(smartGrabResult.GrabResult.IsValid())
        self.assertTrue(smartGrabResult.GrabResult.GrabSucceeded())
        # grabbing is stopped afterwards
        self.assertFalse(testee.IsGrabbing())

    def test_setparameters(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()))
        testee.Load(recipefilename)
        self.assertTrue(len(testee.GetAllParameterNames())>0)
        self.assertTrue(testee.ContainsParameter("BarcodeReaderStarter/@vTool/MaxNumBarcodes"))
        testee.GetParameter("BarcodeReaderStarter/@vTool/MaxNumBarcodes").SetValue(1)
        self.assertEqual(testee.GetParameter("BarcodeReaderStarter/@vTool/MaxNumBarcodes").GetValue(), 1)

    def test_registersmartresulteventhandler(self):
        smartresulthandler = TSmartResultEventHandler()
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)
        testee.Open()

        # Grab with registered EventHandler
        testee.RegisterSmartResultEventHandler(smartresulthandler, pylon.RegistrationMode_Append, pylon.Cleanup_None)
        testee.StartGrabbingMax(True, 3, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser, pylon.GrabLoop_ProvidedByUser)
        while testee.IsGrabbing():
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
        self.assertFalse(testee.IsGrabbing())
        self.assertEqual(smartresulthandler.OnResultCallCount, 3)

        # Grab with deregistered EventHandler
        testee.DeregisterSmartResultEventHandler(smartresulthandler)
        testee.StartGrabbingMax(True, 3, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByUser, pylon.GrabLoop_ProvidedByUser)
        while testee.IsGrabbing():
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            self.assertTrue(result.GrabResult.GrabSucceeded())
        self.assertFalse(testee.IsGrabbing())
        self.assertEqual(smartresulthandler.OnResultCallCount, 3)
        testee.Close()

    def test_waitobject(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)

        testee.StartGrabbingMax(True, 10, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByInstantCamera)
        self.assertTrue(testee.GetGrabStopWaitObject().Wait(1000))
        self.assertFalse(testee.IsGrabbing())

        testee.StartGrabbing(True, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByInstantCamera)
        self.assertFalse(testee.GetGrabStopWaitObject().Wait(0))
        self.assertTrue(testee.IsGrabbing())
        testee.StopGrabbing()

    def test_getsmartresultwaitobject(self):
        thisdir = os.path.dirname(__file__)
        recipefilename = os.path.join(thisdir, 'smartinstantcamera_test.precipe')
        testee = pylondataprocessing.SmartInstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(self.get_filter()), recipefilename)
        testee.Open()
        testee.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)
        testee.StartGrabbingMax(True, 5, pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera, pylon.GrabLoop_ProvidedByUser)
        while testee.IsGrabbing():
            testee.ExecuteSoftwareTrigger()
            testee.GetSmartResultWaitObject().Wait(5000)
            result = testee.RetrieveResult(5000, pylon.TimeoutHandling_Return)
            self.assertTrue(result.GrabResult.IsValid())
            self.assertTrue(result.GrabResult.GrabSucceeded())
            self.assertTrue(result.Update.IsValid())
            self.assertTrue(len(result.Container) == 4)



if __name__ == "__main__":
    unittest.main()
