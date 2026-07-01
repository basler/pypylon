%ignore CGrabResultPtrImpl;
%ignore operator IImage&;
%rename(GrabResult) Pylon::CGrabResultPtr;

%pythoncode %{
    from contextlib import contextmanager

    try:
        class _PylonGrabResultArray(_pylon_numpy.ndarray):
            pass
    except Exception:
        _PylonGrabResultArray = object

    def _pylon_interface_nbytes(interface):
        try:
            shape = interface.get("shape")
            typestr = interface.get("typestr")
            if not shape or not typestr:
                return None
            item_count = 1
            for dim in shape:
                item_count *= int(dim)
            return item_count * _pylon_numpy.dtype(typestr).itemsize
        except Exception:
            return None

    class _PylonOwnerView:
        """
        Keeps GrabResult alive while exposing a shaped view of the owner object.
        """

        def __init__(self, owner, grab_result, shape=None, dtype=None, strides=None, nbytes=None):
            self._owner = owner
            self._grab_result_ref = GrabResult(grab_result)
            self.shape = shape
            self.dtype = dtype
            self.strides = strides
            self.nbytes = nbytes

        @property
        def __array_interface__(self):
            interface = dict(self._owner.__array_interface__)
            if self.shape is not None:
                interface["shape"] = self.shape
            if self.dtype is not None:
                interface["typestr"] = _pylon_numpy.dtype(self.dtype).str
            if self.strides is not None:
                interface["strides"] = self.strides
            return interface

        @property
        def __cuda_array_interface__(self):
            interface = dict(self._owner.__cuda_array_interface__)
            if self.shape is not None:
                interface["shape"] = self.shape
            if self.dtype is not None:
                interface["typestr"] = _pylon_numpy.dtype(self.dtype).str
            if self.strides is not None:
                interface["strides"] = self.strides
            return interface

        def __array__(self, dtype=None):
            ar = _pylon_numpy.asarray(self._owner, dtype=dtype)
            if self.shape is not None and ar.size >= int(_pylon_numpy.prod(self.shape)):
                ar = ar.reshape((-1,))[:int(_pylon_numpy.prod(self.shape))].reshape(self.shape)
            return ar

        def to(self, *args, **kwargs):
            moved = self._owner.to(*args, **kwargs)
            if self.shape is not None and hasattr(moved, "reshape"):
                try:
                    return moved.reshape(self.shape)
                except Exception:
                    pass
            return moved

        def __getattr__(self, item):
            return getattr(self._owner, item)
%}
%extend Pylon::CGrabResultPtr {
%pythoncode %{
    GetImageFormat = needs_numpy(_image_get_image_format)

    @needs_numpy
    def GetArray(self, raw = False, copy = True):
        """
        Return image data as a NumPy-compatible object.

        By default this preserves the historical pypylon behavior and returns a
        copy that is independent from the grab result.

        Pass copy=False for a zero-copy view that keeps this grab result alive
        until the returned object is released. Prefer GetArrayZeroCopy() when the
        view stays inside a single with-block; use copy=False when the view must
        outlive the current scope (for example cross-thread hand-off).

        Works with PythonBufferFactory for host-memory allocators. For non-NumPy
        owners such as Warp pinned memory, use GetBufferOwnerView() instead.
        """
        if not copy:
            return self.GetArrayView(raw=raw)

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

    def GetBufferOwner(self):
        """
        Return the Python keepalive object associated with this grab buffer if available.
        """
        return _pylon.LookupBufferKeepAlive(self.BufferAddress)

    @needs_numpy
    def _GetArrayViewFormat(self, raw=False):
        shape, dtype_tag, strides, required_bytes, _ = self._GetArrayViewInfo(raw)
        dtype, _ = _dtype_from_tag(dtype_tag)
        return shape, dtype, strides, required_bytes

    @needs_numpy
    def _GetArrayViewInfoPython(self, raw=False):
        shape, dtype_tag, strides, required_bytes, owner = self._GetArrayViewInfo(raw)
        dtype, _ = _dtype_from_tag(dtype_tag)
        return shape, dtype, strides, required_bytes, owner

    @needs_numpy
    def GetBufferOwnerView(self, raw=False):
        """
        Return the allocator-native Python owner as a shaped view, keeping this grab result alive.

        This is intended for custom allocator owners such as Warp/CUDA objects.
        """
        shape, dtype, strides, required_bytes, owner = self._GetArrayViewInfoPython(raw)
        if owner is None:
            return None

        owner_capacity = getattr(owner, "nbytes", None)
        if owner_capacity is None:
            owner_capacity = getattr(owner, "capacity", None)
        if owner_capacity is None and hasattr(owner, "__cuda_array_interface__"):
            owner_capacity = _pylon_interface_nbytes(owner.__cuda_array_interface__)
        if owner_capacity is None and hasattr(owner, "__array_interface__"):
            try:
                owner_capacity = _pylon_interface_nbytes(owner.__array_interface__)
            except Exception:
                owner_capacity = None
        if owner_capacity is not None and owner_capacity < required_bytes:
            raise RuntimeError("buffer owner capacity is smaller than current grab result")

        return _PylonOwnerView(owner, self, shape, dtype, strides, required_bytes)

    @needs_numpy
    def GetArrayView(self, raw=False, prefer_owner=True):
        """
        Return a zero-copy array-like object with automatic grab-result lifetime handling.

        - For NumPy/OpenCV use-cases: returns an ndarray subclass.
        - For CUDA-aware owner objects (__cuda_array_interface__): returns a proxy.
        """

        pt = self.GetPixelType()
        if IsPacked(pt):
            # Packed formats require unpacking, which is a copy.
            return self.GetArray(raw=raw)

        owner = None
        shape, dtype, strides, required_bytes, owner = self._GetArrayViewInfoPython(raw)

        if prefer_owner:
            if owner is not None:
                owner_capacity = getattr(owner, "nbytes", None)
                if owner_capacity is None and hasattr(owner, "__cuda_array_interface__"):
                    owner_capacity = _pylon_interface_nbytes(owner.__cuda_array_interface__)
                if owner_capacity is None and hasattr(owner, "__array_interface__"):
                    try:
                        owner_capacity = _pylon_interface_nbytes(owner.__array_interface__)
                    except Exception:
                        owner_capacity = None
                if owner_capacity is not None and owner_capacity < required_bytes:
                    raise RuntimeError("buffer owner capacity is smaller than current grab result")

                if hasattr(owner, "__cuda_array_interface__"):
                    return _PylonOwnerView(owner, self, shape, dtype, strides, required_bytes)
                if hasattr(owner, "__array_interface__"):
                    try:
                        owner_arr = _pylon_numpy.asarray(owner)
                        if owner_arr.nbytes < required_bytes:
                            raise RuntimeError("buffer owner capacity is smaller than current grab result")

                        # Fast path: owner already has matching image shape/type.
                        if not raw:
                            if owner_arr.dtype == dtype and owner_arr.shape == shape and self.PaddingX == 0:
                                ar = owner_arr.view(_PylonGrabResultArray)
                                ar._grab_result_ref = GrabResult(self)
                                ar._buffer_owner_ref = owner
                                return ar
                    except Exception:
                        # Fall back to creating a view from the grab buffer pointer.
                        pass

        if raw:
            mv = self.GetMemoryView()
            ar = _pylon_numpy.ndarray((self.GetPayloadSize(),), dtype=_pylon_numpy.uint8, buffer=mv).view(_PylonGrabResultArray)
            ar._grab_result_ref = GrabResult(self)
            ar._memory_view_ref = mv
            if owner is not None:
                ar._buffer_owner_ref = owner
            return ar

        mv = self.GetImageMemoryView()

        ar = _pylon_numpy.ndarray(shape, dtype=dtype, buffer=mv, strides=strides).view(_PylonGrabResultArray)
        ar._grab_result_ref = GrabResult(self)
        ar._memory_view_ref = mv
        if owner is not None:
            ar._buffer_owner_ref = owner
        return ar

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
        Yield a NumPy array as a zero-copy view of the image buffer.

        The view is valid only inside the with-block. Holding a reference past
        that scope raises RuntimeError. This is the recommended scoped zero-copy
        API and works with PythonBufferFactory allocators.

        For views that must outlive the current scope, use GetArray(copy=False).
        For custom non-NumPy buffer owners, use GetBufferOwnerView().
        '''
        yield from _image_array_zero_copy_gen(self, self.GetImageMemoryView, raw)

%}

    %nothread _GetImageFormatFast;
    %nothread _GetArrayViewInfo;

    PyObject* _GetImageFormatFast(Pylon::EPixelType pt)
    {
        const Pylon::CGrabResultData* resultData = (*$self).operator->();
        return BuildPylonImageFormatTuple(pt, resultData->GetWidth(), resultData->GetHeight());
    }

    PyObject* _GetArrayViewInfo(bool raw)
    {
        const Pylon::CGrabResultData* resultData = (*$self).operator->();
        return Pylon::BuildGrabResultArrayViewInfo(resultData, raw);
    }
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
ADD_PROP_GET(GrabResult, BufferAddress)
