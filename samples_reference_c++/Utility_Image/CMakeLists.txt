add_executable( Utility_Image Utility_Image.cpp)
target_link_libraries( Utility_Image PRIVATE pylon::pylon )
install( TARGETS Utility_Image )
