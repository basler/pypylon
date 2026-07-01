%rename(GrabResultData) Pylon::CGrabResultData;

%ignore CGrabResultDataImpl;
%ignore CGrabResultDataFactory;
%ignore GetFrameNumber;
%ignore GetBuffer() const;
%ignore GetDataComponent;

%include <pylon/PylonVersionNumber.h>;

// Method-qualified typemap: wrap the returned INodeMap& in an NodeMapWrapper
// carrying NodeMapType_ChunkData.
%typemap(out) GENAPI_NAMESPACE::INodeMap& Pylon::CGrabResultData::GetChunkDataNodeMap
%{
    $result = SWIG_NewPointerObj(
        new Pylon::NodeMapWrapper($1, Pylon::NodeMapType_ChunkData),
        $descriptor(Pylon::NodeMapWrapper*),
        SWIG_POINTER_OWN
    );
%}

%include <pylon/GrabResultData.h>;

%extend Pylon::CGrabResultData {

    // Since 'GetBuffer', 'GetImageBuffer', 'GetMemoryView', and 'GetImageMemoryView'
    // allocate memory, they must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling them (%nothread).

    %nothread GetBuffer;
    %nothread GetImageBuffer;
    %nothread GetMemoryView;
    %nothread GetImageMemoryView;

    PyObject * GetBuffer()
    {
        void * buf = $self->GetBuffer();
        size_t length = $self->GetPayloadSize();
        return (buf) ? PyByteArray_FromStringAndSize((const char *) buf, length) : Py_None;
    }

    intptr_t GetBufferAddress()
    {
        return reinterpret_cast<intptr_t>($self->GetBuffer());
    }

    PyObject * GetImageBuffer()
    {
        void * buf = $self->GetBuffer();
        size_t length = $self->GetImageSize();
        return (buf) ? PyByteArray_FromStringAndSize((const char *) buf, length) : Py_None;
    }

    PyObject * GetMemoryView()
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        return PyMemoryView_FromMemory(
            (char*)$self->GetBuffer(),
            $self->GetPayloadSize(),
            PyBUF_WRITE
            );
%#else
        PyErr_SetString(PyExc_RuntimeError, "memory view not available");
        return NULL;
%#endif
    }

    PyObject * GetImageMemoryView()
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        return PyMemoryView_FromMemory(
            (char*)$self->GetBuffer(),
            $self->GetImageSize(),
            PyBUF_WRITE
            );
%#else
        PyErr_SetString(PyExc_RuntimeError, "memory view not available");
        return NULL;
%#endif
    }

    // Access to get data components overloaded methods
    %pythoncode %{
    @deprecated("Use GetDataComponentByIndex instead.")
    def GetDataComponent(self, param):
        return self.GetDataComponentByIndex(param)
    %}

    Pylon::CPylonDataComponent GetDataComponentByIndex(size_t index) {
        return $self->GetDataComponent(index);
    }

#if (PYLON_VERSION_MAJOR > 11) || (PYLON_VERSION_MAJOR == 11 && PYLON_VERSION_MINOR >= 3)

    Pylon::PylonDataComponentList GetDataComponentByType(Pylon::EComponentType componentType) {
        return $self->GetDataComponent(componentType);
    }

#endif
};
