#!/usr/bin/env python3
"""\
Allocate grab buffers from Python and access frames with the zero-copy APIs from
pypylon 26.6.

pylon normally allocates grab buffers internally. A PythonBufferFactory lets your
code provide the memory instead. The camera writes the full grab payload into
that buffer, including GenDC containers when the device delivers them.

This sample demonstrates how the buffer-factory APIs fit together with the
current zero-copy surface:

  * GetArrayZeroCopy() on PylonDataComponent — scoped zero-copy (recommended;
    works for classic payloads and GenDC via GetFirstImageDataComponent).
  * GetArrayZeroCopy() on GrabResult — same contract on the grab result itself.
  * GetArray(copy=False) — persistent NumPy view for hand-offs outside the
    current scope (classic image payloads).
  * GetBufferOwner() — the Python keepalive object from the factory callback.
  * ConvertToArray() — format conversion into a separate owned NumPy array
    while the grab result is still valid.

For non-NumPy owners (Warp pinned memory, CUDA), see
samples/pylon/grab_warp_pinned/ and GetBufferOwnerView().

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound (or CreateFirstDevice):
https://docs.baslerweb.com/camera-emulation
"""
import ctypes
import sys

from pypylon import pylon

COUNT_OF_IMAGES_TO_GRAB = 10
TIMEOUT_MS = 5000
DEMO_CONVERTED_FRAMES = 1


def build_ctypes_factory():
    """Return a factory that allocates grab buffers as ctypes byte arrays."""
    active_buffers = {}

    def allocate(size):
        buf = (ctypes.c_ubyte * size)()
        ptr = ctypes.addressof(buf)
        active_buffers[ptr] = buf
        return ptr, buf, ptr, size

    def free(ptr, context, keep_alive):
        active_buffers.pop(ptr, None)

    return pylon.PythonBufferFactory(allocate, free), active_buffers


def demonstrate_zero_copy_apis(grab_result, frame_index):
    """Show how master zero-copy APIs compose with a Python buffer factory."""
    owner = grab_result.GetBufferOwner()
    print(
        f"frame {frame_index}: payload={grab_result.PayloadSize} bytes, "
        f"buffer_context={grab_result.BufferContext:#x}, "
        f"owner={type(owner).__name__}"
    )

    # Recommended path for classic payloads and GenDC: component + scoped view.
    with grab_result.GetFirstImageDataComponent() as component:
        with component.GetArrayZeroCopy() as image:
            print(
                f"  GetArrayZeroCopy(component): "
                f"{component.Width}x{component.Height}, pixel={image[0, 0]}"
            )

        if frame_index < DEMO_CONVERTED_FRAMES:
            converter = pylon.ImageFormatConverter()
            converter.OutputPixelFormat = pylon.PixelType_Mono8
            converted = converter.ConvertToArray(component)
            print(
                f"  ConvertToArray(component): shape={converted.shape}, "
                f"dtype={converted.dtype}"
            )

    if grab_result.PayloadType != pylon.PayloadType_GenDC:
        # GrabResult access is convenient for classic single-image payloads.
        with grab_result.GetArrayZeroCopy() as grab_view:
            print(
                f"  GetArrayZeroCopy(grab_result): shape={grab_view.shape}, "
                f"pixel={grab_view[0, 0]}"
            )

        # Persistent view: valid after this function returns until released.
        persistent = grab_result.GetArray(copy=False)
        print(
            f"  GetArray(copy=False): shape={persistent.shape}, "
            f"ptr={hex(persistent.ctypes.data)}"
        )
        del persistent


exit_code = 0
try:
    factory, active_buffers = build_ctypes_factory()

    with pylon.InstantCamera(pylon.FirstFound) as camera:
        print("Using device:", camera.DeviceInfo.ModelName)

        camera.MaxNumBuffer.Value = 5
        camera.SetBufferFactory(factory, pylon.Cleanup_None)

        try:
            camera.StartGrabbingMax(COUNT_OF_IMAGES_TO_GRAB)

            frame_index = 0
            while camera.IsGrabbing():
                with camera.RetrieveResult(
                    TIMEOUT_MS, pylon.TimeoutHandling_ThrowException
                ) as grab_result:
                    if not grab_result.GrabSucceeded():
                        print(
                            "Error:",
                            f"{grab_result.ErrorCode:#x}",
                            grab_result.ErrorDescription,
                        )
                        continue

                    demonstrate_zero_copy_apis(grab_result, frame_index)
                    frame_index += 1
        finally:
            if camera.IsGrabbing():
                camera.StopGrabbing()
            camera.SetBufferFactory(None)

    if active_buffers:
        raise RuntimeError("factory still tracks buffers after grabbing stopped")

except Exception as exc:
    print("An exception occurred:", exc)
    import traceback

    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)
