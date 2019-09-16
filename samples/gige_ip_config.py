# This sample demonstrates how to use the methods RestartIpConfiguration and
# ForceIp of the GigETransportLayer object. These can be necessary when
# manipulating the IP configuration of a GigE camera.

from pypylon import pylon
import random

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


ip_nums = list(map(int, cam_info.GetIpAddress().split('.')))
assert len(ip_nums) == 4
# Assume that we get a valid IP address, that is not used by another device,
# when we replace the last number of the original IP address with a random
# number. Whether this assumption applies or not depends strongly on the
# environment. For this simple sample it is OK to make such an unlikely
# assumption. DO NOT DO THAT IN A REAL APPLICATION!
last = ip_nums[3]
next = last
while next == last:
    next = random.randrange(1, 255)
ip_nums[3] = next
next_ip = "%d.%d.%d.%d" % tuple(ip_nums)

print("forcing IP address:", next_ip)
gige_tl = tl_factory.CreateTl('BaslerGigE')

gige_tl.ForceIp(
    cam_info.GetMacAddress(),
    next_ip,
    cam_info.GetSubnetMask(),
    cam_info.GetDefaultGateway()
    )

# Now we trying to find the device again, expecting that is has the same MAC
# address as before, but the new IP address.

found = False
while not found:
    for dev_info in tl_factory.EnumerateDevices():
        if dev_info.GetDeviceClass() == 'BaslerGigE':
            if dev_info.GetMacAddress() == cam_info.GetMacAddress():
                print(
                    "found %s @ %s (%s)" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress()
                        )
                    )
                found = True
                break


# Now that we forced the camera to use a new IP address, we tell it to restart
# the process of determining and assuming its IP address as it normally does.
# Depending on the value of cam_info.GetIpConfigCurrent() and the presence of a
# DHCP server, the time needed for IP reconfiguration varies widely.
print("restarting IP configuration")
gige_tl.RestartIpConfiguration(cam_info.GetMacAddress())

# Now we trying to find the device again, expecting that is has the same MAC
# address as before, but has a different IP address than the one we forced.
# Most likely it will be the one that we saw initially.

found = False
while not found:
    for dev_info in tl_factory.EnumerateDevices():
        if dev_info.GetDeviceClass() == 'BaslerGigE':
            if dev_info.GetMacAddress() == cam_info.GetMacAddress():
                print(
                    "found %s @ %s (%s)" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress()
                        )
                    )
                found = True
                break

