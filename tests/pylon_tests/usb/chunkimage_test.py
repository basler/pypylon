from pylonusbtestcase import PylonTestCase
from pypylon import pylon
from pypylon import genicam
import unittest


class ChunkImageTestSuite(PylonTestCase):
    countOfImagesToGrab = 5

    # sample Grab_ChunkImage as test
    def test_grab_chunk_image(self):

        # Only look for usb cameras
        info = pylon.DeviceInfo()
        info.SetDeviceClass("BaslerUsb")

        # Create an instant camera object with the first found camera device that matches the specified device class.
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))

        # Open the camera.
        camera.Open()

        camera.StaticChunkNodeMapPoolSize = camera.MaxNumBuffer.GetValue()

        if genicam.IsWritable(camera.ChunkModeActive):
            camera.ChunkModeActive = True
        else:
            self.fail()

        # Enable time stamp chunks.
        camera.ChunkSelector = "Timestamp"
        camera.ChunkEnable = True

        # Enable CRC checksum chunks.
        camera.ChunkSelector = "PayloadCRC16"
        camera.ChunkEnable = True

        camera.StartGrabbingMax(self.countOfImagesToGrab)

        while camera.IsGrabbing():

            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            # RetrieveResult calls the image event handler's OnImageGrabbed method.
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Check to see if a buffer containing chunk data has been received.
            if pylon.PayloadType_ChunkData != grabResult.PayloadType:
                self.fail()

            # Since we have activated the CRC Checksum feature, we can check
            # the integrity of the buffer first.
            # Note: Enabling the CRC Checksum feature is not a prerequisite for using
            # chunks. Chunks can also be handled when the CRC Checksum feature is deactivated.
            if grabResult.HasCRC() and grabResult.CheckCRC() == False:
                self.fail()

            if not genicam.IsReadable(grabResult.ChunkTimestamp):
                self.fail()

        camera.ChunkModeActive = False


if __name__ == "__main__":
    unittest.main()
