add_executable( Utility_GrabVideo Utility_GrabVideo.cpp)
target_link_libraries( Utility_GrabVideo PRIVATE pylon::pylon )
install( TARGETS Utility_GrabVideo )