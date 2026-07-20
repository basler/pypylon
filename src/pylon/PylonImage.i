%rename(PylonImage) Pylon::CPylonImage;
// CPylonImageBase uses %nodefaultdtor which would suppress the destructor for
// all subclasses including CPylonImage. Explicitly re-enable the destructor so
// that SWIG registers a 'delete' wrapper and Python can free heap-allocated
// CPylonImage* objects handed over with SWIG_POINTER_OWN (e.g. from
// DecompressImage and the IReusableImage& argout typemap), instead of
// triggering: "swig/python detected a memory leak of type
// 'Pylon::CPylonImage *', no destructor found."
%defaultdtor Pylon::CPylonImage;
%feature("shadow", "0") Pylon::CPylonImage::AttachMemoryView;
%feature("shadow", "0") Pylon::CPylonImage::AttachBytesObject;

%extend Pylon::CPylonImage{

    // Since 'GetBuffer' and 'GetMemoryView'allocate memory, they must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling them (%nothread).
    %nothread GetBuffer;
    %nothread GetMemoryView;
    %nothread GetArrayZeroCopy;

    // Create an overload for 'GetBuffer' for easier type mapping.
    void GetBuffer(void **buf_mem, size_t *length) {
        *buf_mem = $self->GetBuffer();
        *length = $self->GetImageSize();
    }

    PyObject * GetMemoryView()
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

    PyObject* AttachMemoryView(PyObject* object, Pylon::EPixelType pixelType, unsigned int width, unsigned int height, size_t paddingX) {
%#if !defined(Py_LIMITED_API) || Py_LIMITED_API+0 >= 0x030b0000
        Py_buffer buffer;
        if (PyObject_GetBuffer(memoryView, &buffer, PyBUF_SIMPLE) == -1) {
            PyErr_SetString(PyExc_RuntimeError, "Expected a buffer-compatible object");
            Py_RETURN_FALSE;
        }

        // Call the existing C++ AttachUserBuffer method
        $self->AttachUserBuffer(buffer.buf, buffer.len, pixelType, width, height, paddingX);

        // Release the buffer info
        PyBuffer_Release(&buffer);
        Py_RETURN_TRUE;
%#else
        Py_RETURN_FALSE;
%#endif
    }

    PyObject* AttachBytesObject(PyObject* object, Pylon::EPixelType pixelType, unsigned int width, unsigned int height, size_t paddingX)
    {
        // Check input object is bytes object
        if (!PyBytes_Check(object)) {
            PyErr_SetString(PyExc_RuntimeError, "Expected a bytes-compatible object");
            Py_RETURN_FALSE;
        }

        // Get a pointer to the memory and the buffer size
        char* buffer_ptr;
        Py_ssize_t buffer_size;
        if (PyBytes_AsStringAndSize(object, &buffer_ptr, &buffer_size) != 0) {
            PyErr_SetString(PyExc_RuntimeError, "Invalid buffer data");
            Py_RETURN_FALSE;
        }

        // Call the existing C++ AttachUserBuffer method
        $self->AttachUserBuffer(buffer_ptr, static_cast<size_t>(buffer_size), pixelType, width, height, paddingX);

        Py_RETURN_TRUE;
    }

%pythoncode %{

    def AttachMemoryView(self, memoryView, pixelType, width, height, paddingX):
        if memoryView.contiguous == False:
            raise ValueError("Expected a memory view with contiguous ordering")
        result = _pylon.PylonImage_AttachMemoryView(self, memoryView, pixelType, width, height, paddingX)
        if result == False:
          memoryViewBuffer = bytes(memoryView)
          _pylon.PylonImage_AttachBytesObject(self, memoryViewBuffer, pixelType, width, height, paddingX)
          self._memory_view_buffer = memoryViewBuffer # Hold buffer copy to reference to prevent garbage collection
        self._memory_view = memoryView  # Hold the reference to prevent garbage collection

    def AttachBytesObject(self, object, pixelType, width, height, paddingX):
        if not isinstance(object, bytes):
            raise RuntimeError("Expected a bytes-compatible object")
        return _pylon.PylonImage_AttachBytesObject(self, object, pixelType, width, height, paddingX)

    GetImageFormat = needs_numpy(_image_get_image_format)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.Release()

    @needs_numpy
    def AttachArray(self, array, pixeltype):
        width = array.shape[1]
        height = array.shape[0]
        paddingX = 0 # numpy has no concept of padding bytes
        self.AttachMemoryView(array.data, pixeltype, width, height, paddingX)

    @needs_numpy
    def GetArray(self, raw = False):
        # CPylonImage exposes GetImageSize(), not GetPayloadSize().
        return _image_get_array(self, raw, self.GetBuffer, self.GetImageSize)

    @contextmanager
    @needs_numpy
    def GetArrayZeroCopy(self, raw = False):
        '''
        Get a numpy array for the image buffer as zero copy reference to the underlying buffer.
        Note: The context manager variable MUST be released before leaving the scope.
        '''
        yield from _image_array_zero_copy_gen(self, self.GetMemoryView, raw)
%}

}


// Ignore original 'GetBuffer' overloads.
%ignore GetBuffer;
// Ignore original 'AttachUserBuffer' overloads.
%ignore AttachUserBuffer;
%ignore Pylon::CPylonImage::CopyImage(void*, size_t, EPixelType, uint32_t, uint32_t, size_t, EImageOrientation);
%ignore Pylon::CPylonImage::AttachGrabResultBufferWithUserHints(const CGrabResultPtr&, EPixelType, uint32_t, uint32_t, size_t, EImageOrientation);
%ignore Pylon::CPylonImage::AttachUserBuffer(void*, size_t, EPixelType, uint32_t, uint32_t, size_t, EImageOrientation, CPylonImageUserBufferEventHandler*);

%include <pylon/PylonImage.h>;


ADD_PROP_GET(PylonImage, AllocatedBufferSize)
ADD_PROP_GET(PylonImage, Array)
ADD_PROP_GET(PylonImage, Buffer)
ADD_PROP_GET(PylonImage, Height)
ADD_PROP_GET(PylonImage, ImageFormat)
ADD_PROP_GET(PylonImage, ImageSize)
ADD_PROP_GET(PylonImage, Orientation)
ADD_PROP_GET(PylonImage, PaddingX)
ADD_PROP_GET(PylonImage, PixelType)
ADD_PROP_GET(PylonImage, Width)
