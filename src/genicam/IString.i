%nodefaultdtor GENAPI_NAMESPACE::IString;
%extend GENAPI_NAMESPACE::IString {
    //! gets the length of string if it is a stringreg.
    //! Retrieves the Length of the register [Bytes]
    virtual int64_t GetLength()
    {
        IRegister *p_reg;
        p_reg = dynamic_cast<IRegister*>($self);
        if (NULL == p_reg)
            throw LOGICAL_ERROR_EXCEPTION( "Pure string has no Length" );
        return p_reg->GetLength();
    };
    PROP_GETSET(Value)
    PROP_GET(MaxLength)
    PROP_GET(Length)
};
%ignore GENAPI_NAMESPACE::IString::operator*();
#define DOXYGEN_IGNORE
%include <GenApi/IString.h>;
