///-----------------------------------------------------------------------------
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

%nodefaultdtor GENAPI_NAMESPACE::INode;
namespace GENAPI_NAMESPACE
{

    //! a list of node references
    typedef node_vector NodeList_t;

    //! the callback handle for nodes
    typedef intptr_t CallbackHandleType;
    
    %nodefaultctor INodeMap;
	class INodeMap;
	
    //*************************************************************
    // INode interface
    //*************************************************************

    /**
    \brief Interface common to all nodes
    \ingroup GenApi_PublicInterface
    */
    class INode  : virtual public IBase
    {	
	public:
        //! Get node name
        virtual GENICAM_NAMESPACE::gcstring GetName(bool FullQualified=false) const =  0;
        PROP_GET(Name)

        //! Get name space
        virtual GENAPI_NAMESPACE::ENameSpace GetNameSpace() const =  0;
        PROP_GET(NameSpace)

        //! Get the recommended visibility of the node
        virtual EVisibility GetVisibility() const  = 0;
        PROP_GET(Visibility)

        //! Indicates that the node's value may have changed.
        /*! Fires the callback on this and all dependent nodes */
        virtual void InvalidateNode() = 0;

        //! Is the node value cachable
        virtual bool IsCachable() const =  0;

        //! True if the AccessMode can be cached
        virtual EYesNo IsAccessModeCacheable() const = 0;

        //! Get Caching Mode
        virtual ECachingMode GetCachingMode() const = 0;
        PROP_GET(CachingMode)

        //! recommended polling time (for not cachable nodes)
        virtual int64_t GetPollingTime() const = 0;
        PROP_GET(PollingTime)

        //! Get a short description of the node
        virtual GENICAM_NAMESPACE::gcstring GetToolTip() const = 0;
        PROP_GET(ToolTip)

        //! Get a long description of the node
        virtual GENICAM_NAMESPACE::gcstring GetDescription() const = 0;
        PROP_GET(Description)

        //! Get a name string for display
        virtual GENICAM_NAMESPACE::gcstring GetDisplayName() const = 0;
        PROP_GET(DisplayName)

        //! Get a name of the device
        virtual GENICAM_NAMESPACE::gcstring GetDeviceName() const = 0;
        PROP_GET(DeviceName)

        /*!
        \brief Get all nodes this node directly depends on.
        \param[out] Children List of children nodes
        \param LinkType The link type
        */
        virtual void GetChildren(GENAPI_NAMESPACE::NodeList_t &Children, ELinkType LinkType=ctReadingChildren) const =  0;
	PROP_GET(Children)

        /*!
        \brief Gets all nodes this node is directly depending on
        \param[out] Parents List of parent nodes
        */
        virtual void GetParents(GENAPI_NAMESPACE::NodeList_t &Parents) const = 0;
	PROP_GET(Parents)

        //! Register change callback
        /*! Takes ownership of the CNodeCallback object */
        virtual CallbackHandleType RegisterCallback( CNodeCallback *INPUT ) = 0;

        //! De register change callback
        /*! Destroys CNodeCallback object
        \return true if the callback handle was valid
        */
        virtual bool DeregisterCallback( CallbackHandleType hCallback ) = 0;

        //! Retrieves the central node map
        virtual INodeMap* GetNodeMap() const = 0;
	PROP_GET(NodeMap)

        //! Get the EventId of the node
        virtual GENICAM_NAMESPACE::gcstring GetEventID() const =  0;
	PROP_GET(EventID)

        //! True if the node is streamable
        virtual bool IsStreamable() const =  0;

        //! Returns a list of the names all properties set during initialization
        virtual void GetPropertyNames(StringList_t &PropertyNames) const =  0;
	PROP_GET(PropertyNames)

        
	%extend {
        //! Retrieves a property plus an additional attribute by name
        /*! If a property has multiple values/attribute they come with Tabs as delimiters */
        virtual void GetProperty(const GENICAM_NAMESPACE::gcstring& PropertyName, GENICAM_NAMESPACE::gcstring& ValueStr, GENICAM_NAMESPACE::gcstring& AttributeStr) 
		{
            bool result = $self->GetProperty(PropertyName, ValueStr, AttributeStr);
            if (!result)
                throw LOGICAL_ERROR_EXCEPTION( "property does not exit" );
        };
		}
        //! Imposes an access mode to the natural access mode of the node
        virtual void ImposeAccessMode(EAccessMode ImposedAccessMode) =  0;

        //! Imposes a visibility  to the natural visibility of the node
        virtual void ImposeVisibility(EVisibility ImposedVisibility) =  0;

        //! Retrieves the a node which describes the same feature in a different way
        virtual INode* GetAlias() const = 0;
	PROP_GET(Alias)

        //! Retrieves the a node which describes the same feature so that it can be casted
        virtual INode* GetCastAlias() const = 0;
	PROP_GET(CastAlias)

        //! Gets a URL pointing to the documentation of that feature
        virtual GENICAM_NAMESPACE::gcstring GetDocuURL() const =  0;
	PROP_GET(DocuURL)

        //! True if the node should not be used any more
        virtual bool IsDeprecated() const =  0;

        //! Get the type of the main interface of a node
        virtual EInterfaceType GetPrincipalInterfaceType() const = 0;
	PROP_GET(PrincipalInterfaceType)

	
        //! True if the node can be reached via category nodes from a category node named "Root"
        virtual bool IsFeature() const =  0;

	%extend{
        //! true iff this feature selects a group of features
        virtual bool IsSelector() const {
				return dynamic_cast<const ISelector*>($self)->IsSelector();
		}

        //! retrieve the group of selected features
        virtual void GetSelectedFeatures( GENAPI_NAMESPACE::FeatureList_t& thelist) const{
				return dynamic_cast<const ISelector*>($self)->GetSelectedFeatures( thelist);
		}

        //! retrieve the group of features selecting this node
        virtual void GetSelectingFeatures( GENAPI_NAMESPACE::FeatureList_t& thelist) const {
				return dynamic_cast<const ISelector*>($self)->GetSelectingFeatures( thelist);
		}
		}


    };

    //! Tests if readable
    inline bool IsReadable( EAccessMode AccessMode );

    //! Checks if a node is readable
    inline bool IsReadable( const IBase* p);

    //! Tests if writable
    inline bool IsWritable( EAccessMode AccessMode );

    //! Checks if a node is writable
    inline bool IsWritable( const IBase* p);

    //! Tests if implemented
    inline bool IsImplemented( EAccessMode AccessMode );

    //! Checks if a node is implemented
    inline bool IsImplemented( const IBase* p);

    //! Tests if available
    inline bool IsAvailable( EAccessMode AccessMode );

    //! Checks if a node is available
    inline bool IsAvailable( const IBase* p);
    
    //! Computes which access mode the two guards allow together
    inline EAccessMode Combine(EAccessMode Peter, EAccessMode Paul);

    //! Tests Visibility
    /*! CAVE : this relys on the EVisibility enum's coding */
    inline bool IsVisible( EVisibility Visibility, EVisibility MaxVisiblity );


    //! Computes which visibility the two guards allow together
    %rename(CombineVisibility) Combine(EVisibility Peter, EVisibility Paul);
    inline EVisibility Combine(EVisibility Peter, EVisibility Paul);

    //! Tests Cacheability
    inline bool IsCacheable( ECachingMode CachingMode );

    //! Computes which CachingMode results from a combination
    %rename(CombineCachingMode) Combine(ECachingMode Peter, ECachingMode Paul);
    inline ECachingMode Combine(ECachingMode Peter, ECachingMode Paul);

    
	
    
}

