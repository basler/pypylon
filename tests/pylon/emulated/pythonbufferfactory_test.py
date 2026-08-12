"""\
This unit test checks the Python buffer-factory API introduced by
src/pylon/pylon.i (pylon.PythonBufferFactory, pylon._LookupBufferOwner) and the
grab-result owner views it enables in src/pylon/GrabResultPtr.i.

The tests cover the allocator callback contract, the keepalive bookkeeping that
keeps allocator objects alive while pylon owns a buffer, and the zero-copy views
a grab result exposes for classic image and GenDC payloads.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import ctypes
import gc
import numpy
import threading
import unittest
import weakref


EMULATED_WIDTH = 1024
EMULATED_HEIGHT = 1040


class _HostOwner:
    """Allocator object backed by plain host memory, without an array protocol."""

    def __init__(self, size):
        self.block = (ctypes.c_ubyte * size)()
        self.pointer = ctypes.addressof(self.block)
        self.nbytes = size


class _NumpyOwner(numpy.ndarray):
    """Allocator object backed by NumPy memory, exposing the NumPy array protocol."""

    def __new__(cls, size):
        return numpy.empty(size, dtype=numpy.uint8).view(cls)

    @property
    def pointer(self):
        return self.ctypes.data


class _StridedHostOwner:
    """Allocator object that reports explicit strides, as NVIDIA Warp CPU arrays do."""

    def __init__(self, size):
        self.block = (ctypes.c_ubyte * size)()
        self.pointer = ctypes.addressof(self.block)
        self.nbytes = size
        self.__array_interface__ = {
            "shape": (size,),
            "typestr": "|u1",
            "strides": (1,),
            "data": (self.pointer, False),
            "version": 3,
        }


class _CudaLikeOwner:
    """Allocator object that advertises host memory through the CUDA array protocol."""

    def __init__(self, size, reported_nbytes=None):
        self.block = (ctypes.c_ubyte * size)()
        self.pointer = ctypes.addressof(self.block)
        self.nbytes = size if reported_nbytes is None else reported_nbytes
        self.__cuda_array_interface__ = {
            "shape": (size,),
            "typestr": "|u1",
            "data": (self.pointer, False),
            "version": 3,
        }


class _RecordingAllocator:
    """Records every allocation so tests can assert owner identity and cleanup."""

    def __init__(self, owner_factory=_HostOwner):
        self.owner_factory = owner_factory
        self.live_owners = {}
        self.allocated_pointers = []
        self.freed_pointers = []
        self.free_keepalive_seen = []
        self.lock = threading.Lock()
        self.factory = pylon.PythonBufferFactory(self.allocate, self.free)

    def allocate(self, size):
        owner = self.owner_factory(size)
        with self.lock:
            self.live_owners[owner.pointer] = owner
            self.allocated_pointers.append(owner.pointer)
        return owner.pointer, owner, owner.pointer, size

    def free(self, pointer, context, keep_alive):
        with self.lock:
            self.freed_pointers.append(pointer)
            self.free_keepalive_seen.append(keep_alive is not None)
            self.live_owners.pop(pointer, None)

    def assert_all_freed_once(self, test_case):
        with self.lock:
            test_case.assertEqual(sorted(self.allocated_pointers), sorted(self.freed_pointers))
            test_case.assertEqual(len(set(self.freed_pointers)), len(self.freed_pointers))
            test_case.assertEqual({}, self.live_owners)
            test_case.assertTrue(all(self.free_keepalive_seen))


class PythonBufferFactoryTestSuite(PylonEmuTestCase):

    def setUp(self):
        super().setUp()
        self.host_blocks = {}

    def allocate_host_pointer(self, size):
        """Allocate host memory owned by this test and return its address."""
        block = (ctypes.c_ubyte * size)()
        pointer = ctypes.addressof(block)
        self.host_blocks[pointer] = block
        return pointer

    def open_camera_with_allocator(self, allocator, configure=None):
        """Open an emulated camera that grabs into buffers from the allocator."""
        camera = self.create_first()
        camera.Open()
        camera.SetBufferFactory(allocator.factory, pylon.Cleanup_None)
        if configure is not None:
            configure(camera)
        return camera

    def enable_gen_dc(self, camera):
        """Switch the emulated camera to GenDC payloads, or skip if unsupported."""
        try:
            camera.GenDC.Value = True
        except genicam.GenericException as exc:
            self.skipTest("GenDC is not supported on this emulator: %s" % exc)

    # ------------------------------------------------------------------
    # Construction / callback validation
    # ------------------------------------------------------------------

    def test_construction_with_allocate_callback_only(self):
        """A factory can be constructed from an allocate callback alone."""
        factory = pylon.PythonBufferFactory(self.allocate_host_pointer)
        pointer, context = factory.DebugAllocateBuffer(64)
        self.assertIn(pointer, self.host_blocks)
        self.assertEqual(0, context)

    def test_construction_rejects_a_non_callable_allocate_callback(self):
        """PythonBufferFactory requires a callable allocate callback."""
        with self.assertRaises(genicam.InvalidArgumentException):
            pylon.PythonBufferFactory("not callable")

    def test_construction_rejects_non_callable_free_and_destroy_callbacks(self):
        """The optional free and destroy callbacks must be callable or None."""
        with self.assertRaises(genicam.InvalidArgumentException):
            pylon.PythonBufferFactory(self.allocate_host_pointer, "not callable")
        with self.assertRaises(genicam.InvalidArgumentException):
            pylon.PythonBufferFactory(self.allocate_host_pointer, None, "not callable")

    # ------------------------------------------------------------------
    # Allocation callback return values
    # ------------------------------------------------------------------

    def test_allocate_callback_may_return_a_bare_pointer(self):
        """An allocate callback may return only the buffer address."""
        factory = pylon.PythonBufferFactory(self.allocate_host_pointer)
        pointer, context = factory.DebugAllocateBuffer(128)
        self.assertIn(pointer, self.host_blocks)
        self.assertEqual(0, context)
        self.assertIsNone(factory.LookupKeepAlive(pointer))

    def test_allocate_callback_may_return_pointer_keepalive_context_and_capacity(self):
        """The four-element allocate result sets the owner, the context, and the capacity."""
        def allocate(size):
            owner = _HostOwner(size)
            return owner.pointer, owner, 4711, owner.nbytes

        factory = pylon.PythonBufferFactory(allocate)
        pointer, context = factory.DebugAllocateBuffer(256)
        self.assertEqual(4711, context)
        owner = factory.LookupKeepAlive(pointer)
        self.assertIsInstance(owner, _HostOwner)
        self.assertEqual(pointer, owner.pointer)

    def test_allocate_callback_rejects_unsupported_return_values(self):
        """Allocate results that are neither an address nor a 1-to-4 element tuple are rejected."""
        for unsupported in (None, "pointer", (), (0, None, 0, 0, 0)):
            with self.subTest(returned=unsupported):
                factory = pylon.PythonBufferFactory(lambda size: unsupported)
                with self.assertRaises(genicam.InvalidArgumentException):
                    factory.DebugAllocateBuffer(64)

    def test_allocate_callback_rejects_a_null_pointer(self):
        """An allocate callback that returns a null address is rejected."""
        factory = pylon.PythonBufferFactory(lambda size: 0)
        with self.assertRaises(genicam.RuntimeException):
            factory.DebugAllocateBuffer(64)

    def test_allocate_callback_rejects_capacity_below_requested_size(self):
        """A reported capacity smaller than the requested size is rejected."""
        def allocate(size):
            owner = _HostOwner(size)
            return owner.pointer, owner, 0, size - 1

        factory = pylon.PythonBufferFactory(allocate)
        with self.assertRaises(genicam.InvalidArgumentException):
            factory.DebugAllocateBuffer(1024)

    def test_allocate_callback_exception_is_reported_as_runtime_exception(self):
        """An exception inside the allocate callback surfaces as a RuntimeException."""
        def allocate(size):
            raise ValueError("allocation refused")

        factory = pylon.PythonBufferFactory(allocate)
        with self.assertRaises(genicam.RuntimeException):
            factory.DebugAllocateBuffer(64)

    # ------------------------------------------------------------------
    # Keepalive bookkeeping
    # ------------------------------------------------------------------

    def test_keepalive_holds_the_owner_until_the_buffer_is_freed(self):
        """The factory owns a reference to the allocator object until FreeBuffer runs."""
        owner_refs = []

        def allocate(size):
            owner = _HostOwner(size)
            owner_refs.append(weakref.ref(owner))
            return owner.pointer, owner, owner.pointer, size

        factory = pylon.PythonBufferFactory(allocate)
        pointer, context = factory.DebugAllocateBuffer(64)

        gc.collect()
        self.assertIsNotNone(owner_refs[0]())
        self.assertIsNotNone(factory.LookupKeepAlive(pointer))

        factory.DebugFreeBuffer(pointer, context)
        self.assertIsNone(factory.LookupKeepAlive(pointer))

        gc.collect()
        self.assertIsNone(owner_refs[0]())

    def test_reallocating_the_same_address_replaces_the_keepalive(self):
        """Allocating the same address twice releases the previous owner."""
        class _SharedBlockOwner:
            def __init__(self, block):
                self.block = block

        block = (ctypes.c_ubyte * 64)()
        address = ctypes.addressof(block)
        owners = []

        def allocate(size):
            owner = _SharedBlockOwner(block)
            owners.append(owner)
            return address, owner, 0, len(block)

        factory = pylon.PythonBufferFactory(allocate)
        factory.DebugAllocateBuffer(64)
        first_owner_ref = weakref.ref(owners[0])
        factory.DebugAllocateBuffer(64)

        self.assertIs(owners[1], factory.LookupKeepAlive(address))

        owners.pop(0)
        gc.collect()
        self.assertIsNone(first_owner_ref())

    def test_lookup_keepalive_returns_none_for_an_unknown_address(self):
        """LookupKeepAlive reports None for addresses the factory did not allocate."""
        allocator = _RecordingAllocator()
        self.assertIsNone(allocator.factory.LookupKeepAlive(0xDEADBEEF))

    # ------------------------------------------------------------------
    # Free and destroy callbacks
    # ------------------------------------------------------------------

    def test_free_callback_receives_pointer_context_and_owner(self):
        """FreeBuffer passes the address, the allocation context, and the owner object."""
        calls = []

        def allocate(size):
            owner = _HostOwner(size)
            return owner.pointer, owner, 99, size

        def free(pointer, context, keep_alive):
            calls.append((pointer, context, keep_alive))

        factory = pylon.PythonBufferFactory(allocate, free)
        pointer, context = factory.DebugAllocateBuffer(64)
        factory.DebugFreeBuffer(pointer, context)

        self.assertEqual(1, len(calls))
        self.assertEqual(pointer, calls[0][0])
        self.assertEqual(99, calls[0][1])
        self.assertIsInstance(calls[0][2], _HostOwner)

    def test_free_callback_exception_does_not_propagate_and_still_releases(self):
        """A failing free callback is reported but never breaks the pylon buffer release."""
        def allocate(size):
            owner = _HostOwner(size)
            return owner.pointer, owner, 0, size

        def free(pointer, context, keep_alive):
            raise ValueError("release refused")

        factory = pylon.PythonBufferFactory(allocate, free)
        pointer, context = factory.DebugAllocateBuffer(64)

        factory.DebugFreeBuffer(pointer, context)
        self.assertIsNone(factory.LookupKeepAlive(pointer))

    def test_freeing_an_unknown_address_reports_no_owner(self):
        """Releasing an address the factory never allocated passes None as the owner."""
        seen_owners = []

        def free(pointer, context, keep_alive):
            seen_owners.append(keep_alive)

        factory = pylon.PythonBufferFactory(self.allocate_host_pointer, free)
        factory.DebugFreeBuffer(0xDEADBEEF, 0)

        self.assertEqual([None], seen_owners)

    def test_destroy_callback_exception_does_not_propagate(self):
        """A failing destroy callback is reported but DestroyBufferFactory still completes."""
        def destroy():
            raise ValueError("teardown refused")

        factory = pylon.PythonBufferFactory(self.allocate_host_pointer, None, destroy)
        factory.thisown = False
        factory.DestroyBufferFactory()

    # ------------------------------------------------------------------
    # Owner lookup across factories
    # ------------------------------------------------------------------

    def test_owner_lookup_finds_the_allocating_factory(self):
        """_LookupBufferOwner resolves an address through any live factory."""
        allocator = _RecordingAllocator()
        pointer, context = allocator.factory.DebugAllocateBuffer(64)

        self.assertIs(allocator.live_owners[pointer], pylon._LookupBufferOwner(pointer))

        allocator.factory.DebugFreeBuffer(pointer, context)
        self.assertIsNone(pylon._LookupBufferOwner(pointer))

    def test_owner_lookup_returns_none_for_an_unknown_address(self):
        """_LookupBufferOwner reports None when no factory owns the address."""
        self.assertIsNone(pylon._LookupBufferOwner(0xDEADBEEF))

    def test_owner_lookup_rejects_an_address_claimed_by_two_factories(self):
        """An address registered by two factories is ambiguous and raises."""
        shared = _HostOwner(64)

        def allocate(size):
            return shared.pointer, shared, 0, shared.nbytes

        first = pylon.PythonBufferFactory(allocate)
        second = pylon.PythonBufferFactory(allocate)
        pointer, context = first.DebugAllocateBuffer(64)
        second.DebugAllocateBuffer(64)

        with self.assertRaises(RuntimeError):
            pylon._LookupBufferOwner(pointer)

        second.DebugFreeBuffer(pointer, context)
        self.assertIs(shared, pylon._LookupBufferOwner(pointer))

    def test_cameras_resolve_owners_from_their_own_factory(self):
        """Two cameras with separate factories keep their allocations apart."""
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices(self.device_filter)
        if len(devices) < 2:
            self.skipTest("Two emulated cameras are required for this test")

        first_allocator = _RecordingAllocator()
        second_allocator = _RecordingAllocator()
        first_camera = pylon.InstantCamera(tl_factory.CreateDevice(devices[0]))
        second_camera = pylon.InstantCamera(tl_factory.CreateDevice(devices[1]))
        first_camera.Open()
        second_camera.Open()
        first_camera.SetBufferFactory(first_allocator.factory, pylon.Cleanup_None)
        second_camera.SetBufferFactory(second_allocator.factory, pylon.Cleanup_None)

        try:
            with first_camera.GrabOne(5000) as first_result:
                with second_camera.GrabOne(5000) as second_result:
                    self.assertIs(
                        first_allocator.live_owners[first_result.BufferAddress],
                        first_result.GetBufferOwner(),
                    )
                    self.assertIs(
                        second_allocator.live_owners[second_result.BufferAddress],
                        second_result.GetBufferOwner(),
                    )
                    self.assertIsNone(
                        first_allocator.factory.LookupKeepAlive(second_result.BufferAddress)
                    )
        finally:
            first_camera.SetBufferFactory(None)
            second_camera.SetBufferFactory(None)
            first_camera.Close()
            second_camera.Close()

        first_allocator.assert_all_freed_once(self)
        second_allocator.assert_all_freed_once(self)

    # ------------------------------------------------------------------
    # Grab-result owner views (classic image payload)
    # ------------------------------------------------------------------

    def test_owner_view_shapes_the_host_owner_as_an_image(self):
        """GetBufferOwnerView presents a host allocator object with the image shape."""
        allocator = _RecordingAllocator()
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                owner = grab_result.GetBufferOwner()
                self.assertIs(allocator.live_owners[grab_result.BufferAddress], owner)

                owner_view = grab_result.GetBufferOwnerView()
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), owner_view.shape)
                self.assertIs(owner, owner_view._owner)
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_view_reshapes_the_cuda_array_interface(self):
        """A CUDA-aware owner is exposed through a reshaped __cuda_array_interface__."""
        allocator = _RecordingAllocator(_CudaLikeOwner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                owner_view = grab_result.GetBufferOwnerView()
                interface = owner_view.__cuda_array_interface__
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), interface["shape"])
                self.assertEqual(numpy.dtype(numpy.uint8).str, interface["typestr"])
                self.assertEqual(grab_result.BufferAddress, interface["data"][0])
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_zero_copy_view_of_a_cuda_owner_keeps_the_image_shape(self):
        """GetArray(copy=False) returns a CUDA-aware proxy instead of a NumPy copy."""
        allocator = _RecordingAllocator(_CudaLikeOwner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                view = grab_result.GetArray(copy=False)
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), view.shape)
                self.assertEqual(
                    (EMULATED_HEIGHT, EMULATED_WIDTH),
                    view.__cuda_array_interface__["shape"],
                )
                del view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_view_converts_to_a_numpy_array_with_the_image_shape(self):
        """numpy.asarray on an owner view yields the image, not the whole allocation."""
        allocator = _RecordingAllocator(_NumpyOwner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                owner_view = grab_result.GetBufferOwnerView()
                converted = numpy.asarray(owner_view)
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), converted.shape)
                self.assertEqual(numpy.uint8, converted.dtype)
                del converted
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_view_replaces_the_strides_of_the_whole_allocation(self):
        """An owner that reports its own strides is still reshaped into the image."""
        allocator = _RecordingAllocator(_StridedHostOwner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                owner_view = grab_result.GetBufferOwnerView()
                self.assertEqual(
                    (EMULATED_HEIGHT, EMULATED_WIDTH),
                    owner_view.__array_interface__["shape"],
                )

                converted = numpy.asarray(owner_view)
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), converted.shape)
                del converted
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_view_of_a_multi_byte_format_converts_to_numpy(self):
        """A 16-bit owner view converts to NumPy with the image shape and dtype."""
        allocator = _RecordingAllocator(_StridedHostOwner)
        camera = self.open_camera_with_allocator(allocator)
        if not camera.PixelFormat.CanSetValue("Mono16"):
            camera.SetBufferFactory(None)
            camera.Close()
            self.skipTest("The emulated camera does not support Mono16")

        camera.PixelFormat.Value = "Mono16"
        try:
            with camera.GrabOne(5000) as grab_result:
                owner_view = grab_result.GetBufferOwnerView()
                converted = numpy.asarray(owner_view)
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), converted.shape)
                self.assertEqual(numpy.uint16, converted.dtype)
                del converted
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_raw_owner_view_spans_the_whole_payload(self):
        """GetBufferOwnerView(raw=True) exposes the full allocation as a flat view."""
        allocator = _RecordingAllocator(_CudaLikeOwner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                raw_view = grab_result.GetBufferOwnerView(raw=True)
                self.assertEqual((grab_result.PayloadSize,), raw_view.shape)
                del raw_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_view_rejects_an_owner_smaller_than_the_image(self):
        """An owner that reports less memory than the grab result needs is refused."""
        def undersized_owner(size):
            return _CudaLikeOwner(size, reported_nbytes=16)

        allocator = _RecordingAllocator(undersized_owner)
        camera = self.open_camera_with_allocator(allocator)
        try:
            with camera.GrabOne(5000) as grab_result:
                with self.assertRaises(RuntimeError):
                    grab_result.GetBufferOwnerView()
                with self.assertRaises(RuntimeError):
                    grab_result.GetArray(copy=False)

                # The grab buffer itself is intact, so the scoped view still works.
                with grab_result.GetArrayZeroCopy() as image:
                    self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), image.shape)
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_owner_views_follow_a_multi_byte_pixel_format(self):
        """A 16-bit pixel format is reflected in the owner view dtype and shape."""
        allocator = _RecordingAllocator(_CudaLikeOwner)
        camera = self.open_camera_with_allocator(allocator)
        if not camera.PixelFormat.CanSetValue("Mono16"):
            camera.SetBufferFactory(None)
            camera.Close()
            self.skipTest("The emulated camera does not support Mono16")

        camera.PixelFormat.Value = "Mono16"
        try:
            with camera.GrabOne(5000) as grab_result:
                owner_view = grab_result.GetBufferOwnerView()
                self.assertEqual((EMULATED_HEIGHT, EMULATED_WIDTH), owner_view.shape)
                self.assertEqual(
                    numpy.dtype(numpy.uint16).str,
                    owner_view.__cuda_array_interface__["typestr"],
                )
                del owner_view

                with grab_result.GetArrayZeroCopy() as image:
                    self.assertEqual(numpy.uint16, image.dtype)
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_grab_result_without_a_factory_reports_no_owner(self):
        """A grab result from the default allocator has no Python owner."""
        camera = self.create_first()
        camera.Open()
        try:
            with camera.GrabOne(5000) as grab_result:
                self.assertIsNone(grab_result.GetBufferOwner())
                self.assertIsNone(grab_result.GetBufferOwnerView())
        finally:
            camera.Close()

    def test_release_drops_the_cached_owner(self):
        """Releasing a grab result forgets the owner it resolved."""
        allocator = _RecordingAllocator()
        camera = self.open_camera_with_allocator(allocator)
        try:
            grab_result = camera.GrabOne(5000)
            self.assertIsNotNone(grab_result.GetBufferOwner())
            self.assertIn("_buffer_owner", grab_result.__dict__)

            grab_result.Release()
            self.assertNotIn("_buffer_owner", grab_result.__dict__)
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    # ------------------------------------------------------------------
    # Grab-result owner views (GenDC payload)
    # ------------------------------------------------------------------

    def test_gen_dc_owner_is_the_whole_container(self):
        """For GenDC the factory allocates the container, so the owner spans the payload."""
        allocator = _RecordingAllocator()
        camera = self.open_camera_with_allocator(allocator, self.enable_gen_dc)
        try:
            with camera.GrabOne(5000) as grab_result:
                self.assertEqual(pylon.PayloadType_GenDC, grab_result.PayloadType)
                owner = grab_result.GetBufferOwner()
                self.assertIs(allocator.live_owners[grab_result.BufferAddress], owner)
                self.assertGreaterEqual(owner.nbytes, grab_result.PayloadSize)
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_gen_dc_views_address_the_image_component(self):
        """GenDC zero-copy views show the first image component, not the raw container."""
        allocator = _RecordingAllocator()
        camera = self.open_camera_with_allocator(allocator, self.enable_gen_dc)
        try:
            with camera.GrabOne(5000) as grab_result:
                with grab_result.GetFirstImageDataComponent() as component:
                    self.assertTrue(component.IsValid())
                    with component.GetArrayZeroCopy() as component_image:
                        component_shape = component_image.shape
                        component_first_pixel = component_image[0, 0]

                with grab_result.GetArrayZeroCopy() as image:
                    self.assertEqual(component_shape, image.shape)
                    self.assertEqual(component_first_pixel, image[0, 0])

                owner_view = grab_result.GetBufferOwnerView()
                self.assertEqual(component_shape, owner_view.shape)
                del owner_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)

    def test_gen_dc_raw_owner_view_exposes_the_container(self):
        """GetBufferOwnerView(raw=True) keeps the allocator-native GenDC container view."""
        allocator = _RecordingAllocator(_CudaLikeOwner)
        camera = self.open_camera_with_allocator(allocator, self.enable_gen_dc)
        try:
            with camera.GrabOne(5000) as grab_result:
                raw_view = grab_result.GetBufferOwnerView(raw=True)
                self.assertEqual((grab_result.PayloadSize,), raw_view.shape)
                self.assertEqual(
                    grab_result.BufferAddress,
                    raw_view.__cuda_array_interface__["data"][0],
                )
                del raw_view
        finally:
            camera.SetBufferFactory(None)
            camera.Close()

        allocator.assert_all_freed_once(self)


if __name__ == "__main__":
    unittest.main()
