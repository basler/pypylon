cmake_minimum_required(VERSION 3.20)

# Define project - setuptools_scm will provide version automatically
project(pypylon 
    DESCRIPTION "Python wrapper for Basler pylon Camera Software Suite"
    LANGUAGES CXX
)

# Get version from setuptools_scm (via SKBUILD_PROJECT_VERSION)
if(SKBUILD AND SKBUILD_PROJECT_VERSION)
    set(PYPYLON_VERSION_STRING ${SKBUILD_PROJECT_VERSION})
    message(STATUS "pypylon version from setuptools_scm: ${PYPYLON_VERSION_STRING}")
else()
    # Fallback for when building outside of pip/build
    set(PYPYLON_VERSION_STRING "0.0.0+unknown")
    message(WARNING "No version from setuptools_scm, using fallback: ${PYPYLON_VERSION_STRING}")
endif()

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# scikit-build-core sets this automatically, but we can also detect it
if(NOT DEFINED SKBUILD_PROJECT_NAME)
    set(SKBUILD_PROJECT_NAME "pypylon")
endif()

# Configuration options
option(PYPYLON_USE_LIMITED_API "Use Python Limited API for stable ABI" ON)
option(PYPYLON_INCLUDE_DATA_PROCESSING "Include pylon data processing support" ON)
set(PYPYLON_MIN_LIMITED_API_VERSION "0x03090000" CACHE STRING "Minimum Python version for limited API")

# Find required packages
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(SWIG 4.3 REQUIRED)

# Include SWIG
include(UseSWIG)

# Platform detection for reference (though official CMake targets handle this)
if(WIN32)
    set(PYPYLON_PLATFORM "Windows")
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(PYPYLON_ARCH "x64")
    else()
        set(PYPYLON_ARCH "Win32")
    endif()
elseif(APPLE)
    set(PYPYLON_PLATFORM "Darwin")
    set(PYPYLON_ARCH "lib64")
elseif(UNIX)
    set(PYPYLON_PLATFORM "Linux")
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        set(PYPYLON_ARCH "lib64")
    else()
        set(PYPYLON_ARCH "lib")
    endif()
endif()

message(STATUS "Building for platform: ${PYPYLON_PLATFORM} ${PYPYLON_ARCH}")

# Use the same approach as official pylon samples
# for Unix system. All other OS PYLON_ROOT will be empty
list(APPEND CMAKE_PREFIX_PATH $ENV{PYLON_ROOT})
# for Windows system. All other OS PYLON_DEV_DIR will be empty
list(APPEND CMAKE_PREFIX_PATH $ENV{PYLON_DEV_DIR})

# Find pylon using the official CMake configuration
find_package(pylon REQUIRED)

message(STATUS "Found pylon: ${pylon_DIR}")

# Display pylon version info if available
if(DEFINED pylon_VERSION)
    message(STATUS "pylon version: ${pylon_VERSION}")
elseif(DEFINED PYLON_VERSION)
    message(STATUS "pylon version: ${PYLON_VERSION}")
else()
    # Try to get version from pylon target properties
    if(TARGET pylon::pylon)
        get_target_property(PYLON_VERSION_PROP pylon::pylon INTERFACE_PYLON_VERSION)
        if(PYLON_VERSION_PROP)
            message(STATUS "pylon version: ${PYLON_VERSION_PROP}")
        else()
            message(STATUS "pylon version: information not available")
        endif()
    endif()
endif()

# Add local cmake directory to module path for our finders
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Check for data processing support using local finder
if(PYPYLON_INCLUDE_DATA_PROCESSING)
    find_package(pylonDataProcessing QUIET)
    if(pylonDataProcessing_FOUND)
        set(PYLON_DATA_PROCESSING_FOUND TRUE)
        message(STATUS "✓ pylon data processing support found")
    else()
        set(PYLON_DATA_PROCESSING_FOUND FALSE)
        message(STATUS "✗ pylon data processing support not found")
    endif()
else()
    set(PYLON_DATA_PROCESSING_FOUND FALSE)
    message(STATUS "PYPYLON_INCLUDE_DATA_PROCESSING is FALSE, skipping data processing")
endif()

# Set up limited API if enabled
if(PYPYLON_USE_LIMITED_API AND Python_VERSION VERSION_GREATER_EQUAL "3.9")
    set(Python_LIMITED_API TRUE)
    add_compile_definitions(Py_LIMITED_API=${PYPYLON_MIN_LIMITED_API_VERSION})
    message(STATUS "Using Python Limited API: ${PYPYLON_MIN_LIMITED_API_VERSION}")
