cmake_minimum_required(VERSION 3.12)

add_executable(CompositeDataTypesSample
  main.cpp
        composite_data_types.precipe
)

get_filename_component(PYLON_DATAPROCESSING_SHAPE_IMAGES_PATH
  "${CMAKE_CURRENT_SOURCE_DIR}/../images/shapes" ABSOLUTE
)
get_filename_component(PYLON_DATAPROCESSING_COMPOSITE_DATA_TYPES_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/composite_data_types.precipe" ABSOLUTE
)

target_compile_definitions(CompositeDataTypesSample
  PRIVATE
    PYLON_DATAPROCESSING_COMPOSITE_DATA_TYPES_RECIPE="${PYLON_DATAPROCESSING_COMPOSITE_DATA_TYPES_RECIPE}"
    PYLON_DATAPROCESSING_SHAPE_IMAGES_PATH="${PYLON_DATAPROCESSING_SHAPE_IMAGES_PATH}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(CompositeDataTypesSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET CompositeDataTypesSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET CompositeDataTypesSample PROPERTY CXX_STANDARD 11)