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


class ConverterTestSuite(GenicamTestCase):
    FLOAT32_EPSILON = 1.19209e-07  # np.finfo(np.float32).eps
    FLOAT64_EPSILON = 2.22044604925e-16  # np.finfo(float).eps
    FLOAT64_LIMIT_MAX = 1.79769e+308

    def test_PixelFormat(self):

        """[ GenApiTest@ConverterTestSuite_test_PixelFormat.xml|gxml
    
    <Enumeration Name="PixelFormat" NameSpace="Standard">
        <ToolTip>Format coding of the image pixels</ToolTip>
        <Description>This is a readonly register</Description>
        <EnumEntry Name="Mono8" NameSpace="Standard">
            <Value>0</Value>
        </EnumEntry>
        <EnumEntry Name="YUV411Packed" NameSpace="Standard">
            <Value>1</Value>
        </EnumEntry>
        <EnumEntry Name="YUV422Packed" NameSpace="Standard">
            <Value>2</Value>
        </EnumEntry>
        <EnumEntry Name="YUV444Packed" NameSpace="Standard">
            <Value>3</Value>
        </EnumEntry>
        <EnumEntry Name="RGB8Packed" NameSpace="Standard">
            <Value>4</Value>
        </EnumEntry>
        <EnumEntry Name="Mono14" NameSpace="Standard">
            <Value>5</Value>
        </EnumEntry>
        <EnumEntry Name="RGB14Packed" NameSpace="Standard">
            <Value>6</Value>
        </EnumEntry>
        <EnumEntry Name="Mono12Packed" NameSpace="Standard">
            <Value>129</Value>
        </EnumEntry>
        <EnumEntry Name="BayerGR14" NameSpace="Standard">
            <Value>1010</Value>
        </EnumEntry>
        <EnumEntry Name="BayerRG14" NameSpace="Standard">
            <Value>1110</Value>
        </EnumEntry>
        <EnumEntry Name="BayerGB14" NameSpace="Standard">
            <Value>1210</Value>
        </EnumEntry>
        <EnumEntry Name="BayerBG14" NameSpace="Standard">
            <Value>1310</Value>
        </EnumEntry>
        <EnumEntry Name="BayerGR8" NameSpace="Standard">
            <Value>2109</Value>
        </EnumEntry>
        <EnumEntry Name="BayerRG8" NameSpace="Standard">
            <Value>2209</Value>
        </EnumEntry>
        <EnumEntry Name="BayerGB8" NameSpace="Standard">
            <Value>2009</Value>
        </EnumEntry>
        <EnumEntry Name="BayerBG8" NameSpace="Standard">
            <Value>2309</Value>
        </EnumEntry>
        <pValue>PixelFormat_CtrlValue</pValue>
    </Enumeration>
    <IntSwissKnife Name="SensorColorFilter_RG">
        <pVariable Name="FILTER_ID">ColorFilterID</pVariable>
        <Formula>FILTER_ID = 0</Formula>
    </IntSwissKnife>
    <IntSwissKnife Name="SensorColorFilter_GB">
        <pVariable Name="FILTER_ID">ColorFilterID</pVariable>
        <Formula>FILTER_ID = 1</Formula>
    </IntSwissKnife>
    <IntSwissKnife Name="SensorColorFilter_GR">
        <pVariable Name="FILTER_ID">ColorFilterID</pVariable>
        <Formula>FILTER_ID = 2</Formula>
    </IntSwissKnife>
    <IntSwissKnife Name="SensorColorFilter_BG">
        <pVariable Name="FILTER_ID">ColorFilterID</pVariable>
        <Formula>FILTER_ID = 3</Formula>
    </IntSwissKnife>
    <IntConverter Name="PixelFormat_CtrlValue">
        <pVariable Name="FILT_RG">SensorColorFilter_RG</pVariable>
        <pVariable Name="FILT_BG">SensorColorFilter_BG</pVariable>
        <pVariable Name="FILT_GB">SensorColorFilter_GB</pVariable>
        <pVariable Name="FILT_GR">SensorColorFilter_GR</pVariable>
        <FormulaTo>( FROM = 1010)?10:(( FROM = 1110)?10:(( FROM = 1210)?10:(( FROM = 1310)?10:(( FROM = 2009)?9:(( FROM = 2109)?9:(( FROM = 2209)?9:(( FROM = 2309)?9:(( FROM = 5)?5:(( FROM = 0)?0:(( FROM = 6)?6:(( FROM = 4)?4:(( FROM = 1)?1:(( FROM = 2)?2:(( FROM = 3)?3:(( FROM = 129)?129:(0xdeadbeef))))))))))))))))</FormulaTo>
        <FormulaFrom>(TO = 0)?0:((TO = 5)?5:((TO = 4)?4:((TO = 6)?6:((TO = 1)?1:((TO = 2)?2:((TO = 3)?3:((TO = 129)?129:(((TO = 9) &amp;&amp; FILT_RG)?2209:(((TO = 9) &amp;&amp; FILT_GR)?2109:(((TO = 9) &amp;&amp; FILT_GB)?2009:(((TO = 9) &amp;&amp; FILT_BG)?2309:(((TO = 10) &amp;&amp; FILT_RG)?1110:(((TO = 10) &amp;&amp; FILT_GR)?1010:(((TO = 10) &amp;&amp; FILT_GB)?1210:(((TO = 10) &amp;&amp; FILT_BG)?1310:(0xdeadbeef))))))))))))))))</FormulaFrom>
        <pValue>ColorCode</pValue>
        <Slope>Varying</Slope>
    </IntConverter>
    <Integer Name="ColorCode">
        <Value>3</Value>
    </Integer>
    <Integer Name="ColorFilterID">
        <Value>0</Value>
    </Integer>  
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_test_PixelFormat")

        ColorCode = Camera.GetNode("ColorCode")

        ColorFilterID = Camera.GetNode("ColorFilterID")

        PixelFormat = Camera.GetNode("PixelFormat")

        SensorColorFilter_RG = Camera.GetNode("SensorColorFilter_RG")

        SensorColorFilter_GR = Camera.GetNode("SensorColorFilter_GR")

        SensorColorFilter_BG = Camera.GetNode("SensorColorFilter_BG")

        SensorColorFilter_GB = Camera.GetNode("SensorColorFilter_GB")

        ColorCode.SetValue(0)
        self.assertEqual("Mono8", PixelFormat.GetValue())

        ColorCode.SetValue(1)
        self.assertEqual("YUV411Packed", PixelFormat.GetValue())

        ColorCode.SetValue(2)
        self.assertEqual("YUV422Packed", PixelFormat.GetValue())

        ColorCode.SetValue(3)
        self.assertEqual("YUV444Packed", PixelFormat.GetValue())

        ColorCode.SetValue(4)
        self.assertEqual("RGB8Packed", PixelFormat.GetValue())

        ColorCode.SetValue(5)
        self.assertEqual("Mono14", PixelFormat.GetValue())

        ColorCode.SetValue(6)
        self.assertEqual("RGB14Packed", PixelFormat.GetValue())

        ColorCode.SetValue(129)
        self.assertEqual("Mono12Packed", PixelFormat.GetValue())

        # Raw8
        ColorCode.SetValue(9)

        ColorFilterID.SetValue(0)
        self.assertEqual("BayerRG8", PixelFormat.GetValue())

        ColorFilterID.SetValue(1)
        self.assertEqual("BayerGB8", PixelFormat.GetValue())

        ColorFilterID.SetValue(2)
        self.assertEqual("BayerGR8", PixelFormat.GetValue())

        ColorFilterID.SetValue(3)
        self.assertEqual("BayerBG8", PixelFormat.GetValue())

        # Raw16
        ColorCode.SetValue(10)

        ColorFilterID.SetValue(0)
        self.assertEqual("BayerRG14", PixelFormat.GetValue())

        ColorFilterID.SetValue(1)
        self.assertEqual("BayerGB14", PixelFormat.GetValue())

        ColorFilterID.SetValue(2)
        self.assertEqual("BayerGR14", PixelFormat.GetValue())

        ColorFilterID.SetValue(3)
        self.assertEqual("BayerBG14", PixelFormat.GetValue())

        """ -------------------- """

        PixelFormat.SetValue("Mono8")
        self.assertEqual(0, ColorCode.GetValue())

        PixelFormat.SetValue("YUV411Packed")
        self.assertEqual(1, ColorCode.GetValue())

        PixelFormat.SetValue("YUV422Packed")
        self.assertEqual(2, ColorCode.GetValue())

        PixelFormat.SetValue("YUV444Packed")
        self.assertEqual(3, ColorCode.GetValue())

        PixelFormat.SetValue("RGB8Packed")
        self.assertEqual(4, ColorCode.GetValue())

        PixelFormat.SetValue("Mono14")
        self.assertEqual(5, ColorCode.GetValue())

        PixelFormat.SetValue("RGB14Packed")
        self.assertEqual(6, ColorCode.GetValue())

        PixelFormat.SetValue("Mono12Packed")
        self.assertEqual(129, ColorCode.GetValue())

        # Raw8
        ColorFilterID.SetValue(0)  # the color filter stayes unchanged

        PixelFormat.SetValue("BayerRG8")
        self.assertEqual(9, ColorCode.GetValue())
        self.assertEqual(0, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerGB8")
        self.assertEqual(9, ColorCode.GetValue())
        self.assertEqual(0, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerGR8")
        self.assertEqual(9, ColorCode.GetValue())
        self.assertEqual(0, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerBG8")
        self.assertEqual(9, ColorCode.GetValue())
        self.assertEqual(0, ColorFilterID.GetValue())

        # Raw16
        ColorFilterID.SetValue(1)  # the color filter stayes unchanged

        PixelFormat.SetValue("BayerRG14")
        self.assertEqual(10, ColorCode.GetValue())
        self.assertEqual(1, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerGB14")
        self.assertEqual(10, ColorCode.GetValue())
        self.assertEqual(1, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerGR14")
        self.assertEqual(10, ColorCode.GetValue())
        self.assertEqual(1, ColorFilterID.GetValue())

        PixelFormat.SetValue("BayerBG14")
        self.assertEqual(10, ColorCode.GetValue())
        self.assertEqual(1, ColorFilterID.GetValue())

    def test_ReadModifyWrite(self):
        """[ GenApiTest@ConverterTestSuite_TestReadModifyWrite.xml|gxml
    
        <Converter Name="ShutterAbs">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> TO * TIMEBASE </FormulaFrom>
            <pValue>ShutterRaw</pValue>
        <Unit>s</Unit>
            <Slope>Increasing</Slope>
        </Converter>
    
        <Integer Name="ShutterRaw">
            <Value>2</Value>
        </Integer>
    
        <Integer Name="TimeBase">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestReadModifyWrite")

        ShutterAbs = Camera.GetNode("ShutterAbs")
        self.assertEqual(intfIFloat, ShutterAbs.GetNode().GetPrincipalInterfaceType())

        ShutterRaw = Camera.GetNode("ShutterRaw")

        TimeBase = Camera.GetNode("TimeBase")

        # check the converter's units
        self.assertEqual("s", ShutterAbs.GetUnit())

        # reading
        self.assertAlmostEqual(20.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

        ShutterRaw.SetValue(3)
        self.assertAlmostEqual(30.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

        TimeBase.SetValue(100)
        self.assertAlmostEqual(300.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

        # Writing
        ShutterAbs.SetValue(400.0)
        self.assertEqual(4, ShutterRaw.GetValue())

    def test_ReadModifyWriteInt(self):
        """[ GenApiTest@ConverterTestSuite_TestReadModifyWriteInt.xml|gxml
    
        <IntConverter Name="ShutterAbs">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> TO * TIMEBASE </FormulaFrom>
            <pValue>ShutterRaw</pValue>
            <Slope>Increasing</Slope>
        </IntConverter>
        
        <Integer Name="ShutterRaw">
            <Value>2</Value>
            <Min>0</Min>
            <Max>4096</Max>
        </Integer>
    
        <Integer Name="TimeBase">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestReadModifyWriteInt")

        ShutterAbs = Camera.GetNode("ShutterAbs")

        self.assertEqual(intfIInteger, ShutterAbs.GetNode().GetPrincipalInterfaceType())

        ShutterRaw = Camera.GetNode("ShutterRaw")

        TimeBase = Camera.GetNode("TimeBase")

        # reading
        self.assertEqual(20, ShutterAbs.GetValue())

        ShutterRaw.SetValue(3)
        self.assertEqual(30, ShutterAbs.GetValue())

        TimeBase.SetValue(100)
        self.assertEqual(300, ShutterAbs.GetValue())

        # Writing
        ShutterAbs.SetValue(400)
        self.assertEqual(4, ShutterRaw.GetValue())

    def test_Automatic(self):

        # if(GenApiSchemaVersion == v1_0)
        #    return


        """[ GenApiTest@ConverterTestSuite_TestAutomatic.xml|gxml
    
        <Converter Name="IntInc">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> TO * TIMEBASE </FormulaFrom>
            <pValue>ShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="IntDec">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>ShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="FloatInc">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> TO * TIMEBASE </FormulaFrom>
          <pValue>FloatShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="FloatDec">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>FloatShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="Wobble">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>FloatShutterRaw</pValue>
            <Slope>Varying</Slope>
        </Converter>
    
        <Integer Name="ShutterRaw">
            <Value>2</Value>
            <Min>1</Min>
            <Max>5</Max>
          <Representation>Linear</Representation>
        </Integer>
    
        <Float Name="FloatShutterRaw">
            <Value>2.0</Value>
            <Min>1.0</Min>
            <Max>5.0</Max>
          <Representation>PureNumber</Representation>
        </Float>
    
        <Integer Name="TimeBase">
            <Value>2</Value>
        </Integer>
    
        <Converter Name="IntDec_OwnRepre">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>ShutterRaw</pValue>
            <Unit>my_unit</Unit>
            <Representation>Logarithmic</Representation>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Float Name="FloatWithUnit">
            <Value>2.0</Value>
            <Unit>fltu</Unit>
        </Float>
    
        <Float Name="FloatNoUnit">
            <Value>2.0</Value>
        </Float>
    
        <Integer Name="IntWithUnit">
            <Value>2</Value>
            <Unit>intu</Unit>
        </Integer>
    
        <Converter Name="IntCToFloat">
            <FormulaTo> FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
          <pValue>FloatWithUnit</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="IntCToInt">
            <FormulaTo> FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
          <pValue>IntWithUnit</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <Converter Name="IntCToFloat2">
            <FormulaTo> FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
          <pValue>FloatNoUnit</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestAutomatic")

        IntInc = Camera.GetNode("IntInc")

        IntDec = Camera.GetNode("IntDec")

        FloatInc = Camera.GetNode("FloatInc")

        FloatDec = Camera.GetNode("FloatDec")

        Wobble = Camera.GetNode("Wobble")

        ShutterRaw = Camera.GetNode("ShutterRaw")

        FloatShutterRaw = Camera.GetNode("FloatShutterRaw")

        TimeBase = Camera.GetNode("TimeBase")

        # Test automatic slopes
        self.assertTrue(IntInc.GetMin() == 2)
        self.assertTrue(IntInc.GetMax() == 10)

        self.assertTrue(IntDec.GetMin() == 5)
        self.assertTrue(IntDec.GetMax() == 9)

        self.assertTrue(FloatInc.GetMin() == 2)
        self.assertTrue(FloatInc.GetMax() == 10)

        self.assertTrue(FloatDec.GetMin() == 5)
        self.assertTrue(FloatDec.GetMax() == 9)

        self.assertTrue(Wobble.GetMin() < Wobble.GetMax())

        # Do some gets and sets
        self.assertTrue(FloatInc.GetValue() == 4)
        FloatInc.SetValue(6)
        self.assertTrue(FloatInc.GetValue() == 6)

        self.assertTrue(FloatDec.GetValue() == 7)
        FloatInc.SetValue(8)
        self.assertTrue(FloatDec.GetValue() == 6)

        # Check the representations
        self.assertTrue(IntDec.GetRepresentation() == Linear)
        self.assertTrue(FloatInc.GetRepresentation() == PureNumber)
        self.assertTrue(FloatInc.GetRepresentation() == PureNumber)  # second call for happy path
        IntDec_OwnRepre = Camera.GetNode("IntDec_OwnRepre")

        self.assertTrue(IntDec_OwnRepre.GetRepresentation() == Logarithmic)

        # Check the units
        IntCToFloat = Camera.GetNode("IntCToFloat")

        IntCToInt = Camera.GetNode("IntCToInt")

        IntCToFloat2 = Camera.GetNode("IntCToFloat2")

        self.assertEqual("fltu", IntCToFloat.GetUnit())
        self.assertEqual("intu", IntCToInt.GetUnit())
        self.assertEqual("my_unit", IntDec_OwnRepre.GetUnit())
        self.assertEqual("", IntCToFloat2.GetUnit())

    def test_IntAutomatic(self):
        """[ GenApiTest@ConverterTestSuite_TestIntAutomatic.xml|gxml
    
        <IntConverter Name="IntInc">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> TO * TIMEBASE </FormulaFrom>
            <pValue>ShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </IntConverter>
    
        <IntConverter Name="IntDec">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>ShutterRaw</pValue>
            <Slope>Automatic</Slope>
        </IntConverter>
    
      <IntConverter Name="Wobble">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>ShutterRaw</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <Integer Name="ShutterRaw">
            <Value>2</Value>
            <Min>1</Min>
            <Max>5</Max>
          <Representation>Linear</Representation>
        </Integer>
    
        <Integer Name="TimeBase">
            <Value>2</Value>
        </Integer>
    
        <IntConverter Name="IntDec_OwnRepre">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <FormulaTo> FROM / TIMEBASE </FormulaTo>
            <FormulaFrom> 0 - TO + 10 </FormulaFrom>
          <pValue>ShutterRaw</pValue>
            <Representation>HexNumber</Representation>
            <Slope>Automatic</Slope>
        </IntConverter>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestIntAutomatic")

        IntInc = Camera.GetNode("IntInc")

        IntDec = Camera.GetNode("IntDec")

        # Test automatic slopes
        self.assertTrue(IntInc.GetMin() == 2)
        self.assertTrue(IntInc.GetMax() == 10)

        self.assertTrue(IntDec.GetMin() == 5)
        self.assertTrue(IntDec.GetMax() == 9)

        self.assertTrue(IntDec.GetRepresentation() == Linear)
        self.assertTrue(IntDec.GetRepresentation() == Linear)  # second call for happy path
        IntDec_OwnRepre = Camera.GetNode("IntDec_OwnRepre")

        self.assertTrue(IntDec_OwnRepre.GetRepresentation() == HexNumber)

    def test_Slope(self):
        # ESlope SlopVal
        # bool bOk

        # Test FromString
        # bOk = ESlopeClass::FromString("Increasing", 0)
        # self.assertEqual( bOk, false)

        # bOk = ESlopeClass::FromString("Increasing", &SlopVal)
        # self.assertEqual( bOk, true)
        # self.assertEqual( SlopVal, Increasing)

        # bOk = ESlopeClass::FromString("Decreasing", &SlopVal)
        # self.assertEqual( bOk, true)
        # self.assertEqual( SlopVal, Decreasing)

        # bOk = ESlopeClass::FromString("Varying", &SlopVal)
        # self.assertEqual( bOk, true)
        # self.assertEqual( SlopVal, Varying)

        # bOk = ESlopeClass::FromString("Automatic", &SlopVal)
        # self.assertEqual( bOk, true)
        # self.assertEqual( SlopVal, Automatic)

        # bOk = ESlopeClass::FromString("BadVal", &SlopVal)
        # self.assertEqual( bOk, false)


        # Test ToString
        # ESlope * pSlopVal = 0
        # gcstring strVal
        # self.self.assertRaises(
        #    ESlopeClass::ToString(strVal, pSlopVal),
        #    GenICam::InvalidArgumentException
        # )

        # self.assertEqual(gcstring("Increasing"), ESlopeClass::ToString(Increasing))
        # self.assertEqual(gcstring("Decreasing"), ESlopeClass::ToString(Decreasing))
        # self.assertEqual(gcstring("Varying"), ESlopeClass::ToString(Varying))
        # self.assertEqual(gcstring("Automatic"), ESlopeClass::ToString(Automatic))
        # self.assertEqual(gcstring("_UndefinedESlope"), ESlopeClass::ToString(_UndefinedESlope))
        pass

    def test_InvalidFormulas(self):
        """[ GenApiTest@ConverterTestSuite_TestInvalidFormulas.xml|gxml
    
        <Converter Name="Result">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <FormulaTo> FROM / Z </FormulaTo>
            <FormulaFrom> TO * Z </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Automatic</Slope>
        </Converter>
    
        <IntConverter Name="IntResult">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <FormulaTo> FROM / Z </FormulaTo>
            <FormulaFrom> TO * Z </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Automatic</Slope>
        </IntConverter>
    
        <Integer Name="ConvValue">
            <Value>2</Value>
        </Integer>
    
        <Integer Name="ValueX">
            <Value>3</Value>
        </Integer>
    
        <Integer Name="ValueY">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestInvalidFormulas")

        Result = Camera.GetNode("Result")

        with self.assertRaises(LogicalErrorException):
            Result.GetValue()

        IntResult = Camera.GetNode("IntResult")

        with self.assertRaises(LogicalErrorException):
            IntResult.GetValue()

    def test_CaseInsensitive(self):

        # if(GenApiSchemaVersion == v1_0)
        #    return

        # create and initialize node map
        """[ GenApiTest@ConverterTestSuite_TestCaseInsensitive.xml|gxml
    
        <IntConverter Name="IntResult1">
            <pVariable Name="VALUE">ConvValue</pVariable>
            <FormulaTo> VALUE + FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <IntConverter Name="IntResult2">
            <pVariable Name="VALUE">ConvValue</pVariable>
            <FormulaTo> VALUE + from </FormulaTo>
            <FormulaFrom> to </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <IntConverter Name="IntResult3">
            <pVariable Name="VALUE">ConvValue</pVariable>
            <FormulaTo> VALUE + FRoM </FormulaTo>
            <FormulaFrom> tO </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <Integer Name="ConvValue">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestCaseInsensitive")

        # upper case
        IntResult = Camera.GetNode("IntResult1")
        self.assertEqual(0, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(1, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(2, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(3, IntResult.GetValue())

        # lower case
        IntResult = Camera.GetNode("IntResult2")

        with self.assertRaises(LogicalErrorException):   IntResult.SetValue(1)
        with self.assertRaises(LogicalErrorException):   IntResult.GetValue()

        # mixed case
        IntResult = Camera.GetNode("IntResult3")

        with self.assertRaises(LogicalErrorException):   IntResult.SetValue(1)
        with self.assertRaises(LogicalErrorException):   IntResult.GetValue()

    def test_UseTOinFROM(self):
        """[ GenApiTest@ConverterTestSuite_TestUseTOinFROM.xml|gxml
    
        <IntConverter Name="IntResult">
            <pVariable Name="OLDTO">ConvValue</pVariable>
            <FormulaTo> OLDTO + FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <Integer Name="ConvValue">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestUseTOinFROM")

        IntResult = Camera.GetNode("IntResult")
        self.assertEqual(0, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(1, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(2, IntResult.GetValue())
        IntResult.SetValue(1)
        self.assertEqual(3, IntResult.GetValue())

    def test_FormulaProperty(self):
        # TODOT061 : port this test to new GetProperty signature
        return

        # create and initialize node map
        """[ GenApiTest@ConverterTestSuite_TestFormulaProperty.xml|gxml
    
        <IntConverter Name="IntResult">
            <pVariable Name="OLDTO">ConvValue</pVariable>
            <FormulaTo> OLDTO + FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <Converter Name="Result">
            <pVariable Name="OLDTO">ConvValue</pVariable>
            <FormulaTo> OLDTO + FROM </FormulaTo>
            <FormulaFrom> TO </FormulaFrom>
            <pValue>ConvValue</pValue>
            <Slope>Varying</Slope>
        </Converter>
    
        <Integer Name="ConvValue">
            <Value>0</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestFormulaProperty")

        IntResult = Camera.GetNode("IntResult")
        Result = Camera.GetNode("Result")

        ValueStr = ""
        AttributeStr = ""

        res = IntResult.GetProperty("FormulaTo", ValueStr, AttributeStr)
        self.assertEqual(True, res)
        print("FormulaTo = '" + ValueStr + "'\n")
        res = IntResult.GetProperty("FormulaFrom", ValueStr, AttributeStr)
        self.assertEqual(True, res)
        print("FormulaTo = '" + ValueStr + "'\n")

        res = Result.GetProperty("FormulaTo", ValueStr, AttributeStr)
        self.assertEqual(True, res)
        print("FormulaTo = '" + ValueStr + "'\n")
        res = Result.GetProperty("FormulaFrom", ValueStr, AttributeStr)
        self.assertEqual(True, res)
        print("FormulaTo = '" + ValueStr + "'\n")

        # Trac item 1149: negative values rejected when slope is varying
        FloatResult = Result
        Result.GetProperty("Slope", ValueStr, AttributeStr)
        # self.assertEqual(ValueStr, ESlopeClass::ToString(Varying))
        self.assertAlmostEqual(-self.FLOAT64_LIMIT_MAX, FloatResult.GetMin(), delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(+self.FLOAT64_LIMIT_MAX, FloatResult.GetMax(), delta=self.FLOAT64_EPSILON)
        FloatResult.SetValue(-3.141)

    def test_ConstantAndExpression(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@ConverterTestSuite_TestConstantAndExpression.xml|gxml
    
        <Converter Name="FloatResult">
            <pVariable Name="X">FloatVar</pVariable>
            <Constant Name="Two">2.0</Constant>
            <Expression Name="TwoX">2.0*X</Expression>
            <FormulaTo> FROM - TwoX - Two </FormulaTo>
            <FormulaFrom> TO + TwoX + Two </FormulaFrom>
            <pValue>FloatVal</pValue>
            <Slope>Increasing</Slope>
        </Converter>
    
        <Float Name="FloatVal">
            <Value>1.0</Value>
        </Float>
    
        <Float Name="FloatVar">
            <Value>5.0</Value>
        </Float>
    
    
        <IntConverter Name="IntResult">
            <pVariable Name="X">IntVar</pVariable>
            <Constant Name="Two">2</Constant>
            <Expression Name="TwoX">2*X</Expression>
            <FormulaTo> FROM - TwoX - Two </FormulaTo>
            <FormulaFrom> TO + TwoX + Two </FormulaFrom>
            <pValue>IntVal</pValue>
            <Slope>Increasing</Slope>
        </IntConverter>
    
        <Integer Name="IntVal">
            <Value>1</Value>
            <Min>0</Min>
                <Max>4096</Max>
        </Integer>
    
        <Integer Name="IntVar">
            <Value>5</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestConstantAndExpression")

        IntResult = Camera.GetNode("IntResult")

        IntVal = Camera.GetNode("IntVal")

        self.assertEqual(13, IntResult.GetValue())
        IntResult.SetValue(15)
        self.assertEqual(3, IntVal.GetValue())

        FloatResult = Camera.GetNode("FloatResult")

        FloatVal = Camera.GetNode("FloatVal")

        self.assertEqual(13.0, FloatResult.GetValue())
        FloatResult.SetValue(15.0)
        self.assertEqual(3.0, FloatVal.GetValue())

    def test_Limits(self):
        """[ GenApiTest@ConverterTestSuite_TestLimits.xml|gxml
    
        <IntConverter Name="IntResult">
            <pVariable Name="X">IntVar</pVariable>
            <FormulaTo> FROM / 2 </FormulaTo>
            <FormulaFrom> TO * 2 </FormulaFrom>
            <pValue>IntVal</pValue>
            <Slope>Varying</Slope>
        </IntConverter>
    
        <Integer Name="IntVal">
            <Value>1</Value>
            <Min>0</Min>
            <Max>9223372036854775807</Max>
        </Integer>
    
        <Integer Name="IntVar">
            <Value>5</Value>
        </Integer>
    
        <IntConverter Name="IntResult2">
            <pVariable Name="X">IntVar2</pVariable>
            <FormulaTo> FROM / 2 </FormulaTo>
            <FormulaFrom> TO * 2 </FormulaFrom>
            <pValue>IntVal2</pValue>
            <Slope>Increasing</Slope>
        </IntConverter>
    
        <Integer Name="IntVal2">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="IntVar2">
            <Value>5</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestLimits")

        IntResult = Camera.GetNode("IntResult")

        IntVal = Camera.GetNode("IntVal")

        self.assertEqual(9223372036854775807, IntResult.GetMax())
        IntResult.SetValue(15)

    def test_UpperLowerCase(self):
        if self.GenApiSchemaVersion == "v1_0":

            # In schema version 1.0 the variable names inside the formula are
            # converted to upper case. Thus the variable names in the pVariable entry
            # must always be upper case

            """[ GenApiTest@ConverterTestSuite_TestUpperLowerCase_1_0.xml|gxml
        
           <Converter Name="ShutterAbs">
            <pVariable Name="TIMEBASE">TimeBase</pVariable>
            <!--  note the mixture of upper/lower case letters in the two formulas -->
            <FormulaTo> FroM / TiMeBaSe </FormulaTo>
            <FormulaFrom> TO * timeBASE </FormulaFrom>
            <pValue>ShutterRaw</pValue>
            <Unit>s</Unit>
            <Slope>Increasing</Slope>
        </Converter>
    
        <Integer Name="ShutterRaw">
            <Value>2</Value>
        </Integer>
    
        <Integer Name="TimeBase">
            <Value>10</Value>
        </Integer>
    
        
            """

            Camera = CNodeMapRef()
            Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestUpperLowerCase_1_0")

            ShutterAbs = Camera.GetNode("ShutterAbs")

            self.assertEqual(intfIFloat, ShutterAbs.GetNode().GetPrincipalInterfaceType())

            ShutterRaw = Camera.GetNode("ShutterRaw")

            TimeBase = Camera.GetNode("TimeBase")

            # check the converter's units
            self.assertEqual("s", ShutterAbs.GetUnit())

            # reading
            self.assertAlmostEqual(20.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            ShutterRaw.SetValue(3)
            self.assertAlmostEqual(30.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            TimeBase.SetValue(100)
            self.assertAlmostEqual(300.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            # Writing
            ShutterAbs.SetValue(400.0)
            self.assertEqual(4, ShutterRaw.GetValue())

        else:
            # In schema version 1.1 ff the variable names can be mixed upper/lower case
            # but must be the same in the formula and the pVariable statement

            """[ GenApiTest@ConverterTestSuite_TestUpperLowerCase_1_1.xml|gxml
            
            <Converter Name="ShutterAbs">
                <pVariable Name="TiMeBaSe">TimeBase</pVariable>
                <FormulaTo> FROM / TiMeBaSe </FormulaTo>
                <FormulaFrom> TO * TiMeBaSe </FormulaFrom>
                <pValue>ShutterRaw</pValue>
                <Unit>s</Unit>
                <Slope>Increasing</Slope>
            </Converter>
            
            <Integer Name="ShutterRaw">
                <Value>2</Value>
            </Integer>
            
            <Integer Name="TimeBase">
                <Value>10</Value>
            </Integer>
            
            """

            Camera = CNodeMapRef()
            Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestUpperLowerCase_1_1")

            ShutterAbs = Camera.GetNode("ShutterAbs")

            self.assertEqual(intfIFloat, ShutterAbs.GetNode().GetPrincipalInterfaceType())

            ShutterRaw = Camera.GetNode("ShutterRaw")

            TimeBase = Camera.GetNode("TimeBase")

            # check the converter's units
            self.assertEqual("s", ShutterAbs.GetUnit())

            # reading
            self.assertAlmostEqual(20.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            ShutterRaw.SetValue(3)
            self.assertAlmostEqual(30.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            TimeBase.SetValue(100)
            self.assertAlmostEqual(300.0, ShutterAbs.GetValue(), delta=self.FLOAT64_EPSILON)

            # Writing
            ShutterAbs.SetValue(400.0)
            self.assertEqual(4, ShutterRaw.GetValue())


        # CPPUNIT_NS_BEGIN
        # template<>
        # struct assertion_traits< int64_autovector_t >
        # {
        #     static bool equal(const int64_autovector_t& lhs, const int64_autovector_t& rhs)
        #     {
        #         const size_t size = lhs.size()
        #         if (size != rhs.size())
        #         {
        #             return false
        #         }
        #
        #         size_t i = 0
        #         while (i < size)
        #         {
        #             if (lhs[i] != rhs[i]) break
        #             ++i
        #         }
        #         return i == size
        #     }
        #
        #     static std::string toString(const int64_autovector_t& av)
        #     {
        #         OStringStream os
        #         const size_t size = av.size()
        #         const char delimiter = ','
        #
        #         os << "("
        #         for (int i = 1 i < size ++i)
        #         {
        #             os << av[i - 1] << delimiter
        #         }
        #         if (size)
        #         {
        #             os << av[size - 1]
        #         }
        #         os << "]"
        #         return os.str()
        #     }
        # }
        # CPPUNIT_NS_END

    def test_ListOfValidValue(self):
        # if(GenApiSchemaVersion != v1_0)
        # {
        """[ GenApiTest@ConverterTestSuite_TestListOfValidValue.xml|gxml

        <Integer Name="ValueWithSet">
            <Value>16</Value>
            <Min>8</Min>
            <Max>32</Max>
            <Inc>1</Inc>
            <Representation>Linear</Representation>
            <ValidValueSet>1;2;4;8;16;22;64</ValidValueSet>
        </Integer>
        <IntConverter Name="Converter">
          <FormulaTo>FROM/10</FormulaTo>
          <FormulaFrom>TO * 10</FormulaFrom>
          <pValue>ValueWithSet</pValue>
          <Representation>Linear</Representation>
          <Slope>Increasing</Slope>
        </IntConverter>
        <Integer Name="ValueWithNoSet">
            <Value>16</Value>
            <Min>8</Min>
            <Max>32</Max>
            <Inc>1</Inc>
            <Representation>Linear</Representation>
        </Integer>
        <IntConverter Name="ConverterNoSet">
          <FormulaTo>FROM/10</FormulaTo>
          <FormulaFrom>TO * 10</FormulaFrom>
          <pValue>ValueWithNoSet</pValue>
          <Representation>Linear</Representation>
          <Slope>Increasing</Slope>
        </IntConverter>
        <Converter Name="FloatConverter">
          <FormulaTo>FROM*10</FormulaTo>
          <FormulaFrom>TO / 10</FormulaFrom>
          <pValue>ValueWithSet</pValue>
          <Representation>Linear</Representation>
          <Slope>Increasing</Slope>
        </Converter>
        <Converter Name="FloatConverter2">
          <FormulaTo>FROM*10</FormulaTo>
          <FormulaFrom>TO / 10</FormulaFrom>
          <pValue>FloatConverter</pValue>
          <Representation>Linear</Representation>
          <Slope>Increasing</Slope>
        </Converter>
        """

        Camera = CNodeMapRef()

        Camera._LoadXMLFromFile("GenApiTest", "ConverterTestSuite_TestListOfValidValue")

        Value = Camera.GetNode("Converter")
        self.assertEqual(listIncrement, Value.GetIncMode())

        valueList = Value.GetListOfValidValues()
        self.assertEqual(3, len(valueList))

        self.assertEqual(80, valueList[0])
        self.assertEqual(160, valueList[1])
        self.assertEqual(220, valueList[2])
        # self.assertEqual( valueList, refValue.GetListOfValidValues() )
        # self.assertEqual( 80, refValue.GetListOfValidValues()[0] )
        # self.assertEqual( (size_t)7, refValue.GetListOfValidValues( false ).size() )

        Value = Camera.GetNode("ConverterNoSet")
        # self.assertEqual( fixedIncrement, Value.GetIncMode())

        valueList = Value.GetListOfValidValues()
        self.assertEqual(0, len(valueList))

        # CFloatRef refFloatValue
        # double_autovector_t floatList

        FloatValue = Camera.GetNode("FloatConverter")
        # refFloatValue.SetReference(ptrFloatValue)
        # self.assertEqual(listIncrement, FloatValue.GetIncMode())
        # self.assertEqual(listIncrement, refFloatValue.GetIncMode())

        floatList = FloatValue.GetListOfValidValues()
        self.assertEqual(3, len(floatList))

        # double_autovector_t boundedFloatList( refFloatValue.GetListOfValidValues( true ) )
        # double_autovector_t fullFloatList( refFloatValue.GetListOfValidValues( false ) )
        # self.assertEqual( (size_t)3, boundedFloatList.size() )
        # self.assertEqual( (size_t)7, fullFloatList.size() )
        # self.assertEqual( floatList[0], boundedFloatList[0] )
        # self.assertEqual( floatList[1], boundedFloatList[1] )
        # self.assertEqual( floatList[2], boundedFloatList[2] )

        self.assertAlmostEqual(0.8, floatList[0], delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(1.6, floatList[1], delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(2.2, floatList[2], delta=self.FLOAT64_EPSILON)

        FloatValue = Camera.GetNode("FloatConverter2")
        # self.assertEqual( listIncrement, FloatValue.GetIncMode() )

        floatList = FloatValue.GetListOfValidValues()
        self.assertEqual(3, len(floatList))

        self.assertAlmostEqual(0.08, floatList[0], delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(0.16, floatList[1], delta=self.FLOAT64_EPSILON)
        self.assertAlmostEqual(0.22, floatList[2], delta=self.FLOAT64_EPSILON)
        # }


# 
# template<typename _Tx, typename _Ty>
# def CheckAutoVector( _Ty& v1, _Ty& v2 )
# {
#     for( size_t i=0 i<v1.size() i++ )
#     {
#         v1[i] = static_cast<_Tx>(i)
#         v2[i] = static_cast<_Tx>(i + 100)
#         self.assertTrue( v1[i] != v2[i] )
#     }
# 
#     v1 = v1
# 
#     for( size_t i=0 i<v1.size() i++ )
#     {
#         self.assertTrue( v1[i] != v2[i] )
#     }
# 
#     const _Ty& v1Const = v1
#     const _Ty& v2Const = v2
# 
#     for( size_t i=0 i<v1.size() i++ )
#     {
#         self.assertTrue( v1Const[i] != v2Const[i] )
#     }
# 
#     _Ty v1Copy(v1)
#     for( size_t i=0 i<v1.size() i++ )
#     {
#         self.assertTrue( v1[i] == v1Copy[i] )
#     }
# 
#     v1 = v2
# 
#     for( size_t i=0 i<v1.size() i++ )
#     {
#         self.assertTrue( v1Const[i] == v2Const[i] )
#     }
# 
#     _Ty v1Default
#     self.assertEqual( size_t(0), v1Default.size() )
# }
# 
# def ConverterTestSuite::TestAutoVectorInt64()
# {
#     static const size_t cnt = 2
#     int64_autovector_t v1(cnt)
#     int64_autovector_t v2(cnt)
# 
#     CheckAutoVector<int64_t, int64_autovector_t>( v1, v2 )
# }
# 
# def ConverterTestSuite::TestAutoVectorDouble()
# {
#     static const size_t cnt = 2
#     double_autovector_t v1(cnt)
#     double_autovector_t v2(cnt)
# 
#     CheckAutoVector<double, double_autovector_t>( v1, v2 )
# }

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
