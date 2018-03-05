%nodefaultdtor GENAPI_NAMESPACE::IPort;
%extend GENAPI_NAMESPACE::IPort {
            virtual void Read(int64_t Address, void *pBuffer, int64_t Length){
                $self->Read(  pBuffer, Address,Length);
            };

            virtual void Write(int64_t Address, const void *pBuffer, int64_t Length){
                $self->Write( pBuffer, Address,Length);
            };

            virtual GENAPI_NAMESPACE::INode* GetNode() { return dynamic_cast<GENAPI_NAMESPACE::INode*>($self); };

			//! Get the Id of the chunk the port should be attached to
			virtual GENICAM_NAMESPACE::gcstring GetChunkID() const {
				return dynamic_cast<const GENAPI_NAMESPACE::IChunkPort*>($self)->GetChunkID();
			};

			virtual EYesNo CacheChunkData() const {
				return dynamic_cast<const GENAPI_NAMESPACE::IChunkPort*>($self)->CacheChunkData();
			};

			//! Determines if the port adapter must perform an endianess swap
			virtual EYesNo GetSwapEndianess() {
				return dynamic_cast<GENAPI_NAMESPACE::IPortConstruct*>($self)->GetSwapEndianess();
			};

            PROP_GET(Node);
            PROP_GET(ChunkID);

        };

%ignore GENAPI_NAMESPACE::IPort::Read(void *, int64_t, int64_t);
%ignore GENAPI_NAMESPACE::IPort::Write(const void *, int64_t, int64_t);

%include <GenApi/IPort.h>

