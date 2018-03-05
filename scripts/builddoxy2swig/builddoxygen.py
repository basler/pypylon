import subprocess
import os
import warnings
import shutil

#check if PYLON_DEV_DIR is set
print("Is Pylon installed?")
pylonDevDir = os.environ.get("PYLON_DEV_DIR")
if not pylonDevDir:
    raise EnvironmentError("PYLON_DEV_DIR is not set")

#check if doxygen is installed
print("Is Doxygen installed?")
doxyVersion = subprocess.getoutput("doxygen --version")
print ("Version: ", doxyVersion);
if doxyVersion != "1.5.9":
    warnings.warn("Only testet with version 1.5.9 other versions of doxygen may not work.")

#gets the path of this programm.
path = os.path.dirname(os.path.realpath(__file__));


#deletes the xml folder if present
shutil.rmtree(path+"\\xml")

#runs doxygen over the GenApi folder in PYLON_DEV_DIR/includes
os.system("( type "+path+"\\Doxyfile & echo INPUT=\""+pylonDevDir+"\\include\\GenApi\" & echo OUTPUT_DIRECTORY=\""+path+"\") | doxygen.exe -")

#runs doxy2swig for GenApi
subprocess.call("python "+path+"\\doxy2swig\\doxy2swig.py \""+path+"\\xml\index.xml\" \""+path[:-22]+"pypylon\\genicam\\DoxyGenApi.i\"");



#runs doxygen over the pylon folder in PYLON_DEV_DIR/includes
os.system("( type "+path+"\\Doxyfile & echo INPUT=\""+pylonDevDir+"\\include\\pylon\"  & echo OUTPUT_DIRECTORY=\""+path+"\") | doxygen.exe -")

#runs doxy2swig for pylon
subprocess.call("python "+path+"\\doxy2swig\\doxy2swig.py \""+path+"\\xml\index.xml\" \""+path[:-22]+"pypylon\\pylon\\DoxyPylon.i\"");

#deletes the xml folder if present
shutil.rmtree(path+"\\xml")

print("Successfully generated pylon/DoxyPylon.i and genapi/DoxyGenApi.i")
