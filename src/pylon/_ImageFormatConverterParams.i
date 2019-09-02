%rename (ImageFormatConverterParams_Params) Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params;
%ignore CImageFormatConverterParams_ParamsData;
%ignore InconvertibleEdgeHandlingEnumParameter;
%ignore MonoConversionMethodEnumParameter;
%ignore OutputBitAlignmentEnumParameter;
%ignore OutputOrientationEnumParameter;

%extend Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params
{
    GENICAM_EX_PROP(AdditionalLeftShift, GENAPI_NAMESPACE::IInteger);
    GENICAM_EX_PROP(Gamma,               GENAPI_NAMESPACE::IFloat);
    GENICAM_EX_PROP(OutputPaddingX,      GENAPI_NAMESPACE::IInteger);
    GENICAM_ENUM_PROP(InconvertibleEdgeHandling);
    GENICAM_ENUM_PROP(MonoConversionMethod);
    GENICAM_ENUM_PROP(OutputBitAlignment);
    GENICAM_ENUM_PROP(OutputOrientation);
}

%include <pylon/_ImageFormatConverterParams.h>;
