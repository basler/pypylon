cmake_minimum_required(VERSION 3.12)

add_executable(CameraRecipeSample
  main.cpp
  camera.precipe
)

get_filename_component(PYLON_DATAPROCESSING_CAMERA_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/camera.precipe" ABSOLUTE
)

target_compile_definitions(CameraRecipeSample
  PRIVATE
    PYLON_DATAPROCESSING_CAMERA_RECIPE="${PYLON_DATAPROCESSING_CAMERA_RECIPE}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(CameraRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET CameraRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET CameraRecipeSample PROPERTY CXX_STANDARD 11)