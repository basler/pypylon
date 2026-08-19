"""\
This unit test checks the BufferFactory class and InstantCamera.SetBufferFactory
introduced by src/pylon/BufferFactory.i.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import ctypes
import unittest

class TrackingBufferFactory(pylon.BufferFactory):
    def __init__(self):
        super().__init__()
        # (buffer_address, context, ctypes_buffer) for every AllocateBuffer() call.
        # The ctypes buffer is kept alive here, exactly like pypylon keeps the
        # context object alive between AllocateBuffer() and FreeBuffer().
        self.allocations = []
        # (buffer_address, context) for every FreeBuffer() call.
        self.freed = []
        self.released = False

    def AllocateBuffer(self, buffer_size):
        raw_buffer = (ctypes.c_ubyte * buffer_size)()
        address = ctypes.addressof(raw_buffer)
        context = {"size": buffer_size}
        self.allocations.append((address, context, raw_buffer))
        return address, context

    def FreeBuffer(self, buffer, context):
        self.freed.append((buffer, context))

    def OnReleased(self):
        self.released = True


class NoContextBufferFactory(pylon.BufferFactory):
    """A BufferFactory whose AllocateBuffer() does not provide a context object."""

    def __init__(self):
        super().__init__()
        # Keeps the ctypes buffers alive for the lifetime of the factory.
        self._buffers = []

    def AllocateBuffer(self, buffer_size):
        raw_buffer = (ctypes.c_ubyte * buffer_size)()
        self._buffers.append(raw_buffer)
        return ctypes.addressof(raw_buffer)

    def FreeBuffer(self, buffer, context):
        pass


class BufferFactoryTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """Default construction produces a valid BufferFactory object."""
        factory = pylon.BufferFactory()
        self.assertIsNotNone(factory)

    # ------------------------------------------------------------------
    # AllocateBuffer / FreeBuffer
    # ------------------------------------------------------------------

    def test_allocate_buffer_called_while_grabbing(self):
        """AllocateBuffer is called with the payload size while grabbing with a custom factory."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            maximize_num_images = 3
            camera.StartGrabbingMax(maximize_num_images)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
            # StartGrabbingMax() sets MaxNumBuffer to the number of images to grab,
            # so the factory should have been called exactly that many times.
            self.assertEqual(len(factory.allocations), maximize_num_images)

    def test_free_buffer_receives_allocated_buffer_and_context(self):
        """FreeBuffer is eventually called for every (buffer, context) pair returned by AllocateBuffer."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            camera.StartGrabbingMax(3)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
        # Destroying the device (end of the with-block) frees all buffers.
        allocated_pairs = {(address, id(context)) for address, context, _ in factory.allocations}
        freed_pairs = {(address, id(context)) for address, context in factory.freed}
        self.assertEqual(allocated_pairs, freed_pairs)

    # ------------------------------------------------------------------
    # OnReleased
    # ------------------------------------------------------------------

    def test_on_released_called_when_factory_replaced(self):
        """OnReleased is called when the buffer factory is replaced by another one."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            camera.SetBufferFactory(None)
            self.assertTrue(factory.released)

    def test_on_released_called_when_camera_destroyed(self):
        """OnReleased is called when the owning instant camera is destroyed."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
        self.assertTrue(factory.released)

    def test_on_released_called_when_result_released(self):
        """OnReleased is called when the owning instant camera is destroyed."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            grab_result = camera.GrabOne(5000)
        # camera is destroyed, but the grab result still references the buffer, so
        # OnReleased() must not have fired for the factory yet.
        self.assertFalse(factory.released)
        grab_result.Release()
        self.assertTrue(factory.released)

    # ------------------------------------------------------------------
    # GrabResult.GetBufferContext / BufferContext
    # ------------------------------------------------------------------

    def test_get_buffer_context_returns_context_provided_by_factory(self):
        """GetBufferContext() returns the exact context object provided by AllocateBuffer()."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            # A single buffer is allocated and reused for every grab, so every
            # grab result's context is the very object created for that one
            # allocation.
            camera.MaxNumBuffer.Value = 1
            camera.StartGrabbingMax(2)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
                    self.assertEqual(len(factory.allocations), 1)
                    expected_context = factory.allocations[0][1]
                    # Method access
                    self.assertIs(grab_result.GetBufferContext(), expected_context)
                    # Property access (preferred style)
                    self.assertIs(grab_result.BufferContext, expected_context)

    def test_get_buffer_context_is_none_when_factory_provides_no_context(self):
        """GetBufferContext() returns None when AllocateBuffer() does not provide a context object."""
        factory = NoContextBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            camera.StartGrabbingMax(2)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
                    self.assertIsNone(grab_result.GetBufferContext())
                    self.assertIsNone(grab_result.BufferContext)

    def test_get_buffer_context_is_none_without_custom_buffer_factory(self):
        """GetBufferContext() returns None when no custom BufferFactory was ever set on the camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(5000)
        self.assertIsNone(grab_result.GetBufferContext())
        grab_result.Release()

    # ------------------------------------------------------------------
    # GrabResult.GetBufferFactory / BufferFactory
    # ------------------------------------------------------------------

    def test_get_buffer_factory_returns_the_factory_used_to_allocate_the_buffer(self):
        """GetBufferFactory() returns the exact BufferFactory instance passed to SetBufferFactory()."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            camera.StartGrabbingMax(2)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
                    # Method access
                    self.assertIs(grab_result.GetBufferFactory(), factory)
                    # Property access (preferred style)
                    self.assertIs(grab_result.BufferFactory, factory)

    def test_get_buffer_factory_is_none_when_factory_provides_no_context(self):
        """GetBufferFactory() still returns the factory even if AllocateBuffer() provides no context."""
        factory = NoContextBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            camera.StartGrabbingMax(2)
            while camera.IsGrabbing():
                with camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) as grab_result:
                    self.assertTrue(grab_result.GrabSucceeded())
                    self.assertIs(grab_result.GetBufferFactory(), factory)
                    self.assertIs(grab_result.BufferFactory, factory)

    def test_get_buffer_factory_is_none_without_custom_buffer_factory(self):
        """GetBufferFactory() returns None when no custom BufferFactory was ever set on the camera."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            grab_result = camera.GrabOne(5000)
        # Method access
        self.assertIsNone(grab_result.GetBufferFactory())
        # Property access (preferred style)
        self.assertIsNone(grab_result.BufferFactory)
        grab_result.Release()

    def test_get_buffer_factory_survives_factory_replacement(self):
        """GetBufferFactory() still returns the original factory for grab results allocated before it was replaced,
        and OnReleased() is deferred until this grab result is released."""
        factory = TrackingBufferFactory()
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            camera.SetBufferFactory(factory)
            grab_result = camera.GrabOne(5000)
            camera.SetBufferFactory(None)
            # The outstanding grab result still references the buffer, so
            # OnReleased() must not have fired for the replaced factory yet.
            self.assertFalse(factory.released)
            self.assertIs(grab_result.GetBufferFactory(), factory)
        grab_result.Release()
        # Releasing the last outstanding buffer finally allows the replaced
        # factory to be released.
        self.assertTrue(factory.released)


if __name__ == "__main__":
    unittest.main()

