%define DOCSTRING
"
Copyright (C) 2017-2018 Basler AG
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"
%enddef

%module(directors="1", package="pypylon", docstring=DOCSTRING) pylon
%include "DoxyPylon.i";
%begin %{
// allow debug builds of genicam wrapper against release build of python
# ifdef _DEBUG
#	ifdef _MSC_VER
// Include these low level headers before undefing _DEBUG. Otherwise when doing
// a debug build against a release build of python the compiler will end up
// including these low level headers without DEBUG enabled, causing it to try
// and link release versions of this low level C api.
# include <basetsd.h>
# include <assert.h>
# include <ctype.h>
# include <errno.h>
# include <io.h>
# include <math.h>
# include <sal.h>
# include <stdarg.h>
# include <stddef.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <sys/stat.h>
# include <time.h>
# include <wchar.h>


#define SWIG_PYTHON_INTERPRETER_NO_DEBUG

#  endif
# endif
%}

%include "exception.i"

// PylonIncludes.h will include DeviceFactory.h. We want to ignore
// IDeviceFactory that is declared there.
%ignore IDeviceFactory;


%{

#include <vector>

// python defines own version of COMPILER macro which collides with genicam logic
#define _PYTHON_COMPILER COMPILER
#undef COMPILER
#include <pylon/PylonIncludes.h>
#include <pylon/gige/GigETransportLayer.h>
#include <pylon/gige/ActionTriggerConfiguration.h>
#ifdef _MSC_VER
#include <pylon/PylonGUI.h>
#endif
#include <GenApi/GenApiNamespace.h>
#include <GenICam.h>
#include <GenApi/ChunkPort.h>
#include <GenApi/ChunkAdapter.h>
#include <GenApi/ChunkAdapterGeneric.h>
#include <GenApi/ChunkAdapterGEV.h>
#include <GenApi/EventPort.h>
#include <GenApi/EventAdapter.h>
#include <GenApi/EventAdapterGeneric.h>
#include <GenApi/EventAdapterGEV.h>
#include "genicam/PyPortImpl.h"

#define COMPILER _PYTHON_COMPILER
#undef _PYTHON_COMPILER

using namespace Pylon;

static PyObject* _genicam_translate = NULL;

// Translates the C++ exception to a Python exception by calling into _genicam.
// The wrapped function in _genicam expects to receive the pointer as a PyLong.
void TranslateGenicamException(const GenericException* e)
{
    bool ok = false;
    if (_genicam_translate)
    {
        PyObject *wrapped = PyLong_FromSize_t(reinterpret_cast<size_t>(e));
        PyObject *args = PyTuple_Pack(1, wrapped);

        // Calling _genicam_translate is expected to fail (return NULL), since
        // its purpose is to raise a Python exception.
        ok = (PyObject_CallObject(_genicam_translate, args) == NULL);
        Py_DECREF(args);
        Py_DECREF(wrapped);
    }
    if (!ok)
    {
        PyErr_SetString(
            PyExc_RuntimeError,
            "failed to translate genicam exception"
            );
    }
}

//  For copy deployment of pylon DLLs:
//
//  Version 5.0.5 of Pylon started to use LoadLibraryEx in order to load its
//  DLLs. Calling LoadLibraryEx with the full path of the DLL and setting the
//  flag LOAD_WITH_ALTERED_SEARCH_PATH adds the path of that DLL to the DLL
//  search path, while its dependant DLLs are searched. That ensured that all
//  Pylon DLLs that are stored in the pypylon package folder could be loaded.
//  That also meant that nothing had to be done here, to make pypylon work.
//
//  Unfortunately with version 5.0.11 Pylon changed the way how the GigE and
//  USB TLs DLLs loaded gxapi and uxapi. The mechanism was changed to 'delay
//  loading'. This requires that the delay loaded DLLs are found in one of
//  the standard DLL search paths. While this is going to be fixed in a future
//  Pylon release, we now have to play tricks again like we had to do, before
//  Pylon 5.0.5 was released.
//
//  Our trick is still this:
//  The only thing we can do about the DLL search path here is changing the
//  'PATH' environment variable (using 'SetDllDirectory' or 'AddDllDirectory'
//  would not be appropriate). In order not to disturb the way pythons 'os'
//  module handles 'os.environ', we do not want to make a permanent change.
//
//  So what we do is this:
//   - Append the location of this DLL to the PATH.
//   - Request that the TL DLLs (including gxapi and uxapi) are loaded NOW.
//   - Restore the previous PATH.
//
//  We implement this workaround for Pylon versions < 5.0.5, == 5.0.11,
//  == 5.0.12, == 5.1.0 and == 5.1.1. Version 5.2.0 has a fix that makes this
// workaround superfluous.

#ifdef WIN32
#define NEED_PYLON_DLL_WORKAROUND 1
#include <Shlwapi.h>    // for PathRemoveFileSpec()
#pragma comment(lib, "Shlwapi")
#pragma comment(lib, "user32.lib")
#else
#define NEED_PYLON_DLL_WORKAROUND 0
#endif

#if NEED_PYLON_DLL_WORKAROUND
static void FixPylonDllLoadingIfNecessary()
{
    // Pylon::PylonInitialize must have been called before calling this
    // function!

    unsigned int major, minor, subminor, build;
    Pylon::GetPylonVersion(&major, &minor, &subminor, &build);
    if (major != 5)
    {
        return;
    }
    bool necessary = (
        (minor == 0 && (subminor < 5 || subminor == 11 || subminor == 12)) ||
        (minor == 1 && (subminor == 0 || subminor == 1))
        );
    if (!necessary)
    {
        return;
    }

    // Get HMODULE of this function
    HMODULE hmod = NULL;
    GetModuleHandleExW(
        GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
        GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
        reinterpret_cast<PWSTR>(FixPylonDllLoadingIfNecessary),
        &hmod
        );

    // get module file name and remove file spec
    const DWORD ENV_MAX = UNICODE_STRING_MAX_CHARS;
    // ENV_MAX is so large that it should not be allocated on the stack
    PWSTR new_PATH = new WCHAR[ENV_MAX];
    GetModuleFileNameW(hmod, new_PATH, ENV_MAX);
    PathRemoveFileSpecW(new_PATH);

    // append previous PATH
    PWSTR p_Previous_PATH = new_PATH + lstrlenW(new_PATH);
    *p_Previous_PATH++ = L';';
    const DWORD rem = ENV_MAX - static_cast<DWORD>(p_Previous_PATH - new_PATH);
    GetEnvironmentVariableW(L"PATH", p_Previous_PATH, rem);

    // set new PATH
    SetEnvironmentVariableW(L"PATH", new_PATH);

    // Try to load TLs
    try
    {
        Pylon::CTlFactory& tlf = Pylon::CTlFactory::GetInstance();
        Pylon::TlInfoList_t tli;

        tlf.EnumerateTls(tli);
        for (unsigned int i = 0; i < tli.size(); i++)
        {
            try
            {
                ITransportLayer *pTL = tlf.CreateTl(tli[i]);
                tlf.ReleaseTl(pTL);
            }
            catch (Pylon::GenericException&)
            {
                // Ignore TL loading failure and keep on trying other TLs.
            }
        }
    }
    catch (Pylon::GenericException&)
    {
        // Ignore failure of enumerating TLs and carry on loading this
        // module. The user will notice later if he doesn't find any cameras.
    }

    // restore p_Previous_PATH
    SetEnvironmentVariableW(L"PATH", p_Previous_PATH);

    delete[] new_PATH;
}
#endif


#ifdef GENTL_CXP_PRODUCER_DIR

// ExtendGenTLPathForCXP extends the GenTL path, so that
// <path to this module>/<GENTL_CXP_PRODUCER_DIR> becomes part of that path.
// While doing that, we do NOT want the resulting path to contain a reference
// to the producer in this pypylon installation AND a reference to the one of
// a Pylon installation that might be present. Therefore we filter out any
// portion of the original path, that also contains GENTL_CXP_PRODUCER_DIR,
// since the directory name for the producer of an installed Pylon will be
// the same.

#ifdef _WIN32

static void ExtendGenTLPathForCXP()
{
#ifdef _WIN64
    static const WCHAR var_name[] = L"GENICAM_GENTL64_PATH";
#else
    static const WCHAR var_name[] = L"GENICAM_GENTL32_PATH";
#endif

    const DWORD ENV_MAX = UNICODE_STRING_MAX_CHARS;
    // ENV_MAX is so large that it should not be allocated on the stack
    PWSTR new_PATH = new WCHAR[ENV_MAX];
    PWSTR prev_PATH = new WCHAR[ENV_MAX];

    // get module file name and remove file spec
    HMODULE hmod = NULL;
    GetModuleHandleExW(
        GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
        GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
        reinterpret_cast<PWSTR>(ExtendGenTLPathForCXP),
        &hmod
        );
    GetModuleFileNameW(hmod, new_PATH, ENV_MAX);
    PathRemoveFileSpecW(new_PATH); // also removes trailing '\'

    // concatenate 'GENTL_CXP_PRODUCER_DIR'
    PWSTR new_end = new_PATH + lstrlenW(new_PATH);
    *new_end++ = L'\\';
     StrCpyW(new_end, GENTL_CXP_PRODUCER_DIR);
     new_end = new_end + lstrlenW(new_end);
     *new_end++ = L';';
     *new_end = 0;

    // append portions of previous path to new path
    prev_PATH[0] = 0;
    GetEnvironmentVariableW(var_name, prev_PATH, ENV_MAX);
    PWSTR portion = prev_PATH;
    PWSTR semicolon = StrChrW(portion, L';');
    for(;;)
    {
        if (semicolon)
        {
            *semicolon = 0;
        }

        // only add next portion if it does not countain GENTL_CXP_PRODUCER_DIR
        if (!StrStrIW(portion, GENTL_CXP_PRODUCER_DIR))
        {
            int len = lstrlenW(portion);
            StrCpyW(new_end, portion);
            new_end += len;
            *new_end++ = L';';
            *new_end = 0;
        }

        if (!semicolon)
        {
            break;
        }
        else
        {
            portion = semicolon + 1;
            semicolon = wcschr(portion, L';');
        }
    }

    // set new path
    SetEnvironmentVariableW(var_name, new_PATH);

    #if 0
        char msg[1025];
        wsprintfA(msg, "%S is now: %S\n", var_name, new_PATH);
        OutputDebugStringA(msg);
    #endif

    delete[] new_PATH;
    delete[] prev_PATH;
}

#else // _WIN32

#error You have to implement ExtendGenTLPathForCXP for this platform!

#endif // _WIN32

#endif // GENTL_CXP_PRODUCER_DIR

%}

