%rename(RectangleF) Pylon::DataProcessing::SRectangleF;
%rename(_Center) Pylon::DataProcessing::SRectangleF::Center;
%copyctor Pylon::DataProcessing::SRectangleF;

%include <pylondataprocessing/RectangleF.h>;

%extend Pylon::DataProcessing::SRectangleF {
    // When accessing substructs SWIG wraps these as pointers
    // This can cause crashes when accessing the substructs from returned
    // values, e.g. myvariant.ToRectangleF().Center.X, when the returned object goes out of scope early.
    // This is a workaround for this problem.
    SAFE_NESTED_STRUCT_ACCESS(PointF2D, Center)

    %pythoncode %{
        def __str__(self):
            result = "Center: ({0}); Width = {1}; Height = {2}; Rotation = {3} rad".format(self.Center, self.Width, self.Height, self.Rotation)
            return result
    %}
}