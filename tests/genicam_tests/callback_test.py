# -----------------------------------------------------------------------------
#  (c) 2005 by Basler Vision Technologies
#  Section: Vision Components
#  Project: GenApiTest
#    Author:
#  $Header:
# -----------------------------------------------------------------------------

from genicam import *
import unittest
from genicamtestcase import GenicamTestCase, CDFHeader, CDFFooter
from testport import CTestPort, cast_buffer, cast_data
import sys
from callbackhelper import CallbackObject


# ---------------------------------------------------------------------------
# the test callback with a counter
# ---------------------------------------------------------------------------
class CallbackUtility(object):
    m_count = 0

    @classmethod
    def Reset(cls):
        cls.m_Count = 0

    @classmethod
    def Callback(cls, node):
        cls.m_Count += 1

    @classmethod
    def Count(cls):
        return cls.m_Count


class CallbackTestSuite(GenicamTestCase):
    def test_Callback01(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback01.xml|gxml
    
            <Float Name="MyFloat">
              <Value>0.0</Value>
              <Min>0.0</Min>
              <Max>100.0</Max>
              <Unit>dB</Unit>
            </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback01")

        CallbackUtility.Reset()

        Float01 = Camera.GetNode("MyFloat")

        # register function pointer
        Register(Float01.Node, CallbackUtility.Callback)

        # register invalid function pointer - nothing should get broken
        with self.assertRaises(TypeError):
            Register(Float01.Node, None)

        # register member function
        # CallbackObject obj
        # void (CallbackObject.*memfn)(INode*) = NULL
        # Register( Float01.GetNode(), obj, memfn )

        # check if callbacks are fired
        numCalls = 42
        for i in range(0, numCalls):
            Float01.SetValue(i)

        self.assertEqual(numCalls, CallbackUtility.Count())

    # varitant of TestCallback01 for strings
    def test_Callback01String(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@CallbackTestSuite_TestCallback01String.xml|gxml
    
        <String Name="MyString">
            <Value>Alle meine Entchen...</Value>
        </String>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback01String")

        CallbackUtility.Reset()

        String01 = Camera.GetNode("MyString")

        # register function pointer
        Register(String01.Node, CallbackUtility.Callback)

        # check if callbacks are fired
        numCalls = 42
        for i in range(0, numCalls):
            String01.SetValue("...schwimmen auf dem See!")
        self.assertEqual(numCalls, CallbackUtility.Count())

    # varitant of TestCallback01 for register node
    def test_Callback01Register(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback01Register.xml|gxml
    
        <Register Name="MyRegister">
            <Address>0x0000</Address>
            <Length>1</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
        </Register>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback01Register")

        RegVal = 0
        Port = CTestPort()
        Port.CreateEntry(0x0000, "uint8_t", RegVal, RW, LittleEndian)
        Camera._Connect(Port, "Port")

        CallbackUtility.Reset()

        Register01 = Camera.GetNode("MyRegister")

        # register function pointer
        Register(Register01.GetNode(), CallbackUtility.Callback)

        # check if callbacks are fired
        numCalls = 42
        for i in range(0, numCalls):
            Register01.FromString("0xAB")
        self.assertEqual(numCalls, CallbackUtility.Count())
        RegVal = 17
        for i in range(0, numCalls):
            Register01.Set(cast_data("uint8_t", LittleEndian, RegVal))
        self.assertEqual(2 * numCalls, CallbackUtility.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback02()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on Float with two callback objects
     """

    def test_Callback02(self):
        # create and initialize node map
        """[ GenApiTest@CallbackTestSuite_TestCallback02.xml|gxml
    
        <Float Name="MyFloat">
          <Value>0.0</Value>
          <Min>0.0</Min>
          <Max>100.0</Max>
          <Unit>dB</Unit>
        </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback02")

        Float01 = Camera.GetNode("MyFloat")

        O1 = CallbackObject()
        O2 = CallbackObject()

        hCbk1 = Register(Float01.GetNode(), O1.Callback)
        hCbk2 = Register(Float01.GetNode(), O2.Callback)

        numCalls = 42
        for i in range(0, numCalls):
            Float01.SetValue(i)

        self.assertEqual(numCalls, O1.Count())
        self.assertEqual(numCalls, O2.Count())

        # de-register callback
        Deregister(hCbk1)
        self.assertFalse(Float01.GetNode().DeregisterCallback(hCbk1))

        Float01.SetValue(33)
        self.assertEqual(numCalls, O1.Count())
        self.assertEqual(numCalls + 1, O2.Count())

        # deregister invalid callback handle
        self.assertFalse(Float01.GetNode().DeregisterCallback(9999))

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback03()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on Float with two callback objects
     """

    def test_Callback03(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback03.xml|gxml
    
        <Boolean Name="MyBoolean">
          <Value>true</Value>
        </Boolean>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback03")

        O1 = CallbackObject()
        O2 = CallbackObject()

        Bool = Camera.GetNode("MyBoolean")

        Register(Bool.GetNode(), CallbackUtility.Callback)
        Register(Bool.GetNode(), O1.Callback)
        Register(Bool.GetNode(), O2.Callback)

        numCalls = 42
        CallbackUtility.Reset()

        for i in range(0, numCalls):
            Bool.SetValue((i & 0x1) != 0)

        self.assertEqual(numCalls, CallbackUtility.Count())
        self.assertEqual(numCalls, O1.Count())
        self.assertEqual(numCalls, O2.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback04()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on Command with two callback objects and the callbackutility
     """

    def test_Callback04(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback04.xml|gxml
    
        <Command Name="MyCommand">
          <Value>0</Value>
          <CommandValue>0xff</CommandValue>
        </Command>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback04")

        O1 = CallbackObject()
        O2 = CallbackObject()

        Cmd = Camera.GetNode("MyCommand")

        Register(Cmd.GetNode(), CallbackUtility.Callback)
        Register(Cmd.GetNode(), O1.Callback)
        Register(Cmd.GetNode(), O2.Callback)

        numCalls = 42
        CallbackUtility.Reset()

        for i in range(0, numCalls):
            Cmd.Execute()

        self.assertEqual(numCalls, CallbackUtility.Count())
        self.assertEqual(numCalls, O1.Count())
        self.assertEqual(numCalls, O2.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback05()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on Enums with two callback objects and the callbackutility
     """

    def test_Callback05(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback05.xml|gxml
    
        <Enumeration Name="MyFood">
          <EnumEntry Name="Orange" >
            <Value>0</Value>
          </EnumEntry>
          <EnumEntry Name="Apple" >
            <Value>1</Value>
          </EnumEntry>
          <EnumEntry Name="Pretzel" >
            <Value>2</Value>
          </EnumEntry>
          <EnumEntry Name="Juice" >
            <Value>3</Value>
          </EnumEntry>
          <Value>0</Value>
        </Enumeration>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback05")

        O1 = CallbackObject()
        O2 = CallbackObject()

        Enum = Camera.GetNode("MyFood")

        Register(Enum.GetNode(), CallbackUtility.Callback)
        Register(Enum.GetNode(), O1.Callback)
        Register(Enum.GetNode(), O2.Callback)

        numCalls = 42
        CallbackUtility.Reset()

        for i in range(0, numCalls):
            Enum.SetIntValue(i & 0x3)

        self.assertEqual(numCalls, CallbackUtility.Count())
        self.assertEqual(numCalls, O1.Count())
        self.assertEqual(numCalls, O2.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback06()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on a float with static callback function
     """

    def test_Callback06(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback06.xml|gxml
    
        <Float Name="A">
          <pValue>B</pValue>
          <pMin>C</pMin>
          <pMax>D</pMax>
        </Float>
    
        <FloatReg Name="B">
          <pIsAvailable>E</pIsAvailable>
          <Address>0</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="C">
          <pIsAvailable>E</pIsAvailable>
          <Address>4</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="D">
          <pIsAvailable>E</pIsAvailable>
          <Address>8</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <Integer Name="E">
           <Value>1</Value>
        </Integer>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback06")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x000, "float32_t", 42, RW, BigEndian)
        Port.CreateEntry(0x004, "float32_t", 42, RW, BigEndian)
        Port.CreateEntry(0x008, "float32_t", 42, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        CallbackUtility.Reset()

        A = Camera.GetNode("A")
        B = Camera.GetNode("B")
        C = Camera.GetNode("C")
        D = Camera.GetNode("D")

        ##### getproperty of boolean pointer - 
        try:
            ValueStr, AttributeStr = B.GetNode().GetProperty("ValueIndexed")
            print("ValueIndexed = " + ValueStr + " : " + AttributeStr + "\n")
        except LogicalErrorException:
            pass

        Register(A.GetNode(), CallbackUtility.Callback)
        Register(B.GetNode(), CallbackUtility.Callback)
        Register(C.GetNode(), CallbackUtility.Callback)
        Register(D.GetNode(), CallbackUtility.Callback)

        C.SetValue(0.0)
        D.SetValue(1.0)

        CallbackUtility.Reset()
        A.SetValue(0.5)
        numCalls = 2
        self.assertEqual(numCalls, CallbackUtility.Count())

        CallbackUtility.Reset()
        B.SetValue(0.5)
        numCalls = 2
        self.assertEqual(numCalls, CallbackUtility.Count())

        CallbackUtility.Reset()
        C.SetValue(-1.0)
        numCalls = 2
        self.assertEqual(numCalls, CallbackUtility.Count())

        CallbackUtility.Reset()
        D.SetValue(2.5)
        numCalls = 2
        self.assertEqual(numCalls, CallbackUtility.Count())

        CallbackUtility.Reset()
        D.GetValue()
        numCalls = 0
        self.assertEqual(numCalls, CallbackUtility.Count())

        numCalls = 2
        D.GetNode().InvalidateNode()
        self.assertEqual(numCalls, CallbackUtility.Count())

        CallbackUtility.Reset()
        E = Camera.GetNode("E")
        numCalls = 4
        E.SetValue(0)
        self.assertEqual(numCalls, CallbackUtility.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback07()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on Enums with two callback objects and the callbackutility
     """

    def test_Callback07(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback07.xml|gxml
    
        <Enumeration Name="MyFood">
          <EnumEntry Name="Orange" >
            <Value>0</Value>
          </EnumEntry>
          <EnumEntry Name="Apple" >
            <Value>1</Value>
          </EnumEntry>
          <EnumEntry Name="Pretzel" >
            <Value>2</Value>
          </EnumEntry>
          <EnumEntry Name="Juice" >
            <Value>3</Value>
          </EnumEntry>
          <pValue>curFood</pValue>
          <pSelected>curDishPrice</pSelected>
          <pSelected>GrandTotal</pSelected>
        </Enumeration>
    
        <Integer Name="Price">
          <pValue>GrandTotal</pValue>
        </Integer>
    
        <Integer Name="NumPersons">
          <Value>5</Value>
        </Integer>
    
        <IntReg Name="curFood">
          <Address>0</Address>
          <Length>8</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <IntReg Name="curDishPrice">
          <Address>8</Address>
          <pAddress>curFood</pAddress>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <IntSwissKnife Name="GrandTotal">
          <pVariable Name="N">NumPersons</pVariable>
          <pVariable Name="P">curDishPrice</pVariable>
          <Formula>N*P</Formula>
        </IntSwissKnife>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback07")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0, "uint64_t", 42, RW, BigEndian)
        Port.CreateEntry(8, "uint32_t", 10, RW, BigEndian)
        Port.CreateEntry(12, "uint32_t", 20, RW, BigEndian)
        Port.CreateEntry(16, "uint32_t", 40, RW, BigEndian)
        Port.CreateEntry(20, "uint32_t", 50, RW, BigEndian)
        Port.CreateEntry(24, "uint32_t", 60, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")
        cbPrice, cbFood, cbPerson = [CallbackObject() for i in range(3)]

        Enum = Camera.GetNode("MyFood")

        Food = Camera.GetNode("curFood")

        Price = Camera.GetNode("Price")

        DishPrice = Camera.GetNode("curDishPrice")

        NumPersons = Camera.GetNode("NumPersons")

        Register(Enum.GetNode(), cbFood.Callback)
        Register(Price.GetNode(), cbPrice.Callback)
        Register(NumPersons.GetNode(), cbPerson.Callback)

        numCalls = 1

        # change the number of persons . Price changes, food not
        cbFood.Reset()
        cbPrice.Reset()
        cbPerson.Reset()
        NumPersons.SetValue(2)
        numCalls = 0
        self.assertEqual(numCalls, cbFood.Count())
        numCalls = 1
        self.assertEqual(numCalls, cbPrice.Count())
        self.assertEqual(numCalls, cbPerson.Count())

        # change the food . Price changes, number of persons not
        cbFood.Reset()
        cbPrice.Reset()
        cbPerson.Reset()
        Food.SetValue(2)
        numCalls = 0
        self.assertEqual(numCalls, cbPerson.Count())
        numCalls = 1
        self.assertEqual(numCalls, cbFood.Count())
        self.assertEqual(numCalls, cbPrice.Count())

        # change the dish price . Price changes, number of persons and food not
        Food.SetValue(0)  # otherwise 'DishPrice's address is incorrect
        cbFood.Reset()
        cbPrice.Reset()
        cbPerson.Reset()
        DishPrice.SetValue(2)
        numCalls = 0
        self.assertEqual(numCalls, cbPerson.Count())
        self.assertEqual(numCalls, cbFood.Count())
        numCalls = 1
        self.assertEqual(numCalls, cbPrice.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback08()
    # ---------------------------------------------------------------------------
    """!
     * Perform  tests selector and invalidator
     """

    def test_Callback08(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback08.xml|gxml
    
        <Integer Name="A">
          <pValue>D</pValue>
        </Integer>
    
        <Integer Name="B">
          <pValue>F</pValue>
        </Integer>
    
        <Float Name="C">
          <Value>3.141</Value>
        </Float>
    
        <MaskedIntReg Name="D" >
          <Address>0x0</Address>
          <Length>8</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <pInvalidator>E</pInvalidator>
          <LSB>15</LSB>
          <MSB>8</MSB>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
          <pSelected>F</pSelected>
        </MaskedIntReg>
    
        <IntReg Name="E">
          <Address>0x0</Address>
          <Length>8</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <pInvalidator>D</pInvalidator>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <IntReg Name="F">
          <Address>0x8</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <IntReg Name="G">
          <Address>0xC</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <pInvalidator>E</pInvalidator>
          <Sign>Unsigned</Sign>
          <Endianess>BigEndian</Endianess>
        </IntReg>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback08")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0, "uint64_t", 42, RW, BigEndian)
        Port.CreateEntry(8, "uint32_t", 10, RW, BigEndian)
        Port.CreateEntry(12, "uint32_t", 20, RW, BigEndian)
        Port.CreateEntry(16, "uint32_t", 40, RW, BigEndian)
        Port.CreateEntry(20, "uint32_t", 50, RW, BigEndian)
        Port.CreateEntry(24, "uint32_t", 60, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        cbA, cbB, cbC, cbD, cbE, cbF, cbG = [CallbackObject() for i in range(7)]

        A = Camera.GetNode("A")
        B = Camera.GetNode("B")
        C = Camera.GetNode("C")
        D = Camera.GetNode("D")
        E = Camera.GetNode("E")
        F = Camera.GetNode("F")
        G = Camera.GetNode("G")

        Register(A.GetNode(), cbA.Callback)
        Register(B.GetNode(), cbB.Callback)
        Register(C.GetNode(), cbC.Callback)
        Register(D.GetNode(), cbD.Callback)
        Register(E.GetNode(), cbE.Callback)
        Register(F.GetNode(), cbF.Callback)
        Register(G.GetNode(), cbG.Callback)

        # set A => cb of A, B, D, E F, G not C
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        A.SetValue(0)
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbF.Count())
        self.assertEqual(numCalls, cbG.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbC.Count())
        # set B => cb of B, F not A, C, D, E, G
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        B.SetValue(0)
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbB.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbC.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbG.Count())

        # set C => no cb
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        C.SetValue(0)
        self.assertEqual(numCalls, cbC.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbF.Count())
        self.assertEqual(numCalls, cbG.Count())

        # set D => cb of A, B, D, F, E, G, C
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        D.SetValue(0)
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbF.Count())
        self.assertEqual(numCalls, cbG.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbC.Count())

        # set E => cb of A, B, D, F, E, G, C
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        E.SetValue(0)
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbF.Count())
        self.assertEqual(numCalls, cbG.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbC.Count())

        # set F => cb of B, F not of A, B, C, D, E,
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        F.SetValue(0)
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbF.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbC.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbG.Count())

        # set G => cb of G not of A, B, C, D, E, F
        numCalls = 1
        cbA.Reset()
        cbA.Reset()
        cbB.Reset()
        cbC.Reset()
        cbD.Reset()
        cbE.Reset()
        cbF.Reset()
        cbG.Reset()
        G.SetValue(0)
        self.assertEqual(numCalls, cbG.Count())
        numCalls = 0
        self.assertEqual(numCalls, cbA.Count())
        self.assertEqual(numCalls, cbB.Count())
        self.assertEqual(numCalls, cbC.Count())
        self.assertEqual(numCalls, cbD.Count())
        self.assertEqual(numCalls, cbE.Count())
        self.assertEqual(numCalls, cbF.Count())

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback09()
    # ---------------------------------------------------------------------------
    """!
     * \brief Perform tests on DCAM-like feature block
     *
     * The feature contains two numerical values ("C" and "D") and a read-only flag
     * ("A") signalling the presence. The base address is obtained from a SmartFeature
     * register ("C"). This register is enabled by unlocking the Advanced Feature
     * Register ("F").
     *
     *
     * Several tricks are used to mimic the camera.
     * - the smart feature address is directly set in the register space (see sfvalue
     *   bitset) and matches the value in XML description
     * - the port object handles the hardcoded address (0) differently and returns
     *   0 or -1 depending on an internal state.
     """

    @unittest.skip("SKIPPING DCAM CODE")
    def test_Callback09(self):
        class CMyTestPort(CTestPort):
            m_Enable = False

            def EnableAdvFeature(self, enable):
                m_Enable = enable

            def Write(self, Buffer, Address, Length):
                if (Address >= 0 and Address < 8):
                    pass
                else:
                    super(CTestPort, self).Write(Buffer, Address, Length)

            def Read(self, Buffer, Address, Length):
                if (Address >= 0 and Address < 8):
                    pass
                else:
                    super(CTestPort, self).Read(Buffer, Address, Length)

        """[ GenApiTest@CallbackTestSuite_TestCallback09.xml|gxml
    
        <StructReg Comment="Fancy Feature" >
    
          <pIsAvailable>B</pIsAvailable>
          <pAddress>B</pAddress>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>LittleEndian</Endianess>
    
        <!--  bool meaning Feature Available -->
          <StructEntry Name="A">
            <AccessMode>RO</AccessMode>
            <Bit>0</Bit>
          </StructEntry>
    
        <!--  Value 1 -->
          <StructEntry Name="C" >
            <pIsAvailable>A</pIsAvailable>
            <LSB>8</LSB>
            <MSB>15</MSB>
          </StructEntry>
    
        <!--  Value 2 -->
          <StructEntry Name="D" >
            <pIsAvailable>A</pIsAvailable>
            <LSB>16</LSB>
            <MSB>23</MSB>
          </StructEntry>
    
        </StructReg>
    
        <!--  Base-Address of Fancy -->
        <SmartFeature Name="B">
          <FeatureID>A014EDBC-6768-4bcb-B039-9070961F2843</FeatureID>
          <Address>8</Address>
          <pPort>MyPort</pPort>
          <pIsAvailable>F</pIsAvailable>
        </SmartFeature>
    
        <!--  DCAM-like lock -->
        <AdvFeatureLock Name="F">
          <Address>0</Address>
          <Length>8</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <FeatureID>0x0030533B73C3</FeatureID>
          <Timeout>0</Timeout>
        </AdvFeatureLock>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback09")

        # create and initialize a test port
        Port = CMyTestPort()
        # int8_t sfvalue[24]
        # all bits set => feature is not available
        # for(uint32_t i=0 i < sizeof(sfvalue) i++) {
        #    sfvalue[i] = (int8_t)0xFF
        # }
        Port.CreateEntry(0x000, "uint32_t", -1, RW, LittleEndian)
        Port.CreateEntry(0x004, "uint32_t", -1, RW, LittleEndian)
        Port.CreateEntry(0x008, "raw", 24, sfvalue, RW)
        Port.CreateEntry(0x020, "uint32_t", -1, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        cbA, cbB, cbC, cbD, cbE, cbF, cbG = [CallbackObject() for i in range(7)]

        A = Camera.GetNode("A")
        B = Camera.GetNode("B")
        C = Camera.GetNode("C")
        D = Camera.GetNode("D")
        F = Camera.GetNode("F")

        # Register( A.GetNode(), cbA.Callback )
        # Register( B.GetNode(), cbB.Callback )
        # Register( C.GetNode(), cbC.Callback )
        # Register( D.GetNode(), cbD.Callback )
        # Register( F.GetNode(), cbF.Callback )

        self.assertEqual(RO, F.GetAccessMode())
        self.assertEqual(NA, B.GetAccessMode())
        self.assertEqual(NA, A.GetAccessMode())
        self.assertEqual(NA, C.GetAccessMode())
        self.assertEqual(NA, D.GetAccessMode())

        # enable advanced feature and set address 0x20in quad 5
        Port.EnableAdvFeature(True)
        # for(uint32_t i=0 i < sizeof(sfvalue) i++) {
        #    sfvalue[i] = 0
        # }
        # sfvalue[19] |= (1 << 5)
        # Port.Write( &sfvalue, 0x8, 24 )
        F.GetNode().InvalidateNode()  # invalidate advanced feature lock F
        B.GetNode().InvalidateNode()  # invalidate smart feature B
        # cbA.Reset(), cbB.Reset(), cbC.Reset(), cbD.Reset(), cbE.Reset(), cbF.Reset()

        self.assertEqual(RO, B.GetAccessMode())
        self.assertEqual(RO, A.GetAccessMode())
        self.assertEqual(RW, C.GetAccessMode())
        self.assertEqual(RW, D.GetAccessMode())

        # no callbacks although B and F write implicitly
        numCalls = 0
        # self.assertEqual( numCalls, cbA.Count() )
        # self.assertEqual( numCalls, cbB.Count() )
        # self.assertEqual( numCalls, cbC.Count() )
        # self.assertEqual( numCalls, cbD.Count() )
        # self.assertEqual( numCalls, cbF.Count() )

        # Set feature C => no callbacks but C itself
        C.SetValue(0)
        numCalls = 0
        # self.assertEqual( numCalls, cbA.Count() )
        # self.assertEqual( numCalls, cbB.Count() )
        # self.assertEqual( numCalls, cbD.Count() )
        # self.assertEqual( numCalls, cbF.Count() )
        numCalls = 1
        # self.assertEqual( numCalls, cbC.Count() )
        # cbC.Reset()

        # Set feature D => no callbacks but D itself
        D.SetValue(0)
        numCalls = 0
        # self.assertEqual( numCalls, cbA.Count() )
        # self.assertEqual( numCalls, cbB.Count() )
        # self.assertEqual( numCalls, cbC.Count() )
        # self.assertEqual( numCalls, cbF.Count() )
        numCalls = 1
        # self.assertEqual( numCalls, cbD.Count() )

    """!
     * Checks callbacks triggered by InvalidateNode() & SetValue().
     """

    def test_Callback10_LoadXMLFromString(self):
        # create and initialize node map
        CameraDescription = (
            CDFHeader +
            """
            <Float Name="A">
              <pValue>B</pValue>
              <pMin>C</pMin>
              <pMax>D</pMax>
            </Float>
            <FloatReg Name="B">
              <pIsAvailable>E</pIsAvailable>
              <Address>0</Address>
              <Length>4</Length>
              <AccessMode>RW</AccessMode>
              <pPort>MyPort</pPort>
              <Endianess>BigEndian</Endianess>
            </FloatReg>
            <FloatReg Name="C">
              <pIsAvailable>E</pIsAvailable>
              <Address>4</Address>
              <Length>4</Length>
              <AccessMode>RW</AccessMode>
              <pPort>MyPort</pPort>
              <Endianess>BigEndian</Endianess>
            </FloatReg>
            <FloatReg Name="D">
              <pIsAvailable>E</pIsAvailable>
              <Address>8</Address>
              <Length>4</Length>
              <AccessMode>RW</AccessMode>
              <pPort>MyPort</pPort>
              <Endianess>BigEndian</Endianess>
            </FloatReg>
            <Integer Name="E">
               <Value>1</Value>
            </Integer>
            <Port Name="MyPort" />
            """
            + CDFFooter
        )

        Camera = CNodeMapRef()
        Camera._LoadXMLFromString(CameraDescription)
        self._TestCallback10(Camera)

    def _TestCallback10(self, Camera):

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x000, "uint32_t", 42, RW, LittleEndian)
        Port.CreateEntry(0x004, "uint32_t", 42, RW, LittleEndian)
        Port.CreateEntry(0x008, "uint32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        A = Camera.GetNode("A")
        B = Camera.GetNode("B")
        C = Camera.GetNode("C")
        D = Camera.GetNode("D")
        E = Camera.GetNode("E")
        MyPort = Camera.GetNode("MyPort")

        obA, obB, obC, obD, obE, obMyPort = [CallbackObject() for i in range(6)]
        Register(A.Node, obA.Callback)
        Register(B.Node, obB.Callback)
        Register(C.Node, obC.Callback)
        Register(D.Node, obD.Callback)
        Register(E.Node, obE.Callback)
        Register(MyPort.Node, obMyPort.Callback)

        # Check number of callbacks triggered by SetValue
        # Use C und D first, because they serve as pMin and pMax for A
        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        C.SetValue(0.0)

        self.assertEqual(1, obA.Count())
        self.assertEqual(0, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        D.SetValue(1.0)
        self.assertEqual(1, obA.Count())
        self.assertEqual(0, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        B.SetValue(1.0)
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        A.SetValue(1.0)
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        E.SetValue(1)
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(1, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        A.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(0, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        B.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        C.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(0, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(0, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        D.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(0, obB.Count())
        self.assertEqual(0, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        E.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(1, obE.Count())
        self.assertEqual(0, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        MyPort.Node.InvalidateNode()
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(0, obE.Count())
        self.assertEqual(1, obMyPort.Count())

        for o in (obA, obB, obC, obD, obE, obMyPort):
            o.Reset()
        Camera._InvalidateNodes()
        self.assertEqual(1, obA.Count())
        self.assertEqual(1, obB.Count())
        self.assertEqual(1, obC.Count())
        self.assertEqual(1, obD.Count())
        self.assertEqual(1, obE.Count())
        self.assertEqual(1, obMyPort.Count())

    def test_Callback10_LoadXMLFromFile(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback10.xml|gxml
    
        <Float Name="A">
          <pValue>B</pValue>
          <pMin>C</pMin>
          <pMax>D</pMax>
        </Float>
    
        <FloatReg Name="B">
          <pIsAvailable>E</pIsAvailable>
          <Address>0</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="C">
          <pIsAvailable>E</pIsAvailable>
          <Address>4</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="D">
          <pIsAvailable>E</pIsAvailable>
          <Address>8</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <Integer Name="E">
           <Value>1</Value>
        </Integer>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback10")
        self._TestCallback10(Camera)

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback11()
    # ---------------------------------------------------------------------------
    """!
     * Perform basic tests on a float with static callback function
     """

    def test_Callback11(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback11.xml|gxml
    
        <StringReg Name="MyString">
          <Address>4</Address>
          <pLength>StringLength</pLength>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
        </StringReg>
    
        <IntReg Name="StringLength" >
          <Address>0</Address>
          <Length>4</Length>
          <AccessMode>RW</AccessMode>
          <pPort>MyPort</pPort>
          <Sign>Unsigned</Sign>
          <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="MyPort" />
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback11")

        # create and initialize a test port
        Port = CTestPort()
        testvalue = "foobar "
        testlength = 7
        Port.CreateEntry(0x000, "int32_t", testlength, RW, LittleEndian)  # StringLenght
        Port.CreateEntry(0x004, "str", testvalue, RW, LittleEndian)  # StringValue

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        CallbackUtility.Reset()

        String = Camera.GetNode("MyString")
        Length = Camera.GetNode("StringLength")

        Register(String.GetNode(), CallbackUtility.Callback)

        Port.ShowMap()
        self.assertEqual(testvalue, String.GetValue())

        # change the length => callback of string
        Length.SetValue(4)
        numCalls = 1
        self.assertEqual(numCalls, CallbackUtility.Count())
        g = testvalue
        self.assertEqual(g[0:4], String.GetValue())
        StringReg = String
        self.assertEqual(4, StringReg.GetLength())

    def test_Callback12(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback12.xml|gxml
    
        <Category Name="Event">
          <pFeature>Node</pFeature>
        </Category>
    
        <Integer Name="Node">
          <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback12")

        Node = Camera.GetNode("Node")

        cbEvent = CallbackObject()
        Register(Node.GetNode(), cbEvent.Callback)

        self.assertEqual(0, cbEvent.Count())
        Node.SetValue(0)
        self.assertEqual(1, cbEvent.Count())

    def Callback13_inside(self, Node):
        # if defined (_WIN32)
        # Never(!) use CLockEx in client code this is for test only
        # GenApi.CLockEx &Lock( *static_cast<GenApi.CLockEx*>(&(pNode.GetNodeMap().GetLock())) )

        # We must be inside the critical section
        # CPPUNIT_ASSERT( Lock.GetRecursionCount() > 0 )
        # endif
        pass

    def Callback13_outside(self, Node):
        # if defined (_WIN32)
        # Never(!) use CLockEx in client code this is for test only
        # GenApi.CLockEx &Lock( *static_cast<GenApi.CLockEx*>(&(pNode.GetNodeMap().GetLock())) )

        # We must be outside the critical section
        # CPPUNIT_ASSERT( Lock.GetRecursionCount() == 0 )
        # endif
        pass

    def test_Callback13(self):
        # create and initialize node map
        """[ GenApiTest@CallbackTestSuite_TestCallback13.xml|gxml
    
        <Integer Name="Node">
          <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback13")

        Node = Camera.GetNode("Node")

        cbEvent = CallbackObject()
        Register(Node.GetNode(), self.Callback13_inside, cbPostInsideLock)
        Register(Node.GetNode(), self.Callback13_outside, cbPostOutsideLock)

        Node.SetValue(0)

    # ---------------------------------------------------------------------------
    # def CallbackTestSuite.TestCallback14()
    # ---------------------------------------------------------------------------
    """!
     * Perform tests on RW Command with callback on pValue
     """

    def test_Callback14(self):
        """[ GenApiTest@CallbackTestSuite_TestCallback14.xml|gxml
    
        <Command Name="MyCommand">
            <pValue>MyCommandReg</pValue>
            <CommandValue>0xff</CommandValue>
        </Command>
    
        <IntReg Name="MyCommandReg">
            <Address>0x10000000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>NoCache</Cachable>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="Feature">
            <pValue>FeatureReg</pValue>
        </Integer>
    
        <IntReg Name="FeatureReg">
            <Address>0x10000004</Address>
            <Length>4</Length>
            <AccessMode>RO</AccessMode>
            <pPort>Port</pPort>
            <pInvalidator>MyCommandReg</pInvalidator>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestCallback14")

        Port = CTestPort()
        Port.CreateEntry(0x10000000, "uint32_t", 0, RW, LittleEndian)
        Port.CreateEntry(0x10000004, "uint32_t", 0, RW, LittleEndian)

        Camera._Connect(Port, "Port")
        # CallbackObject O1

        Cmd = Camera.GetNode("MyCommand")
        Feature = Camera.GetNode("Feature")

        Register(Feature.GetNode(), CallbackUtility.Callback)
        CallbackUtility.Reset()

        # Executing writes MyCommandReg which in turn invalidates FeatureReg and Feature
        # thus reading Feature yields the register value 
        Cmd.Execute()
        self.assertEqual(1, CallbackUtility.Count())
        self.assertEqual(0, Feature.GetValue())

        # Polling the Command does not invalidate anything because the command is not yet done
        self.assertFalse(Cmd.IsDone())
        self.assertEqual(1, CallbackUtility.Count())

        # change both registers 
        value = 0
        Port.Write(0x10000000, cast_data("uint32_t", LittleEndian, value))
        value = 1234
        Port.Write(0x10000004, cast_data("uint32_t", LittleEndian, value))

        # Polling the command invalidates the command
        self.assertTrue(Cmd.IsDone())
        # this yields a second callback on the command...
        self.assertEqual(2, CallbackUtility.Count())
        # ... and invalidates the Feature since it has a pInvalidales link to the Command
        self.assertEqual(1234, Feature.GetValue())

    def test_PortInvalidate(self):
        # if(GenApiSchemaVersion < v1_1)
        #    return

        """[ GenApiTest@CallbackTestSuite_TestPortInvalidate.xml|gxml
    
        <IntReg Name="Invalidator">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Integer Name="FloatingInvalidator">
            <Value>0</Value>
        </Integer>
    
        <IntReg Name="Invalidated">
            <Address>0x0004</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port" >
            <pInvalidator>Invalidator</pInvalidator>
            <pInvalidator>FloatingInvalidator</pInvalidator>
        </Port>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CallbackTestSuite_TestPortInvalidate")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x000, "int32_t", 42, RW, LittleEndian)
        Port.CreateEntry(0x004, "int32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        CallbackUtility.Reset()

        Invalidator = Camera.GetNode("Invalidator")
        FloatingInvalidator = Camera.GetNode("FloatingInvalidator")
        Invalidated = Camera.GetNode("Invalidated")

        Register(Invalidated.GetNode(), CallbackUtility.Callback)

        # touch the invalidator
        Invalidator.SetValue(80)
        # verify that the values depending on the port were invalidated
        # ie. cache bypassed

        Value = 88
        Port.Write(0x04, cast_data("uint32_t", LittleEndian, Value))
        self.assertEqual(88, Invalidated.GetValue())
        # check if the callback was fired
        self.assertEqual(1, CallbackUtility.Count())

        # the same with floating invalidator
        FloatingInvalidator.SetValue(80)
        Value = 99
        Port.Write(0x04, cast_data("uint32_t", LittleEndian, Value))
        self.assertEqual(99, Invalidated.GetValue())
        self.assertEqual(2, CallbackUtility.Count())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
