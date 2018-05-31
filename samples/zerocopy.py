"""This sample shows how some time can be saved by accessing the image buffer
without copying its contents. Keep in mind that while a zero-copy array has a
reference to the image buffer, this buffer cannot be released and cannot be
reused for grabbing.
"""
import numpy
import time
from pypylon import pylon

cam = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
cam.Open()
print("camera model: %s" % cam.DeviceModelName.GetValue())
print("AOI: %d x %d" % (cam.Width.GetValue(), cam.Height.GetValue()))
print("payload size: %d\n" % cam.PayloadSize.GetValue())

pxl_sum = 0
time_zc = 0
count_zc = 0
time_cpy = 0
count_cpy = 0
cam.StartGrabbing(pylon.GrabStrategy_OneByOne)

deadline = time.perf_counter() + 10
print("Using zero copy for 10 seconds.")
while time.perf_counter() < deadline:
    with cam.RetrieveResult(1000) as result:
        start = time.perf_counter()
        with result.GetArrayZeroCopy() as zc:
            pxl_sum += zc[0, 0]
        time_zc += time.perf_counter() - start
    count_zc += 1

deadline = time.perf_counter() + 10
print("Using copy for 10 seconds.")
while time.perf_counter() < deadline:
    with cam.RetrieveResult(1000) as result:
        start = time.perf_counter()
        pxl_sum += result.GetArray()[0, 0]
        time_cpy += time.perf_counter() - start
    count_cpy += 1

cam.StopGrabbing()
cam.Close()


print(
    " zc: %.3g s,  %d images, %.3g s / per image" %
    (time_zc, count_zc, time_zc / count_zc)
    )
print(
    "cpy: %.3g s,  %d images, %.3g s / per image" %
    (time_cpy, count_cpy, time_cpy / count_cpy)
    )
ratio = (time_cpy * count_zc) / (time_zc * count_cpy)
print("zero copy is %.1f times faster" % ratio)
