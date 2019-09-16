# This sample demonstates the usage of the GigE transport layer methods
# AnnounceRemoteDevice and RenounceRemoteDevice.

from pypylon import pylon

tl_factory = pylon.TlFactory.GetInstance()

for dev_info in tl_factory.EnumerateDevices():
    if dev_info.GetDeviceClass() == 'BaslerGigE':
        cam_info = dev_info
        print(
            "using %s @ %s (%s)" % (
                cam_info.GetModelName(),
                cam_info.GetIpAddress(),
                cam_info.GetMacAddress()
                )
            )
        break
else:
    raise EnvironmentError("no GigE device found")


def announce_renounce(tl, addr):
    ok, info = tl.AnnounceRemoteDevice(addr)
    print("announce %s: %s" % (addr, "ok" if ok else "failed"))
    if ok:
        print("found:", info.GetFullName())

    ok = tl.RenounceRemoteDevice(addr)
    print("rennounce %s: %s" % (addr, "ok" if ok else "failed"))



gige_tl = tl_factory.CreateTl('BaslerGigE')
announce_renounce(gige_tl, cam_info.GetIpAddress())

non_existant = "1.2.3.4"
announce_renounce(gige_tl, non_existant)
