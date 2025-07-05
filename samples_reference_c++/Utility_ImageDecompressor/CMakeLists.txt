add_executable( Utility_ImageDecompressor Utility_ImageDecompressor.cpp)
target_link_libraries( Utility_ImageDecompressor PRIVATE pylon::pylon )
install( TARGETS Utility_ImageDecompressor )