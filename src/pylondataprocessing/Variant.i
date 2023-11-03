%rename(Variant) Pylon::DataProcessing::CVariant;

%ignore GetArrayDataValues;
%ignore SetArrayDataValues;
%ignore CVariant(const char* value);
%ignore CVariant(uint64_t);
%ignore CVariant(EVariantDataType);
%ignore CVariant(EVariantDataType, size_t);
%ignore CVariant(CVariant &&);
%ignore GetTypeName;
%ignore CreateFromTypeName;
%ignore CanCreateFromTypeName;
%ignore CVariant(const StringList_t& valueList);

%include <pylondataprocessing/Variant.h>;

%extend Pylon::DataProcessing::CVariant {

    static Pylon::DataProcessing::CVariant MakeVariant(Pylon::DataProcessing::EVariantDataType dataType)
    {
        return Pylon::DataProcessing::CVariant(dataType);
    }

    static Pylon::DataProcessing::CVariant MakeVariant(Pylon::DataProcessing::EVariantDataType dataType, Pylon::DataProcessing::EVariantContainerType containerType)
    {
        if (containerType == Pylon::DataProcessing::VariantContainerType_Array)
        {
            return Pylon::DataProcessing::CVariant(dataType, static_cast<size_t>(0));
        }
        else if (containerType == Pylon::DataProcessing::VariantContainerType_None)
        {
            return Pylon::DataProcessing::CVariant(dataType);
        }
        else
        {
            throw INVALID_ARGUMENT_EXCEPTION("Unsupported variant container type.");
        }
    }

    static Pylon::DataProcessing::CVariant MakeVariant(Pylon::DataProcessing::EVariantDataType dataType, Pylon::DataProcessing::EVariantContainerType containerType, size_t arraySize)
    {
        if (containerType == Pylon::DataProcessing::VariantContainerType_Array)
        {
            return Pylon::DataProcessing::CVariant(dataType, arraySize);
        }
        else
        {
            throw INVALID_ARGUMENT_EXCEPTION("Size argument not valid for variant container type.");
        }
    }

    %pythoncode %{
        def __str__(self):
            resultList = ["Type = "]
            dt = self.GetDataType()
            hasString = False
            if (dt == VariantDataType_None):
                resultList.append("None")
            elif (dt == VariantDataType_Int64):
                resultList.append("Int64")
                hasString = True
            elif (dt == VariantDataType_UInt64):
                resultList.append("UInt64")
                hasString = True
            elif (dt == VariantDataType_Boolean):
                resultList.append("Boolean")
                hasString = True
            elif (dt == VariantDataType_String):
                resultList.append("String")
                hasString = True
            elif (dt == VariantDataType_Float):
                resultList.append("Float")
                hasString = True
            elif (dt == VariantDataType_PylonImage):
                resultList.append("PylonImage")
            elif (dt == VariantDataType_Region):
                resultList.append("Region")
            elif (dt == VariantDataType_TransformationData):
                resultList.append("TransformationData")
                hasString = True
            elif (dt == VariantDataType_PointF2D):
                resultList.append("PointF2D")
                hasString = True
            elif (dt == VariantDataType_LineF2D):
                resultList.append("LineF2D")
                hasString = True
            elif (dt == VariantDataType_RectangleF):
                resultList.append("RectangleF")
                hasString = True
            elif (dt == VariantDataType_CircleF):
                resultList.append("CircleF")
                hasString = True
            elif (dt == VariantDataType_EllipseF):
                resultList.append("EllipseF")
                hasString = True
            else:
                resultList.append("?")

            if self.HasError():
                resultList.append("; Error = ")
                resultList.append(self.GetErrorDescription())
            elif hasString:
                resultList.append("; ")
                resultList.append(self.ToString())

            result = "".join(resultList)
            return result
    %}
}