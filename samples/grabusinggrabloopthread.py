# Grab_UsingGrabLoopThread.cpp
# This sample illustrates how to grab and process images using the grab loop thread
# provided by the Instant Camera class.

from pypylon import genicam
from pypylon import pylon

from samples.configurationeventprinter import ConfigurationEventPrinter
from samples.imageeventprinter import ImageEventPrinter

import time


def getkey():
    return input("Enter \"t\" to trigger the camera or \"e\" to exit and press enter? (t/e) ")


# Example of an image event handler.
class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        print("CSampleImageEventHandler::OnImageGrabbed called.")
        print()
        print()


if __name__ == '__main__':
    try:
        # Create an instant camera object for the camera device found first.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Register the standard configuration event handler for enabling software triggering.
        # The software trigger configuration handler replaces the default configuration
        # as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
                                     pylon.Cleanup_Delete)

        # For demonstration purposes only, add a sample configuration event handler to print out information
        # about camera use.t
        camera.RegisterConfiguration(ConfigurationEventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # The image event printer serves as sample image processing.
        # When using the grab loop thread provided by the Instant Camera object, an image event handler processing the grab
        # results must be created and registered.
        camera.RegisterImageEventHandler(ImageEventPrinter(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # For demonstration purposes only, register another image event handler.
        camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # Start the grabbing using the grab loop thread, by setting the grabLoopType parameter
        # to GrabLoop_ProvidedByInstantCamera. The grab results are delivered to the image event handlers.
        # The GrabStrategy_OneByOne default grab strategy is used.
        camera.StartGrabbing(pylon.GrabStrategy_OneByOne, pylon.GrabLoop_ProvidedByInstantCamera)

        # Wait for user input to trigger the camera or exit the program.
        # The grabbing is stopped, the device is closed and destroyed automatically when the camera object goes out of scope.
        while True:
            time.sleep(0.05)
            key = getkey()
            print(key)
            if (key == 't' or key == 'T'):
                # Execute the software trigger. Wait up to 100 ms for the camera to be ready for trigger.
                if camera.WaitForFrameTriggerReady(100, pylon.TimeoutHandling_ThrowException):
                    camera.ExecuteSoftwareTrigger();
            if (key == 'e') or (key == 'E'):
                break
    except genicam.GenericException as e:
        # Error handling.
        print("An exception occurred.", e.GetDescription())
