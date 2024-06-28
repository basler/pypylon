%rename(Region) Pylon::DataProcessing::CRegion;

%ignore AttachUserBuffer;
%ignore CopyRegion(const void*,size_t,Pylon::DataProcessing::ERegionType,uint32_t,uint32_t,int32_t,int32_t,uint32_t,uint32_t);
%ignore GetBuffer;
%ignore GetBufferConst;
%rename(GetBuffer) GetBuffer2;

%include <pylondataprocessing/Region.h>;

%extend Pylon::DataProcessing::CRegion {

    // Since 'GetBuffer', 'GetMemoryView'
    // allocate memory, they must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling them (%nothread).

    %nothread GetBuffer;
    %nothread GetBuffer2;
    %nothread GetMemoryView;
    %nothread ToArray;

    PyObject * GetBuffer2()
    {
        const void * buf = $self->GetBufferConst();
        size_t length = $self->GetDataSize();
        return (buf) ? PyByteArray_FromStringAndSize((const char *) buf, length) : Py_None;
    }

    PyObject * GetMemoryView()
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        if ($self->IsReadOnly())
        {
            return PyMemoryView_FromMemory(
                (char*)const_cast<void*>($self->GetBufferConst()),
                $self->GetDataSize(),
                PyBUF_READ
                );
        }
        else
        {
            return PyMemoryView_FromMemory(
                (char*)$self->GetBuffer(),
                $self->GetDataSize(),
                PyBUF_WRITE
                );
        }
%#else
        PyErr_SetString(PyExc_RuntimeError, "memory view not available");
        return NULL;
%#endif
    }
    
    PyObject * ToArray()
    {
        Pylon::DataProcessing::ERegionType regionType = $self->GetRegionType();
        if (regionType == Pylon::DataProcessing::RegionType_RLE32)
        {
            const Pylon::DataProcessing::SRegionEntryRLE32* p = reinterpret_cast<const Pylon::DataProcessing::SRegionEntryRLE32*>($self->GetBufferConst());
            size_t elementCount = ($self->GetDataSize() / sizeof(Pylon::DataProcessing::SRegionEntryRLE32));
            PyObject *listObject = PyList_New(elementCount);
            for (size_t i = 0; i < elementCount; ++i, ++p)
            {
                PyList_SetItem(listObject, i, SWIG_NewPointerObj(SWIG_as_voidptr(new Pylon::DataProcessing::SRegionEntryRLE32(*p)), SWIGTYPE_p_Pylon__DataProcessing__SRegionEntryRLE32, SWIG_POINTER_OWN));
            }
            return listObject;
        }
        else
        {
            PyErr_SetString(PyExc_RuntimeError, "Region cannot be converted to an array.");
            return NULL;
        }
    }
}