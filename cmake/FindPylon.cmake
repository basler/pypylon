# FindPylon.cmake - Find Basler Pylon SDK
#
# This module defines:
#  PYLON_FOUND - True if Pylon SDK is found
#  PYLON_INCLUDE_DIRS - Include directories for Pylon
#  PYLON_LIBRARIES - Libraries to link against
#  PYLON_RUNTIME_FILES - Runtime files to copy
#  PYLON_DATA_PROCESSING_FOUND - True if data processing support is available
#  PYLON_DATA_PROCESSING_LIBRARIES - Data processing libraries
#  PYLON_VERSION - Version of Pylon SDK

set(PYLON_FOUND FALSE)
set(PYLON_DATA_PROCESSING_FOUND FALSE)

if(WIN32)
    # Windows - Look for Pylon SDK
    if(DEFINED ENV{PYLON_DEV_DIR})
        set(PYLON_ROOT $ENV{PYLON_DEV_DIR})
    else()
        # Default installation paths
        file(GLOB PYLON_CANDIDATES
            "C:/Program Files/Basler/pylon*/Development"
            "C:/Program Files (x86)/Basler/pylon*/Development"
        )
        if(PYLON_CANDIDATES)
            list(GET PYLON_CANDIDATES 0 PYLON_ROOT)
        endif()
    endif()
    
    if(PYLON_ROOT AND EXISTS "${PYLON_ROOT}")
        message(STATUS "Found Pylon SDK at: ${PYLON_ROOT}")
        
        # Include directories
        set(PYLON_INCLUDE_DIRS
            "${PYLON_ROOT}/include"
        )
        
        # Library directories and libraries
        if(CMAKE_SIZEOF_VOID_P EQUAL 8)
            set(PYLON_LIB_DIR "${PYLON_ROOT}/lib/x64")
            set(PYLON_BIN_DIR "${PYLON_ROOT}/bin/x64")
        else()
            set(PYLON_LIB_DIR "${PYLON_ROOT}/lib/Win32")
            set(PYLON_BIN_DIR "${PYLON_ROOT}/bin/Win32")
        endif()
        
        # Find required libraries
        find_library(PYLON_BASE_LIB
            NAMES PylonBase_v6_3 PylonBase_v7_0 PylonBase_v7_1 PylonBase_v7_2 PylonBase_v7_3 PylonBase_v7_4 PylonBase_v8_0
            PATHS ${PYLON_LIB_DIR}
            NO_DEFAULT_PATH
        )
        
        if(PYLON_BASE_LIB)
            set(PYLON_LIBRARIES ${PYLON_BASE_LIB})
            set(PYLON_FOUND TRUE)
            
            # Get version from library name
            get_filename_component(PYLON_LIB_NAME ${PYLON_BASE_LIB} NAME_WE)
            string(REGEX MATCH "v([0-9]+)_([0-9]+)" PYLON_VERSION_MATCH ${PYLON_LIB_NAME})
            if(PYLON_VERSION_MATCH)
                set(PYLON_VERSION "${CMAKE_MATCH_1}.${CMAKE_MATCH_2}")
            endif()
            
            # Check for data processing support
            find_library(PYLON_DATA_PROCESSING_LIB
                NAMES PylonDataProcessing_v1_3 PylonDataProcessing_v1_4 PylonDataProcessing_v2_0
                PATHS ${PYLON_LIB_DIR}
                NO_DEFAULT_PATH
            )
            
            if(PYLON_DATA_PROCESSING_LIB)
                set(PYLON_DATA_PROCESSING_LIBRARIES ${PYLON_DATA_PROCESSING_LIB})
                set(PYLON_DATA_PROCESSING_FOUND TRUE)
            endif()
        endif()
    endif()
    
elseif(APPLE)
    # macOS - Look for Pylon Framework
    if(DEFINED ENV{PYLON_FRAMEWORK_LOCATION})
        set(PYLON_FRAMEWORK_PATH $ENV{PYLON_FRAMEWORK_LOCATION})
    else()
        set(PYLON_FRAMEWORK_PATH "/Library/Frameworks")
    endif()
    
    set(PYLON_FRAMEWORK "${PYLON_FRAMEWORK_PATH}/pylon.framework")
    
    if(EXISTS "${PYLON_FRAMEWORK}")
        message(STATUS "Found Pylon Framework at: ${PYLON_FRAMEWORK}")
        
        # Include directories
        set(PYLON_INCLUDE_DIRS
            "${PYLON_FRAMEWORK}/Headers"
            "${PYLON_FRAMEWORK}/Headers/GenICam"
        )
        
        # Framework linking
        set(PYLON_LIBRARIES "-framework pylon")
        set(PYLON_FOUND TRUE)
        
        # Get version using pylon-config
        set(PYLON_CONFIG "${PYLON_FRAMEWORK}/Versions/Current/Resources/Tools/pylon-config")
        if(EXISTS "${PYLON_CONFIG}")
            execute_process(
                COMMAND ${PYLON_CONFIG} --version
                OUTPUT_VARIABLE PYLON_VERSION
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
            )
        endif()
        
        # Data processing is typically not available on macOS
        set(PYLON_DATA_PROCESSING_FOUND FALSE)
    endif()
    
