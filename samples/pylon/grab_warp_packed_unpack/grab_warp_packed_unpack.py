#!/usr/bin/env python3
"""\
Grab packed 10/12-bit Mono/Bayer frames and unpack them with Warp on CUDA.

For cameras that support packed raw formats such as Mono12p or BayerRG12p, the
camera writes packed bytes into Warp pinned CPU memory. Those bytes are copied
to CUDA and pypylon.warp.unpack_to_uint16() expands them to a shaped uint16
image on the GPU.

Requires an NVIDIA GPU and `pip install warp-lang`. For NumPy-based buffer
factories, see samples/pylon/grab_buffer_factory/grab_buffer_factory.py.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import os
import sys

_INCLUDE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "common")
)
if _INCLUDE_DIR not in sys.path:
    sys.path.insert(0, _INCLUDE_DIR)

import warp as wp
from pypylon import pylon
from pypylon import warp as pylon_warp

from warp_bufferfactory_common import (
    WarpPinnedBufferFactory,
    open_first_camera,
    require_cuda_device,
    set_first_available_pixel_format,
    synchronize,
)

FRAMES_TO_GRAB = 50
DEVICE = "cuda:0"

PACKED_PIXEL_FORMATS = (
    "BayerRG12p",
    "BayerGB12p",
    "BayerGR12p",
    "BayerBG12p",
    "Mono12p",
    "BayerRG10p",
    "BayerGB10p",
    "BayerGR10p",
    "BayerBG10p",
    "Mono10p",
    "BayerRG12Packed",
    "BayerGB12Packed",
    "BayerGR12Packed",
    "BayerBG12Packed",
    "Mono12Packed",
    "Mono12packed",
    "Mono10Packed",
    "Mono10packed",
)


@wp.kernel
def scale_u16_to_f32_kernel(
    src: wp.array2d(dtype=wp.uint16),
    dst: wp.array2d(dtype=wp.float32),
    pixel_count: int,
    max_value: float,
):
    index = wp.tid()
    if index >= pixel_count:
        return

    width = dst.shape[1]
    row = index // width
    col = index - row * width
    dst[row, col] = wp.float32(src[row, col]) / wp.float32(max_value)


def bit_depth_from_name(pixel_format):
    if "10" in pixel_format:
        return 10
    if "12" in pixel_format:
        return 12
    raise ValueError("unsupported packed bit depth in %r" % pixel_format)


exit_code = 0
camera = None
buffers = None

try:
    device = require_cuda_device(DEVICE)
    buffers = WarpPinnedBufferFactory()
    camera = open_first_camera()
    pixel_format = set_first_available_pixel_format(camera, PACKED_PIXEL_FORMATS)
    bit_depth = bit_depth_from_name(pixel_format)
    max_value = float((1 << bit_depth) - 1)
    print("Using pixel format", pixel_format)

    camera.MaxNumBuffer.Value = 8
    camera.SetBufferFactory(buffers.factory, pylon.Cleanup_None)
    camera.StartGrabbingMax(FRAMES_TO_GRAB, pylon.GrabStrategy_OneByOne)

    frame_index = 0
    while camera.IsGrabbing():
        with camera.RetrieveResult(
            5000,
            pylon.TimeoutHandling_ThrowException,
        ) as result:
            if not result.GrabSucceeded():
                raise RuntimeError(result.ErrorDescription)

            width = result.Width
            height = result.Height
            raw_host = result.GetBufferOwnerView(raw=True)
            raw_cuda = raw_host.to(device)
            synchronize(device)
            del raw_host

        image_u16 = pylon_warp.unpack_to_uint16(
            raw_cuda,
            pixel_format,
            width,
            height,
            device=device,
        )
        normalized = wp.empty(image_u16.shape, dtype=wp.float32, device=device)
        pixel_count = int(image_u16.shape[0] * image_u16.shape[1])
        wp.launch(
            scale_u16_to_f32_kernel,
            dim=pixel_count,
            inputs=[image_u16, normalized, pixel_count, max_value],
            device=device,
        )
        synchronize(device)

        if frame_index % 10 == 0:
            print("unpacked frame %d: %s" % (frame_index, tuple(image_u16.shape)))
        frame_index += 1

    print("unpacked %d frames" % frame_index)

    if buffers.active_buffers:
        raise RuntimeError(
            "%d grab buffers still active" % len(buffers.active_buffers)
        )
except Exception as e:
    print("An exception occurred:", e)
    import traceback

    traceback.print_exc()
    exit_code = 1
finally:
    if camera is not None:
        if camera.IsGrabbing():
            camera.StopGrabbing()
        camera.SetBufferFactory(None)
        camera.Close()

sys.exit(exit_code)
