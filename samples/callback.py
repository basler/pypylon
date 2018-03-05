from pypylon import pylon
from pypylon import genicam

camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.Open()

# Print the model name of the camera.
print("Using device ", camera.GetDeviceInfo().GetModelName())


def callback(node):
    print("Callback", type(node))
    print("Callback", node.Node.Name)


genicam.Register(camera.GainRaw.Node, callback)

camera.GainRaw = camera.GainRaw.Max

camera.Close()
