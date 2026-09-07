////////////////////////////////////////////////////////////////////////////////
//
// Pylon::IBufferFactory is a pure interface used to plug a user-provided
// buffer allocator into Pylon::CInstantCamera::SetBufferFactory(). Its real
// C++ ABI (AllocateBuffer()/FreeBuffer() with "void**"/"intptr_t&"
// out-parameters, called by the pylon grab engine - potentially from threads
// that never held the GIL) is not pythonic and there is no director typemap
// combination in this codebase for marshalling such out-parameters through a
// director callback.
//
// Instead of using a SWIG director, this file hand-implements a small
// internal C++ adapter (Pylon::CPyBufferFactory, exposed to Python as the
// private "_BufferFactoryAdapter") that:
//   * is the actual Pylon::IBufferFactory instance handed to pylon,
//   * forwards AllocateBuffer()/FreeBuffer()/DestroyBufferFactory() calls to
//     a plain Python object (any instance of the pypylon.pylon.BufferFactory
//     duck-typed base class defined below) using the plain CPython C-API,
//     acquiring the GIL as needed since these calls may originate from
//     non-Python threads,
//   * boxes the user-supplied Python "context" object (together with a
//     reference to the owning BufferFactory) behind the intptr_t
//     "bufferContext" value that pylon carries unchanged between
//     AllocateBuffer() and FreeBuffer(). There is no global registry: the box
//     is a small heap-allocated object (Pylon::CPyBufferContextBox, defined in
//     BufferFactoryContext.h and shared with GrabResultData.i, which unboxes
//     it again in CGrabResultData::GetBufferContext()) owned exclusively
//     through this intptr_t value and freed exactly once, in FreeBuffer().
//
// pypylon.pylon.BufferFactory itself is a plain Python base class (see the
// %pythoncode block below); it does not need to derive from any SWIG-wrapped
// type.
//
////////////////////////////////////////////////////////////////////////////////

// The real ABI methods are not pythonic and must never be called from
// Python; only the class itself needs to be known to SWIG so that
// _BufferFactoryAdapter can be upcast to IBufferFactory* for SetBufferFactory().
%ignore Pylon::IBufferFactory::AllocateBuffer;
%ignore Pylon::IBufferFactory::FreeBuffer;
%ignore Pylon::IBufferFactory::DestroyBufferFactory;
%rename(_IBufferFactory) Pylon::IBufferFactory;

%include <pylon/BufferFactory.h>

