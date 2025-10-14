# CopyRuntimeDeps.cmake - Copy runtime dependencies for pypylon
#
# This module copies the necessary runtime files (DLLs, shared libraries, etc.)
# from the Pylon SDK to the pypylon package directory

# Function to copy files matching patterns
function(copy_files_matching source_dir dest_dir patterns)
    foreach(pattern ${patterns})
        if(WIN32)
            # On Windows, use glob for shell patterns
            file(GLOB matching_files "${source_dir}/${pattern}")
        else()
            # On Unix, use regex patterns
            file(GLOB all_files "${source_dir}/*")
            set(matching_files)
            foreach(file ${all_files})
                get_filename_component(filename ${file} NAME)
                if(filename MATCHES ${pattern})
                    list(APPEND matching_files ${file})
                endif()
            endforeach()
        endif()

        foreach(file ${matching_files})
            get_filename_component(filename ${file} NAME)
            
            # Resolve symlinks to get the actual file
            if(UNIX AND NOT APPLE)
                get_filename_component(resolved_file ${file} REALPATH)
                if(EXISTS ${resolved_file})
                    message(STATUS "Copying runtime file: ${filename} (resolved from symlink)")
                    # Copy the resolved file but keep the original name
                    install(FILES ${resolved_file} DESTINATION pypylon RENAME ${filename})
                else()
                    message(STATUS "Copying runtime file: ${filename}")
                    install(FILES ${file} DESTINATION pypylon)
                endif()
            else()
                message(STATUS "Copying runtime file: ${filename}")
                install(FILES ${file} DESTINATION pypylon)
            endif()
        endforeach()
    endforeach()
endfunction()

# Function to copy directories
function(copy_directory source_dir dest_dir)
    if(EXISTS ${source_dir})
        message(STATUS "Copying runtime directory: ${source_dir}")
        install(DIRECTORY ${source_dir}/ DESTINATION pypylon/${dest_dir})
    endif()
endfunction()

# Function to copy directories excluding Editor packages
function(copy_directory_excluding_editors source_dir dest_dir)
    if(EXISTS ${source_dir})
        message(STATUS "Copying runtime directory (excluding editors): ${source_dir}")
        install(DIRECTORY ${source_dir}/ 
                DESTINATION pypylon/${dest_dir}
                PATTERN "*Editor*.so" EXCLUDE
                PATTERN "*Editor*.dll" EXCLUDE)
    endif()
endfunction()

# Platform-specific runtime copying
if(WIN32 AND (PYLON_FOUND OR pylon_FOUND))
    message(STATUS "Copying Windows runtime files...")

    # Base runtime files
    set(BASE_PATTERNS
        "PylonBase_*.dll"
        "GCBase_MD_*.dll"
        "GenApi_MD_*.dll"
        "log4cpp_MD_*.dll"
        "Log_MD_*.dll"
        "NodeMapData_MD_*.dll"
        "XmlParser_MD_*.dll"
        "MathParser_MD_*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${BASE_PATTERNS}")

    # GigE runtime files
    set(GIGE_PATTERNS
        "PylonGigE_*.dll"
        "gxapi*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${GIGE_PATTERNS}")

    # USB runtime files
    set(USB_PATTERNS
        "PylonUsb_*.dll"
        "uxapi*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${USB_PATTERNS}")

    # Camera emulation runtime files
    set(CAMEMU_PATTERNS
        "PylonCamEmu_*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${CAMEMU_PATTERNS}")

    # Extra runtime files
    set(EXTRA_PATTERNS
        "PylonGUI_*.dll"
        "PylonUtility_*.dll"
        "PylonUtilityPcl_*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${EXTRA_PATTERNS}")
    
    # GenTL runtime files
    set(GENTL_PATTERNS
        "PylonGtc_*.dll"
    )
    copy_files_matching(${PYLON_BIN_DIR} pypylon "${GENTL_PATTERNS}")
    
    # Data processing runtime files (if available)
    if(PYLON_DATA_PROCESSING_FOUND)
        set(DP_PATTERNS
            "PylonDataProcessing_v*.dll"
            "PylonDataProcessing_v*.sig"
            "PylonDataProcessingCore_*.dll"
        )
        copy_files_matching(${PYLON_BIN_DIR} pypylon "${DP_PATTERNS}")
        
        # Windows data processing plugin directories
        # Use PYLON_BIN_DIR for the base runtime directory
        set(DP_PLUGIN_DIR "${PYLON_BIN_DIR}/pylonDataProcessingPlugins")
        if(EXISTS "${DP_PLUGIN_DIR}")
            copy_directory_excluding_editors("${DP_PLUGIN_DIR}" "pylonDataProcessingPlugins")
        endif()
        
        set(DP_CREATOR_DIR "${PYLON_BIN_DIR}/DataProcessingPluginsB")
        if(EXISTS "${DP_CREATOR_DIR}")
            copy_directory_excluding_editors("${DP_CREATOR_DIR}" "DataProcessingPluginsB")
        endif()
    endif()

