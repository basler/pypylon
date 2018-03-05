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
from TestPort import CTestPort
from locale import setlocale, LC_ALL


class FloatTestSuite(GenicamTestCase):
    FLOAT32_EPSILON = 1.19209e-07  # np.finfo(np.float32).eps
    FLOAT64_EPSILON = 2.22044604925e-16  # np.finfo(float).eps

    def test_ValueAccess(self):
        """[ GenApiTest@FloatTestSuite_TestValueAccess.xml|gxml
    
            <Float Name="MyFloat">
              <pValue>MyFloatReg</pValue>
              <Unit>dB</Unit>
            </Float>
    
            <FloatReg Name="MyFloatReg">
                <Address>0x00ff</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>MyPort</pPort>
                <Endianess>LittleEndian</Endianess>
            </FloatReg>
    
            <Port Name="MyPort"/>
    
            <Float Name="MyFloatingFloat">
              <Value>1.0</Value>
            </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestValueAccess")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x00ff, "float32_t", 42, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "MyPort")

        floatValue = Camera._GetNode("MyFloat")
        self.assertEqual(intfIFloat, floatValue.Node.GetPrincipalInterfaceType())

        # Check IFloat of CFloat
        self.assertEqual("dB", floatValue.GetUnit())

        floatValue.SetValue(0.1)
        self.assertAlmostEqual(0.1, floatValue.GetValue(), delta=0.001)
        self.assertAlmostEqual(0.1, floatValue.GetValue(False, True), delta=0.001)

        # CPPUNIT_ASSERT_DOUBLES_EQUAL( -(double)std::numeric_limits<float>::max(), ptrFloat01.GetMin(), std::numeric_limits<double>::epsilon())
        # CPPUNIT_ASSERT( ptrFloat01.GetMin() <= ptrFloat01.GetMax() )

        # Check IValue of CFloat
        node = floatValue.GetNode()

        floatValue.FromString("1e-6")
        self.assertAlmostEqual(1.0e-6, floatValue.GetValue(), delta=0.001)
        dbl01 = float(floatValue.ToString())
        self.assertAlmostEqual(dbl01, floatValue.GetValue(), delta=0.001)

        # Check IBase
        self.assertEqual(RW, floatValue.GetAccessMode())

        # Check CFltReg implementation, does not support units
        floatValue2 = Camera.GetNode("MyFloatReg")
        self.assertEqual(intfIFloat, floatValue2.GetNode().GetPrincipalInterfaceType())
        self.assertEqual("", floatValue2.GetUnit())
        self.assertEqual(PureNumber, floatValue2.GetRepresentation())

    #             CFloatRef refFloat
    #             CPPUNIT_ASSERT_NO_THROW(refFloat.SetReference( ptrFloat01 ) )
    #             self.assertEqual( unit, refFloat.GetUnit() )
    #             self.assertEqual( RW, refFloat.GetAccessMode() )
    #             CPPUNIT_ASSERT_DOUBLES_EQUAL( -(double)std::numeric_limits<float>::max(), refFloat.GetMin(), std::numeric_limits<double>::epsilon())
    #             CPPUNIT_ASSERT( refFloat.GetMin() <= refFloat.GetMax() )
    #             self.assertEqual( PureNumber, refFloat.GetRepresentation() )
    #             CPPUNIT_ASSERT_DOUBLES_EQUAL( 1.0e-6, refFloat.GetValue() , 0.001 )
    #             # adef problems in precision and representation by converting back to numbers
    #             double dbl01
    #             String2Value( refFloat.ToString(), &dbl01 )
    #             CPPUNIT_ASSERT_DOUBLES_EQUAL( dbl01, refFloat.GetValue(), 0.001 )
    #             CPPUNIT_ASSERT_NO_THROW( refFloat.SetReference( 0 ) )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.FromString( "2e-005" ), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.ToString(), AccessException )
    #             self.assertEqual( NI, refFloat.GetAccessMode() )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetMax(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetMin(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetNode(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetRepresentation(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetUnit(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetValue(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.SetValue( 3e-004 ), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.operator ()(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.operator =( 4e-004 ), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.operator *(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetDisplayNotation(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetDisplayPrecision(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.GetIntAlias(), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.ImposeMin(0.0), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.ImposeMax(0.0), AccessException )

    #             #
    #             # Pleora FG - Adding missing cases, and maybe more...
    #             #
    #
    #             # Pleora FG - SetValue, valid
    #             refFloat.SetReference( ptrFloat01 )
    #             CPPUNIT_ASSERT_NO_THROW( refFloat.SetValue( 1.0 ) )
    #             CPPUNIT_ASSERT_NO_THROW( refFloat.SetValue( 1.0, true ) )
    #             CPPUNIT_ASSERT_NO_THROW( refFloat.SetValue( 1.0, false ) )
    #             self.assertEqual( refFloat.GetValue(), ptrFloat01.GetValue() )
    #
    #             # Pleora FG - SetValue, invalid
    #             refFloat.SetReference( NULL )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.SetValue( 0.0 ), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.SetValue( 0.0, true ), AccessException )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.SetValue( 0.0, false ), AccessException )
    #
    #             # Pleora FG - operator=, valid
    #             refFloat.SetReference( ptrFloat01 )
    #             CPPUNIT_ASSERT_NO_THROW( refFloat = 2.0 )
    #             CPPUNIT_ASSERT( refFloat.GetValue() == 2.0 )
    #
    #             # Pleora FG - operator=, invalid
    #             refFloat.SetReference( NULL )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat = 2.0, AccessException )
    #
    #             # Pleora FG - operator(), valid
    #             refFloat.SetReference( ptrFloat01 )
    #             ptrFloat01.SetValue( 3.0 )
    #             CPPUNIT_ASSERT( refFloat() == ptrFloat01.GetValue() )
    #
    #             # Pleora FG - operator(), invalid
    #             refFloat.SetReference( NULL )
    #             CPPUNIT_ASSERT_THROW_EX( refFloat.operator()(), AccessException )
    #
    #             # Pleora FG - operator*, valid
    #             refFloat.SetReference( ptrFloat01 )
    #             ptrFloat01.SetValue( 4.0 )
    #             CPPUNIT_ASSERT( *refFloat == ptrFloat01.GetValue() )

    #         NODE_POINTER( Float, MyFloatingFloat )
    #         cout << "Min = " << ptrMyFloatingFloat.GetMin() << endl
    #         cout << "Max = " << ptrMyFloatingFloat.GetMax() << endl

    def test_FloatNodeAccess(self):
        """[ GenApiTest@FloatTestSuite_TestFloatNodeAccess.xml|gxml
    
        <Float Name="Value">
            <pValue>ValueValue</pValue>
            <pMin>ValueMin</pMin>
            <pMax>ValueMax</pMax>
        </Float>
    
        <Float Name="ValueValue">
            <Value>20</Value>
            <Min>0</Min>
            <Max>100</Max>
        </Float>
    
        <Float Name="ValueMin">
            <Value>10</Value>
        </Float>
    
        <Float Name="ValueMax">
            <Value>30</Value>
        </Float>
    
        <Float Name="ValueRepRef">
            <pValue>ValueRep</pValue>
        </Float>
    
        <Float Name="ValueRep">
            <Value>30</Value>
            <Representation>Logarithmic</Representation>
        </Float>
    
        <FloatReg Name="ValueRep2">
            <Address>0x00ff</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>MyPort</pPort>
            <Endianess>LittleEndian</Endianess>
            <Representation>Logarithmic</Representation>
        </FloatReg>
    
        <SwissKnife Name="ValueRep3">
            <Formula>30</Formula>
            <Representation>Logarithmic</Representation>
        </SwissKnife>
    
        <Port Name="MyPort"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatNodeAccess")

        floatValue = Camera.GetNode("Value")
        floatValueMin = Camera.GetNode("ValueMin")
        floatValueValue = Camera.GetNode("ValueValue")

        # happy path
        self.assertAlmostEqual(20.0, floatValue.GetValue(), delta=0.0000001)
        floatValue.SetValue(22.0)
        self.assertAlmostEqual(22.0, floatValue.GetValue(), delta=0.0000001)

        # value too small
        with self.assertRaises(OutOfRangeException):   floatValue.SetValue(0.0)

        # value too large
        with self.assertRaises(OutOfRangeException):   floatValue.SetValue(40.0)

        # set without verify
        floatValue.SetValue(1000.0, False)

        # get with verify
        with self.assertRaises(OutOfRangeException):   floatValue.GetValue(True)

        floatValue.SetValue(20.0, False)

        # make a node in a deeper layer inconsistent (Min = 0)
        floatValueValue.SetValue(-1.0, False)

        # get with verify
        with self.assertRaises(OutOfRangeException):   floatValue.GetValue(True)
        floatValueValue.SetValue(20.0)

        # play around with strings
        floatValue.FromString("18.4")
        # adef problems in precision and representation by converting back to numbers
        dbl01 = float(floatValue.ToString())
        self.assertAlmostEqual(dbl01, floatValue.GetValue(), delta=0.001)
        with self.assertRaises(InvalidArgumentException):   floatValue.FromString("abc")

        # unit
        self.assertEqual("", floatValueValue.GetUnit())
        self.assertEqual("", floatValue.GetUnit())

        #
        # Pleora FG - Representation validation
        #

        # Pleora FG - Direct access
        valueRep = Camera.GetNode("ValueRep")
        self.assertEqual(valueRep.GetRepresentation(), Logarithmic)

        # Pleora FG - Indirect access
        valueRepRef = Camera.GetNode("ValueRepRef")
        self.assertEqual(valueRepRef.GetRepresentation(), Logarithmic)

        # Access for terminal node
        self.assertEqual(floatValueValue.GetRepresentation(), PureNumber)

        # similar for FloatReg and SwissKnife
        valueRep2 = Camera.GetNode("ValueRep2")
        self.assertEqual(valueRep2.GetRepresentation(), Logarithmic)
        valueRep3 = Camera.GetNode("ValueRep3")
        self.assertEqual(valueRep3.GetRepresentation(), Logarithmic)

        #
        # Pleora FG - FloatT missing coverage
        #

        # Pleora FG - FloatT::operator=
        floatValueValue = Camera.GetNode("ValueValue")
        floatValueValue.SetValue(42.001)
        self.assertEqual(floatValueValue.GetValue(), 42.001)

        # Pleora FG - FloatT::operator()
        self.assertEqual(floatValueValue(), 42.001)

        # Pleora FG - FloatT::operator*
        # CPPUNIT_ASSERT( ptrValueValue.IsValid() )
        # self.assertEqual( *(*ptrValueValue), 42.001 )

        # Test value cache valid
        floatValueValue.SetValue(20.0)
        self.assertEqual(False, floatValue.IsValueCacheValid())
        self.assertEqual(20.0, floatValue.GetValue())
        self.assertEqual(True, floatValue.IsValueCacheValid())

    def test_FloatRegNodeAccess(self):
        """[ GenApiTest@FloatTestSuite_TestFloatRegNodeAccess.xml|gxml
    
        <FloatReg Name="Float">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="Double">
            <Address>0x0010</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="ValueReadOnly">
            <Address>0x0020</Address>
            <Length>8</Length>
            <AccessMode>RO</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="ValueWriteOnly">
            <Address>0x0030</Address>
            <Length>8</Length>
            <AccessMode>WO</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="ValueWriteThrough">
            <Address>0x0040</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>WriteThrough</Cachable>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="ValueWriteAround">
            <Address>0x0050</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>WriteAround</Cachable>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="ValueNoCache">
            <Address>0x0060</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>NoCache</Cachable>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
        <FloatReg Name="BigFloat">
            <Address>0x0070</Address>
            <Length>8</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>NoCache</Cachable>         <!--  Pleora FG - Needed to trig a real read reg -->
            <Endianess>BigEndian</Endianess>
        </FloatReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatRegNodeAccess")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x0000, "float32_t", 3.12159, RW, LittleEndian)
        Port.CreateEntry(0x0010, "float64_t", 2.71828, RW, LittleEndian)
        Port.CreateEntry(0x0020, "float64_t", 42.0, RO, LittleEndian)
        Port.CreateEntry(0x0030, "float64_t", 42.0, WO, LittleEndian)
        Port.CreateEntry(0x0040, "float64_t", 42.0, RW, LittleEndian)
        Port.CreateEntry(0x0050, "float64_t", 42.0, RW, LittleEndian)
        Port.CreateEntry(0x0060, "float64_t", 42.0, RW, LittleEndian)
        Port.CreateEntry(0x0070, "float64_t", 42.0, RW, BigEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        floatValue = Camera.GetNode("Float")

        doubleValue = Camera.GetNode("Double")

        # CPPUNIT_ASSERT_DOUBLES_EQUAL( -(double)std::numeric_limits<float>::max(), ptrFloatReg.GetMin(), (double)std::numeric_limits<float>::epsilon() )
        # CPPUNIT_ASSERT_DOUBLES_EQUAL( (double)std::numeric_limits<float>::max(), ptrFloatReg.GetMax(), (double)std::numeric_limits<float>::epsilon() )

        # CPPUNIT_ASSERT_DOUBLES_EQUAL( -std::numeric_limits<double>::max(), ptrDoubleReg.GetMin(), std::numeric_limits<double>::epsilon() )
        # CPPUNIT_ASSERT_DOUBLES_EQUAL( std::numeric_limits<double>::max(), ptrDoubleReg.GetMax(), std::numeric_limits<double>::epsilon() )

        self.assertAlmostEqual(3.12159, floatValue.GetValue(), delta=self.FLOAT32_EPSILON)
        floatValue.SetValue(42.0)
        self.assertAlmostEqual(42.0, floatValue.GetValue(), delta=self.FLOAT32_EPSILON)

        self.assertAlmostEqual(2.71828, doubleValue.GetValue(), delta=self.FLOAT64_EPSILON)
        doubleValue.SetValue(42.0)
        self.assertAlmostEqual(42.0, doubleValue.GetValue(), delta=self.FLOAT64_EPSILON)

        doubleValue.FromString("12.3")
        # adef problems in precision and representation by converting back to numbers
        dbl01 = float(doubleValue.ToString())
        self.assertAlmostEqual(dbl01, doubleValue.GetValue(), 0.001)
        with self.assertRaises(InvalidArgumentException):
            doubleValue.FromString("abc")

        #
        # Pleora FG - FloatT missing coverage
        #

        # Pleora FG - SetValue on non-writable float
        valueRO = Camera.GetNode("ValueReadOnly")
        with self.assertRaises(AccessException):
            valueRO.SetValue(5.0, True)

            # Pleora FG - SetValue chache-related execution paths
        valueWriteThrough = Camera.GetNode("ValueWriteThrough")
        self.assertEqual(42.0, valueWriteThrough.GetValue())
        valueWriteThrough.SetValue(6.0)
        self.assertEqual(6.0, valueWriteThrough.GetValue())
        valueWriteAround = Camera.GetNode("ValueWriteAround")
        valueWriteAround.SetValue(7.0)

        # Pleora FG - GetValue on no-readable float
        valueWO = Camera.GetNode("ValueWriteOnly")
        with self.assertRaises(AccessException):
            valueWO.GetValue(True)

        # Pleora FG - GetValue chache-related execution paths - trigs all possible 'if' values
        valueWriteThrough = Camera.GetNode("ValueWriteThrough")
        valueWriteThrough.GetValue()
        valueWriteAround = Camera.GetNode("ValueWriteAround")
        valueWriteAround.GetValue()
        valueNoCache = Camera.GetNode("ValueNoCache")
        valueNoCache.GetValue()

        # Pleora FG - Big endian registers
        valueBigEndian = Camera.GetNode("BigFloat")
        valueBigEndian.SetValue(3.1416)
        self.assertEqual(valueBigEndian.GetValue(), 3.1416)

    def test_FloatRegWriteAroundCaching(self):
        """[ GenApiTest@FloatTestSuite_TestFloatRegWriteAroundCaching.xml|gxml
    
        <FloatReg Name="FloatReg">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Cachable>WriteAround</Cachable>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <Port Name="Port"/>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatRegWriteAroundCaching")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x0000, "float32_t", 3.0, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        floatReg = Camera.GetNode("FloatReg")

        # ensure that FloatReg's value cache is valid
        self.assertAlmostEqual(3.0, floatReg.GetValue(), 0.001)

        # write a new value
        floatReg.SetValue(4.5)

        # modifiy the value in the port object to simulate a hardware that modifies
        # a written value (e.g. rounding)

        # CLittleEndian<float> newValue = 5.0
        # GenApi::EAccessMode newAccessMode = GenApi::RW
        # Port.UpdateEntry(0x0, sizeof(float), &newValue, newAccessMode)

        # ensure that
        # CPPUNIT_ASSERT_DOUBLES_EQUAL( (float)newValue, ptrFloatReg.GetValue(), 0.001)

    def test_FloatFormatting(self):
        # added <DisplayNotation> and <DisplayPrecision> elements
        # if(GenApiSchemaVersion == v1_0)
        #   return

        """[ GenApiTest@FloatTestSuite_TestFloatFormatting.xml|gxml
    
        <Float Name="MyFloat0">
            <Value>12.3456789</Value>
        </Float>
    
        <Float Name="MyFloat1">
            <Value>12.3456789e99</Value>
        </Float>
    
        <Float Name="MyFloat2">
            <Value>12.3456789</Value>
            <DisplayNotation>Scientific</DisplayNotation>
            <DisplayPrecision>4</DisplayPrecision>
        </Float>
    
        <Float Name="MyFloat3">
            <Value>12.3456789</Value>
            <DisplayNotation>Fixed</DisplayNotation>
            <DisplayPrecision>5</DisplayPrecision>
        </Float>
    
        <Float Name="MyFloat4">
            <Value>12.3456789</Value>
            <DisplayNotation>Fixed</DisplayNotation>
        </Float>
    
        <Float Name="MyFloat5">
            <Value>12.3456789</Value>
            <DisplayPrecision>3</DisplayPrecision>
        </Float>
    
        <Float Name="MyFloat6">
            <pValue>MyFloat3</pValue>
        </Float>
    
        <Converter Name="MyFloat7">
            <FormulaTo>FROM</FormulaTo>
            <FormulaFrom>TO</FormulaFrom>
            <pValue>MyFloat3</pValue>
            <Slope>Increasing</Slope>
        </Converter>
    
        <Converter Name="MyFloat8">
            <FormulaTo>FROM</FormulaTo>
            <FormulaFrom>TO</FormulaFrom>
            <pValue>MyFloat3</pValue>
            <DisplayNotation>Scientific</DisplayNotation>
            <DisplayPrecision>1</DisplayPrecision>
            <Slope>Increasing</Slope>
        </Converter>
    
        <Float Name="MyFloat9">
            <Value>3.14159</Value>
            <Max>3.14159</Max>
            <DisplayNotation>Fixed</DisplayNotation>
            <DisplayPrecision>4</DisplayPrecision>
        </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatFormatting")

        floatValue = Camera.GetNode("MyFloat0")

        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ",")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnAutomatic, floatValue.GetDisplayNotation())
        # 6 is the display precision the STL uses as default
        self.assertEqual(6, floatValue.GetDisplayPrecision())
        self.assertEqual("12.3457", floatValue.ToString())

        #             CFloatRef refFloat
        #             refFloat.SetReference( ptrFloat )
        #             self.assertEqual( refFloat.GetDisplayNotation(), ptrFloat.GetDisplayNotation() )
        #             self.assertEqual( refFloat.GetDisplayPrecision(), ptrFloat.GetDisplayPrecision() )

        floatValue = Camera.GetNode("MyFloat1")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnAutomatic, floatValue.GetDisplayNotation())
        self.assertEqual(6, floatValue.GetDisplayPrecision())
        self.assertEqual("1.23457e+100", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat2")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = ", floatValue.ToString(), "\n")
        self.assertEqual(fnScientific, floatValue.GetDisplayNotation())
        self.assertEqual(4, floatValue.GetDisplayPrecision())
        self.assertTrue(("1.2346e+001" == floatValue.ToString()) or ("1.2346e+01" == floatValue.ToString()))

        floatValue = Camera.GetNode("MyFloat3")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnFixed, floatValue.GetDisplayNotation())
        self.assertEqual(5, floatValue.GetDisplayPrecision())
        self.assertEqual("12.34568", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat4")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnFixed, floatValue.GetDisplayNotation())
        self.assertEqual(6, floatValue.GetDisplayPrecision())
        self.assertEqual("12.345679", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat5")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnAutomatic, floatValue.GetDisplayNotation())
        self.assertEqual(3, floatValue.GetDisplayPrecision())
        self.assertEqual("12.3", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat6")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnFixed, floatValue.GetDisplayNotation())
        self.assertEqual(5, floatValue.GetDisplayPrecision())
        self.assertEqual("12.34568", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat7")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnFixed, floatValue.GetDisplayNotation())
        self.assertEqual(5, floatValue.GetDisplayPrecision())
        self.assertEqual("12.34568", floatValue.ToString())

        floatValue = Camera.GetNode("MyFloat8")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual(fnScientific, floatValue.GetDisplayNotation())
        self.assertEqual(1, floatValue.GetDisplayPrecision())
        self.assertTrue(("1.2e+001" == floatValue.ToString()) or ("1.2e+01" == floatValue.ToString()))

        floatValue = Camera.GetNode("MyFloat9")
        print("Notation = " + EDisplayNotationClass.ToString(floatValue.GetDisplayNotation()) + ", ")
        print("DisplayPrecision = ", floatValue.GetDisplayPrecision(), " : ")
        print("Value = " + floatValue.ToString() + "\n")
        self.assertEqual("3.1415", floatValue.ToString())
        floatValue.FromString(floatValue.ToString())

    def test_FloatInc(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        # create and initialize node map
        """[ GenApiTest@FloatTestSuite_TestFloatInc.xml|gxml
    
            <Float Name="GainWithInc">
                <Value>5.2</Value>
                <Min>1.6</Min>
                <Max>10.0</Max>
                <Inc>0.2</Inc>
            </Float>
    
            <Float Name="GainWithOutInc">
                <Value>5.2</Value>
                <Min>1.6</Min>
                <Max>10.0</Max>
            </Float>
    
            <Float Name="GainWithpInc">
                <Value>5.2</Value>
                <Min>1.6</Min>
                <Max>10.0</Max>
                <pInc>Inc</pInc>
            </Float>
    
            <Float Name="Inc">
                <Value>0.2</Value>
            </Float>
    
            <Float Name="GainFromFloat">
                <pValue>GainWithInc</pValue>
            </Float>
    
            <Float Name="GainFromInt">
                <pValue>GainRaw</pValue>
            </Float>
    
            <Integer Name="GainRaw">
                <Value>0</Value>
                <Min>-2</Min>
                <Max>10</Max>
                <Inc>2</Inc>
            </Integer>
    
            <Converter Name="GainFromLinearConverter">
                <FormulaTo> FROM / 2.0 </FormulaTo>
                <FormulaFrom> TO * 2.0 </FormulaFrom>
                <pValue>GainWithInc</pValue>
                <Slope>Increasing</Slope>
                <IsLinear>Yes</IsLinear>
            </Converter>
    
            <Converter Name="GainFromNonLinearConverter">
                <FormulaTo> FROM / 2.0 </FormulaTo>
                <FormulaFrom> TO * 2.0 </FormulaFrom>
                <pValue>GainWithInc</pValue>
                <Slope>Increasing</Slope>
                <IsLinear>No</IsLinear>
            </Converter>
    
            <Converter Name="GainFromAutomaticConverter">
                <FormulaTo> FROM / 2.0 </FormulaTo>
                <FormulaFrom> TO * 2.0 </FormulaFrom>
                <pValue>GainWithInc</pValue>
                <Slope>Automatic</Slope>
                <IsLinear>Yes</IsLinear>
            </Converter>
    
            <Converter Name="GainFromDecreasingConverter">
                <FormulaTo> FROM / (-2.0) </FormulaTo>
                <FormulaFrom> TO * (-2.0) </FormulaFrom>
                <pValue>GainWithInc</pValue>
                <Slope>Decreasing</Slope>
                <IsLinear>Yes</IsLinear>
            </Converter>
    
            <Converter Name="GainFromVaryingConverter">
                <FormulaTo> FROM / 2.0 </FormulaTo>
                <FormulaFrom> TO * 2.0 </FormulaFrom>
                <pValue>GainWithInc</pValue>
                <Slope>Varying</Slope>
                <IsLinear>Yes</IsLinear>
            </Converter>
    
            <SwissKnife Name="GainFromSwissKnife">
                <pVariable Name="VALUE">GainWithInc</pVariable>
                <Formula> VALUE * 2.0 </Formula>
            </SwissKnife>
    
            <FloatReg Name="GainFloatReg">
                <Address>0x00ff</Address>
                <Length>4</Length>
                <AccessMode>RW</AccessMode>
                <pPort>MyPort</pPort>
                <Endianess>LittleEndian</Endianess>
            </FloatReg>
    
            <Port Name="MyPort"/>
    
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatInc")

        gainWithInc = Camera.GetNode("GainWithInc")
        self.assertAlmostEqual(5.2, gainWithInc.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6, gainWithInc.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0, gainWithInc.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainWithInc.HasInc())
        self.assertAlmostEqual(0.2, gainWithInc.GetInc(), delta=self.FLOAT64_EPSILON)

        #             CFloatRef refFloatWithInc
        #             CPPUNIT_ASSERT_THROW_EX (refFloatWithInc.HasInc(), AccessException)
        #             CPPUNIT_ASSERT_THROW_EX (refFloatWithInc.GetInc(), AccessException)
        #             CPPUNIT_ASSERT_NO_THROW(refFloatWithInc.SetReference( ptrGainWithInc ) )
        #             self.assertEqual (true, refFloatWithInc.HasInc() )
        #             CPPUNIT_ASSERT_DOUBLES_EQUAL( (double)0.2, refFloatWithInc.GetInc(), std::numeric_limits<double>::epsilon() )

        gainWithoutInc = Camera.GetNode("GainWithOutInc")
        self.assertEqual(False, gainWithoutInc.HasInc())
        with self.assertRaises(RuntimeException):
            gainWithoutInc.GetInc()

        #             CFloatRef refFloatWithoutInc
        #             CPPUNIT_ASSERT_NO_THROW(refFloatWithoutInc.SetReference( ptrGainWithoutInc ) )
        #             self.assertEqual (false, refFloatWithoutInc.HasInc() )

        gainWithpInc = Camera.GetNode("GainWithpInc")
        self.assertAlmostEqual(5.2, gainWithpInc.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6, gainWithpInc.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0, gainWithpInc.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainWithpInc.HasInc())
        self.assertAlmostEqual(0.2, gainWithpInc.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromFloat = Camera.GetNode("GainFromFloat")
        self.assertAlmostEqual(5.2, gainFromFloat.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6, gainFromFloat.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0, gainFromFloat.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainFromFloat.HasInc())
        self.assertAlmostEqual(0.2, gainFromFloat.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromInt = Camera.GetNode("GainFromInt")
        self.assertAlmostEqual(0.0, gainFromInt.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(-2.0, gainFromInt.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0, gainFromInt.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainFromInt.HasInc())
        self.assertAlmostEqual(2.0, gainFromInt.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromLinearConverter = Camera.GetNode("GainFromLinearConverter")
        self.assertAlmostEqual(5.2 * 2.0, gainFromLinearConverter.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6 * 2.0, gainFromLinearConverter.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0 * 2.0, gainFromLinearConverter.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainFromLinearConverter.HasInc())
        self.assertAlmostEqual(0.2 * 2.0, gainFromLinearConverter.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromAutomaticConverter = Camera.GetNode("GainFromAutomaticConverter")
        self.assertAlmostEqual(5.2 * 2.0, gainFromAutomaticConverter.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6 * 2.0, gainFromAutomaticConverter.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0 * 2.0, gainFromAutomaticConverter.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainFromAutomaticConverter.HasInc())
        self.assertAlmostEqual(0.2 * 2.0, gainFromAutomaticConverter.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromDecreasingConverter = Camera.GetNode("GainFromDecreasingConverter")
        self.assertAlmostEqual(5.2 * -2.0, gainFromDecreasingConverter.GetValue(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(10.0 * -2.0, gainFromDecreasingConverter.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6 * -2.0, gainFromDecreasingConverter.GetMax(), delta=self.FLOAT64_EPSILON)
        self.assertEqual(True, gainFromDecreasingConverter.HasInc())
        self.assertAlmostEqual(0.2 * 2.0, gainFromDecreasingConverter.GetInc(), delta=self.FLOAT64_EPSILON)

        gainFromVaryingConverter = Camera.GetNode("GainFromVaryingConverter")
        self.assertEqual(False, gainFromVaryingConverter.HasInc())
        with self.assertRaises(RuntimeException):
            gainFromVaryingConverter.GetInc()

        gainFromNonLinearConverter = Camera.GetNode("GainFromNonLinearConverter")
        self.assertEqual(False, gainFromNonLinearConverter.HasInc())
        with self.assertRaises(RuntimeException):
            gainFromNonLinearConverter.GetInc()

        gainFromSwissKnife = Camera.GetNode("GainFromSwissKnife")
        self.assertEqual(False, gainFromSwissKnife.HasInc())
        with self.assertRaises(RuntimeException):
            gainFromSwissKnife.GetInc()
        self.assertEqual(PureNumber, gainFromSwissKnife.GetRepresentation())

        gainFloatReg = Camera.GetNode("GainFloatReg")
        self.assertEqual(False, gainFloatReg.HasInc())
        with self.assertRaises(RuntimeException):
            gainFloatReg.GetInc()

    def test_FloatpLength(self):
        """[ GenApiTest@FloatTestSuite_TestFloatpLength.xml|gxml
    
            <FloatReg Name="Float">
                <pAddress>Address</pAddress>
                <pLength>Length</pLength>
                <AccessMode>RW</AccessMode>
                <pPort>Port</pPort>
                <Endianess>LittleEndian</Endianess>
            </FloatReg>
    
            <Integer Name="Length">
                <Value>1</Value>
            </Integer>
    
            <Integer Name="Address">
                <Value>0x0000</Value>
            </Integer>
    
            <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestFloatpLength")

        # create and initialize a test port
        Port = CTestPort()
        Port.CreateEntry(0x0000, "float32_t", 42.1, RW, LittleEndian)
        Port.CreateEntry(0x00ff, "float64_t", 13.2, RW, LittleEndian)

        # connect the node map to the port
        Camera._Connect(Port, "Port")

        floatValue = Camera.GetNode("Float")
        length = Camera.GetNode("Length")
        address = Camera.GetNode("Address")

        address.SetValue(0x0000)
        length.SetValue(4)
        self.assertAlmostEqual(42.1, floatValue.GetValue(), delta=0.00001)

        address.SetValue(0x00ff)
        length.SetValue(8)
        self.assertAlmostEqual(13.2, floatValue.GetValue(), delta=0.00001)
        length.SetValue(3)
        with self.assertRaises(OutOfRangeException):
            floatValue.GetValue()

    def test_PolyReference(self):
        # test artificially the hard-to-test code paths
        #         CFloatPolyRef poly
        #         self.assertEqual (false, poly.IsInitialized())
        #         CPPUNIT_ASSERT_THROW_EX (poly.SetValue (1.0), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetValue (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetMin (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetMax (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetInc (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetRepresentation (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetUnit (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetDisplayNotation (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetDisplayPrecision (), GenICam::RuntimeException)
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetCachingMode (), GenICam::RuntimeException)
        #         self.assertEqual (poly.HasInc (), false)
        # CPPUNIT_ASSERT_THROW_EX (poly.IsValueCacheValid(), GenICam::RuntimeException)
        #         poly = 1.0
        #         gcstring bar
        #         GenApi::Value2String( poly, bar )
        #         self.assertEqual( bar, gcstring("1"))
        #         self.assertEqual (true, poly.IsInitialized())
        #         self.assertEqual (false, poly.IsPointer())
        #         self.assertEqual((INodePrivate*)NULL, poly.GetPointer())
        #         self.assertEqual (WriteThrough, poly.GetCachingMode())
        #         CPPUNIT_ASSERT_THROW_EX (poly.GetInc (), GenICam::RuntimeException)
        # CPPUNIT_ASSERT_THROW_EX (poly.IsValueCacheValid(), GenICam::RuntimeException)
        #         gcstring str
        #         Value2String (poly, str)
        #         self.assertEqual (gcstring("1"), str)
        #         CPPUNIT_ASSERT (!String2Value (gcstring("grrrgh"), &poly))
        #         CPPUNIT_ASSERT (!String2Value (gcstring(), &poly))
        pass

    def test_PolyPointers(self):
        # if(GenApiSchemaVersion == v1_0)
        #   return

        """[ GenApiTest@FloatTestSuite_TestPolyPointers.xml|gxml
    
        <Float Name="FloatFromInt">
            <pValue>Int</pValue>
        </Float>
    
        <Integer Name="Int">
            <Value>1</Value>
            <Min>1</Min>
            <Max>31</Max>
            <Inc>3</Inc>
            <Unit>foo</Unit>
        </Integer>
    
        <Node Name="SimpleNode">
        </Node>
    
        <Float Name="FloatFromEnum">
            <pValue>Enum</pValue>
        </Float>
    
        <Enumeration Name="Enum">
            <EnumEntry Name="EnumValue1">
                <Value>1</Value>
           </EnumEntry>
            <EnumEntry Name="EnumValue2">
                <Value>2</Value>
           </EnumEntry>
            <Value>1</Value>
        </Enumeration>
    
        <Enumeration Name="EnumNA">
            <EnumEntry Name="EnumValueNA">
                <pIsAvailable>Zero</pIsAvailable>
                <Value>1</Value>
           </EnumEntry>
            <Value>1</Value>
        </Enumeration>
    
        <Integer Name="Zero">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestPolyPointers")

        # test float.integer
        floatFromInt = Camera.GetNode("FloatFromInt")
        intValue = Camera.GetNode("Int")

        self.assertAlmostEqual(1.0, floatFromInt.GetValue(), delta=self.FLOAT64_EPSILON)
        with self.assertRaises(OutOfRangeException):   floatFromInt.SetValue(1e200)
        with self.assertRaises(OutOfRangeException):   floatFromInt.SetValue(-1e200)
        floatFromInt.SetValue(2.4)
        self.assertEqual(1, intValue.GetValue())
        self.assertAlmostEqual(1.0, floatFromInt.GetValue(), delta=self.FLOAT64_EPSILON)
        floatFromInt.SetValue(2.6)
        self.assertEqual(4, intValue.GetValue())
        self.assertAlmostEqual(4.0, floatFromInt.GetValue(), delta=self.FLOAT64_EPSILON)

    #         CFloatPolyRef polyFloatFromInt
    #         polyFloatFromInt = (IInteger*)ptrInt
    #         self.assertEqual (true, polyFloatFromInt.IsInitialized())
    #         self.assertEqual (true, polyFloatFromInt.IsPointer())
    #         ptrInt.SetValue (1)
    #         CPPUNIT_ASSERT_DOUBLES_EQUAL (1.0, polyFloatFromInt.GetValue(), std::numeric_limits<double>::epsilon())
    #         CPPUNIT_ASSERT_THROW_EX (polyFloatFromInt.SetValue (1E200), OutOfRangeException)
    #         CPPUNIT_ASSERT_THROW_EX (polyFloatFromInt.SetValue (-1E200), OutOfRangeException)

    #         CNodePtr ptrNode = Camera._GetNode ("SimpleNode")
    #         CPPUNIT_ASSERT( ptrNode.IsValid() )
    #         CFloatPolyRef polyFloatFromNode
    #         CPPUNIT_ASSERT_THROW_EX (polyFloatFromNode = (INode*)ptrNode, RuntimeException)
    #         self.assertEqual (false, polyFloatFromNode.IsInitialized())

    # test float.enum
    #         CFloatPtr ptrFloatFromEnum = Camera._GetNode("FloatFromEnum")
    #         CPPUNIT_ASSERT( ptrFloatFromEnum.IsValid() )
    #         CEnumerationPtr ptrEnum = Camera._GetNode("Enum")
    #         CPPUNIT_ASSERT( ptrEnum.IsValid() )
    #
    #         self.assertEqual (gcstring(), ptrFloatFromEnum.GetUnit())
    #         self.assertEqual (PureNumber, ptrFloatFromEnum.GetRepresentation())
    #         self.assertEqual (fnAutomatic, ptrFloatFromEnum.GetDisplayNotation())
    #         self.assertEqual ((int64_t)6LL, ptrFloatFromEnum.GetDisplayPrecision())
    #         self.assertEqual (false, ptrFloatFromEnum.HasInc())
    #         CPPUNIT_ASSERT_THROW_EX (ptrFloatFromEnum.GetInc (), GenICam::RuntimeException)
    #         CPPUNIT_ASSERT_DOUBLES_EQUAL (1.0, ptrFloatFromEnum.GetValue(), std::numeric_limits<double>::epsilon())
    #         ptrFloatFromEnum.SetValue (2.0)
    #         self.assertEqual (gcstring("EnumValue2"), ptrEnum.ToString())
    #
    #         CFloatPolyRef polyFloatFromEnum
    #         polyFloatFromEnum = (IEnumeration*)ptrEnum
    #         self.assertEqual (true, polyFloatFromEnum.IsInitialized())
    #         self.assertEqual (true, polyFloatFromEnum.IsPointer())
    #         self.assertEqual (2.0, polyFloatFromEnum.GetValue())
    #         CPPUNIT_ASSERT_THROW_EX (polyFloatFromEnum.GetInc(), RuntimeException)
    #
    #         CEnumerationPtr ptrEnumNA = Camera._GetNode("EnumNA")
    #         CPPUNIT_ASSERT( ptrEnumNA.IsValid() )
    #         CFloatPolyRef polyFloatFromEnumNA
    #         polyFloatFromEnumNA = (IEnumeration*)ptrEnumNA
    #         self.assertEqual (true, polyFloatFromEnumNA.IsInitialized())
    #         CPPUNIT_ASSERT_THROW_EX (polyFloatFromEnumNA.SetValue(1.0), AccessException)


    """! Make sure laoding a flaot constant works even if the global lacale of 
        the C runtime is set to French (were a float constant reads 1,234 instaed of 1.234)
    """

    def test_TheFrenchWay(self):
        """[ GenApiTest@FloatTestSuite_TestTheFrenchWay.xml|gxml
    
        <SwissKnife Name="Value">
            <Formula>1.234</Formula>
        </SwissKnife>
    
        <Float Name="FloatValue">
            <Value>1.234</Value>
        </Float>
    
        """

        OldLocale = setlocale(LC_ALL, None)
        print("Original Locale = " + OldLocale + "\n")

        if (not setlocale(LC_ALL, "French")):
            if (not setlocale(LC_ALL, "fr_FR.UTF-8")):
                setlocale(LC_ALL, "fr_FR")

        print("French locale = " + setlocale(LC_ALL, None) + "\n")

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestTheFrenchWay")
        value = Camera.GetNode("Value")
        value.GetValue()
        self.assertAlmostEqual(1.234, value.GetValue(), self.FLOAT64_EPSILON)

        setlocale(LC_ALL, OldLocale)
        print("Restored locale = " + setlocale(LC_ALL, None) + "\n")

    def TestTicket785_TestStep(self, Camera, NodeName, UncorrectedError=True):

        test = Camera.GetNode(NodeName)

    #         std::stringstream lout
    #
    #
    #        # lout << endl
    #         lout << "TestNode = " << pNodeName
    #         lout << "DisplayNotation  = " << EDisplayNotationClass::ToString(ptrTest.GetDisplayNotation())
    #         lout << "DisplayPrecision = " << ptrTest.GetDisplayPrecision()
    #
    #         lout << "Test.Value       = " << std::setprecision (numeric_limits<double>::digits10) << ptrTest.GetValue() << "\n"
    #         lout << "Test.Min         = " << std::setprecision (numeric_limits<double>::digits10) << ptrTest.GetMin() << "\n"
    #         lout << "Test.Max         = " << std::setprecision (numeric_limits<double>::digits10) << ptrTest.GetMax() << "\n"
    #         lout << "Test.ToString    = " << ptrTest.ToString() << "\n"
    #
    #         GCLOGINFO( &( GenICam::CLog::GetLogger("CppUnit") ), lout.str().c_str() )
    #
    #         # emulate what would happen without the correction in ToString
    #         ostringstream StrBuffer
    #         switch(ptrTest.GetDisplayNotation())
    #         {
    #         case fnFixed:
    #             StrBuffer.setf(ios::fixed, ios::floatfield)
    #             break
    #         case fnScientific:
    #             StrBuffer.setf(ios::scientific, ios::floatfield)
    #             break
    #         case fnAutomatic:
    #             # default
    #             break
    #         default:
    #             assert(false)
    #         }
    #         StrBuffer.precision((std::streamsize)ptrTest.GetDisplayPrecision())
    #         StrBuffer << ptrTest.GetValue()
    #         lout << "Test.uncorrected = " << StrBuffer.str() << "\n"
    #
    #         CPPUNIT_ASSERT_NO_THROW( ptrTest.FromString( ptrTest.ToString() ) )
    #         if(UncorrectedError)
    #             CPPUNIT_ASSERT_THROW_EX( ptrTest.FromString( StrBuffer.str().c_str() ), OutOfRangeException )



    def test_Ticket785(self):
        # added <DisplayNotation> and <DisplayPrecision> elements
        # if(GenApiSchemaVersion == v1_0)
        #    return

        # create and initialize node map
        """[ GenApiTest@FloatTestSuite_TestTicket785.xml|gxml
    
            <Float Name="TestFixedMax">
                <Value>31.415926</Value>
                <Max>31.415926</Max>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestAutomaticMax">
                <Value>31.415926</Value>
                <Max>31.415926</Max>
                <DisplayNotation>Automatic</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestScientificMax">
                <Value>3.415926</Value>
                <Max>3.415926</Max>
                <DisplayNotation>Scientific</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestFixedMaxNegative">
                <Value>-31.415923</Value>
                <Max>-31.415923</Max>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestFixedMin">
                <Value>31.415922</Value>
                <Min>31.415922</Min>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestAutomaticMin">
                <Value>31.415226</Value>
                <Min>31.415226</Min>
                <DisplayNotation>Automatic</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestScientificMin">
                <Value>3.415922</Value>
                <Min>3.415922</Min>
                <DisplayNotation>Scientific</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestFixedMinNegative">
                <Value>-31.415926</Value>
                <Min>-31.415926</Min>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>5</DisplayPrecision>
            </Float>
    
            <Float Name="TestCornerCase01">
                <Value>31.8</Value>
                <Max>31.8</Max>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>0</DisplayPrecision>
            </Float>
    
            <Float Name="TestCornerCase02">
                <Value>31.2</Value>
                <Min>31.2</Min>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>0</DisplayPrecision>
            </Float>
    
            <Float Name="TestCornerCase03">
                <Value>-31.8</Value>
                <Min>-31.8</Min>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>0</DisplayPrecision>
            </Float>
    
            <Float Name="TestCornerCase04">
                <Value>-31.2</Value>
                <Max>-31.2</Max>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>0</DisplayPrecision>
            </Float>
    
            <Float Name="TestCornerCase05">
                <Value>31.8</Value>
                <Min>31.8</Min>
                <Max>31.81</Max>
                <DisplayNotation>Fixed</DisplayNotation>
                <DisplayPrecision>0</DisplayPrecision>
            </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestTicket785")

        self.TestTicket785_TestStep(Camera, "TestFixedMax")
        self.TestTicket785_TestStep(Camera, "TestAutomaticMax")
        self.TestTicket785_TestStep(Camera, "TestScientificMax")
        self.TestTicket785_TestStep(Camera, "TestFixedMaxNegative")

        self.TestTicket785_TestStep(Camera, "TestFixedMin")
        self.TestTicket785_TestStep(Camera, "TestAutomaticMin")
        self.TestTicket785_TestStep(Camera, "TestScientificMin")
        self.TestTicket785_TestStep(Camera, "TestFixedMinNegative")

        self.TestTicket785_TestStep(Camera, "TestCornerCase01")
        self.TestTicket785_TestStep(Camera, "TestCornerCase02")
        self.TestTicket785_TestStep(Camera, "TestCornerCase03")
        self.TestTicket785_TestStep(Camera, "TestCornerCase04")

        # TBD : this fails because the precision is not enough for the resulting number to fit between min and max 
        # TestTicket785_TestStep( Camera._Ptr, "TestCornerCase05", false )

    def test_ListOfValidValues(self):
        """GenApiSchemaVersion != v1_0"""
        if (True):
            """[ GenApiTest@FloatTestSuite_TestListOfValidValues.xml|gxml
        <Float Name="ValueWithIndex">
            <pIndex>index</pIndex>
            <pValueIndexed Index="0" >ValueWithPValue</pValueIndexed>
            <pValueDefault>default</pValueDefault>
        </Float>

        <Integer Name="index">
            <Value>0</Value>
        </Integer>

        <Float Name="default">
            <Value>1.2345</Value>
        </Float>
        <Float Name="ValueWithPValue">
            <pValue>converter</pValue>
            <Min>8</Min>
            <Max>22</Max>
        </Float>

        <Float Name="converter">
            <pValue>ValueRaw</pValue>
        </Float>

        <Integer Name="ValueRaw">
            <pValue>index</pValue>
            <Representation>Linear</Representation>
            <ValidValueSet>1;2;4;8;16;22;64</ValidValueSet>
        </Integer>
        <FloatReg Name="floatReg">
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>MyPort</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>

        <Port Name="MyPort"/>

            """

            Port = CTestPort()
            Port.CreateEntry(0x0000, "float32_t", 42, RW, LittleEndian)
            Camera = CNodeMapRef()
            Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestListOfValidValues")
            Camera._Connect(Port, "MyPort")

            value = Camera.GetNode("ValueWithPValue")
            self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()

            self.assertEqual(3, len(valueList))

            self.assertAlmostEqual(8, valueList[0], self.FLOAT64_EPSILON)
            self.assertAlmostEqual(16, valueList[1], self.FLOAT64_EPSILON)
            self.assertAlmostEqual(22, valueList[2], self.FLOAT64_EPSILON)

            value = Camera.GetNode("ValueWithIndex")
            self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(3, len(valueList))

            self.assertAlmostEqual(8, valueList[0], self.FLOAT64_EPSILON)
            self.assertAlmostEqual(16, valueList[1], self.FLOAT64_EPSILON)
            self.assertAlmostEqual(22, valueList[2], self.FLOAT64_EPSILON)

            index = Camera.GetNode("index")
            index.SetValue(2)

            # self.assertEqual(noIncrement, value.GetIncMode())
            valueList = value.GetListOfValidValues()
            self.assertEqual(0, len(valueList))

            index.SetValue(0)
            # self.assertEqual(listIncrement, value.GetIncMode())

            valueList = value.GetListOfValidValues()
            self.assertEqual(3, len(valueList))

            value = Camera.GetNode("floatReg")

            # self.assertEqual( noIncrement, value.GetIncMode())
            valueList = value.GetListOfValidValues()
            self.assertEqual(0, len(valueList))

    def test_AccessModeNoCache(self):
        """[ GenApiTest@FloatTestSuite_TestAccessModeNoCache.xml|gxml
        <Float Name="FloatA">
           <pIsImplemented>NoCachableIntReg</pIsImplemented>
           <pValue>FloatRegA</pValue>
        </Float>
        <FloatReg Name="FloatRegA">
           <pIsImplemented>NoCachableIntReg</pIsImplemented>
            <Address>0x0000</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <Float Name="FloatB">
           <pIsImplemented>NoCachableIntReg</pIsImplemented>
           <pValue>FloatRegB</pValue>
        </Float>
        <FloatReg Name="FloatRegB">
           <pIsAvailable>NoCachableIntReg</pIsAvailable>
            <Address>0x0004</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
        <Float Name="FloatC">
           <pIsLocked>NoCachableIntReg</pIsLocked>
           <pValue>FloatRegC</pValue>
        </Float>
        <FloatReg Name="FloatRegC">
           <pIsLocked>NoCachableIntReg</pIsLocked>
            <Address>0x0008</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <Endianess>LittleEndian</Endianess>
        </FloatReg>
    
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
        Camera._LoadXMLFromFile("GenApiTest", "FloatTestSuite_TestAccessModeNoCache")

        Port = CTestPort()
        Port.CreateEntry(0x4, "int32_t", 1, RW, LittleEndian)
        Camera._Connect(Port, "Port")


# NODE_POINTER( Float, FloatA )
#         NODE_POINTER( Float, FloatB )
#         NODE_POINTER( Float, FloatC )
#         NODE_POINTER( Float, FloatRegA )
#         NODE_POINTER( Float, FloatRegB )
#         NODE_POINTER( Float, FloatRegC )
#         NODE_POINTER( Integer, NoCachableIntReg )
#     
#         self.assertEqual( NoCache, ptrNoCachableIntReg.GetNode().GetCachingMode() )
#         self.assertEqual( Yes, ptrNoCachableIntReg.GetNode().IsAccessModeCacheable())
#     
#         self.assertEqual( No, ptrFloatA.GetNode().IsAccessModeCacheable() )
#         self.assertEqual( No, ptrFloatB.GetNode().IsAccessModeCacheable() )
#         self.assertEqual( No, ptrFloatC.GetNode().IsAccessModeCacheable() )
#     
#         self.assertEqual( No, ptrFloatRegA.GetNode().IsAccessModeCacheable() )
#         self.assertEqual( No, ptrFloatRegB.GetNode().IsAccessModeCacheable() )
#         self.assertEqual( No, ptrFloatRegC.GetNode().IsAccessModeCacheable() )
#     
#         self.assertEqual( RW, ptrFloatA.GetAccessMode() )
#         self.assertEqual( RW, ptrFloatB.GetAccessMode() )
#         self.assertEqual( RO, ptrFloatC.GetAccessMode() )
#     
#         self.assertEqual( RW, ptrFloatRegA.GetAccessMode() )
#         self.assertEqual( RW, ptrFloatRegB.GetAccessMode() )
#         self.assertEqual( RO, ptrFloatRegC.GetAccessMode() )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'FloatTestSuite.test_ListOfValidValues']
    unittest.main()
