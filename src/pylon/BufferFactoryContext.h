////////////////////////////////////////////////////////////////////////////////
//
// Shared support header for src/pylon/BufferFactory.i and
// src/pylon/GrabResultData.i.
//
// Boxes a Python "context" object (plus a strong reference to the owning
// pypylon.pylon.BufferFactory) behind an intptr_t so it can travel through
// the Pylon::IBufferFactory C++ ABI (see Pylon::CPyBufferFactory in
// BufferFactory.i). CGrabResultData::GetBufferContext() (see
// GrabResultData.i) unboxes the same intptr_t back into the original Python
// context object.
//
// This lives in its own header (rather than inline in BufferFactory.i's
// runtime block) so both .i files can use it regardless of their relative
// %include order in pylon.i.
//
////////////////////////////////////////////////////////////////////////////////

#ifndef INCLUDED_PYPYLON_BUFFERFACTORYCONTEXT_H
#define INCLUDED_PYPYLON_BUFFERFACTORYCONTEXT_H

#include <Python.h>
#include <cstdint>

namespace Pylon
{
    // Heap-allocated once per buffer in Pylon::CPyBufferFactory::AllocateBuffer(),
    // destroyed exactly once in Pylon::CPyBufferFactory::FreeBuffer(); never
    // tracked in a global registry. Owned exclusively through the intptr_t
    // value pylon carries as the buffer context.
    class CPyBufferContextBox
    {
    public:
        CPyBufferContextBox( PyObject* context, PyObject* factory )
            : m_magic( kMagic )
            , m_context( context )
            , m_factory( factory )
        {
            Py_XINCREF( m_context );
            Py_XINCREF( m_factory );
        }

        ~CPyBufferContextBox()
        {
            Py_XDECREF( m_context );
            Py_XDECREF( m_factory );
            m_magic = 0xdddddddd; // deleted
        }

        // Borrowed references, valid for the lifetime of the box.
        PyObject* GetContext() const
        {
            return m_context;
        }

        PyObject* GetFactory() const
        {
            return m_factory;
        }

        // Returns true if this looks like a genuine box, as opposed to some
        // unrelated intptr_t value produced. This is just a sanity check for faster debugging.
        // The pylon default buffer factory reports bufferContext=0.
        // Otherwise, only the pypylon buffer factory adapter (CPyBufferFactory) is used,
        // and it always produces a valid box.
        bool IsValid() const
        {
            return m_magic == kMagic;
        }

        // Unboxes a raw CGrabResultData::GetBufferContext() value into a new
        // reference to the user-provided context object. Returns a new
        // reference to Py_None if bufferContext is 0, does not originate
        // from a CPyBufferFactory, or no context object was provided to
        // AllocateBuffer().
        static PyObject* UnboxContext( intptr_t bufferContext )
        {
            if (bufferContext != 0)
            {
                const CPyBufferContextBox* pBox = reinterpret_cast<const CPyBufferContextBox*>( bufferContext );
                if (pBox->IsValid() && pBox->GetContext())
                {
                    PyObject* pContext = pBox->GetContext();
                    Py_INCREF( pContext );
                    return pContext;
                }
            }
            Py_RETURN_NONE;
        }

        // Unboxes a raw CGrabResultData::GetBufferContext() value into a new
        // reference to the user-provided buffer factory object. Returns a new
        // reference to Py_None if bufferContext is 0, does not originate
        // from a CPyBufferFactory.
        static PyObject* UnboxFactory( intptr_t bufferContext )
        {
            if (bufferContext != 0)
            {
                const CPyBufferContextBox* pBox = reinterpret_cast<const CPyBufferContextBox*>( bufferContext );
                if (pBox->IsValid() && pBox->GetFactory())
                {
                    PyObject* pFactory = pBox->GetFactory();
                    Py_INCREF( pFactory );
                    return pFactory;
                }
            }
            Py_RETURN_NONE;
        }

    private:
        CPyBufferContextBox( const CPyBufferContextBox& );
        CPyBufferContextBox& operator=( const CPyBufferContextBox& );

        enum
        {
            kMagic = 0x50594246
        }; // 'PYBF'

        uint32_t m_magic;
        PyObject* m_context;
        PyObject* m_factory;
    };
}

#endif /* INCLUDED_PYPYLON_BUFFERFACTORYCONTEXT_H */


