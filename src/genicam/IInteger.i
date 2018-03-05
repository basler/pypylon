#define DOXYGEN_IGNORE
%nodefaultdtor GENAPI_NAMESPACE::IInteger;
%ignore GENAPI_NAMESPACE::IInteger::operator*();
%extend GENAPI_NAMESPACE::IInteger {
    //! gets the interface of an integer alias node.
    IFloat *GetFloatAlias()
    {
        IFloat *p_float;
        p_float = dynamic_cast<IFloat*>($self->GetNode()->GetCastAlias());
        if (NULL == p_float)
            throw LOGICAL_ERROR_EXCEPTION( "Int node as no Float alias" );
        return p_float;
    };

    //! Set the register's contents
    /*!
    \param pBuffer The buffer containing the data to set
    \param Length The number of bytes in pBuffer
    \param Verify Enables AccessMode and Range verification (default = true)
    */
    virtual void Set(const uint8_t *pBuffer, int64_t Length, bool Verify = true){
        IRegister *p_reg;
        p_reg = dynamic_cast<IRegister*>($self);
        if (NULL == p_reg)
            throw LOGICAL_ERROR_EXCEPTION( "Pure Integer has no Set" );
        p_reg->Set(pBuffer, Length, Verify);
    };

    //! Fills a buffer with the register's contents
    /*!
    \param pBuffer The buffer receiving the data to read
    \param Length The number of bytes to retrieve
    \param Verify Enables Range verification (default = false). The AccessMode is always checked
    \param IgnoreCache If true the value is read ignoring any caches (default = false)
    */
    virtual void Get(uint8_t *pBuffer, int64_t Length, bool Verify = false, bool IgnoreCache = false){
        IRegister *p_reg;
        p_reg = dynamic_cast<IRegister*>($self);
        if (NULL == p_reg)
            throw LOGICAL_ERROR_EXCEPTION( "Pure Integer has no Set" );
        p_reg->Get(pBuffer, Length, Verify, IgnoreCache);
    };

    //! Retrieves the Length of the register [Bytes]
    virtual int64_t GetLength(){
        IRegister *p_reg;
        p_reg = dynamic_cast<IRegister*>($self);
        if (NULL == p_reg)
            throw LOGICAL_ERROR_EXCEPTION( "Pure Integer has no Set" );
        return p_reg->GetLength();
    };

    //! Retrieves the Address of the register
    virtual int64_t GetAddress(){
        IRegister *p_reg;
        p_reg = dynamic_cast<IRegister*>($self);
        if (NULL == p_reg)
            throw LOGICAL_ERROR_EXCEPTION( "Pure Integer has no Set" );
        return p_reg->GetAddress();
    };

    PROP_GETSET(Value)
    PROP_GET(Min)
    PROP_GET(Max)
    PROP_GET(IncMode)
    PROP_GET(Inc)
    PROP_GET(ListOfValidValues)
    PROP_GET(Representation)
    PROP_GET(Unit)
    PROP_GET(FloatAlias)
    PROP_GET(Address)
    PROP_GET(Length)

} // extend
%include <GenApi/IInteger.h>;