%init %{

#ifdef GENTL_CXP_PRODUCER_DIR
    ExtendGenTLPathForCXP();
#endif

    Pylon::PylonInitialize();

#if NEED_PYLON_DLL_WORKAROUND
    FixPylonDllLoadingIfNecessary();
#endif

    // Need to import TranslateGenicamException from _genicam in order to be
    // able to translate C++ Genicam exceptions to the correct Python exceptions.

    // The correct way of importing _genicam is to import "pypylon._genicam".
    PyObject* mod = PyImport_ImportModule("pypylon._genicam");
    if (mod == NULL)
    {
        // But that does not work, if pypylon is used in an executable that
        // was created with PyInstaller. PyInstaller installs various import
        // hooks, but obviously none that handles our case.

        // Very important: Clear the error state from the previous failure.
        // Without this the following retry will always fail.
        PyErr_Clear();

        // In the PyInstaller case the name of the imported module has to be:
        mod = PyImport_ImportModule("_genicam");
    }

    if (mod)
    {
        _genicam_translate = PyObject_GetAttrString(    // new obj
            mod,
            "TranslateGenicamException"
            );
        Py_DECREF(mod);
    }
    if (!_genicam_translate)
    {
        # if PY_VERSION_HEX >= 0x03000000
        return NULL;
        # else
        return;
        # endif
    }
%}

