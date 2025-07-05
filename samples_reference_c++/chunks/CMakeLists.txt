cmake_minimum_required(VERSION 3.12)

add_executable(ChunksRecipeSample
  main.cpp
  chunks.precipe
)

get_filename_component(PYLON_DATAPROCESSING_CHUNKS_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/chunks.precipe" ABSOLUTE
)

target_compile_definitions(ChunksRecipeSample
  PRIVATE
    PYLON_DATAPROCESSING_CHUNKS_RECIPE="${PYLON_DATAPROCESSING_CHUNKS_RECIPE}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(ChunksRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET ChunksRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET ChunksRecipeSample PROPERTY CXX_STANDARD 11)