%rename (ChunkAdapterGEV) GENAPI_NAMESPACE::CChunkAdapterGEV;
%include <GenApi/ChunkAdapterGEV.h>
%pythoncode %{
    CChunkAdapterGEV = ChunkAdapterGEV
%}