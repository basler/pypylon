cmake_minimum_required(VERSION 3.12)

add_executable(RegionRecipeSample
  main.cpp
  region.precipe
)

get_filename_component(PYLON_DATAPROCESSING_REGION_RECIPE
  "${CMAKE_CURRENT_SOURCE_DIR}/region.precipe" ABSOLUTE
)

target_compile_definitions(RegionRecipeSample
  PRIVATE
    PYLON_DATAPROCESSING_REGION_RECIPE="${PYLON_DATAPROCESSING_REGION_RECIPE}"
    PYLON_DATAPROCESSING_NO_AUTO_IMPLIB
)

target_link_libraries(RegionRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_property(TARGET RegionRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET RegionRecipeSample PROPERTY CXX_STANDARD 11)