%rename (ImageFormatConverterParams_Params) Basler_ImageFormatConverterParams::CImageFormatConverterParams_Params;
#define GenApi GENAPI_NAMESPACE
%include <pylon/_ImageFormatConverterParams.h>;
#undef GenApi

%pythoncode %{
    CImageFormatConverterParams_Params = ImageFormatConverterParams_Params
%}

