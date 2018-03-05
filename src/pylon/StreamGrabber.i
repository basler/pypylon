%rename (StreamGrabber) Pylon::IStreamGrabber;
%include <pylon/StreamGrabber.h>;
%pythoncode %{
    IStreamGrabber = StreamGrabber
%}
