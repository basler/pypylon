%rename(PylonDataComponent) Pylon::CPylonDataComponent;

%ignore CPylonDataComponentImpl;
%ignore operator IImage&;
%ignore GetData() const;

%pythoncode %{
    from contextlib import contextmanager
    import sys
%} 

%include <pylon/PylonDataComponent.h>;
%extend Pylon::CPylonDataComponent {
%pythoncode %{
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

    @needs_numpy
    def GetArray(self, raw = False):

        # Raw case => Simple byte wrapping of buffer
        if raw:
            shape, dtype, format = ( self.GetDataSize() ), _pylon_numpy.uint8, "B"
            buf = self.GetData()
            return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

        pt = self.GetPixelType()
        if IsPacked(pt):
            buf, new_pt = self._Unpack10or12BitPacked()
            shape, dtype, format = self.GetImageFormat(new_pt)
        else:
            shape, dtype, format = self.GetImageFormat(pt)
            buf = self.GetData()

        # Now we will copy the data into an array:
        return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.Release()

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

    // To allow the instant camera to reuse the CGrabResultData
    // and prevent buffer underruns, you must release the PylonDataContainer and all its PylonDataComponent objects.
    void Release()
    {
        *($self) = Pylon::CPylonDataComponent();
    }
    
    // Since 'GetData', 'GetImageBuffer', 'GetMemoryView', 'GetImageMemoryView'
    // and '_Unpack10or12BitPacked' allocate memory, they must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling them (%nothread).

    %nothread GetData;
    %nothread GetMemoryView;
    %nothread _Unpack10or12BitPacked;

    PyObject * GetData()
    {
        void * buf = const_cast<void*>($self->GetData());
        size_t length = $self->GetDataSize();
        return (buf) ? PyByteArray_FromStringAndSize((const char *) buf, length) : Py_None;
    }

    PyObject * GetMemoryView()
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        return PyMemoryView_FromMemory(
            (char*)$self->GetData(),
            $self->GetDataSize(),
            PyBUF_WRITE
            );
%#else
        PyErr_SetString(PyExc_RuntimeError, "memory view not available");
        return NULL;
%#endif
    }

    PyObject * _Unpack10or12BitPacked()
    {
        // Current pixel type of our data
        EPixelType cur_pt = $self->GetPixelType();

        // Parameter for conversion
        EPixelType conv_src_pt = PixelType_Undefined;
        EPixelType conv_dst_pt = PixelType_Undefined;

        // Type of resulting image data
        EPixelType ret_pt = PixelType_Undefined;

        /*
         * Now set conversion parameter depending on the current type
         * Hack: Image format converter does not allow Bayer* as output format
         *       so we treat Bayer* as Mono* as we only are interested in the
         *       unpack operation.
         */
        switch(cur_pt)
        {
        case PixelType_Mono12packed:
            conv_src_pt = PixelType_Mono12packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_Mono12;
            break;

        case PixelType_Mono12p:
            conv_src_pt = PixelType_Mono12p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_Mono12;
            break;

        case PixelType_BayerBG12Packed:
            conv_src_pt = PixelType_Mono12packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerBG12;
            break;

        case PixelType_BayerBG12p:
            conv_src_pt = PixelType_Mono12p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerBG12;
            break;

        case PixelType_BayerGB12Packed:
            conv_src_pt = PixelType_Mono12packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGB12;
            break;

        case PixelType_BayerGB12p:
            conv_src_pt = PixelType_Mono12p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGB12;
            break;

        case PixelType_BayerRG12Packed:
            conv_src_pt = PixelType_Mono12packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerRG12;
            break;

        case PixelType_BayerRG12p:
            conv_src_pt = PixelType_Mono12p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerRG12;
            break;

        case PixelType_BayerGR12Packed:
            conv_src_pt = PixelType_Mono12packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGR12;
            break;

        case PixelType_BayerGR12p:
            conv_src_pt = PixelType_Mono12p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGR12;
            break;

        case PixelType_Mono10packed:
            conv_src_pt = PixelType_Mono10packed;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_Mono10;
            break;

        case PixelType_Mono10p:
            conv_src_pt = PixelType_Mono10p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_Mono10;
            break;

        case PixelType_BayerBG10p:
            conv_src_pt = PixelType_Mono10p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerBG10;
            break;

        case PixelType_BayerGB10p:
            conv_src_pt = PixelType_Mono10p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGB10;
            break;

        case PixelType_BayerRG10p:
            conv_src_pt = PixelType_Mono10p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerRG10;
            break;

        case PixelType_BayerGR10p:
            conv_src_pt = PixelType_Mono10p;
            conv_dst_pt = PixelType_Mono16;
            ret_pt = PixelType_BayerGR10;
            break;

        default:
            throw INVALID_ARGUMENT_EXCEPTION( "Invalid PixelFormat, unable to unpack.");
        }

        // Now get some info for the current image data
        const void * const buf = $self->GetData();
        const size_t sz = $self->GetDataSize();
        const uint32_t width = $self->GetWidth();
        const uint32_t height = $self->GetHeight();
        const size_t padding_x = $self->GetPaddingX();

        // Use the pylon converter to do the real work
        CImageFormatConverter converter;
        converter.OutputPixelFormat = conv_dst_pt;

        // Create a new buffer, the allocated memory is returned
        size_t new_size = converter.GetBufferSizeForConversion(conv_src_pt, width, height);
        uint8_t *dst = new uint8_t[new_size];

        try
        {
            converter.Convert(dst, new_size, buf, sz, conv_src_pt,  width, height, padding_x, ImageOrientation_TopDown);
        }
        catch(...)
        {
            // Unable to convert, free temp buffer and return empty
            delete[] dst;
            throw LOGICAL_ERROR_EXCEPTION( "Failed to unpack!");
        }

        // Build python return object
        PyObject * result = 0;

        PyObject * data = (dst) ? PyByteArray_FromStringAndSize((const char *) dst, new_size) : Py_None;
        // workaround for using AppendOutput outside of template for swig >= 4.3
        const int IS_VOID = 1;
        result = SWIG_Python_AppendOutput(result, data, IS_VOID);
        delete [] dst;

        PyObject * tp = PyInt_FromLong((long) ret_pt);
        result = SWIG_Python_AppendOutput(result, tp, IS_VOID);

        return result;
    }

};
