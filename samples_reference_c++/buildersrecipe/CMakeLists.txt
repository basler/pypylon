cmake_minimum_required(VERSION 3.12)

add_executable(BuildersRecipeSample
  main.cpp
)

target_link_libraries(BuildersRecipeSample
  PRIVATE
    pylon
    pylon::DataProcessing
)

set_target_properties(BuildersRecipeSample PROPERTIES
  BUILD_RPATH "@executable_path/../../../Frameworks"
  INSTALL_RPATH "$@executable_path/../../../Frameworks"
)

set_property(TARGET BuildersRecipeSample
  APPEND PROPERTY COMPILE_OPTIONS
    $<$<CXX_COMPILER_ID:MSVC>:/WX>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -pedantic -Werror>
)

set_property(TARGET BuildersRecipeSample PROPERTY CXX_STANDARD 11)