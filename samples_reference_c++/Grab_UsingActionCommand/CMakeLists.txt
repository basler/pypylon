add_executable( Grab_UsingActionCommand Grab_UsingActionCommand.cpp)
target_link_libraries( Grab_UsingActionCommand PRIVATE pylon::pylon )
install( TARGETS Grab_UsingActionCommand )