%{
#include <pylon/BufferFactory.h>
#include "pylon/BufferFactoryContext.h"
#include <stdexcept>
#include <string>

namespace Pylon
{

    // The actual Pylon::IBufferFactory instance handed to
    // CInstantCamera::SetBufferFactory(). Forwards to a plain Python object
    // (an instance of a class implementing the pypylon.pylon.BufferFactory
    // interface) using the plain CPython C-API.
    class CPyBufferFactory : public Pylon::IBufferFactory
    {
    public:
        // pyFactory is a borrowed reference; a new strong reference is taken
        // and held until DestroyBufferFactory() releases it.
        explicit CPyBufferFactory( PyObject* pyFactory )
            : m_pyFactory( pyFactory )
        {
            Py_XINCREF( m_pyFactory );
        }

        virtual ~CPyBufferFactory()
        {
        }

        virtual void AllocateBuffer( size_t bufferSize, void** pCreatedBuffer, intptr_t& bufferContext )
        {
            PyGILState_STATE gstate = PyGILState_Ensure();

            *pCreatedBuffer = NULL;
            bufferContext = 0;

            PyObject* pResult = PyObject_CallMethod( m_pyFactory, "AllocateBuffer", "n", (Py_ssize_t) bufferSize );
            if (!pResult)
            {
                std::string message = DescribeCurrentPythonError( "BufferFactory.AllocateBuffer() failed" );
                PyGILState_Release( gstate );
                throw RUNTIME_EXCEPTION( message.c_str() );
            }

            PyObject* pBufferObj = pResult;
            PyObject* pContextObj = NULL;
            if (PyTuple_Check( pResult ))
            {
                Py_ssize_t size = PyTuple_Size( pResult );
                if (size == 2)
                {
                    pBufferObj = PyTuple_GET_ITEM( pResult, 0 );
                    pContextObj = PyTuple_GET_ITEM( pResult, 1 );
                }
                else if (size == 1)
                {
                    pBufferObj = PyTuple_GET_ITEM( pResult, 0 );
                }
                else
                {
                    Py_DECREF( pResult );
                    PyGILState_Release( gstate );
                    throw RUNTIME_EXCEPTION(
                        "BufferFactory.AllocateBuffer() must return (buffer, context), (buffer,), or buffer." );
                }
            }

            void* pBuffer = NULL;
            if (pBufferObj != Py_None)
            {
                pBuffer = PyLong_AsVoidPtr( pBufferObj );
                if (pBuffer == NULL && PyErr_Occurred())
                {
                    std::string message = DescribeCurrentPythonError(
                        "BufferFactory.AllocateBuffer() must return the allocated buffer address (int) as the "
                        "first element (or as the sole return value)" );
                    Py_DECREF( pResult );
                    PyGILState_Release( gstate );
                    throw RUNTIME_EXCEPTION( message.c_str() );
                }
            }

            *pCreatedBuffer = pBuffer;
            if (pBuffer)
            {
                bufferContext = reinterpret_cast<intptr_t>( new CPyBufferContextBox( pContextObj, m_pyFactory ) );
            }
            else
            {
                bufferContext = 0;
            }

            Py_DECREF( pResult );
            PyGILState_Release( gstate );
        }

        virtual void FreeBuffer( void* pCreatedBuffer, intptr_t bufferContext )
        {
            PyGILState_STATE gstate = PyGILState_Ensure();

            CPyBufferContextBox* pBox = reinterpret_cast<CPyBufferContextBox*>( bufferContext );
            PyObject* pContext = (pBox && pBox->GetContext()) ? pBox->GetContext() : Py_None;

            PyObject* pBufferObj = pCreatedBuffer ? PyLong_FromVoidPtr( pCreatedBuffer ) : NewNoneRef();

            PyObject* pResult = PyObject_CallMethod( m_pyFactory, "FreeBuffer", "NO", pBufferObj, pContext );
            if (!pResult)
            {
                // FreeBuffer() must not throw (see Pylon::IBufferFactory::FreeBuffer()):
                // log and ignore, matching pylon's own handling of DestroyBufferFactory().
                PyErr_WriteUnraisable( m_pyFactory );
                PyErr_Clear();
            }
            else
            {
                Py_DECREF( pResult );
            }

            delete pBox;

            PyGILState_Release( gstate );
        }

        virtual void DestroyBufferFactory()
        {
            PyGILState_STATE gstate = PyGILState_Ensure();

            PyObject* pResult = PyObject_CallMethod( m_pyFactory, "OnReleased", NULL );
            if (!pResult)
            {
                // Exceptions from OnReleased() are logged and ignored, matching
                // pylon's own handling of DestroyBufferFactory().
                PyErr_WriteUnraisable( m_pyFactory );
                PyErr_Clear();
            }
            else
            {
                Py_DECREF( pResult );
            }

            Py_CLEAR( m_pyFactory );

            PyGILState_Release( gstate );

            delete this;
        }

    private:
        static PyObject* NewNoneRef() { Py_INCREF( Py_None ); return Py_None; }

        // Builds an error message from the currently set Python exception
        // (which is cleared as a side effect) and restores no error state,
        // so the caller can safely release the GIL and throw a C++ exception
        // instead.
        static std::string DescribeCurrentPythonError( const char* context )
        {
            std::string message( context );
            PyObject *ptype = NULL, *pvalue = NULL, *ptraceback = NULL;
            PyErr_Fetch( &ptype, &pvalue, &ptraceback );
            PyErr_NormalizeException( &ptype, &pvalue, &ptraceback );
            if (pvalue)
            {
                PyObject* pStr = PyObject_Str( pvalue );
                if (pStr)
                {
                    // PyUnicode_AsUTF8() is not part of the limited API; go
                    // through a bytes object instead.
                    PyObject* pBytes = PyUnicode_AsUTF8String( pStr );
                    if (pBytes)
                    {
                        const char* s = PyBytes_AsString( pBytes );
                        if (s)
                        {
                            message += ": ";
                            message += s;
                        }
                        Py_DECREF( pBytes );
                    }
                    Py_DECREF( pStr );
                }
            }
            Py_XDECREF( ptype );
            Py_XDECREF( pvalue );
            Py_XDECREF( ptraceback );
            return message;
        }

        PyObject* m_pyFactory; // strong reference
    };
}
%}

