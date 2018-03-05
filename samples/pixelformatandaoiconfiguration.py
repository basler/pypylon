# Contains a configuration that sets pixel data format and Image AOI.

from pypylon import pylon
from pypylon import genicam


class CPixelFormatAndAoiConfiguration(pylon.ConfigurationEventHandler):
    def OnOpened(self, camera):
        try:
            # Maximize the Image AOI.
            if genicam.IsWritable(camera.OffsetX):
                camera.OffsetX = camera.OffsetX.Min
            if genicam.IsWritable(camera.OffsetY):
                camera.OffsetY = camera.OffsetY.Min
            camera.Width = camera.Width.Max
            camera.Height = camera.Height.Max

            # Set the pixel data format.
            camera.PixelFormat = "Mono8"
        except genicam.GenericException as e:
            raise genicam.RuntimeException("Could not apply configuration. GenICam::GenericException \
                                            caught in OnOpened method msg=%s" % e.what())
