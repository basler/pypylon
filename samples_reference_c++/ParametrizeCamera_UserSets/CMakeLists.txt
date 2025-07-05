add_executable( ParametrizeCamera_UserSets ParametrizeCamera_UserSets.cpp)
target_link_libraries( ParametrizeCamera_UserSets PRIVATE pylon::pylon )
install( TARGETS ParametrizeCamera_UserSets )