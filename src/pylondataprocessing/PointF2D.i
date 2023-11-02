%rename(PointF2D) Pylon::DataProcessing::SPointF2D;
%copyctor Pylon::DataProcessing::SPointF2D;

%include <pylondataprocessing/PointF2D.h>;

%extend Pylon::DataProcessing::SPointF2D {
    %pythoncode %{
        def __str__(self):
            result = "X = {0}; Y = {1}".format(self.X,self.Y)
            return result
    %}
}
