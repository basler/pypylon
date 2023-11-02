%rename(TransformationData) Pylon::DataProcessing::CTransformationData;

%ignore CTransformationData(CTransformationData &&);

%include <pylondataprocessing/TransformationData.h>;

%extend Pylon::DataProcessing::CTransformationData {
    %pythoncode %{
        def __str__(self):
            resultList = []
            for rowIndex in range(self.RowCount):
                if rowIndex != 0:
                    resultList.append("\n")
                for columnIndex in range(self.ColumnCount):
                    if columnIndex != 0:
                        resultList.append(", ")
                    resultList.append(str(self.GetEntry(columnIndex, rowIndex)))
            result = "".join(resultList)
            return result
    %}
}
