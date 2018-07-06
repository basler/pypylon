%rename (Image) Pylon::IImage;
%ignore GetBuffer() const;
%include <Image.h>;

%pythoncode %{
    IImage = Image
%}
