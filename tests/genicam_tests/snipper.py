'''
Created on 03.08.2015

@author: TMoeller
'''

import sys
import re
import os
import errno
import tempfile
import atexit
import shutil

# Global temporary directory for XML files
_temp_xml_dir = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_xml_temp_dir():
    """Get or create a temporary directory for XML files."""
    global _temp_xml_dir
    if _temp_xml_dir is None:
        _temp_xml_dir = tempfile.mkdtemp(prefix='pypylon_xml_')
        # Register cleanup function to remove temp directory on exit
        atexit.register(lambda: shutil.rmtree(_temp_xml_dir, ignore_errors=True))
        print(f"Using temporary XML directory: {_temp_xml_dir}")
    return _temp_xml_dir

def createXMLSnippet(file_content):
    # parse template file extract comment and 
    # spit out xml file

    header = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
                <RegisterDescription
                  ModelName=\"{ModelName}\"
                  VendorName=\"{VendorName}\"
                  ToolTip=\"XML file extracted from test code\"
                  StandardNameSpace=\"GEV\"
                  SchemaMajorVersion=\"1\"
                  SchemaMinorVersion=\"1\"
                  SchemaSubMinorVersion=\"0\"
                  MajorVersion=\"3\"
                  MinorVersion=\"0\"
                  SubMinorVersion=\"0\"
                  ProductGuid=\"2D932CC6-EB68-40bd-B6CC-F03B55B7D653\"
                  VersionGuid=\"02A8C268-BEE8-463b-A6C0-53ED8256E3D8\"
                  xmlns=\"http://www.genicam.org/GenApi/Version_1_1\"
                  xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">
             """

    footer = "</RegisterDescription>\n"

    start_rule = re.compile("^\\s*\"\"\"\\[?\\s*(\\S+)@(\\S+)\\|(\\S+)")
    end_rule = re.compile("^\\s*\"\"\"")

    in_snippet = False
    out_file = None
    xml_temp_dir = get_xml_temp_dir()
    
    for l in file_content.splitlines():
        m_s = start_rule.match(l)
        m_e = end_rule.match(l)
        if m_s:
            in_snippet = True
            vendor_name, model_name, option = m_s.groups()
            # Use temporary directory instead of 'xml'
            # Create file as-is (model_name already includes .xml from docstring)
            file_path = os.path.join(xml_temp_dir, vendor_name, model_name)
            mkdir_p(os.path.dirname(file_path))
            out_file = open(file_path, "w")
            # Use model_name as-is for the ModelName attribute in XML header
            out_file.write(header.format(ModelName=model_name, VendorName=vendor_name))
            print("Create Snippet ", file_path)
        elif in_snippet and m_e:
            in_snippet = False
            out_file.write(footer)
            out_file.close()
            out_file = None
        elif in_snippet:
            out_file.write(l)
