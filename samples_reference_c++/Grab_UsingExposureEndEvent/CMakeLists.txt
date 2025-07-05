add_executable( Grab_UsingExposureEndEvent Grab_UsingExposureEndEvent.cpp)
target_link_libraries( Grab_UsingExposureEndEvent PRIVATE pylon::pylon )
install( TARGETS Grab_UsingExposureEndEvent )