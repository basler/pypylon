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


class AliasTestSuite(GenicamTestCase):
    FLOAT32_EPSILON = 1.19209e-07  # np.finfo(np.float32).eps
    FLOAT64_EPSILON = 2.22044604925e-16  # np.finfo(float).eps

    def test_Basics(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@AliasTestSuite_TestBasics.xml|gxml

        <Float Name="Abs">
            <pCastAlias>Raw</pCastAlias>
            <Value>42.0</Value>
        </Float>

        <Integer Name="Raw">
            <pCastAlias>Abs</pCastAlias>
            <Value>42</Value>
        </Integer>

        <Integer Name="NoAlias">
            <Value>0815</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "AliasTestSuite_TestBasics")

        Abs = Camera.GetNode("Abs")
        # CPPUNIT_ASSERT( (bool) ptrAbs )

        Raw = Camera.GetNode("Raw")
        # CPPUNIT_ASSERT( (bool) ptrRaw )

        NoAlias = Camera.GetNode("NoAlias")
        # CPPUNIT_ASSERT( (bool) NoAlias )

        # retrieving the alias manually
        Alias = Abs.GetNode().GetCastAlias()
        # CPPUNIT_ASSERT( (bool) ptrAlias )
        self.assertEqual("Raw", Alias.Node.GetName())

        # CIntegerPtr ptrIntAlias(ptrAlias)
        # CPPUNIT_ASSERT( (bool) ptrIntAlias )
        # self.assertEqual( ptrRaw.GetValue(), ptrIntAlias.GetValue() )

        # retrieving the alias via helper function
        self.assertEqual(Raw.GetValue(), Abs.GetIntAlias().GetValue())

        # the same with references

    #         CIntegerRef refRaw
    #         refRaw.SetReference( ptrRaw )
    #         CFloatRef refAbs
    #         CPPUNIT_ASSERT_THROW_EX (refAbs.GetEnumAlias(), AccessException)
    #         refAbs.SetReference( ptrAbs )
    #         CIntegerRef refNoAlias
    #         refNoAlias.SetReference( ptrNoAlias )
    #         {
    #             self.assertEqual( refRaw.GetValue(), refAbs.GetIntAlias().GetValue() )
    #             self.assertEqual( (IEnumeration*)NULL, refAbs.GetEnumAlias() )
    #         }



    def test_WithSwissKnife(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@AliasTestSuite_TestWithSwissKnife.xml|gxml

        <Converter Name="Abs">
            <ToolTip>20 us per tick</ToolTip>
            <pCastAlias>Raw</pCastAlias>
            <FormulaTo> FROM / 0.00002</FormulaTo>
            <FormulaFrom> TO * 0.00002</FormulaFrom>
            <pValue>Raw</pValue>
            <Unit>s</Unit>
            <Slope>Increasing</Slope>
        </Converter>

        <Integer Name="Raw">
            <pCastAlias>Abs</pCastAlias>
            <Value>10</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "AliasTestSuite_TestWithSwissKnife")

        Abs = Camera.GetNode("Abs")
        # CPPUNIT_ASSERT( (bool) ptrAbs )

        # gcstring valName, AttributeStr
        # ptrAbs.GetNode().GetProperty("Name", valName, AttributeStr)
        # CPPUNIT_ASSERT(valName == "Abs")

        Raw = Camera.GetNode("Raw")
        # CPPUNIT_ASSERT( (bool) ptrRaw )

        # *ptrAbs = 0.01 # 10 ms
        # self.assertEqual( (int64_t) 500LL, ptrAbs.GetIntAlias().GetValue() )

    def test_SliderUseCases(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        # This example shows how to get rid of Abs / Raw features using an Alias node.

        # For demonstration a digital shift Gain is used, i.e.
        #     GainAbs = 1 << GainRaw = 2^GainRaw
        #     GainRaw = ld(GainAbs) = ln(GainAbs)/ln(2)
        #
        # which yields the following possible values:
        #     GainRaw, GainAbs
        #        0        1.0
        #        1        2.0
        #        2        4.0
        #        3        8.0
        #        4       16.0

        # "GainRaw" and "GainAbs" are implemented using a Converter node
        # However they could also be implemented by using two camera registers
        # The important thing is that changing one of the two values must automatically
        # change the other, too.

        # The "Gain" feature is in essence the same as the "GainAbs" feature. However since
        # for backward compatibility "GainAbs" and "GainRaw" must be available "Gain" is made a separate node

        # Note however that "GainAbs" and "GainRaw" are made invisible so that they will not show
        # up in a GUI but will be present in an API to be used by legacy software.

        # The <pAlias> entry of the "Gain" node shows that "GainRaw" is it's alias.
        # The same entry is (optionally) present in the "GainAbs" node.

        """[ GenApiTest@AliasTestSuite_TestSliderUseCases.xml|gxml

        <Category Name="Root">
            <pFeature>Gain</pFeature>
            <pFeature>GainAbs</pFeature>
            <pFeature>GainRaw</pFeature>
        </Category>

        <Float Name="Gain">
            <Visibility>Beginner</Visibility>
            <pCastAlias>GainRaw</pCastAlias>
            <pValue>GainAbs</pValue>
        </Float>

        <Converter Name="GainAbs">
            <Visibility>Invisible</Visibility>
            <pCastAlias>GainRaw</pCastAlias>
            <FormulaTo> LN(FROM)/LN(2) </FormulaTo>
            <FormulaFrom><![CDATA[ 1<<TO ]]></FormulaFrom>
            <pValue>GainRaw</pValue>
            <Slope>Increasing</Slope>
        </Converter>

        <Integer Name="GainRaw">
            <Visibility>Invisible</Visibility>
            <Value>0</Value>
            <Min>0</Min>
            <Max>4</Max>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "AliasTestSuite_TestSliderUseCases")

        # Get the "Gain" node
        Gain = Camera.GetNode("Gain")
        # CPPUNIT_ASSERT( (bool) ptrGain )

        # Check if an alias is present
        # Note that .GetXXXAlias() is accessed via the . (dot) operator, not via the . (arrow) operator
        # because GetXXXAlias is a method of the CFloatPtr smart pointer not the IFloat interface
        if (Gain.GetIntAlias()):
            # Show a slider with an edit box
            pass
        else:
            # Show an edit box only
            pass

        # the following assumes an alias is present
        self.assertIsNotNone(Gain.GetIntAlias())

        # compute the number of ticks to draw on the slider
        NumberOfTicks = (Gain.GetIntAlias().GetMax() - Gain.GetIntAlias().GetMin()) / Gain.GetIntAlias().GetInc()
        self.assertEqual(4, NumberOfTicks)

        # initialize the gain
        Gain.SetValue(1.0)

        # fill the edit box
        EditBox = Gain.ToString()
        self.assertEqual("1", EditBox)

        # user sets a gain not fitting exactly Gain's granularity
        # the gain will jump backwards to the nearest possible value
        Gain.FromString("5.2")
        self.assertEqual("4", Gain.ToString())
        # or will forward back to the nearest possible value
        Gain.FromString("5.7")
        self.assertEqual("8", Gain.ToString())

        # Tick the slider up
        TickUp = min(Gain.GetIntAlias().GetValue() + Gain.GetIntAlias().GetInc(), Gain.GetIntAlias().GetMax())
        Gain.GetIntAlias().SetValue(TickUp)
        self.assertEqual("16", Gain.ToString())

        # Try again (but now the maximum is already reached)
        TickUp = min(Gain.GetIntAlias().GetValue() + Gain.GetIntAlias().GetInc(), Gain.GetIntAlias().GetMax())
        Gain.GetIntAlias().SetValue(TickUp)
        self.assertEqual("16", Gain.ToString())

    def test_JoeCustomer(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@AliasTestSuite_TestJoeCustomer.xml|gxml

            <Float Name="GainA">
                <pAlias>GainAbs</pAlias>
                <pValue>GainAbs</pValue>
            </Float>

            <Float Name="GainR1">
                <pAlias>GainRaw1</pAlias>
                <pValue>GainRaw1</pValue>
            </Float>

            <!--  the following converter emulates a digital shift Gain -->
            <!--      Gain = 2^GainRaw = 1 << GainRaw -->
            <!--      GainRaw = ld(Abs) = ln(Abs)/ln(2) -->
            <Converter Name="GainR2">
                <pAlias>GainRaw2</pAlias>
                <FormulaTo> LN(FROM)/LN(2) </FormulaTo>
                <FormulaFrom><![CDATA[ 1<<TO ]]></FormulaFrom>
                <pValue>GainRaw2</pValue>
                <Slope>Increasing</Slope>
            </Converter>

            <Float Name="GainL">
                <pAlias>GainList</pAlias>
                <pValue>GainList</pValue>
            </Float>

            <Float Name="GainAbs">
                <Value>1.0</Value>
            </Float>

            <Integer Name="GainRaw1">
                <Value>1</Value>
            </Integer>

            <Integer Name="GainRaw2">
                <Value>0</Value>
                <Min>0</Min>
                <Max>20</Max>
                <Inc>2</Inc>
            </Integer>

            <Enumeration Name="GainList">
                <EnumEntry Name="Low">
                    <Value>0</Value>
                    <NumericValue>1.0</NumericValue>
               </EnumEntry>
                <EnumEntry Name="Medium">
                    <Value>1</Value>
                    <NumericValue>50.0</NumericValue>
               </EnumEntry>
                <EnumEntry Name="Heigh">
                    <Value>2</Value>
                    <NumericValue>100.0</NumericValue>
               </EnumEntry>
                <Value>1</Value>
            </Enumeration>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "AliasTestSuite_TestJoeCustomer")

        GainA = Camera.GetNode("GainA")
        GainR1 = Camera.GetNode("GainR1")
        GainR2 = Camera.GetNode("GainR2")
        GainL = Camera.GetNode("GainL")
        GainList = Camera.GetNode("GainList")

        self.assertEqual(GainList.Node.Name, GainL.Node.Alias.Node.Name)

        GainA.SetValue(41.6)
        self.assertAlmostEqual(41.6, GainA.GetValue(), delta=self.FLOAT64_EPSILON)

        GainR1.SetValue(41.6)
        self.assertAlmostEqual(42.0, GainR1.GetValue(), delta=self.FLOAT64_EPSILON)
        GainR1.SetValue(17.1)
        self.assertAlmostEqual(17.0, GainR1.GetValue(), delta=self.FLOAT64_EPSILON)

        GainR2.SetValue(5.2)
        self.assertAlmostEqual(4.0, GainR2.GetValue(), delta=self.FLOAT64_EPSILON)
        GainR2.SetValue(15.1)
        self.assertAlmostEqual(16.0, GainR2.GetValue(), delta=self.FLOAT64_EPSILON)

        GainL.SetValue(41.6)
        self.assertAlmostEqual(50.0, GainL.GetValue(), delta=self.FLOAT64_EPSILON)
        GainL.SetValue(76.0)
        self.assertAlmostEqual(100.0, GainL.GetValue(), delta=self.FLOAT64_EPSILON)

    def test_VeronicaVendor(self):
        # if(GenApiSchemaVersion == v1_0)
        #    return

        """[ GenApiTest@AliasTestSuite_TestVeronicaVendor.xml|gxml

            <Float Name="GainA">
                <pCastAlias>GainAbs</pCastAlias>
                <pValue>GainAbs</pValue>
            </Float>


            <!--  the following converter emulates a digital shift Gain -->
            <!--      Gain = 2^GainRaw = 1 << GainRaw -->
            <!--      GainRaw = ld(Abs) = ln(Abs)/ln(2) -->
            <Converter Name="GainR">
                <pCastAlias>GainRaw</pCastAlias>
                <FormulaTo> LN(FROM)/LN(2) </FormulaTo>
                <FormulaFrom><![CDATA[ 1<<TO ]]></FormulaFrom>
                <pValue>GainRaw</pValue>
                <Slope>Increasing</Slope>
            </Converter>

            <Float Name="GainL">
                <pCastAlias>GainList</pCastAlias>
                <pValue>GainList</pValue>
            </Float>

            <Float Name="GainAbs">
                <Value>1.0</Value>
            </Float>

            <Integer Name="GainRaw">
                <Value>0</Value>
                <Min>0</Min>
                <Max>20</Max>
                <Inc>2</Inc>
            </Integer>

            <Enumeration Name="GainList">
                <EnumEntry Name="Low">
                    <Value>0</Value>
                    <NumericValue>1.0</NumericValue>
               </EnumEntry>
                <EnumEntry Name="Medium">
                    <Value>1</Value>
                    <NumericValue>50.0</NumericValue>
               </EnumEntry>
                <EnumEntry Name="High">
                    <Value>2</Value>
                    <NumericValue>100.0</NumericValue>
               </EnumEntry>
                <Value>1</Value>
            </Enumeration>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "AliasTestSuite_TestVeronicaVendor")

        GainA = Camera.GetNode("GainA")
        GainR = Camera.GetNode("GainR")
        GainL = Camera.GetNode("GainL")

        self.RunVeronicaTest(GainA)
        self.RunVeronicaTest(GainR)
        self.RunVeronicaTest(GainL)

    def RunVeronicaTest(self, Gain):
        print("Gain.GetAlias() does not work on float")

        try:
            GainRaw = Gain.GetIntAlias()
        except LogicalErrorException:
            GainRaw = None

        try:
            GainList = Gain.GetEnumAlias()
        except LogicalErrorException:
            GainList = None

        if (GainRaw):
            print("==> Gain with IInteger alias" + "\n")

            print("GainMin = ", Gain.GetMin(), "\n")

            print("GainMax = ", Gain.GetMax(), "\n")

            NumTics = (GainRaw.GetMax() - GainRaw.GetMin()) / GainRaw.GetInc()
            print("NumTics = ", NumTics, "\n")

            GainRaw.SetValue(GainRaw.GetMin() + int(float(GainRaw.GetInc()) * float(NumTics) * 0.1))
            print(GainRaw.GetValue(), "\n")
            print("10% slider range = ", Gain.GetValue(), "\n")

            GainRaw.SetValue(GainRaw.GetValue() + GainRaw.GetInc())
            print("+ 1 Tic = ", Gain.GetValue(), "\n")
        elif (GainList):
            print("==> Gain with IEnumeration alias\n")

            EnumEntries = None
            for EnumEntry in GainList.GetEntries():
                print(EnumEntry.GetSymbolic(), ", IntValue = ", EnumEntry.GetValue(), ", NumericValue = ",
                      EnumEntry.GetNumericValue(), "\n")

            GainList.FromString("High")
            print("High Gain = ", Gain.GetValue(), "\n")
        else:
            print("==> Gain with no alias\n")

            print("Gain = ", Gain.GetValue(), "\n")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
