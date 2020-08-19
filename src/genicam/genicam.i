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

%module(directors="1", package="pypylon", docstring=DOCSTRING) genicam
%include "DoxyGenApi.i";
%begin %{

// allow debug builds of genicam wrapper against release build of python
# ifdef _DEBUG
#  ifdef _MSC_VER
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


%include "std_string.i"
%include "std_map.i"
%include "std_vector.i"
%include "cstring.i"
%include "std_ios.i"
%include "exception.i"
%include "pybuffer.i"


%{

#include <vector>
#include <exception>
#include <stdexcept>

// python defines own version of COMPILER macro which collides with genicam logic
#define _PYTHON_COMPILER COMPILER
#undef COMPILER
#include <GenICam.h>

#include <GenApi/EnumClasses.h>
#include <GenApi/ChunkPort.h>
#include <GenApi/ChunkAdapter.h>
#include <GenApi/ChunkAdapterGeneric.h>
#include <GenApi/ChunkAdapterGEV.h>
#include <GenApi/ChunkAdapterU3V.h>
#include <GenApi/EventPort.h>
#include <GenApi/EventAdapter.h>
#include <GenApi/EventAdapterGeneric.h>
#include <GenApi/EventAdapterGEV.h>
#include <GenApi/EventAdapterU3V.h>
#include <Base/GCException.h>

#define COMPILER _PYTHON_COMPILER
#undef _PYTHON_COMPILER

// namespace for using genicam
using namespace GENICAM_NAMESPACE;
using namespace GENAPI_NAMESPACE;
%}

///////////////////////
//////  stdint ////////
///////////////////////


%include <swigarch.i>

#ifdef _WIN32

#if defined(SWIGWORDSIZE64) || defined(SWIGWORDSIZE32)
#error "On windows SWIGWORDSIZE32/64 must not be used as it is not correctly implemented in swig."
#endif

typedef signed char        int8_t;
typedef short              int16_t;
typedef int                int32_t;
typedef long long          int64_t;
typedef unsigned char      uint8_t;
typedef unsigned short     uint16_t;
typedef unsigned int       uint32_t;
typedef unsigned long long uint64_t;

typedef signed char        int_least8_t;
typedef short              int_least16_t;
typedef int                int_least32_t;
typedef long long          int_least64_t;
typedef unsigned char      uint_least8_t;
typedef unsigned short     uint_least16_t;
typedef unsigned int       uint_least32_t;
typedef unsigned long long uint_least64_t;

typedef signed char        int_fast8_t;
typedef int                int_fast16_t;
typedef int                int_fast32_t;
typedef long long          int_fast64_t;
typedef unsigned char      uint_fast8_t;
typedef unsigned int       uint_fast16_t;
typedef unsigned int       uint_fast32_t;
typedef unsigned long long uint_fast64_t;

typedef long long          intmax_t;
typedef unsigned long long uintmax_t;

#ifdef _WIN64
    typedef unsigned long long  size_t;
    typedef long long           ptrdiff_t;
    typedef long long           intptr_t;
    typedef unsigned long long  uintptr_t;
#else
    typedef unsigned int        size_t;
    typedef int                 ptrdiff_t;
    typedef int                 intptr_t;
    typedef unsigned int        uintptr_t;
#endif

#else // _WIN32

/* Exact integral types.  */

#if !defined(SWIGWORDSIZE64) && !defined(SWIGWORDSIZE32)
#error "On linux either SWIGWORDSIZE64 or SWIGWORDSIZE32 must be defined on the command line."
#endif

/* Signed.  */
typedef signed char             int8_t;
typedef short int               int16_t;
typedef int                     int32_t;
#if defined(SWIGWORDSIZE64)
typedef long int                int64_t;
#else
typedef long long int           int64_t;
#endif

/* Unsigned.  */
typedef unsigned char           uint8_t;
typedef unsigned short int      uint16_t;
typedef unsigned int            uint32_t;
#if defined(SWIGWORDSIZE64)
typedef unsigned long int       uint64_t;
#else
typedef unsigned long long int  uint64_t;
#endif


/* Small types.  */

/* Signed.  */
typedef signed char             int_least8_t;
typedef short int               int_least16_t;
typedef int                     int_least32_t;
#if defined(SWIGWORDSIZE64)
typedef long int                int_least64_t;
#else
typedef long long int           int_least64_t;
#endif

/* Unsigned.  */
typedef unsigned char           uint_least8_t;
typedef unsigned short int      uint_least16_t;
typedef unsigned int            uint_least32_t;
#if defined(SWIGWORDSIZE64)
typedef unsigned long int       uint_least64_t;
#else
typedef unsigned long long int  uint_least64_t;
#endif


/* Fast types.  */

/* Signed.  */
typedef signed char             int_fast8_t;
#if defined(SWIGWORDSIZE64)
typedef long int                int_fast16_t;
typedef long int                int_fast32_t;
typedef long int                int_fast64_t;
#else
typedef int                     int_fast16_t;
typedef int                     int_fast32_t;
typedef long long int           int_fast64_t;
#endif

/* Unsigned.  */
typedef unsigned char           uint_fast8_t;
#if defined(SWIGWORDSIZE64)
typedef unsigned long int       uint_fast16_t;
typedef unsigned long int       uint_fast32_t;
typedef unsigned long int       uint_fast64_t;
#else
typedef unsigned int            uint_fast16_t;
typedef unsigned int            uint_fast32_t;
typedef unsigned long long int  uint_fast64_t;
#endif


/* Types for `void *' pointers.  */
#if defined(SWIGWORDSIZE64)
typedef long int                intptr_t;
typedef unsigned long int       uintptr_t;
#else
typedef int                     intptr_t;
typedef unsigned int            uintptr_t;
#endif



/* Largest integral types.  */
#if defined(SWIGWORDSIZE64)
typedef long int                intmax_t;
typedef unsigned long int       uintmax_t;
#else
typedef long long int           intmax_t;
typedef unsigned long long int  uintmax_t;
#endif

#endif // _WIN32

////////////////////////////////////////////

#define MODULE_NAME _genicam
%include "GCException.i"
#undef MODULE_NAME

%typemap(in) (uint8_t *pBuffer, int64_t Length), (void *pBuffer, int64_t Length), (char *pBuffer, int64_t Length)
{
    $2 = PyLong_AsLongLong($input);
    if (PyErr_Occurred()) SWIG_fail;
    if ( ($2 < 0) || ($2 > INT_MAX) ) {
        PyErr_SetString(PyExc_ValueError, "Invalid Length: 0 >= Length <= INT_MAX");
        SWIG_fail;
    }
    $1 = ($1_ltype) new char[(int)$2+1];
}



%typemap(argout,fragment="t_output_helper") (uint8_t *pBuffer, int64_t Length), (void *pBuffer, int64_t Length), (char *pBuffer, int64_t Length)
{
    PyObject *o;
    if ( ($2 < 0) || ($2 > INT_MAX) ) {
        PyErr_SetString(PyExc_ValueError, "Invalid Length: 0 >= Length <= INT_MAX");
        SWIG_fail;
    }
    o = PyBytes_FromStringAndSize((const char*)$1,(int)$2);
    $result = t_output_helper($result,o);
}

%typemap(freearg,fragment="t_output_helper") (uint8_t *pBuffer, int64_t Length), (void *pBuffer, int64_t Length), (char *pBuffer, int64_t Length)
{
    delete [] (char*)$1;
}

%define %pybuffer_binary_input(TYPEMAP, SIZE)
%typemap(in, noblock=1) (TYPEMAP, SIZE)
{
%#if PY_VERSION_HEX >= 0x03000000
    Py_buffer buffer_view;
    int get_buf_res;
    get_buf_res = PyObject_GetBuffer($input, &buffer_view, PyBUF_SIMPLE);
    if (get_buf_res < 0)
    {
        PyErr_Clear();
        %argument_fail(get_buf_res, "(TYPEMAP, SIZE)", $symname, $argnum);
    }
    $1 = ($1_ltype) buffer_view.buf;
    $2 = ($2_ltype) buffer_view.len;
%#else
    Py_ssize_t size;
    const void *buf;
    int get_buf_res;
    size = 0;
    buf = 0;
    get_buf_res = PyObject_AsReadBuffer($input, &buf, &size);
    if (get_buf_res < 0)
    {
        PyErr_Clear();
        %argument_fail(get_buf_res, "(TYPEMAP, SIZE)", $symname, $argnum);
    }
    $1 = ($1_ltype) buf;
    $2 = ($2_ltype) (size);
%#endif
}
%typemap(freearg, noblock=1) (TYPEMAP, SIZE)
{
%#if PY_VERSION_HEX >= 0x03000000
    PyBuffer_Release(&buffer_view);
%#endif
}
%enddef


%pybuffer_binary_input(const uint8_t *pBuffer, int64_t Length);
%pybuffer_binary_input(const void *pBuffer, int64_t Length);
%pybuffer_binary_input(uint8_t *pBuffer, int64_t BufferLength);
%pybuffer_binary_input(const uint8_t msg[], uint32_t numBytes);
%pybuffer_binary_input(const char *pBuffer, int64_t Length);

////////////


%typemap(typecheck,precedence=SWIG_TYPECHECK_CHAR)  (const uint8_t* pBuffer, int64_t Length),
                                                    (const void *pBuffer, int64_t Length),
                                                    (uint8_t *pBuffer, int64_t BufferLength),
                                                    uint8_t *pChunkBuffer,
                                                    (const uint8_t msg[], uint32_t numBytes)
{
    $1 = PyBytes_Check($input) ? 1 : 0;
}

%typemap(typecheck,precedence=SWIG_TYPECHECK_CHAR) (uint8_t* pBuffer, int64_t Length) ,(void* pBuffer, int64_t Length)
{
    $1 = ( PyLong_Check($input) || PyInt_Check($input) )? 1 : 0;
}



namespace GENICAM_NAMESPACE {
%typemap(out) GENICAM_NAMESPACE::gcstring {
%#if PY_VERSION_HEX >= 0x03000000
    $result = PyUnicode_FromStringAndSize($1.c_str(),$1.length());
%#else
    $result = PyString_FromStringAndSize($1.c_str(),$1.length());
%#endif
}

%typemap(in) GENICAM_NAMESPACE::gcstring {
    if (PyBytes_Check($input)) {
        $1 = GENICAM_NAMESPACE::gcstring(PyBytes_AsString($input));
    } else
%#if PY_VERSION_HEX >= 0x03000000
    if(PyUnicode_Check($input)) {
        PyObject *utf8 = PyUnicode_AsUTF8String($input);
        $1 = GENICAM_NAMESPACE::gcstring(PyBytes_AsString(utf8));
        Py_DECREF(utf8);
    }
%#else
    if(PyString_Check($input)) {
        $1 = GENICAM_NAMESPACE::gcstring(PyBytes_AsString($input));
    }
%#endif
    else {
        PyErr_SetString(PyExc_ValueError,"Expected a string");
        SWIG_fail;
    }
}

%typemap(in) const GENICAM_NAMESPACE::gcstring & {
    if (PyBytes_Check($input)) {
        $1 = new GENICAM_NAMESPACE::gcstring(PyBytes_AsString($input));
    } else
%#if PY_VERSION_HEX >= 0x03000000
    if(PyUnicode_Check($input)) {
        PyObject *utf8 = PyUnicode_AsUTF8String($input);
        $1 = new GENICAM_NAMESPACE::gcstring(PyBytes_AsString(utf8));
        Py_DECREF(utf8);
    }
%#else
    if(PyString_Check($input)) {
        $1 = new GENICAM_NAMESPACE::gcstring(PyBytes_AsString($input));
    }
%#endif
    else {
        PyErr_SetString(PyExc_ValueError,"Expected a string");
        SWIG_fail;
    }
}


%typemap(freearg) const GENICAM_NAMESPACE::gcstring & {
    delete $1;
}

%typemap(in,numinputs=0) GENICAM_NAMESPACE::gcstring & {
    $1 = new GENICAM_NAMESPACE::gcstring();
}

// Make sure the non-const typemap below will not match the const params
%typemap(argout) const GENICAM_NAMESPACE::gcstring & {}
%typemap(argout) GENICAM_NAMESPACE::gcstring & {
%#if PY_VERSION_HEX >= 0x03000000
    $result = t_output_helper($result,PyUnicode_FromStringAndSize($1->c_str(),$1->length()));
%#else
    $result = t_output_helper($result,PyString_FromStringAndSize($1->c_str(),$1->length()));
%#endif
}

%typemap(freearg) GENICAM_NAMESPACE::gcstring & {
    delete $1;
}

%typemap(in,numinputs=0) GENICAM_NAMESPACE::Version_t & {
    $1 = new GENICAM_NAMESPACE::Version_t();
}

%typemap(argout) GENICAM_NAMESPACE::Version_t&{
    $result = SWIG_NewPointerObj($1, $descriptor(GENICAM_NAMESPACE::Version_t*), 1 /*python owns*/);
}

// Copy the typecheck code for "char *".
%typemap(typecheck) GENICAM_NAMESPACE::gcstring = char *;

// Copy the typecheck code for "char *".
%typemap(typecheck) const GENICAM_NAMESPACE::gcstring & = const char *;
}

%typemap(directorin) (const void *pBuffer, int64_t Length) {
    if ( (Length < 0) || (Length > INT_MAX) ) {
        Swig::DirectorMethodException::raise("Length too large ");
    }
    $input = PyBytes_FromStringAndSize((const char*)$1,(int)$2);
}

%typemap(directorin) (void *pBuffer, int64_t Length) {
    if ( (Length < 0) || (Length > INT_MAX) ) {
        Swig::DirectorMethodException::raise("Length too large ");
    }
    $input = PyLong_FromLongLong(int($2));
}

%typemap(directorargout) (void *pBuffer, int64_t Length) {
    if ( !PyBytes_Check(result)){
        Swig::DirectorMethodException::raise("Method must return a buffer");
    }
    if ( PyBytes_Size(result) != Length){
        Swig::DirectorMethodException::raise("Method must return exactly Length byte");
    }
    void *p = (void*)PyBytes_AsString(result);
    memcpy(pBuffer,p,int($2));
}

%typemap(in, numinputs=0) GENAPI_NAMESPACE::NodeList_t & {
    $1 = new NodeList_t();
}

%typemap(argout,fragment="t_output_helper") GENAPI_NAMESPACE::NodeList_t & {
    PyObject *o = PyTuple_New($1->size());
    for( unsigned int i = 0; i < $1->size(); i++){
        PyObject *o_item;
        INode* n = (*$1)[i];
        swig_type_info *outtype = 0;
        void * outptr = 0;
        switch (n->GetPrincipalInterfaceType()){
             case intfIValue :
                        outtype = $descriptor(GENAPI_NAMESPACE::IValue*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>(n);
                        break;
             case intfIInteger :
                        outtype = $descriptor(GENAPI_NAMESPACE::IInteger*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>(n);
                         break;
              case intfIBoolean :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBoolean*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>(n);
                         break;
             case intfICommand :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICommand*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>(n);
                         break;
             case intfIFloat :
                        outtype = $descriptor(GENAPI_NAMESPACE::IFloat*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>(n);
                         break;
             case intfIString :
                        outtype = $descriptor(GENAPI_NAMESPACE::IString*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>(n);
                         break;
             case intfIRegister :
                        outtype = $descriptor(GENAPI_NAMESPACE::IRegister*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>(n);
                         break;
             case intfICategory :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICategory*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>(n);
                         break;
             case intfIEnumeration :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumeration*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>(n);
                         break;
             case intfIEnumEntry :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumEntry*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>(n);
                         break;
             case intfIPort :
                        outtype = $descriptor(GENAPI_NAMESPACE::IPort*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>(n);
                         break;
             case intfIBase :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBase*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>(n);
                         break;
            };
        o_item = SWIG_NewPointerObj(outptr, outtype, 0);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = t_output_helper($result,o);
    delete $1;
}

%typemap(out) int64_autovector_t {
    PyObject *o = PyTuple_New($1.size());
    for( unsigned int i = 0; i < $1.size(); i++){
        PyObject *o_item;
        o_item = PyLong_FromLongLong($1[i]);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = t_output_helper($result,o);
}

%typemap(out) double_autovector_t {
    PyObject *o = PyTuple_New($1.size());
    for( unsigned int i = 0; i < $1.size(); i++){
        PyObject *o_item;
        o_item = PyFloat_FromDouble($1[i]);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = t_output_helper($result,o);
}


%typemap(in, numinputs=0) GENAPI_NAMESPACE::FeatureList_t & {
    $1 = new FeatureList_t();
}

%typemap(argout,fragment="t_output_helper") GENAPI_NAMESPACE::FeatureList_t & {
    PyObject *o = PyTuple_New($1->size());
    for( unsigned int i = 0; i < $1->size(); i++){
        PyObject *o_item;
        INode* n = dynamic_cast<GENAPI_NAMESPACE::INode*>((*$1)[i]);
        swig_type_info *outtype = 0;
        void * outptr = 0;
        switch (n->GetPrincipalInterfaceType()){
             case intfIValue :
                        outtype = $descriptor(GENAPI_NAMESPACE::IValue*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>(n);
                        break;
             case intfIInteger :
                        outtype = $descriptor(GENAPI_NAMESPACE::IInteger*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>(n);
                         break;
              case intfIBoolean :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBoolean*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>(n);
                         break;
             case intfICommand :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICommand*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>(n);
                         break;
             case intfIFloat :
                        outtype = $descriptor(GENAPI_NAMESPACE::IFloat*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>(n);
                         break;
             case intfIString :
                        outtype = $descriptor(GENAPI_NAMESPACE::IString*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>(n);
                         break;
             case intfIRegister :
                        outtype = $descriptor(GENAPI_NAMESPACE::IRegister*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>(n);
                         break;
             case intfICategory :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICategory*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>(n);
                         break;
             case intfIEnumeration :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumeration*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>(n);
                         break;
             case intfIEnumEntry :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumEntry*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>(n);
                         break;
             case intfIPort :
                        outtype = $descriptor(GENAPI_NAMESPACE::IPort*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>(n);
                         break;
             case intfIBase :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBase*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>(n);
                         break;
            };
        o_item = SWIG_NewPointerObj(outptr, outtype, 0);
        PyTuple_SetItem(o,i,o_item);
    }
    $result = t_output_helper($result,o);
    delete $1;
}

%typemap(in, numinputs=0) GENICAM_NAMESPACE::gcstring_vector & {
    $1 = new GENICAM_NAMESPACE::gcstring_vector();
}

%typemap(argout,fragment="t_output_helper") GENICAM_NAMESPACE::gcstring_vector & {
    PyObject *o = PyTuple_New($1->size());
    for( unsigned int i = 0; i < $1->size(); i++){
      PyObject *o_item;
%#if PY_VERSION_HEX >= 0x03000000
      o_item = PyUnicode_FromStringAndSize((*$1)[i].c_str(),(*$1)[i].length());
%#else
      o_item = PyString_FromStringAndSize((*$1)[i].c_str(),(*$1)[i].length());
%#endif
      PyTuple_SetItem(o,i,o_item);
    }
    $result = t_output_helper($result,o);
    delete $1;
}

// Make sure the above typemap is no applied on const references
%typemap(argout,fragment="t_output_helper") const GENICAM_NAMESPACE::gcstring_vector & {}


// typemaps for chunk handling

%typemap(in) uint8_t *pChunkBuffer {
    $1 = reinterpret_cast<uint8_t *>(PyBytes_AsString($input));
}

// map a list of SingleChunkData_t elements to c++ array
%typecheck(SWIG_TYPECHECK_POINTER) (GENAPI_NAMESPACE::SingleChunkData_t *ChunkData, int64_t NumChunks)
{
    void *check_data;
    $1 = (  PySequence_Check($input)
        && (PySequence_Length($input) > 0)
        && (SWIG_IsOK(SWIG_ConvertPtr(PySequence_GetItem($input,0),&check_data,SWIGTYPE_p_GENAPI_NAMESPACE__SingleChunkData_t, 0 )))
    )? 1 : 0;
}

%typecheck(SWIG_TYPECHECK_POINTER) (GENAPI_NAMESPACE::SingleChunkDataStr_t *ChunkData, int64_t NumChunks)
{
    void *check_data_str;
    $1 = (  PySequence_Check($input)
        && (PySequence_Length($input) > 0)
        && (SWIG_IsOK(SWIG_ConvertPtr(PySequence_GetItem($input,0),&check_data_str,SWIGTYPE_p_GENAPI_NAMESPACE__SingleChunkDataStr_t, 0 )))
    )? 1 : 0;
}

%typemap(in) (GENAPI_NAMESPACE::SingleChunkData_t *ChunkData, int64_t NumChunks) {
    if (!PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
        SWIG_fail;
    }
    $1 = new GENAPI_NAMESPACE::SingleChunkData_t[PySequence_Length($input)];
    $2 = PySequence_Length($input);
    for (int i =0; i < PySequence_Length($input); i++) {
        PyObject *o = PySequence_GetItem($input,i);
        // TODO: add more checking code here
        void *item = 0 ;
        SWIG_ConvertPtr(o, &item,SWIGTYPE_p_GENAPI_NAMESPACE__SingleChunkData_t, 0 );
        reinterpret_cast<GENAPI_NAMESPACE::SingleChunkData_t*>($1)[i] = *reinterpret_cast<GENAPI_NAMESPACE::SingleChunkData_t*>(item);
        Py_DECREF(o);
    }
}

%typemap(argout) (GENAPI_NAMESPACE::SingleChunkData_t *ChunkData, int64_t NumChunks) {
    delete $1;
}

%typemap(in) (GENAPI_NAMESPACE::SingleChunkDataStr_t *ChunkData, int64_t NumChunks) {
    if (!PySequence_Check($input)) {
        PyErr_SetString(PyExc_TypeError,"Expecting a sequence");
        return NULL;
    }
    $1 = new GENAPI_NAMESPACE::SingleChunkDataStr_t[PySequence_Length($input)];
    $2 = PySequence_Length($input);
    for (int i =0; i < PySequence_Length($input); i++) {
        PyObject *o = PySequence_GetItem($input,i);
        // TODO: add more checking code here
        void *item = 0 ;
        SWIG_ConvertPtr(o, &item,SWIGTYPE_p_GENAPI_NAMESPACE__SingleChunkDataStr_t, 0 );
        reinterpret_cast<GENAPI_NAMESPACE::SingleChunkDataStr_t*>($1)[i] = *reinterpret_cast<GENAPI_NAMESPACE::SingleChunkDataStr_t*>(item);
        Py_DECREF(o);
    }
}

%typemap(argout) (GENAPI_NAMESPACE::SingleChunkDataStr_t *ChunkData, int64_t NumChunks) {
    delete $1;
}



// the INode* factory
%typemap(out) GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::INodeMap::GetNode,
              GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::CNodeMapRef::_GetNode,
              GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::CNodeMapRef::GetNode,
              GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::IEnumEnumeration::GetCurrentEntry,
              GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::INode::GetAlias,
              GENAPI_NAMESPACE::INode* GENAPI_NAMESPACE::INode::GetCastAlias
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
                case intfIValue :
                    outtype = $descriptor(GENAPI_NAMESPACE::IValue*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>($1);
                    break;
                case intfIInteger :
                    outtype = $descriptor(GENAPI_NAMESPACE::IInteger*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>($1);
                    break;
                case intfIBoolean :
                    outtype = $descriptor(GENAPI_NAMESPACE::IBoolean*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>($1);
                    break;
                case intfICommand :
                    outtype = $descriptor(GENAPI_NAMESPACE::ICommand*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>($1);
                    break;
                case intfIFloat :
                    outtype = $descriptor(GENAPI_NAMESPACE::IFloat*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>($1);
                    break;
                case intfIString :
                    outtype = $descriptor(GENAPI_NAMESPACE::IString*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>($1);
                    break;
                case intfIRegister :
                    outtype = $descriptor(GENAPI_NAMESPACE::IRegister*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>($1);
                    break;
                case intfICategory :
                    outtype = $descriptor(GENAPI_NAMESPACE::ICategory*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>($1);
                    break;
                case intfIEnumeration :
                    outtype = $descriptor(GENAPI_NAMESPACE::IEnumeration*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>($1);
                    break;
                case intfIEnumEntry :
                    outtype = $descriptor(GENAPI_NAMESPACE::IEnumEntry*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>($1);
                    break;
                case intfIPort :
                    outtype = $descriptor(GENAPI_NAMESPACE::IPort*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>($1);
                    break;
                case intfIBase :
                    outtype = $descriptor(GENAPI_NAMESPACE::IBase*);
                    outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>($1);
                    break;
            };
        }
        $result = SWIG_NewPointerObj(outptr, outtype, $owner);
    }
%}


%define PROP_GET(name)
    %pythoncode %{ name = property(Get ## name) %}
%enddef

%define PROP_GETSET(name)
    %pythoncode %{ name = property(Get ## name,Set ## name) %}
%enddef

// definitions to directly include the SDK headers
#define GENAPI_DECL

//TODO Adapt
#define GENAPI_DECL_ABSTRACT
#define interface struct

// ignore assignment operator in all classes
%ignore *::operator=;

%include "Types.i"
%include "EnumClasses.i"
%include "Version.i"
%include "IBase.i"
%include "INode.i"
%include "INodeMap.i"
%include "NodeCallback.i"
%include "IValue.i"
%include "Container.i"
%include "IPort.i"
%include "IChunkPort.i"
%include "IPortConstruct.i"
%include "IPortRecorder.i"
%include "PortImpl.i"
%include "IDeviceInfo.i"
%include "CNodeMapRef.i"
%include "IFloat.i"
%include "IInteger.i"
%include "IRegister.i"
%include "IEnumEntry.i"
%include "IEnumeration.i"
%include "IBoolean.i"
%include "ICommand.i"
%include "IString.i"
%include "ICategory.i"
%include "Reference.i"
%include "ISelector.i"
%include "ISelectorDigit.i"
%include "SelectorSet.i"
%include "ChunkPort.i"
%include "ChunkAdapter.i"
%include "ChunkAdapterGEV.i"
%include "ChunkAdapterU3V.i"
%include "ChunkAdapterGeneric.i"
%include "EventPort.i"
%include "EventAdapter.i"
%include "EventAdapterGEV.i"
%include "EventAdapterU3V.i"
%include "EventAdapterGeneric.i"
%include "FileProtocolAdapter.i"

// circumvent macro eval order of SWIG to implement attributes on
// template classes

%define ADD_PROP_GET(class, name)
    %pythoncode %{ class ## .name = property(class ## .Get ## name) %}
%enddef

%define ADD_PROP_GETSET(class, name)
    %pythoncode %{ class ## .name = property(class ## .Get ## name,class ## .Set ## name) %}
%enddef



