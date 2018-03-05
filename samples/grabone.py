from pypylon import pylon
from pypylon import genicam
import numpy

camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.Open()

# enable all chunks
camera.ChunkModeActive = True

for cf in camera.ChunkSelector.Symbolics:
    camera.ChunkSelector = cf
    camera.ChunkEnable = True

result = camera.GrabOne(100)
print("Mean Gray value:", numpy.mean(result.Array[0:20, 0]))


def ChunksOnResult(result):
    ret = ""
    for f in camera.ChunkSelector.Symbolics:
        try:
            if genicam.IsAvailable(getattr(result, "Chunk" + f)):
                ret += f + ","
        except AttributeError as e:
            # some cameras have chunkselectors which never occur in the video stream
            print(e)
    return ret


print(ChunksOnResult(result))
