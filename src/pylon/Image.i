// We need to include ImagePersistence.h for the definition of EImageFileFormat.
// But supporting Pylon::CImagePersistence would be too convoluted. So we ignore
// that, since PylonImageBase already supports saving and loading images.
%ignore Pylon::CImagePersistence;
%rename (ImagePersistenceOptions) Pylon::CImagePersistenceOptions;
%rename (Image) Pylon::IImage;
%ignore GetBuffer() const;

%include <pylon/ImagePersistence.h>;
%include <pylon/Image.h>;

%pythoncode %{
    IImage = Image
%}
