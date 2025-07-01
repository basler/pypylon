# Script to append version information to SWIG-generated Python files
# Usage: cmake -DMODULE_FILE=<file> -DVERSION_STRING=<version> -P AppendVersion.cmake

if(NOT MODULE_FILE OR NOT VERSION_STRING)
    message(FATAL_ERROR "MODULE_FILE and VERSION_STRING must be defined")
endif()

# Append version information to the Python file
file(APPEND "${MODULE_FILE}" "\n__version__ = '${VERSION_STRING}'\n") 