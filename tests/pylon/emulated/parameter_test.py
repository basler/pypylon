from parametertestcase import PylonParameterTestCase
from pypylon import pylon, genicam
import unittest

class ParameterTestSuite(PylonParameterTestCase):
    """Test suite for Pylon::CParameter class functionality."""

    def test_parameter_construction_default(self):
        """Test CParameter default construction."""
        p = pylon.Parameter()
        self.assertFalse(p.IsValid())

    def test_parameter_construction_from_inode(self):
        """Test CParameter construction from GenApi::INode."""
        node_a = self.getINode("TestIntRO")
        # Construction from INode
        p = pylon.Parameter(node_a)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_a))

    def test_parameter_construction_from_ivalue(self):
        """Test CParameter construction from GenApi::IValue."""
        node_a = self.nodemap.GetNode("TestIntRO")

        # Construction from IValue (if available)
        p = pylon.Parameter(node_a)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_a))

    def test_parameter_construction_from_nodemap_name(self):
        """Test CParameter construction from nodemap and name."""
        # Construction from nodemap and name
        p = pylon.Parameter(self.nodemap, "TestIntRO")
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(self.getINode("TestIntRO")))
        self.assertFalse(p.Equals(self.getINode("TestIntWO")))

    def test_parameter_construction_copy(self):
        """Test CParameter copy construction."""
        node_a = self.nodemap.GetNode("TestIntRO")

        p1 = pylon.Parameter(node_a)
        p2 = pylon.Parameter(p1)

        self.assertTrue(p1.IsValid())
        self.assertTrue(p2.IsValid())
        self.assertTrue(p1.Equals(p2))

    def test_parameter_attach_from_inode(self):
        """Test CParameter Attach from GenApi::INode."""
        node_a = self.getINode("TestIntRO")
        node_b = self.getINode("TestIntWO")

        p = pylon.Parameter()
        self.assertFalse(p.IsValid())

        # Attach node
        result = p.Attach(node_a)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_a))
        self.assertFalse(p.Equals(node_b))

        # Attach different node
        result = p.Attach(node_b)
        self.assertTrue(result)
        self.assertTrue(p.IsValid())
        self.assertTrue(p.Equals(node_b))
        self.assertFalse(p.Equals(node_a))

    def test_parameter_attach_from_nodemap_name(self):
        """Test CParameter Attach from nodemap and name."""
        nodemapref = self.create_nodemapref()
        nodemap = nodemapref._Ptr

        p = pylon.Parameter()
        self.assertFalse(p.IsValid())

        # Attach from nodemap
        result = p.Attach(nodemap, "TestIntRO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        # Attach different node
        result = p.Attach(nodemap, "TestIntWO")
        self.assertTrue(result)
        self.assertTrue(p.IsValid())

        # Try to attach non-existent node
        result = p.Attach(nodemap, "NonExistent")
        self.assertFalse(result)

        nodemapref._Destroy()

    def test_parameter_release(self):
        """Test CParameter Release."""
        node_a = self.nodemap.GetNode("TestIntRO")

        p = pylon.Parameter(node_a)
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    def test_parameter_equals_parameter(self):
        """Test CParameter Equals with another parameter."""
        node_a = self.nodemap.GetNode("TestIntRO")
        node_b = self.nodemap.GetNode("TestIntWO")

        p1 = pylon.Parameter()
        p2 = pylon.Parameter(node_a)
        p3 = pylon.Parameter(node_a)
        p4 = pylon.Parameter(node_b)

        # Both empty
        p1_empty = pylon.Parameter()
        self.assertTrue(p1.Equals(p1_empty))

        # Same node
        self.assertTrue(p2.Equals(p3))
        self.assertTrue(p3.Equals(p2))

        # Different nodes
        self.assertFalse(p2.Equals(p4))
        self.assertFalse(p4.Equals(p2))

        # Empty vs attached
        self.assertFalse(p1.Equals(p2))
        self.assertFalse(p2.Equals(p1))

    def test_parameter_equals_inode(self):
        """Test CParameter Equals with GenApi::INode."""
        node_a = self.getINode("TestIntRO")
        node_b = self.getINode("TestIntWO")

        p1 = pylon.Parameter()
        p2 = pylon.Parameter(node_a)

        # Empty parameter
        self.assertTrue(p1.Equals(None))
        self.assertFalse(p1.Equals(node_a))

        # Attached parameter
        self.assertTrue(p2.Equals(node_a))
        self.assertFalse(p2.Equals(node_b))
        self.assertFalse(p2.Equals(None))

    def test_parameter_is_valid(self):
        """Test CParameter IsValid."""
        node_a = self.nodemap.GetNode("TestIntRO")

        p = pylon.Parameter()
        self.assertFalse(p.IsValid())

        p.Attach(node_a)
        self.assertTrue(p.IsValid())

        p.Release()
        self.assertFalse(p.IsValid())

    def test_parameter_is_readable_writable(self):
        """Test CParameter IsReadable and IsWritable."""

        # Read-only parameter
        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        self.assertTrue(p_ro.IsReadable())
        self.assertFalse(p_ro.IsWritable())

        # Write-only parameter
        p_wo = pylon.Parameter(self.nodemap, "TestIntWO")
        self.assertFalse(p_wo.IsReadable())
        self.assertTrue(p_wo.IsWritable())

        # Read-write parameter
        p_rw = pylon.Parameter(self.nodemap, "TestInt")
        self.assertTrue(p_rw.IsReadable())
        self.assertTrue(p_rw.IsWritable())

        # Unattached parameter
        p_unattached = pylon.Parameter()
        self.assertFalse(p_unattached.IsReadable())
        self.assertFalse(p_unattached.IsWritable())

    def test_parameter_get_node(self):
        """Test CParameter GetNode."""
        node_a = self.getINode("TestIntRO")

        p = pylon.Parameter(node_a)
        self.assertEqual(p.GetNode().GetName(), node_a.GetName())
        self.assertEqual(p.Node.GetName(), node_a.GetName())
        self.assertIsInstance(p.GetNode(), genicam.INode)

        p.Release()
        with self.assertRaises(Exception):
            p.GetNode()

    def test_parameter_to_string(self):
        """Test CParameter ToString."""
        # Unattached parameter should throw exception
        p = pylon.Parameter()
        with self.assertRaises(Exception):
            p.ToString()

        # Attached parameter
        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        # The TestIntRO has an initial value of 1500
        value_str = p_ro.ToString()
        self.assertEqual(value_str, "1500")
        # The TestIntRO has an initial value of 1500
        value_str = p_ro.ToString(True, True)
        self.assertEqual(value_str, "1500")
        value_str = p_ro.ToString(True)
        self.assertEqual(value_str, "1500")

    def test_parameter_from_string(self):
        """Test CParameter FromString."""
        # Unattached parameter should throw exception
        p = pylon.Parameter()
        with self.assertRaises(Exception):
            p.FromString("1234")

        # Write to read-write parameter
        p_rw = pylon.Parameter(self.nodemap, "TestInt")
        p_rw.FromString("1236")
        self.assertEqual(p_rw.ToString(), "1236")
        p_rw.FromString("1240, True")
        self.assertEqual(p_rw.ToString(), "1240")

    def test_parameter_is_value_cache_valid(self):
        """Test CParameter IsValueCacheValid."""
        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        # Cache validity depends on the implementation
        # Just verify the method is callable
        cache_valid = p_ro.IsValueCacheValid()
        self.assertIsInstance(cache_valid, bool)

    def test_parameter_get_access_mode(self):
        """Test CParameter GetAccessMode."""
        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        p_wo = pylon.Parameter(self.nodemap, "TestIntWO")
        p_rw = pylon.Parameter(self.nodemap, "TestInt")
        p_unattached = pylon.Parameter()

        # Verify access modes
        # RO should be readable only
        # WO should be writable only
        # RW should be both
        # Unattached should be neither (NI - Not Implemented)
        self.assertEqual(p_ro.GetAccessMode(), genicam.RO)
        self.assertEqual(p_wo.GetAccessMode(), genicam.WO)
        self.assertEqual(p_rw.AccessMode, genicam.RW)
        self.assertEqual(p_unattached.GetAccessMode(), genicam.NI)

    def test_parameter_get_info_or_default(self):
        """Test CParameter GetInfoOrDefault."""
        p_unattached = pylon.Parameter()
        self.assertEqual(p_unattached.GetInfoOrDefault(pylon.ParameterInfo_Name, "A"), "A")
        self.assertEqual(p_unattached.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "B"), "B")
        self.assertEqual(p_unattached.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "C"), "C")
        self.assertEqual(p_unattached.GetInfoOrDefault(pylon.ParameterInfo_Description, "D"), "D")

        p_attached = pylon.Parameter(self.nodemap, "TestBoolRW")
        self.assertEqual(p_attached.GetInfoOrDefault(pylon.ParameterInfo_Name, "A"), "TestBoolRW")
        self.assertEqual(
            p_attached.GetInfoOrDefault(pylon.ParameterInfo_DisplayName, "B"),
            "TestBooleanRW Display Name",
        )
        self.assertEqual(p_attached.GetInfoOrDefault(pylon.ParameterInfo_ToolTip, "C"), "TestBoolRW Tooltip")
        self.assertEqual(
            p_attached.GetInfoOrDefault(pylon.ParameterInfo_Description, "D"),
            "TestBoolRW Description",
        )

    def test_parameter_get_info(self):
        """Test CParameter GetInfo."""
        p_attached = pylon.Parameter(self.nodemap, "TestBoolRW")
        self.assertEqual(p_attached.GetInfo(pylon.ParameterInfo_Name), "TestBoolRW")
        self.assertEqual(p_attached.GetInfo(pylon.ParameterInfo_DisplayName), "TestBooleanRW Display Name")
        self.assertEqual(p_attached.GetInfo(pylon.ParameterInfo_ToolTip), "TestBoolRW Tooltip")
        self.assertEqual(p_attached.GetInfo(pylon.ParameterInfo_Description), "TestBoolRW Description")

        p_unattached = pylon.Parameter()
        with self.assertRaises(Exception):
            p_unattached.GetInfo(pylon.ParameterInfo_Name)
        with self.assertRaises(Exception):
            p_unattached.GetInfo(pylon.ParameterInfo_DisplayName)
        with self.assertRaises(Exception):
            p_unattached.GetInfo(pylon.ParameterInfo_ToolTip)
        with self.assertRaises(Exception):
            p_unattached.GetInfo(pylon.ParameterInfo_Description)

    def test_parameter_to_string_or_default(self):
        """Test CParameter ToStringOrDefault."""
        p_unattached = pylon.Parameter()
        self.assertEqual(p_unattached.ToStringOrDefault("A"), "A")

        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        self.assertEqual(p_ro.ToStringOrDefault("A"), "1500")

        p_wo = pylon.Parameter(self.nodemap, "TestIntWO")
        self.assertEqual(p_wo.ToStringOrDefault("A"), "A")

    def test_parameter_str(self):
        """Test CParameter __str__."""
        p_unattached = pylon.Parameter()
        self.assertEqual(str(p_unattached), "<not found>")
        p_wo = pylon.Parameter(self.nodemap, "TestIntWO")
        self.assertEqual(str(p_wo), "<not readable>")
        p_ro = pylon.Parameter(self.nodemap, "TestIntRO")
        self.assertEqual(str(p_ro), "1500")

    # ------------------------------------------------------------------
    # Compatibility with genicam
    # ------------------------------------------------------------------

    def test_genicam_compatibility(self):
        """Parameter can be used wherever genicam interfaces are expected."""
        p = pylon.Parameter(self.nodemap, "TestInt")
        self.assertIsInstance(p, genicam.IValue)
        self.assertTrue(genicam.IsReadable(p))
        self.assertTrue(genicam.IsWritable(p))

    # ------------------------------------------------------------------
    # GetValueOrDefault
    # ------------------------------------------------------------------

    def test_get_value_or_default_readable(self):
        """GetValueOrDefault returns the parameter value as a string for a readable parameter."""
        p = pylon.Parameter(self.nodemap, "TestIntRO")
        self.assertEqual("1500", p.GetValueOrDefault("fallback"))

    def test_get_value_or_default_write_only(self):
        """GetValueOrDefault returns the supplied default for a write-only parameter."""
        p = pylon.Parameter(self.nodemap, "TestIntWO")
        self.assertFalse(p.IsReadable())
        self.assertEqual("fallback", p.GetValueOrDefault("fallback"))

    def test_get_value_or_default_unattached(self):
        """GetValueOrDefault returns the supplied default for an unattached parameter."""
        p = pylon.Parameter()
        self.assertFalse(p.IsReadable())
        self.assertEqual("fallback", p.GetValueOrDefault("fallback"))


if __name__ == "__main__":
    unittest.main()
