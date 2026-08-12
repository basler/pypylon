"""\
Buffer-factory tests that allocate pylon grab buffers with NVIDIA Warp.

These use the Warp CPU backend so they run without a GPU: they prove that a
third-party allocator whose owner objects expose __array_interface__ works with
pylon.PythonBufferFactory and the grab-result owner views. GPU-backed Warp
pinned memory is covered by the benchmarks under tests/performance/.

Requires NVIDIA Warp. Skipped automatically when it is not installed.
"""
import numpy
import pytest
from pypylon import pylon

from nvidia_warp_support import require_warp_cpu

pytestmark = pytest.mark.warp

EMULATED_WIDTH = 1024
EMULATED_HEIGHT = 1040


def _make_warp_cpu_factory(wp):
    """Return a factory allocating Warp CPU arrays, plus its live-owner map."""
    live_owners = {}

    def allocate(size):
        owner = wp.empty((int(size),), dtype=wp.uint8, device="cpu")
        pointer = int(owner.ptr)
        live_owners[pointer] = owner
        return pointer, owner, pointer, int(getattr(owner, "capacity", size))

    def free(pointer, context, keep_alive):
        live_owners.pop(int(pointer), None)

    return pylon.PythonBufferFactory(allocate, free), live_owners


def _open_emulated_camera():
    device_info = pylon.DeviceInfo()
    device_info.DeviceClass = pylon.BaslerCamEmuDeviceClass
    tl_factory = pylon.TlFactory.GetInstance()
    if not tl_factory.EnumerateDevices([device_info]):
        pytest.skip("No emulated camera available")

    camera = pylon.InstantCamera(tl_factory.CreateFirstDevice(device_info))
    camera.Open()
    return camera


def test_warp_cpu_allocator_provides_the_grab_buffer():
    """A Warp CPU array supplies the grab buffer and stays the grab-result owner."""
    wp = require_warp_cpu()
    factory, live_owners = _make_warp_cpu_factory(wp)
    camera = _open_emulated_camera()
    camera.SetBufferFactory(factory, pylon.Cleanup_None)

    try:
        with camera.GrabOne(5000) as grab_result:
            assert grab_result.GrabSucceeded()
            owner = grab_result.GetBufferOwner()
            assert owner is live_owners[grab_result.BufferAddress]
            assert int(owner.ptr) == grab_result.BufferAddress
    finally:
        camera.SetBufferFactory(None)
        camera.Close()

    assert live_owners == {}


def test_warp_cpu_owner_view_has_the_image_shape():
    """The owner view reshapes the flat Warp allocation into the grabbed image."""
    wp = require_warp_cpu()
    factory, live_owners = _make_warp_cpu_factory(wp)
    camera = _open_emulated_camera()
    camera.SetBufferFactory(factory, pylon.Cleanup_None)

    try:
        with camera.GrabOne(5000) as grab_result:
            owner_view = grab_result.GetBufferOwnerView()
            assert owner_view.shape == (EMULATED_HEIGHT, EMULATED_WIDTH)

            converted = numpy.asarray(owner_view)
            assert converted.shape == (EMULATED_HEIGHT, EMULATED_WIDTH)
            assert converted.dtype == numpy.uint8
            del converted
            del owner_view
    finally:
        camera.SetBufferFactory(None)
        camera.Close()

    assert live_owners == {}


def test_warp_cpu_buffer_is_readable_as_a_warp_array():
    """The grabbed image can be read back through the Warp owner without a copy."""
    wp = require_warp_cpu()
    factory, live_owners = _make_warp_cpu_factory(wp)
    camera = _open_emulated_camera()
    camera.SetBufferFactory(factory, pylon.Cleanup_None)

    try:
        with camera.GrabOne(5000) as grab_result:
            owner = grab_result.GetBufferOwner()
            payload_size = grab_result.PayloadSize
            warp_bytes = owner.numpy()[:payload_size]

            with grab_result.GetArrayZeroCopy() as image:
                assert image.shape == (EMULATED_HEIGHT, EMULATED_WIDTH)
                numpy.testing.assert_array_equal(image.reshape(-1), warp_bytes[: image.size])
    finally:
        camera.SetBufferFactory(None)
        camera.Close()

    assert live_owners == {}


def test_warp_cpu_allocator_serves_gen_dc_payloads():
    """A Warp CPU allocator also backs GenDC containers and their component views."""
    wp = require_warp_cpu()
    factory, live_owners = _make_warp_cpu_factory(wp)
    camera = _open_emulated_camera()
    camera.SetBufferFactory(factory, pylon.Cleanup_None)

    try:
        try:
            camera.GenDC.Value = True
        except Exception as exc:
            pytest.skip("GenDC is not supported on this emulator: %s" % exc)

        with camera.GrabOne(5000) as grab_result:
            assert grab_result.PayloadType == pylon.PayloadType_GenDC
            owner = grab_result.GetBufferOwner()
            assert owner is live_owners[grab_result.BufferAddress]

            with grab_result.GetFirstImageDataComponent() as component:
                with component.GetArrayZeroCopy() as component_image:
                    component_shape = component_image.shape
                    component_first_pixel = component_image[0, 0]

            with grab_result.GetArrayZeroCopy() as image:
                assert image.shape == component_shape
                assert image[0, 0] == component_first_pixel
    finally:
        camera.SetBufferFactory(None)
        camera.Close()

    assert live_owners == {}


def test_warp_cpu_buffers_are_released_after_a_grab_sequence():
    """Every Warp allocation is handed back when grabbing stops and the factory is cleared."""
    wp = require_warp_cpu()
    factory, live_owners = _make_warp_cpu_factory(wp)
    camera = _open_emulated_camera()
    camera.SetBufferFactory(factory, pylon.Cleanup_None)

    try:
        camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
        for _ in range(5):
            with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                assert grab_result.GrabSucceeded()
                assert grab_result.GetBufferOwner() is not None
        assert live_owners != {}
    finally:
        if camera.IsGrabbing():
            camera.StopGrabbing()
        camera.SetBufferFactory(None)
        camera.Close()

    assert live_owners == {}
