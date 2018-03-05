# Contains a Camera Event Handler that prints a message for each event method call.

from pypylon import pylon
from pypylon import genicam


class CameraEventPrinter(pylon.CameraEventHandler):
    def OnCameraEvent(self, camera, userProvidedId, node):
        print("OnCameraEvent event for device ", camera.GetDeviceInfo().GetModelName())
        print("User provided ID: ", userProvidedId)
        print("Event data node name: ", node.GetName())
        value = genicam.CValuePtr(node)
        if value.IsValid():
            print("Event node data: ", value.ToString())
        print()
