add_executable( Utility_ImageLoadAndSave Utility_ImageLoadAndSave.cpp)
target_link_libraries( Utility_ImageLoadAndSave PRIVATE pylon::pylon )
install( TARGETS Utility_ImageLoadAndSave )
