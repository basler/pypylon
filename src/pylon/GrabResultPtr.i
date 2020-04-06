
%ignore CGrabResultPtrImpl;
%ignore operator IImage&;
%rename(GrabResult) Pylon::CGrabResultPtr;

%extend Pylon::CGrabResultPtr {
%pythoncode %{
    @needs_numpy
    def GetImageFormat(self, pt = None):
        if pt is None:
            pt = self.GetPixelType()
        if IsPacked(pt):
            raise ValueError("Packed Formats are not supported with numpy interface")
        if pt in ( PixelType_Mono8, PixelType_BayerGR8, PixelType_BayerRG8, PixelType_BayerGB8, PixelType_BayerBG8 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "B"
            dtype = _pylon_numpy.uint8
        elif pt in ( PixelType_Mono10, PixelType_BayerGR10, PixelType_BayerRG10, PixelType_BayerGB10, PixelType_BayerBG10 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_Mono12, PixelType_BayerGR12, PixelType_BayerRG12, PixelType_BayerGB12, PixelType_BayerBG12 ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_Mono16, ):
            shape = (self.GetHeight(), self.GetWidth())
            format = "H"
            dtype = _pylon_numpy.uint16
        elif pt in ( PixelType_RGB8packed, PixelType_BGR8packed ):
            shape = (self.GetHeight(), self.GetWidth(), 3)
            dtype = _pylon_numpy.uint8
            format = "B"
        elif pt in ( PixelType_YUV422_YUYV_Packed, PixelType_YUV422packed ):
            shape = (self.GetHeight(), self.GetWidth(), 2)
            dtype = _pylon_numpy.uint8
            format = "B"
        else:
            raise ValueError("Pixel format currently not supported")

        return (shape, dtype, format)

    @needs_numpy
    def GetArray(self, raw = False):

        # Raw case => Simple byte wrapping of buffer
        if raw:
            shape, dtype, format = ( self.GetPayloadSize() ), _pylon_numpy.uint8, "B"
            buf = self.GetBuffer()
            return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

        pt = self.GetPixelType()
        if IsPacked(pt):
            buf, new_pt = self._Unpack10or12BitPacked()
            shape, dtype, format = self.GetImageFormat(new_pt)
        else:
            shape, dtype, format = self.GetImageFormat(pt)
            buf = self.GetImageBuffer()

        # Now we will copy the data into an array:
        return _pylon_numpy.ndarray(shape, dtype = dtype, buffer=buf)

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

    from sys import version_info as _gazc_python_version_info
    # need at least Python 3.3 for memory view
    if _gazc_python_version_info >= (3, 3, 0):
        from contextlib import contextmanager
        @contextmanager
        @needs_numpy
        def GetArrayZeroCopy(self, raw = False):
            '''
            Get a numpy array for the image buffer as zero copy reference to the underlying buffer.
            Note: The context manager variable MUST be released before leaving the scope.
            '''

            # For packed formats, we cannot zero-copy, so use GetArray
            pt = self.GetPixelType()
            if IsPacked(pt):
                yield self.GetArray()
                return

            # Here is the procedure:
            #  1. prepare and get image format info
            #  2. get a memory view for our image buffer and
            #     cast it to the right shape and data format
            #  3. build an array upon the view (zero copy!)
            #  4. as context manager, we yield this array
            #  5. delete the array and release our memory
            #  6. check the number of exports of the encapsuled buffer
            #     => if this is > 0 => somebody else still has a reference!

            mv = self.GetImageMemoryView()
            if not raw:
                shape, dtype, format = self.GetImageFormat()
                mv = mv.cast(format, shape)

            ar = _pylon_numpy.asarray(mv)

            yield ar

            del ar
            mv.release() # Only release() so we can check the references

            # There will be one outstanding reference for the 'with target'.
            # That is OK since that will be released right after this function
            # returns.
            if self.GetNumBufferExports(mv) > 1:
                raise RuntimeError("Please remove any references to the array before leaving context manager scope!!!")
    del _gazc_python_version_info
%}
}

%include <pylon/GrabResultPtr.h>;
