cmake_minimum_required(VERSION 3.12)

add_executable(BarcodeRecipeSample
  main.cpp
  barcode.precipe
)

get_filename_component(PYLON_DATAPROCESSING_IMAGES_PATH
  "${CMAKE_CURRENT_SOURCE_DIR}/../images/barcode" ABSOLUTE
)
get_filename_component(PYLON_DATAPROCESSING_BARCODE_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/barcode.precipe" ABSOLUTE
)

target_compile_definitions(BarcodeRecipeSample
  PRIVATE
    PYLON_DATAPROCESSING_BARCODE_RECIPE="${PYLON_DATAPROCESSING_BARCODE_RECIPE}"
    PYLON_DATAPROCESSING_IMAGES_PATH="${PYLON_DATAPROCESSING_IMAGES_PATH}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(BarcodeRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET BarcodeRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET BarcodeRecipeSample PROPERTY CXX_STANDARD 11)