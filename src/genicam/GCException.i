
%include "stl.i"
%include "exception.i"

namespace GENICAM_NAMESPACE
{

    // define the base genicam exception
    %{
        static PyObject* pGenericException = NULL;
    %}
    %init %{
        pGenericException = PyErr_NewException(SWIG_name ".GenericException", NULL, NULL);
        if (pGenericException) {
            PyModule_AddObject(m, "GenericException", pGenericException);
        }
    %}

    // embed pythoncode in macro to evaluate arguments
    %define GENERIC_EXCEPTION_PYCODE()
    %pythoncode %{
        GenericException = MODULE_NAME##.GenericException
    %}
    %enddef
    GENERIC_EXCEPTION_PYCODE()

    %define GENI_EXCEPTION(x)
        %{
            static PyObject* p##x = NULL;
        %}
        %init %{
            p##x = PyErr_NewException(SWIG_name ".x", pGenericException, NULL);
            if (p##x) {
                PyModule_AddObject(m, "x", p##x);
            }
        %}

        %pythoncode %{
            x = MODULE_NAME##.x
        %}
    %enddef

    GENI_EXCEPTION(BadAllocException)
    GENI_EXCEPTION(InvalidArgumentException)
    GENI_EXCEPTION(OutOfRangeException)
    GENI_EXCEPTION(PropertyException)
    GENI_EXCEPTION(RuntimeException)
    GENI_EXCEPTION(LogicalErrorException)
    GENI_EXCEPTION(AccessException)
    GENI_EXCEPTION(TimeoutException)
    GENI_EXCEPTION(DynamicCastException)

}

// Typemap for the following function 'TranslateGenicamException' that will
// be exported from this module, so that other modules can use it for exception
// handling. Since exported functions have a Python interface, we have to wrap
// the parameter of type 'const GenericException*' to some Python type.
// We choose 'PyLong'.
%typemap(in, numinputs=1) const GenericException* _gcex_e
{
    if (!PyLong_Check($input))
    {
        PyErr_SetString(PyExc_TypeError, "not a long");
        SWIG_fail;
    }
    $1 = reinterpret_cast<GenericException*>(PyLong_AsLongLong($input));
}

// The wrapped version of 'TranslateGenicamException' that will be called from
// other modules must not return a valid Python object, since it sets a Python
// error (exception). Otherwise Python would raise a
//
// SystemError: <built-in function TranslateGenicamException> returned a result with an error set
//
// We ensure this by supplying the following output typemap. It simply discards
// the return value that SWIG set up (SWIG_Py_Void) and returns NULL.
%typemap(argout) const GenericException* _gcex_e
{
    Py_DECREF($result);
    $result = NULL;
}


#define TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(x)\
if (p##x && dynamic_cast<const x*>(_gcex_e) != NULL) \
{ PyErr_SetString(p##x, _gcex_e->what()); return; }

// Since 'TranslateGenicamException' mutates the Python state, it must not be
// called without the GIL being held. Therefore we have to tell SWIG not to
// release the GIL when calling it.
%nothread TranslateGenicamException;

%inline {
void TranslateGenicamException(const GenericException* _gcex_e)
{
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(BadAllocException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(InvalidArgumentException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(OutOfRangeException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(PropertyException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(RuntimeException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(LogicalErrorException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(AccessException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(TimeoutException);
    TRY_HANDLE_GENICAM_DERIVED_EXCEPTION(DynamicCastException);

    // None of the derived exception types matched -> raise GenericException.
    if (pGenericException)
    {
        PyErr_SetString(pGenericException, _gcex_e->what());
    }
    else
    {
        PyErr_SetString(PyExc_RuntimeError, "missing genicam exception");
    }
}

} // %inline

%exception {
    try {
        $action
    } catch (const GENICAM_NAMESPACE::GenericException& e) {
        TranslateGenicamException(&e);
        SWIG_fail;
    } catch (Swig::DirectorException &e) {
        (void)e;
        // PyErr is still set from director call
        SWIG_fail;
    } catch (const std::exception & e) {
        SWIG_exception(SWIG_RuntimeError, (std::string("C++ std::exception: ") + e.what()).c_str());
    } catch (...) {
        SWIG_exception(SWIG_UnknownError, "C++ anonymous exception");
    }
}
