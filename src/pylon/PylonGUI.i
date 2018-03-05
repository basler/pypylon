%rename(PylonImageWindow) Pylon::CPylonImageWindow;
%typemap(out) HWND {
    $result = PyLong_FromVoidPtr($1);
}

%extend Pylon::CPylonImageWindow {
    %pythoncode %{
    #
    # let python code easily detect whether an image window is visible
    #

    import ctypes as _tmp_ctypes
    __IsWindowVisible = _tmp_ctypes.WinDLL("user32").IsWindowVisible
    __IsWindowVisible.argtypes = [_tmp_ctypes.c_void_p]
    __IsWindowVisible.restype = _tmp_ctypes.c_bool
    del _tmp_ctypes

    def IsVisible(self):
        """

        Checks if this PylonImageWindow is visible

        Returns
        -------
        True if visible.

        """
        return self.__IsWindowVisible(self.GetWindowHandle())
    %}
}

#define IImage CGrabResultPtr
%include <pylon/PylonGUI.h>;
#undef IImage
