#!/usr/bin/env python3
"""\
Save and load all available node maps to or from .pfs (Pylon Feature Stream) files.

FeaturePersistence writes the opened device's parameters to disk and can read them
back into the node map; loading with validation checks that stored values apply.

Each call covers exactly one node map, so persisting a camera completely takes multiple
files. Transport settings such as FrameRetention, PacketTimeout or AutoPacketSize
belong to the stream grabber node map, not to the camera node map. A .pfs file does
not record which node map it was written for; features are matched by name, and
loading with validation reports the names the target node map does not provide.

Only the node maps that are really needed should be persisted. If only the camera
settings are nessesary then the others should not be saved and loaded.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import sys
from pypylon import pylon

# The names of the pylon feature stream files, one per node map.
CAMERA_FILENAME = "CameraDeviceNodeMap.pfs"
STREAM_GRABBER_FILENAME = "StreamGrabberNodeMap.pfs"
DEVICE_TRANSPORT_LAYER_FILENAME = "DeviceTransportLayerNodeMap.pfs"
EVENT_GRABBER_FILENAME = "EventGrabberNodeMap.pfs"
INSTANT_CAMERA_FILENAME = "InstantCameraNodeMap.pfs"

exit_code = 0

try:
    # Create an instant camera object with the camera device found first.
    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)
        print()

        print("Saving camera's node map to file...")
        # Save the content of the camera's node map into the file.
        pylon.FeaturePersistence.Save(CAMERA_FILENAME, camera.NodeMap)

        print("Saving stream grabber's node map to file...")
        # The stream grabber's node map is available while the camera is open.
        pylon.FeaturePersistence.Save(STREAM_GRABBER_FILENAME, camera.StreamGrabberNodeMap)

        print("Saving transport layer node map to file...")
        # Save the transport layer specific node map into the file.
        pylon.FeaturePersistence.Save(DEVICE_TRANSPORT_LAYER_FILENAME, camera.TLNodeMap)

        print("Saving event grabber node map to file...")
        # The event grabber's node map is available while the camera is open.
        pylon.FeaturePersistence.Save(EVENT_GRABBER_FILENAME, camera.EventGrabberNodeMap)

        print("Saving instant camera node map to file...")
        pylon.FeaturePersistence.Save(INSTANT_CAMERA_FILENAME, camera.InstantCameraNodeMap)

        print("Reading files back to the node maps...")
        # Read the content of each file back to its node map with enabled validation.
        pylon.FeaturePersistence.Load(CAMERA_FILENAME, camera.NodeMap, True)
        pylon.FeaturePersistence.Load(STREAM_GRABBER_FILENAME, camera.StreamGrabberNodeMap, True)
        pylon.FeaturePersistence.Load(DEVICE_TRANSPORT_LAYER_FILENAME, camera.TLNodeMap, True)
        pylon.FeaturePersistence.Load(EVENT_GRABBER_FILENAME, camera.EventGrabberNodeMap, True)
        pylon.FeaturePersistence.Load(INSTANT_CAMERA_FILENAME, camera.InstantCameraNodeMap, True)

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
