add_executable( Grab_UsingGrabLoopThread Grab_UsingGrabLoopThread.cpp)
target_link_libraries( Grab_UsingGrabLoopThread PRIVATE pylon::pylon )
install( TARGETS Grab_UsingGrabLoopThread )