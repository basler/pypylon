%rename(PixelData) Pylon::SPixelData;
%rename(PixelDataType_Unknown) Pylon::SPixelData::PixelDataType_Unknown;
%rename(PixelDataType_Mono) Pylon::SPixelData::PixelDataType_Mono;
%rename(PixelDataType_YUV) Pylon::SPixelData::PixelDataType_YUV;
%rename(PixelDataType_RGB) Pylon::SPixelData::PixelDataType_RGB;
%rename(PixelDataType_RGBA) Pylon::SPixelData::PixelDataType_RGBA;
%rename(PixelDataType_BayerR) Pylon::SPixelData::PixelDataType_BayerR;
%rename(PixelDataType_BayerG) Pylon::SPixelData::PixelDataType_BayerG;
%rename(PixelDataType_BayerB) Pylon::SPixelData::PixelDataType_BayerB;
%rename(PixelDataType_BiColorRG) Pylon::SPixelData::PixelDataType_BiColorRG;
%rename(PixelDataType_BiColorBG) Pylon::SPixelData::PixelDataType_BiColorBG;
%copyctor Pylon::SPixelData;
%warnfilter(312) Pylon::SPixelData::Data;

// SPixelData::Data is a C++ union. Expose its active member only through the
// type-checked getters below.
%ignore Pylon::SPixelData::Data;
%ignore Pylon::SPixelData::PixelDataType;
%ignore Pylon::SPixelData::BitDepth;

%{
#include <pylon/PixelData.h>

static const char* PixelDataTypeName(Pylon::SPixelData::EPixelDataType pixel_data_type)
{
    switch (pixel_data_type)
    {
    case Pylon::SPixelData::PixelDataType_Unknown:
        return "PixelDataType_Unknown";
    case Pylon::SPixelData::PixelDataType_Mono:
        return "PixelDataType_Mono";
    case Pylon::SPixelData::PixelDataType_YUV:
        return "PixelDataType_YUV";
    case Pylon::SPixelData::PixelDataType_RGB:
        return "PixelDataType_RGB";
    case Pylon::SPixelData::PixelDataType_RGBA:
        return "PixelDataType_RGBA";
    case Pylon::SPixelData::PixelDataType_BayerR:
        return "PixelDataType_BayerR";
    case Pylon::SPixelData::PixelDataType_BayerG:
        return "PixelDataType_BayerG";
    case Pylon::SPixelData::PixelDataType_BayerB:
        return "PixelDataType_BayerB";
    case Pylon::SPixelData::PixelDataType_BiColorRG:
        return "PixelDataType_BiColorRG";
    case Pylon::SPixelData::PixelDataType_BiColorBG:
        return "PixelDataType_BiColorBG";
    default:
        return "unknown PixelDataType";
    }
}

static std::logic_error PixelDataComponentError(
    const char* component_name,
    const char* expected_types,
    Pylon::SPixelData::EPixelDataType actual_type)
{
    return std::logic_error(
        std::string(component_name) + " is available only for " + expected_types
        + "; actual type is " + PixelDataTypeName(actual_type));
}
%}

%include <pylon/PixelData.h>;

