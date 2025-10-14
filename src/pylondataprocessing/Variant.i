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

        # A method that takes a variant as input and returns the contained data type according to the value returned by GetDataType().
        def ToData(self):
            """
            Returns the value contained in a pylondataprocessing.Variant by calling the appropriate To* method based on its data type.
            If the variant is an array, returns a list of values for each array item.
            Uses a switch-case like structure for data type handling, with a loop for every data type. Calls GetDataType only once.
            """
            dt = self.GetDataType()
            if self.GetContainerType() == VariantContainerType_Array:
                if (dt == VariantDataType_Int64):
                    return [self.GetArrayValue(i).ToInt64() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_UInt64):
                    return [self.GetArrayValue(i).ToUInt64() for i in range(self.GetNumArrayValues())]
                elif (dt ==  VariantDataType_Boolean):
                    return [self.GetArrayValue(i).ToBool() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_String):
                    return [self.GetArrayValue(i).ToString() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_Float):
                    return [self.GetArrayValue(i).ToDouble() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_PylonImage):
                    return [self.GetArrayValue(i).ToImage() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_Region):
                    return [self.GetArrayValue(i).ToRegion() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_TransformationData):
                    return [self.GetArrayValue(i).ToTransformationData() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_PointF2D):
                    return [self.GetArrayValue(i).ToPointF2D() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_LineF2D):
                    return [self.GetArrayValue(i).ToLineF2D() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_RectangleF):
                    return [self.GetArrayValue(i).ToRectangleF() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_CircleF):
                    return [self.GetArrayValue(i).ToCircleF() for i in range(self.GetNumArrayValues())]
                elif (dt == VariantDataType_EllipseF):
                    return [self.GetArrayValue(i).ToEllipseF() for i in range(self.GetNumArrayValues())]
                else:
                    return [None for _ in range(self.GetNumArrayValues())]
            else:
                if (dt == VariantDataType_Int64):
                    return self.ToInt64()
                elif (dt == VariantDataType_UInt64):
                    return self.ToUInt64()
                elif (dt == VariantDataType_Boolean):
                    return self.ToBool()
                elif (dt == VariantDataType_String):
                    return self.ToString()
                elif (dt == VariantDataType_Float):
                    return self.ToDouble()
                elif (dt == VariantDataType_PylonImage):
                    return self.ToImage()
                elif (dt == VariantDataType_Region):
                    return self.ToRegion()
                elif (dt == VariantDataType_TransformationData):
                    return self.ToTransformationData()
                elif (dt == VariantDataType_PointF2D):
                    return self.ToPointF2D()
                elif (dt == VariantDataType_LineF2D):
                    return self.ToLineF2D()
                elif (dt == VariantDataType_RectangleF):
                    return self.ToRectangleF()
                elif (dt == VariantDataType_CircleF):
                    return self.ToCircleF()
                elif (dt == VariantDataType_EllipseF):
                    return self.ToEllipseF()
                else:
                    return None
    %}
}