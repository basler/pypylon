%define PYLON_DOCSTRING
"
Copyright (C) 2017-2023 Basler AG
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

%module(directors="1", package="pypylon", docstring=PYLON_DOCSTRING) pylon
%include "DoxyPylon.i";
%begin %{

#ifdef Py_LIMITED_API
#include <stdlib.h> // malloc / free
// Although PyMemoryView_FromMemory has been part of limited API since
// version 3.3, the flags PyBUF_READ and PyBUF_WRITE, which are needed to use
// this function, are not defined in newer Python headers unless Py_LIMITED_API
// is set to >= 3.11. Since this is obviously a bug, we need the following
// workarond:
#ifndef PyBUF_READ
#define PyBUF_READ  0x100
#endif
#ifndef PyBUF_WRITE
#define PyBUF_WRITE 0x200
#endif
#endif

// allow debug builds of genicam wrapper against release build of python
# ifdef _DEBUG
#    ifdef _MSC_VER
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

%include <exception.i>
%include <std_container.i>

%{

#include <vector>

// python defines own version of COMPILER macro which collides with genicam logic
#define _PYTHON_COMPILER COMPILER
#undef COMPILER

#ifdef _MSC_VER  // MSVC
#  pragma warning(push)
#  pragma warning(disable : 4265)
#elif __GNUC__  // GCC, CLANG, MinGW
#  pragma GCC diagnostic push
#  pragma GCC diagnostic ignored "-Wnon-virtual-dtor"
#  pragma GCC diagnostic ignored "-Woverloaded-virtual"
#  pragma GCC diagnostic ignored "-Wunused-variable"
#  ifdef __clang__
#    pragma GCC diagnostic ignored "-Wunknown-warning-option"
#    pragma GCC diagnostic ignored "-Wc++11-extensions"
#  endif
#endif



#include <pylon/PylonIncludes.h>
#include <pylon/gige/GigETransportLayer.h>
#include <pylon/gige/ActionTriggerConfiguration.h>
#include <pylon/StaticDefectPixelCorrection.h>
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
#include <GenApi/IDeviceInfo.h>
#include "pylon/NodeMapWrapper.h"
#include "pylon/EnumEntryParameter.h"
#include "pylon/CategoryParameter.h"
#include "pylon/PortParameter.h"
#include "pylon/PlaceholderParameter.h"
#include <pylon/PixelTypeMapper.h>
#include "pylon/BufferFactoryContext.h"

#ifdef _MSC_VER  // MSVC
#  pragma warning(pop)
#elif __GNUC__  // GCC, CLANG, MinWG
#  pragma GCC diagnostic pop
#endif

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
%}

%init %{

    Pylon::PylonInitialize();

    // register PylonTerminate on interpreter shutdown
    auto pylon_terminate = [](){ Pylon::PylonTerminate(true);};
    Py_AtExit( pylon_terminate );

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

import warnings

# Compatibility layer for @deprecated decorator across Python versions
try:
  # Try to import the native deprecated decorator (Python 3.13+)
  from warnings import deprecated
except ImportError:
  # Fallback implementation for Python < 3.13
  def deprecated(message):
    def decorator(func):
      def wrapper(*args, **kwargs):
        import warnings
        warnings.warn(
          f"{func.__name__} is deprecated. {message}",
          DeprecationWarning,
          stacklevel=2
        )
        return func(*args, **kwargs)
      return wrapper
    return decorator

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
// Helper macro: dispatch one INode* to the matching Pylon::C*Parameter type.
// Used by the NodeMapWrapper::GetNode typemap above and by the NodeList_t /
// FeatureList_t argout overrides below.
//
// Arguments:
//   node_ptr  - a local INode* variable (must not be null)
//   out_item  - the PyObject* that receives the new reference
//
%define PYLON_NODE_TO_PARAMETER(node_ptr, out_item)
    switch ((node_ptr)->GetPrincipalInterfaceType())
    {
        // ------------------------------------------------------------------
        // Standard value-bearing node types
        // ------------------------------------------------------------------
        case GENAPI_NAMESPACE::intfIInteger:
        {
            Pylon::CIntegerParameter *p = new Pylon::CIntegerParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CIntegerParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIBoolean:
        {
            Pylon::CBooleanParameter *p = new Pylon::CBooleanParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CBooleanParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfICommand:
        {
            Pylon::CCommandParameter *p = new Pylon::CCommandParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CCommandParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIFloat:
        {
            Pylon::CFloatParameter *p = new Pylon::CFloatParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CFloatParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIString:
        {
            Pylon::CStringParameter *p = new Pylon::CStringParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CStringParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIRegister:
        {
            Pylon::CArrayParameter *p = new Pylon::CArrayParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CArrayParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIEnumeration:
        {
            Pylon::CEnumParameter *p = new Pylon::CEnumParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CEnumParameter*), SWIG_POINTER_OWN);
            break;
        }
        // ------------------------------------------------------------------
        // Special-purpose node types (structural / non-value nodes)
        // ------------------------------------------------------------------
        case GENAPI_NAMESPACE::intfIEnumEntry:
        {
            Pylon::CEnumEntryParameter *p = new Pylon::CEnumEntryParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CEnumEntryParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfICategory:
        {
            Pylon::CCategoryParameter *p = new Pylon::CCategoryParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CCategoryParameter*), SWIG_POINTER_OWN);
            break;
        }
        case GENAPI_NAMESPACE::intfIPort:
        {
            Pylon::CPortParameter *p = new Pylon::CPortParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CPortParameter*), SWIG_POINTER_OWN);
            break;
        }
        // ------------------------------------------------------------------
        // intfIValue: should have been caught by a specific case above;
        // wrap as a base CParameter as a last resort.
        // ------------------------------------------------------------------
        case GENAPI_NAMESPACE::intfIValue:
        {
            Pylon::CParameter *p = new Pylon::CParameter(node_ptr);
            out_item = SWIG_NewPointerObj(p, $descriptor(Pylon::CParameter*), SWIG_POINTER_OWN);
            break;
        }
        default:
        {
            // Could be intfIBase or a newly added GenApi interface type.
            // There is no node with principal interface intfIBase only.
            // It is not expected to enter this branch in normal operation.
            throw DYNAMICCAST_EXCEPTION(
                "Unknown node type with principal interface %d",
                (node_ptr)->GetPrincipalInterfaceType());
        }
    }
%enddef

////////////////////////////////////////////////////////////////////////////////
//
// Override the genicam INode* factory typemap so that GetNode() (and the other
// nodemap lookup methods) return Pylon::C*Parameter objects instead of raw
// genicam interface types when called from the pylon module.
//
// Standard node interface types and their Pylon wrappers:
//   intfIInteger     -> Pylon::CIntegerParameter
//   intfIBoolean     -> Pylon::CBooleanParameter
//   intfICommand     -> Pylon::CCommandParameter
//   intfIFloat       -> Pylon::CFloatParameter
//   intfIString      -> Pylon::CStringParameter
//   intfIRegister    -> Pylon::CArrayParameter
//   intfIEnumeration -> Pylon::CEnumParameter
//
// Special-purpose node interface types:
//   intfIEnumEntry   -> Pylon::CEnumEntryParameter (should not be needed, use EnumParameter instead)
//   intfICategory    -> Pylon::CCategoryParameter (needed only for displaying parameter trees)
//   intfIPort        -> Pylon::CPortParameter (non-value)
//
%typemap(out) GENAPI_NAMESPACE::INode* Pylon::NodeMapWrapper::GetNode2,
              GENAPI_NAMESPACE::INode* Pylon::NodeMapWrapper::GetNode
{
    {
        if (0 == $1)
        {
            // Node not found: create a PlaceholderParameter whose path is
            // "NodeMapTypeString/requestedNodeName" for diagnostic purposes.
            // arg1 is the first declared parameter of GetNode / GetNode2 (const char* pName).
            GENICAM_NAMESPACE::gcstring path =
                (arg1 ? arg1->GetNodeMapTypeString() : GENICAM_NAMESPACE::gcstring()) +
                GENICAM_NAMESPACE::gcstring("/") +
                (arg2 ? *arg2 : GENICAM_NAMESPACE::gcstring());
            Pylon::CPlaceholderParameter *p = new Pylon::CPlaceholderParameter(path);
            $result = SWIG_NewPointerObj(p, $descriptor(Pylon::CPlaceholderParameter*), SWIG_POINTER_OWN);
        }
        else
        {
            PYLON_NODE_TO_PARAMETER($1, $result)
        }
    }
}

////////////////////////////////////////////////////////////////////////////////
//
// Override NodeList_t argout: GetNodes() returns a tuple of Pylon::C*Parameter.
//
%typemap(argout) GENAPI_NAMESPACE::NodeList_t & {
    PyObject *o = PyTuple_New($1->size());
    for (unsigned int i = 0; i < $1->size(); i++) {
        PyObject *o_item = 0;
        GENAPI_NAMESPACE::INode *n = (*$1)[i];
        PYLON_NODE_TO_PARAMETER(n, o_item)
        PyTuple_SetItem(o, i, o_item);
    }
    $result = SWIG_AppendOutput($result, o);
    delete $1;
}

////////////////////////////////////////////////////////////////////////////////
//
// Override FeatureList_t argout: GetFeatures() returns a tuple of Pylon::C*Parameter.
// Elements are IValue* so we dynamic_cast to INode* first.
//
%typemap(argout) GENAPI_NAMESPACE::FeatureList_t & {
    PyObject *o = PyTuple_New($1->size());
    for (unsigned int i = 0; i < $1->size(); i++) {
        PyObject *o_item = 0;
        GENAPI_NAMESPACE::INode *n = dynamic_cast<GENAPI_NAMESPACE::INode*>((*$1)[i]);
        PYLON_NODE_TO_PARAMETER(n, o_item)
        PyTuple_SetItem(o, i, o_item);
    }
    $result = SWIG_AppendOutput($result, o);
    delete $1;
}

%typemap(in, numinputs=0) GENAPI_NAMESPACE::NodeList_t & {
    $1 = new GENAPI_NAMESPACE::NodeList_t();
}

////////////////////////////////////////////////////////////////////////////////
//
// Expose NodeMapWrapper to SWIG so that $descriptor(Pylon::NodeMapWrapper*)
// resolves correctly and the method-qualified typemap for GetNode fires.
%include "NodeMapWrapper.i"

////////////////////////////////////////////////////////////////////////////////
//
// Wrap every returned INodeMap* in an NodeMapWrapper so that subsequent
// typemaps (GetNode, GetNodes, GetFeatures) map INode* to Pylon::C*Parameter.
//
// The wrapper is heap-allocated and owned by Python (SWIG_POINTER_OWN).
//
%typemap(out) GENAPI_NAMESPACE::INodeMap*,
              GENAPI_NAMESPACE::INodeMap&
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, NodeMapType_Unknown),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

////////////////////////////////////////////////////////////////////////////////
//
// Python helper: ToParameter(val)
//
// Accepts any genicam interface object (IInteger, IBoolean, ICommand, IFloat,
// IString, IRegister, IEnumeration, INode, IValue) and wraps it in the
// corresponding Pylon::C*Parameter.  Any object that is not a recognised
// genicam type is returned unchanged, so callers can pass any value safely.
//
%pythoncode %{
def ToParameter(val):
    """Convert any supported value to the most specific Pylon *Parameter type available.

    The conversion rules are applied in the following order:

    1. None / null
           -> PlaceholderParameter()  (permanently-invalid sentinel, empty path)

    2. Already a Pylon Parameter instance
           If the parameter wraps a node whose interface type can be mapped to a
           more specific subclass, that subclass is returned.  If the input is
           already the most specific type, or no more specific type exists, the
           input object is returned unchanged.

    3. genicam.IBase (IPort, …) or genicam.IValue (IInteger, IBoolean, ICommand,
                       IFloat, IString, IRegister, IEnumeration, IEnumEntry, …)
           The underlying INode is retrieved and dispatch continues as below.

    4. genicam.INode
           Dispatched via GetPrincipalInterfaceType():
               intfIInteger     -> IntegerParameter
               intfIBoolean     -> BooleanParameter
               intfICommand     -> CommandParameter
               intfIFloat       -> FloatParameter
               intfIString      -> StringParameter
               intfIRegister    -> ArrayParameter
               intfIEnumeration -> EnumParameter
               intfIEnumEntry   -> EnumEntryParameter
               intfICategory    -> CategoryParameter
               intfIPort        -> PortParameter
               any other type   -> Parameter  (base, wraps the node)

    5. Any other value
           -> PlaceholderParameter()  (permanently-invalid sentinel, empty path)
    """
    from pypylon import genicam as _genicam

    # ------------------------------------------------------------------ #
    # Helper: map an INode* to the most specific Parameter subclass.      #
    # Returns None when no specific mapping exists.                        #
    # ------------------------------------------------------------------ #
    def _node_to_specific(node):
        t = node.GetPrincipalInterfaceType()
        if t == _genicam.intfIInteger:
            return IntegerParameter(node)
        elif t == _genicam.intfIBoolean:
            return BooleanParameter(node)
        elif t == _genicam.intfICommand:
            return CommandParameter(node)
        elif t == _genicam.intfIFloat:
            return FloatParameter(node)
        elif t == _genicam.intfIString:
            return StringParameter(node)
        elif t == _genicam.intfIRegister:
            return ArrayParameter(node)
        elif t == _genicam.intfIEnumeration:
            return EnumParameter(node)
        elif t == _genicam.intfIEnumEntry:
            return EnumEntryParameter(node)
        elif t == _genicam.intfICategory:
            return CategoryParameter(node)
        elif t == _genicam.intfIPort:
            return PortParameter(node)
        return None  # no more-specific type available

    # 1. None -> permanently-invalid placeholder
    if val is None:
        return PlaceholderParameter()

    # 2. Already a Pylon Parameter – try to specialise, keep if already specific
    if isinstance(val, Parameter):
        # Only the base Parameter class can potentially be specialised;
        # subclasses are already as specific as we can get.
        if type(val) is Parameter:
            node = val.GetNode() if val.IsValid() else None
            if node is not None:
                specific = _node_to_specific(node)
                if specific is not None:
                    return specific
        return val

    # 3. genicam.IValue – unwrap to INode first
    if isinstance(val, _genicam.IValue):
        val = val.GetNode()

    # 4. genicam.INode – dispatch on interface type
    if isinstance(val, _genicam.INode):
        specific = _node_to_specific(val)
        return specific if specific is not None else Parameter(val)
    if isinstance(val, _genicam.IPort):
        return PortParameter(val)

    # 5. Unrecognised type -> permanently-invalid placeholder
    return PlaceholderParameter()
%}

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
// ImageConverter and ImagePersistence output
//

%typemap(in,numinputs=0, noblock=1) Pylon::IReusableImage&, IReusableImage& {
  $1 = new Pylon::CPylonImage();
}

%typemap(argout, noblock=1) Pylon::IReusableImage&, IReusableImage& {
  Py_DECREF($result);
  $result = SWIG_NewPointerObj(
    SWIG_as_voidptr($1),
    SWIGTYPE_p_Pylon__CPylonImage,
    SWIG_POINTER_OWN
    ); // Now $1 is owned by $result. Must not 'delete' it now!
}

// '%typemap(freearg)' must be empty!
%typemap(freearg, noblock=1) Pylon::IReusableImage&, IReusableImage& {}

////////////////////////////////////////////////////////////////////////////////
//
// ImageConverter and ImagePersistence input, maps the IImage cast operators of pylon C++
//

%typemap(in) const Pylon::IImage &, const IImage & {
    // Reject None early: SWIG_ConvertPtr accepts None as a null pointer, which
    // would result in a null reference and a SEGFAULT inside the C++ call.
    if ($input == Py_None) {
        SWIG_exception_fail(SWIG_TypeError,
                            "None is not a valid IImage, CGrabResultPtr or CPylonDataComponent");
    }

    // Case 1: already an IImage*
    if (SWIG_IsOK(SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_Pylon__IImage, 0)) && $1) {
    $1 = (IImage*)$1;
    }

    // Case 2: CGrabResultPtr -> extract IImage
    else if (SWIG_IsOK(SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_Pylon__CGrabResultPtr, 0)) && $1) {
    Pylon::CGrabResultPtr* grabPtr = (Pylon::CGrabResultPtr*)$1;
    if (!(*grabPtr)) {
        SWIG_exception_fail(SWIG_ValueError, "Invalid CGrabResultPtr");
    }
    $1 = &(grabPtr->operator Pylon::IImage&());
    }

    // Case 3: Pylon::CPylonDataComponent -> extract IImage
    else if (SWIG_IsOK(SWIG_ConvertPtr($input, (void**)&$1, SWIGTYPE_p_Pylon__CPylonDataComponent, 0)) && $1) {
    $1 = const_cast<Pylon::IImage*>(&(((Pylon::CPylonDataComponent*)$1)->operator const Pylon::IImage&()));
    }

    else {
    SWIG_exception_fail(SWIG_TypeError,
                "Expected IImage, CGrabResultPtr or CPylonDataComponent");
    }
}

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) const Pylon::IImage &, const IImage & {
  // SWIG_ConvertPtr accepts None (Python null) as a null pointer and returns
  // SWIG_OK.  We must reject that explicitly with the '&& ptr' guards so that
  // None does not accidentally match this overload and reach the 'in' typemap
  // where a null IImage reference would SEGFAULT.
  Pylon::IImage *ptr = nullptr;
  $1 =
      (SWIG_IsOK(SWIG_ConvertPtr($input, (void **)(&ptr), SWIGTYPE_p_Pylon__IImage, 0)) && ptr)
      || (SWIG_IsOK(SWIG_ConvertPtr($input, (void **)(&ptr), SWIGTYPE_p_Pylon__CGrabResultPtr, 0)) && ptr)
      || (SWIG_IsOK(SWIG_ConvertPtr($input, (void **)(&ptr), SWIGTYPE_p_Pylon__CPylonDataComponent, 0)) && ptr)
      ;
}

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
#define PYLON_INTERFACE struct
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

