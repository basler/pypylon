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


class IntegerTestSuite(GenicamTestCase):
    FLOAT32_EPSILON = 1.19209e-07  # np.finfo(np.float32).eps
    FLOAT64_EPSILON = 2.22044604925e-16  # np.finfo(float).eps

    def test_ValueAccess(self):
        """[ GenApiTest@IntegerTestSuite_TestValueAccess.xml|gxml
    
        <Integer Name="Value">
            <pValue>ValueValue</pValue>
            <pMin>ValueMin</pMin>
            <pMax>ValueMax</pMax>
            <pInc>ValueInc</pInc>
            <Representation>Linear</Representation>
        </Integer>
    
        <Integer Name="ValueValue">
            <Value>20</Value>
            <Min>0</Min>
            <Max>100</Max>
        </Integer>
    
        <Integer Name="ValueMin">
            <Value>10</Value>
        </Integer>
    
        <Integer Name="ValueMax">
            <Value>30</Value>
        </Integer>
    
        <Integer Name="ValueInc">
            <Value>2</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestValueAccess")

        value = Camera.GetNode("Value")
        self.assertEqual(intfIInteger, value.Node.GetPrincipalInterfaceType())

        valueMin = Camera.GetNode("ValueMin")

        valueValue = Camera.GetNode("ValueValue")

        #         CPPUNIT_ASSERT_NO_THROW(refInteger.SetReference( ptrValue ) )
        #         self.assertEqual( Linear, refInteger.GetRepresentation() )
        #         self.assertEqual( (int64_t)2, refInteger.GetInc() )
        #         self.assertEqual( (int64_t)30, refInteger.GetMax() )
        #         self.assertEqual( (int64_t)10, refInteger.GetMin() )
        #         refInteger.SetValue(18)
        #         self.assertEqual( (int64_t)18, refInteger.GetValue() )
        #         refInteger.SetValue(16)
        #         self.assertEqual( (int64_t)16, refInteger.operator()() )
        #         refInteger.operator=(20)
        #         self.assertEqual( (int64_t)20, refInteger.operator*() )
        #         self.assertEqual( (IFloat*)NULL, refInteger.GetFloatAlias() )

        self.assertEqual(2, value.GetInc())

        # happy path
        self.assertEqual(20, value.GetValue())
        value.SetValue(22)
        self.assertEqual(22, value.GetValue())

        # value too small

        with self.assertRaises(OutOfRangeException):
            value.SetValue(0)

        # value too large
        with self.assertRaises(OutOfRangeException):
            value.SetValue(40)

        # value not fitting the increment
        with self.assertRaises(OutOfRangeException):
            value.SetValue(21)

        # With another Min the Value 21 is now fitting
        # remember, the rule is : (Value - Min) % Inc == 0
        valueMin.SetValue(11)
        value.SetValue(21)
        valueMin.SetValue(10)

        # set without verify
        value.SetValue(21, False)

        # get with verify
        with self.assertRaises(OutOfRangeException):
            value.GetValue(True)

        # make a node in a deeper layer inconsistent (Min = 0)
        valueValue.SetValue(-1, False)

        # get with verify
        with self.assertRaises(OutOfRangeException):
            value.GetValue(Verify=True)

        # play around with strings
        value.FromString("18")
        self.assertEqual("18", value.ToString())
        with self.assertRaises(InvalidArgumentException):
            value.FromString("abc")

        # exercise the invalid case of Inc==0
        valueInc = Camera.GetNode("ValueInc")
        value.SetValue(28)
        valueInc.SetValue(0)
        self.assertEqual(0, value.GetInc())
        with self.assertRaises(OutOfRangeException):   value.SetValue(1)
        # note that on reading Inc is only checked if Verify=
        with self.assertRaises(LogicalErrorException):   value.GetValue(True)
        self.assertEqual(28, value.GetValue())

    def test_RegValueAccess(self):
        """[ GenApiTest@IntegerTestSuite_TestRegValueAccess.xml|gxml
    
        <Integer Name="Value">
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
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestRegValueAccess")

        Port = CTestPort()
        Port.CreateEntry(0x0104, "uint32_t", 1024, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        value = Camera.GetNode("Value")

        self.assertEqual(Linear, value.GetRepresentation())
        self.assertEqual(WO, value.GetAccessMode())
        self.assertEqual(WO, value.GetAccessMode())
        with self.assertRaises(AccessException):   value.GetValue()

        value.SetValue(0)

        with self.assertRaises(AccessException):   value.GetValue()

        with self.assertRaises(OutOfRangeException):   value.SetValue(-1)
        value.SetValue(-1, False)

    def test_RegValueAccessRO(self):
        """[ GenApiTest@IntegerTestSuite_TestRegValueAccessRO.xml|gxml
    
        <Integer Name="Value">
            <pValue>ValueReg</pValue>
            <Min>0</Min>
            <Max>4294967296</Max>
            <Inc>1</Inc>
        </Integer>
        <IntReg Name="ValueReg">
                <Address>0x0104</Address>
                <Length>4</Length>
                <AccessMode>RO</AccessMode>
                 <pPort>Port</pPort>
                <Sign>Unsigned</Sign>
                 <Endianess>LittleEndian</Endianess>
                <Representation>Linear</Representation>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestRegValueAccessRO")

        Port = CTestPort()
        Port.CreateEntry(0x0104, "uint32_t", 1024, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        value = Camera.GetNode("Value")

        self.assertEqual(1024, value.GetValue(True))

        with self.assertRaises(AccessException):
            value.SetValue(0)

    def test_RepresentationValueAccess(self):
        """[ GenApiTest@IntegerTestSuite_TestRepresentationValueAccess.xml|gxml
    
        <Integer Name="Value">
            <Value>30</Value>
            <Min>0</Min>
            <Max>4294967296</Max>
            <Inc>1</Inc>
        </Integer>
    
        <IntSwissKnife Name="Value2">
            <Formula>30</Formula>
        </IntSwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestRepresentationValueAccess")

        value = Camera.GetNode("Value")
        self.assertEqual(PureNumber, value.GetRepresentation())

        value2 = Camera.GetNode("Value2")
        self.assertEqual(PureNumber, value2.GetRepresentation())

    def test_ValueCache(self):
        """[ GenApiTest@IntegerTestSuite_TestValueCache.xml|gxml
    
        <Integer Name="Value">
            <pValue>HiddenValue</pValue>
        </Integer>
    
        <Integer Name="HiddenValue">
            <Value>42</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestValueCache")

        value = Camera.GetNode("Value")

    #         CIntegerRef refValue
    #         refValue.SetReference (ptrValue)
    #
    #         CIntegerPtr ptrHiddenValue = Camera.GetNode("HiddenValue")
    #         CPPUNIT_ASSERT( ptrHiddenValue.IsValid() )
    #
    #         CPPUNIT_ASSERT( !ptrValue.IsValueCacheValid() )
    #         CPPUNIT_ASSERT( !refValue.IsValueCacheValid() )
    #         ptrValue.GetValue()
    #         CPPUNIT_ASSERT( ptrValue.IsValueCacheValid() )
    #         CPPUNIT_ASSERT( refValue.IsValueCacheValid() )


    def test_Unit(self):
        # added <Unit> element
        # if(GenApiSchemaVersion == v1_0)
        #   return

        """[ GenApiTest@IntegerTestSuite_TestUnit.xml|gxml
    
        <Integer Name="Value">
            <pValue>HiddenValue</pValue>
        </Integer>
    
        <Integer Name="HiddenValue">
            <Value>42</Value>
            <Unit>Blubb</Unit>
        </Integer>
    
        <IntConverter Name="ConvertedValue">
            <FormulaTo> FROM / 2 </FormulaTo>
            <FormulaFrom> TO * 2 </FormulaFrom>
            <pValue>RawValue</pValue>
            <Unit>Gigameter</Unit>
            <Slope>Increasing</Slope>
        </IntConverter>
    
        <IntConverter Name="ConvertedValue2">
            <FormulaTo> FROM / 3 </FormulaTo>
            <FormulaFrom> TO * 3 </FormulaFrom>
            <pValue>RawValue</pValue>
            <Slope>Increasing</Slope>
        </IntConverter>
    
        <Integer Name="RawValue">
            <Value>2</Value>
            <Min>0</Min>
            <Max>4096</Max>
            <Unit>Nanocandela</Unit>
        </Integer>
    
        <IntSwissKnife Name="SwissValue">
            <pVariable Name="X">RawValue</pVariable>
            <Formula> X + 12 </Formula>
            <Unit>Terakelvin</Unit>
        </IntSwissKnife>
    
        <IntReg Name="IntReg">
            <Address>0x0000</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Sign>Signed</Sign>
            <Endianess>LittleEndian</Endianess>
            <Unit>Picoampere</Unit>
        </IntReg>
    
        <Port Name="Port"/>
    
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestUnit")

        Port = CTestPort()
        Port.CreateEntry(0x0000, "int64_t", 117, RW, LittleEndian)
        Camera._Connect(Port, "Port")

        value = Camera.GetNode("Value")

        hiddenValue = Camera.GetNode("HiddenValue")

        #         CIntegerRef refInteger
        #         refInteger.SetReference( ptrValue )

        converter = Camera.GetNode("ConvertedValue")
        converter2 = Camera.GetNode("ConvertedValue2")
        swiss = Camera.GetNode("SwissValue")

        intReg = Camera.GetNode("IntReg")

        value.GetValue()

        self.assertEqual("Blubb", value.GetUnit())
        self.assertEqual("Blubb", hiddenValue.GetUnit())
        #         self.assertEqual("Blubb", refInteger.GetUnit() )
        self.assertEqual("Gigameter", converter.GetUnit())
        self.assertEqual("Nanocandela", converter2.GetUnit())
        self.assertEqual("Terakelvin", swiss.GetUnit())
        self.assertEqual("Picoampere", intReg.GetUnit())

    def test_NumberRepresentation(self):
        #         if(GenApiSchemaVersion == v1_0)
        #             return


        # create and initialize node map
        """[ GenApiTest@IntegerTestSuite_TestNumberRepresentation.xml|gxml

        <Integer Name="Linear">
            <Value>14</Value>
            <Representation>Linear</Representation>
        </Integer>

        <Integer Name="Logarithmic">
            <Value>14</Value>
            <Representation>Logarithmic</Representation>
        </Integer>

        <Integer Name="Boolean">
            <Value>14</Value>
            <Representation>Boolean</Representation>
        </Integer>

        <Integer Name="PureNumber">
            <Value>14</Value>
            <Representation>PureNumber</Representation>
        </Integer>

        <Integer Name="HexNumber">
            <Value>0x123456789abcdef</Value>
            <Representation>HexNumber</Representation>
        </Integer>

        <Integer Name="IPV4Address">
            <Value>0x56789abc</Value>
            <Representation>IPV4Address</Representation>
        </Integer>

        <Integer Name="MACAddress">
            <Value>0x123456789abc</Value>
            <Representation>MACAddress</Representation>
        </Integer>

        <IntSwissKnife Name="LogarithmicKnife">
            <Formula>14</Formula>
            <Representation>Logarithmic</Representation>
        </IntSwissKnife>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestNumberRepresentation")

        linear = Camera.GetNode("Linear")
        logarithmic = Camera.GetNode("Logarithmic")
        boolean = Camera.GetNode("Boolean")
        pureNumber = Camera.GetNode("PureNumber")
        hexNumber = Camera.GetNode("HexNumber")
        IPV4Address = Camera.GetNode("IPV4Address")
        MACAddress = Camera.GetNode("MACAddress")
        logarithmicKnife = Camera.GetNode("LogarithmicKnife")

        print("Linear : " + linear.ToString() + "\n")
        self.assertEqual("14", linear.ToString())
        Result = linear.GetValue()
        linear.SetValue(0)
        linear.FromString("14")
        self.assertEqual(Result, linear.GetValue())

        print("Logarithmic : " + logarithmic.ToString() + "\n")
        self.assertEqual("14", logarithmic.ToString())
        Result = logarithmic.GetValue()
        logarithmic.SetValue(0)
        logarithmic.FromString("14")
        self.assertEqual(Result, logarithmic.GetValue())

        print("Boolean : " + boolean.ToString() + "\n")
        self.assertEqual("true", boolean.ToString())
        Result = boolean.GetValue()
        boolean.SetValue(0)
        boolean.FromString("true")
        self.assertEqual(1, boolean.GetValue())  # note, this is different

        print("PureNumber : " + pureNumber.ToString() + "\n")
        self.assertEqual("14", pureNumber.ToString())
        Result = pureNumber.GetValue()
        pureNumber.SetValue(0)
        pureNumber.FromString("14")
        self.assertEqual(Result, pureNumber.GetValue())

        print("HexNumber : " + hexNumber.ToString() + "\n")
        self.assertEqual("0x123456789abcdef", hexNumber.ToString())
        Result = hexNumber.GetValue()
        hexNumber.SetValue(0)
        hexNumber.FromString("0X123456789ABCDEF")
        self.assertEqual(Result, hexNumber.GetValue())

        print("IPV4Address : " + IPV4Address.ToString() + "\n")
        self.assertEqual("86.120.154.188", IPV4Address.ToString())
        Result = IPV4Address.GetValue()
        IPV4Address.SetValue(0)
        IPV4Address.FromString("86.120.154.188")
        self.assertEqual(Result, IPV4Address.GetValue())

        print("MACAddress : " + MACAddress.ToString() + "\n")
        self.assertEqual("12:34:56:78:9a:bc", MACAddress.ToString())
        Result = MACAddress.GetValue()
        MACAddress.SetValue(0)
        MACAddress.FromString("12:34:56:78:9A:BC")
        self.assertEqual(Result, MACAddress.GetValue())

        self.assertEqual(Logarithmic, logarithmicKnife.GetRepresentation())

    def test_PolyReference(self):
        # test artificially the hard-to-test code paths
        pass

    #         CIntegerPolyRef poly
    #         self.assertEqual (False, poly.IsInitialized())
    #         self.assertRaises (poly.SetValue (1), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetValue (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetMin (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetMax (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetInc (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetRepresentation (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetUnit (), GenICam::RuntimeException)
    #         self.assertRaises (poly.GetCachingMode (), GenICam::RuntimeException)
    #         self.assertRaises (poly.IsValueCacheValid(), GenICam::RuntimeException)
    #         poly = 1
    #         gcstring foo
    #         GenApi::Value2String(poly, foo)
    #         self.assertEqual(gcstring("1"), foo)
    #         self.assertEqual (True, poly.IsInitialized())
    #         self.assertEqual (False, poly.IsPointer())
    #         self.assertEqual ((INodePrivate*)NULL, poly.GetPointer())
    #         self.assertEqual (WriteThrough, poly.GetCachingMode())
    #         self.assertEqual ((int64_t)1LL, poly.GetValue())
    #         self.assertEqual (True, poly.IsValueCacheValid())
    #         gcstring str
    #         Value2String (poly, str)
    #         self.assertEqual (gcstring("1"), str)
    #         CPPUNIT_ASSERT (!String2Value (gcstring("grrrgh"), &poly))


    def test_PolyPointers(self):
        # if(GenApiSchemaVersion == v1_0)
        #   return

        """[ GenApiTest@IntegerTestSuite_TestPolyPointers.xml|gxml
    
        <Integer Name="IntFromFloat">
            <pValue>Float</pValue>
        </Integer>
    
        <Float Name="Float">
            <Value>1.0</Value>
            <pMin>FloatMin</pMin>
            <pMax>FloatMax</pMax>
            <Unit>foo</Unit>
        </Float>
    
        <Float Name="FloatMax">
            <Value>3.0</Value>
        </Float>
    
        <Float Name="FloatMin">
            <Value>0.0</Value>
        </Float>
    
        <Integer Name="IntFromFloatWithInc">
            <pValue>FloatWithInc</pValue>
        </Integer>
    
        <Float Name="FloatWithInc">
            <Value>11.2</Value>
            <Inc>2.1</Inc>
        </Float>
    
        <Node Name="SimpleNode">
        </Node>
    
        <Integer Name="IntFromEnum">
            <pValue>Enum</pValue>
        </Integer>
    
        <Enumeration Name="Enum">
            <EnumEntry Name="EnumValue1">
                <Value>1</Value>
           </EnumEntry>
            <EnumEntry Name="EnumValue2">
                <Value>2</Value>
           </EnumEntry>
            <Value>1</Value>
        </Enumeration>
    
        <Integer Name="IntFromBool">
            <pValue>Bool</pValue>
        </Integer>
    
        <Boolean Name="Bool">
            <Value>1</Value>
            <OnValue>7</OnValue>
            <OffValue>5</OffValue>
        </Boolean>
    
        <Integer Name="IntFromEnumWithoutEntry">
            <pValue>EnumWithoutEntry</pValue>
        </Integer>
    
        <Enumeration Name="EnumWithoutEntry">
            <EnumEntry Name="EnumValue1">
                <pIsAvailable>False</pIsAvailable>
                <Value>1</Value>
           </EnumEntry>
            <Value>1</Value>
        </Enumeration>
    
        <Integer Name="False">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestPolyPointers")

        # test integer.floatValue
        intFromFloat = Camera.GetNode("IntFromFloat")
        floatValue = Camera.GetNode("Float")
        floatMax = Camera.GetNode("FloatMax")
        floatMin = Camera.GetNode("FloatMin")

        self.assertEqual(3, intFromFloat.GetMax())
        floatMax.SetValue(1e200)

        with self.assertRaises(RuntimeException):
            intFromFloat.GetMax()

        floatMax.SetValue(-1e200)

        with self.assertRaises(RuntimeException):
            intFromFloat.GetMax()

        floatMax.SetValue(3.0)
        self.assertEqual(0, intFromFloat.GetMin())
        floatMin.SetValue(1e200)
        with self.assertRaises(RuntimeException):
            intFromFloat.GetMin()

        floatMin.SetValue(-1e200)
        with self.assertRaises(RuntimeException):
            intFromFloat.GetMin()

        floatMin.SetValue(0.0)
        self.assertEqual(PureNumber, intFromFloat.GetRepresentation())
        self.assertEqual("foo", intFromFloat.GetUnit())
        self.assertEqual(1, intFromFloat.GetValue())
        floatMax.SetValue(1e200)
        floatMin.SetValue(-1e200)
        floatValue.SetValue(1e200)
        with self.assertRaises(RuntimeException):
            intFromFloat.GetValue()
        floatValue.SetValue(-1e200)
        with self.assertRaises(RuntimeException):
            intFromFloat.GetValue()
        floatValue.SetValue(-1e200)
        floatMax.SetValue(3.0)
        floatMin.SetValue(0.0)
        floatValue.SetValue(1.0)
        self.assertEqual(1, intFromFloat.GetInc())
        intFromFloat.SetValue(2)
        self.assertAlmostEqual(2.0, floatValue.GetValue(), self.FLOAT64_EPSILON)

        intFromFloatWithInc = Camera.GetNode("IntFromFloatWithInc")
        self.assertEqual(2, intFromFloatWithInc.GetInc())

        floatMax.SetValue(13.0)
        floatValue.SetValue(11.2)
        #         CIntegerPolyRef polyIntFromFloat
        #         polyIntFromFloat = (IFloat*)ptrFloat
        #         self.assertEqual (True, polyIntFromFloat.IsInitialized())
        #         self.assertEqual (True, polyIntFromFloat.IsPointer())
        #         self.assertEqual ((int64_t)11LL, polyIntFromFloat.GetValue())
        #         self.assertEqual (True, polyIntFromFloat.IsValueCacheValid())

        node = Camera.GetNode("SimpleNode")
        #         CIntegerPolyRef polyIntFromNode
        #         self.assertRaises (polyIntFromNode = (INode*)ptrNode, RuntimeException)
        #         self.assertEqual (False, polyIntFromNode.IsInitialized())
        #         CStringPolyRef polyStrFromNode
        #         self.assertRaises (polyStrFromNode = (INode*)ptrNode, RuntimeException)
        #         self.assertEqual (False, polyStrFromNode.IsInitialized())
        #
        # test integer.boolValue
        intFromBool = Camera.GetNode("IntFromBool")
        boolValue = Camera.GetNode("Bool")

        self.assertEqual("", intFromBool.GetUnit())
        self.assertEqual(1, intFromBool.GetValue())
        intFromBool.SetValue(0)
        self.assertEqual(False, boolValue.GetValue())
        self.assertEqual(True, intFromBool.IsValueCacheValid())
        intFromBool.SetValue(-253)
        self.assertEqual(True, boolValue.GetValue())

        #         CIntegerPolyRef polyIntFromBool
        #         polyIntFromBool = (IBoolean*)ptrBool
        #         self.assertEqual (True, polyIntFromBool.IsInitialized())
        #         self.assertEqual (True, polyIntFromBool.IsPointer())
        #         self.assertEqual ((int64_t)1LL, polyIntFromBool.GetValue())
        #         self.assertEqual (True, polyIntFromBool.IsValueCacheValid())

        # test integer.enum
        intFromEnum = Camera.GetNode("IntFromEnum")
        enum = Camera.GetNode("Enum")

        self.assertEqual("", intFromEnum.GetUnit())
        self.assertEqual(1, intFromEnum.GetValue())
        intFromEnum.SetValue(2)
        self.assertEqual("EnumValue2", enum.ToString())
        self.assertEqual(True, intFromEnum.IsValueCacheValid())

        #         CIntegerPolyRef polyIntFromEnum
        #         polyIntFromEnum = (IEnumeration*)ptrEnum
        #         self.assertEqual (True, polyIntFromEnum.IsInitialized())
        #         self.assertEqual (True, polyIntFromEnum.IsPointer())
        #         self.assertEqual ((int64_t)2LL, polyIntFromEnum.GetValue())
        #         self.assertEqual (True, polyIntFromEnum.IsValueCacheValid())

        intFromEnumWithoutEntry = Camera.GetNode("IntFromEnumWithoutEntry")
        with self.assertRaises(GenericException):
            intFromEnumWithoutEntry.SetValue(2)
        enumWithoutEntry = Camera.GetNode("EnumWithoutEntry")

    #         CIntegerPolyRef polyIntFromEnumWithoutEntry
    #         polyIntFromEnumWithoutEntry = (IEnumeration*)ptrEnumWithoutEntry
    #         self.assertEqual (True, polyIntFromEnumWithoutEntry.IsInitialized())
    #         self.assertEqual (True, polyIntFromEnumWithoutEntry.IsPointer())
    #         CPPUNIT_ASSERT_THROW (polyIntFromEnumWithoutEntry.SetValue (5), GenericException)



    def test_ListOfValidValue(self):
        # if (GenApiSchemaVersion != v1_0)
        # {
        if (True):
            """[ GenApiTest@IntegerTestSuite_TestListOfValidValue.xml|gxml
        <Integer Name="ValueWithIndex">
            <pIndex>index</pIndex>
            <pValueIndexed Index="0" >ValueWithPValue</pValueIndexed>
            <pValueDefault>index</pValueDefault>
        </Integer>

        <Integer Name="index">
            <Value>0</Value>
        </Integer>

        <Integer Name="ValueWithPValue">
            <pValue>ValueRaw</pValue>
            <Min>8</Min>
            <Max>16</Max>
        </Integer>

        <Integer Name="ValueOverload">
            <pValue>ValueRaw</pValue>
            <ValidValueSet>8;9;10;11;32</ValidValueSet>
        </Integer>

        <Integer Name="ValueRaw">
            <pValue>index</pValue>
            <Min>8</Min>
            <Max>32</Max>
            <Inc>1</Inc>
            <Representation>Linear</Representation>
            <ValidValueSet>1;2;4;8;16;22;64</ValidValueSet>
        </Integer>

            """

            Camera = CNodeMapRef()

            Camera._LoadXMLFromFile("GenApiTest", "IntegerTestSuite_TestListOfValidValue")

            value = Camera.GetNode("ValueRaw")

            self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()

            self.assertEqual(3, len(valueList))

            self.assertEqual(8, valueList[0])
            self.assertEqual(16, valueList[1])
            self.assertEqual(22, valueList[2])

            value = Camera.GetNode("ValueWithPValue")
            self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(2, len(valueList))

            self.assertEqual(8, valueList[0])
            self.assertEqual(16, valueList[1])

            value = Camera.GetNode("ValueOverload")
            # self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(5, len(valueList))
            self.assertEqual(8, valueList[0])
            self.assertEqual(9, valueList[1])
            self.assertEqual(10, valueList[2])
            self.assertEqual(11, valueList[3])
            self.assertEqual(32, valueList[4])

            value = Camera.GetNode("ValueWithIndex")
            # self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(2, len(valueList))

            self.assertEqual(8, valueList[0])
            self.assertEqual(16, valueList[1])

            indexNode = Camera.GetNode("index")
            indexNode.SetValue(2)

            # self.assertEqual(fixedIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(0, len(valueList))
            indexNode.SetValue(0)
            # self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(2, len(valueList))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
