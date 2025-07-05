add_executable( Utility_IpConfig Utility_IpConfig.cpp)
target_link_libraries( Utility_IpConfig PRIVATE pylon::pylon )
install( TARGETS Utility_IpConfig )