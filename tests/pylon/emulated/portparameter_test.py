"""\
This unit test checks all of the mapped pypylon API introduced by src/pylon/PortParameter.i.

Note: IPort is derived from IBase, not IValue.
"""
from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

# Port nodes defined in the test nodemap
PORT_DEVICE = "Device"
PORT_TEST = "TestPort"
PORT_CHUNK_TEST = "TestChunkPort"


# ---------------------------------------------------------------------------
# A minimal in-process port backed by a plain bytearray, used to exercise
# Read() and Write() on an attached PortParameter.
# ---------------------------------------------------------------------------
class _ByteArrayPort(genicam.CPortImpl):
    def __init__(self, size=256):
        genicam.CPortImpl.__init__(self)
        self._mem = bytearray(size)

    def Read(self, address, length):
        return bytes(self._mem[address:address + length])

    def Write(self, address, data):
        n = len(data)
        self._mem[address:address + n] = data

    def GetAccessMode(self):
        return genicam.RW


class PortParameterTestSuite(PylonParameterTestCase):

    def setUp(self):
        super().setUp()
        # Connect a software port implementation to TestPort so that
        # Read() and Write() become exercisable.
        self._port = _ByteArrayPort()
        self.nodemapref._Connect(self._port, PORT_TEST)

    # Helper: obtain IPort via nodemap auto-downcast
    def _get_iport(self, name):
        return self.nodemap.GetNode(name)

    # ------------------------------------------------------------------
    # Construction / Attach / Release
    # ------------------------------------------------------------------

    def test_port_parameter_construction_default(self):
        """Default construction produces an invalid parameter."""
        p = pylon.PortParameter()
        self.assertFalse(p.IsValid())

    def test_port_parameter_construction_from_inode_matching(self):
        """Construction from a matching INode (port) attaches and validates."""
        node = self.getINode(PORT_TEST)
        p = pylon.PortParameter(node)
        self.assertTrue(p.IsValid())

    def test_port_parameter_construction_from_inode_wrong_type(self):
        """Construction from a non-port INode yields an invalid parameter."""
        node_int = self.getINode("TestInt")
        p = pylon.PortParameter(node_int)
        self.assertFalse(p.IsValid())

    def test_port_parameter_construction_from_iport(self):
        """Construction from a GenApi IPort object attaches and validates."""
        iport = self._get_iport(PORT_TEST)
        self.assertIsInstance(iport, genicam.IPort)
        p = pylon.PortParameter(iport)
        self.assertTrue(p.IsValid())

    def test_port_parameter_construction_from_nodemap_name(self):
        """Construction from nodemap + name attaches and validates."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode(PORT_TEST)))
        self.assertFalse(p.Equals(self.getINode(PORT_DEVICE)))

    def test_port_parameter_construction_from_nonexistent_name(self):
        """Construction from nodemap + non-existent name produces an invalid parameter."""
        p = pylon.PortParameter(self.nodemap, "PortDoesNotExist")
        self.assertFalse(p.IsValid())

    def test_port_parameter_construction_copy(self):
        """Copy construction produces a valid, equal parameter."""
        p1 = pylon.PortParameter(self.nodemap, PORT_TEST)
        p2 = pylon.PortParameter(p1)
        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_port_parameter_attach_from_inode(self):
        """Attach from INode sets validity and the correct node."""
        node_test = self.getINode(PORT_TEST)
        node_device = self.getINode(PORT_DEVICE)

        p = pylon.PortParameter()
        self.assertFalse(p.IsValid())

        result = p.Attach(node_test)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_test))
        self.assertFalse(p.Equals(node_device))

        result = p.Attach(node_device)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_device))
        self.assertFalse(p.Equals(node_test))

    def test_port_parameter_attach_from_iport(self):
        """Attach from GenApi IPort attaches correctly."""
        iport = self._get_iport(PORT_TEST)
        p = pylon.PortParameter()
        result = p.Attach(iport)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

    def test_port_parameter_attach_from_nodemap_name(self):
        """Attach from nodemap + name; non-existent name returns False."""
        p = pylon.PortParameter()

        result = p.Attach(self.nodemap, PORT_TEST)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, PORT_DEVICE)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        result = p.Attach(self.nodemap, "PortDoesNotExist")
        self.assertFalse(result)

    def test_port_parameter_release(self):
        """Release makes parameter invalid."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    # ------------------------------------------------------------------
    # Equals
    # ------------------------------------------------------------------

    def test_port_parameter_equals_parameter(self):
        """Equals between two PortParameters."""
        node_test = self.nodemap.GetNode(PORT_TEST)
        node_device = self.nodemap.GetNode(PORT_DEVICE)

        p1 = pylon.PortParameter(node_test)
        p2 = pylon.PortParameter(node_test)
        p3 = pylon.PortParameter(node_device)
        p_empty1 = pylon.PortParameter()
        p_empty2 = pylon.PortParameter()

        self.assertTrue(p_empty1.Equals(p_empty2))
        self.assertTrue(p1.Equals(p2))
        self.assertTrue(p2.Equals(p1))
        self.assertFalse(p1.Equals(p3))
        self.assertFalse(p3.Equals(p1))
        self.assertFalse(p1.Equals(p_empty1))
        self.assertFalse(p_empty1.Equals(p1))

    def test_port_parameter_equals_inode(self):
        """Equals against INode and None."""
        node_test = self.getINode(PORT_TEST)
        node_device = self.getINode(PORT_DEVICE)

        p_empty = pylon.PortParameter()
        p = pylon.PortParameter(node_test)

        self.assertTrue(p_empty.Equals(None))
        self.assertFalse(p_empty.Equals(node_test))
        self.assertTrue(p.Equals(node_test))
        self.assertFalse(p.Equals(node_device))
        self.assertFalse(p.Equals(None))

    def test_port_parameter_equals_iport(self):
        """Equals against a GenApi IPort object."""
        iport_test = self._get_iport(PORT_TEST)
        iport_device = self._get_iport(PORT_DEVICE)

        p_empty = pylon.PortParameter()
        p = pylon.PortParameter(iport_test)

        self.assertTrue(p.Equals(iport_test))
        self.assertFalse(p.Equals(iport_device))
        self.assertFalse(p_empty.Equals(iport_test))

    # ------------------------------------------------------------------
    # IsValid / IsReadable / IsWritable / GetAccessMode
    # ------------------------------------------------------------------

    def test_port_parameter_is_valid(self):
        """IsValid reflects attachment state."""
        p = pylon.PortParameter()
        self.assertFalse(p.IsValid())
        p.Attach(self.nodemap, PORT_TEST)
        self.assertTrue(p.IsValid())
        p.Release()
        self.assertFalse(p.IsValid())

    def test_port_parameter_is_readable_writable_unattached(self):
        """An unattached parameter reports not readable and not writable."""
        p = pylon.PortParameter()
        self.assertFalse(p.IsReadable())
        self.assertFalse(p.IsWritable())

    def test_port_parameter_get_access_mode_unattached(self):
        """GetAccessMode returns genicam.NI when unattached."""
        self.assertEqual(genicam.NI, pylon.PortParameter().GetAccessMode())

    def test_port_parameter_get_access_mode_attached(self):
        """GetAccessMode returns RW when a port implementation is connected."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertTrue(p.IsValid())
        self.assertEqual(genicam.RW, p.GetAccessMode())

    # ------------------------------------------------------------------
    # Read / Write
    # ------------------------------------------------------------------

    def test_port_parameter_read_returns_bytes(self):
        """Read returns a bytes object of the requested length."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        result = p.Read(0, 4)
        self.assertIsInstance(result, bytes)
        self.assertEqual(4, len(result))

    def test_port_parameter_write_read_roundtrip(self):
        """Data written via Write is returned unchanged by Read."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
        p.Write(0, data)
        result = p.Read(0, len(data))
        self.assertEqual(data, result)

    def test_port_parameter_write_read_multiple_addresses(self):
        """Write and Read work correctly at different offsets."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)

        p.Write(0, bytes([0x11, 0x22]))
        p.Write(16, bytes([0xAA, 0xBB, 0xCC]))

        self.assertEqual(bytes([0x11, 0x22]), p.Read(0, 2))
        self.assertEqual(bytes([0xAA, 0xBB, 0xCC]), p.Read(16, 3))

    def test_port_parameter_write_visible_in_port_memory(self):
        """Data written via Write is visible directly in the backing port memory."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        data = bytes([0x01, 0x02, 0x03, 0x04])
        p.Write(0, data)
        self.assertEqual(data, bytes(self._port._mem[0:4]))

    def test_port_parameter_read_reflects_port_memory(self):
        """Data written directly into port memory is returned by Read."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        expected = bytes([0xCA, 0xFE, 0xBA, 0xBE])
        self._port._mem[0:4] = expected
        self.assertEqual(expected, p.Read(0, 4))

    def test_port_parameter_unattached_read_raises(self):
        """Read on an unattached parameter raises."""
        p = pylon.PortParameter()
        with self.assertRaises(Exception):
            p.Read(0, 4)

    def test_port_parameter_unattached_write_raises(self):
        """Write on an unattached parameter raises."""
        p = pylon.PortParameter()
        with self.assertRaises(Exception):
            p.Write(0, bytes([0x00, 0x00, 0x00, 0x00]))

    # ------------------------------------------------------------------
    # GetInfo / GetInfoOrDefault
    # ------------------------------------------------------------------

    def test_port_parameter_get_info_name(self):
        """GetInfo with ParameterInfo_Name returns the node name."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual(PORT_TEST, p.GetInfo(pylon.ParameterInfo_Name))

    def test_port_parameter_get_info_display_name(self):
        """GetInfo with ParameterInfo_DisplayName returns the display name."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual("TestPort Display Name", p.GetInfo(pylon.ParameterInfo_DisplayName))

    def test_port_parameter_get_info_tool_tip(self):
        """GetInfo with ParameterInfo_ToolTip returns the tooltip."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual("TestPort ToolTip", p.GetInfo(pylon.ParameterInfo_ToolTip))

    def test_port_parameter_get_info_description(self):
        """GetInfo with ParameterInfo_Description returns the description."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual("TestPort Description", p.GetInfo(pylon.ParameterInfo_Description))

    def test_port_parameter_get_info_unattached_raises(self):
        """GetInfo raises for all ParameterInfo values when unattached."""
        p = pylon.PortParameter()
        for info in (
            pylon.ParameterInfo_Name,
            pylon.ParameterInfo_DisplayName,
            pylon.ParameterInfo_ToolTip,
            pylon.ParameterInfo_Description,
        ):
            with self.assertRaises(Exception):
                p.GetInfo(info)

    def test_port_parameter_get_info_or_default_unattached(self):
        """GetInfoOrDefault returns the supplied default when unattached."""
        p = pylon.PortParameter()
        self.assertEqual("a", p.GetInfoOrDefault(pylon.ParameterInfo_Name, "a"))
        self.assertEqual("b", p.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "b"))
        self.assertEqual("c", p.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "c"))
        self.assertEqual("d", p.GetInfoOrDefault(pylon.ParameterInfo_Description, "d"))

    def test_port_parameter_get_info_or_default_attached(self):
        """GetInfoOrDefault returns the real value when attached."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual(PORT_TEST, p.GetInfoOrDefault(pylon.ParameterInfo_Name, "fallback"))

    # ------------------------------------------------------------------
    # GetChunkID / CacheChunkData
    # ------------------------------------------------------------------

    def test_port_parameter_get_chunk_id_chunk_port(self):
        """GetChunkID returns the chunk ID string for a chunk port node."""
        p = pylon.PortParameter(self.nodemap, PORT_CHUNK_TEST)
        self.assertEqual("42", p.GetChunkID())

    def test_port_parameter_chunk_id_property(self):
        """ChunkID property returns the same value as GetChunkID()."""
        p = pylon.PortParameter(self.nodemap, PORT_CHUNK_TEST)
        self.assertEqual(p.GetChunkID(), p.ChunkID)

    def test_port_parameter_cache_chunk_data_chunk_port(self):
        """CacheChunkData returns genicam.No for a static chunk ID port."""
        p = pylon.PortParameter(self.nodemap, PORT_CHUNK_TEST)
        self.assertEqual(genicam.No, p.CacheChunkData())

    def test_port_parameter_get_chunk_id_non_chunk_port(self):
        """GetChunkID returns an empty string for a plain port (no ChunkID defined)."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual("", p.GetChunkID())

    def test_port_parameter_cache_chunk_data_non_chunk_port(self):
        """CacheChunkData returns genicam.No for a plain port (no ChunkID defined)."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual(genicam.No, p.CacheChunkData())

    def test_port_parameter_get_chunk_id_unattached_raises(self):
        """GetChunkID raises when unattached."""
        p = pylon.PortParameter()
        with self.assertRaises(Exception):
            p.GetChunkID()

    def test_port_parameter_cache_chunk_data_unattached_raises(self):
        """CacheChunkData raises when unattached."""
        p = pylon.PortParameter()
        with self.assertRaises(Exception):
            p.CacheChunkData()

    # ------------------------------------------------------------------
    # GetSwapEndianess
    # ------------------------------------------------------------------

    def test_port_parameter_get_swap_endianess_plain_port(self):
        """GetSwapEndianess returns genicam.No for a plain port node."""
        p = pylon.PortParameter(self.nodemap, PORT_TEST)
        self.assertEqual(genicam.No, p.GetSwapEndianess())

    def test_port_parameter_get_swap_endianess_chunk_port(self):
        """GetSwapEndianess returns genicam.No for a chunk port node."""
        p = pylon.PortParameter(self.nodemap, PORT_CHUNK_TEST)
        self.assertEqual(genicam.No, p.GetSwapEndianess())

    def test_port_parameter_get_swap_endianess_unattached_raises(self):
        """GetSwapEndianess raises when unattached."""
        p = pylon.PortParameter()
        with self.assertRaises(Exception):
            p.GetSwapEndianess()

if __name__ == "__main__":
    unittest.main()
