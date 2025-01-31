%define PYLONDP_DOCSTRING
"
Copyright (C) 2023 Basler AG
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

%module(directors="1", package="pypylon", docstring=PYLONDP_DOCSTRING) pylondataprocessing
%include "DoxyPylonDataProcessing.i";
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

#include <pylondataprocessing/BuildersRecipe.h>
#include <pylondataprocessing/IOutputObserver.h>
#include <pylondataprocessing/IParameterCollection.h>
#include <pylondataprocessing/IUpdateObserver.h>
#include <pylondataprocessing/ParameterNames.h>
#include <pylondataprocessing/PylonDataProcessing.h>
#include <pylondataprocessing/PylonDataProcessingVersion.h>
#include <pylondataprocessing/Recipe.h>
#include <pylondataprocessing/Update.h>
#include <pylondataprocessing/Variant.h>
#include <pylondataprocessing/VariantContainer.h>
#include <pylondataprocessing/VariantDataType.h>
#if PYLON_DATAPROCESSING_VERSION_MAJOR >= 2
#include <pylondataprocessing/AcquisitionMode.h>
#include <pylondataprocessing/VariantContainerType.h>
#endif

namespace Pylon
{
    namespace DataProcessing
    {
        struct SGenericOutputObserverResult
        {
            CUpdate Update; //!< The update the output belongs to.
            intptr_t UserProvidedID = 0; //!< The user provided id belonging to the update.
            CVariantContainer Container; //!< The output data of the recipe.
        };

        class CGenericOutputObserver : public IOutputObserver
        {
        public:
            CGenericOutputObserver()
                : m_waitObject(Pylon::WaitObjectEx::Create())
            {
            }

            // Implements IOutputObserver::OutputDataPush.
            // This method is called when an output of the CRecipe pushes data out.
            // The call of the method can be performed by any thread of the thread pool of the recipe.
            void OutputDataPush(
                CRecipe& recipe,
                CVariantContainer value,
                const CUpdate& update,
                intptr_t userProvidedId) override
            {
                // Add data to the result queue in a thread-safe way.
                AutoLock scopedLock(m_memberLock);

                // The following variables are not used here:
                PYLON_UNUSED(recipe);

                SGenericOutputObserverResult outputData = {update, userProvidedId, value};
                m_queue.emplace_back(outputData);
                m_waitObject.Signal();
            }

            // Get the wait object for waiting for data.
            const WaitObject& GetWaitObject()
            {
                return m_waitObject;
            }

            size_t GetNumResults() const
            {
                AutoLock scopedLock(m_memberLock);
                return !m_queue.empty();
            }

            void Clear()
            {
                AutoLock scopedLock(m_memberLock);
                m_waitObject.Reset();
                m_queue.clear();
            }

            // Get one result data object from the queue.
            CVariantContainer GetResultContainer()
            {
                AutoLock scopedLock(m_memberLock);
                if (m_queue.empty())
                {
                    return CVariantContainer();
                }

                auto resultDataOut = std::move(m_queue.front());
                m_queue.pop_front();
                if (m_queue.empty())
                {
                    m_waitObject.Reset();
                }
                return resultDataOut.Container;
            }

            SGenericOutputObserverResult GetResult()
            {
                AutoLock scopedLock(m_memberLock);
                if (m_queue.empty())
                {
                    return {CUpdate(), 0, CVariantContainer()};
                }

                auto result = std::move(m_queue.front());
                m_queue.pop_front();
                if (m_queue.empty())
                {
                    m_waitObject.Reset();
                }
                return result;
            }

        private:
            mutable CLock m_memberLock;
            WaitObjectEx m_waitObject;
            std::list<SGenericOutputObserverResult> m_queue;
        };
#if PYLON_DATAPROCESSING_VERSION_MAJOR < 2
        /*!
         \brief
            Lists the built-in variant container types.
        **/
        enum EVariantContainerType
        {
            VariantContainerType_None           = 0,    //!< A basic data object without any container.
            VariantContainerType_Array          = 1,    //!< An array that may contain basic data objects.
            VariantContainerType_Unsupported    = 2     //!< A container type that is not supported natively by this SDK yet.
        };
#endif

        Pylon::VersionInfo GetVersion()
        {
            return Pylon::VersionInfo(PYLON_DATAPROCESSING_VERSION_MAJOR, PYLON_DATAPROCESSING_VERSION_MINOR, PYLON_DATAPROCESSING_VERSION_SUBMINOR);
        }
    }
}
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

///////////////////////////////////
//// fetch pylon definitions ////
///////////////////////////////////
%import "../pylon/pylon.i"

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

