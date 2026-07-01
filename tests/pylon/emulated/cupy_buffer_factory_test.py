"""\
CuPy buffer-factory tests for CUDA owner keepalive and proxy views.

Requires an NVIDIA GPU and CuPy. Skipped automatically when either is missing.
"""
import pytest
from pypylon import pylon

from nvidia_warp_support import require_cupy

pytestmark = [pytest.mark.nvidia, pytest.mark.cupy]


def test_python_buffer_factory_cupy_owner_proxy():
    """CUDA owner objects registered by the buffer factory are exposed via LookupBufferKeepAlive."""
    cupy = require_cupy()

    def allocate(size):
        arr = cupy.empty((size,), dtype=cupy.uint8)
        return (int(arr.data.ptr), arr, 77, size)

    factory = pylon.PythonBufferFactory(allocate)
    ptr, context = factory.DebugAllocateBuffer(64)
    assert context == 77

    owner = pylon.LookupBufferKeepAlive(ptr)
    assert owner is not None
    assert hasattr(owner, "__cuda_array_interface__")
    assert int(owner.__cuda_array_interface__["data"][0]) == ptr

    proxy = pylon._PylonOwnerView(owner, pylon.GrabResult())
    assert int(proxy.__cuda_array_interface__["data"][0]) == int(
        owner.__cuda_array_interface__["data"][0]
    )

    factory.DebugFreeBuffer(ptr, context)
    assert pylon.LookupBufferKeepAlive(ptr) is None
