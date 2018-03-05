import unittest
import os
import sys
num = 3
os.environ["PYLON_CAMEMU"] = "%d" % num
from pypylon import pylon

def get_class_and_filter():
    device_class = "BaslerCamEmu"
    di = pylon.DeviceInfo()
    di.SetDeviceClass(device_class)
    return device_class, [di]


class PylonEmuTestCase(unittest.TestCase):
    num_dev = num
    device_class, device_filter = get_class_and_filter()

    def create_first(self):
        tlf = pylon.TlFactory.GetInstance()
        return pylon.InstantCamera(tlf.CreateFirstDevice(self.device_filter[0]))


