%rename (ChunkAdapter) GENAPI_NAMESPACE::CChunkAdapter;
%include <GenApi/ChunkAdapter.h>
%pythoncode %{
    CChunkAdapter = ChunkAdapter
%}