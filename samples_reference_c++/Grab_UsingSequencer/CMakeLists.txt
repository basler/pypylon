add_executable( Grab_UsingSequencer Grab_UsingSequencer.cpp)
target_link_libraries( Grab_UsingSequencer PRIVATE pylon::pylon )
install( TARGETS Grab_UsingSequencer )