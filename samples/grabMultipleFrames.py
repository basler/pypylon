'''
Use pypylon to grab multiple image frames with hardware triggers.
Test camera: acA640-750um
Version: pypylon == 4.1.0
Maximum framerate: 1000fps
'''
from pypylon import pylon
import traceback
import numpy as np

# your recording frames
numFrames = 1000
# Initialize camera instance and open the camera
cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
cam.Open()
# Print the model name of the camera.
print("Using camera device: ", cam.GetDeviceInfo().GetModelName())

# class of image handler
class ImageHandler(pylon.ImageEventHandler):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.img_sum = []
        
    def OnImagesSkipped(self, camera, countOfSkippedImages):
        print(countOfSkippedImages, " images have been skipped.")
        
    def OnImageGrabbed(self, camera, grabResult):
        """ we get called on every image
            !! this code is run in a pylon thread context
            always wrap your code in the try .. except to capture
            errors inside the grabbing as this can't be properly reported from 
            the background thread to the foreground python code
        """
        try:
            if grabResult.GrabSucceeded():
                # check image contents
                img = grabResult.Array
                # Stack images to 3D array
                self.img_sum.append(img)
                self.count += 1
                grabResult.Release()
            else:
                raise RuntimeError("Grab Failed")
        except Exception as e:
            traceback.print_exc() 
            
# Control the parameter of the Basler camera
# Get clean powerup state
cam.UserSetSelector.Value = "Default"
cam.UserSetLoad.Execute()
# Set the io section
cam.LineSelector.Value = "Line1"
cam.LineMode.Value = "Input"
# Setup the trigger/ acquisition controls
cam.TriggerSelector.Value = "FrameStart"
cam.TriggerSource.Value = "Line1"
cam.TriggerMode.Value = "On"
cam.TriggerActivation.Value = "RisingEdge"
print("The resulting Trigger Activation is: " + str(cam.TriggerActivation.Value))

# Instantiate callback handler of camera image
handler = ImageHandler()
# handler registration for camera
cam.RegisterImageEventHandler(handler , pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)
# start capturing frames
cam.StartGrabbingMax(numFrames + 1, pylon.GrabStrategy_LatestImages, pylon.GrabLoop_ProvidedByInstantCamera)
# other hardware running time here...
cam.StopGrabbing()
cam.DeregisterImageEventHandler(handler)
cam.TriggerMode.Value = "Off"
cam.Close()
print("Recorded frames in the camera is: ", str(handler.count)) 
cameraImages = np.array(handler.img_sum).transpose(1,2,0)
# check if captured camera frames are the same with the patterns
assert cameraImages.shape[2] == numFrames