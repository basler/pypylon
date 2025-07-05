#.rst:
# FindpylonDataProcessing.cmake
# Copyright (c) 2021-2025 Basler AG
# http://www.baslerweb.com
#
# Find and using pylon Data Processing C++ SDK
# --------------------------------------------
#
# Try to locate the pylon C++ Data Processing SDK package.
#
# The ``PYLON_DEV_DIR`` (CMake or Environment) variable should be used
# to pinpoint the pylon C++ Data Processing SDK package files.
#
# If found, this will define the following variables:
#
# ``pylonDataProcessing_FOUND``
#     True if the pylon C++ Data Processing SDK package has been found.
#
# ``pylonDataProcessing_INCLUDE_DIRS``
#     List containing needed include directory's for pylon C++ Data Processing SDK.
#
# ``pylonDataProcessing_LIBRARIES``
#     List containing needed libraries for linking pylon C++ Data Processing SDK.
#

# Checks the PYLON_DEV_DIR and PYLON_ROOT environment variables
if(DEFINED ENV{PYLON_DEV_DIR})
  set(PYLON_DEV_DIR "$ENV{PYLON_DEV_DIR}")
elseif(DEFINED ENV{PYLON_ROOT})
  set(PYLON_DEV_DIR "$ENV{PYLON_ROOT}")
endif()

if(APPLE)
  # Find pylondataprocessing framework includes
  find_path(pylonDataProcessing_INCLUDE_DIRS
    NAMES pylondataprocessing/PylonDataProcessingIncludes.h
    HINTS
      "${PYLON_DEV_DIR}"
      "/Library/Frameworks"
  )

  # Find pylondataprocessing framework
  find_library(pylonDataProcessing_LIBRARIES
    NAMES pylondataprocessing
    HINTS
      "${PYLON_DEV_DIR}"
      "/Library/Frameworks"
  )

  # Check if pylondataprocessing framework was found
  if(pylonDataProcessing_INCLUDE_DIRS AND pylonDataProcessing_LIBRARIES)
    set(pylonDataProcessing_FOUND TRUE)
  endif()

elseif(MSVC)
  # To make this finder compatible with future pylon versions, we search for a wide range of versions.
  set(min_pylon_version 8)
  set(max_pylon_version 29)

  set(pylon_include_path_names)
  foreach(version RANGE ${min_pylon_version} ${max_pylon_version})
    list(APPEND pylon_include_path_names C:/Program Files/Basler/pylon ${version}/Development/include)
  endforeach()

  # Reverse list to prefer newer versions over older versions.
  list(REVERSE pylon_include_path_names)

  # Windows include paths
  find_path(_PYLON_DATAPROCESSING_SDK_INCLUDE_DIR
    NAMES pylondataprocessing/PylonDataProcessingIncludes.h
    HINTS
      "${PYLON_DEV_DIR}/include"
      "${pylon_include_path_names}"
  )

  # Search locations for libraries
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    # Windows 64 bits
    list(APPEND _PYLON_DATAPROCESSING_SDK_LIB_SEARCH_PATH "${_PYLON_DATAPROCESSING_SDK_INCLUDE_DIR}/../lib/x64")
  else()
    # Windows 32 bits
    list(APPEND _PYLON_DATAPROCESSING_SDK_LIB_SEARCH_PATH "${_PYLON_DATAPROCESSING_SDK_INCLUDE_DIR}/../lib/Win32")
  endif()

  # Find locations of pylon libraries
  find_library(pylonDataProcessing_LIBRARIES
    NAMES PylonDataProcessing_v3.lib
    PATHS ${_PYLON_DATAPROCESSING_SDK_LIB_SEARCH_PATH}
  )

  # Append found pylon include path
  if(_PYLON_DATAPROCESSING_SDK_INCLUDE_DIR)
    list(APPEND pylonDataProcessing_INCLUDE_DIRS ${_PYLON_DATAPROCESSING_SDK_INCLUDE_DIR})
  endif()

  # Check if pylon include and libraries are found
  if(pylonDataProcessing_INCLUDE_DIRS AND pylonDataProcessing_LIBRARIES)
    set(pylonDataProcessing_FOUND TRUE)
  endif()

elseif(UNIX)
  # Find pylon-config tool
  find_program(_PYLON_DATAPROCESSING_SDK_CONFIG
    NAMES pylon-dataprocessing-config
    HINTS
      "${PYLON_DEV_DIR}"
      "/opt/pylon"
    PATH_SUFFIXES bin
  )

  # Parse include and libraries from pylon-config tool
  if(_PYLON_DATAPROCESSING_SDK_CONFIG)
    execute_process(COMMAND ${_PYLON_DATAPROCESSING_SDK_CONFIG} "--libs"
                    OUTPUT_VARIABLE _PYLON_DATAPROCESSING_SDK_BASELIBS_LFLAGS
                    OUTPUT_STRIP_TRAILING_WHITESPACE)
    execute_process(COMMAND ${_PYLON_DATAPROCESSING_SDK_CONFIG} "--libs-rpath"
                    OUTPUT_VARIABLE _PYLON_DATAPROCESSING_SDK_RPATH_LINK_LFLAGS_TMP
                    OUTPUT_STRIP_TRAILING_WHITESPACE)
    execute_process(COMMAND ${_PYLON_DATAPROCESSING_SDK_CONFIG} "--cflags-only-I"
                    OUTPUT_VARIABLE _PYLON_DATAPROCESSING_SDK_INCLUDE_TMP
                    OUTPUT_STRIP_TRAILING_WHITESPACE)
    string(REPLACE "-I" "" pylonDataProcessing_INCLUDE_DIRS ${_PYLON_DATAPROCESSING_SDK_INCLUDE_TMP})

    # Remove the erroneous @ on the -rpath-link parameter comming from pylon-config,
    # manually assemble linker flags for pylon core linkage.
    string(REPLACE "@" "" _PYLON_DATAPROCESSING_SDK_RPATH_LINK_LFLAGS ${_PYLON_DATAPROCESSING_SDK_RPATH_LINK_LFLAGS_TMP})
    string(APPEND pylonDataProcessing_LIBRARIES "${_PYLON_DATAPROCESSING_SDK_BASELIBS_LFLAGS} ${_PYLON_DATAPROCESSING_SDK_RPATH_LINK_LFLAGS}")

    set(pylonDataProcessing_FOUND TRUE)
  endif()

endif()

if (pylonDataProcessing_FOUND)
  add_library(pylon::DataProcessing INTERFACE IMPORTED)
  set_target_properties(pylon::DataProcessing PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${pylonDataProcessing_INCLUDE_DIRS}"
    INTERFACE_LINK_LIBRARIES "${pylonDataProcessing_LIBRARIES}"
  )
endif()

mark_as_advanced(pylonDataProcessing_INCLUDE_DIRS pylonDataProcessing_LIBRARIES)

include(FeatureSummary)
set_package_properties(pylonDataProcessing PROPERTIES
  URL "https://www.baslerweb.com/de/produkte/software/basler-pylon-camera-software-suite"
  DESCRIPTION "Basler Camera Software Suite - pylon Data Processing C++ SDK"
)
