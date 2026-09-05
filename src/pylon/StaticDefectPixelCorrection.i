%rename(StaticDefectPixelCorrection) Pylon::CStaticDefectPixelCorrection;

%nodefaultctor Pylon::CStaticDefectPixelCorrection;
%nodefaultdtor Pylon::CStaticDefectPixelCorrection;

// StaticDefectPixel and the pixel-list container used by this module live here
// (not in Container.i) so all StaticDefectPixel bindings stay in one place.
// Nothing included before this file depends on them.
%include <pylon/StaticDefectPixel.h>
namespace std
{
    %template(staticdefectpixel_vector) std::vector<StaticDefectPixel>;
}
namespace Pylon
{
    typedef staticdefectpixel_vector StaticDefectPixelList_t;
}

// The single StaticDefectPixelList_t& parameter is in/out:
//   - SetDefectPixelList / NormalizePixelList read it as input,
//   - GetDefectPixelList ignores the input content and only uses the argument
//     to receive the result.
// Every call returns [success, pixel_list], where pixel_list is a Python list
// of (x, y, type) tuples.
%feature("docstring") Pylon::CStaticDefectPixelCorrection::GetDefectPixelList
    "GetDefectPixelList(nodemap, pixel_list, list_type=ListType_User) -> [success, pixel_list]";
%feature("docstring") Pylon::CStaticDefectPixelCorrection::SetDefectPixelList
    "SetDefectPixelList(nodemap, pixel_list, list_type=ListType_User) -> [success, pixel_list]";
%feature("docstring") Pylon::CStaticDefectPixelCorrection::NormalizePixelList
    "NormalizePixelList(nodemap, pixel_list) -> [success, pixel_list]";

// Accept Python lists for StaticDefectPixelList_t& parameters and return the
// potentially modified list as a Python list of (x, y, type) tuples.
%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER) Pylon::StaticDefectPixelList_t&
{
    $1 = PyList_Check($input) ? 1 : 0;
}

%typemap(in, numinputs=1)
Pylon::StaticDefectPixelList_t&
(Pylon::StaticDefectPixelList_t pixel_list)
{
    if (!PyList_Check($input))
    {
        PyErr_SetString(PyExc_TypeError, "pixelList must be a list of (x, y[, type]) tuples");
        SWIG_fail;
    }

    const Py_ssize_t size = PyList_Size($input);
    for (Py_ssize_t i = 0; i < size; ++i)
    {
        PyObject* item = PyList_GetItem($input, i);  // borrowed ref

        if (!PyTuple_Check(item) && !PyList_Check(item))
        {
            PyErr_SetString(PyExc_TypeError, "each pixel entry must be a tuple/list");
            SWIG_fail;
        }

        const Py_ssize_t n = PySequence_Size(item);
        if (n != 2 && n != 3)
        {
            PyErr_SetString(PyExc_ValueError, "each pixel entry must contain (x, y) or (x, y, type)");
            SWIG_fail;
        }

        PyObject* x_obj = PySequence_GetItem(item, 0);  // new ref
        PyObject* y_obj = PySequence_GetItem(item, 1);  // new ref
        PyObject* type_obj = (n == 3) ? PySequence_GetItem(item, 2) : 0;  // new ref / null

        if (!x_obj || !y_obj || (n == 3 && !type_obj))
        {
            Py_XDECREF(x_obj);
            Py_XDECREF(y_obj);
            Py_XDECREF(type_obj);
            SWIG_fail;
        }

        const long x = PyLong_AsLong(x_obj);
        const long y = PyLong_AsLong(y_obj);
        const long type = (n == 3) ? PyLong_AsLong(type_obj) : static_cast<long>(Pylon::StaticDefectPixelType_Reserved);

        Py_DECREF(x_obj);
        Py_DECREF(y_obj);
        Py_XDECREF(type_obj);

        if (PyErr_Occurred())
        {
            SWIG_fail;
        }

        if (x < 0 || x > UINT16_MAX || y < 0 || y > UINT16_MAX)
        {
            PyErr_Format(PyExc_ValueError, "x and y must be in range [0, %d]", UINT16_MAX);
            SWIG_fail;
        }

        Pylon::StaticDefectPixel pixel;
        pixel.X = static_cast<uint16_t>(x);
        pixel.Y = static_cast<uint16_t>(y);
        pixel.Type = static_cast<Pylon::EStaticDefectPixelType>(type);
        pixel_list.push_back(pixel);
    }

    $1 = &pixel_list;
}

%typemap(argout) Pylon::StaticDefectPixelList_t& {
    PyObject* out_list = PyList_New($1->size());
    for (size_t i = 0; i < $1->size(); ++i)
    {
        const Pylon::StaticDefectPixel& pixel = (*$1)[i];
        PyObject* item = PyTuple_New(3);
        PyTuple_SetItem(item, 0, PyLong_FromUnsignedLong(pixel.X));
        PyTuple_SetItem(item, 1, PyLong_FromUnsignedLong(pixel.Y));
        PyTuple_SetItem(item, 2, PyLong_FromLong(static_cast<long>(pixel.Type)));
        PyList_SetItem(out_list, i, item);
    }
    $result = SWIG_AppendOutput($result, out_list);
}

%include <pylon/StaticDefectPixelCorrection.h>

