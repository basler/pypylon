'''
Created on 03.08.2015

@author: TMoeller
'''
import snipper
import inspect
import unittest
from genicam import *
import os

CNodeMapRef__LoadXMLFromFile = CNodeMapRef._LoadXMLFromFile


def _LoadXMLFromFile(self, vendor, model):
    return CNodeMapRef__LoadXMLFromFile(self, os.path.join("xml", vendor, model) + ".xml")


class GenicamTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        if "GENAPISCHEMAVERSION" in os.environ:
            self.GenApiSchemaVersion = os.environ["GENAPISCHEMAVERSION"]
        else:
            self.GenApiSchemaVersion = "v1_1"

    @classmethod
    def setUpClass(cls):
        super(GenicamTestCase, cls).setUpClass()
        # run snipper on current test
        snipper.createXMLSnippet(inspect.getsource(cls))
        CNodeMapRef._LoadXMLFromFile = _LoadXMLFromFile

    @classmethod
    def tearDownClass(cls):
        CNodeMapRef._LoadXMLFromFile = CNodeMapRef__LoadXMLFromFile
        super(GenicamTestCase, cls).tearDownClass()


CDFHeader = """<?xml version="1.0" encoding="utf-8"?>
              <RegisterDescription
              ModelName="GenApiTest"
              VendorName="Generic"
              ToolTip="nodes for testing the GenApi reference implementation"
              StandardNameSpace="GEV"
              SchemaMajorVersion="1"
              SchemaMinorVersion="1"
              SchemaSubMinorVersion="0"
              MajorVersion="3"
              MinorVersion="0"
              SubMinorVersion="0"
              ProductGuid="2D932CC6-EB68-40bd-B6CC-F03B55B7D653"
              VersionGuid="02A8C268-BEE8-463b-A6C0-53ED8256E3D8"
              xmlns="http://www.genicam.org/GenApi/Version_1_1"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://www.genicam.org/GenApi/Version_1_1
                    http://www.genicam.org/GenApi/GenApiSchema_Version_1_1.xsd">
            """
CDFFooter = """</RegisterDescription>"""
