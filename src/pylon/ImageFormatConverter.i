%rename(ImageFormatConverter) Pylon::CImageFormatConverter;
%ignore CImageFormatConverterImpl;

// CImageFormatConverter has a nested class (IOutputPixelFormatEnum) which
// is not supported by SWIG.
%ignore Pylon::CImageFormatConverter::IOutputPixelFormatEnum;

// Not all overloads of 'Convert' are usable. So we ignore all of them and
// redefine those that we want.
%extend Pylon::CImageFormatConverter {

    // Repeat conversion from IImage.
    void Convert(IReusableImage& dst, const IImage& src)
    {
        $self->Convert(dst, src);
    }
    // Make sure CGrabResultPtr can be converted directly
    void Convert(IReusableImage& dst, const CGrabResultPtr& src)
    {
        $self->Convert(dst, src);
    }

    // Access nested class instance
    void SetOutputPixelFormat(EPixelType pxl_fmt)
    {
        $self->OutputPixelFormat.SetValue(pxl_fmt);
    }
    EPixelType GetOutputPixelFormat()
    {
        return $self->OutputPixelFormat.GetValue();
    }
    PROP_GETSET(OutputPixelFormat)
};

%ignore Pylon::CImageFormatConverter::Convert;
%ignore Pylon::CImageFormatConverter::OutputPixelFormat;

%include <pylon/ImageFormatConverter.h>;
