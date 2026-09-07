"""\
This unit test checks the mapped pypylon API introduced by
src/genicam/ChunkAdapterU3V.i.

A Basler USB3 Vision camera that supports Chunk mode is required.
Tests skip gracefully if the attached camera does not support chunk mode.
"""
from pylonusbtestcase import PylonTestCase
from pypylon import pylon, genicam
import unittest


class ChunkAdapterU3VTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    def _open_with_chunk(self, camera):
        """Enable chunk mode with Timestamp chunk. Skip if unsupported."""
        if not camera.ChunkModeActive.IsWritable():
            self.skipTest("Camera does not support chunk mode.")
        camera.ChunkModeActive.Value = True
        if not camera.ChunkSelector.TrySetValue("Timestamp"):
            camera.ChunkModeActive.Value = False
            self.skipTest("Camera does not support Timestamp chunk.")
        camera.ChunkEnable.Value = True

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction_no_args(self):
        """ChunkAdapterU3V() constructs without error."""
        adapter = genicam.ChunkAdapterU3V()
        self.assertIsNotNone(adapter)

    def test_construction_with_node_map(self):
        """ChunkAdapterU3V(nodeMap) constructs and attaches the node map in one step."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.ChunkAdapterU3V(camera.GetNodeMap())
            self.assertIsNotNone(adapter)
            # Detach before the camera (and its node map) is destroyed.
            adapter.DetachNodeMap()

    # ------------------------------------------------------------------
    # AttachNodeMap / DetachNodeMap
    # ------------------------------------------------------------------

    def test_attach_and_detach_node_map(self):
        """AttachNodeMap and DetachNodeMap succeed without error."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            adapter.DetachNodeMap()

    # ------------------------------------------------------------------
    # ClearCaches
    # ------------------------------------------------------------------

    def test_clear_caches_without_buffer(self):
        """ClearCaches succeeds even when no buffer is attached."""
        adapter = genicam.ChunkAdapterU3V()
        adapter.ClearCaches()

    def test_clear_caches_with_node_map(self):
        """ClearCaches succeeds when a node map is attached but no buffer."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            adapter.ClearCaches()
            adapter.DetachNodeMap()

    # ------------------------------------------------------------------
    # CheckBufferLayout
    # ------------------------------------------------------------------

    def test_check_buffer_layout_returns_true_for_valid_chunk_buffer(self):
        """CheckBufferLayout returns True for a buffer grabbed with chunk mode enabled."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self._open_with_chunk(camera)
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with camera.GrabOne(5000) as result:
                self.assertTrue(adapter.CheckBufferLayout(bytes(result.GetBuffer())))
            adapter.DetachNodeMap()
            camera.ChunkModeActive.Value = False

    # ------------------------------------------------------------------
    # AttachBuffer / DetachBuffer
    # ------------------------------------------------------------------

    def test_attach_buffer_makes_chunk_nodes_readable(self):
        """After AttachBuffer, chunk parameter nodes become readable."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self._open_with_chunk(camera)
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with camera.GrabOne(5000) as result:
                self.assertFalse(camera.ChunkTimestamp.IsReadable())
                adapter.AttachBuffer(bytes(result.GetBuffer()))
                self.assertTrue(camera.ChunkTimestamp.IsReadable())
                adapter.DetachBuffer()
            adapter.DetachNodeMap()
            camera.ChunkModeActive.Value = False

    def test_detach_buffer_makes_chunk_nodes_unreadable(self):
        """After DetachBuffer, chunk parameter nodes become unreadable again."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self._open_with_chunk(camera)
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with camera.GrabOne(5000) as result:
                adapter.AttachBuffer(bytes(result.GetBuffer()))
                self.assertTrue(camera.ChunkTimestamp.IsReadable())
                adapter.DetachBuffer()
                self.assertFalse(camera.ChunkTimestamp.IsReadable())
            adapter.DetachNodeMap()
            camera.ChunkModeActive.Value = False

    def test_attach_buffer_chunk_timestamp_value_is_positive(self):
        """After AttachBuffer, ChunkTimestamp reports a positive integer value."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            self._open_with_chunk(camera)
            adapter = genicam.ChunkAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with camera.GrabOne(5000) as result:
                adapter.AttachBuffer(bytes(result.GetBuffer()))
                self.assertGreater(camera.ChunkTimestamp.Value, 0)
                adapter.DetachBuffer()
            adapter.DetachNodeMap()
            camera.ChunkModeActive.Value = False


if __name__ == "__main__":
    unittest.main()