elseif(UNIX AND NOT APPLE AND (PYLON_FOUND OR pylon_FOUND))
    message(STATUS "Copying Linux runtime files...")
    
    # Ensure PYLON_ROOT has a default value for Linux
    if(NOT DEFINED PYLON_ROOT)
        if(DEFINED ENV{PYLON_ROOT})
            set(PYLON_ROOT $ENV{PYLON_ROOT})
        else()
            set(PYLON_ROOT "/opt/pylon")
        endif()
    endif()
    
    # Get Pylon library directory
    set(PYLON_LIB_DIR "${PYLON_ROOT}/lib")

    # Determine Pylon version to use appropriate patterns
    set(RUNTIME_PYLON_VERSION ${PYLON_VERSION_FOR_RUNTIME})
    if(NOT RUNTIME_PYLON_VERSION)
        set(RUNTIME_PYLON_VERSION ${pylon_VERSION})
    endif()
    if(NOT RUNTIME_PYLON_VERSION)
        set(RUNTIME_PYLON_VERSION ${PYLON_VERSION})
    endif()
    
    if(RUNTIME_PYLON_VERSION VERSION_LESS "9.0.3")
        # Newer naming scheme
        set(BASE_PATTERNS
            "libpylonbase\\.so\\.[0-9]+$"
            "libGCBase_.*\\.so"
            "libGenApi_.*\\.so"
            "liblog4cpp_.*\\.so"
            "libLog_.*\\.so"
            "libNodeMapData_.*\\.so"
            "libXmlParser_.*\\.so"
            "libMathParser_.*\\.so"
        )
        
        set(GIGE_PATTERNS
            "libpylon_TL_gige\\.so"
            "libgxapi\\.so\\.[0-9]+$"
        )
        
        set(USB_PATTERNS
            "libpylon_TL_usb\\.so"
            "libuxapi\\.so\\.[0-9]+$"
            "pylon-libusb-.*\\.so"
        )
        
        set(CAMEMU_PATTERNS
            "libpylon_TL_camemu\\.so"
        )
        
        set(EXTRA_PATTERNS
            "libpylonutility\\.so\\.[0-9]+$"
            "libpylonutilitypcl\\.so\\.[0-9]+$"
        )
        
        set(GENTL_PATTERNS
            "libpylon_TL_gtc\\.so"
        )
        
        if(PYLON_DATA_PROCESSING_FOUND)
            set(DP_PATTERNS
                "libPylonDataProcessing\\.so\\.[0-9]+$"
                "libPylonDataProcessing.sig"
                "libPylonDataProcessingCore\\.so\\.[0-9]+$"
            )
        endif()
        
    else()
        # Latest naming scheme  
        set(BASE_PATTERNS
            "libpylonbase\\.so\\.[0-9]+$"
            "libpylonutility\\.so\\.[0-9]+$"
            "libGCBase_.*\\.so"
            "libGenApi_.*\\.so"
            "liblog4cpp_.*\\.so"
            "libLog_.*\\.so"
            "libNodeMapData_.*\\.so"
            "libXmlParser_.*\\.so"
            "libMathParser_.*\\.so"
        )
        
        set(GIGE_PATTERNS
            "libpylon_TL_gige\\.so"
            "libgxapi\\.so\\.[0-9]+$"
        )
        
        set(USB_PATTERNS
            "libpylon_TL_usb\\.so"
            "libuxapi\\.so\\.[0-9]+$"
            "pylon-libusb-.*\\.so"
        )
        
        set(CAMEMU_PATTERNS
            "libpylon_TL_camemu\\.so"
        )
        
        set(EXTRA_PATTERNS
            "libpylonutilitypcl\\.so\\.[0-9]+$"
        )
        
        set(GENTL_PATTERNS
            "libpylon_TL_gtc\\.so"
        )
        
        if(PYLON_DATA_PROCESSING_FOUND)
            set(DP_PATTERNS
                "libPylonDataProcessing\\.so\\.[0-9]+$"
                "libPylonDataProcessing.sig"
                "libPylonDataProcessingCore\\.so\\.[0-9]+$"
            )
        endif()
    endif()
    
    # Copy all pattern sets
    message(STATUS "Pylon library directory: ${PYLON_LIB_DIR}")
    message(STATUS "Pylon version for runtime: ${RUNTIME_PYLON_VERSION}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${BASE_PATTERNS}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${GIGE_PATTERNS}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${USB_PATTERNS}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${CAMEMU_PATTERNS}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${EXTRA_PATTERNS}")
    copy_files_matching(${PYLON_LIB_DIR} pypylon "${GENTL_PATTERNS}")
    
    if(PYLON_DATA_PROCESSING_FOUND)
        copy_files_matching(${PYLON_LIB_DIR} pypylon "${DP_PATTERNS}")
        
        # Data processing plugin directories (excluding Editor packages)
        set(DP_PLUGIN_DIR "${PYLON_ROOT}/lib/pylondataprocessingplugins")
        if(EXISTS "${DP_PLUGIN_DIR}")
            copy_directory_excluding_editors("${DP_PLUGIN_DIR}" "pylondataprocessingplugins")
        endif()
        
        set(DP_CREATOR_DIR "${PYLON_ROOT}/lib/dataprocessingpluginsb")
        if(EXISTS "${DP_CREATOR_DIR}")
            copy_directory_excluding_editors("${DP_CREATOR_DIR}" "dataprocessingpluginsb")
        endif()
    endif()