%pythoncode %{
try:
  from types import ModuleType
  import numpy as _pylon_numpy
except:
  pass

def needs_numpy(func):
 def func_wrapper(*args, **kwargs):
    e = None
    try:
      if not isinstance(_pylon_numpy, ModuleType):
        e = RuntimeError("_pylon_numpy not a module - not good!")
    except NameError:
      e = NotImplementedError("please install numpy to use this method")
    if e: raise e
    return func(*args, **kwargs)
 return func_wrapper
%}

///////////////////////
//////  stdint ////////
///////////////////////
%include <swigarch.i>

///////////////////////////////////
//// fetch genicam definitions ////
///////////////////////////////////
%import "../genicam/genicam.i"

////////////////////////////////////////////////////////////////////////////////
//
// bool typecheck: Whenever a Python argument is used in a typecheck (resolving
// overloaded functions), we want to enforce that the user has to supply a
// 'real' Python bool object. Otherwise almost any other Python type would
// match, since all those will pass the default 'SWIG_AsVal_bool' test. We want
// to avoid the confusion that might be caused by that.

%typemap(typecheck, precedence=SWIG_TYPECHECK_BOOL) bool
{
  $1 = PyBool_Check($input);
}

////////////////////////////////////////////////////////////////////////////////
//
// GrabResult smart ptr output
//

