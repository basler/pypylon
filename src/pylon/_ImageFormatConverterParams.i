%rename (ImageFormatConverterParams_Params) Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params;
#define GenApi GENAPI_NAMESPACE
%ignore Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params::CImageFormatConverterParams_Params(void);
%ignore Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params::~CImageFormatConverterParams_Params(void);
%ignore Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params::_Initialize(GenApi::INodeMap*);
%ignore Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params::_GetVendorName(void);
%ignore Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params::_GetModelName(void);

%extend Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params {
    GENICAM_PROP(AdditionalLeftShift);
    GENICAM_PROP(Gamma);
    GENICAM_ENUM_PROP(InconvertibleEdgeHandling);
    GENICAM_ENUM_PROP(MonoConversionMethod);
    GENICAM_ENUM_PROP(OutputBitAlignment);
    GENICAM_ENUM_PROP(OutputOrientation);
    GENICAM_PROP(OutputPaddingX);
}
%include <pylon/_ImageFormatConverterParams.h>;

%pythoncode %{
    CImageFormatConverterParams_Params = ImageFormatConverterParams_Params
%}

#undef GenApi