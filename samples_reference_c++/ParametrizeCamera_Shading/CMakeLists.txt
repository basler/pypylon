add_executable( ParametrizeCamera_Shading ParametrizeCamera_Shading.cpp)
target_link_libraries( ParametrizeCamera_Shading PRIVATE pylon::pylon )
install( TARGETS ParametrizeCamera_Shading )