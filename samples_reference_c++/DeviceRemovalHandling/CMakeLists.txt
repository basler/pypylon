add_executable( DeviceRemovalHandling DeviceRemovalHandling.cpp)
target_link_libraries( DeviceRemovalHandling PRIVATE pylon::pylon )
install( TARGETS DeviceRemovalHandling )
