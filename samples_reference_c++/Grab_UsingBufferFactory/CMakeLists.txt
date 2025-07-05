add_executable( Grab_UsingBufferFactory Grab_UsingBufferFactory.cpp)
target_link_libraries( Grab_UsingBufferFactory PRIVATE pylon::pylon )
install( TARGETS Grab_UsingBufferFactory )