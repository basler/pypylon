"""Shared helpers for pypylon Warp GPU grab samples."""

from __future__ import annotations

from dataclasses import dataclass, field

import warp as wp
from pypylon import pylon


def synchronize(device: str) -> None:
    if hasattr(wp, "synchronize_device"):
        wp.synchronize_device(device)
    else:
        wp.synchronize()


def require_cuda_device(device: str = "cuda:0") -> str:
    wp.init()
    try:
        probe = wp.empty((1,), dtype=wp.uint8, device=device)
        synchronize(device)
        del probe
    except Exception as exc:
        raise RuntimeError(
            "NVIDIA Warp CUDA device %r is not available" % device
        ) from exc
    return device


@dataclass
class WarpPinnedBufferFactory:
    """Allocate pylon grab buffers as Warp pinned CPU arrays."""

    active_buffers: dict[int, object] = field(default_factory=dict)
    factory: object = field(init=False)

    def __post_init__(self) -> None:
        active_buffers = self.active_buffers

        def allocate(size: int):
            owner = wp.empty((int(size),), dtype=wp.uint8, device="cpu", pinned=True)
            ptr = int(owner.ptr)
            capacity = int(getattr(owner, "capacity", size))
            active_buffers[ptr] = owner
            return ptr, owner, ptr, capacity

        def free(ptr, context, keep_alive) -> None:
            active_buffers.pop(int(ptr), None)

        # The callbacks capture only the buffer dictionary, avoiding a
        # PythonBufferFactory -> bound method -> helper object reference cycle.
        self.factory = pylon.PythonBufferFactory(allocate, free)


def open_first_camera() -> pylon.InstantCamera:
    camera = pylon.InstantCamera(pylon.FirstFound)
    camera.Open()
    print("Using device:", camera.DeviceInfo.ModelName)
    return camera


def set_first_available_pixel_format(camera, names: tuple[str, ...]) -> str:
    available = set(camera.PixelFormat.Symbolics)
    for name in names:
        if name in available:
            camera.PixelFormat.Value = name
            return name
    raise RuntimeError(
        "The camera does not support any of these pixel formats: "
        + ", ".join(names)
    )
