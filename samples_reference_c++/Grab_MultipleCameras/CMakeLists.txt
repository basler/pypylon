add_executable( Grab_MultipleCameras Grab_MultipleCameras.cpp)
target_link_libraries( Grab_MultipleCameras PRIVATE pylon::pylon )
install( TARGETS Grab_MultipleCameras )