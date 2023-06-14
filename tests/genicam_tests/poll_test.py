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
from callbackhelper import CallbackObject


class PollTestSuite(GenicamTestCase):
    def test_Polling_Integer(self):
        """[ GenApiTest@PollTestSuite_TestPolling_Integer.xml|gxml
    
        <Integer Name="Value">
           <pValue>Register</pValue>
        </Integer>
    
        <IntReg Name="Register">
            <Address>0x0f00</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <PollingTime>1000</PollingTime>
            <Sign>Unsigned</Sign>
            <Endianess>LittleEndian</Endianess>
        </IntReg>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PollTestSuite_TestPolling_Integer")
        Node = Camera.GetNode("Register")

        self.assertEqual(1000, Node.Node.GetPollingTime())

        Value = Camera.GetNode("Value")

        self.assertEqual(-1, Value.Node.GetPollingTime())

        CallBackTarget = CallbackObject()
        Register(Node.Node, CallBackTarget.Callback)
        Register(Value.Node, CallBackTarget.Callback)

        Camera._Poll(500)
        self.assertEqual(0, CallBackTarget.Count())

        Camera._Poll(500)
        self.assertEqual(2, CallBackTarget.Count())

    def test_Polling_Register(self):
        """[ GenApiTest@PollTestSuite_TestPolling_Register.xml|gxml
    
        <Register Name="Register">
            <Address>0x0f00</Address>
            <Length>4</Length>
            <AccessMode>RW</AccessMode>
            <pPort>Port</pPort>
            <PollingTime>1000</PollingTime>
        </Register>
    
        <Port Name="Port"/>
    
        """

        Camera = CNodeMapRef()
        Camera._LoadXMLFromFile("GenApiTest", "PollTestSuite_TestPolling_Register")

        Node = Camera.GetNode("Register")

        self.assertEqual(1000, Node.Node.GetPollingTime())

        CallBackTarget = CallbackObject()
        Register(Node.Node, CallBackTarget.Callback)

        Camera._Poll(500)
        self.assertEqual(0, CallBackTarget.Count())

        Camera._Poll(500)
        self.assertEqual(1, CallBackTarget.Count())

        Camera._Poll(500)
        self.assertEqual(1, CallBackTarget.Count())

        Camera._Poll(500)
        self.assertEqual(2, CallBackTarget.Count())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
