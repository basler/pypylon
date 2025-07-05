cmake_minimum_required(VERSION 3.12)

add_executable(OCRRecipeSample
  main.cpp
  ocr.precipe
)

get_filename_component(PYLON_DATAPROCESSING_OCR_IMAGES_PATH
  "${CMAKE_CURRENT_SOURCE_DIR}/../images/ocr" ABSOLUTE
)
get_filename_component(PYLON_DATAPROCESSING_OCR_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/ocr.precipe" ABSOLUTE
)

target_compile_definitions(OCRRecipeSample
  PRIVATE
    PYLON_DATAPROCESSING_OCR_RECIPE="${PYLON_DATAPROCESSING_OCR_RECIPE}"
    PYLON_DATAPROCESSING_OCR_IMAGES_PATH="${PYLON_DATAPROCESSING_OCR_IMAGES_PATH}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(OCRRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET OCRRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET OCRRecipeSample PROPERTY CXX_STANDARD 11)