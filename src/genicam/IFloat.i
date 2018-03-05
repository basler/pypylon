#define DOXYGEN_IGNORE
%nodefaultdtor GENAPI_NAMESPACE::IFloat;
namespace GENAPI_NAMESPACE {
    class IInteger;
	class IEnumeration;
}
%extend GENAPI_NAMESPACE::IFloat {
    //! gets the interface of an integer alias node.
    IInteger *GetIntAlias()
    {
        IInteger *p_int;
        p_int = dynamic_cast<IInteger*>($self->GetNode()->GetCastAlias());
        if (NULL == p_int)
            throw LOGICAL_ERROR_EXCEPTION( "Float node as no Int alias" );
        return p_int;
    }

    //! gets the interface of an enum alias node.
    IEnumeration *GetEnumAlias()
    {
        IEnumeration *p_enum;
        p_enum = dynamic_cast<IEnumeration*>($self->GetNode()->GetCastAlias());
        if (NULL == p_enum)
            throw LOGICAL_ERROR_EXCEPTION( "Float node as no Enum alias" );
        return p_enum;
    }
    PROP_GETSET(Value)
    PROP_GET(Min)
    PROP_GET(Max)
    PROP_GET(IncMode);
    PROP_GET(Inc)
    PROP_GET(ListOfValidValues)
    PROP_GET(Representation)
    PROP_GET(Unit)
    PROP_GET(DisplayNotation)
    PROP_GET(DisplayPrecision)
    PROP_GET(IntAlias)
    PROP_GET(EnumAlias)
}
%ignore GENAPI_NAMESPACE::IFloat::operator*();
%include <GenApi/IFloat.h>;