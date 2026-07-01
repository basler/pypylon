"""\
Warp buffer-factory performance benchmarks.

Requires NVIDIA Warp, an emulated camera, and an NVIDIA GPU with CUDA.
Skipped automatically when CUDA hardware is not available.
"""
import os

os.environ.setdefault("PYLON_CAMEMU", "3")
os.environ.setdefault("WARP_CACHE_PATH", "/tmp/pypylon-warp-cache")

import pytest
from pypylon import pylon

from nvidia_warp_support import require_warp_cuda

pytestmark = [pytest.mark.nvidia, pytest.mark.warp]

try:
    import pytest_benchmark  # noqa: F401
except Exception:
    @pytest.fixture
    def benchmark():
        pytest.skip("pytest-benchmark is not installed")


def _device_filter() -> list[pylon.DeviceInfo]:
    di = pylon.DeviceInfo()
    di.SetDeviceClass("BaslerCamEmu")
    return [di]


def _require_emulated_camera() -> pylon.InstantCamera:
    tlf = pylon.TlFactory.GetInstance()
    devices = tlf.EnumerateDevices(_device_filter())
    if not devices:
        pytest.skip("No BaslerCamEmu device available for Warp benchmarks")

    camera = pylon.InstantCamera(tlf.CreateFirstDevice(_device_filter()[0]))
    camera.Open()
    return camera


def _warp_synchronize(wp, device) -> None:
    if hasattr(wp, "synchronize_device"):
        wp.synchronize_device(device)
    elif hasattr(wp, "synchronize"):
        wp.synchronize()


def _make_warp_pinned_factory(wp):
    active_buffers = {}
    try:
        probe = wp.empty((1,), dtype=wp.uint8, device="cpu", pinned=True)
        del probe
    except TypeError as exc:
        pytest.skip("NVIDIA Warp does not support pinned CPU allocation here: %s" % exc)

    def allocate(size):
        owner = wp.empty((size,), dtype=wp.uint8, device="cpu", pinned=True)
        ptr = int(owner.ptr)
        capacity = int(getattr(owner, "capacity", size))
        active_buffers[ptr] = owner
        return ptr, owner, ptr, capacity

    def free(ptr, context, keep_alive):
        active_buffers.pop(ptr, None)

    return pylon.PythonBufferFactory(allocate, free), active_buffers


def test_perf_warp_baseline_grabresult_array_copy_to_cuda(benchmark) -> None:
    wp, device = require_warp_cuda()
    camera = _require_emulated_camera()
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    def run() -> tuple[int, int]:
        with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as result:
            if not result.GrabSucceeded():
                raise RuntimeError(result.ErrorDescription)
            host_copy = result.Array
            device_frame = wp.array(data=host_copy, dtype=wp.uint8, device=device)
            _warp_synchronize(wp, device)
            shape = tuple(device_frame.shape)
            del device_frame
            return shape

    try:
        shape = benchmark(run)
    finally:
        camera.StopGrabbing()
        camera.Close()

    assert shape[0] > 0
    assert shape[1] > 0
    benchmark.extra_info["path"] = "GrabResult.Array copy, then Warp host-to-device copy"


def test_perf_warp_bufferfactory_pinned_owner_to_cuda(benchmark) -> None:
    wp, device = require_warp_cuda()
    camera = _require_emulated_camera()
    factory, active_buffers = _make_warp_pinned_factory(wp)
    camera.SetBufferFactory(factory, pylon.Cleanup_None)
    camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    def run() -> tuple[int, int]:
        with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as result:
            if not result.GrabSucceeded():
                raise RuntimeError(result.ErrorDescription)
            view = result.GetBufferOwnerView()
            device_frame = view.to(device)
            _warp_synchronize(wp, device)
            shape = tuple(getattr(view, "shape", (result.Height, result.Width)))
            del device_frame
            del view
            return shape

    try:
        shape = benchmark(run)
    finally:
        if camera.IsGrabbing():
            camera.StopGrabbing()
        camera.SetBufferFactory(None)
        camera.Close()

    assert shape[0] > 0
    assert shape[1] > 0
    assert not active_buffers
    benchmark.extra_info["path"] = "Warp pinned host buffer factory, then Warp host-to-device copy"