%typemap(in,numinputs=0, noblock=1) Pylon::CGrabResultPtr& {
  $1 = new CGrabResultPtr();
}

%typemap(argout, noblock=1) Pylon::CGrabResultPtr& {
  Py_DECREF($result);
  $result = SWIG_NewPointerObj(
    SWIG_as_voidptr($1),
    SWIGTYPE_p_Pylon__CGrabResultPtr,
    SWIG_POINTER_OWN
    ); // Now $1 is owned by $result. Must not 'delete' it now!
}

// '%typemap(freearg)' must be empty!
%typemap(freearg, noblock=1) Pylon::CGrabResultPtr& {}

// ensure the above typemap will not be applied to const references
%typemap(in) const Pylon::CGrabResultPtr& = const SWIGTYPE &;
%typemap(argout, noblock=1) const Pylon::CGrabResultPtr& {};
%typemap(freearg, noblock=1) const Pylon::CGrabResultPtr& {};

////////////////////////////////////////////////////////////////////////////////
//
// ImageConverter output
//

%typemap(in,numinputs=0, noblock=1) Pylon::IReusableImage& {
  $1 = new Pylon::CPylonImage();
}

%typemap(argout, noblock=1) Pylon::IReusableImage& {
  Py_DECREF($result);
  $result = SWIG_NewPointerObj(
    SWIG_as_voidptr($1),
    SWIGTYPE_p_Pylon__CPylonImage,
    SWIG_POINTER_OWN
    ); // Now $1 is owned by $result. Must not 'delete' it now!
}

// '%typemap(freearg)' must be empty!
%typemap(freearg, noblock=1) Pylon::IReusableImage& {}


////////////////////////////////////////////////////////////////////////////////
//
// Buffer access
//

%typemap(in,noblock=1,numinputs=0, noblock=1)
( void **buf_mem, size_t *length)
($*1_ltype temp = 0, $*2_ltype tempn) {
  $1 = &temp;
  $2 = &tempn;
}
%typemap(freearg,match="in", noblock=1) (void **buf_mem, size_t *length) "";