%extend Pylon::SPixelData {
    Pylon::SPixelData::EPixelDataType GetPixelDataType() const {
        return $self->PixelDataType;
    }

    uint32_t GetBitDepth() const {
        return $self->BitDepth;
    }

    int GetMono() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_Mono) {
            throw PixelDataComponentError("Mono", "PixelDataType_Mono", $self->PixelDataType);
        }
        return $self->Data.Mono;
    }

    int GetBayerR() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_BayerR) {
            throw PixelDataComponentError("BayerR", "PixelDataType_BayerR", $self->PixelDataType);
        }
        return $self->Data.BayerR;
    }

    int GetBayerG() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_BayerG) {
            throw PixelDataComponentError("BayerG", "PixelDataType_BayerG", $self->PixelDataType);
        }
        return $self->Data.BayerG;
    }

    int GetBayerB() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_BayerB) {
            throw PixelDataComponentError("BayerB", "PixelDataType_BayerB", $self->PixelDataType);
        }
        return $self->Data.BayerB;
    }

    int GetR() const {
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGB) {
            return $self->Data.RGB.R;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGBA) {
            return $self->Data.RGBA.R;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_BiColorRG) {
            return $self->Data.BiColorRG.R;
        }
        throw PixelDataComponentError("R", "PixelDataType_RGB, PixelDataType_RGBA, or PixelDataType_BiColorRG", $self->PixelDataType);
    }

    int GetG() const {
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGB) {
            return $self->Data.RGB.G;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGBA) {
            return $self->Data.RGBA.G;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_BiColorRG) {
            return $self->Data.BiColorRG.G;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_BiColorBG) {
            return $self->Data.BiColorBG.G;
        }
        throw PixelDataComponentError("G", "PixelDataType_RGB, PixelDataType_RGBA, PixelDataType_BiColorRG, or PixelDataType_BiColorBG", $self->PixelDataType);
    }

    int GetB() const {
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGB) {
            return $self->Data.RGB.B;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_RGBA) {
            return $self->Data.RGBA.B;
        }
        if ($self->PixelDataType == Pylon::SPixelData::PixelDataType_BiColorBG) {
            return $self->Data.BiColorBG.B;
        }
        throw PixelDataComponentError("B", "PixelDataType_RGB, PixelDataType_RGBA, or PixelDataType_BiColorBG", $self->PixelDataType);
    }

    int GetA() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_RGBA) {
            throw PixelDataComponentError("A", "PixelDataType_RGBA", $self->PixelDataType);
        }
        return $self->Data.RGBA.A;
    }

    int GetY() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_YUV) {
            throw PixelDataComponentError("Y", "PixelDataType_YUV", $self->PixelDataType);
        }
        return $self->Data.YUV.Y;
    }

    int GetU() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_YUV) {
            throw PixelDataComponentError("U", "PixelDataType_YUV", $self->PixelDataType);
        }
        return $self->Data.YUV.U;
    }

    int GetV() const {
        if ($self->PixelDataType != Pylon::SPixelData::PixelDataType_YUV) {
            throw PixelDataComponentError("V", "PixelDataType_YUV", $self->PixelDataType);
        }
        return $self->Data.YUV.V;
    }
}

ADD_PROP_GET(PixelData, PixelDataType)
ADD_PROP_GET(PixelData, BitDepth)
ADD_PROP_GET(PixelData, Mono)
ADD_PROP_GET(PixelData, BayerR)
ADD_PROP_GET(PixelData, BayerG)
ADD_PROP_GET(PixelData, BayerB)
ADD_PROP_GET(PixelData, R)
ADD_PROP_GET(PixelData, G)
ADD_PROP_GET(PixelData, B)
ADD_PROP_GET(PixelData, A)
ADD_PROP_GET(PixelData, Y)
ADD_PROP_GET(PixelData, U)
ADD_PROP_GET(PixelData, V)

%pythoncode %{
PixelDataType_Unknown = PixelData.PixelDataType_Unknown
PixelDataType_Mono = PixelData.PixelDataType_Mono
PixelDataType_YUV = PixelData.PixelDataType_YUV
PixelDataType_RGB = PixelData.PixelDataType_RGB
PixelDataType_RGBA = PixelData.PixelDataType_RGBA
PixelDataType_BayerR = PixelData.PixelDataType_BayerR
PixelDataType_BayerG = PixelData.PixelDataType_BayerG
PixelDataType_BayerB = PixelData.PixelDataType_BayerB
PixelDataType_BiColorRG = PixelData.PixelDataType_BiColorRG
PixelDataType_BiColorBG = PixelData.PixelDataType_BiColorBG
%}




