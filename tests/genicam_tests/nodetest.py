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
from testport import CTestPort, cast_data, CStructTestPort, cast_buffer, sizeof
from callbackhelper import CallbackObject
import sys
import genicam


class NodeTestSuite(GenicamTestCase):
    def test_AccessMode(self):
        """[ GenApiTest@NodeTestSuite_TestAccessMode_1.xml|gxml
    
            <Category Name="Node0">
                <pFeature>Node00</pFeature>
                <pFeature>Node01</pFeature>
            </Category>
    
            <Category Name="Cat">
                <pIsImplemented>CatImplemented</pIsImplemented>
                <pIsAvailable>CatAvailable</pIsAvailable>
                <pFeature>CatNode</pFeature>
            </Category>
    
            <Node Name="CatNode">
            </Node>
    
            <Category Name="CatFtrNI">
                <pFeature>FtrNI</pFeature>
            </Category>
    
            <Integer Name="FtrNI">
            <pIsImplemented>AMCtrl</pIsImplemented>
            <Value>0</Value>
            </Integer>
    
            <Category Name="CatFtrNA">
                <pFeature>FtrNA</pFeature>
            </Category>
    
            <Integer Name="FtrNA">
            <pIsAvailable>AMCtrl</pIsAvailable>
            <Value>0</Value>
            </Integer>
    
            <Integer Name="AMCtrl">
            <Value>0</Value>
            </Integer>
    
            <Node Name="Node00">
                <pIsImplemented>Implemented0</pIsImplemented>
                <pIsAvailable>Available</pIsAvailable>
                <pIsLocked>Locked</pIsLocked>
            </Node>
    
            <Category Name="Node01">
                <pFeature>Node010</pFeature>
            </Category>
    
            <Node Name="Node010">
                <pIsImplemented>Implemented010</pIsImplemented>
            </Node>
    
            <Integer Name="Implemented0">
                <pIsAvailable>Implemented0Available</pIsAvailable>
                <Value>1</Value>
            </Integer>
    
            <Integer Name="Implemented010">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="Available">
                <pIsAvailable>AvailableAvailable</pIsAvailable>
                <Value>1</Value>
            </Integer>
    
            <Integer Name="Locked">
                <pIsAvailable>LockedAvailable</pIsAvailable>
                <Value>0</Value>
            </Integer>
    
            <Integer Name="Implemented0Available">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="AvailableAvailable">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="LockedAvailable">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="CatImplemented">
                <pIsAvailable>CatImplementedAvailable</pIsAvailable>
                <Value>1</Value>
            </Integer>
    
            <Integer Name="CatAvailable">
                <pIsAvailable>CatAvailableAvailable</pIsAvailable>
                <Value>1</Value>
            </Integer>
    
            <Integer Name="CatImplementedAvailable">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="CatAvailableAvailable">
                <Value>1</Value>
            </Integer>
    
            <Node Name="NodeImplWO">
                <pIsImplemented>WONode</pIsImplemented>
            </Node>
    
            <Node Name="NodeAvailWO">
                <pIsAvailable>WONode</pIsAvailable>
            </Node>
    
            <Node Name="NodeLockedWO">
                <pIsLocked>WONode</pIsLocked>
            </Node>
    
            <Integer Name="WONode">
                <ImposedAccessMode>WO</ImposedAccessMode>
                <Value>0</Value>
            </Integer>
    
            <Integer Name="WONode2">
                <pIsLocked>LockedAvailable</pIsLocked>
                <ImposedAccessMode>WO</ImposedAccessMode>
                <Value>0</Value>
            </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestAccessMode_1")

        Node0 = Camera.GetNode("Node0")
        Cat = Camera.GetNode("Cat")
        CatFtrNI = Camera.GetNode("CatFtrNI")
        CatFtrNA = Camera.GetNode("CatFtrNA")
        Node00 = Camera.GetNode("Node00")
        Node01 = Camera.GetNode("Node01")
        Node010 = Camera.GetNode("Node010")
        Implemented0 = Camera.GetNode("Implemented0")
        Implemented010 = Camera.GetNode("Implemented010")
        Available = Camera.GetNode("Available")
        Locked = Camera.GetNode("Locked")
        CatImplemented = Camera.GetNode("CatImplemented")
        CatAvailable = Camera.GetNode("CatAvailable")
        # CatLocked = Camera.GetNode("CatLocked")
        CatNode = Camera.GetNode("CatNode")
        NodeImplWO = Camera.GetNode("NodeImplWO")
        NodeAvailWO = Camera.GetNode("NodeAvailWO")
        NodeLockedWO = Camera.GetNode("NodeLockedWO")
        WONode = Camera.GetNode("WONode")
        WONode2 = Camera.GetNode("WONode2")
        ######## test to GetParents
        # NodeList_t mParents
        # NodeImplWO.GetParents(mParents)

        self.assertEqual(intfIValue, CatNode.Node.GetPrincipalInterfaceType())
        self.assertEqual(intfIValue, Node00.Node.GetPrincipalInterfaceType())
        self.assertEqual(intfICategory, Node0.Node.GetPrincipalInterfaceType())
        MyNode = Camera.GetNode("Node00")
        self.assertEqual(intfIValue, MyNode.Node.GetPrincipalInterfaceType())

        # Check default access mode
        with self.assertRaises(LogicalErrorException):
            Node0.Node.GetAlias()
        self.assertEqual(RO, Node0.Node.GetAccessMode())
        self.assertEqual(RW, Node00.Node.GetAccessMode())
        self.assertEqual(RO, Node01.Node.GetAccessMode())
        self.assertEqual(RW, Node010.Node.GetAccessMode())

        # Use cache
        self.assertEqual(RO, Node0.GetAccessMode())

        # Check Implemented
        Implemented0.SetValue(0)
        self.assertEqual(NI, Node00.GetAccessMode())
        Implemented0.SetValue(1)

        # Check Available
        Available.SetValue(0)
        self.assertEqual(NA, Node00.GetAccessMode())
        Available.SetValue(1)

        # Check Locked
        Locked.SetValue(1)
        self.assertEqual(RO, Node00.GetAccessMode())
        Locked.SetValue(0)

        # Check Implemented of a <pFeature> node
        Implemented010.SetValue(0)
        self.assertEqual(RO, Node0.GetAccessMode())

        # note that the access mode is either NI or RO since NI does not change
        # the access mode can be always(!) cacheable
        # as a consequence this test case is not valid for categories
        self.assertEqual(RO, Node01.GetAccessMode())
        Implemented010.SetValue(1)

        # Check Category access mode implied by pFeature
        self.assertEqual(NI, CatFtrNI.GetAccessMode())
        self.assertEqual(RO, CatFtrNA.GetAccessMode())

        # Check flag access
        Implemented0.SetValue(0)
        Available.SetValue(0)
        Locked.SetValue(1)
        self.assertEqual(False, IsImplemented(Node00))
        self.assertEqual(False, IsAvailable(Node00))
        Implemented0.SetValue(1)
        Available.SetValue(0)
        self.assertEqual(True, IsImplemented(Node00))
        self.assertEqual(False, IsAvailable(Node00))
        self.assertEqual(False, IsReadable(Node00))
        self.assertEqual(False, IsWritable(Node00))
        Available.SetValue(1)
        self.assertEqual(True, IsAvailable(Node00))
        Locked.SetValue(1)
        self.assertEqual(RO, Node00.GetAccessMode())
        self.assertEqual(True, IsReadable(Node00))
        self.assertEqual(False, IsWritable(Node00))
        Locked.SetValue(0)
        self.assertEqual(True, IsWritable(Node00))
        # and again with the flags made "not available"
        Implemented0Available = Camera.GetNode("Implemented0Available")
        AvailableAvailable = Camera.GetNode("AvailableAvailable")
        LockedAvailable = Camera.GetNode("LockedAvailable")
        Implemented0Available.SetValue(0)
        self.assertEqual(True, IsImplemented(Node00))
        self.assertEqual(False, IsAvailable(Node00))
        Implemented0Available.SetValue(1)
        self.assertEqual(True, IsImplemented(Node00))
        AvailableAvailable.SetValue(0)
        self.assertEqual(True, IsImplemented(Node00))
        self.assertEqual(False, IsAvailable(Node00))
        self.assertEqual(False, IsReadable(Node00))
        self.assertEqual(False, IsWritable(Node00))
        AvailableAvailable.SetValue(1)
        self.assertEqual(True, IsWritable(Node00))

        # WO flags
        self.assertEqual(False, IsReadable(WONode))
        self.assertEqual(NA, NodeImplWO.GetAccessMode())
        self.assertEqual(NA, NodeAvailWO.GetAccessMode())
        self.assertEqual(NA, NodeLockedWO.GetAccessMode())

        LockedAvailable.SetValue(0)
        self.assertEqual(NA, Node00.GetAccessMode())
        self.assertEqual(False, IsReadable(Node00))
        self.assertEqual(False, IsWritable(Node00))
        LockedAvailable.SetValue(1)
        self.assertEqual(True, IsWritable(Node00))
        # Do similar checks for category
        CatImplemented.SetValue(0)
        self.assertEqual(NI, Cat.GetAccessMode())
        CatImplemented.SetValue(1)
        CatAvailable.SetValue(0)
        self.assertEqual(NI, Cat.GetAccessMode())
        CatAvailable.SetValue(1)
        self.assertEqual(False, IsAvailable(Cat))
        CatImplementedAvailable = Camera.GetNode("CatImplementedAvailable")
        CatAvailableAvailable = Camera.GetNode("CatAvailableAvailable")
        CatImplementedAvailable.SetValue(0)
        self.assertEqual(False, IsImplemented(Cat))
        self.assertEqual(False, IsAvailable(Cat))
        CatImplementedAvailable.SetValue(1)
        CatAvailableAvailable.SetValue(0)
        IsImplemented(Cat)
        IsAvailable(Cat)
        self.assertEqual(False, IsImplemented(Cat))
        self.assertEqual(False, IsAvailable(Cat))
        self.assertEqual(False, IsReadable(Cat))
        self.assertEqual(False, IsWritable(Cat))
        CatAvailableAvailable.SetValue(1)
        self.assertEqual(False, IsAvailable(Cat))

        # Check visibility
        self.assertEqual(True, IsVisible(Beginner, Guru))
        self.assertEqual(False, IsVisible(Invisible, Expert))

        # Check flag combinations
        self.assertEqual(NI, Combine(RO, NI))
        self.assertEqual(NA, Combine(RO, NA))
        self.assertEqual(NA, Combine(WO, RO))

        # check what happens if a WO node is locked
        LockedAvailable.SetValue(0)
        self.assertTrue(IsWritable(WONode2))
        self.assertTrue(not IsReadable(WONode2))
        LockedAvailable.SetValue(1)
        self.assertTrue(not IsWritable(WONode2))
        self.assertTrue(not IsReadable(WONode2))

        # ticket #693
        self.assertTrue(not IsReadable(None))
        self.assertTrue(not IsWritable(None))
        self.assertTrue(not IsImplemented(None))
        self.assertTrue(not IsAvailable(None))

        self.assertTrue(not IsReadable(None))
        self.assertTrue(not IsWritable(None))
        self.assertTrue(not IsImplemented(None))
        self.assertTrue(not IsAvailable(None))

        # to complete happy path, check also locked node
        # whose value had different access mode than RW
        """[ GenApiTest@NodeTestSuite_TestAccessMode_2.xml|gxml
    
        <Integer Name="Value">
            <pIsLocked>Locked</pIsLocked>
            <pValue>ValueReg</pValue>
            <Min>0</Min>
            <Max>4294967296</Max>
            <Inc>1</Inc>
        </Integer>
    
        <IntReg Name="ValueReg">
            <Address>0x0104</Address>
            <Length>4</Length>
            <AccessMode>WO</AccessMode>
             <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
             <Endianess>LittleEndian</Endianess>
            <Representation>Linear</Representation>
        </IntReg>
    
        <Integer Name="Locked">
            <Value>1</Value>
        </Integer>
    
        <Port Name="Port"/>
    
        """

        Camera2 = CNodeMapRef()
        Camera2._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestAccessMode_2")

        Port2 = CTestPort()
        Port2.CreateEntry(0x0104, "uint32_t", 1024, RW, LittleEndian)
        Camera2._Connect(Port2, "Port")

        Value = Camera2.GetNode("Value")

        with self.assertRaises(AccessException):
            Value.GetValue()

        self.assertEqual(False, IsAvailable(Value))

    def test_NameSpace(self):

        """[ GenApiTest@NodeTestSuite_TestNameSpace.xml|gxml
            <Category Name="Root">
                <pFeature>MyDefault</pFeature>
                <pFeature>MyStandard</pFeature>
                <pFeature>MyCustom</pFeature>
            </Category>
            <Node Name="MyDefault"/>
            <Node Name="MyStandard" NameSpace="Standard"/>
            <Node Name="MyCustom" NameSpace="Custom"/>
        """
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestNameSpace")

        with self.assertRaises(LogicalErrorException):
            Camera.GetNode("Std::")  # check an invalid name. This must work but has to return a None-pointer!

        Node = Camera.GetNode("Cust::MyDefault")

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Std::MyDefault")

        Node = Camera.GetNode("MyDefault").Node

        self.assertEqual(Custom, Node.GetNameSpace())
        self.assertEqual("MyDefault", Node.GetName())
        self.assertEqual("Cust::MyDefault", Node.GetName(True))

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Cust::MyStandard")

        Node = Camera.GetNode("Std::MyStandard")

        Node = Camera.GetNode("MyStandard").Node

        self.assertEqual(Standard, Node.GetNameSpace())
        self.assertEqual("MyStandard", Node.GetName())
        self.assertEqual("Std::MyStandard", Node.GetName(True))

        Node = Camera.GetNode("Cust::MyCustom")

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Std::MyCustom")

        Node = Camera.GetNode("MyCustom").Node

        self.assertEqual(Custom, Node.GetNameSpace())
        self.assertEqual("MyCustom", Node.GetName())
        self.assertEqual("Cust::MyCustom", Node.GetName(True))

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Trallala::MyDefault")

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Std::Trallala")

        with self.assertRaises(LogicalErrorException):
            Node = Camera.GetNode("Trallala")

    def test_PropertyAccess(self):
        # Note that DisplayName is handled slightly different way for EnumEntry
        # where Symbolic is also considered

        """[ GenApiTest@NodeTestSuite_TestPropertyAccess.xml|gxml
    
        <Node Name="MyName" NameSpace="Standard">
            <ToolTip>MyToolTip</ToolTip>
            <Description>MyDescription</Description>
            <DisplayName>MyDisplayName</DisplayName>
            <Visibility>Guru</Visibility>
        </Node>
        <Enumeration Name="Enum0">
            <EnumEntry Name="EnumEntry0">
                <DisplayName>EnumDisplayName</DisplayName>
                <Value>0</Value>
            </EnumEntry>
            <EnumEntry Name="EnumEntry1">
                <Value>1</Value>
                <Symbolic>EnumSymbolic</Symbolic>
            </EnumEntry>
            <EnumEntry Name="EnumEntry2">
                <Value>2</Value>
            </EnumEntry>
            <Value>0</Value>
        </Enumeration>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestPropertyAccess")

        MyName = Camera.GetNode("MyName")

        self.assertEqual(RW, MyName.GetAccessMode())
        self.assertEqual("MyName", MyName.Node.GetName())
        self.assertEqual("Std::MyName", MyName.Node.GetName(True))
        self.assertEqual(Standard, MyName.Node.GetNameSpace())
        self.assertEqual("MyDisplayName", MyName.Node.GetDisplayName())
        self.assertEqual(Guru, MyName.Node.GetVisibility())
        self.assertEqual("MyToolTip", MyName.Node.GetToolTip())
        self.assertEqual("MyDescription", MyName.Node.GetDescription())

    def test_CachingMode(self):

        """[ GenApiTest@NodeTestSuite_TestCachingMode.xml|gxml
    
     <IntReg Name="Int01" >
       <Address>0x10</Address>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>NoCache</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int02" >
       <Address>0x12</Address>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteThrough</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int03" >
       <Address>0x14</Address>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteAround</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int04" >
       <pAddress>Int01</pAddress>    <!--  note: a connection to a node with NoCache -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteAround</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int05" >
       <pAddress>Int02</pAddress>   <!--  note: a connection to a node with WriteThrough -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteAround</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int06" >
       <pAddress>Int03</pAddress>   <!--  note: a connection to a node with WriteAround -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteAround</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int07" >
       <pAddress>Int01</pAddress>    <!--  note: a connection to a node with NoCache -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteThrough</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int08" >
       <pAddress>Int02</pAddress>   <!--  note: a connection to a node with WriteThrough -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteThrough</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int09" >
       <pAddress>Int03</pAddress>    <!--  note: a connection to a node with WriteAround -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Cachable>WriteThrough</Cachable>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int10" >  <!--  note : no explicite CachingMode given -->
       <Address>0</Address>
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

     <IntReg Name="Int11" >
       <pAddress>Int10</pAddress>   <!--  note: a connection to a node with implicite WriteThrough -->
       <Length>2</Length>
       <AccessMode>RW</AccessMode>
       <pPort>MyPort</pPort>
       <Sign>Unsigned</Sign>
       <Endianess>LittleEndian</Endianess>
     </IntReg>

        <Integer Name="IntNoCache">
        <pValue>Int01</pValue>
        </Integer>

        <Integer Name="IntThrough">
        <pValue>Int02</pValue>
        </Integer>

        <Integer Name="IntAround">
        <pValue>Int03</pValue>
        </Integer>

        <Converter Name="ConvAround">
            <FormulaTo> FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
            <pValue>Int03</pValue>
            <Slope>Increasing</Slope>
        </Converter>

        <Float Name="FloatAround">
        <pValue>ConvAround</pValue>
        </Float>

     <Port Name="MyPort"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestCachingMode")

        Int01 = Camera.GetNode("Int01")
        Int02 = Camera.GetNode("Int02")
        Int03 = Camera.GetNode("Int03")
        Int04 = Camera.GetNode("Int04")
        Int05 = Camera.GetNode("Int05")
        Int06 = Camera.GetNode("Int06")
        Int07 = Camera.GetNode("Int07")
        Int08 = Camera.GetNode("Int08")
        Int09 = Camera.GetNode("Int09")
        Int10 = Camera.GetNode("Int10")
        Int11 = Camera.GetNode("Int11")

        self.assertEqual(genicam.NoCache, Int01.Node.GetCachingMode())
        self.assertEqual(genicam.WriteThrough, Int02.Node.GetCachingMode())
        self.assertEqual(genicam.WriteAround, Int03.Node.GetCachingMode())
        self.assertEqual(genicam.NoCache, Int04.Node.GetCachingMode())
        self.assertEqual(genicam.WriteAround, Int05.Node.GetCachingMode())
        self.assertEqual(genicam.WriteAround, Int06.Node.GetCachingMode())
        self.assertEqual(genicam.NoCache, Int07.Node.GetCachingMode())
        self.assertEqual(genicam.WriteThrough, Int08.Node.GetCachingMode())
        self.assertEqual(genicam.WriteAround, Int09.Node.GetCachingMode())
        # ensure that the default caching mode is WriteThrough (single node)
        self.assertEqual(genicam.WriteThrough, Int10.Node.GetCachingMode())
        # ensure that the default caching mode is WriteThrough (for both, child and parent node, there is no caching mode specified
        self.assertEqual(genicam.WriteThrough, Int11.Node.GetCachingMode())

        # create and initialize a test port
        Port = CTestPort()
        #    short s = (short)0xfdfd # *JS* removed warning
        s = 0xfdfd
        Port.CreateEntry(0x0010, "uint16_t", s, RW, LittleEndian)
        Port.CreateEntry(0x0012, "uint16_t", s, RW, LittleEndian)
        Port.CreateEntry(0x0014, "uint16_t", s, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        # No cache
        Int = Int01
        Int.SetValue(42)
        self.assertEqual(42, Int.GetValue())
        # Write through
        Int = Int02
        n1 = 4711
        Int.SetValue(n1)
        self.assertEqual(n1, Int.GetValue())
        # Write around
        Int = Int03
        n2 = 123
        Int.SetValue(n2)
        self.assertEqual(n2, Int.GetValue())

        # Let's play directly with the values within the port
        NoCache = Camera.GetNode("Int01")
        Through = Camera.GetNode("Int02")
        Around = Camera.GetNode("Int03")
        self.assertEqual(genicam.NoCache, NoCache.GetNode().GetCachingMode())
        self.assertEqual(genicam.WriteThrough, Through.GetNode().GetCachingMode())
        self.assertEqual(genicam.WriteAround, Around.GetNode().GetCachingMode())
        IntNoCache = Camera.GetNode("IntNoCache")
        IntThrough = Camera.GetNode("IntThrough")
        IntAround = Camera.GetNode("IntAround")
        NoCache.SetValue(0)
        Through.SetValue(0)
        Around.SetValue(0)
        self.assertEqual(0, NoCache.GetValue())
        self.assertEqual(0, Around.GetValue())
        self.assertEqual(0, Through.GetValue())
        self.assertEqual(0, IntNoCache.GetValue())
        self.assertEqual(0, IntAround.GetValue())
        self.assertEqual(0, IntThrough.GetValue())

        # Volatile change of value is visible only to NoCache nodes
        Value = 1
        Port.Write(0x10, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x12, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x14, cast_data("uint16_t", LittleEndian, Value))
        self.assertEqual(1, NoCache.GetValue())
        self.assertEqual(0, Around.GetValue())
        self.assertEqual(0, Through.GetValue())
        Value = 2
        Port.Write(0x10, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x12, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x14, cast_data("uint16_t", LittleEndian, Value))
        self.assertEqual(2, IntNoCache.GetValue())
        self.assertEqual(0, IntAround.GetValue())
        self.assertEqual(0, IntThrough.GetValue())
        # Adapting the value after writing is visible to all but WriteThrough node
        NoCache.SetValue(3)
        Through.SetValue(3)
        Around.SetValue(3)
        Value = 4
        Port.Write(0x10, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x12, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x14, cast_data("uint16_t", LittleEndian, Value))

        self.assertEqual(4, NoCache.GetValue())
        self.assertEqual(4, Around.GetValue())
        self.assertEqual(3, Through.GetValue())
        IntNoCache.SetValue(5)
        IntThrough.SetValue(5)
        IntAround.SetValue(5)
        Value = 6
        Port.Write(0x10, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x12, cast_data("uint16_t", LittleEndian, Value))
        Port.Write(0x14, cast_data("uint16_t", LittleEndian, Value))

        self.assertEqual(6, IntNoCache.GetValue())
        self.assertEqual(6, IntAround.GetValue())
        self.assertEqual(5, IntThrough.GetValue())
        # make sure the cache is avoided if the write fails
        Through.SetValue(7)
        with self.assertRaises(OutOfRangeException):
            Through.SetValue(0xFFFFFFFF)
        self.assertEqual(7, Through.GetValue())
        Through.SetValue(7)
        with self.assertRaises(OutOfRangeException):
            Through.SetValue(0xFFFFFFFF)
        self.assertEqual(7, Through.GetValue())

        # repeat the write-around tests also with float
        FloatAround = Camera.GetNode("FloatAround")
        FloatAround.SetValue(50.0)
        Value = 60
        Port.Write(0x14, cast_data("uint16_t", LittleEndian, Value))

        self.assertAlmostEqual(60.0, FloatAround.GetValue(), delta=(7. / 3 - 4. / 3 - 1))

    def test_DeviceInformation(self):

        """[ GenApiTest@NodeTestSuite_TestDeviceInformation.xml|gxml
            <Node Name="Dummy"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestDeviceInformation")

        # CDeviceInfoPtr DeviceInfo(Camera._Ptr)

        # Version_t Version
        # DeviceInfo.GetDeviceVersion(Version)
        # self.assertEqual( 3, Version.Major )
        # self.assertEqual( 0, Version.Minor )
        # self.assertEqual( 0, Version.SubMinor )

        # uint16_t Build
        # DeviceInfo.GetGenApiVersion(Version, Build)
        # self.assertEqual( GENICAM_VERSION_MAJOR, Version.Major )
        # self.assertEqual( GENICAM_VERSION_MINOR, Version.Minor )
        # self.assertEqual( GENICAM_VERSION_SUBMINOR, Version.SubMinor )
        # self.assertEqual( GENICAM_VERSION_BUILD, Build )

        # DeviceInfo.GetSchemaVersion(Version)
        # switch(GenApiSchemaVersion)
        # {
        # case v1_0:
        #    self.assertEqual( 1, Version.Major )
        #    self.assertEqual( 0, Version.Minor )
        #    self.assertEqual( 1, Version.SubMinor )
        #    break
        # case v1_1:
        #    self.assertEqual( 1, Version.Major )
        #    self.assertEqual( 1, Version.Minor )
        #    self.assertEqual( 0, Version.SubMinor )
        #    break
        # default:
        #    self.assertTrue(False)
        # }
        # self.assertEqual( "NodeTestSuite_TestDeviceInformation", DeviceInfo.GetModelName() )
        # self.assertEqual( "GenApiTest", DeviceInfo.GetVendorName() )
        # self.assertEqual( "2D932CC6-EB68-40bd-B6CC-F03B55B7D653", DeviceInfo.GetProductGuid() )
        # self.assertEqual( "02A8C268-BEE8-463b-A6C0-53ED8256E3D8", DeviceInfo.GetVersionGuid() )
        # self.assertEqual( "XML file extracted from test code", DeviceInfo.GetToolTip() )
        # self.assertEqual( "GEV", DeviceInfo.GetStandardNameSpace() )

    def test_TheRest(self):
        """[ GenApiTest@NodeTestSuite_TestTheRest.xml|gxml
    
             <IntReg Name="IntChild" >
             <Address>0</Address>
             <Length>2</Length>
             <AccessMode>RW</AccessMode>
             <pPort>MyPort</pPort>
             <Sign>Unsigned</Sign>
             <Endianess>LittleEndian</Endianess>
             </IntReg>
             <IntReg Name="IntParent" >
             <pAlias>IntChild</pAlias>
             <pAddress>IntChild</pAddress>
             <Length>2</Length>
             <AccessMode>RW</AccessMode>
             <pPort>MyPort</pPort>
             <Sign>Unsigned</Sign>
             <Endianess>LittleEndian</Endianess>
             </IntReg>
             <Port Name="MyPort"/>
    
             """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestTheRest")

        IntChild = Camera.GetNode("IntChild")
        IntParent = Camera.GetNode("IntParent")

        # NodeList_t NodeList
        # IntChild.GetParents(NodeList)
        print("Parents\n")
        # for (NodeList_t::iterator itParent = NodeList.begin() itParent != NodeList.end() itParent++)
        # {
        #    print("- " , (*itParent).GetName() , "\n")
        # }
        # self.assertTrue(NodeList.size() == 1)
        # self.assertEqual("IntParent", NodeList[0].GetName())

        # CNodeMapPtr NodeMap = IntChild.GetNodeMap()

        self.assertEqual("IntChild", IntParent.Node.GetAlias().Node.GetName())
        with self.assertRaises(LogicalErrorException):
            IntChild.Node.GetAlias()


            # const void * pSelf = &Camera

            # NodeList_t allnodes
            # Camera.GetNodes(allnodes)
            # for (NodeList_t::const_iterator itNode = allnodes.begin(), endNode = allnodes.end() itNode != endNode ++itNode)
            # {
            #    IUserData pUserData.SetValue(dynamic_cast<IUserData*>(*itNode))
            #    CNodeUserDataPtr UserData(*itNode)

            # self.assertTrue(None != pUserData, "Interface IUserData is not implemented.")
            # self.assertTrue(None == pUserData.GetUserData(), "UserData is not initialized correctly.")
            # self.assertTrue(None == pUserData.SetUserData(None), "UserData")
            # self.assertTrue(None == (void*)pUserData.SetUserData((UserData_t)pSelf), "UserData returned unexpected value.")
            # self.assertTrue(pSelf == (void*)pUserData.GetUserData(), "UserData returned unexpected value.")

            # self.assertTrue(pSelf == UserData.GetUserData(), "UserData returned unexpected value.")
            # self.assertTrue(pSelf == UserData.SetUserData(None), "UserData returned unexpected value.")

    def test_StringConversions(self):
        """[ GenApiTest@NodeTestSuite_TestStringConversions.xml|gxml
    
        <Integer Name="TestInt">
            <Value>0</Value>
        </Integer>
    
        <Register Name="TestReg">
            <Address>0x0000</Address>
            <Length>1</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <Register Name="TestReg2L">
            <Address>0x0110</Address>
            <Length>2</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <Register Name="TestReg2B">
            <Address>0x0120</Address>
            <Length>2</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <Register Name="TestRegBig">
            <Address>0x0130</Address>
            <Length>128</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestStringConversions")

        Int = Camera.GetNode("TestInt")

        RegVal = 0
        RegVal2L = 0
        RegVal2B = 0
        BigRegVal = "\0" * 128

        Port = CTestPort()
        Port.CreateEntry(0x0000, "uint8_t", RegVal, RW, LittleEndian)
        Port.CreateEntry(0x0110, "uint16_t", RegVal2L, RW, LittleEndian)
        Port.CreateEntry(0x0120, "uint16_t", RegVal2B, RW, LittleEndian)
        Port.CreateEntry(0x0130, "str128", BigRegVal, RW, LittleEndian)
        Camera._Connect(Port, "Port")

        Register = Camera.GetNode("TestReg")
        Register2L = Camera.GetNode("TestReg2L")
        Register2B = Camera.GetNode("TestReg2B")
        BigRegister = Camera.GetNode("TestRegBig")

        self.assertEqual(intfIRegister, Register.Node.GetPrincipalInterfaceType())

        # test options not yet covered by other tests
        Int.FromString("0X100")
        self.assertEqual(0x100, Int.GetValue())
        Int.FromString("0x200")
        self.assertEqual(0x200, Int.GetValue())
        # and the old '&h' options, no more supported
        with self.assertRaises(InvalidArgumentException):
            Int.FromString("&h1")
        with self.assertRaises(InvalidArgumentException):
            Int.FromString("&HFF")
        with self.assertRaises(InvalidArgumentException):
            Int.FromString("&FFF")

        # the same for byte arrays
        self.assertEqual("0x00", Register.ToString())
        bigRegisterStr = BigRegister.ToString()
        self.assertEqual(2 + 2 * len(BigRegVal), len(bigRegisterStr))
        self.assertEqual("0x00", bigRegisterStr[0:4])
        # for i in range(1, sys.getsizeof(BigRegVal)):
        #    self.assertEqual( "00", bigRegisterStr.substr(2*(i+1),2) )


        # single byte register, including some invalid strings
        # (the string should start with 0x following by one or more pairs of hexa-digits)
        with self.assertRaises(InvalidArgumentException):
            Register.FromString("1")
        with self.assertRaises(InvalidArgumentException):
            Register.FromString("0x")
        with self.assertRaises(InvalidArgumentException):
            Register.FromString("0x1")
        with self.assertRaises(InvalidArgumentException):
            Register.FromString("0x123")

        Register.FromString("0xAB")
        # Register.Get((uint8_t*)&RegVal, sizeof(RegVal))
        # self.assertEqual( 0xAB, RegVal )
        self.assertEqual("0xab", Register.ToString())

        # 2-byte registers, both little and big endian
        Register2L.FromString("0xaabb")
        # Register2L.Get((uint8_t*)&RegVal2L, sizeof(RegVal2L))
        # self.assertEqual( 0xBBAA, RegVal2L )
        self.assertEqual("0xaabb", Register2L.ToString())

        Register2B.FromString("0xaabb")
        # Register2B.Get((uint8_t*)&RegVal2B, sizeof(RegVal2B))
        # self.assertEqual( 0xBBAA, RegVal2B )
        self.assertEqual("0xaabb", Register2B.ToString())

    def test_Bool(self):

        """[ GenApiTest@NodeTestSuite_TestBool.xml|gxml
    
              <Node Name="Node">
            <pIsImplemented>Implemented</pIsImplemented>
            <pIsAvailable>Available</pIsAvailable>
            <pIsLocked>Locked</pIsLocked>
        </Node>

        <Boolean Name="Implemented">
            <Value>true</Value>
        </Boolean>

        <Boolean Name="Available">
            <Value>true</Value>
        </Boolean>

        <Boolean Name="Locked">
            <Value>false</Value>
        </Boolean>

    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestBool")

        Node = Camera.GetNode("Node")
        Implemented = Camera.GetNode("Implemented")
        Available = Camera.GetNode("Available")
        Locked = Camera.GetNode("Locked")

        # Check Implemented
        Implemented.SetValue(False)
        self.assertEqual(NI, Node.GetAccessMode())
        Implemented.SetValue(True)

        # Check Available
        Available.SetValue(False)
        self.assertEqual(NA, Node.GetAccessMode())
        Available.SetValue(True)

        # Check Locked
        Locked.SetValue(True)
        self.assertEqual(RO, Node.GetAccessMode())
        Locked.SetValue(False)

    def test_ImposeAccessMode(self):
        TestRegCb = CallbackObject()
        """[ GenApiTest@NodeTestSuite_TestImposeAccessMode.xml|gxml
    
            <Integer Name="TestInt">
                <Value>0</Value>
            </Integer>
    
            <Register Name="TestReg">
                <Address>0x0000</Address>
                <Length>1</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
            </Register>
            <Category Name="Root">
                 <pFeature>TestInt</pFeature>
            </Category>
    
            <Port Name="Port"/>
        """

        Camera = CNodeMapRef()
        Port = CTestPort()

        # now initialize map
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestImposeAccessMode")
        Camera._Connect(Port, "Port")

        # test the access mode
        Value = Camera.GetNode("TestReg")
        Register(Value.Node, TestRegCb.Callback)
        self.assertEqual(RW, Value.GetAccessMode(), "Expected Imposed Access mode is taken in account.")
        self.assertEqual(RW, Value.GetAccessMode(), "Expected Imposed Access mode is taken in account.")
        Value.Node.ImposeAccessMode(RO)
        self.assertEqual(1, TestRegCb.Count(), "Callback not fired by ImposeAccessMode.")
        self.assertEqual(RO, Value.GetAccessMode(), "Expected Imposed Access mode is taken in account.")
        self.assertEqual(RO, Value.GetAccessMode(), "Expected Imposed Access mode is taken in account.")

    def test_Const(self):
        """[ GenApiTest@NodeTestSuite_TestConst.xml|gxml
    
            <Integer Name="TestInt">
                <Value>0</Value>
            </Integer>
    
            <Register Name="TestReg">
                <Address>0x0000</Address>
                <Length>1</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
            </Register>
            <Category Name="Root">
                 <pFeature>TestInt</pFeature>
            </Category>
    
            <Port Name="Port"/>
        """

        Camera = CNodeMapRef()
        Port = CTestPort()

        # now test initialized map
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestConst")
        Camera._Connect(Port, "Port")

        # node pointer
        pNode = Camera.GetNode("Root")
        if IsReadable(pNode):
            pass
        elif IsWritable(pNode):
            pass
        elif IsAvailable(pNode):
            pass
        elif IsImplemented(pNode):
            pass
        else:
            self.assertTrue(False, "unexpected AccessMode")

        # node reference
        Node = Camera.GetNode("Port")
        # const INode& rNode = *Node
        # if (IsReadable( rNode ))
        # else if (IsWritable( rNode ))
        # else if (IsAvailable( rNode ))
        # else if (IsImplemented( rNode ))
        # else self.assertTrue( 0 && "unexpected AccessMode" )

    def test_ReadOnlyPort(self):
        """[ GenApiTest@NodeTestSuite_TestReadOnlyPort.xml|gxml
    
            <Register Name="TestReg">
                <Address>0x0000</Address>
                <Length>1</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
            </Register>
    
            <Port Name="Port"/>
        """

        Camera = CNodeMapRef()

        # Extended Test Port declaring that read access is allowed only.
        class CReadonlyTestPort(CTestPort):
            def GetAccessMode(self):
                return RO

        Port = CReadonlyTestPort()
        # Initial register value
        RegVal = 0xcd
        Port.CreateEntry(0x0000, "uint8_t", RegVal, RW, LittleEndian)

        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestReadOnlyPort")
        Camera._Connect(Port, "Port")
        self.assertEqual(RO, Port.GetAccessMode())

        Reg = Camera.GetNode("TestReg")
        CurRegVal = 0xff
        self.assertEqual(RO, Reg.GetAccessMode(), "Access mode is not R0!")
        with self.assertRaises(AccessException):
            Reg.Set(cast_data("uint8_t", LittleEndian, CurRegVal))

        CurRegVal = cast_buffer("uint8_t", LittleEndian, Reg.Get(sizeof("uint8_t")))
        self.assertEqual(RegVal, CurRegVal)

    def test_URL(self):

        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@NodeTestSuite_TestURL.xml|gxml
    
        <Node Name="TheNodeA">
            <DocuURL><![CDATA[http://www.mycompany.com/docu/MyCamera.pdf#MyFeature]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeB">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?Feature=$(Sys::NodeName)&Value=$(Value)]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeC">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?Vendor=$(Sys::VendorName)&Model=$(Sys::ModelName)&GenApiVersion=$(Sys::GenApiVersion)&DeviceVersion=$(Sys::DeviceVersion)&SchemaVersion=$(Sys::SchemaVersion)]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeD">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?Unk1=$(Sys::NotKnown)&Unk=$(Bla)]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeE">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?App=$(Sys::Application)&OS=$(Sys::OperatingSystem)&Language=$(Sys::Language)]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeF">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?Namespace=$(Sys::StandardNamespace)]]></DocuURL>
        </Node>
    
        <Node Name="TheNodeG">
            <DocuURL><![CDATA[http://www.mycompany.com/docu.php?MissingBracket=$(Sys::StandardNamespace]]></DocuURL>
        </Node>
    
        <Integer Name="Value">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestURL")

        TheNodeA = Camera.GetNode("TheNodeA").Node
        self.assertEqual("http://www.mycompany.com/docu/MyCamera.pdf#MyFeature", TheNodeA.GetDocuURL())
        print(TheNodeA.GetDocuURL(), "\n")

        TheNodeB = Camera.GetNode("TheNodeB").Node
        self.assertEqual("http://www.mycompany.com/docu.php?Feature=TheNodeB&Value=10", TheNodeB.GetDocuURL())
        print(TheNodeB.GetDocuURL(), "\n")

        print(Camera.GetDeviceInfo().GetGenApiVersion())

        TheNodeC = Camera.GetNode("TheNodeC").Node
        version, build = Camera.DeviceInfo.GetGenApiVersion()
        print(TheNodeC.GetDocuURL(), "\n")
        self.assertEqual(
            "http://www.mycompany.com/docu.php?Vendor=GenApiTest&Model=NodeTestSuite_TestURL.xml&GenApiVersion="
            + str(version.Major) + "."
            + str(version.Minor) + "."
            + str(version.SubMinor) +
            "&DeviceVersion=3.0.0&SchemaVersion=1.1.0", TheNodeC.GetDocuURL())
        print(TheNodeC.GetDocuURL(), "\n")

        TheNodeD = Camera.GetNode("TheNodeD").Node
        self.assertEqual("http://www.mycompany.com/docu.php?Unk1=Unknown&Unk=Unknown", TheNodeD.GetDocuURL())
        print(TheNodeD.GetDocuURL(), "\n")

        TheNodeE = Camera.GetNode("TheNodeE").Node
        print("!!!!!! Check manually : ", TheNodeE.GetDocuURL(), "\n")
        self.assertTrue("python.exe" in TheNodeE.GetDocuURL() or "python" in TheNodeE.GetDocuURL())

        TheNodeF = Camera.GetNode("TheNodeF").Node
        self.assertEqual("http://www.mycompany.com/docu.php?Namespace=GEV", TheNodeF.GetDocuURL())
        print(TheNodeF.GetDocuURL(), "\n")

        TheNodeG = Camera.GetNode("TheNodeG").Node
        self.assertEqual("http://www.mycompany.com/docu.php?MissingBracket=$(Sys::StandardNamespace",
                         TheNodeG.GetDocuURL())

        # note that GenICam does not care if the URL makes sense 
        print(TheNodeG.GetDocuURL(), "\n")

    def test_Deprecated(self):

        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@NodeTestSuite_TestDeprecated.xml|gxml

            <Node Name="TheNode"/>

            <Node Name="TheDeprecatedNode">
              <IsDeprecated>Yes</IsDeprecated>
            </Node>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestDeprecated")

        TheNode = Camera.GetNode("TheNode")
        TheDeprecatedNode = Camera.GetNode("TheDeprecatedNode")
        self.assertEqual(False, TheNode.Node.IsDeprecated())
        self.assertEqual(True, TheDeprecatedNode.Node.IsDeprecated())

    def test_StructReg(self):
        """[ GenApiTest@NodeTestSuite_TestStructReg.xml|gxml
    
            <StructReg Comment="MyStruct">
               <Address>2</Address>
               <Length>2</Length>
               <AccessMode>RW</AccessMode>
               <pPort>MyPort</pPort>
               <Endianess>BigEndian</Endianess>
               <StructEntry Name="Bit0" NameSpace="Custom">
                  <Bit>0</Bit>
               </StructEntry>
               <StructEntry Name="Bit1" NameSpace="Custom">
                  <Bit>1</Bit>
               </StructEntry>
               <StructEntry Name="Bit2" NameSpace="Custom">
                  <Bit>2</Bit>
               </StructEntry>
            </StructReg>
    
            <Port Name="MyPort"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestStructReg")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x02, "uint32_t", 0xFFFFFFFF, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        Bit0 = Camera.GetNode("Bit0")
        self.assertTrue(bool(Bit0))
        Bit1 = Camera.GetNode("Bit1")
        self.assertTrue(bool(Bit1))
        Bit2 = Camera.GetNode("Bit2")
        self.assertTrue(bool(Bit2))
        Bit0 = Bit0.GetValue()
        Bit1 = Bit1.GetValue()
        Bit2 = Bit2.GetValue()
        self.assertEqual(1, Bit0)
        self.assertEqual(1, Bit1)
        self.assertEqual(1, Bit2)

    def test_Extension(self):
        """[ GenApiTest@NodeTestSuite_TestExtension.xml|gxml
    
        <Node Name="CatNode">
           <Extension>
               <MyFavourite>123</MyFavourite>
               <AnotherNode>
                   <WithSubNode>bla</WithSubNode>
                   <WithSubNode>blub</WithSubNode>
               </AnotherNode>
           </Extension>
        </Node>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestExtension")

    def test_AccessModeCache(self):
        Port = CTestPort()
        RegisterA = 0
        RegisterB = 0
        Port.CreateEntry(0x4000, "uint32_t", RegisterA, RW, LittleEndian)
        Port.CreateEntry(0x4004, "uint32_t", RegisterB, RW, LittleEndian)

        """[ GenApiTest@NodeTestSuite_TestAccessModeCache.xml|gxml
    
            <IntReg Name="A">
               <Address>0x4000</Address>
               <Length>4</Length>
               <AccessMode>RO</AccessMode>
               <pPort>MyPort</pPort>
               <Cachable>NoCache</Cachable>
               <Sign>Unsigned</Sign>
               <Endianess>BigEndian</Endianess>
            </IntReg>
    
            <IntReg Name="B">
               <Address>0x4004</Address>
               <Length>4</Length>
               <AccessMode>RO</AccessMode>
               <pPort>MyPort</pPort>
               <Cachable>NoCache</Cachable>
               <Sign>Unsigned</Sign>
               <Endianess>BigEndian</Endianess>
            </IntReg>
    
            <IntSwissKnife Name="C">
               <pVariable Name="VAR_A">A</pVariable>
               <pVariable Name="VAR_B">B</pVariable>
               <Formula>(VAR_A + VAR_B) > 0</Formula>
            </IntSwissKnife>
    
            <Integer Name="D">
               <pIsAvailable>C</pIsAvailable>
               <Value>0</Value>
            </Integer>
    
            <Float Name="E">
               <pIsAvailable>C</pIsAvailable>
               <Value>0</Value>
            </Float>
    
            <Command Name="F">
               <pIsAvailable>C</pIsAvailable>
               <pValue>Helper</pValue>
               <CommandValue>1</CommandValue>
            </Command>
    
            <IntSwissKnife Name="G">
               <pIsAvailable>C</pIsAvailable>
               <Formula>0</Formula>
            </IntSwissKnife>
    
            <SwissKnife Name="H">
               <pIsAvailable>C</pIsAvailable>
               <Formula>0</Formula>
            </SwissKnife>
    
            <Enumeration Name="I">
               <pIsAvailable>C</pIsAvailable>
                <EnumEntry Name="EnumValue1">
                    <Value>0</Value>
               </EnumEntry>
               <Value>0</Value>
            </Enumeration>
    
            <Port Name="J">
               <pIsAvailable>C</pIsAvailable>
            </Port>
    
            <Register Name="K">
               <pIsAvailable>C</pIsAvailable>
                <Address>0</Address>
                <Length>1</Length>
                <AccessMode>RW</AccessMode>
                <pPort>MyPort</pPort>
            </Register>
    
            <Boolean Name="L">
               <pIsAvailable>C</pIsAvailable>
               <Value>0</Value>
            </Boolean>
    
            <Enumeration Name="M">
                <EnumEntry Name="EnumValue1">
                   <pIsAvailable>C</pIsAvailable>
                    <Value>0</Value>
               </EnumEntry>
               <Value>0</Value>
            </Enumeration>
    
            <Integer Name="N">
               <pIsImplemented>C</pIsImplemented>
               <Value>0</Value>
            </Integer>
    
            <Integer Name="O">
               <pIsLocked>C</pIsLocked>
               <Value>0</Value>
            </Integer>
    
            <Integer Name="P">
               <pValue>D</pValue>
            </Integer>
    
            <IntSwissKnife Name="isk">
               <pVariable Name="VAR_A">A</pVariable>
               <pVariable Name="VAR_B">B</pVariable>
               <Formula>VAR_A + VAR_B</Formula>
            </IntSwissKnife>
    
            <SwissKnife Name="fsk">
               <pVariable Name="VAR_A">A</pVariable>
               <pVariable Name="VAR_B">B</pVariable>
               <Formula>VAR_A + VAR_B</Formula>
            </SwissKnife>
    
            <IntConverter Name="ic">
               <pVariable Name="VAR_A">A</pVariable>
               <pVariable Name="VAR_B">B</pVariable>
               <FormulaTo>0</FormulaTo>
               <FormulaFrom>VAR_A + VAR_B</FormulaFrom>
               <pValue>Helper</pValue>
            </IntConverter>
    
            <Converter Name="fc">
               <pVariable Name="VAR_A">A</pVariable>
               <pVariable Name="VAR_B">B</pVariable>
               <FormulaTo>0</FormulaTo>
               <FormulaFrom>VAR_A + VAR_B</FormulaFrom>
               <pValue>Helper</pValue>
            </Converter>
    
            <Integer Name="Helper">
               <ImposedAccessMode>WO</ImposedAccessMode>
               <Value>0</Value>
            </Integer>
    
            <Port Name="MyPort"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestAccessModeCache")
        Camera._Connect(Port, "MyPort")

        # (connect also the other tested port)
        PortJ = CTestPort()
        Camera._Connect(PortJ, "J")

        lA = Camera.GetNode("A")
        lB = Camera.GetNode("B")
        lD = Camera.GetNode("D")
        lE = Camera.GetNode("E")
        lF = Camera.GetNode("F")
        lG = Camera.GetNode("G")
        lH = Camera.GetNode("H")
        lI = Camera.GetNode("I")
        lJ = Camera.GetNode("J")
        lK = Camera.GetNode("K")
        lL = Camera.GetNode("L")
        lM = Camera.GetNode("M")
        lN = Camera.GetNode("N")
        lO = Camera.GetNode("O")
        lP = Camera.GetNode("P")

        # Validate registers initial state
        self.assertTrue(lA.GetValue() == 0)
        self.assertTrue(lB.GetValue() == 0)

        # Validate expected original access mode: NA.
        # Required as it populates the access mode cache.
        self.assertTrue(not IsAvailable(lD.GetAccessMode()))
        self.assertTrue(not IsAvailable(lE.GetAccessMode()))
        self.assertTrue(not IsAvailable(lF.GetAccessMode()))
        self.assertTrue(not IsAvailable(lG.GetAccessMode()))
        self.assertTrue(not IsAvailable(lH.GetAccessMode()))
        self.assertTrue(not IsAvailable(lI.GetAccessMode()))
        self.assertTrue(not IsAvailable(lJ.GetAccessMode()))
        self.assertTrue(not IsAvailable(lK.GetAccessMode()))
        self.assertTrue(not IsAvailable(lL.GetAccessMode()))
        self.assertTrue(not IsAvailable(lM.GetAccessMode()))
        self.assertTrue(not IsImplemented(lN.GetAccessMode()))
        self.assertTrue(IsWritable(lO.GetAccessMode()))
        self.assertTrue(not IsAvailable(lP.GetAccessMode()))

        # Directly change A value
        lNewAVal = 4
        lAccessA = RW  # Out, irrelevant
        Port.UpdateEntry(0x4000, cast_data("uint32_t", LittleEndian, lNewAVal), lAccessA)

        # Directly change B value
        lNewBVal = 2
        lAccessB = RW  # Out, irrelevant
        Port.UpdateEntry(0x4004, cast_data("uint32_t", LittleEndian, lNewBVal), lAccessB)

        # Now the big test - with 0000378 fixed, should pass
        self.assertTrue(IsAvailable(lD.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lE.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lF.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lG.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lH.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lI.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lJ.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lK.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lL.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lM.Node.GetAccessMode()))
        self.assertTrue(IsImplemented(lN.Node.GetAccessMode()))
        self.assertTrue(not IsWritable(lO.Node.GetAccessMode()))
        self.assertTrue(IsAvailable(lP.Node.GetAccessMode()))

        isk = Camera.GetNode("isk")
        fsk = Camera.GetNode("fsk")
        ic = Camera.GetNode("ic")
        fc = Camera.GetNode("fc")
        self.assertEqual(NoCache, isk.GetNode().GetCachingMode())
        self.assertEqual(NoCache, fsk.GetNode().GetCachingMode())
        self.assertEqual(NoCache, ic.GetNode().GetCachingMode())
        self.assertEqual(NoCache, fc.GetNode().GetCachingMode())

    def test_IsUncached(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@NodeTestSuite_TestIsUncached.xml|gxml
    
            <Integer Name="Value">
                <pValue>ValueReg</pValue>
            </Integer>
    
            <IntReg Name="ValueReg">
                <pBlockPolling>PollingDisabler</pBlockPolling>
                <Address>0x0000</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <PollingTime>1000</PollingTime>
                <Sign>Unsigned</Sign>
                <Endianess>LittleEndian</Endianess>
            </IntReg>
    
            <Integer Name="PollingDisabler">
                <pIsAvailable>PollingDisablerAvail</pIsAvailable>
                <Value>0</Value>
            </Integer>
    
            <Integer Name="PollingDisablerAvail">
                <Value>1</Value>
            </Integer>
    
            <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestIsUncached")

        # type definition of TestIsUncached is above
        regs = [("Value", "uint32_t", 0, RW, LittleEndian), ]

        Port = CStructTestPort(regs)

        self.assertEqual(intfIPort, Port.GetPrincipalInterfaceType())
        Port.Value = 42
        Camera._Connect(Port, "Port")

        Value = Camera.GetNode("Value")
        ValueReg = Camera.GetNode("ValueReg")
        PollingDisabler = Camera.GetNode("PollingDisabler")
        PollingDisablerAvail = Camera.GetNode("PollingDisablerAvail")

        self.assertEqual(42, Value.GetValue())

        # Change register value since the register is cached the Value node will not notice...
        Port.Value = 13
        self.assertEqual(42, Value.GetValue())

        # ...until the register is polled
        Camera._Poll(2000)
        self.assertEqual(13, Value.GetValue())

        # Now we do it again but first we block the polling
        Port.Value = 42
        PollingDisabler.SetValue(1)
        # setting the disabler invalidates the nodes so we have to fill the caches again by reading the Value
        self.assertEqual(42, Value.GetValue())

        # Change register value since the register is cached the Value node will not notice...
        Port.Value = 13
        self.assertEqual(42, Value.GetValue())

        # ...until the register is polled
        Camera._Poll(2000)
        # But the polling didn't happen so the cached value is still valid
        self.assertEqual(42, Value.GetValue())

        # If we invalidate the Value node explicitly...
        Value.GetNode().InvalidateNode()
        # ...nothing happens because the cache of the register node was not invalidated
        self.assertEqual(42, Value.GetValue())

        # However if we invalidate the ValueReg node explicitely...
        ValueReg.GetNode().InvalidateNode()
        # ... we finally get the value
        self.assertEqual(13, Value.GetValue())

        # now make the disabler unreadable and repeate similar tests
        PollingDisablerAvail.SetValue(0)
        self.assertTrue(not IsAvailable(Value))  ## is this expected?

    #
    #     struct MyCallbackUtility
    #     {
    #         static void Reset() { m_Count=0 }
    #         static void Callback( INode* ) { ++m_Count }
    #         static uint32_t Count() { return m_Count }
    #     private:
    #         static unsigned m_Count
    #     }
    #     unsigned MyCallbackUtility::m_Count=0
    #
    #

    def test_WriteCache(self):
        """[ GenApiTest@NodeTestSuite_TestWriteCache.xml|gxml
    
        <Boolean Name="IOBit">
           <pValue>IOBitInteger</pValue>
        </Boolean>

        <Integer Name="IOBitSelector">
           <Value>0</Value>
           <Min>0</Min>
           <Max>7</Max>
        </Integer>

        <IntConverter Name="IOBitInteger">
           <pVariable Name="SEL">IOBitSelector</pVariable>
           <pVariable Name="CUR">IORegister</pVariable>
        <!--   To = From ? CUR | 1 << SEL : CUR & ~(1 << SEL) -->
           <FormulaTo>(FROM) ? (CUR | (1 &lt;&lt; SEL)) : (CUR &amp; (~ (1 &lt;&lt; SEL)))</FormulaTo>
        <!--   From = To >> SEL & 1 -->
           <FormulaFrom>(TO &gt;&gt; SEL) &amp; 1</FormulaFrom>
           <pValue>IORegister</pValue>
           <Slope>Varying</Slope>
        </IntConverter>

        <IntReg Name="IORegister">
           <Address>0x00000000</Address>
           <Length>1</Length>
           <AccessMode>RW</AccessMode>
           <pPort>Device</pPort>
           <Cachable>WriteThrough</Cachable>
           <Sign>Unsigned</Sign>
           <Endianess>LittleEndian</Endianess>
        </IntReg>

        <Port Name="Device" >
        </Port>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestWriteCache")

        regs = [("bit", "uint8_t,bits", 0, RW, LittleEndian),
                ]
        Port = CStructTestPort(regs)

        print(Port.struct_entries.keys())
        Port.bit0 = 0
        Port.bit1 = 1
        Port.bit2 = 0
        Port.bit3 = 1
        Port.bit4 = 0
        Port.bit5 = 1
        Port.bit6 = 0
        Port.bit7 = 1
        Camera._Connect(Port, "Device")

        IOBitSelector = Camera.GetNode("IOBitSelector")

        IOBit = Camera.GetNode("IOBit")

        IORegister = Camera.GetNode("IORegister")

        #################/
        # test reading

        # prepare measurement
        Port.InvalidateNode()
        Port.ResetStatistics()
        self.assertEqual(0, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())
        self.assertTrue(not IORegister.IsValueCacheValid())
        print("write")
        Port.bit2 = 0

        # read bit2
        IOBitSelector.SetValue(2)
        self.assertEqual(0, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())

        # first time
        self.assertEqual(False, IOBit.GetValue())
        self.assertEqual(1, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())
        self.assertTrue(IORegister.IsValueCacheValid())

        # second time
        self.assertEqual(False, IOBit.GetValue())
        self.assertEqual(1, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())
        self.assertTrue(IORegister.IsValueCacheValid())

        #################/
        # test writing 

        # prepare measurement
        Port.InvalidateNode()
        Port.ResetStatistics()
        self.assertEqual(0, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())
        self.assertTrue(not IORegister.IsValueCacheValid())

        # write bit3
        IOBitSelector.SetValue(3)
        self.assertEqual(0, Port.GetNumReads())
        self.assertEqual(0, Port.GetNumWrites())

        # first time
        IOBit.SetValue(False)
        self.assertEqual(1, Port.GetNumReads())
        self.assertEqual(1, Port.GetNumWrites())
        self.assertEqual(0, Port.bit3)
        self.assertTrue(IORegister.IsValueCacheValid())

        # second time
        IOBit.SetValue(True)
        self.assertEqual(1, Port.GetNumReads())
        self.assertEqual(2, Port.GetNumWrites())
        self.assertEqual(True, Port.bit3)
        self.assertTrue(IORegister.IsValueCacheValid())

    #
    #     class NodeNameTester : public std::unary_function<INode*, bool>
    #     {
    #         gcstring Name
    #     public:
    #         NodeNameTester (const char _Name[]) : Name(_Name) {}
    #         bool operator() (INode *pNode) const { return pNode.GetName()==Name}
    #     }
    #
    #     class NodeFinder
    #     {
    #         NodeNameTester Test
    #     public:
    #         NodeFinder (const char _Name[]) : Test(_Name) {}
    #         bool operator() (NodeList_t &List) const { return count_if(List.begin(), List.end(), Test)>0}
    #     }

    def test_LinkTypes(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@NodeTestSuite_TestLinkTypes.xml|gxml
    
            <Integer Name="TheNode">
               <pInvalidator>G</pInvalidator>
               <pValue>A</pValue>
               <pMin>B</pMin>
            </Integer>
    
            <Integer Name="A">
               <pValue>C</pValue>
            </Integer>
    
            <Integer Name="B">
               <Value>0</Value>
            </Integer>
    
            <Integer Name="C">
               <Value>0</Value>
            </Integer>
    
            <Integer Name="D">
               <pValue>TheNode</pValue>
            </Integer>
    
            <Integer Name="E">
               <pValue>D</pValue>
            </Integer>
    
            <Integer Name="F">
               <pInvalidator>TheNode</pInvalidator>
               <Value>0</Value>
            </Integer>
    
            <Integer Name="G">
               <pInvalidator>H</pInvalidator>
               <Value>0</Value>
            </Integer>
    
            <Integer Name="H">
               <Value>0</Value>
            </Integer>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "NodeTestSuite_TestLinkTypes")

        Node = Camera.GetNode("TheNode")
        # NodeList_t Children

        # NodeFinder FindA("A")
        # NodeFinder FindB("B")
        # NodeFinder FindC("C")
        # NodeFinder FindD("D")
        # NodeFinder FindE("E")
        # NodeFinder FindF("F")
        # NodeFinder FindG("G")
        # NodeFinder FindH("H")

        # Children.clear ()
        # Node.GetChildren (Children, ctWritingChildren)
        # self.assertEqual (1, Children.size())
        # self.assertTrue (FindA(Children))
        # self.assertTrue (not FindB(Children))
        # self.assertTrue (not FindC(Children))

        # Children.clear ()
        # Node.GetChildren (Children, ctReadingChildren)
        # self.assertEqual (2, Children.size())
        # self.assertTrue (FindA(Children))
        # self.assertTrue (FindB(Children))
        # self.assertTrue (not FindC(Children))

        # Children.clear ()
        # Node.GetChildren (Children, ctTerminalNodes)
        # self.assertEqual (1, Children.size())
        # self.assertTrue (not FindA(Children))
        # self.assertTrue (not FindB(Children))
        # self.assertTrue (FindC(Children))

        # Children.clear ()
        # Node.GetChildren (Children, ctDependingNodes)
        # self.assertEqual (3, Children.size())
        # self.assertTrue (FindD(Children))
        # self.assertTrue (FindE(Children))
        # self.assertTrue (FindF(Children))

        # Children.clear ()
        # Node.GetChildren (Children, ctParentNodes)
        # self.assertEqual (1, Children.size())
        # self.assertTrue (not FindA(Children))
        # self.assertTrue (FindD(Children))
        # self.assertTrue (not FindF(Children))

        # (the name "Invalidators" and comment in Types.h could imply that it should be about all invalidating nodes)
        # Children.clear ()
        # Node.GetChildren (Children, ctInvalidatingChildren)
        # self.assertEqual (3, Children.size())
        # self.assertTrue (FindA(Children))
        # self.assertTrue (FindB(Children))
        # self.assertTrue (FindG(Children))
        # self.assertTrue (not FindH(Children))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
