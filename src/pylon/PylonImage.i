%rename(PylonImage) Pylon::CPylonImage;
%feature("shadow", "0") Pylon::CPylonImage::AttachMemoryView;

%pythoncode %{
    from contextlib import contextmanager
    import sys
%} 

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

    @needs_numpy
    def GetImageFormat(self, pt = None):
        if pt is None:
            pt = self.GetPixelType()
        if IsPacked(pt):
            raise ValueError("Packed Formats are not supported with numpy interface")
        if pt in ( PixelType_Mono8, PixelType_BayerGR8, PixelType_BayerRG8, PixelType_BayerGB8, PixelType_BayerBG8, PixelType_Confidence8, PixelType_Coord3D_C8 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "B"
            dtype = _pylon_numpy.uint8
        elif pt in ( PixelType_Mono10, PixelType_BayerGR10, PixelType_BayerRG10, PixelType_BayerGB10, PixelType_BayerBG10 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_Mono12, PixelType_BayerGR12, PixelType_BayerRG12, PixelType_BayerGB12, PixelType_BayerBG12 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_Mono16, PixelType_BayerGR16, PixelType_BayerRG16, PixelType_BayerGB16, PixelType_BayerBG16, PixelType_Confidence16, PixelType_Coord3D_C16 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_RGB8packed, PixelType_BGR8packed ):
            shape = (self.GetHeight(), self.GetWidth(), 3)
            dtype = _pylon_numpy.uint8
            format = "B"
        elif pt in ( PixelType_RGB12packed, PixelType_BGR12packed, PixelType_RGB10packed, PixelType_BGR10packed ):
            shape = (self.GetHeight(), self.GetWidth(), 3)
            format = "H"
            dtype = _pylon_numpy.uint16            
        elif pt in ( PixelType_YUV422_YUYV_Packed, PixelType_YUV422packed ):
            shape = (self.GetHeight(), self.GetWidth(), 2)
            dtype = _pylon_numpy.uint8
            format = "B"
        elif pt in ( PixelType_Coord3D_ABC32f, ):
            shape = (self.GetHeight(), self.GetWidth(), 3)
            dtype = _pylon_numpy.float32
            format = "f"
        elif pt in ( PixelType_Data32f, ):
            shape = (self.GetHeight(), self.GetWidth(), 1)
            dtype = _pylon_numpy.float32
            format = "f"
        elif pt in ( PixelType_BiColorRGBG8, PixelType_BiColorBGRG8 ):
            shape = (self.GetHeight(), self.GetWidth() * 2)
            format = "B"
            dtype = _pylon_numpy.uint8
        elif pt in ( PixelType_BiColorRGBG10, PixelType_BiColorBGRG10, PixelType_BiColorRGBG12, PixelType_BiColorBGRG12 ):
            shape = (self.GetHeight(), self.GetWidth() * 2)
            format = "H"
            dtype = _pylon_numpy.uint16
        else:
            raise ValueError("Pixel format currently not supported")

        return (shape, dtype, format)

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

        # Raw case => Simple byte wrapping of buffer
        if raw:
            shape, dtype, format = ( self.GetPayloadSize() ), _pylon_numpy.uint8, "B"
            buf = self.GetBuffer()
            return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

        pt = self.GetPixelType()
        if IsPacked(pt):
            buf, new_pt = self._Unpack10or12BitPacked()
            shape, dtype, format = self.GetImageFormat(new_pt)
        else:
            shape, dtype, format = self.GetImageFormat(pt)
            buf = self.GetBuffer()

        # Now we will copy the data into an array:
        return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

    @contextmanager
    @needs_numpy
    def GetArrayZeroCopy(self, raw = False):
        '''
        Get a numpy array for the image buffer as zero copy reference to the underlying buffer.
        Note: The context manager variable MUST be released before leaving the scope.
        '''

        # For packed formats, we cannot zero-copy, so use GetArray
        pt = self.GetPixelType()
        if IsPacked(pt):
            yield self.GetArray()
            return

        mv = self.GetMemoryView()
        if not raw:
            shape, dtype, format = self.GetImageFormat()
            mv = mv.cast(format, shape)

        ar = _pylon_numpy.asarray(mv)

        # trace external references to array
        initial_refcount = sys.getrefcount(ar)

        # yield the array to the context code
        yield ar

        # detect if more refs than the one from the yield are held
        if sys.getrefcount(ar) > initial_refcount + 1:
            raise RuntimeError("Please remove any references to the array before leaving context manager scope!!!")

        # release the memory view
        mv.release()
%}

}


// Ignore original 'GetBuffer' overloads.
%ignore GetBuffer;
// Ignore original 'AttachUserBuffer' overloads.
%ignore AttachUserBuffer;

%include <pylon/PylonImage.h>;
