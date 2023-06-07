# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:
#  $Header:
# -----------------------------------------------------------------------------

from genicam import *
import unittest
from genicamtestcase import GenicamTestCase
from testport import CTestPort, cast_buffer, cast_data


class RegisterTestSuite(GenicamTestCase):
    def test_ValueAccessSwiss(self):
        """[ GenApiTest@RegisterTestSuite_TestValueAccessSwiss.xml|gxml
    
        <IntReg Name="Register">
            <pIsAvailable>RegAvailable</pIsAvailable>
            <pIsLocked>RegLocked</pIsLocked>
            <pAddress>BaseAddress</pAddress>
            <Address>0x0f00</Address>
            <IntSwissKnife Name="Dummy">
                <pVariable Name="I">Index</pVariable>
                <Formula>0x00f0 * I</Formula>
            </IntSwissKnife>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
    
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Integer Name="Index">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="RegAvailable">
            <Value>1</Value>
        </Integer>
        <Integer Name="RegLocked">
            <Value>0</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        # LOG4CPP_NS::Category pLogger.SetValue(&CLog::GetLogger( "CppUnit.Performance" ))

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestValueAccessSwiss")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xfff0, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Index = Camera.GetNode("Index")

        self.assertEqual(4, Register.GetLength())

        self.assertEqual(0xff00, Register.GetAddress())

        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Index.SetValue(1)
        self.assertEqual(1, Index.GetValue())
        self.assertEqual(0xfff0, Register.GetAddress())

        # from the other one read less bytes
        # Result = 0xFEDCBA98
        # Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        # print(hex(Result))
        # self.assertEqual( 0xFEDC4321, Result )


        Index.SetValue(0)
        Index.GetNode().InvalidateNode()
        # TEST_BEGIN(1000)
        #    Register.Get((uint8_t*)&Result, 4)
        #    StopWatch.PauseBegin()
        #    Index = Index ? 0 : 1
        #    Index.SetValue(Index)
        #    StopWatch.PauseEnd()
        # TEST_END( Register::GetValue (with index computed via SwissKnife) )

    def test_ValueAccessIndex(self):
        """[ GenApiTest@RegisterTestSuite_TestValueAccessIndex.xml|gxml
    
        <IntReg Name="Register">
            <pAddress>BaseAddress</pAddress>
            <Address>0x0f00</Address>
            <pIndex Offset="0x00f0">Index</pIndex>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Integer Name="Index">
            <Value>0</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        # LOG4CPP_NS::Category pLogger.SetValue(&CLog::GetLogger( "CppUnit.Performance" ))

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestValueAccessIndex")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xfff0, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Index = Camera.GetNode("Index")

        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Index.SetValue(1)
        self.assertEqual(1, Index.GetValue())

        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x87654321, Result)

        # GCLOGINFO( pLogger, "-------------------------------------------------" )
        # GCLOGINFO( pLogger, "Setup : Register <=> Integer (BaseAddress)" )
        # GCLOGINFO( pLogger, "                 <=> Integer (Index via Swissknife)" )

        Index.SetValue(0)
        Index.GetNode().InvalidateNode()
        # TEST_BEGIN(1000)
        #    Register.Get((uint8_t*)&Result, 4)
        #    StopWatch.PauseBegin()
        #    Index = Index ? 0 : 1
        #    Index.SetValue(Index)
        #    StopWatch.PauseEnd()
        # TEST_END( Register::GetValue (with index computed via Index) )

    def test_ValueAccessIndexPOffset(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return


        """[ GenApiTest@RegisterTestSuite_TestValueAccessIndexPOffset.xml|gxml
    
        <IntReg Name="Register">
            <pAddress>BaseAddress</pAddress>
            <Address>0x0f00</Address>
            <pIndex pOffset="Offset">Index</pIndex>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Integer Name="Index">
            <Value>0</Value>
        </Integer>
    
        <Integer Name="Offset">
            <Value>0</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestValueAccessIndexPOffset")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xfff0, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Index = Camera.GetNode("Index")

        Offset = Camera.GetNode("Offset")

        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Index.SetValue(1)
        self.assertEqual(1, Index.GetValue())
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Offset.SetValue(0xf0)
        self.assertEqual(0xf0, Offset.GetValue())
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x87654321, Result)

    def test_ValueAccessIndexNoOffset(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return


        """[ GenApiTest@RegisterTestSuite_TestValueAccessIndexNoOffset.xml|gxml
    
        <IntReg Name="Register">
            <pAddress>BaseAddress</pAddress>
            <Address>0x0f00</Address>
            <pIndex>Index</pIndex>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Integer Name="Index">
            <Value>0</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestValueAccessIndexNoOffset")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xff04, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Index = Camera.GetNode("Index")

        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Index.SetValue(1)
        self.assertEqual(1, Index.GetValue())

        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x87654321, Result)

    def test_ValueAccess(self):
        """[ GenApiTest@RegisterTestSuite_TestValueAccess.xml|gxml
    
        <IntReg Name="Register">
            <pAddress>BaseAddress</pAddress>
            <pAddress>Enum</pAddress>
            <Address>0x0f00</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Enumeration Name="Enum">
            <EnumEntry Name="EnumValue1">
                <Value>0x00</Value>
           </EnumEntry>
            <EnumEntry Name="EnumValue2">
                <Value>0xf0</Value>
           </EnumEntry>
            <Value>0x00</Value>
        </Enumeration>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestValueAccess")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xfff0, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Enum = Camera.GetNode("Enum")

        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Enum.SetValue("EnumValue2")

        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x87654321, Result)

    def test_EmbeddedSwissKnife(self):
        """[ GenApiTest@RegisterTestSuite_TestEmbeddedSwissKnife.xml|gxml
    
        <IntReg Name="Register">
            <pAddress>BaseAddress</pAddress>
            <pAddress>Enum</pAddress>
            <IntSwissKnife Name="R1" >
            <Formula>0x0100</Formula>
            </IntSwissKnife>
            <IntSwissKnife Name="R2" >
            <Formula>0x0100</Formula>
            </IntSwissKnife>
            <IntSwissKnife Name="R3" >
            <Formula>0x0100</Formula>
            </IntSwissKnife>
            <IntSwissKnife Name="R4" >
            <Formula>0x0100</Formula>
            </IntSwissKnife>
            <Address>0x0b00</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="BaseAddress">
            <Value>0xf000</Value>
        </Integer>
    
        <Enumeration Name="Enum">
            <EnumEntry Name="EnumValue1">
                <Value>0x00</Value>
           </EnumEntry>
            <EnumEntry Name="EnumValue2">
                <Value>0xf0</Value>
           </EnumEntry>
            <Value>0x00</Value>
        </Enumeration>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestEmbeddedSwissKnife")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0xff00, "uint32_t", 0x12345678, RW, LittleEndian)
        Port.CreateEntry(0xfff0, "uint32_t", 0x87654321, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        Enum = Camera.GetNode("Enum")
        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

        Enum.SetValue("EnumValue2")

        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x87654321, Result)

    def test_EmbeddedSwissKnife2(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return


        """[ GenApiTest@RegisterTestSuite_TestEmbeddedSwissKnife2.xml|gxml
    
        <IntReg Name="Register">
            <IntSwissKnife Name="Addr" >
            <pVariable Name="Var">MyVar</pVariable>
            <Constant Name="Const">0x100</Constant>
            <Expression Name="Expr">Const+Var+0x100</Expression>
            <Formula>Expr+0x100</Formula>
            </IntSwissKnife>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="MyVar">
            <Value>0x100</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestEmbeddedSwissKnife2")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x400, "uint32_t", 0x12345678, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("Register")

        self.assertEqual(4, Register.GetLength())

        Result = 0
        Result = cast_buffer("uint32_t", LittleEndian, Register.Get(4))
        self.assertEqual(0x12345678, Result)

    def test_RegisterNode(self):
        """[ GenApiTest@RegisterTestSuite_TestRegisterNode.xml|gxml
    
        <Register Name="Register">
            <pAddress>Address</pAddress>
            <pLength>Length</pLength>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <IntReg Name="Length">
            <Address>0</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <IntReg Name="Address">
            <Address>4</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestRegisterNode")

        LenVal = 1
        AddrVal = 0x100

        Port = CTestPort()
        Port.CreateEntry(0x0, "uint32_t", LenVal, RW, LittleEndian)
        Port.CreateEntry(0x4, "uint32_t", AddrVal, RW, LittleEndian)
        RegVal = 0x11
        Port.CreateEntry(0x100, "uint8_t", RegVal, RW, LittleEndian)
        RegVal = 0x22
        Port.CreateEntry(0x101, "uint8_t", RegVal, RW, LittleEndian)
        RegVal2 = 0x3344
        Port.CreateEntry(0x102, "uint16_t", RegVal2, RW, LittleEndian)
        Camera._Connect(Port, "Port")

        Len = Camera.GetNode("Length")
        Addr = Camera.GetNode("Address")
        Register = Camera.GetNode("Register")

        # excercise pAddress and pLength
        Byte = cast_buffer("uint8_t", LittleEndian, Register.Get(1))
        self.assertEqual(0x11, Byte)
        Addr.SetValue(0x101)
        Byte = cast_buffer("uint8_t", LittleEndian, Register.Get(1))
        self.assertEqual(0x22, Byte)
        Addr.SetValue(0x102)
        Len.SetValue(2)
        Word = cast_buffer("uint16_t", LittleEndian, Register.Get(2))
        self.assertEqual(0x3344, Word)
        Addr.SetValue(0x100)
        Len.SetValue(1)
        # try to get/set more data than register length
        with self.assertRaises(OutOfRangeException):
            Register.Get(2)
        with self.assertRaises(OutOfRangeException):
            Register.Set(cast_data("uint16_t", LittleEndian, 0xaa55))

    def test_AccessModeNoCache(self):
        """[ GenApiTest@RegisterTestSuite_TestAccessModeNoCache.xml|gxml
        <Register Name="RegisterA">
           <pIsImplemented>NoCachableIntReg</pIsImplemented>
           <Address>0</Address>
           <Length>4</Length>
           <AccessMode>RW</AccessMode>
           <pPort>Port</pPort>
        </Register>
        <Register Name="RegisterB">
           <pIsAvailable>NoCachableIntReg</pIsAvailable>
           <Address>0</Address>
           <Length>4</Length>
           <AccessMode>RW</AccessMode>
           <pPort>Port</pPort>
        </Register>
        <Register Name="RegisterC">
           <pIsLocked>NoCachableIntReg</pIsLocked>
           <Address>0</Address>
           <Length>4</Length>
           <AccessMode>RW</AccessMode>
           <pPort>Port</pPort>
        </Register>
    
        <IntReg Name="NoCachableIntReg">
            <Address>4</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>NoCache</Cachable>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
        <Port Name="Port"/>
        """
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "RegisterTestSuite_TestAccessModeNoCache")

        Port = CTestPort()
        Port.CreateEntry(0x4, "int32_t", 1, RW, LittleEndian)
        Camera._Connect(Port, "Port")

        RegisterA = Camera.GetNode("RegisterA")
        RegisterB = Camera.GetNode("RegisterB")
        RegisterC = Camera.GetNode("RegisterC")
        NoCachableIntReg = Camera.GetNode("NoCachableIntReg")

        self.assertEqual(NoCache, NoCachableIntReg.GetNode().GetCachingMode())
        self.assertEqual(Yes, NoCachableIntReg.GetNode().IsAccessModeCacheable())

        self.assertEqual(No, RegisterA.GetNode().IsAccessModeCacheable())
        self.assertEqual(No, RegisterB.GetNode().IsAccessModeCacheable())
        self.assertEqual(No, RegisterC.GetNode().IsAccessModeCacheable())

        self.assertEqual(RW, RegisterA.GetAccessMode())
        self.assertEqual(RW, RegisterB.GetAccessMode())
        self.assertEqual(RO, RegisterC.GetAccessMode())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
