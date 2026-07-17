%rename(Error) Pylon::DataProcessing::CError;

// Move constructor and move assignment are not exposed to Python.
%ignore Pylon::DataProcessing::CError::CError(CError&&);
%ignore Pylon::DataProcessing::CError::operator=;

// Comparison operators are not exposed as Python API.
%ignore Pylon::DataProcessing::CError::operator==;
%ignore Pylon::DataProcessing::CError::operator!=;

%include <pylondataprocessing/Error.h>;

%extend Pylon::DataProcessing::CError {
    %pythoncode %{
        def __str__(self):
            return self.GetDescription()
    %}
}