endif()

# Common compile definitions
add_compile_definitions(SWIG_TYPE_TABLE=pylon)

# Platform-specific compile definitions and flags
if(WIN32)
    add_compile_definitions(
        UNICODE
        _UNICODE  
        _CRT_SECURE_NO_WARNINGS
    )
    
    if(MSVC)
        add_compile_options(
            /Gy      # separate functions for linker
            /GL      # enable link-time code generation  
            /EHsc    # set exception handling model
        )
        add_link_options(
            /LTCG    # link-time code generation
        )
    endif()
    
elseif(UNIX)
    add_compile_options(
        -Wno-unknown-pragmas
        -fPIC
        -g0
        -Wall
        -O3
        -Wno-switch
    )
    
    if(APPLE)
        add_compile_options(-std=c++17)
        add_link_options(
            -g0
            -Wl,-rpath,@loader_path
        )
    else()
        add_link_options(
            -g0
            -Wl,--enable-new-dtags
            -Wl,-rpath,$ORIGIN
            -Wl,-rpath,$ORIGIN/pypylon
        )
    endif()
endif()

# Configure version files
configure_file(
    "${CMAKE_SOURCE_DIR}/cmake/pypylon_version.h.in"
    "${CMAKE_BINARY_DIR}/generated/pypylon_version.h"
    @ONLY
)

# SWIG configuration
set(CMAKE_SWIG_FLAGS 
    -c++
    -Wextra
    -Wall
    -threads
)

# Platform-specific SWIG flags
if(UNIX AND NOT APPLE)
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
        list(APPEND CMAKE_SWIG_FLAGS -DSWIGWORDSIZE64)
    else()
        list(APPEND CMAKE_SWIG_FLAGS -DSWIGWORDSIZE32)
    endif()
endif()

# Function to create a SWIG Python module
function(add_swig_python_module module_name swig_file)
    message(STATUS "Creating SWIG module: ${module_name} from ${swig_file}")
    set_property(SOURCE ${swig_file} PROPERTY CPLUSPLUS ON)
    set_property(SOURCE ${swig_file} PROPERTY SWIG_MODULE_NAME ${module_name})
    
    # Set basic SWIG flags
    set_property(SOURCE ${swig_file} PROPERTY SWIG_FLAGS ${CMAKE_SWIG_FLAGS})
    
    swig_add_library(${module_name}
        TYPE MODULE
        LANGUAGE python
        SOURCES ${swig_file}
    )
    
    # Set module properties
    set_target_properties(${module_name} PROPERTIES
        OUTPUT_NAME "_${module_name}"
        PREFIX ""
    )
    
    # Link with Python and pylon using official targets
    target_link_libraries(${module_name} 
        PRIVATE 
        Python::Module
        pylon::pylon
    )
    
    # CRUCIAL: Tell SWIG to use target include directories (requires CMake 3.13+)
    set_property(TARGET ${module_name} PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)
    
    # Set rpath for the extension module to find bundled pylon libraries
    if(UNIX AND NOT APPLE)
        set_target_properties(${module_name} PROPERTIES
            INSTALL_RPATH "$ORIGIN"
            BUILD_WITH_INSTALL_RPATH TRUE
        )
    endif()
    
    # Add our source include directories
    target_include_directories(${module_name} 
        PRIVATE 
        ${CMAKE_SOURCE_DIR}/src/genicam
        ${CMAKE_SOURCE_DIR}/src/pylon
        ${CMAKE_SOURCE_DIR}/src/pylondataprocessing
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_BINARY_DIR}/generated
    )
    
    # Install the module
    install(TARGETS ${module_name} DESTINATION pypylon)
    
    # Install the SWIG-generated Python wrapper file
    install(FILES ${CMAKE_BINARY_DIR}/${module_name}.py DESTINATION pypylon)
    
    # Add version information to the SWIG-generated Python file
    add_custom_command(TARGET ${module_name} POST_BUILD
        COMMAND ${CMAKE_COMMAND} 
            -DMODULE_FILE=${CMAKE_BINARY_DIR}/${module_name}.py
            -DVERSION_STRING=${PYPYLON_VERSION_STRING}
            -P ${CMAKE_SOURCE_DIR}/cmake/AppendVersion.cmake
        COMMENT "Adding version info to ${module_name}.py"
    )
