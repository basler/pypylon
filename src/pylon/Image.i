%rename (Image) Pylon::IImage;
%ignore GetBuffer() const;
%include <pylon/Image.h>;

%pythoncode %{
    IImage = Image
%}
