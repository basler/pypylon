%rename(EllipseF) Pylon::DataProcessing::SEllipseF;
%rename(_Center) Pylon::DataProcessing::SEllipseF::Center;
%copyctor Pylon::DataProcessing::SEllipseF;

%include <pylondataprocessing/EllipseF.h>;

%extend Pylon::DataProcessing::SEllipseF {
    // When accessing substructs SWIG wraps these as pointers
    // This can cause crashes when accessing the substructs from returned
    // values, e.g. myvariant.ToEllipseF().Center.X, when the returned object goes out of scope early.
    // This is a workaround for this problem.
    SAFE_NESTED_STRUCT_ACCESS(PointF2D, Center)

    %pythoncode %{
        def __str__(self):
            result = "Center: ({0}); Radius1 = {1}; Radius2 = {2}; Rotation = {3} rad".format(self.Center, self.Radius1, self.Radius2, self.Rotation)
            return result
    %}
}