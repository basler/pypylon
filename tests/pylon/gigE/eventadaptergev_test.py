"""\
This unit test checks the mapped pypylon API introduced by
src/genicam/EventAdapterGEV.i.

A Basler GigE camera is required.
The DeliverMessage tests require only a node map attachment and verify
correct error handling for malformed event messages without needing live
camera events.
"""
from pylongigetestcase import PylonTestCase
from pypylon import pylon, genicam
import unittest


class EventAdapterGEVTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """EventAdapterGEV() constructs without error."""
        adapter = genicam.EventAdapterGEV()
        self.assertIsNotNone(adapter)

    # ------------------------------------------------------------------
    # AttachNodeMap / DetachNodeMap
    # ------------------------------------------------------------------

    def test_attach_and_detach_node_map(self):
        """AttachNodeMap and DetachNodeMap succeed without error."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterGEV()
            adapter.AttachNodeMap(camera.GetNodeMap())
            adapter.DetachNodeMap()

    # ------------------------------------------------------------------
    # DeliverMessage
    # ------------------------------------------------------------------

    def test_deliver_message_with_wrong_magic_raises(self):
        """DeliverMessage raises RuntimeException for a message with a wrong magic value."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterGEV()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with self.assertRaises(genicam.RuntimeException) as context:
                adapter.DeliverMessage(b"\x00" * 16)
            self.assertIn("magic", str(context.exception).lower())
            adapter.DetachNodeMap()

    def test_deliver_message_too_short_raises(self):
        """DeliverMessage raises RuntimeException for a message that is too short."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterGEV()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with self.assertRaises(genicam.RuntimeException):
                adapter.DeliverMessage(b"\x00" * 4)
            adapter.DetachNodeMap()


if __name__ == "__main__":
    unittest.main()
