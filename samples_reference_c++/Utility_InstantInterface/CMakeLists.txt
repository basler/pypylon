add_executable( Utility_InstantInterface Utility_InstantInterface.cpp)
target_link_libraries( Utility_InstantInterface PRIVATE pylon::pylon )
install( TARGETS Utility_InstantInterface )