%typemap(argout, noblock=1) (void ** buf_mem, size_t *length) {
  if (*$1) {
    %append_output(PyByteArray_FromStringAndSize(
        (const char *)*$1, %numeric_cast(*$2, int))
        );
  }
};

////////////////////////////////////////////////////////////////////////////////
//
// String vector input (for XML injection)
//

// Check typemap to make the overload working with python lists
%typemap(typecheck,precedence=SWIG_TYPECHECK_STRING_ARRAY)
const Pylon::StringList_t &
{
    // We need a list
    $1 = PyList_Check($input) ? 1 : 0;
}

// Convert a python string list into a StringList_t
%typemap(in, numinputs=1)
const Pylon::StringList_t & (Pylon::StringList_t str_list)
{
    if (PyList_Check($input)) {
        Py_ssize_t size = PyList_Size($input);
        str_list.resize(size);
        Py_ssize_t i = 0;
        for (i = 0; i < size; i++) {
            PyObject *o = PyList_GetItem($input,i);
            if (PyBytes_Check(o)) {
                str_list[i] = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(o));
            } else
%#if PY_VERSION_HEX >= 0x03000000
            if(PyUnicode_Check(o)) {
                PyObject *utf8 = PyUnicode_AsUTF8String(o);
                str_list[i] = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(utf8));
                Py_DECREF(utf8);
            }
%#else
            if(PyString_Check(o)) {
                str_list[i] = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(o));
            }
%#endif
            else {
                PyErr_SetString(PyExc_TypeError,"list must contain strings");
                SWIG_fail;
            }
        }
        $1 = &str_list;
    } else {
        PyErr_SetString(PyExc_TypeError,"not a list");
        SWIG_fail;
    }
}

// Make sure the above typemap is no applied on const references
%typemap(argout, noblock=1) const StringList_t & {}

////////////////////////////////////////////////////////////////////////////////

#define interface struct
#define PYLONUTILITY_API
#define PYLONBASE_API
#define PUBLIC_INTERFACE
#define PYLON_BASE_3_0_DEPRECATED(message)
#define PYLON_DEPRECATED(message)
#define APIIMPORT
#define APIEXPORT

