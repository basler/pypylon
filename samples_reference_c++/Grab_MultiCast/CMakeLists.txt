add_executable( Grab_MultiCast Grab_MultiCast.cpp)
target_link_libraries( Grab_MultiCast PRIVATE pylon::pylon )
install( TARGETS Grab_MultiCast )