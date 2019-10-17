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
from _locale import LC_ALL
from locale import setlocale


class SwissKnifeTestSuite(GenicamTestCase):
    def test_SwissKnife(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnife.xml|gxml
    
            <Integer Name="Int0">
                <Value>2</Value>
            </Integer>
    
            <Integer Name="Int1">
                <Value>-2</Value>
            </Integer>
    
            <Float Name="Dbl0">
                <Value>0.5</Value>
            </Float>
    
            <Float Name="Dbl1">
                <Value>-0.5</Value>
            </Float>
    
            <IntSwissKnife Name="SwsNoVarInt">
                <Formula>((3-4)*(2+(-1)))/(6-5)</Formula>
            </IntSwissKnife>
    
            <IntSwissKnife Name="SwsMultDivInt">
                <pVariable Name="V0">Int0</pVariable>
                <pVariable Name="V1">Int1</pVariable>
                <Formula>-1*((V0*V1)/(V1*V0))</Formula>
            </IntSwissKnife>
    
            <IntSwissKnife Name="SwsAddSubInt">
                <pVariable Name="SK0">SwsMultDivInt</pVariable>
                <Formula>(SK0 + SK0) - (SK0 + SK0)</Formula>
            </IntSwissKnife>
    
            <IntSwissKnife Name="SwsBitsInt">
                <pVariable Name="SK0">Int0</pVariable>
                <pVariable Name="SK1">Int1</pVariable>
                <Formula>SK0/SK1*(0x01||(((((~(SK0^0x03)=SK1))+SK0-SK1)>>SK0)>0))%SK1</Formula>
            </IntSwissKnife>
    
            <SwissKnife Name="SwsNoVarDbl">
                <Formula>((3.0-4.0)*(2+(-1.0)))/(6.0-0x05)</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsMultDivDbl">
                <pVariable Name="V0">Dbl0</pVariable>
                <pVariable Name="V1">Int1</pVariable>
                <Formula>neg((V0*V1)/(V1*V0))</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsAddSubDbl">
                <pVariable Name="SK0">SwsMultDivInt</pVariable>
                <pVariable Name="SK1">Int0</pVariable>
                <Formula>(SK0 + SK1) - (SK1 + SK0)</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsTrigDbl">
                <pVariable Name="SK0">SwsMultDivDbl</pVariable>
                <pVariable Name="SK1">Int1</pVariable>
                <Formula>SK1*atan(tan(asin(sin(acos(cos(PI*(SK0)))/PI))))/SK1</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsTruncFracDbl">
                <pVariable Name="SK0">Dbl1</pVariable>
                <pVariable Name="SK1">SwsAddSubInt</pVariable>
                <Formula>(trunc(SK0*3) + frac(SK0*3))+SK1</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsCeilFloorDbl">
                <pVariable Name="SK0">Dbl1</pVariable>
                <pVariable Name="SK1">Int0</pVariable>
                <Formula>(ceil(SK0)*SK1 - floor(SK0)*SK1)/SK1</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsRoundDbl">
                <pVariable Name="SK0">Dbl0</pVariable>
                <pVariable Name="SK1">Int0</pVariable>
                <Formula>round(SK0+SK1)-SK1</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsSqrtDbl">
                <pVariable Name="SK0">Dbl0</pVariable>
                <pVariable Name="SK1">Int0</pVariable>
                <Formula>sqrt(SK0*SK1)</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsPowersDbl">
                <pVariable Name="SK0">Dbl0</pVariable>
                <pVariable Name="SK1">Int0</pVariable>
                <Formula>ln(lg(SK1*5)*e*exp(SK0*2))</Formula>
            </SwissKnife>
    
            <SwissKnife Name="SwsNegSgnDbl">
                <pVariable Name="SK0">Dbl1</pVariable>
                <pVariable Name="SK1">SwsMultDivInt</pVariable>
                <Formula>(neg(SK0)*sgn(SK0))*neg(SK1)</Formula>
                <Unit>s</Unit>
                <Representation>Linear</Representation>
                <DisplayNotation>Fixed</DisplayNotation>
            </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnife")

        Int0 = Camera.GetNode("Int0")
        Int1 = Camera.GetNode("Int1")
        Dbl0 = Camera.GetNode("Dbl0")
        Dbl1 = Camera.GetNode("Dbl1")

        SwsNoVarInt = Camera.GetNode("SwsNoVarInt")
        SwsMultDivInt = Camera.GetNode("SwsMultDivInt")
        SwsAddSubInt = Camera.GetNode("SwsAddSubInt")
        SwsBitsInt = Camera.GetNode("SwsBitsInt")

        SwsNoVarDbl = Camera.GetNode("SwsNoVarDbl")
        SwsMultDivDbl = Camera.GetNode("SwsMultDivDbl")
        SwsAddSubDbl = Camera.GetNode("SwsAddSubDbl")
        SwsTrigDbl = Camera.GetNode("SwsTrigDbl")
        SwsTruncFracDbl = Camera.GetNode("SwsTruncFracDbl")
        SwsCeilFloorDbl = Camera.GetNode("SwsCeilFloorDbl")
        SwsRoundDbl = Camera.GetNode("SwsRoundDbl")
        SwsSqrtDbl = Camera.GetNode("SwsSqrtDbl")
        SwsPowersDbl = Camera.GetNode("SwsPowersDbl")
        SwsNegSgnDbl = Camera.GetNode("SwsNegSgnDbl")

        # Check functional correctness and SwissKnife nesting
        noVarInt = -1
        multDivInt = -1
        addSubInt = 0
        bitsInt = -1

        noVarDbl = -1.0
        multDivDbl = -1.0
        addSubDbl = 0.0
        trigDbl = 1.0
        truncFracDbl = -1.5
        ceilFloorDbl = 1.0
        roundDbl = 1.0
        sqrtDbl = 1.0
        powersDbl = 2.0
        negSgnDbl = -0.5

        with self.assertRaises(GenericException):
            SwsNoVarInt.SetValue(77)
        self.assertEqual(noVarInt, SwsNoVarInt.GetValue())
        self.assertEqual(multDivInt, SwsMultDivInt.GetValue())
        self.assertEqual(addSubInt, SwsAddSubInt.GetValue())
        self.assertEqual(bitsInt, SwsBitsInt.GetValue())

        with self.assertRaises(GenericException):
            SwsNoVarDbl.SetValue(7.7)
        self.assertEqual(noVarDbl, SwsNoVarDbl.GetValue())
        self.assertEqual(multDivDbl, SwsMultDivDbl.GetValue())
        self.assertEqual(addSubDbl, SwsAddSubDbl.GetValue())
        self.assertEqual(trigDbl, SwsTrigDbl.GetValue())
        self.assertEqual(truncFracDbl, SwsTruncFracDbl.GetValue())
        self.assertEqual(ceilFloorDbl, SwsCeilFloorDbl.GetValue())
        self.assertEqual(roundDbl, SwsRoundDbl.GetValue())
        self.assertEqual(sqrtDbl, SwsSqrtDbl.GetValue())
        self.assertEqual(powersDbl, SwsPowersDbl.GetValue())
        self.assertEqual(negSgnDbl, SwsNegSgnDbl.GetValue())

    def test_Minimum(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestMinimum.xml|gxml
    
        <SwissKnife Name="SwsConstFormula">
            <Formula>((3.0-4.0)+1.0) = 0.0</Formula>
        </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestMinimum")
        SwsConstFormula = Camera.GetNode("SwsConstFormula")
        minimum = SwsConstFormula.GetMin()
        maximum = SwsConstFormula.GetMax()
        value = SwsConstFormula.GetValue()
        self.assertAlmostEqual(-minimum, maximum, delta=1e-6)
        self.assertEqual(value, 1)
        self.assertEqual(intfIFloat, SwsConstFormula.GetNode().GetPrincipalInterfaceType())

    def test_SwissKnifeBrokenBitOps(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnifeBrokenBitOps.xml|gxml
    
            <Integer Name="Int0">
                <Value>2</Value>
            </Integer>
    
            <Integer Name="Int1">
                <Value>-2</Value>
            </Integer>
    
            <IntSwissKnife Name="SwsBrokenBitOpsInt">
                <pVariable Name="SK0">Int0</pVariable>
                <pVariable Name="SK1">Int1</pVariable>
                <Formula><![CDATA[ ((((SK0<<1) & 0x01) <= (SK1<0)) >=0 ) && 1 ]]></Formula>
        <!--  here an alternative formulation -->
        <!--         <Formula>((((SK0&lt&lt1)&amp0x01)&lt=(SK1&lt0))&gt=0)&amp&amp1</Formula> -->
            </IntSwissKnife>
        <!-- operators not tested: $" "?" ":" "," "" "/ *" ":=" "<>" "**" -->
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnifeBrokenBitOps")
        SwsBrokenBitOpsInt = Camera.GetNode("SwsBrokenBitOpsInt")
        # Check additional bit operations
        # Integers have a easy to calculate expected values for bit operations
        brokenBitOpsInt = 1
        self.assertEqual(brokenBitOpsInt, SwsBrokenBitOpsInt.GetValue())

    def test_SwissKnifeVariableMinMax(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnifeVariableMinMax.xml|gxml
    
            <Integer Name="Int1">
                <Value>-2</Value>
            </Integer>
    
            <Float Name="Dbl0">
                <Value>0.5</Value>
                <Min>1</Min>
                <Max>2</Max>
            </Float>
    
            <SwissKnife Name="SwsMultDivDbl">
                <pVariable Name="V0">Dbl0</pVariable>
                <pVariable Name="V1">Int1</pVariable>
                <Formula>neg((V0*V1)/(V1*V0))</Formula>
            </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnifeVariableMinMax")
        SwsMultDivDbl = Camera.GetNode("SwsMultDivDbl")
        # Check that variable ranges are respected when loading variables into formulas
        multDivDbl = -1.0
        self.assertEqual(multDivDbl, SwsMultDivDbl.GetValue())

    def test_SwissKnifeVariableValue(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnifeVariableValue.xml|gxml
    
            <Integer Name="Int1">
                <Value>1</Value>
            </Integer>
    
            <Float Name="Dbl0">
                <Value>1.0</Value>
            </Float>
    
            <SwissKnife Name="SwsMultDivDbl">
                <pVariable Name="V0">Dbl0</pVariable>
                <pVariable Name="V1">Int1</pVariable>
                <Formula>neg((V0*V1)/(V1*V0))</Formula>
            </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnifeVariableValue")
        SwsMultDivDbl = Camera.GetNode("SwsMultDivDbl")
        # Check that variable values are defined
        multDivDbl = -1.0
        self.assertEqual(multDivDbl, SwsMultDivDbl.GetValue())

    def test_SwissKnifeArgumentType(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnifeArgumentType.xml|gxml
    
            <Float Name="Dbl1">
                <Value>1.0</Value>
            </Float>
    
            <Integer Name="Int0">
                <Value>1</Value>
            </Integer>
    
            <SwissKnife Name="SwsMultDivDbl">
                <pVariable Name="V0">Dbl1</pVariable>
                <pVariable Name="V1">Int0</pVariable>
                <Formula>neg((V0*V1)/(V1*V0))</Formula>
            </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnifeArgumentType")
        SwsMultDivDbl = Camera.GetNode("SwsMultDivDbl")
        # Check that the arguments in the formula are all supported types
        multDivDbl = -1.0
        self.assertEqual(multDivDbl, SwsMultDivDbl.GetValue())

    def test_SwissKnifeGetSetProperties(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestSwissKnifeGetSetProperties.xml|gxml
    
        <SwissKnife Name="Result">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <Formula> X * Y + 42 </Formula>
            <Unit>s</Unit>
            <Representation>Linear</Representation>
            <DisplayNotation>Fixed</DisplayNotation>
            <DisplayPrecision>1</DisplayPrecision>
        </SwissKnife>
    
        <Float Name="ValueX">
        <Value>3</Value>
        </Float>
    
        <Integer Name="ValueY">
        <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestSwissKnifeGetSetProperties")

        Result = Camera.GetNode("Result")

        mVal = ""
        mAttribute = ""

        mVal, mAttribute = Result.GetNode().GetProperty("Name")
        self.assertTrue(mVal == "Result")

        mVal, mAttribute = Result.GetNode().GetProperty("Unit")
        self.assertTrue(mVal == "s")

        mVal, mAttribute = Result.GetNode().GetProperty("Representation")
        self.assertTrue(mVal == "Linear")

        mVal, mAttribute = Result.GetNode().GetProperty("DisplayNotation")
        self.assertTrue(mVal == "Fixed")

        mVal, mAttribute = Result.GetNode().GetProperty("DisplayPrecision")
        self.assertTrue(mVal == "1")

    def test_ValueAccess(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestValueAccess.xml|gxml
    
        <SwissKnife Name="Result">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <Formula> X * Y + 12 </Formula>
        </SwissKnife>
    
        <Float Name="ValueX">
            <Value>3</Value>
        </Float>
    
        <Integer Name="ValueY">
            <Value>10</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestValueAccess")

        Result = Camera.GetNode("Result")
        ResultNode = Result

        self.assertEqual(42.0, Result.GetValue())

        # LOG_PERFORMANCE("-------------------------------------------------")
        # LOG_PERFORMANCE("Setup : SwissKnife <=> Integer (X = const)")
        # LOG_PERFORMANCE("                   <=> Integer (Y = const)")

        ResultNode.Node.InvalidateNode()
        # TEST_BEGIN(1000)
        #    """double Result = """Result.GetValue()
        #    StopWatch.PauseBegin()
        #    ResultNode.InvalidateNode()
        #    StopWatch.PauseEnd()
        # TEST_END( SwissKnife::GetValue (dynamic, without caching) )

    def test_IntSwissKnifeTrig(self):
        """[ GenApiTest@TestIntSwissKnifeTrig.xml|gxml
    
            <Integer Name="Int0">
                <Value>2</Value>
            </Integer>
    
            <Integer Name="Int1">
                <Value>-2</Value>
            </Integer>
    
            <IntSwissKnife Name="SwsMultDivInt">
                <pVariable Name="V0">Int0</pVariable>
                <pVariable Name="V1">Int1</pVariable>
                <Formula>-1*((V0*V1)/(V1*V0))</Formula>
            </IntSwissKnife>
    
            <IntSwissKnife Name="SwsTrigInt">
                <pVariable Name="SK0">SwsMultDivInt</pVariable>
                <Formula>atan(tan(asin(sin(acos(cos(PI*(SK0)))/PI))))</Formula>
            </IntSwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "TestIntSwissKnifeTrig")

        SwsMultDivInt = Camera.GetNode("SwsMultDivInt")
        SwsTrigInt = Camera.GetNode("SwsTrigInt")

        # Check trig parsing for IntSwsKnife
        multDivInt = -1
        self.assertEqual(multDivInt, SwsMultDivInt.GetValue())

        # Beware: an IntSwissKnife does not support float functions like sin, cos etc.
        with self.assertRaises(LogicalErrorException):
            SwsTrigInt.GetValue()

    # Pleora FG
    # ---------------------------------------------------------------------------
    # This method tests is used to trig cases where not all variables
    # are present in order to evaluate an expression. This will trigger
    # some yet-to-be-covered cases in VariableDelegate.cpp
    #
    def test_VariableDelegates(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestVariableDelegates.xml|gxml
        <Boolean Name ="FalseNode">
          <Value>false</Value>
        </Boolean>
    
        <Float Name="Float0">
          <Value>4</Value>
        </Float>
        <Float Name="Float1">
          <Value>2</Value>
        </Float>
        <SwissKnife Name="SwsAdd">
          <pVariable Name="V0">Float0</pVariable>
          <pVariable Name="V1">Float1</pVariable>
          <Formula>V0+V1</Formula>
          <Representation>Linear</Representation>
        </SwissKnife>
    
        <Float Name="FloatNotAvailable">
          <pIsAvailable>FalseNode</pIsAvailable>
          <Value>3</Value>
        </Float>
        <SwissKnife Name="SwsAddNA">
          <pVariable Name="V0">Float0</pVariable>
          <pVariable Name="V1">FloatNotAvailable</pVariable>
          <Formula>V0+V1</Formula>
        </SwissKnife>
    
        <Float Name="FloatNotImplemented">
          <pIsImplemented>FalseNode</pIsImplemented>
          <Value>3</Value>
        </Float>
        <SwissKnife Name="SwsAddNI">
          <pVariable Name="V0">Float0</pVariable>
          <pVariable Name="V1">FloatNotImplemented</pVariable>
          <Formula>V0+V1</Formula>
        </SwissKnife>
    
        <Float Name="FloatReadOnly">
          <ImposedAccessMode>RO</ImposedAccessMode>
          <Value>3</Value>
        </Float>
        <SwissKnife Name="SwsAddRO">
          <pVariable Name="V0">Float0</pVariable>
          <pVariable Name="V1">FloatReadOnly</pVariable>
          <Formula>V0+V1</Formula>
        </SwissKnife>
    
        <SwissKnife Name="SwsBadFormula">
          <pVariable Name="V0">Float0</pVariable>
          <pVariable Name="V1">Float1</pVariable>
          <Formula>ITALY2GERMANY0</Formula>
        </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestVariableDelegates")

        # Regular float
        SwsAdd = Camera.GetNode("SwsAdd")
        self.assertTrue(SwsAdd.GetAccessMode() == RO)
        self.assertTrue(SwsAdd.GetRepresentation() == Linear)
        """double lMin = """
        SwsAdd.GetMin()
        """double lMax = """
        SwsAdd.GetMax()
        lUnit = SwsAdd.GetUnit()
        with self.assertRaises(AccessException):
            SwsAdd.SetValue(1.0)
        with self.assertRaises(AccessException):
            SwsAdd.FromString("1.0")
        lStrVal = SwsAdd.ToString()

        # NI float
        SwsAddNI = Camera.GetNode("SwsAddNI")
        self.assertTrue(SwsAddNI.GetAccessMode() == NI)

        # NA float
        SwsAddNA = Camera.GetNode("SwsAddNA")
        self.assertTrue(SwsAddNA.GetAccessMode() == NA)

        # RO float
        SwsAddRO = Camera.GetNode("SwsAddRO")
        self.assertTrue(SwsAddRO.GetAccessMode() == RO)

        # Bad formula
        SwsBadFormula = Camera.GetNode("SwsBadFormula")
        with self.assertRaises(LogicalErrorException):
            SwsBadFormula.GetValue()

    def test_VariableNames(self):
        """[ GenApiTest@SwissKnifeTestSuite_VariableNames_GoodExamples.xml|gxml

            <IntSwissKnife Name="Knife1">
                <pVariable Name="BLADE">Blade</pVariable>
                <Formula>100*BLADE</Formula>
            </IntSwissKnife>

            <IntSwissKnife Name="Knife2">
                <pVariable Name="BLADE2">Blade</pVariable>
                <Formula>100*BLADE2</Formula>
            </IntSwissKnife>

            <IntSwissKnife Name="Knife3">
                <pVariable Name="BLADE_">Blade</pVariable>
                <Formula>100*BLADE_</Formula>
            </IntSwissKnife>

            <Integer Name="Blade">
                <Value>1</Value>
            </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_VariableNames_GoodExamples")

        Blade = Camera.GetNode("Knife1")
        self.assertTrue(bool(Blade))
        self.assertEqual(100, Blade.GetValue())

        Blade = Camera.GetNode("Knife2")
        self.assertTrue(bool(Blade))
        self.assertEqual(100, Blade.GetValue())

        Blade = Camera.GetNode("Knife3")
        self.assertTrue(bool(Blade))
        self.assertEqual(100, Blade.GetValue())

        """[ GenApiTest@SwissKnifeTestSuite_VariableNames_BadExamples.xml|gxml

            <IntSwissKnife Name="Knife">
                <pVariable Name="blade">Blade</pVariable>
                <Formula>100*blade</Formula>
            </IntSwissKnife>

        """

        Camera = CNodeMapRef()
        with self.assertRaises(GenericException):
            Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_VariableNames_BadExamples")

    # Mantis #288
    def test_VariableNames2(self):
        # the implementation belonging to schema v1.0 can handle uppercase names only
        # if( GenApiSchemaVersion == v1_0 )
        #    return

        """[ GenApiTest@SwissKnifeTestSuite_TestVariableNames.xml|gxml
                <SwissKnife Name="Knife1">
                    <pVariable Name="BLADE">Blade</pVariable>
                    <Formula>100*BLADE</Formula>
                </SwissKnife>
                <SwissKnife Name="Knife2">
                    <pVariable Name="bLaDe">Blade</pVariable>
                    <Formula>100*bLaDe</Formula>
                </SwissKnife>
                <SwissKnife Name="Knife3">
                    <pVariable Name="blade">Blade</pVariable>
                    <Formula>100*blade</Formula>
                </SwissKnife>
                <SwissKnife Name="Knife4">
                    <pVariable Name="BLADE">Blade</pVariable>
                    <Formula>100*Blade</Formula>
                </SwissKnife>
    
                <Integer Name="Blade">
                    <Value>1</Value>
                </Integer>
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestVariableNames")

        Blade = Camera.GetNode("Knife1")
        self.assertTrue(bool(Blade))
        self.assertEqual(100.0, Blade.GetValue())

        Blade = Camera.GetNode("Knife2")
        self.assertTrue(bool(Blade))
        self.assertEqual(100.0, Blade.GetValue())

        Blade = Camera.GetNode("Knife3")
        self.assertTrue(bool(Blade))
        self.assertEqual(100.0, Blade.GetValue())

        Blade = Camera.GetNode("Knife4")
        self.assertTrue(bool(Blade))
        with self.assertRaises(LogicalErrorException):
            Blade.GetValue()

    def test_ConstantAndExpression(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@SwissKnifeTestSuite_TestConstantAndExpression.xml|gxml
    
        <SwissKnife Name="Result">
            <pVariable Name="X">ValueX</pVariable>
            <pVariable Name="Y">ValueY</pVariable>
            <Constant Name="Two">2.0</Constant>
            <Expression Name="TwoX">2.0*X</Expression>
            <Formula> TwoX * Y + Two </Formula>
        </SwissKnife>
    
        <Float Name="ValueX">
            <Value>5.0</Value>
        </Float>
    
        <Float Name="ValueY">
            <Value>4.0</Value>
        </Float>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestConstantAndExpression")

        Result = Camera.GetNode("Result")
        ResultNode = Result

        self.assertEqual(42.0, Result.GetValue())

    # Added with std::vector change in Int64MathParser
    def test_Big(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestBig.xml|gxml
    
        <Integer Name="MySelector">
            <Value>0</Value>
        </Integer>
    
        <SwissKnife Name="MyBigSwissKnife">
            <pVariable Name="SEL">MySelector</pVariable>
            <Formula>
            (SEL = 0) ? 0.0 : ((SEL = 1) ? 0.0 : ((SEL = 2) ? 0.0 : ((SEL = 3) ? 0.0 : 
            ((SEL = 4) ? 0.0 : ((SEL = 5) ? 0.0 : ((SEL = 6) ? 0.0 : ((SEL = 7) ? 0.0 : ((SEL = 8) ? 0.0 :
            ((SEL = 9) ? 0.0 : ((SEL = 10) ? 0.0 : ((SEL = 11) ? 0.0 : ((SEL = 12) ? 0.0 : 
            ((SEL = 13) ? 0.0 : ((SEL = 14) ? 0.0 : ((SEL = 15) ? 0.0 : ((SEL = 16) ? 0.0 : 
            ((SEL = 17) ? 0.0 : ((SEL = 18) ? 0.0 : ((SEL = 19) ? 0.0 : ((SEL = 20) ? 0.0 : 
            ((SEL = 21) ? 0.0 : ((SEL = 22) ? 0.0 : ((SEL = 23) ? 0.0 : ((SEL = 24) ? 0.0 : 
            ((SEL = 25) ? 0.0 : ((SEL = 26) ? 0.0 : ((SEL = 27) ? 0.0 : ((SEL = 28) ? 0.0 : 
            ((SEL = 29) ? 0.0 : ((SEL = 30) ? 0.0 : ((SEL = 31) ? 0.0 : ((SEL = 32) ? 0.0 : 
            ((SEL = 33) ? 0.0 : ((SEL = 34) ? 0.0 : ((SEL = 35) ? 0.0 : ((SEL = 36) ? 0.0 : 
            ((SEL = 37) ? 0.0 : ((SEL = 38) ? 0.0 : ((SEL = 39) ? 0.0 : ((SEL = 40) ? 0.0 : 
            ((SEL = 41) ? 0.0 : ((SEL = 42) ? 3.1416 : ((SEL = 43) ? 0.0 : ((SEL = 44) ? 0.0 : 
            ((SEL = 45) ? 0.0 : ((SEL = 46) ? 0.0 : ((SEL = 47) ? 0.0 : ((SEL = 48) ? 0.0 : 
            ((SEL = 49) ? 0.0 : ((SEL = 50) ? 0.0 : ((SEL = 51) ? 0.0 : ((SEL = 52) ? 0.0 : 
            ((SEL = 53) ? 0.0 : ((SEL = 54) ? 0.0 : ((SEL = 55) ? 0.0 : ((SEL = 56) ? 0.0 : 
            ((SEL = 57) ? 0.0 : ((SEL = 58) ? 0.0 : ((SEL = 59) ? 0.0 : ((SEL = 60) ? 0.0 : 
            ((SEL = 61) ? 0.0 : ((SEL = 62) ? 0.0 : ((SEL = 63) ? 0.0 : ((SEL = 64) ? 0.0 : 
            ((SEL = 65) ? 0.0 : ((SEL = 66) ? 0.0 : ((SEL = 67) ? 0.0 : ((SEL = 68) ? 0.0 : 
            ((SEL = 69) ? 0.0 : ((SEL = 70) ? 0.0 : ((SEL = 71) ? 0.0 : ((SEL = 72) ? 0.0 : 
            ((SEL = 73) ? 0.0 : ((SEL = 74) ? 0.0 : ((SEL = 75) ? 0.0 : ((SEL = 76) ? 0.0 : 
            ((SEL = 77) ? 0.0 : ((SEL = 78) ? 0.0 : ((SEL = 79) ? 0.0 : ((SEL = 80) ? 0.0 : 
            ((SEL = 81) ? 0.0 : ((SEL = 82) ? 0.0 : ((SEL = 83) ? 0.0 : ((SEL = 84) ? 0.0 : 
            ((SEL = 85) ? 0.0 : ((SEL = 86) ? 0.0 : ((SEL = 87) ? 0.0 : ((SEL = 88) ? 0.0 : 
            ((SEL = 89) ? 0.0 : ((SEL = 90) ? 0.0 : ((SEL = 91) ? 0.0 : ((SEL = 92) ? 0.0 : 
            ((SEL = 93) ? 0.0 : ((SEL = 94) ? 0.0 : ((SEL = 95) ? 0.0 : ((SEL = 96) ? 0.0 : 
            ((SEL = 97) ? 0.0 : ((SEL = 98) ? 0.0 : ((SEL = 99) ? 0.0 : ((SEL = 100) ? 0.0 : 
            ((SEL = 101) ? 0.0 : ((SEL = 102) ? 0.0 : ((SEL = 103) ? 0.0 : ((SEL = 104) ? 0.0 : 
            ((SEL = 105) ? 0.0 : ((SEL = 106) ? 0.0 : ((SEL = 107) ? 0.0 : ((SEL = 108) ? 0.0 : 
            ((SEL = 109) ? 0.0 : ((SEL = 110) ? 0.0 : ((SEL = 111) ? 0.0 : ((SEL = 112) ? 0.0 : 
            ((SEL = 113) ? 0.0 : ((SEL = 114) ? 0.0 : ((SEL = 115) ? 0.0 : ((SEL = 116) ? 0.0 : 
            ((SEL = 117) ? 0.0 : ((SEL = 118) ? 0.0 : ((SEL = 119) ? 0.0 : ((SEL = 120) ? 0.0 : 
            ((SEL = 121) ? 0.0 : ((SEL = 122) ? 0.0 : ((SEL = 123) ? 0.0 : ((SEL = 124) ? 0.0 : 
            ((SEL = 125) ? 0.0 : ((SEL = 126) ? 0.0 : ((SEL = 127) ? 0.0 : (-1.0))))))))))))))))))
            ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
            ))))))))))))))))))))))))</Formula>
        </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestBig")

        lSelector = Camera.GetNode("MySelector")
        self.assertTrue(lSelector != None)

        lSwissKnife = Camera.GetNode("MyBigSwissKnife")
        self.assertTrue(lSwissKnife != None)

        lSelector.SetValue(0)
        lValue = lSwissKnife.GetValue()
        # self.assertTrue( fabs( lValue ) < 0.000001 )

        lSelector.SetValue(42)
        lValue = lSwissKnife.GetValue()
        # self.assertTrue( fabs( lValue - 3.1416 ) < 0.000001 )

        lSelector.SetValue(128)
        lValue = lSwissKnife.GetValue()
        # self.assertTrue( fabs( lValue + 1.0 ) < 0.000001 )

    def test_VariableExtensions(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@SwissKnifeTestSuite_TestVariableExtensions.xml|gxml
    
        <SwissKnife Name="Knife">
            <pVariable Name="BLADE.Min">Blade</pVariable>
            <Formula>10*BLADE.Min</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeMin">
            <pVariable Name="BLADE.Min">Blade</pVariable>
            <Formula>BLADE.Min</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeMax">
            <pVariable Name="BLADE.Max">Blade</pVariable>
            <Formula>BLADE.Max</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeInc">
            <pVariable Name="BLADE.Inc">Blade</pVariable>
            <Formula>BLADE.Inc</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeVal">
            <pVariable Name="BLADE.Value">Blade</pVariable>
            <Formula>BLADE.Value</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeAccessMode">
            <pVariable Name="BLADE.AccessMode">Blade</pVariable>
            <Formula>BLADE.AccessMode</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeVisibility">
            <pVariable Name="BLADE.Visibility">Blade</pVariable>
            <Formula>BLADE.Visibility</Formula>
        </SwissKnife>
    
        <SwissKnife Name="BladeCachingMode">
            <pVariable Name="BLADE.CachingMode">Blade</pVariable>
            <Formula>BLADE.CachingMode</Formula>
        </SwissKnife>
    
        <Float Name="Blade">
            <Value>0.2</Value>
            <Min>-1.0</Min>
            <Max>1.0</Max>
            <Inc>0.1</Inc>
        </Float>
    
        <SwissKnife Name="Dagger">
            <pVariable Name="OPTSEL.Entry.Option1">OptionSelector</pVariable>
            <pVariable Name="OPTSEL.Entry.Option2">OptionSelector</pVariable>
            <Formula>OPTSEL.Entry.Option1 + OPTSEL.Entry.Option2</Formula>
        </SwissKnife>
    
        <Enumeration Name="OptionSelector">
           <EnumEntry Name="Option1">
              <Value>10</Value>
              <NumericValue>1.5</NumericValue>
           </EnumEntry>
           <EnumEntry Name="Option2">
              <Value>20</Value>
           </EnumEntry>
           <Value>10</Value>
        </Enumeration>
    
        <SwissKnife Name="DaggerNoEnum">
            <pVariable Name="Blade.Entry.Foo">Blade</pVariable>
            <Formula>Blade.Entry.Foo</Formula>
        </SwissKnife>
    
        <SwissKnife Name="DaggerNoEnumEntry">
            <pVariable Name="OptionSelector.Entry.Foo">OptionSelector</pVariable>
            <Formula>OptionSelector.Entry.Foo</Formula>
        </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestVariableExtensions")

        Knife = Camera.GetNode("Knife")
        Blade = Camera.GetNode("Blade")
        Dagger = Camera.GetNode("Dagger")

        FLOAT64_EPSILON = 7. / 3 - 4. / 3 - 1
        Blade.SetValue(-0.3)
        self.assertAlmostEqual(-10.0, Knife.GetValue(), delta=FLOAT64_EPSILON)

        # note that the ".Entry.XX" variable uses Value rather than NumericValue by design
        self.assertAlmostEqual(30.0, Dagger.GetValue(), delta=FLOAT64_EPSILON)

        BladeMin = Camera.GetNode("BladeMin")
        self.assertAlmostEqual(-1.0, BladeMin.GetValue(), delta=FLOAT64_EPSILON)

        BladeMax = Camera.GetNode("BladeMax")
        self.assertAlmostEqual(1.0, BladeMax.GetValue(), delta=FLOAT64_EPSILON)

        BladeInc = Camera.GetNode("BladeInc")
        self.assertAlmostEqual(0.1, BladeInc.GetValue(), delta=FLOAT64_EPSILON)

        BladeVal = Camera.GetNode("BladeVal")
        self.assertAlmostEqual(-0.3, BladeVal.GetValue(), delta=FLOAT64_EPSILON)

        BladeVisibility = Camera.GetNode("BladeVisibility")
        self.assertAlmostEqual(0.0, BladeVisibility.GetValue(), delta=FLOAT64_EPSILON)

        BladeAccessMode = Camera.GetNode("BladeAccessMode")
        self.assertAlmostEqual(4.0, BladeAccessMode.GetValue(), delta=FLOAT64_EPSILON)

        BladeCachingMode = Camera.GetNode("BladeCachingMode")
        self.assertAlmostEqual(WriteAround, BladeCachingMode.GetValue(), delta=FLOAT64_EPSILON)

        DaggerNoEnum = Camera.GetNode("DaggerNoEnum")
        with self.assertRaises(RuntimeException):
            DaggerNoEnum.GetValue()

        DaggerNoEnumEntry = Camera.GetNode("DaggerNoEnumEntry")
        with self.assertRaises(RuntimeException):
            DaggerNoEnumEntry.GetValue()

    def test_MathParser(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestMathParser.xml|gxml
    
        <Float Name="A">
            <Value>0.0</Value>
        </Float>
    
        <Float Name="B">
            <Value>0.0</Value>
        </Float>
    
        <Float Name="C">
            <Value>0.0</Value>
        </Float>
    
        <SwissKnife Name="BitNot">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[  ~A ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="BitAnd">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A&B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="BitOr">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A|B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="BitXor">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A^B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="BitLeft">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A<<B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="BitRight">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A>>B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Power">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A**B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Neq">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A<>B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Eq">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A=B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Geq">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A>=B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Leq">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A<=B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Greater">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A>B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Less">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A<B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="And">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A&&B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Or">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A||B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Plus">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A+B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Minus">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A-B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Times">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A*B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Div">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A/B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Mod">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A%B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Ternary">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <pVariable Name="C">C</pVariable>
            <Formula><![CDATA[ A?B:C ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Precedence1">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <pVariable Name="C">C</pVariable>
            <Formula><![CDATA[ A+B*C ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Brackets1">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <pVariable Name="C">C</pVariable>
            <Formula><![CDATA[ (A+B)*C ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Sgn">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ SGN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Neg">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ NEG(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Frac">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ FRAC(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Trunc">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ TRUNC(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Floor">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ FLOOR(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Ceil">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ CEIL(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Round">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ ROUND(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="RoundPrec">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ ROUND(A,B) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Pi">
            <Formula><![CDATA[ PI ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="E">
            <Formula><![CDATA[ E ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Abs">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ ABS(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Exp">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ EXP(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Ln">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ LN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Lg">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ LG(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Sqrt">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ SQRT(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Sin">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ SIN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Cos">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ COS(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Tan">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ TAN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Asin">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ ASIN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Acos">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ ACOS(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Atan">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ ATAN(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Digits1">
            <Formula><![CDATA[ 10.2+10+0x10+010 ]]></Formula>                 <!--  010 treated as decimal !?! -->
        </SwissKnife>
    
        <SwissKnife Name="Digits2">
            <Formula><![CDATA[ +2.2 ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Digits3">
            <Formula><![CDATA[ -2.2 ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid1">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ /A ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid2">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ A/ ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid3">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ / ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid4">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A==B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid5">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A$B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid6">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A#B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid7">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ !A ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid8">
            <pVariable Name="A">A</pVariable>
            <Formula><![CDATA[ FOOBAR(A) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid9">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ (A+B ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid10">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ A+B) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid11">
            <Formula></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid12">
            <Formula>    </Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid13">
            <Formula>1 2 3</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid14">
            <Formula>0x</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid15">
            <Formula>"abc"</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid16">
            <Formula>'abc'</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid17">
            <Formula>\* aha *\ 1</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid18">
            <Formula>'abc</Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid19">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ () ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid20">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ SGN() ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid21">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula><![CDATA[ SGN(A,B) ]]></Formula>
        </SwissKnife>
    
        <SwissKnife Name="Invalid22">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <pVariable Name="C">C</pVariable>
            <Formula><![CDATA[ ROUND(A,B,C) ]]></Formula>
        </SwissKnife>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestMathParser")

        A = Camera.GetNode("A")
        B = Camera.GetNode("B")
        C = Camera.GetNode("C")

        """BitNot = Camera.GetNode("BitNot")
        self.assertTrue( BitNot.IsValid() )
        A.SetValue (0)
        self.assertAlmostEqual (0xFFFFFFFFFFFFFFFF, BitNot.GetValue(), delta=FLOAT64_EPSILON )
        A.SetValue (0x1111111111111111)
        self.assertAlmostEqual (0xEEEEEEEEEEEEEEEE, BitNot.GetValue(), delta=FLOAT64_EPSILON )
    
        BitAnd = Camera.GetNode("BitAnd")
        self.assertTrue( BitAnd.IsValid() )
        A.SetValue (0xCCCCCCCCCCCCCCCC)
        B.SetValue (0xAAAAAAAAAAAAAAAA)
        self.assertEqual (0x8888888888888888, BitAnd.GetValue(), delta=FLOAT64_EPSILON )
    
        BitOr = Camera.GetNode("BitOr")
        self.assertTrue( BitOr.IsValid() )
        A.SetValue (0xCCCCCCCCCCCCCCCC)
        B.SetValue (0xAAAAAAAAAAAAAAAA)
        self.assertAlmostEqual (0xEEEEEEEEEEEEEEEE, BitOr.GetValue(), delta=FLOAT64_EPSILON )
    
        BitXor = Camera.GetNode("BitXor")
        self.assertTrue( BitXor.IsValid() )
        A.SetValue (0xCCCCCCCCCCCCCCCC)
        B.SetValue (0xAAAAAAAAAAAAAAAA)
        self.assertAlmostEqual (0x6666666666666666, BitXor.GetValue(), delta=FLOAT64_EPSILON )
    
        BitLeft = Camera.GetNode("BitLeft")
        self.assertTrue( BitLeft.IsValid() )
        A.SetValue (1)
        B.SetValue (2)
        self.assertAlmostEqual (4, BitLeft.GetValue(), delta=FLOAT64_EPSILON )
    
        BitRight = Camera.GetNode("BitRight")
        self.assertTrue( BitRight.IsValid() )
        A.SetValue (8)
        B.SetValue (2)
        self.assertAlmostEqual (2, BitRight.GetValue(), delta=FLOAT64_EPSILON )"""

        FLOAT64_EPSILON = 7. / 3 - 4. / 3 - 1

        Power = Camera.GetNode("Power")
        A.SetValue(3)
        B.SetValue(2)
        self.assertAlmostEqual(9, Power.GetValue(), delta=FLOAT64_EPSILON)

        Neq = Camera.GetNode("Neq")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(1, Neq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(0, Neq.GetValue(), delta=FLOAT64_EPSILON)

        Eq = Camera.GetNode("Eq")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(0, Eq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(1, Eq.GetValue(), delta=FLOAT64_EPSILON)

        Geq = Camera.GetNode("Geq")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(0, Geq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(1, Geq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(1, Geq.GetValue(), delta=FLOAT64_EPSILON)

        Leq = Camera.GetNode("Leq")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(1, Leq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(1, Leq.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(0, Leq.GetValue(), delta=FLOAT64_EPSILON)

        Greater = Camera.GetNode("Greater")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(0, Greater.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(0, Greater.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(1, Greater.GetValue(), delta=FLOAT64_EPSILON)

        Less = Camera.GetNode("Less")
        A.SetValue(1)
        B.SetValue(2)
        self.assertAlmostEqual(1, Less.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(0, Less.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(0, Less.GetValue(), delta=FLOAT64_EPSILON)

        And = Camera.GetNode("And")
        A.SetValue(-5)
        B.SetValue(7)
        self.assertAlmostEqual(1, And.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(0, And.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(0)
        self.assertAlmostEqual(0, And.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(0, And.GetValue(), delta=FLOAT64_EPSILON)

        Or = Camera.GetNode("Or")
        A.SetValue(-5)
        B.SetValue(7)
        self.assertAlmostEqual(1, Or.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        self.assertAlmostEqual(1, Or.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(0)
        self.assertAlmostEqual(0, Or.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(1)
        self.assertAlmostEqual(1, Or.GetValue(), delta=FLOAT64_EPSILON)

        Plus = Camera.GetNode("Plus")
        A.SetValue(25.2)
        B.SetValue(7)
        self.assertAlmostEqual(32.2, Plus.GetValue(), delta=FLOAT64_EPSILON)

        Minus = Camera.GetNode("Minus")
        A.SetValue(25.2)
        B.SetValue(7)
        self.assertAlmostEqual(18.2, Minus.GetValue(), delta=FLOAT64_EPSILON)

        Times = Camera.GetNode("Times")
        A.SetValue(25.2)
        B.SetValue(7)
        self.assertAlmostEqual(176.4, Times.GetValue(), delta=FLOAT64_EPSILON)

        Div = Camera.GetNode("Div")
        A.SetValue(15)
        B.SetValue(6)
        self.assertAlmostEqual(2.5, Div.GetValue(), delta=FLOAT64_EPSILON)
        B.SetValue(0)
        with self.assertRaises(GenericException):
            Div.GetValue()

        Mod = Camera.GetNode("Mod")
        A.SetValue(25.2)
        B.SetValue(7)
        # self.assertAlmostEqual (4.2, Mod.GetValue(), delta=FLOAT64_EPSILON ) # lacks precision
        self.assertAlmostEqual(4.2, Mod.GetValue(), delta=10e-10)
        B.SetValue(0)
        with self.assertRaises(GenericException):
            Mod.GetValue()

        Ternary = Camera.GetNode("Ternary")
        A.SetValue(5)
        B.SetValue(7)
        C.SetValue(8)
        self.assertAlmostEqual(7, Ternary.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(0)
        self.assertAlmostEqual(8, Ternary.GetValue(), delta=FLOAT64_EPSILON)

        Precedence1 = Camera.GetNode("Precedence1")
        A.SetValue(2)
        B.SetValue(3)
        C.SetValue(4)
        self.assertAlmostEqual(14, Precedence1.GetValue(), delta=FLOAT64_EPSILON)

        Brackets1 = Camera.GetNode("Brackets1")
        A.SetValue(2)
        B.SetValue(3)
        C.SetValue(4)
        self.assertAlmostEqual(20, Brackets1.GetValue(), delta=FLOAT64_EPSILON)

        Sgn = Camera.GetNode("Sgn")
        A.SetValue(5)
        self.assertAlmostEqual(1, Sgn.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(0)
        self.assertAlmostEqual(0, Sgn.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-7)
        self.assertAlmostEqual(-1, Sgn.GetValue(), delta=FLOAT64_EPSILON)

        Neg = Camera.GetNode("Neg")
        A.SetValue(5)
        self.assertAlmostEqual(-5, Neg.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(0)
        self.assertAlmostEqual(0, Neg.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-7)
        self.assertAlmostEqual(7, Neg.GetValue(), delta=FLOAT64_EPSILON)

        Frac = Camera.GetNode("Frac")
        A.SetValue(5.4)
        # self.assertAlmostEqual (0.4, Frac.GetValue(), delta=FLOAT64_EPSILON ) # lacks precision
        self.assertAlmostEqual(0.4, Frac.GetValue(), delta=10e-10)
        A.SetValue(-5.4)
        # self.assertAlmostEqual (-0.4, Frac.GetValue(), delta=FLOAT64_EPSILON ) # lacks precision
        self.assertAlmostEqual(-0.4, Frac.GetValue(), delta=10e-10)

        Trunc = Camera.GetNode("Trunc")
        A.SetValue(5.4)
        self.assertAlmostEqual(5.0, Trunc.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(5.5)
        self.assertAlmostEqual(5.0, Trunc.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.4)
        self.assertAlmostEqual(-5.0, Trunc.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.5)
        self.assertAlmostEqual(-5.0, Trunc.GetValue(), delta=FLOAT64_EPSILON)

        Floor = Camera.GetNode("Floor")
        A.SetValue(5.4)
        self.assertAlmostEqual(5.0, Floor.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(5.5)
        self.assertAlmostEqual(5.0, Floor.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.4)
        self.assertAlmostEqual(-6.0, Floor.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.5)
        self.assertAlmostEqual(-6.0, Floor.GetValue(), delta=FLOAT64_EPSILON)

        Ceil = Camera.GetNode("Ceil")
        A.SetValue(5.4)
        self.assertAlmostEqual(6.0, Ceil.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(5.5)
        self.assertAlmostEqual(6.0, Ceil.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.4)
        self.assertAlmostEqual(-5.0, Ceil.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.5)
        self.assertAlmostEqual(-5.0, Ceil.GetValue(), delta=FLOAT64_EPSILON)

        Round = Camera.GetNode("Round")
        A.SetValue(5.4)
        self.assertAlmostEqual(5.0, Round.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(5.5)
        self.assertAlmostEqual(6.0, Round.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.4)
        self.assertAlmostEqual(-5.0, Round.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.5)
        self.assertAlmostEqual(-6.0, Round.GetValue(), delta=FLOAT64_EPSILON)

        RoundPrec = Camera.GetNode("RoundPrec")
        A.SetValue(45.4545)
        B.SetValue(1)
        self.assertAlmostEqual(45.5, RoundPrec.GetValue(), delta=10e-2)  # """delta=FLOAT64_EPSILON"""
        B.SetValue(2)
        self.assertAlmostEqual(45.45, RoundPrec.GetValue(), delta=10e-3)  # """delta=FLOAT64_EPSILON""" )
        B.SetValue(3)
        self.assertAlmostEqual(45.455, RoundPrec.GetValue(), delta=10e-4)  # """delta=FLOAT64_EPSILON""" )
        B.SetValue(0)
        self.assertAlmostEqual(45.0, RoundPrec.GetValue(), delta=10e-1)  # """delta=FLOAT64_EPSILON""" )
        B.SetValue(-1)
        self.assertAlmostEqual(50.0, RoundPrec.GetValue(), delta=1)  # """delta=FLOAT64_EPSILON""" )

        Pi = Camera.GetNode("Pi")
        self.assertAlmostEqual(3.1415926536, Pi.GetValue(), delta=10e-10)

        E = Camera.GetNode("E")
        self.assertAlmostEqual(2.7182818285, E.GetValue(), delta=10e-10)

        Abs = Camera.GetNode("Abs")
        A.SetValue(5.4)
        self.assertAlmostEqual(5.4, Abs.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(-5.4)
        self.assertAlmostEqual(5.4, Abs.GetValue(), delta=FLOAT64_EPSILON)

        Exp = Camera.GetNode("Exp")
        A.SetValue(1)
        self.assertAlmostEqual(E.GetValue(), Exp.GetValue(), delta=FLOAT64_EPSILON)

        Ln = Camera.GetNode("Ln")
        A.SetValue(E.GetValue() * E.GetValue())
        self.assertAlmostEqual(2.0, Ln.GetValue(), delta=FLOAT64_EPSILON)

        Lg = Camera.GetNode("Lg")
        A.SetValue(1000)
        self.assertAlmostEqual(3.0, Lg.GetValue(), delta=FLOAT64_EPSILON)

        Sqrt = Camera.GetNode("Sqrt")
        A.SetValue(2.25)
        self.assertAlmostEqual(1.5, Sqrt.GetValue(), delta=FLOAT64_EPSILON)

        Sin = Camera.GetNode("Sin")
        A.SetValue(0.0)
        self.assertAlmostEqual(0.0, Sin.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(Pi.GetValue() / 2)
        self.assertAlmostEqual(1.0, Sin.GetValue(), delta=FLOAT64_EPSILON)

        Cos = Camera.GetNode("Cos")
        A.SetValue(0.0)
        self.assertAlmostEqual(1.0, Cos.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(Pi.GetValue() / 2)
        self.assertAlmostEqual(0.0, Cos.GetValue(), delta=FLOAT64_EPSILON)

        Tan = Camera.GetNode("Tan")
        A.SetValue(0.0)
        self.assertAlmostEqual(0.0, Tan.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(Pi.GetValue() / 4)
        self.assertAlmostEqual(1, Tan.GetValue(), delta=FLOAT64_EPSILON)

        Asin = Camera.GetNode("Asin")
        A.SetValue(0.0)
        self.assertAlmostEqual(0.0, Asin.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(1.0)
        self.assertAlmostEqual(Pi.GetValue() / 2, Asin.GetValue(), delta=FLOAT64_EPSILON)

        Acos = Camera.GetNode("Acos")
        A.SetValue(0.0)
        self.assertAlmostEqual(Pi.GetValue() / 2, Acos.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(1.0)
        self.assertAlmostEqual(0.0, Acos.GetValue(), delta=FLOAT64_EPSILON)

        Atan = Camera.GetNode("Atan")
        A.SetValue(0.0)
        self.assertAlmostEqual(0.0, Atan.GetValue(), delta=FLOAT64_EPSILON)
        A.SetValue(1.0)
        self.assertAlmostEqual(Pi.GetValue() / 4, Atan.GetValue(), delta=FLOAT64_EPSILON)

        Digits1 = Camera.GetNode("Digits1")
        self.assertAlmostEqual(46.2, Digits1.GetValue(), delta=FLOAT64_EPSILON)

        Digits2 = Camera.GetNode("Digits2")
        self.assertAlmostEqual(2.2, Digits2.GetValue(), delta=FLOAT64_EPSILON)

        Digits3 = Camera.GetNode("Digits3")
        self.assertAlmostEqual(-2.2, Digits3.GetValue(), delta=FLOAT64_EPSILON)

        # some invalid stuff
        Invalid1 = Camera.GetNode("Invalid1")
        with self.assertRaises(GenericException):
            Invalid1.GetValue()

        Invalid2 = Camera.GetNode("Invalid2")
        with self.assertRaises(GenericException):
            Invalid2.GetValue()

        Invalid3 = Camera.GetNode("Invalid3")
        with self.assertRaises(GenericException):
            Invalid3.GetValue()

        Invalid4 = Camera.GetNode("Invalid4")
        with self.assertRaises(GenericException):
            Invalid4.GetValue()

        Invalid5 = Camera.GetNode("Invalid5")
        with self.assertRaises(GenericException):
            Invalid5.GetValue()

        Invalid6 = Camera.GetNode("Invalid6")
        with self.assertRaises(GenericException):
            Invalid6.GetValue()

        Invalid7 = Camera.GetNode("Invalid7")
        with self.assertRaises(GenericException):
            Invalid7.GetValue()

        Invalid8 = Camera.GetNode("Invalid8")
        with self.assertRaises(GenericException):
            Invalid8.GetValue()

        Invalid9 = Camera.GetNode("Invalid9")
        with self.assertRaises(GenericException):
            Invalid9.GetValue()

        Invalid10 = Camera.GetNode("Invalid10")
        with self.assertRaises(GenericException):
            Invalid10.GetValue()

        Invalid11 = Camera.GetNode("Invalid11")
        with self.assertRaises(GenericException):
            Invalid11.GetValue()

        Invalid12 = Camera.GetNode("Invalid12")
        with self.assertRaises(GenericException):
            Invalid12.GetValue()

        Invalid13 = Camera.GetNode("Invalid13")
        with self.assertRaises(GenericException):
            Invalid13.GetValue()

        Invalid14 = Camera.GetNode("Invalid14")
        with self.assertRaises(GenericException):
            Invalid14.GetValue()

        Invalid15 = Camera.GetNode("Invalid15")
        with self.assertRaises(GenericException):
            Invalid15.GetValue()

        Invalid16 = Camera.GetNode("Invalid16")
        with self.assertRaises(GenericException):
            Invalid16.GetValue()

        Invalid17 = Camera.GetNode("Invalid17")
        with self.assertRaises(GenericException):
            Invalid17.GetValue()

        Invalid18 = Camera.GetNode("Invalid18")
        with self.assertRaises(GenericException):
            Invalid18.GetValue()

        Invalid19 = Camera.GetNode("Invalid19")
        with self.assertRaises(GenericException):
            Invalid19.GetValue()

        Invalid20 = Camera.GetNode("Invalid20")
        with self.assertRaises(GenericException):
            Invalid20.GetValue()

        Invalid21 = Camera.GetNode("Invalid21")
        with self.assertRaises(GenericException):
            Invalid21.GetValue()

        Invalid22 = Camera.GetNode("Invalid22")
        with self.assertRaises(GenericException):
            Invalid22.GetValue()

    def test_TheFrenchWay(self):
        # create and initialize node map
        """[ GenApiTest@SwissKnifeTestSuite_TestTheFrenchWay.xml|gxml
    
            <SwissKnife Name="Value">
                <Formula>1.234</Formula>
            </SwissKnife>
    
        """

        # LOG4CPP_NS::Category& testlogger(CLog::GetLogger("CppUnit.Tests"))
        OldLocale = setlocale(LC_ALL, None)

        # cs << "Original locale = " << OldLocale << "\n"
        # stringstream ss ss << "Original locale = " << OldLocale << "\n"
        # testlogger.info( ss.str().c_str() )
        # ss.clear()

        try:
            setlocale(LC_ALL, "French")
        except:
            try:
                setlocale(LC_ALL, "fr_FR.UTF-8")
            except:
                setlocale(LC_ALL, "fr_FR")

        # ss << "French locale = " << setlocale(LC_A, NU) << "\n"
        # testlogger.info( ss.str().c_str() )
        # ss.clear()

        # Ticket #704 seems to imply that this goes wrong because the French locale
        # denotes float numbers as 1,234 instead of 1.234.
        # However this does not fail. I tried to set the locale in DMain directly
        # but it made no difference
        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestTheFrenchWay")

        setlocale(LC_ALL, OldLocale )
        # ss << "Restored locale = " << setlocale(LC_ALL, NU) << "\n"
        # testlogger.info( ss.str().c_str() )

    def test_Tickets_788_789_790(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestTickets_788_789_790.xml|gxml
    
        <IntSwissKnife Name="Ticket788">
            <pVariable Name="A">A</pVariable>
            <Formula>A % 0</Formula>
        </IntSwissKnife>
    
        <IntSwissKnife Name="Ticket789">
            <Formula></Formula>
        </IntSwissKnife>
    
        <IntSwissKnife Name="Ticket790">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula>A}B</Formula>
        </IntSwissKnife>
    
        <IntSwissKnife Name="Ticket788_Float">
            <pVariable Name="A">A</pVariable>
            <Formula>A % 0</Formula>
        </IntSwissKnife>
    
        <IntSwissKnife Name="Ticket789_Float">
            <Formula></Formula>
        </IntSwissKnife>
    
        <IntSwissKnife Name="Ticket790_Float">
            <pVariable Name="A">A</pVariable>
            <pVariable Name="B">B</pVariable>
            <Formula>A}B</Formula>
        </IntSwissKnife>
    
        <Integer Name="A">
            <Value>1</Value>
        </Integer>
    
        <Integer Name="B">
            <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestTickets_788_789_790")

        Ticket788 = Camera.GetNode("Ticket788")
        Ticket789 = Camera.GetNode("Ticket789")
        Ticket790 = Camera.GetNode("Ticket790")

        Ticket788_Float = Camera.GetNode("Ticket788_Float")
        Ticket789_Float = Camera.GetNode("Ticket789_Float")
        Ticket790_Float = Camera.GetNode("Ticket790_Float")

        with self.assertRaises(LogicalErrorException):
            Ticket788.GetValue()
        with self.assertRaises(LogicalErrorException):
            Ticket789.GetValue()
        with self.assertRaises(LogicalErrorException):
            Ticket790.GetValue()

        with self.assertRaises(LogicalErrorException):
            Ticket788_Float.GetValue()
        with self.assertRaises(LogicalErrorException):
            Ticket789_Float.GetValue()
        with self.assertRaises(LogicalErrorException):
            Ticket790_Float.GetValue()

    def test_ListOfValidValue(self):
        """[ GenApiTest@SwissKnifeTestSuite_TestListOfValidValue.xml|gxml
    
            <SwissKnife Name="Value">
                <Formula>1.234</Formula>
            </SwissKnife>
    
        """

        Camera = CNodeMapRef()

        Camera._LoadXMLFromFile("GenApiTest", "SwissKnifeTestSuite_TestListOfValidValue")
        Value = Camera.GetNode("Value")

        self.assertEqual(noIncrement, Value.GetIncMode())

        valueList = Value.GetListOfValidValues()
        self.assertEqual(0, len(valueList))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
