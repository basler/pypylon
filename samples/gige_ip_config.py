# This sample demonstrates how to use the methods RestartIpConfiguration,
# BroadcastIpConfiguration and ForceIp of the GigETransportLayer object. These
# can be necessary when manipulating the IP configuration of a GigE camera.

from pypylon import pylon
import random

################################################################################

def format_ip_config(cfg_str):
    result = []
    cfg = int(cfg_str)
    if cfg & 1:
        result.append("PersistentIP")
    if cfg & 2:
        result.append("DHCP")
    if cfg & 4:
        result.append("LLA")
    return ", ".join(result)

################################################################################

tl_factory = pylon.TlFactory.GetInstance()

for dev_info in tl_factory.EnumerateDevices():
    if dev_info.GetDeviceClass() == 'BaslerGigE':
        cam_info = dev_info
        print(
            "using %s @ %s (%s), IP config = %s" % (
                cam_info.GetModelName(),
                cam_info.GetIpAddress(),
                cam_info.GetMacAddress(),
                format_ip_config(cam_info.GetIpConfigCurrent())
                )
            )
        break
else:
    raise EnvironmentError("no GigE device found")

################################################################################
#
# Demonstrating how to use ForceIp to assign a temporary IP address to a device.
#
################################################################################

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
ip_address = "%d.%d.%d.%d" % tuple(ip_nums)
subnet = cam_info.GetSubnetMask()
gateway = cam_info.GetDefaultGateway()
user_defined_name = cam_info.GetUserDefinedName()

print("forcing IP address:", ip_address)
gige_tl = tl_factory.CreateTl('BaslerGigE')

gige_tl.ForceIp(
    cam_info.GetMacAddress(),
    ip_address,
    subnet,
    gateway
    )

# Now we trying to find the device again, expecting that is has the same MAC
# address as before, but the new IP address.

found = False
while not found:
    for dev_info in tl_factory.EnumerateDevices():
        if dev_info.GetDeviceClass() == 'BaslerGigE':
            if dev_info.GetMacAddress() == cam_info.GetMacAddress():
                print(
                    "found %s @ %s (%s), IP config = %s" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress(),
                        format_ip_config(dev_info.GetIpConfigCurrent())
                        )
                    )
                found = True
                break

################################################################################
#
# Demonstrating how to use RestartIpConfiguration to let a device go through
# its IP configuration process.
#
################################################################################


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
                    "found %s @ %s (%s), IP config = %s" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress(),
                        format_ip_config(dev_info.GetIpConfigCurrent())
                        )
                    )
                found = True
                break

################################################################################
#
# Demonstrating how to use BroadcastIpConfiguration to assign a persistent IP
# address to a device.
#
################################################################################

print("setting persistent IP address:", ip_address)
gige_tl.BroadcastIpConfiguration(
    cam_info.GetMacAddress(),
    True,       # EnablePersistentIp
    False,      # EnableDhcp
    ip_address,
    subnet,
    gateway,
    user_defined_name
    )

# Now that we set a persistent IP address, we tell the camera to restart
# the process of determining and assuming its IP address as it normally does.
print("restarting IP configuration")
gige_tl.RestartIpConfiguration(cam_info.GetMacAddress())

# Now we trying to find the device again, expecting that is has the same MAC
# address as before, but the new IP address.

found = False
while not found:
    for dev_info in tl_factory.EnumerateDevices():
        if dev_info.GetDeviceClass() == 'BaslerGigE':
            if dev_info.GetMacAddress() == cam_info.GetMacAddress():
                print(
                    "found %s @ %s (%s), config = %s" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress(),
                        format_ip_config(dev_info.GetIpConfigCurrent())
                        )
                    )
                found = True
                break

################################################################################
#
# Demonstrating how to use BroadcastIpConfiguration to switch to DHCP and LLA
# IP configuration.
#
################################################################################

print("setting IP configuration to: DHCP, LLA")
gige_tl.BroadcastIpConfiguration(
    cam_info.GetMacAddress(),
    False,      # EnablePersistentIp
    True,       # EnableDhcp
    "",
    "",
    "",
    user_defined_name
    )

# Now that we set an IP configuration, we tell the camera to restart
# the process of determining and assuming its IP address as it normally does.
print("restarting IP configuration")
gige_tl.RestartIpConfiguration(cam_info.GetMacAddress())

# Now we trying to find the device again, expecting that is has the same MAC
# address as before.

found = False
while not found:
    for dev_info in tl_factory.EnumerateDevices():
        if dev_info.GetDeviceClass() == 'BaslerGigE':
            if dev_info.GetMacAddress() == cam_info.GetMacAddress():
                print(
                    "found %s @ %s (%s), config = %s" % (
                        dev_info.GetModelName(),
                        dev_info.GetIpAddress(),
                        dev_info.GetMacAddress(),
                        format_ip_config(dev_info.GetIpConfigCurrent())
                        )
                    )
                found = True
                break
