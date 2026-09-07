%ignore CGrabResultPtrImpl;
%ignore operator IImage&;
%rename(GrabResult) Pylon::CGrabResultPtr;

%{
#include "pylon/BufferFactoryContext.h"
%}

%extend Pylon::CGrabResultPtr {
%pythoncode %{
    GetImageFormat = needs_numpy(_image_get_image_format)

    @needs_numpy
    def GetArray(self, raw = False):
        # Raw case => Simple byte wrapping of buffer
        if raw:
            shape = self.GetPayloadSize()
            buf = self.GetBuffer()
            return _pylon_numpy.ndarray(shape, dtype=_pylon_numpy.uint8, buffer=buf)

        pt = self.GetPixelType()
        if IsPacked(pt):
            unpacked = ImageFormatConverter._Unpack(self)
            shape, dtype, format = _image_get_image_format(unpacked)
            buf = unpacked.GetBuffer()
            strides = None
        else:
            shape, dtype, format = self.GetImageFormat(pt)
            buf = self.GetImageBuffer()

            strides = None
            if self.PaddingX > 0:
                # If padding is present, we need to calculate the strides
                # strides = (bytes per row, bytes per pixel)
                strides = self.Width * _pylon_numpy.dtype(dtype).itemsize + self.PaddingX, _pylon_numpy.dtype(dtype).itemsize

        # Now we will copy the data into an array:
        return _pylon_numpy.ndarray(shape, dtype=dtype, buffer=buf, strides=strides)

    def GetChunkNode( self, nodeName ):
        return self.GetChunkDataNodeMap().GetNode(nodeName)

    def __getattr__(self, attribute):
        # Check "normal" attributes first
        if attribute in self.__dict__ or attribute in ("thisown", "this") or attribute.startswith("__"):
            return object.__getattr__(self, attribute)

        # If chunk data is available, maybe "attribute" is a chunk node?
        if self.IsChunkDataAvailable():
            try:
                return self.GetChunkNode(attribute)
            except pypylon.genicam.LogicalErrorException:
                pass

        # Nothing found -> Raise AttributeError
        raise AttributeError("no attribute '%s' in GrabResult" % attribute)

    def __setattr__(self, attribute, val):
        # Check "normal" attributes first
        if attribute in self.__dict__ or attribute in ("thisown", "this") or attribute.startswith("__"):
            object.__setattr__(self, attribute, val)
            return

        # If chunk data is available, maybe "attribute" is a chunk node?
        if self.IsChunkDataAvailable():
            try:
                node = self.GetChunkNode(attribute)
            except pypylon.genicam.LogicalErrorException:
                pass
            else:
                warnings.warn(f"Setting a feature value by direct assignment is deprecated. Use <nodemap>.{node.Node.GetName()}.Value = {val}", DeprecationWarning, stacklevel=2)
                node.SetValue(val)
                return

        # Nothing found -> Raise AttributeError
        raise AttributeError("no attribute '%s' in GrabResult" % attribute)

    def __dir__(self):
        l = dir(type(self))
        l.extend(self.__dict__.keys())
        try:
            nodes = self.GetChunkDataNodeMap().GetNodes()
            chunks = filter(lambda n: "ChunkData" in (f.GetNode().Name for f in n.GetNode().GetParents()), nodes)
            l.extend(x.GetNode().GetName() for x in chunks)
        except:
            pass
        return sorted(set(l))

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
        yield from _image_array_zero_copy_gen(self, self.GetImageMemoryView, raw)

%}
}

%include <pylon/GrabResultPtr.h>;

ADD_PROP_GET(GrabResult, ErrorDescription)
ADD_PROP_GET(GrabResult, ErrorCode)
ADD_PROP_GET(GrabResult, PayloadType)
ADD_PROP_GET(GrabResult, PixelType)
ADD_PROP_GET(GrabResult, Width)
ADD_PROP_GET(GrabResult, Height)
ADD_PROP_GET(GrabResult, OffsetX)
ADD_PROP_GET(GrabResult, OffsetY)
ADD_PROP_GET(GrabResult, PaddingX)
ADD_PROP_GET(GrabResult, PaddingY)
ADD_PROP_GET(GrabResult, Buffer)
ADD_PROP_GET(GrabResult, Array)
ADD_PROP_GET(GrabResult, PayloadSize)
ADD_PROP_GET(GrabResult, BlockID)
ADD_PROP_GET(GrabResult, TimeStamp)
ADD_PROP_GET(GrabResult, ImageSize)
ADD_PROP_GET(GrabResult, ID)
ADD_PROP_GET(GrabResult, ImageNumber)
ADD_PROP_GET(GrabResult, NumberOfSkippedImages)
ADD_PROP_GET(GrabResult, ChunkDataNodeMap)
ADD_PROP_GET(GrabResult, DataComponentCount)
ADD_PROP_GET(GrabResult, DataContainer)
ADD_PROP_GET(GrabResult, CameraContext)
ADD_PROP_GET(GrabResult, BufferSize)
ADD_PROP_GET(GrabResult, BufferContext)
ADD_PROP_GET(GrabResult, BufferFactory)
