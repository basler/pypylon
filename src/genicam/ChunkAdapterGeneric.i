%rename (ChunkAdapterGeneric) GENAPI_NAMESPACE::CChunkAdapterGeneric;
%include <GenApi/ChunkAdapterGeneric.h>
%pythoncode %{
    CChunkAdapterGeneric = ChunkAdapterGeneric
%}