////////////////////////////////////////////////////////////////////////////////
//
// GetStride output parameter typemap
//
// GetStride(size_t& strideBytes) uses a C++ output-reference parameter.
// Hide it from Python (numinputs=0) and append the value to the return tuple
// so that the Python call is:
//
//   ok, stride = obj.GetStride()
//
// The typemap matches on the parameter name "strideBytes" which is used
// consistently across CGrabResultData, CPylonImage, and CPylonDataComponent.
//
%typemap(in, numinputs=0) size_t& strideBytes (size_t temp = 0) {
    $1 = &temp;
}
%typemap(argout) size_t& strideBytes {
    %append_output(PyLong_FromSize_t(*$1));
}

// ignore assignment operator in all classes
%ignore *::operator=;
%ignore "operator const Pylon::IImage&";
%ignore "operator const IImage&";

%include <pylon/PylonVersionNumber.h>

// The entire functionality of GenApi is placed in a namespace. The actual name
// of this namespace is formed by a macro called 'GENAPI_NAMESPACE'. But there
// is also the alias 'namespace GenApi = GENAPI_NAMESPACE;'. For a long time,
// pylon used the macro exclusively. With version 6.3.0, pylon has started to
// use the alias. In the genicam sources, however, the macro is used. While
// these two have the same meaning for the actual C++ compiler, SWIG treats them
// differently. This is important to us because we want SWIG to use the data
// types it learned when parsing the Genicam sources when parsing the Pylon
// sources. The following macro ensures that SWIG again uses 'GENAPI_NAMESPACE'
// in all the places where pylon uses 'GenApi'.
#define GenApi GENAPI_NAMESPACE
#define GenICam GENICAM_NAMESPACE
%include "parameter_lookup.i"
%include "Device.i"
%include "PylonVersionInfo.i"
%include "TypeMappings.i"
%include "Container.i"
%include "PixelType.i"
%include "PixelTypeMapper.i"
%include "ImageMixin.i"
%include "PayloadType.i"
%include "Info.i"
%include "DeviceInfo.i"
%include "InterfaceInfo.i"
%include "TlInfo.i"
%include "DeviceFactory.i"
%include "Interface.i"
%include "TransportLayer.i"
%include "GigETransportLayer.i"
%include "TlFactory.i"
%include "GrabResultData.i"
%include "GrabResultPtr.i"
%include "WaitObject.i"
%include "WaitObjects.i"
%include "BufferFactory.i"
%include "InstantCamera.i"
%include "InstantCameraArray.i"
%include "ImageEventHandler.i"
%include "ConfigurationEventHandler.i"
%include "CameraEventHandler.i"
%include "SoftwareTriggerConfiguration.i"
%include "StaticDefectPixelCorrection.i"
%include "AcquireContinuousConfiguration.i"
%include "AcquireSingleFrameConfiguration.i"
%include "ActionTriggerConfiguration.i"
%include "ImagePersistence.i"
%include "Image.i"
%include "ReusableImage.i"
%include "PixelData.i"
%include "PylonImageBase.i"
%include "PylonImage.i"
%include "ImageFormatConverter.i"
%include "Parameter.i"
%include "IntegerParameter.i"
%include "CommandParameter.i"
%include "StringParameter.i"
%include "FloatParameter.i"
%include "BooleanParameter.i"
%include "EnumParameter.i"
%include "EnumEntryParameter.i"
%include "CategoryParameter.i"
%include "PortParameter.i"
%include "PlaceholderParameter.i"
%include "ArrayParameter.i"
%include "PylonGUI.i"
%include "FeaturePersistence.i"
%include "ImageDecompressor.i"
%include "PylonDataComponent.i"
%include "PylonDataContainer.i"
%include "DeviceClass.i"
%include "SfncVersion.i"
%include "ConfigurationHelper.i"

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
