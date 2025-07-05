add_executable( Utility_FFC Utility_FFC.cpp)
target_link_libraries( Utility_FFC PRIVATE pylon::pylon )
install( TARGETS Utility_FFC )