// the INode* factory
%typemap(out) GENAPI_NAMESPACE::INode* Pylon::DataProcessing::CRecipe::GetParameter
%{
    // Need a new scope here, so this block can be skipped
    // by a 'goto' or 'SWIG_fail'.
    {
        swig_type_info *outtype = 0;
        void * outptr = 0;
        if (0 == $1)
        {
            GENICAM_NAMESPACE::LogicalErrorException except(
                "Node not existing",
                __FILE__,
                __LINE__
                );
            TranslateGenicamException(&except);
            SWIG_fail;
        }
        else
        {
            switch ($1->GetPrincipalInterfaceType())
            {
                case GENAPI_NAMESPACE::intfIValue :
                    outtype = $descriptor(GENAPI_NAMESPACE::IValue*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIInteger :
                    outtype = $descriptor(GENAPI_NAMESPACE::IInteger*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIBoolean :
                    outtype = $descriptor(GENAPI_NAMESPACE::IBoolean*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>($1);
                    break;
                case GENAPI_NAMESPACE::intfICommand :
                    outtype = $descriptor(GENAPI_NAMESPACE::ICommand*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIFloat :
                    outtype = $descriptor(GENAPI_NAMESPACE::IFloat*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIString :
                    outtype = $descriptor(GENAPI_NAMESPACE::IString*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIRegister :
                    outtype = $descriptor(GENAPI_NAMESPACE::IRegister*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>($1);
                    break;
                case GENAPI_NAMESPACE::intfICategory :
                    outtype = $descriptor(GENAPI_NAMESPACE::ICategory*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIEnumeration :
                    outtype = $descriptor(GENAPI_NAMESPACE::IEnumeration*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIEnumEntry :
                    outtype = $descriptor(GENAPI_NAMESPACE::IEnumEntry*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIPort :
                    outtype = $descriptor(GENAPI_NAMESPACE::IPort*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>($1);
                    break;
                case GENAPI_NAMESPACE::intfIBase :
                    outtype = $descriptor(GENAPI_NAMESPACE::IBase*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>($1);
                    break;
            };
        }
        $result = SWIG_NewPointerObj(outptr, outtype, $owner);
    }
%}
////////////////////////////////////////////////////////////////////////////////

// Check typemap to make the TriggerUpdate overloads working with python dictionaries
%typemap(typecheck, precedence=SWIG_TYPECHECK_MAP)
Pylon::DataProcessing::CVariantContainer inputCollection,
Pylon::DataProcessing::CVariantContainer value
{
    // We need a list
    $1 = PyDict_Check($input) ? 1 : 0;
}

////////////////////////////////////////////////////////////////////////////////
// Convert a python dictionary of (String, CVariant) tuples
%typemap(in)
Pylon::DataProcessing::CVariantContainer inputCollection,
Pylon::DataProcessing::CVariantContainer value
{
    if (PyDict_Check($input))
    {
        PyObject *key = nullptr;
        PyObject *value = nullptr;
        Py_ssize_t pos = 0;

        while (PyDict_Next($input, &pos, &key, &value))
        {
            GENICAM_NAMESPACE::gcstring keyCpp;

            if (PyBytes_Check(key)) {
                keyCpp = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(key));
            } else
%#if PY_VERSION_HEX >= 0x03000000
            if(PyUnicode_Check(key)) {
                PyObject *utf8 = PyUnicode_AsUTF8String(key);
                keyCpp = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(utf8));
                Py_DECREF(utf8);
            }
%#else
            if(PyString_Check(key)) {
                keyCpp = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(key));
            }
%#endif
            else {
                PyErr_SetString(PyExc_ValueError, "Expected a string as key.");
                SWIG_fail;
            }

            // python object possibly wrapping a CVariant
            // pointer to wrapped CVariant
            void *wrappedVariant = 0;
            if (!SWIG_IsOK(
                    SWIG_ConvertPtr(value, &wrappedVariant, SWIGTYPE_p_Pylon__DataProcessing__CVariant, 0)
                    )
                )
            {
                PyErr_SetString(
                    PyExc_TypeError,
                    "Value must contain CVariant objects."
                    );
                SWIG_fail;
            }
            Pylon::DataProcessing::CVariant valueCpp(*reinterpret_cast<Pylon::DataProcessing::CVariant*>(wrappedVariant));
            $1[keyCpp] = valueCpp;
        }
    }
    else
    {
        PyErr_SetString(PyExc_TypeError,"not a dictionary");
        SWIG_fail;
    }
}
////////////////////////////////////////////////////////////////////////////////
%typemap(out) Pylon::DataProcessing::CVariantContainer (PyObject* obj)
%{
  obj = PyDict_New();
  for (const auto& n : $1) {
    PyObject* stringObject = PyUnicode_FromString(n.first.c_str());
    PyObject* variantObject = SWIG_NewPointerObj(SWIG_as_voidptr(new Pylon::DataProcessing::CVariant(n.second)), SWIGTYPE_p_Pylon__DataProcessing__CVariant, SWIG_POINTER_OWN);
    PyDict_SetItem(obj, stringObject, variantObject);
    Py_XDECREF(stringObject);
    Py_XDECREF(variantObject);
  }
  $result = SWIG_Python_AppendOutput($result, obj,$isvoid);
%}

////////////////////////////////////////////////////////////////////////////////

%typemap(directorin) Pylon::DataProcessing::CVariantContainer value (PyObject* obj)
%{
  obj = PyDict_New();
  for (const auto& n : $1) {
    PyObject* stringObject = PyUnicode_FromString(n.first.c_str());
    PyObject* variantObject = SWIG_NewPointerObj(SWIG_as_voidptr(new Pylon::DataProcessing::CVariant(n.second)), SWIGTYPE_p_Pylon__DataProcessing__CVariant, SWIG_POINTER_OWN);
    PyDict_SetItem(obj, stringObject, variantObject);
    Py_XDECREF(stringObject);
    Py_XDECREF(variantObject);
  }
  $input = obj;
%}
//////////////////////////////////////////////////////////////////////////////

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

%define SAFE_NESTED_STRUCT_ACCESS(membertypename, membername)

    %pythoncode
    %{
        def _Get_##membername(self):
            result = self._##membername # creates a new SWIG wrapper containing a pointer to the wrapped C++ object of self
            result._myParentStruct = self #we add a reference to the parent here to work around lifetime issues
            return result
        def _Set_##membername(self, value):
            self._##membername = value
        membername = property(_Get_##membername, _Set_##membername )
    %}

%enddef

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

#define PYLONDATAPROCESSING_API
%include <pylondataprocessing/PylonDataProcessingVersion.h>
namespace Pylon
{
    namespace DataProcessing
    {
        Pylon::VersionInfo GetVersion()
        {
            return Pylon::VersionInfo(PYLON_DATAPROCESSING_VERSION_MAJOR, PYLON_DATAPROCESSING_VERSION_MINOR, PYLON_DATAPROCESSING_VERSION_SUBMINOR);
        }
    }
}
#if PYLON_DATAPROCESSING_VERSION_MAJOR >= 2
%include "AcquisitionMode.i"
#endif
%include "PointF2D.i"
%include "LineF2D.i"
%include "EllipseF.i"
%include "CircleF.i"
%include "RectangleF.i"
%include "RegionEntry.i"
%include "RegionType.i"
%include "TransformationData.i"
%include "Region.i"
%include "VariantDataType.i"
%include "VariantContainerType.i"
%include "Variant.i"
%include "Update.i"
%include "QueueMode.i"
%include "VariantContainer.i"
%include "OutputObserver.i"
%include "GenericOutputObserver.i"
%include "UpdateObserver.i"
%include "EventObserver.i"
%include "Recipe.i"
#if ((PYLON_DATAPROCESSING_VERSION_MAJOR > 3) || (PYLON_DATAPROCESSING_VERSION_MAJOR >= 3 && PYLON_DATAPROCESSING_VERSION_MINOR >= 1))
%include "RecipeFileFormat.i"
#endif
%include "BuildersRecipe.i"

ADD_PROP_GET(TransformationData, ColumnCount)
ADD_PROP_GET(TransformationData, RowCount)
ADD_PROP_GET(Region, RegionType)
ADD_PROP_GET(Region, AllocatedBufferSize)
ADD_PROP_GET(Region, DataSize)
ADD_PROP_GET(Region, ReferenceWidth)
ADD_PROP_GET(Region, ReferenceHeight)
ADD_PROP_GET(Region, BoundingBoxTopLeftX)
ADD_PROP_GET(Region, BoundingBoxTopLeftY)
ADD_PROP_GET(Region, BoundingBoxWidth)
ADD_PROP_GET(Region, BoundingBoxHeight)
ADD_PROP_GET(Variant, DataType)
ADD_PROP_GET(Variant, NumSubValues)
ADD_PROP_GET(Variant, NumArrayValues)
ADD_PROP_GET(Update, NumPrecedingUpdates)
ADD_PROP_GET(Recipe, RecipeContext)
ADD_PROP_GET(GenericOutputObserver, NumResults)
ADD_PROP_GET(GenericOutputObserver, WaitObject)
