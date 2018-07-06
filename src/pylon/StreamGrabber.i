%rename (StreamGrabber) Pylon::IStreamGrabber;
%include <StreamGrabber.h>;
%pythoncode %{
    IStreamGrabber = StreamGrabber
%}
