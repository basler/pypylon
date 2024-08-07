# This sample demonstrates the use of an interface node map.
# Here we are going to use the interface node map of a Basler CXP interface
# card to toggle 'Power Over CoaXPress' (PoCXP) between 'Auto' and 'Off'.

from os import environ
from pypylon import pylon

# First check if GENICAM_GENTL64_PATH environment variable is set.
# This is set automatically by the Basler setup when installing pylon CXP
if environ.get('GENICAM_GENTL64_PATH') is None:
    raise RuntimeError("GENICAM_GENTL64_PATH not set! Please install the CXP GenTL producer and drivers using the pylon Camera Software Suite setup.")

# We need access to the interface node map. This can only be obtained from
# a transport layer. Therefore we have to create the TL first.
tl = pylon.TlFactory.GetInstance().CreateTl('BaslerGTC/Basler/CXP')
iface_infos = tl.EnumerateInterfaces()
if iface_infos:
    print("Toggling PoCXP on these interfaces:")

for info in iface_infos:
    # Handling interface node maps is actually more complicated:
    # - create interface
    # - open interface
    # - get node map and deal with it
    # - close interface
    # - destroy interface
    # Therefore there is this context manager object called InterfaceNodeMap
    # that handles all that.
    with tl.InterfaceNodeMap(info) as nmap:
        # Some transport layers (GigE, Usb ...) only have interfaces
        # without node maps. Therefore we have to test for None.
        if nmap is None:
            # Since we are using the CXP TL, we assume there is a node map.
            raise ValueError("node map should be present")
        node = nmap.GetNode('CxpPoCxpStatus')
        old_value = node.Value
        new_value = 'Auto' if old_value == 'Off' else 'Off'
        print("    %s: %s -> %s" % (info.GetFriendlyName(), old_value, new_value))
        node.Value = new_value

# A transport layer object has to be released when it is no longer needed.
pylon.TlFactory.GetInstance().ReleaseTl(tl)