elseif(APPLE AND (PYLON_FOUND OR pylon_FOUND))
    message(STATUS "macOS: Copying pylon.framework to pypylon package")
    
    # Determine framework path
    if(DEFINED ENV{PYLON_FRAMEWORK_LOCATION})
        set(PYLON_FRAMEWORK_PATH "$ENV{PYLON_FRAMEWORK_LOCATION}")
    else()
        set(PYLON_FRAMEWORK_PATH "/Library/Frameworks")
    endif()
    
    set(FRAMEWORK_SOURCE "${PYLON_FRAMEWORK_PATH}/pylon.framework")
    
    if(EXISTS "${FRAMEWORK_SOURCE}")
        message(STATUS "Copying pylon.framework from: ${FRAMEWORK_SOURCE}")
        
        # Copy the entire framework, excluding headers, CMake files, and Tools
        install(DIRECTORY "${FRAMEWORK_SOURCE}"
                DESTINATION pypylon
                USE_SOURCE_PERMISSIONS
                PATTERN "*.h" EXCLUDE
                PATTERN "Headers" EXCLUDE
                PATTERN "CMake" EXCLUDE
                PATTERN "Tools" EXCLUDE
        )
        
        # Patch pylon-libusb for macOS 14+ compatibility
        # This uses LIEF (which is in build-requires for macOS) to adjust the minimum OS version
        message(STATUS "Installing post-install script to patch pylon-libusb for macOS 14+")
        install(CODE "
            message(STATUS \"Patching pylon.framework for macOS 14+ compatibility...\")
            execute_process(
                COMMAND ${Python_EXECUTABLE} ${CMAKE_SOURCE_DIR}/cmake/patch_macos_framework.py 
                        \${CMAKE_INSTALL_PREFIX}/pypylon/pylon.framework
                RESULT_VARIABLE PATCH_RESULT
                OUTPUT_VARIABLE PATCH_OUTPUT
                ERROR_VARIABLE PATCH_ERROR
            )
            if(NOT PATCH_RESULT EQUAL 0)
                message(WARNING \"pylon.framework patching failed (this is non-fatal):\")
                message(WARNING \"  \${PATCH_OUTPUT}\")
                message(WARNING \"  \${PATCH_ERROR}\")
            else()
                message(STATUS \"Successfully patched pylon.framework\")
            endif()
        ")
        
        # Optionally copy data processing framework if found
        set(DP_FRAMEWORK_SOURCE "${PYLON_FRAMEWORK_PATH}/pylondataprocessing.framework")
        if(PYLON_DATA_PROCESSING_FOUND AND EXISTS "${DP_FRAMEWORK_SOURCE}")
            message(STATUS "Copying pylondataprocessing.framework from: ${DP_FRAMEWORK_SOURCE}")
            install(DIRECTORY "${DP_FRAMEWORK_SOURCE}"
                    DESTINATION pypylon
                    USE_SOURCE_PERMISSIONS
                    PATTERN "*.h" EXCLUDE
                    PATTERN "Headers" EXCLUDE
                    PATTERN "CMake" EXCLUDE
                    PATTERN "Tools" EXCLUDE
            )
        endif()
    else()
        message(FATAL_ERROR "pylon.framework not found at: ${FRAMEWORK_SOURCE}")
    endif()
    
endif()

message(STATUS "Runtime dependencies copying configured") 
