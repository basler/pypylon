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
from testport import CTestPort


class BooleanTestSuite(GenicamTestCase):
    def test_ValueAccess(self):

        """ GenApiTest@BooleanTestSuite_TestValueAccess.xml|gxml

        <Boolean Name="Trigger">
            <Value>1</Value>
            <OnValue>1</OnValue>
            <OffValue>0</OffValue>
        </Boolean>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestValueAccess")

        # create and initialize a test port
        value = Camera._GetNode("Trigger")
        value = Camera.GetNode("Trigger")

        self.assertEqual(intfIBoolean, value.Node.GetPrincipalInterfaceType())

        ##### getproperty of boolean pointer - 
        try:
            AttributeStr = value.Node.GetProperty("ValueIndexed")
            print("ValueIndexed = ", " : ", AttributeStr, "\n")
        except LogicalErrorException:
            pass

        self.assertEqual(1, value.GetValue())
        value.SetValue(False)
        self.assertEqual(0, value.GetValue())
        # once again with verification
        self.assertEqual(0, value.GetValue(True))

        value.SetValue(True)
        self.assertEqual(1, value.GetValue())

        value.FromString("0")

        self.assertEqual("0", value.ToString())

        value.FromString("1")

        self.assertEqual("1", value.ToString())

        with self.assertRaises(InvalidArgumentException):
            value.FromString("X")

        self.assertEqual(RW, value.GetAccessMode())

        # operators
        value.SetValue(False)
        self.assertEqual(0, value())

        # Check IBoolean operators
        value.SetValue(True)
        self.assertEqual(1, value())

        # access without verification
        # (currently just to reach happy path, invalid access is not possible for boolean)
        value.SetValue(True, False)
        value.FromString("0", False)

    def test_RegAccess(self):
        """[ GenApiTest@BooleanTestSuite_TestRegAccess.xml|gxml
    
        <Boolean Name="Trigger">
            <pValue>TriggerReg</pValue>
            <OnValue>1</OnValue>
            <OffValue>0</OffValue>
        </Boolean>
    
        <IntReg Name="TriggerReg">
            <Address>0x00ff</Address>
            <Length>1</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestRegAccess")

        # create and initialize a test port
        Port = CTestPort()

        Port.CreateEntry(0x00ff, "uint8_t", 0, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        value = Camera._GetNode("Trigger")
        self.assertEqual(0, value.GetValue())
        value.SetValue(True)
        self.assertEqual(1, value.GetValue())

        value.SetValue(False)
        self.assertEqual(0, value.GetValue())

        value.FromString("1")
        self.assertEqual("1", value.ToString())

        value.FromString("0")
        self.assertEqual("0", value.ToString())

        self.assertEqual(RW, value.GetAccessMode())

    def test_RegAccess1(self):
        """[ GenApiTest@BooleanTestSuite_TestRegAccess1.xml|gxml
    
        <Boolean Name="Trigger">
            <pValue>TriggerReg</pValue>
            <OnValue>0</OnValue>
            <OffValue>1</OffValue>
        </Boolean>
    
        <IntReg Name="TriggerReg">
            <Address>0x00ff</Address>
            <Length>1</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestRegAccess1")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x00ff, "uint8_t", 3, RW, LittleEndian)  # for LOGICAL_ERROR_EXCEPTION in GetValue

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        value = Camera._GetNode("Trigger")

        with self.assertRaises(LogicalErrorException):   value.GetValue()

    def test_AccessMode(self):
        """[ GenApiTest@BooleanTestSuite_TestAccessMode.xml|gxml
    
        <Boolean Name="Trigger">
            <ImposedAccessMode>RO</ImposedAccessMode>
            <Value>1</Value>
            <OnValue>1</OnValue>
            <OffValue>0</OffValue>
        </Boolean>
    
        <Boolean Name="TriggerWO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <Value>1</Value>
            <OnValue>1</OnValue>
            <OffValue>0</OffValue>
        </Boolean>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestAccessMode")

        # create and initialize a test port
        value = Camera._GetNode("Trigger")

        self.assertEqual(1, value.GetValue())

        with self.assertRaises(AccessException):   value.SetValue(False)

        # now the WO value
        valueWO = Camera._GetNode("TriggerWO")
        valueWO.SetValue(True)
        with self.assertRaises(GenericException):   valueWO.GetValue()

    def test_CornerCases(self):
        """[ GenApiTest@BooleanTestSuite_TestCornerCases.xml|gxml
    
        <!--  JB: Value=7 is not allowed by the schema, changed to correct one -->
        <!--     <Value>7</Value> -->
        <Boolean Name="Invalid">
            <Value>1</Value>
            <OnValue>7</OnValue>
            <OffValue>7</OffValue>
        </Boolean>
    
        """

        Camera = CNodeMapRef()
        with self.assertRaises(RuntimeException):
            Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestCornerCases")

    def test_PolyReference(self):
        # need to test the value access to boolean polydeference artificially
        # because as of this writing, it's not used in GenApi
        pass

    #         CBooleanPolydef poly;
    #         CPPUNIT_ASSERT_EQUAL (false, poly.IsInitialized());
    #         CPPUNIT_ASSERT_EQUAL (false, poly.IsPointer());
    #         CPPUNIT_ASSERT_THROW_EX (poly.SetValue (false), GenICam::RuntimeException);
    #         CPPUNIT_ASSERT_THROW_EX (poly.GetValue (), GenICam::RuntimeException);
    #         CPPUNIT_ASSERT_THROW_EX (poly.GetCachingMode (), GenICam::RuntimeException);
    #         poly = false;
    #         CPPUNIT_ASSERT_EQUAL (true, poly.IsInitialized());
    #         CPPUNIT_ASSERT_EQUAL (false, poly.IsPointer());
    #         CPPUNIT_ASSERT_EQUAL ((INodePrivate*)NULL, poly.GetPointer());
    #         gcstring str;
    #         Value2String (poly, str);
    #         CPPUNIT_ASSERT_EQUAL (gcstring("0"), str);
    #         String2Value (gcstring("1"), &poly);
    #         CPPUNIT_ASSERT_EQUAL (true, poly.GetValue());
    #         CPPUNIT_ASSERT_NO_THROW (poly.SetValue (false));
    #         CPPUNIT_ASSERT_EQUAL (false, poly.GetValue());
    #         CPPUNIT_ASSERT_EQUAL (WriteThrough, poly.GetCachingMode());
    #         CPPUNIT_ASSERT (!String2Value (gcstring("grrrgh"), &poly));

    def test_OnOffValue(self):
        """[ GenApiTest@BooleanTestSuite_TestOnOffValue.xml|gxml
    
        <Boolean Name="BoolValue">
            <pValue>IntValue</pValue>
            <OnValue>5</OnValue>
            <OffValue>3</OffValue>
        </Boolean>
    
        <Integer Name="IntValue">
            <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestOnOffValue")

        # test value which is not On or Off-value
        boolValue = Camera._GetNode("BoolValue")
        intValue = Camera._GetNode("IntValue")

        with self.assertRaises(LogicalErrorException):   boolValue.GetValue()

        boolValue.SetValue(False)
        self.assertEqual(3, intValue.GetValue())
        boolValue.SetValue(True)
        self.assertEqual(5, intValue.GetValue())

    def test_PolyPointers(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return;

        """[ GenApiTest@BooleanTestSuite_TestPolyPointers.xml|gxml
    
        <Integer Name="Int">
            <Value>1</Value>
        </Integer>
    
        <Node Name="SimpleNode">
        </Node>
    
        <Boolean Name="Bool">
            <Value>1</Value>
        </Boolean>
    
        <Enumeration Name="Enum">
            <EnumEntry Name="EnumValue0">
                <Value>0</Value>
           </EnumEntry>
            <EnumEntry Name="EnumValue1">
                <Value>1</Value>
           </EnumEntry>
            <Value>1</Value>
        </Enumeration>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "BooleanTestSuite_TestPolyPointers")

        # test bool->int
        intValue = Camera._GetNode("Int")


# CBooleanPolydef polyBoolFromInt;
#         polyBoolFromInt = (IInteger*)ptrInt;
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromInt.IsInitialized());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromInt.IsPointer());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromInt.GetValue());
#         polyBoolFromInt.SetValue (false);
#         CPPUNIT_ASSERT_EQUAL ((int64_t)0LL, ptrInt->GetValue());
#         polyBoolFromInt.SetValue (true);
#         CPPUNIT_ASSERT_EQUAL ((int64_t)1LL, ptrInt->GetValue());
#     
#         CNodePtr ptrNode = Camera._GetNode ("SimpleNode");
#         CPPUNIT_ASSERT( ptrNode.IsValid() );
#         CBooleanPolydef polyBoolFromNode;
#         CPPUNIT_ASSERT_THROW_EX (polyBoolFromNode = (INode*)ptrNode, RuntimeException);
#         CPPUNIT_ASSERT_EQUAL (false, polyBoolFromNode.IsInitialized());
#     
#         # test bool->bool
#         CBooleanPtr ptrBool = Camera._GetNode("Bool");
#         CPPUNIT_ASSERT( ptrBool.IsValid() );
#         CBooleanPolydef polyBoolFromBool;
#         polyBoolFromBool = (IBoolean*)ptrBool;
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromBool.IsInitialized());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromBool.IsPointer());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromBool.GetValue());
#         polyBoolFromBool.SetValue (false);
#         CPPUNIT_ASSERT_EQUAL (false, ptrBool->GetValue());
#         polyBoolFromBool.SetValue (true);
#         CPPUNIT_ASSERT_EQUAL (true, ptrBool->GetValue());
#     
#         # test bool->enum
#         CEnumerationPtr ptrEnum = Camera._GetNode("Enum");
#         CPPUNIT_ASSERT( ptrEnum.IsValid() );
#         CBooleanPolydef polyBoolFromEnum;
#         polyBoolFromEnum = (IEnumeration*)ptrEnum;
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromEnum.IsInitialized());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromEnum.IsPointer());
#         CPPUNIT_ASSERT_EQUAL (true, polyBoolFromEnum.GetValue());
#         CPPUNIT_ASSERT_EQUAL (dynamic_cast<INodePrivate*>((IEnumeration*)ptrEnum), polyBoolFromEnum.GetPointer());
#         polyBoolFromEnum.SetValue (false);
#         CPPUNIT_ASSERT_EQUAL (gcstring("EnumValue0"), ptrEnum->ToString());
#         polyBoolFromEnum.SetValue (true);
#         CPPUNIT_ASSERT_EQUAL (gcstring("EnumValue1"), ptrEnum->ToString());
#         CPPUNIT_ASSERT_EQUAL (WriteThrough, polyBoolFromEnum.GetCachingMode());



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