elseif(UNIX)
    # Linux - Look for Pylon installation
    if(DEFINED ENV{PYLON_ROOT})
        set(PYLON_ROOT $ENV{PYLON_ROOT})
    else()
        set(PYLON_ROOT "/opt/pylon")
    endif()
    
    # Check for pylon-config
    set(PYLON_CONFIG "${PYLON_ROOT}/bin/pylon-config")
    if(EXISTS "${PYLON_CONFIG}")
        message(STATUS "Found pylon-config at: ${PYLON_CONFIG}")
        
        # Get compiler flags
        execute_process(
            COMMAND ${PYLON_CONFIG} --cflags-only-I
            OUTPUT_VARIABLE PYLON_CFLAGS
            OUTPUT_STRIP_TRAILING_WHITESPACE
            ERROR_QUIET
        )
        
        # Parse include directories
        string(REPLACE " " ";" PYLON_CFLAGS_LIST ${PYLON_CFLAGS})
        set(PYLON_INCLUDE_DIRS)
        foreach(flag ${PYLON_CFLAGS_LIST})
            if(flag MATCHES "^-I(.+)")
                list(APPEND PYLON_INCLUDE_DIRS ${CMAKE_MATCH_1})
            endif()
        endforeach()
        
        # Get library flags
        execute_process(
            COMMAND ${PYLON_CONFIG} --libs
            OUTPUT_VARIABLE PYLON_LIBS
            OUTPUT_STRIP_TRAILING_WHITESPACE
            ERROR_QUIET
        )
        
        # Parse libraries
        string(REPLACE " " ";" PYLON_LIBS_LIST ${PYLON_LIBS})
        set(PYLON_LIBRARIES)
        set(PYLON_LIBRARY_DIRS)
        foreach(flag ${PYLON_LIBS_LIST})
            if(flag MATCHES "^-L(.+)")
                list(APPEND PYLON_LIBRARY_DIRS ${CMAKE_MATCH_1})
            elseif(flag MATCHES "^-l(.+)")
                list(APPEND PYLON_LIBRARIES ${CMAKE_MATCH_1})
            endif()
        endforeach()
        
        set(PYLON_FOUND TRUE)
        
        # Get version
        execute_process(
            COMMAND ${PYLON_CONFIG} --version
            OUTPUT_VARIABLE PYLON_VERSION
            OUTPUT_STRIP_TRAILING_WHITESPACE
            ERROR_QUIET
        )
        
        # Check for data processing support
        set(PYLON_DATA_PROCESSING_CONFIG "${PYLON_ROOT}/bin/pylon-dataprocessing-config")
        if(EXISTS "${PYLON_DATA_PROCESSING_CONFIG}")
            execute_process(
                COMMAND ${PYLON_DATA_PROCESSING_CONFIG} --libs
                OUTPUT_VARIABLE PYLON_DP_LIBS
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
            )
            
            if(PYLON_DP_LIBS)
                # Parse data processing libraries
                string(REPLACE " " ";" PYLON_DP_LIBS_LIST ${PYLON_DP_LIBS})
                set(PYLON_DATA_PROCESSING_LIBRARIES)
                foreach(flag ${PYLON_DP_LIBS_LIST})
                    if(flag MATCHES "^-l(.+)")
                        list(APPEND PYLON_DATA_PROCESSING_LIBRARIES ${CMAKE_MATCH_1})
                    endif()
                endforeach()
                set(PYLON_DATA_PROCESSING_FOUND TRUE)
            endif()
        endif()
    endif()
endif()

# Set library directories for linking
if(PYLON_LIBRARY_DIRS)
    link_directories(${PYLON_LIBRARY_DIRS})
endif()

# Framework path for macOS
if(APPLE AND PYLON_FRAMEWORK_PATH)
    link_directories(${PYLON_FRAMEWORK_PATH})
endif()

# Report results
if(PYLON_FOUND)
    message(STATUS "Pylon SDK found:")
    message(STATUS "  Version: ${PYLON_VERSION}")
    message(STATUS "  Include dirs: ${PYLON_INCLUDE_DIRS}")
    message(STATUS "  Libraries: ${PYLON_LIBRARIES}")
    if(PYLON_DATA_PROCESSING_FOUND)
        message(STATUS "  Data processing: Available")
        message(STATUS "  Data processing libs: ${PYLON_DATA_PROCESSING_LIBRARIES}")
    else()
        message(STATUS "  Data processing: Not available")
    endif()
else()
    message(WARNING "Pylon SDK not found! Set PYLON_ROOT, PYLON_DEV_DIR, or PYLON_FRAMEWORK_LOCATION environment variable")
endif()

# Handle required/optional components
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Pylon
    REQUIRED_VARS PYLON_INCLUDE_DIRS PYLON_LIBRARIES
    VERSION_VAR PYLON_VERSION
)

mark_as_advanced(
    PYLON_INCLUDE_DIRS
    PYLON_LIBRARIES  
    PYLON_DATA_PROCESSING_LIBRARIES
    PYLON_VERSION
) 