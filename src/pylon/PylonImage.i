
%rename(PylonImage) Pylon::CPylonImage;
%extend Pylon::CPylonImage{
    // Create an overload for 'GetBuffer' for easier type mapping.
    void GetBuffer(void **buf_mem, size_t *length) {
        *buf_mem = $self->GetBuffer();
        *length = $self->GetImageSize();
    }
}

// Ignore original 'GetBuffer' overloads.
%ignore GetBuffer;

%include <pylon/PylonImage.h>;
