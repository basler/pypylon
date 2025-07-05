add_executable( Grab_Strategies Grab_Strategies.cpp)
target_link_libraries( Grab_Strategies PRIVATE pylon::pylon )
install( TARGETS Grab_Strategies )