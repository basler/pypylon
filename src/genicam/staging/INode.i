%nodefaultdtor GENAPI_NAMESPACE::INode;
%nodefaultctor GENAPI_NAMESPACE::INodeMap;
%rename(CombineVisibility) Combine(EVisibility Peter, EVisibility Paul);
%rename(CombineCachingMode) Combine(ECachingMode Peter, ECachingMode Paul);
%extend GENAPI_NAMESPACE::INode {

    //! Retrieves a property plus an additional attribute by name
    /*! If a property has multiple values/attribute they come with Tabs as delimiters */
    virtual void GetProperty(const GENICAM_NAMESPACE::gcstring& PropertyName, GENICAM_NAMESPACE::gcstring& ValueStr, GENICAM_NAMESPACE::gcstring& AttributeStr)
    {
        bool result = $self->GetProperty(PropertyName, ValueStr, AttributeStr);
        if (!result)
            throw LOGICAL_ERROR_EXCEPTION( "property does not exit" );
    };

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

    virtual CallbackHandleType RegisterCallback( CNodeCallback *INPUT ) = 0;

    PROP_GET(Name)
    PROP_GET(NameSpace)
    PROP_GET(Visibility)
    PROP_GET(CachingMode)
    PROP_GET(PollingTime)
    PROP_GET(ToolTip)
    PROP_GET(Description)
    PROP_GET(DisplayName)
    PROP_GET(DeviceName)
    PROP_GET(Children)
    PROP_GET(Parents)
    PROP_GET(NodeMap)
    PROP_GET(EventID)
    PROP_GET(PropertyNames)
    PROP_GET(Alias)
    PROP_GET(CastAlias)
    PROP_GET(DocuURL)
    PROP_GET(PrincipalInterfaceType)

}
%ignore GENAPI_NAMESPACE::INode::GetProperty(const GENICAM_NAMESPACE::gcstring& PropertyName, GENICAM_NAMESPACE::gcstring& ValueStr, GENICAM_NAMESPACE::gcstring& AttributeStr);

%ignore CNodeCallback;
%ignore RegisterCallback( CNodeCallback *pCallback );
#define pCallback INPUT

%include <GenApi/INode.h>;

