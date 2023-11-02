%rename(CircleF) Pylon::DataProcessing::SCircleF;
%rename(_Center) Pylon::DataProcessing::SCircleF::Center;
%copyctor Pylon::DataProcessing::SCircleF;

%include <pylondataprocessing/CircleF.h>;

%extend Pylon::DataProcessing::SCircleF {
    // When accessing substructs SWIG wraps these as pointers
    // This can cause crashes when accessing the substructs from returned
    // values, e.g. myvariant.ToCircleF().Center.X, when the returned object goes out of scope early.
    // This is a workaround for this problem.
    SAFE_NESTED_STRUCT_ACCESS(PointF2D, Center)

    %pythoncode %{
        def __str__(self):
            result = "Center: ({0}); Radius = {1}".format(self.Center, self.Radius)
            return result
    %}
}