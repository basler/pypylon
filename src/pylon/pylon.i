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

%include "typemaps.i"
%include "std_string.i"
%include "std_map.i"
%include "std_vector.i"
%include "cstring.i"
%include "std_ios.i"
%include "exception.i"

%{

#include <vector>

// python defines own version of COMPILER macro which collides with genicam logic
#define _PYTHON_COMPILER COMPILER
#undef COMPILER
#include <pylon/PylonIncludes.h>
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

// Tranlates the C++ exception to a Python exception by calling into _genicam.
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

%}

%init %{

    Pylon::PylonInitialize();

    // Need to import TranslateGenicamException from _genicam in order to be
    // able to translate C++ Genicam exceptions to the correct Python exceptions.

    PyObject* mod = PyImport_ImportModule("pypylon._genicam"); // new obj
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
// TlInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::TlInfoList_t & {
  $1 = new Pylon::TlInfoList_t();
}

%typemap(argout,fragment="t_output_helper") Pylon::TlInfoList_t & {
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CTlInfo *ti = new CTlInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(ti),
        SWIGTYPE_p_Pylon__CTlInfo,
        0
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}


////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList output
//

%typemap(in, numinputs=0, noblock=1) Pylon::DeviceInfoList_t & {
  $1 = new DeviceInfoList_t();
}

%typemap(argout,fragment="t_output_helper") Pylon::DeviceInfoList_t & {
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CDeviceInfo *di = new CDeviceInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(di),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        0
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}

// ensure the above typemap will not be applied to const references
%typemap(argout, noblock=1) const Pylon::DeviceInfoList_t & {}

////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList intput
//
// needed for EnumerateDevices(
//     DeviceInfoList_t& list,
//     const DeviceInfoList_t& filter,
//     bool addToList = false
//     );
//

// Type check to make overloading work
// Note:  %typecheck(X) is a macro for %typemap(typecheck,precedence=X)
%typecheck(SWIG_TYPECHECK_POINTER)
const Pylon::DeviceInfoList_t&
{
    // We need a list
    $1 = PyList_Check($input) ? 1 : 0;
}

// Convert a python list of wrapped DeviceInfos to a DeviceInfoList_t
%typemap(in, numinputs=1, noblock=1)
const Pylon::DeviceInfoList_t&
(Pylon::DeviceInfoList_t di_list)
{
    if (PyList_Check($input))
    {
        Py_ssize_t size = PyList_Size($input);
        for (Py_ssize_t i = 0; i < size; i++)
        {
            // python object possibly wrapping a DeviceInfo
            PyObject *o = PyList_GetItem($input,i);
            // pointer to wrapped DeviceInfo
            void *w = 0;
            if (!SWIG_IsOK(
                    SWIG_ConvertPtr(o, &w, SWIGTYPE_p_Pylon__CDeviceInfo, 0)
                    )
                )
            {
                PyErr_SetString(
                    PyExc_TypeError,
                    "list must contain DeviceInfo objects"
                    );
                return NULL;
            }
            di_list.push_back(*reinterpret_cast<Pylon::CDeviceInfo*>(w));
        }
        $1 = &di_list;
    }
    else
    {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
    }
}

////////////////////////////////////////////////////////////////////////////////
//
// String vector input (for XML injection)
//

// Check typemap to make the overload working with python lists
// Note:  %typecheck(X) is a macro for %typemap(typecheck,precedence=X)
%typecheck(SWIG_TYPECHECK_STRING_ARRAY) const Pylon::StringList_t & {
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
                return NULL;
            }
        }
        $1 = &str_list;
    } else {
        PyErr_SetString(PyExc_TypeError,"not a list");
        return NULL;
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

// ignore assignment operator in all classes
%ignore *::operator=;

%include "TypeMappings.i"
%include "Container.i"
%include "PixelType.i"
%include "PayloadType.i"
%include "Info.i"
%include "DeviceInfo.i"
%include "TlInfo.i"
%include "DeviceFactory.i"
%include "TransportLayer.i"
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