endfunction()

# Create the modules
add_swig_python_module(genicam ${CMAKE_SOURCE_DIR}/src/genicam/genicam.i)
add_swig_python_module(pylon ${CMAKE_SOURCE_DIR}/src/pylon/pylon.i)

# Handle data processing module if available
if(PYPYLON_INCLUDE_DATA_PROCESSING AND PYLON_DATA_PROCESSING_FOUND)
    add_swig_python_module(pylondataprocessing ${CMAKE_SOURCE_DIR}/src/pylondataprocessing/pylondataprocessing.i)
    
    # Link with data processing target (created by local finder)
    if(TARGET pylon::DataProcessing)
        target_link_libraries(pylondataprocessing PRIVATE pylon::DataProcessing)
        message(STATUS "Linking pylondataprocessing with pylon::DataProcessing")
    else()
        message(WARNING "Data processing found but pylon::DataProcessing target not available")
    endif()
    
    message(STATUS "Including pylon data processing support")
else()
    message(STATUS "Pylon data processing support disabled or not available")
endif()

# Install Python package files
install(DIRECTORY ${CMAKE_SOURCE_DIR}/src/pypylon/ 
        DESTINATION .
        FILES_MATCHING 
        PATTERN "*.py"
        PATTERN "__pycache__" EXCLUDE
)

# Install Pylon license files - get path from pylon target
if(DEFINED SKBUILD_METADATA_DIR)
    # Try to get pylon installation directory from the target
    get_target_property(PYLON_IMPORTED_LOCATION pylon::pylon IMPORTED_LOCATION)
    if(PYLON_IMPORTED_LOCATION)
        get_filename_component(PYLON_LIB_DIR ${PYLON_IMPORTED_LOCATION} DIRECTORY)
        get_filename_component(PYLON_ROOT_DIR ${PYLON_LIB_DIR} DIRECTORY)
        set(PYLON_LICENSE_DIR "${PYLON_ROOT_DIR}/share/pylon/licenses")
    elseif(DEFINED ENV{PYLON_ROOT})
        set(PYLON_LICENSE_DIR "$ENV{PYLON_ROOT}/share/pylon/licenses")
    endif()
    
    if(DEFINED PYLON_LICENSE_DIR AND EXISTS "${PYLON_LICENSE_DIR}/License.txt")
        message(STATUS "Installing Pylon license from ${PYLON_LICENSE_DIR}")
        install(FILES "${PYLON_LICENSE_DIR}/License.txt"
                DESTINATION "${SKBUILD_METADATA_DIR}/licenses"
                RENAME "PYLON_LICENSE.txt")
    else()
        message(WARNING "Pylon license not found at expected location")
    endif()
    
    if(DEFINED PYLON_LICENSE_DIR AND EXISTS "${PYLON_LICENSE_DIR}/pylon_Third-Party_Licenses.txt")
        install(FILES "${PYLON_LICENSE_DIR}/pylon_Third-Party_Licenses.txt"
                DESTINATION "${SKBUILD_METADATA_DIR}/licenses"
                RENAME "PYLON_THIRD_PARTY_LICENSES.txt")
    else()
        message(WARNING "Pylon third-party licenses not found at expected location")
    endif()
else()
    message(WARNING "SKBUILD_METADATA_DIR not defined")
endif()

# Copy runtime dependencies
# Pass pylon version to runtime dependencies and include
set(PYLON_VERSION_FOR_RUNTIME ${pylon_VERSION})
include(cmake/CopyRuntimeDeps.cmake)

# Set version for the package
if(SKBUILD)
    # setuptools_scm handles version detection automatically
    set_property(TARGET genicam PROPERTY SWIG_COMPILE_DEFINITIONS PYPYLON_VERSION="${PYPYLON_VERSION_STRING}")
    set_property(TARGET pylon PROPERTY SWIG_COMPILE_DEFINITIONS PYPYLON_VERSION="${PYPYLON_VERSION_STRING}")
    # Handle data processing module if available
    if(PYPYLON_INCLUDE_DATA_PROCESSING AND PYLON_DATA_PROCESSING_FOUND)
        set_property(TARGET pylondataprocessing PROPERTY SWIG_COMPILE_DEFINITIONS PYPYLON_VERSION="${PYPYLON_VERSION_STRING}")
    endif()
endif()

message(STATUS "CMake configuration complete with version: ${PYPYLON_VERSION_STRING}")