// SWIG-visible declaration of the adapter (kept in sync with the real
// implementation above). Only the constructor/destructor are exposed; the
// AllocateBuffer/FreeBuffer/DestroyBufferFactory overrides are pure C++
// internals and must never be called from Python. They are redeclared here
// (without bodies) purely so that SWIG considers all of IBufferFactory's
// pure virtuals implemented - otherwise it treats CPyBufferFactory as
// abstract and silently skips generating a constructor wrapper.
%ignore Pylon::CPyBufferFactory::AllocateBuffer;
%ignore Pylon::CPyBufferFactory::FreeBuffer;
%ignore Pylon::CPyBufferFactory::DestroyBufferFactory;
%rename(_BufferFactoryAdapter) Pylon::CPyBufferFactory;

// The constructor stores a Python object reference (Py_XINCREF), so it must
// not be called without the GIL being held.
%nothread Pylon::CPyBufferFactory::CPyBufferFactory;

namespace Pylon
{
    class CPyBufferFactory : public Pylon::IBufferFactory
    {
    public:
        explicit CPyBufferFactory( PyObject* pyFactory );
        virtual ~CPyBufferFactory();

        virtual void AllocateBuffer( size_t bufferSize, void** pCreatedBuffer, intptr_t& bufferContext );
        virtual void FreeBuffer( void* pCreatedBuffer, intptr_t bufferContext );
        virtual void DestroyBufferFactory();
    };
}

%pythoncode %{
class BufferFactory:
    """Base class for a custom buffer factory, used with
    InstantCamera.SetBufferFactory().

    Derive from this class and override AllocateBuffer() and FreeBuffer().
    OnReleased() can optionally be overridden to clean up resources once the
    buffer factory is no longer used by pylon.

    A buffer factory can be used by multiple InstantCamera instances from
    multiple threads at the same time, but a given InstantCamera instance
    only ever uses one buffer factory at a time.
    """

    def AllocateBuffer(self, buffer_size):
        """Allocates a buffer of at least buffer_size bytes.

        Must be overridden. Must return a tuple (buffer, context), a
        one-element tuple (buffer,), or just buffer if no context is needed.
        buffer is the integer address of the allocated memory (or None if
        the allocation failed). context is an arbitrary, optional Python
        object that is passed back unchanged to FreeBuffer().

        May return null for buffer if the allocation fails.

        This method can be called from different threads, including an
        internal pylon grab engine thread.
        """
        raise NotImplementedError("BufferFactory.AllocateBuffer() must be overridden.")

    def FreeBuffer(self, buffer, context):
        """Frees a buffer previously allocated by AllocateBuffer().

        Must be overridden. buffer is the integer address returned by
        AllocateBuffer(). context is the context object returned by
        AllocateBuffer() for this buffer, or None if none was provided.

        This method must not raise; exceptions are logged and ignored.
        """
        raise NotImplementedError("BufferFactory.FreeBuffer() must be overridden.")

    def OnReleased(self):
        """Called exactly once when the buffer factory is no longer used by
        pylon, i.e. after InstantCamera.SetBufferFactory() replaces this
        factory with another one (or None), or when the owning
        InstantCamera is destroyed. The default implementation does nothing.

        All grab results with buffers allocated by this factory keep the factory
        alive until they are released or destroyed, so this method is only called
        once all buffers have been freed.

        Since this method can be called via releasing a grab result when the camera object is no longer alive
        there is no reference to the camera object passed to this method.
        If you use one buffer factory for multiple cameras, you may want to keep track of the cameras
        by using a buffer factory for each camera that reroute to the master buffer factory.

        Exceptions raised here are logged and ignored.
        """
        pass
%}
