# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:  Fritz Dierks
#  $Header$
# -----------------------------------------------------------------------------
"""!
\file
"""
from genicam import *
import unittest
from genicamtestcase import GenicamTestCase

from testport import CTestPort, sizeof, cast_buffer, cast_data, CQuadTestPort


class PortTestSuite(GenicamTestCase):
    def test_PortAccess(self):
        # create and initialize a test port
        Port = CTestPort()
        MyRegister = 42
        Port.CreateEntry(0x00ff, "uint32_t", MyRegister, RW, LittleEndian)

        """[ GenApiTest@PortTestSuite_TestPortAccess.xml|gxml
            <Port Name="MyPort" >
            </Port>
        """
        # create and connect a camera object
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PortTestSuite_TestPortAccess")
        Camera._Connect(Port, "MyPort")

        port = Camera._GetNode("MyPort")

        # read back value
        Buffer = port.Read(0x00ff, sizeof("uint32_t"))
        self.assertEqual(MyRegister, cast_buffer("uint32_t", LittleEndian, Buffer))

        # write a new value
        MyNewRegister = 99
        port.Write(0x00ff, cast_data("uint32_t", LittleEndian, MyNewRegister))
        Buffer = port.Read(0x00ff, sizeof("uint32_t"))
        self.assertEqual(MyNewRegister, cast_buffer("uint32_t", LittleEndian, Buffer))

    def test_TestPort(self):
        # some basics
        # create and initialize a test port
        Port = CTestPort()
        MyRegister = 42
        Port.CreateEntry(0x0000, "uint32_t", 42, RW, LittleEndian)
        Port.CreateEntry(0x000f, "uint32_t", MyRegister, RW, LittleEndian)
        MyRegisterLittleEndian = MyRegister
        Port.CreateEntry(0x00ff, "uint32_t", MyRegisterLittleEndian, RW, LittleEndian)

        # Test IPort::Read method
        Port = CTestPort()

        # write something to the register map
        MyRegister = 42
        Port.CreateEntry(0x00ff, "uint32_t", MyRegister, RO, LittleEndian)

        # check if it's there
        Buffer = Port.Read(0x00ff, sizeof("uint32_t"))
        self.assertEqual(MyRegister, cast_buffer("uint32_t", LittleEndian, Buffer))

        # try to read from an invalid address
        with self.assertRaises(GenericException):
            Port.Read(0x0000, sizeof("uint32_t"))

        # try to read with invalid length
        with self.assertRaises(GenericException):
            Port.Read(0x00ff, 8)

        # Create an WO entry
        MyRegister = 43
        Port.CreateEntry(0x000f, "uint32_t", MyRegister, WO, LittleEndian)

        # try to read from a WO address
        with self.assertRaises(GenericException):
            Port.Read(0x000f, sizeof("uint32_t"))
        # Test IPort::Write method

        Port = CTestPort()

        # write something to the register map
        MyRegister = 0
        Port.CreateEntry(0x00ff, "uint32_t", MyRegister, RW, LittleEndian)

        # write at the location
        MyRegister = 42
        Port.Write(0x00ff, cast_data("uint32_t", LittleEndian, MyRegister))

        # read back
        Buffer = Port.Read(0x00ff, sizeof("uint32_t"))
        self.assertEqual(MyRegister, cast_buffer("uint32_t", LittleEndian, Buffer))

        # try to write at an invalid address
        with self.assertRaises(GenericException):
            Port.Write(0x0000, cast_data("uint32_t", LittleEndian, MyRegister))

        # try to write with invalid length
        with self.assertRaises(GenericException):
            Port.Write(0x00ff, bytes(8))

        # make the entry RO
        MyRegister = 0
        Port.CreateEntry(0x000f, "uint32_t", MyRegister, RO, LittleEndian)

        # try to write to a RO address
        with self.assertRaises(GenericException):
            Port.Write(0x000f, cast_data("uint32_t", LittleEndian, MyRegister))

    def test_PortRef(self):
        # create and initialize a test port
        Port = CTestPort()
        MyRegister = 0
        Port.CreateEntry(0x00ff, "uint32_t", MyRegister, RW, LittleEndian)

        """[ GenApiTest@PortTestSuite_TestPortRef.xml|gxml
            <Port Name="MyPort" >
            </Port>
            <IntReg Name="TestReg">
               <Address>0x00ff</Address>
               <Length>1</Length>
               <AccessMode>RW</AccessMode>
               <pPort>MyPort</pPort>
               <Sign>Unsigned</Sign>
               <Endianess>BigEndian</Endianess>
            </IntReg>
        """

        # create and connect a camera object
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PortTestSuite_TestPortRef")
        Camera._Connect(Port, "MyPort")

        # Create a pointer to MyPort, a pointer to the IntReg and a CPortRef object referencing MyPort
        port = Camera._GetNode("MyPort")
        testReg = Camera._GetNode("TestReg")

        # Write and read back using CPortRef
        WriteBuffer = 3

        port.Write(0x00ff, cast_data("uint32_t", LittleEndian, WriteBuffer))
        ReadBuffer = port.Read(0x00ff, sizeof("uint32_t"))
        self.assertTrue(cast_buffer("uint32_t", LittleEndian, ReadBuffer) == WriteBuffer)

        # Write and read back using IntReg
        testReg.SetValue(25)
        self.assertTrue(testReg.GetValue() == 25)

        # Write using pointer to IntReg, read back through CPortRef
        testReg.SetValue(42)
        ReadBuffer = port.Read(0x00ff, sizeof("uint32_t"))
        self.assertTrue(cast_buffer("uint32_t", LittleEndian, ReadBuffer) == 42)

        # Write through CPortRef, read back through pointer to IntReg
        # The values should only match once the IntReg cache has been invalidated.
        WriteBuffer = 31
        port.Write(0x00ff, cast_data("uint32_t", LittleEndian, WriteBuffer))
        self.assertTrue(testReg.GetValue() != WriteBuffer)

        # Invalidate the port's node cache and test for correct read back
        Port.InvalidateNode()
        self.assertTrue(testReg.GetValue() == WriteBuffer)

        # Make sure the failed write didn't modify the value of the node.
        self.assertTrue(testReg.GetValue() == WriteBuffer)

    def test_Chunk(self):
        """[ GenApiTest@PortTestSuite_TestChunk_1.xml|gxml
         
          <Port Name="BogusPort">
                <ChunkID>12</ChunkID>
            </Port>
         
        """

        # create and connect a camera object
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PortTestSuite_TestChunk_1")
        Port = Camera._GetNode("BogusPort")

        self.assertEqual(NA, Port.GetAccessMode())
        self.assertTrue(Port.GetChunkID() == "12")

        self.assertTrue(Port.GetSwapEndianess() == No)

        """[ GenApiTest@PortTestSuite_TestChunk_2.xml|gxml
         
          <Port Name="BogusPort">
            </Port>
         
        """

        # create and connect a camera object
        Camera2 = CNodeMapRef()
        Camera2._LoadXMLFromFile("GenApiTest", "PortTestSuite_TestChunk_2")
        Port2 = Camera2._GetNode("BogusPort")

        self.assertEqual(NI, Port2.GetAccessMode())
        self.assertTrue(Port2.GetChunkID() == "")

        self.assertTrue(Port2.GetSwapEndianess() == No)

    @unittest.skip("CreateEntries not implemented")
    def test_Chunk2(self):
        """[ GenApiTest@PortTestSuite_TestChunk_3.xml|gxml
      
        <Port Name="BogusPort">
            <pChunkID>ChunkIDReg</pChunkID>
        </Port>
          
        <StringReg Name="ChunkIDReg">
            <Address>0x00A0</Address>
            <Length>40</Length>
            <AccessMode>RW</AccessMode>
            <pPort>MyPort</pPort>
        </StringReg>
          
        <Port Name="MyPort"/>
          
        """
        # create and connect a camera object
        Camera3 = CNodeMapRef()
        Camera3._LoadXMLFromFile("GenApiTest", "PortTestSuite_TestChunk_3")
        Port3 = Camera3._GetNode("BogusPort")
        # self.assertEqual ("IPort", GetInterfaceName(Port3))

        # create and initialize a test port
        MyPort = CQuadTestPort()
        TestValue = "30"
        MyPort.CreateEntries(0x00A0, 0x00E0, "uint32_t", TestValue, RW, LittleEndian)

        # connect the node map to the port
        Camera3._Connect(MyPort, "MyPort")

        # Manits #95
        self.assertEqual(NA, Port3.GetAccessMode())
        self.assertTrue(Port3.GetChunkID() == "30")
        PortConstr3 = Camera3._GetNode("BogusPort")
        self.assertTrue(PortConstr3.GetSwapEndianess() == No)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
