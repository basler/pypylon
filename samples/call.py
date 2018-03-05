'''
Created on 09.06.2015

@author: TMoeller
'''

from pypylon import pylon

cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
cam.Open()
print(cam.GetSfncVersion)
cam.MaxNumBuffer = 22

cam.GainRaw.Value = 127
print(cam.GainRaw)

print(cam.MaxNumBuffer)
cam.Close()

print("done")
