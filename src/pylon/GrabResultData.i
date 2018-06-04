%rename(GrabResultData) Pylon::CGrabResultData;

%ignore CGrabResultDataImpl;
%ignore CGrabResultDataFactory;
%ignore GetFrameNumber;
%ignore GetBuffer() const;

%include <pylon/GrabResultData.h>;
%extend Pylon::CGrabResultData {
    PyObject * GetBuffer()
    {
        void * buf = $self->GetBuffer();
        size_t length = $self->GetPayloadSize();
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

    int GetNumBufferExports(PyObject * omv)
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        PyMemoryViewObject * mv = (PyMemoryViewObject *) omv;
        int ret = (int) mv->mbuf->exports;
        Py_DECREF(omv);
        return ret;
%#else
        return 0;
%#endif
    }

    PyObject * _Unpack12BitPacked()
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
            ret_pt = PixelType_Mono12;
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

        default:
            throw INVALID_ARGUMENT_EXCEPTION( "Invalid PixelFormat, unable to unpack.");
        }

        // Now get some info for the current image data
        const void * const buf = $self->GetBuffer();
        const size_t sz = $self->GetImageSize();
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
        result = SWIG_Python_AppendOutput(result, data);
        delete [] dst;

        PyObject * tp = PyInt_FromLong((long) ret_pt);
        result = SWIG_Python_AppendOutput(result, tp);

        return result;
    }

};
