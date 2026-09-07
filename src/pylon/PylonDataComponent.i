%rename(PylonDataComponent) Pylon::CPylonDataComponent;

%ignore CPylonDataComponentImpl;
%ignore operator IImage&;
// CPylonDataComponent declares two overloads of GetData in the pylon C++ SDK:
//     const void* GetData() const;
//     void*       GetData();
// Both must be hidden so that the custom %extend implementation below (which
// returns a Python bytearray) is used instead of the raw void* pointer.
// We cannot use '%ignore GetData();' to hide the non-const overload, because
// that directive has the same signature as the %extend'ed method and would
// suppress it as well, leaving PylonDataComponent without any GetData method.
// Therefore we ignore every base-class GetData overload by name and expose the
// custom implementation (named 'GetDataAsBytes') under the name 'GetData' via
// %rename.
%ignore Pylon::CPylonDataComponent::GetData;
%rename(GetData) Pylon::CPylonDataComponent::GetDataAsBytes;


%include <pylon/PylonDataComponent.h>;
%extend Pylon::CPylonDataComponent {
%pythoncode %{
    GetImageFormat = needs_numpy(_image_get_image_format)

    @needs_numpy
    def GetArray(self, raw = False):
        return _image_get_array(self, raw, self.GetData, self.GetDataSize)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.Release()

    @contextmanager
    @needs_numpy
    def GetArrayZeroCopy(self, raw = False):
        '''
        Get a numpy array for the image buffer as zero copy reference to the underlying buffer.
        Note: The context manager variable MUST be released before leaving the scope.
        '''
        yield from _image_array_zero_copy_gen(self, self.GetMemoryView, raw)
%}

    // To allow the instant camera to reuse the CGrabResultData
    // and prevent buffer underruns, you must release the PylonDataContainer and all its PylonDataComponent objects.
    void Release()
    {
        *($self) = Pylon::CPylonDataComponent();
    }
    
    // Since 'GetData', 'GetImageBuffer', 'GetMemoryView', and 'GetImageMemoryView'
    // allocate memory, they must not be called without
    // the GIL being held. Therefore we have to tell SWIG not to release the GIL
    // when calling them (%nothread).

    %nothread GetDataAsBytes;
    %nothread GetMemoryView;

    PyObject * GetDataAsBytes()
    {
        void * buf = const_cast<void*>($self->GetData());
        size_t length = $self->GetDataSize();
        return (buf) ? PyByteArray_FromStringAndSize((const char *) buf, length) : Py_None;
    }

    PyObject * GetMemoryView()
    {
// need at least Python 3.3 for memory view
%#if PY_VERSION_HEX >= 0x03030000
        return PyMemoryView_FromMemory(
            (char*)$self->GetData(),
            $self->GetDataSize(),
            PyBUF_WRITE
            );
%#else
        PyErr_SetString(PyExc_RuntimeError, "memory view not available");
        return NULL;
%#endif
    }
};

ADD_PROP_GET(PylonDataComponent, ComponentType)
ADD_PROP_GET(PylonDataComponent, PixelType)
ADD_PROP_GET(PylonDataComponent, Width)
ADD_PROP_GET(PylonDataComponent, Height)
ADD_PROP_GET(PylonDataComponent, OffsetX)
ADD_PROP_GET(PylonDataComponent, OffsetY)
ADD_PROP_GET(PylonDataComponent, PaddingX)
ADD_PROP_GET(PylonDataComponent, PaddingY)
ADD_PROP_GET(PylonDataComponent, Data)
ADD_PROP_GET(PylonDataComponent, DataSize)
ADD_PROP_GET(PylonDataComponent, TimeStamp)
ADD_PROP_GET(PylonDataComponent, Array)
ADD_PROP_GET(PylonDataComponent, ImageFormat)
ADD_PROP_GET(PylonDataComponent, SourceId)
ADD_PROP_GET(PylonDataComponent, ComponentIndex)
