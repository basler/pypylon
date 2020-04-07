//-----------------------------------------------------------------------------
//  (c) 2012 by Basler Vision Technologies
//  Section: Vision Components
//  Project: GenApi
//  Author:  Thies Moeller
//  $Header$
//
//  License: This file is published under the license of the EMVA GenICam  Standard Group.
//  A text file describing the legal terms is included in  your installation as 'GenICam_license.pdf'.
//  If for some reason you are missing  this file please contact the EMVA or visit the website
//  (http://www.genicam.org) for a full copy.
//
//  THIS SOFTWARE IS PROVIDED BY THE EMVA GENICAM STANDARD GROUP "AS IS"
//  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE EMVA GENICAM STANDARD  GROUP
//  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,  SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT  LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,  DATA, OR PROFITS;
//  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY  THEORY OF LIABILITY,
//  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT  (INCLUDING NEGLIGENCE OR OTHERWISE)
//  ARISING IN ANY WAY OUT OF THE USE  OF THIS SOFTWARE, EVEN IF ADVISED OF THE
//  POSSIBILITY OF SUCH DAMAGE.
//-----------------------------------------------------------------------------



namespace GENAPI_NAMESPACE
{

	class IDeviceInfo;
    /**
    \brief Smartpointer for NodeMaps with create function
    \ingroup GenApi_PublicInterface
    */
    class CNodeMapRef 
    {
    public:
        //! Constructor
        CNodeMapRef(GENICAM_NAMESPACE::gcstring DeviceName = "Device" );

        //! Destructor
        virtual ~CNodeMapRef();

        //! Creates the object from a XML file with given file name
        void _LoadXMLFromFile(GENICAM_NAMESPACE::gcstring FileName);

        //! Creates the object from XML data given in a string
        void _LoadXMLFromString(const GENICAM_NAMESPACE::gcstring& XMLData);

        //! Get device name 
        virtual GENICAM_NAMESPACE::gcstring _GetDeviceName();
		
        //! Fires nodes which have a polling time
        virtual void _Poll( int64_t ElapsedTime );

        //! Destroys the node map
        void _Destroy();

        //! Clears the cache of the camera description files
        static bool _ClearXMLCache();

        //----------------------------------------------------------------
        // INodeMap
        //----------------------------------------------------------------

        //! Retrieves all nodes in the node map
        virtual void _GetNodes(NodeList_t &Nodes) const;

        //! Retrieves the node from the central map by name
        virtual INode* _GetNode( const GENICAM_NAMESPACE::gcstring& key) const;

		%extend {
        virtual INode* GetNode( const GENICAM_NAMESPACE::gcstring& key) const{
			return $self->_GetNode(key);
		};
		};

        //! Invalidates all nodes
        virtual void _InvalidateNodes() const;

        //! Connects a port to a port node with given name
        virtual bool _Connect( IPort* pPort, const GENICAM_NAMESPACE::gcstring& PortName) const;

        //! Connects a port to the standard port "Device"
        virtual bool _Connect( IPort* pPort) const;

        //! Pointer to the NodeMap
        INodeMap *_Ptr;

        %extend {
        //! gets the interface of IDeviceInfo.
        IDeviceInfo *GetDeviceInfo()
        {   
            IDeviceInfo *p_di;
            p_di = dynamic_cast<IDeviceInfo*>($self->_Ptr);
            if (NULL == p_di)
                throw LOGICAL_ERROR_EXCEPTION( "Nodemap has no deviceinfo" );
            return p_di;
        };
        };

        PROP_GET(DeviceInfo)

        %pythoncode %{
        def __getattr__(self, attribute):
            if attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
                return object.__getattr__(self, attribute)
            else:
                return self.GetNode(attribute)

        def __setattr__(self, attribute, val):
            if attribute in self.__dict__ or attribute in ( "thisown","this") or attribute.startswith("__"):
                object.__setattr__(self, attribute, val)
            else:
                self.GetNode(attribute).SetValue(val)

        def __dir__(self):
            l = []
            l += [x for x in dir(type(self))]
            l += [x for x in self.__dict__.keys()]
            try:
                l += [x.GetNode().GetName() for x in filter(lambda n: n.GetNode().IsFeature(), self.GetNodeMap().GetNodes())]
            except:
                pass
            return sorted(set(l))
        %}


    };
}

