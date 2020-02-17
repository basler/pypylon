%rename(ImageDecompressor) Pylon::CImageDecompressor;
%rename(CompressionInfo) Pylon::CompressionInfo_t;

%extend Pylon::CompressionInfo_t {
    %pythoncode %{
        def to_dict(self):
            return {
                "hasCompressedImage": self.hasCompressedImage,
                "compressionStatus": self.compressionStatus,
                "lossy": self.lossy,
                "pixelType": self.pixelType,
                "width": self.width,
                "height": self.height,
                "offsetX": self.offsetX,
                "offsetY": self.offsetY,
                "paddingX": self.paddingX,
                "paddingY": self.paddingY,
                "decompressedImageSize": self.decompressedImageSize,
                "decompressedPayloadSize": self.decompressedPayloadSize,
            }

        def __repr__(self):
            return "<CompressionInfo " + repr(self.to_dict()) + ">"
    %}
}

%{
    /*
     * Helper to convert a Python bytes or bytearray object to a raw readonly buffer
     * After calling, the pointer stored in `buffer` points to the raw data of the incoming PyObject.
     * This is not a transfer of ownership!
     *   Attempts to deallocate this pointer are a path to the dark side.
     *   Deallocation leads to corruption.
     *   Corruption lead to crashes.
     *   Crashes lead to suffering.
     */
    size_t extractByteLikePyObject(PyObject * src, const char *& buffer)
    {
        size_t length = 0;
        if (PyBytes_Check(src)) {
            buffer = PyBytes_AsString(src);
            length = PyBytes_Size(src);
        } else if (PyByteArray_Check(src)) {
            buffer = PyByteArray_AsString(src);
            length = PyByteArray_Size(src);
        } else {
            throw INVALID_ARGUMENT_EXCEPTION("Invalid type of buffer (bytes and bytearray are supported)!.");
        }
        return length;
    }
%}

/*
 * A note on the use of PyByteArray_FromStringAndSize:
 * See for yourself: https://github.com/python/cpython/blob/master/Objects/bytearrayobject.c#L116
 *
 * PyByteArray_FromStringAndSize and many similar functions allocate memory on their own and copy
 * the provided data into the new buffer. The new memory is managed by reference counting and in
 * the domain of the garbage collector.
 * If we create a buffer to pass to PyByteArray_FromStringAndSize(...), we must free our buffer!
 */

%extend Pylon::CImageDecompressor {
    // Since all wrapped functions access Python objects, they must not be
    // called without the GIL being held. Therefore we have to tell SWIG not
    // to release the GIL when calling them (%nothread).
    %nothread SetCompressionDescriptor;
    %nothread GetCompressionInfo;
    %nothread ComputeCompressionDescriptorHash;
    %nothread GetCurrentCompressionDescriptorHash;
    %nothread GetCompressionDescriptorHash;
    %nothread DecompressImage;

    void SetCompressionDescriptor(PyObject * pCompressionDescriptor)
    {
        const char * buffer = NULL;
        size_t length = extractByteLikePyObject(pCompressionDescriptor, buffer);

        $self->SetCompressionDescriptor((void *) buffer, length);
    }

    CompressionInfo_t * GetCompressionInfo(PyObject * pGrabBuffer, EEndianness endianness = Endianness_Auto)
    {
        const char * payloadBuffer = NULL;
        size_t payloadSize = extractByteLikePyObject(pGrabBuffer, payloadBuffer);

        CompressionInfo_t * compressionInfo = new CompressionInfo_t();
        $self->GetCompressionInfo(*compressionInfo, (void *) payloadBuffer, payloadSize, endianness);

        return compressionInfo;
    }

    PyObject * ComputeCompressionDescriptorHash(PyObject * pCompressionDescriptor)
    {
        const char * buffer = NULL;
        size_t length = extractByteLikePyObject(pCompressionDescriptor, buffer);

        size_t hashSize = 0;
        $self->ComputeCompressionDescriptorHash(NULL, &hashSize, buffer, length);

        char * hashBuffer = new char[hashSize];
        $self->ComputeCompressionDescriptorHash(hashBuffer, &hashSize, buffer, length);

        PyObject * result = PyByteArray_FromStringAndSize(hashBuffer, hashSize);
        delete[] hashBuffer; // see note above
        return result;
    }

    PyObject * GetCurrentCompressionDescriptorHash()
    {
        size_t hashSize = 0;
        $self->GetCompressionDescriptorHash(NULL, &hashSize);

        char * hashBuffer = new char[hashSize];
        $self->GetCompressionDescriptorHash(hashBuffer, &hashSize);

        PyObject * result = PyByteArray_FromStringAndSize(hashBuffer, hashSize);
        delete[] hashBuffer; // see note above
        return result;
    }

    PyObject * GetCompressionDescriptorHash(PyObject * pGrabBuffer, EEndianness endianness = Endianness_Auto)
    {
        const char * payloadBuffer = NULL;
        size_t payloadSize = extractByteLikePyObject(pGrabBuffer, payloadBuffer);

        size_t hashSize = 0;
        $self->GetCompressionDescriptorHash(NULL, &hashSize, payloadBuffer, payloadSize, endianness);

        char * hashBuffer = new char[hashSize];
        $self->GetCompressionDescriptorHash(hashBuffer, &hashSize, payloadBuffer, payloadSize, endianness);

        PyObject * result = PyByteArray_FromStringAndSize(hashBuffer, hashSize);
        delete[] hashBuffer; // see note above
        return result;
    }

    Pylon::CPylonImage * DecompressImage(PyObject * pData)
    {
        PyObject * pGrabBuffer = NULL;

        if (PyObject_HasAttrString(pData, "GetBuffer"))
        {
            // if this is something that supports "GetBuffer", we better use it.
            pGrabBuffer = PyObject_CallMethod(pData, "GetBuffer", NULL);
        } else {
            // we have to assume that this is some kind of byte-like thing
            pGrabBuffer = pData;
        }

        const char * payloadBuffer = NULL;
        size_t payloadSize = extractByteLikePyObject(pGrabBuffer, payloadBuffer);

        Pylon::CPylonImage * image = new Pylon::CPylonImage();
        $self->DecompressImage(*image, payloadBuffer, payloadSize);
        return image;
    }
}

// Ignore original overloads for functions with void* in their signature.
%ignore SetCompressionDescriptor;
%ignore GetCompressionInfo;
%ignore ComputeCompressionDescriptorHash;
%ignore GetCompressionDescriptorHash;
%ignore DecompressImage;

// Ignore methods using the node map, these are currently not supported.
%ignore GetCompressionMode;
%ignore GetImageSizeForDecompression;

// Ignode other currently unsupported methods.
%ignore GetCompressionDescriptor;

%include <pylon/ImageDecompressor.h>;
