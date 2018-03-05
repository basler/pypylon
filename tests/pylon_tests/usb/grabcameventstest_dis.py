from pylonusbtestcase import PylonTestCase
from pypylon import pylon
from pypylon import genicam
from samples.cameraEventPrinter import CameraEventPrinter

eMyExposureEndEvent = 100


# Example handler for camera events.
class SampleCameraEventHandler(pylon.CameraEventHandler):
    # Only very short processing tasks should be performed by this method. Otherwise, the event notification will block the
    # processing of images.
    def OnCameraEvent(self, camera, userProvidedId, node):
        print()
        if userProvidedId == eMyExposureEndEvent:
            print("Exposure End event. FrameID: ", camera.EventExposureEndFrameID.Value, " Timestamp: ",
                  camera.EventExposureEndTimestamp.Value)
            # More events can be added here.


# Example of an image event handler.
class SampleImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        print("CSampleImageEventHandler.OnImageGrabbed called.")
        print()
        print()


class GrabEventTestSuite(PylonTestCase):
    # Number of images to be grabbed.
    countOfImagesToGrab = 1

    def test_grab_events(self):
        print("test_grab_event")
        self.assertTrue(True)
        # Create an example event handler. In the present case, we use one single camera handler for handling multiple camera events.
        # The handler prints a message for each received event.
        handler1 = SampleCameraEventHandler()

        # Create another more generic event handler printing out information about the node for which an event callback
        # is fired.
        handler2 = CameraEventPrinter()
        # Only look for cameras supported by Camera_t
        info = pylon.DeviceInfo()
        # info.SetDeviceClass( ## fetch deviceclass from environment ##);
        info.SetDeviceClass("BaslerUsb")

        # Create an instant camera object with the first found camera device matching the specified device class.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

        # Register the standard configuration event handler for enabling software triggering.
        # The software trigger configuration handler replaces the default configuration
        # as all currently registered configuration handlers are removed by setting the registration mode to RegistrationMode_ReplaceAll.
        camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
                                     pylon.Cleanup_Delete)

        # For demonstration purposes only, add sample configuration event handlers to print out information
        # about camera use and image grabbing.
        # camera.RegisterConfiguration(ConfigurationEventPrinter(), pylon.RegistrationMode_Append,
        #                            pylon.Cleanup_Delete)  # Camera use.

        # For demonstration purposes only, register another image event handler.
        camera.RegisterImageEventHandler(SampleImageEventHandler(), pylon.RegistrationMode_Append, pylon.Cleanup_Delete)

        # Camera event processing must be activated first, the default is off.
        camera.GrabCameraEvents = True

        # Register an event handler for the Exposure End event. For each event type, there is a "data" node
        # representing the event. The actual data that is carried by the event is held by child nodes of the
        # data node. In the case of the Exposure End event, the child nodes are EventExposureEndFrameID and EventExposureEndTimestamp.
        # The CSampleCameraEventHandler demonstrates how to access the child nodes within
        # a callback that is fired for the parent data node.
        # The user-provided ID eMyExposureEndEvent can be used to distinguish between multiple events (not shown).
        camera.RegisterCameraEventHandler(handler1, "EventExposureEndData", eMyExposureEndEvent,
                                          pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)

        # The handler is registered for both, the EventExposureEndFrameID and the EventExposureEndTimestamp
        # node. These nodes represent the data carried by the Exposure End event.
        # For each Exposure End event received, the handler will be called twice, once for the frame ID, and
        # once for the time stamp.
        camera.RegisterCameraEventHandler(handler2, "EventExposureEndFrameID", eMyExposureEndEvent,
                                          pylon.RegistrationMode_Append, pylon.Cleanup_None)
        camera.RegisterCameraEventHandler(handler2, "EventExposureEndTimestamp", eMyExposureEndEvent,
                                          pylon.RegistrationMode_Append, pylon.Cleanup_None)

        # Open the camera for setting parameters.
        camera.Open()

        camera.ExposureTime.Value = camera.ExposureTime.Min

        # Check if the device supports events.
        if not genicam.IsAvailable(camera.EventSelector):
            raise genicam.RuntimeException("The device doesn't support events.")

        # Enable sending of Exposure End events.
        # Select the event to receive.
        camera.EventSelector = "ExposureEnd"
        # Enable it.
        camera.EventNotification = "On"

        # Start the grabbing of c_countOfImagesToGrab images.
        camera.StartGrabbingMax(self.countOfImagesToGrab)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while camera.IsGrabbing():
            # Execute the software trigger. Wait up to 1000 ms for the camera to be ready for trigger.
            if camera.WaitForFrameTriggerReady(100, pylon.TimeoutHandling_ThrowException):
                camera.ExecuteSoftwareTrigger()

            # Retrieve grab results and notify the camera event and image event handlers.
            grabResult = camera.RetrieveResult(100)
            # Nothing to do here with the grab result, the grab results are handled by the registered event handler.

        # Disable sending Exposure End events.
        camera.EventSelector = "ExposureEnd"
        camera.EventNotification = "Off"
        camera.Close()


if __name__ == '__main__':
    import unittest

    unittest.main()
