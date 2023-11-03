%rename(LineF2D) Pylon::DataProcessing::SLineF2D;
%rename(_PointA) Pylon::DataProcessing::SLineF2D::PointA;
%rename(_PointB) Pylon::DataProcessing::SLineF2D::PointB;
%copyctor Pylon::DataProcessing::SLineF2D;

%include <pylondataprocessing/LineF2D.h>;

%extend Pylon::DataProcessing::SLineF2D {
    // When accessing substructs SWIG wraps these as pointers
    // This can cause crashes when accessing the substructs from returned
    // values, e.g. myvariant.ToLineF2D().PointA.X, when the returned object goes out of scope early.
    // This is a workaround for this problem.
    SAFE_NESTED_STRUCT_ACCESS(PointF2D, PointA)
    SAFE_NESTED_STRUCT_ACCESS(PointF2D, PointB)

    %pythoncode %{
        def __str__(self):
            result = "PointA: ({0}); PointB: ({1})".format(self.PointA,self.PointB)
            return result
    %}
}