// for properties that have a standard genicam type like IInteger or IBoolean
%define GENICAM_PROP(name)
    %rename(_##name) name;

    %pythoncode
    %{
        def _Get_## name(self):
           return self._ ## name
        def _Set_ ## name(self, value):
           self._ ## name.SetValue(value)
        name = property(_Get_ ## name, _Set_ ## name )
    %}
%enddef

// for properties whose type is derived IEnumeration
%define GENICAM_ENUM_PROP(name)
    %rename(_##name) name;

    GENAPI_NAMESPACE::IEnumeration& _GetEnum_##name()
    {
        return static_cast<GENAPI_NAMESPACE::IEnumeration&>($self->##name);
    }

    %pythoncode
    %{
        def _Get_##name(self):
           return self._GetEnum_##name()
        def _Set_ ## name(self, value):
           if isinstance(value, int):
            self._GetEnum_##name().SetIntValue(value)
           else:
            self._GetEnum_##name().SetValue(value)
        name = property(_Get_ ## name, _Set_ ## name )
    %}

%enddef

// for properties with one of those extended types like IIntegerEx or IBooleanEx
%define GENICAM_EX_PROP(name, type)
    %ignore name;

    type& _GetBaseType_##name()
    {
        return static_cast<type&>($self->name);
    }

    %pythoncode
    %{
        def _Get_##name(self):
           return self._GetBaseType_##name()
        def _Set_##name(self, value):
           self._GetBaseType_##name().SetValue(value)
        name = property(_Get_##name, _Set_##name )
    %}

%enddef

// ignore assignment operator in all classes
%ignore *::operator=;

%include <pylon/PylonVersionNumber.h>

%include "TypeMappings.i"
%include "Container.i"
%include "PixelType.i"
%include "PayloadType.i"
%include "Info.i"
%include "DeviceInfo.i"
%include "InterfaceInfo.i"
%include "TlInfo.i"
%include "DeviceFactory.i"
#if PYLON_VERSION_MAJOR >= 6
%include "Interface.i"
#endif
%include "TransportLayer.i"
%include "GigETransportLayer.i"
%include "TlFactory.i"
%include "GrabResultData.i"
%include "GrabResultPtr.i"
%include "WaitObject.i"
%include "WaitObjects.i"
%include "InstantCameraParams.i"
%include "InstantCamera.i"
%include "InstantCameraArray.i"
%include "ImageEventHandler.i"
%include "ConfigurationEventHandler.i"
%include "CameraEventHandler.i"
%include "SoftwareTriggerConfiguration.i"
%include "AcquireContinuousConfiguration.i"
%include "AcquireSingleFrameConfiguration.i"
%include "ActionTriggerConfiguration.i"
%include "Image.i"
%include "ReusableImage.i"
%include "PylonImageBase.i"
%include "PylonImage.i"
%include "_ImageFormatConverterParams.i"
%include "ImageFormatConverter.i"
#ifdef HAVE_PYLON_GUI
%include "PylonGUI.i"
#endif
%include "FeaturePersistence.i"
#if (PYLON_VERSION_MAJOR == 6 && PYLON_VERSION_MINOR >= 1) || PYLON_VERSION_MAJOR > 6
%include "ImageDecompressor.i"
#endif

ADD_PROP_GET(GrabResult, ErrorDescription)
ADD_PROP_GET(GrabResult, ErrorCode)
ADD_PROP_GET(GrabResult, PayloadType)
ADD_PROP_GET(GrabResult, PixelType)
ADD_PROP_GET(GrabResult, Width)
ADD_PROP_GET(GrabResult, Height)
ADD_PROP_GET(GrabResult, OffsetX)
ADD_PROP_GET(GrabResult, OffsetY)
ADD_PROP_GET(GrabResult, PaddingX)
ADD_PROP_GET(GrabResult, PaddingY)
ADD_PROP_GET(GrabResult, Buffer)
ADD_PROP_GET(GrabResult, Array)
ADD_PROP_GET(GrabResult, PayloadSize)
ADD_PROP_GET(GrabResult, BlockID)
ADD_PROP_GET(GrabResult, TimeStamp)
ADD_PROP_GET(GrabResult, ImageSize)
ADD_PROP_GET(GrabResult, ID)
ADD_PROP_GET(GrabResult, ImageNumber)
ADD_PROP_GET(GrabResult, NumberOfSkippedImages)
ADD_PROP_GET(GrabResult, ChunkDataNodeMap)

ADD_PROP_GET(PylonImage, AllocatedBufferSize)
ADD_PROP_GET(PylonImage, Aoi)
ADD_PROP_GET(PylonImage, Array)
ADD_PROP_GET(PylonImage, Buffer)
ADD_PROP_GET(PylonImage, Height)
ADD_PROP_GET(PylonImage, ImageFormat)
ADD_PROP_GET(PylonImage, ImageSize)
ADD_PROP_GET(PylonImage, Orientation)
ADD_PROP_GET(PylonImage, PaddingX)
ADD_PROP_GET(PylonImage, PixelData)
ADD_PROP_GET(PylonImage, PixelType)
ADD_PROP_GET(PylonImage, Plane)
ADD_PROP_GET(PylonImage, Stride)
ADD_PROP_GET(PylonImage, Width)

%apply unsigned int *OUTPUT {
    unsigned int* major,
    unsigned int* minor,
    unsigned int* subminor,
    unsigned int* build
    };

void GetPylonVersion(
    unsigned int* major,
    unsigned int* minor,
    unsigned int* subminor,
    unsigned int* build
    );
const char* GetPylonVersionString();
