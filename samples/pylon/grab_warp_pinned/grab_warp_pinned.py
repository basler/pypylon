#!/usr/bin/env python3
"""\
Grab Mono8 frames into Warp pinned memory and process them on CUDA.

The camera writes into Warp pinned CPU memory supplied by a Python buffer
factory. Each frame is copied to CUDA with Warp, then the pylon grab buffer is
released as soon as that device copy is synchronized. A background thread runs a
small normalization kernel so acquisition can overlap processing.

Requires an NVIDIA GPU and `pip install warp-lang`. For NumPy-based buffer
factories and the standard zero-copy APIs, see
samples/pylon/grab_buffer_factory/grab_buffer_factory.py.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import os
import queue
import sys
import threading

_INCLUDE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "common")
)
if _INCLUDE_DIR not in sys.path:
    sys.path.insert(0, _INCLUDE_DIR)

import warp as wp
from pypylon import pylon

from warp_bufferfactory_common import (
    WarpPinnedBufferFactory,
    open_first_camera,
    require_cuda_device,
    set_first_available_pixel_format,
    synchronize,
)

FRAMES_TO_GRAB = 100
DEVICE = "cuda:0"
STOP = object()


@wp.kernel
def normalize_u8_to_f32_kernel(
    src: wp.array2d(dtype=wp.uint8),
    dst: wp.array2d(dtype=wp.float32),
    pixel_count: int,
):
    index = wp.tid()
    if index >= pixel_count:
        return

    width = dst.shape[1]
    row = index // width
    col = index - row * width
    dst[row, col] = wp.float32(src[row, col]) / wp.float32(255.0)


def processing_worker(work_queue, error_queue, device):
    while True:
        item = work_queue.get()
        try:
            if item is STOP:
                return

            try:
                frame_index, device_frame = item
                normalized = wp.empty(
                    device_frame.shape,
                    dtype=wp.float32,
                    device=device,
                )
                pixel_count = int(device_frame.shape[0] * device_frame.shape[1])
                wp.launch(
                    normalize_u8_to_f32_kernel,
                    dim=pixel_count,
                    inputs=[device_frame, normalized, pixel_count],
                    device=device,
                )
                synchronize(device)

                if frame_index % 25 == 0:
                    print(
                        "processed frame %d: %s" % (frame_index, tuple(device_frame.shape))
                    )
            except Exception as exc:
                error_queue.put(exc)
        finally:
            work_queue.task_done()


exit_code = 0
camera = None
buffers = None
work_queue = None
worker = None

try:
    device = require_cuda_device(DEVICE)
    buffers = WarpPinnedBufferFactory()
    work_queue = queue.Queue(maxsize=4)
    error_queue = queue.Queue()
    worker = threading.Thread(
        target=processing_worker,
        args=(work_queue, error_queue, device),
        daemon=True,
    )
    worker.start()

    camera = open_first_camera()
    pixel_format = set_first_available_pixel_format(camera, ("Mono8",))
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

            host_view = result.GetBufferOwnerView()
            device_frame = host_view.to(device)
            synchronize(device)
            del host_view

        work_queue.put((frame_index, device_frame))
        if not error_queue.empty():
            raise RuntimeError("GPU processing worker failed") from error_queue.get()
        frame_index += 1

    work_queue.join()
    if not error_queue.empty():
        raise RuntimeError("GPU processing worker failed") from error_queue.get()
    print("processed %d frames" % frame_index)

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
    if work_queue is not None:
        work_queue.put(STOP)
        work_queue.join()
    if worker is not None:
        worker.join(timeout=2.0)
    if camera is not None:
        if camera.IsGrabbing():
            camera.StopGrabbing()
        camera.SetBufferFactory(None)
        camera.Close()

sys.exit(exit_code)
