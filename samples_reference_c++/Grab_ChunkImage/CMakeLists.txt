add_executable( Grab_ChunkImage Grab_ChunkImage.cpp)
target_link_libraries( Grab_ChunkImage PRIVATE pylon::pylon )
install( TARGETS Grab_ChunkImage )
