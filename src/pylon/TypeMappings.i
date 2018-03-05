
namespace Pylon
{
    // Pylon's string definition
    typedef GENICAM_NAMESPACE::gcstring String_t;
    // Pylon's string list definition
    typedef GENICAM_NAMESPACE::gcstring_vector StringList_t;
}

//The string class shouldn't get wrapped
%ignore String_t;
%ignore StringList_t;

#include<pylon/TypeMappings.h>

// The exceptions are only imported from genicam into the pylon namespace.
// We therefore want to reuse the wrapped types from genicam.

%types( GENICAM_NAMESPACE::GenericException *,
        GENICAM_NAMESPACE::BadAllocException *,
        GENICAM_NAMESPACE::InvalidArgumentException *,
        GENICAM_NAMESPACE::OutOfRangeException *,
        GENICAM_NAMESPACE::PropertyException *,
        GENICAM_NAMESPACE::RuntimeException *,
        GENICAM_NAMESPACE::LogicalErrorException *,
        GENICAM_NAMESPACE::AccessException *,
        GENICAM_NAMESPACE::TimeoutException *,
        GENICAM_NAMESPACE::DynamicCastException *);

%pythoncode %{
    GenericException = pypylon.genicam.GenericException
    BadAllocException = pypylon.genicam.BadAllocException
    InvalidArgumentException = pypylon.genicam.InvalidArgumentException
    OutOfRangeException = pypylon.genicam.OutOfRangeException
    PropertyException = pypylon.genicam.PropertyException
    RuntimeException = pypylon.genicam.RuntimeException
    LogicalErrorException = pypylon.genicam.LogicalErrorException
    AccessException = pypylon.genicam.AccessException
    TimeoutException = pypylon.genicam.TimeoutException
    DynamicCastException = pypylon.genicam.DynamicCastException
%}