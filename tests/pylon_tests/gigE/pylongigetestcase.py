import unittest
from pypylon import pylon

def get_class_and_filter():
    device_class = "BaslerGigE"
    di = pylon.DeviceInfo()
    di.SetDeviceClass(device_class)
    return device_class, [di]

class PylonTestCase(unittest.TestCase):
    device_class, device_filter = get_class_and_filter()

    def create_first(self):
        tlf = pylon.TlFactory.GetInstance()
        return pylon.InstantCamera(tlf.CreateFirstDevice(self.device_filter[0]))
