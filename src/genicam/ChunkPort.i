%rename (ChunkPort) GENAPI_NAMESPACE::CChunkPort;
%include <GenApi/ChunkPort.h>
%pythoncode %{
    CChunkPort = ChunkPort
%}
%extend GENAPI_NAMESPACE::CChunkPort{
        PROP_GET(AccessMode)
        PROP_GET(PrincipalInterfaceType)
}