"""\
This unit test checks the mapped pypylon API introduced by
src/genicam/EventAdapterU3V.i.

A Basler USB3 Vision camera is required.
The DeliverMessage tests require only a node map attachment and verify
correct error handling for malformed event messages without needing live
camera events.
"""
from pylonusbtestcase import PylonTestCase
from pypylon import pylon, genicam
import unittest


class EventAdapterU3VTestSuite(PylonTestCase):

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_construction(self):
        """EventAdapterU3V() constructs without error."""
        adapter = genicam.EventAdapterU3V()
        self.assertIsNotNone(adapter)

    # ------------------------------------------------------------------
    # AttachNodeMap / DetachNodeMap
    # ------------------------------------------------------------------

    def test_attach_and_detach_node_map(self):
        """AttachNodeMap and DetachNodeMap succeed without error."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            adapter.DetachNodeMap()

    # ------------------------------------------------------------------
    # DeliverMessage
    # ------------------------------------------------------------------

    def test_deliver_message_too_small_raises(self):
        """DeliverMessage raises RuntimeException for a message that is too small."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with self.assertRaises(genicam.RuntimeException) as context:
                adapter.DeliverMessage(b"\x00" * 16)
            self.assertIn("too small", str(context.exception).lower())
            adapter.DetachNodeMap()

    def test_deliver_empty_message_raises(self):
        """DeliverMessage raises RuntimeException for a completely empty message."""
        with pylon.InstantCamera(self.get_camera_traits(), pylon.FirstFound) as camera:
            adapter = genicam.EventAdapterU3V()
            adapter.AttachNodeMap(camera.GetNodeMap())
            with self.assertRaises(genicam.RuntimeException):
                adapter.DeliverMessage(b"")
            adapter.DetachNodeMap()


if __name__ == "__main__":
    unittest.main()
