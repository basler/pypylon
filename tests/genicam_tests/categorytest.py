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


class CategoryTestSuite(GenicamTestCase):
    def test_1(self):
        """[ GenApiTest@CategoryTestSuite_Test1.xml|gxml
    
        <Category Name="ScalarFeatures">
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="Shutter">
            <Value>20</Value>
            <Min>0</Min>
            <Max>100</Max>
        </Integer>
    
        <Integer Name="Gain">
            <Value>20</Value>
            <Min>5</Min>
            <Max>200</Max>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_Test1")

        Cat = Camera.GetNode("ScalarFeatures")
        self.assertEqual(intfICategory, Cat.GetNode().GetPrincipalInterfaceType())

        strMainCat = "ScalarFeatures"
        self.assertEqual(strMainCat, Cat.ToString())

        FeatureList = Cat.GetFeatures()

        CatName = ["Shutter", "Gain"]
        i = 0
        for feature in FeatureList:
            strName = feature.GetNode().GetName()
            self.assertEqual(CatName[i], strName)
            i += 1

        strName = "toto"
        with self.assertRaises(AccessException):
            Cat.FromString(strName)

        # Reference
        # CCategoryRef refCategory

        # self.assertRaises(
        #    refCategory.GetFeatures(pFeatureList),
        #    GenICam::AccessException
        # )

        # CPPUNIT_ASSERT_NO_THROW(refCategory.SetReference( ptrCat ) )
        # refCategory.GetFeatures(pFeatureList)

        i = 0
        for feature in FeatureList:
            strName = feature.GetNode().GetName()
            self.assertEqual(CatName[i], strName)
            i += 1

    def test_FeatureTest(self):
        """[ GenApiTest@CategoryTestSuite_FeatureTest_NoRootNode.xml|gxml

        <Category Name="NotTheRoot">
            <pFeature>ScalarFeatures</pFeature>
        </Category>

        <Category Name="ScalarFeatures">
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>

        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>

        <Integer Name="Gain">
            <pValue>GainImpl</pValue>
        </Integer>

        <Integer Name="GainImpl">
            <Value>20</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_NoRootNode")

        Gain = Camera.GetNode("Gain")
        GainImpl = Camera.GetNode("GainImpl")
        self.assertFalse(Gain.Node.IsFeature())
        self.assertFalse(GainImpl.Node.IsFeature())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_WithRootNode.xml|gxml

        <Category Name="Root">
           <pFeature>ScalarFeatures</pFeature>
        </Category>

        <Category Name="ScalarFeatures">
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>

        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>

        <Integer Name="Gain">
            <pValue>GainImpl</pValue>
        </Integer>

        <Integer Name="GainImpl">
            <Value>20</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_WithRootNode")

        Gain = Camera.GetNode("Gain")
        GainImpl = Camera.GetNode("GainImpl")
        self.assertTrue(Gain.Node.IsFeature())
        self.assertFalse(GainImpl.Node.IsFeature())

        # A second time with Root node to make sure the XML file pre-processing works
        """[ GenApiTest@CategoryTestSuite_FeatureTest_WithRootNode2.xml|gxml

        <Category Name="Root">
            <pFeature>ScalarFeatures</pFeature>
        </Category>

        <Category Name="ScalarFeatures">
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>

        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>

        <Integer Name="Gain">
            <pValue>GainImpl</pValue>
        </Integer>

        <Integer Name="GainImpl">
            <Value>20</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_WithRootNode2")

        Gain = Camera.GetNode("Gain")
        GainImpl = Camera.GetNode("GainImpl")
        self.assertTrue(Gain.Node.IsFeature())
        self.assertFalse(GainImpl.Node.IsFeature())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_OverrideAccessmode.xml|gxml

        <Category Name="Root">
            <Visibility>Beginner</Visibility>
            <pFeature>ScalarFeatures</pFeature>
        </Category>

        <Category Name="ScalarFeatures">
            <Visibility>Expert</Visibility>
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>

        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>

        <Integer Name="Gain">
            <pValue>GainImpl</pValue>
        </Integer>

        <Integer Name="GainImpl">
            <Value>20</Value>
        </Integer>

        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_OverrideAccessmode")
        Gain = Camera.GetNode("Gain")
        GainImpl = Camera.GetNode("GainImpl")
        Root = Camera.GetNode("Root")
        ScalarFeatures = Camera.GetNode("ScalarFeatures")
        self.assertTrue(Gain.Node.IsFeature())
        self.assertFalse(GainImpl.Node.IsFeature())
        self.assertEqual(Beginner, ScalarFeatures.Node.GetVisibility())
        self.assertEqual(Beginner, Root.Node.GetVisibility())
        self.assertEqual(Beginner, Gain.Node.GetVisibility())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_EmptyCategories_Invisible.xml|gxml
        
        <Category Name="Root">
             <pFeature>ContainsEmptyOne</pFeature>
        </Category>
        
        <Category Name="EmptyOne"/>
        <Category Name="ContainsEmptyOne">
             <pFeature>EmptyOne</pFeature>
             <pFeature>Gain</pFeature>
        </Category>
        
        <Integer Name="Gain">
        <Visibility>Invisible</Visibility>
        <Value>20</Value>
        </Integer>
        
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_EmptyCategories_Invisible")
        EmptyOne = Camera.GetNode("EmptyOne")
        ContainsEmptyOne = Camera.GetNode("ContainsEmptyOne")
        Root = Camera.GetNode("Root")
        Gain = Camera.GetNode("Gain")
        self.assertEqual(Invisible, Gain.Node.GetVisibility())
        self.assertEqual(Invisible, ContainsEmptyOne.Node.GetVisibility())
        self.assertEqual(Invisible, EmptyOne.Node.GetVisibility())
        self.assertEqual(Invisible, Root.Node.GetVisibility())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_EmptyCategories_Guru.xml|gxml
        
        <Category Name="Root">
        <pFeature>ContainsEmptyOne</pFeature>
        </Category>
        
        <Category Name="EmptyOne"/>
        <Category Name="ContainsEmptyOne">
        <pFeature>EmptyOne</pFeature>
        <pFeature>Gain</pFeature>
        </Category>
        
        <Integer Name="Gain">
        <Visibility>Guru</Visibility>
        <Value>20</Value>
        </Integer>
        
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_EmptyCategories_Guru")
        EmptyOne = Camera.GetNode("EmptyOne")
        ContainsEmptyOne = Camera.GetNode("ContainsEmptyOne")
        Root = Camera.GetNode("Root")
        Gain = Camera.GetNode("Gain")
        self.assertEqual(Guru, Gain.Node.GetVisibility())
        self.assertEqual(Guru, ContainsEmptyOne.Node.GetVisibility())
        self.assertEqual(Invisible, EmptyOne.Node.GetVisibility())
        self.assertEqual(Guru, Root.Node.GetVisibility())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_EmptyCategories_Beginner.xml|gxml
        
        <Category Name="Root">
        <pFeature>ContainsEmptyOne</pFeature>
        </Category>
        
        <Category Name="EmptyOne"/>
        <Category Name="ContainsEmptyOne">
        <pFeature>EmptyOne</pFeature>
        <pFeature>Gain</pFeature>
        </Category>
        
        <Integer Name="Gain">
        <Visibility>Beginner</Visibility>
        <Value>20</Value>
        </Integer>
        
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_EmptyCategories_Beginner")
        EmptyOne = Camera.GetNode("EmptyOne")
        ContainsEmptyOne = Camera.GetNode("ContainsEmptyOne")
        Root = Camera.GetNode("Root")
        Gain = Camera.GetNode("Gain")
        self.assertEqual(Beginner, Gain.Node.GetVisibility())
        self.assertEqual(Beginner, ContainsEmptyOne.Node.GetVisibility())
        self.assertEqual(Invisible, EmptyOne.Node.GetVisibility())
        self.assertEqual(Beginner, Root.Node.GetVisibility())

        """[ GenApiTest@CategoryTestSuite_FeatureTest_EmptyCategories_Expert.xml|gxml
        
        <Category Name="Root">
        <pFeature>ContainsEmptyOne</pFeature>
        </Category>
        
        <Category Name="EmptyOne"/>
        <Category Name="ContainsEmptyOne">
        <pFeature>EmptyOne</pFeature>
        <pFeature>Gain</pFeature>
        </Category>
        
        <Integer Name="Gain">
        <Visibility>Expert</Visibility>
        <Value>20</Value>
        </Integer>
        
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_FeatureTest_EmptyCategories_Expert")
        EmptyOne = Camera.GetNode("EmptyOne")
        ContainsEmptyOne = Camera.GetNode("ContainsEmptyOne")
        Root = Camera.GetNode("Root")
        Gain = Camera.GetNode("Gain")
        self.assertEqual(Expert, Gain.Node.GetVisibility())
        self.assertEqual(Expert, ContainsEmptyOne.Node.GetVisibility())
        self.assertEqual(Invisible, EmptyOne.Node.GetVisibility())
        self.assertEqual(Expert, Root.Node.GetVisibility())

    # For debugging the access mode of categories
    def test_AccessModeTest(self):
        """[ GenApiTest@CategoryTestSuite_AccessModeTest.xml|gxml
    
        <Category Name="Root">
            <pFeature>ScalarFeatures</pFeature>
        </Category>
    
        <Category Name="ScalarFeatures">
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>
    
        <Integer Name="Gain">
            <pValue>GainImpl</pValue>
        </Integer>
    
        <Integer Name="GainImpl">
            <Value>20</Value>
        </Integer>
    
        <Category Name="NICat1">
            <pIsImplemented>False</pIsImplemented>
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="False">
            <Value>0</Value>
        </Integer>
    
        <Category Name="NICat2">
            <pIsImplemented>ImplWO</pIsImplemented>
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="ImplWO">
            <ImposedAccessMode>WO</ImposedAccessMode>
            <Value>1</Value>
        </Integer>
    
        <Category Name="ROCat1">
            <pIsImplemented>True</pIsImplemented>
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="True">
            <Value>1</Value>
        </Integer>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_AccessModeTest")

        Root = Camera.GetNode("Root")

        self.assertEqual(RO, Root.GetAccessMode())
        # happy path (now the access mode should be cached)
        self.assertEqual(RO, Root.GetAccessMode())

        NICat1 = Camera.GetNode("NICat1")
        self.assertEqual(NI, NICat1.GetAccessMode())
        ROCat1 = Camera.GetNode("ROCat1")
        self.assertEqual(RO, ROCat1.GetAccessMode())

        # since categories are never NA, if pIsImpl is not readable, leave the category implemented
        NICat2 = Camera.GetNode("NICat2")
        self.assertEqual(RO, NICat2.GetAccessMode())

    def test_VisibilityTest(self):
        """[ GenApiTest@CategoryTestSuite_VisibilityTest.xml|gxml
    
        <Category Name="Root">
            <Visibility>Beginner</Visibility>
            <pFeature>ScalarFeatures</pFeature>
        </Category>
    
        <Category Name="ScalarFeatures">
            <Visibility>Expert</Visibility>
            <pFeature>Shutter</pFeature>
            <pFeature>Gain</pFeature>
        </Category>
    
        <Integer Name="Shutter">
            <Value>20</Value>
        </Integer>
    
        <Integer Name="Gain">
            <Value>20</Value>
        </Integer>
           
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "CategoryTestSuite_VisibilityTest")

        # NODE_POINTER(Category, Root)
        # NODE_POINTER(Category, ScalarFeatures)

        # NOTE:  A category gets the most visibility of itself and the most visible child 
        # 
        # - Shutter = Beginner (default)
        # - Gain = Beginner (default)
        # - ScalarFeatures = Root (inspite of <Expert> entry, because it is promoted)
        # - Root = Beginner (because ScalarFeatures' Beginner visibility is promoted)

        # self.assertEqual(Beginner """!!!""", ptrRoot.GetNode().GetVisibility())
        # self.assertEqual(Beginner """!!!""", ptrScalarFeatures.GetNode().GetVisibility())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
