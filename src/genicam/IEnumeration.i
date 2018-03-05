
%ignore GENAPI_NAMESPACE::IEnumeration::operator*();
%nodefaultdtor GENAPI_NAMESPACE::IEnumeration;

%extend GENAPI_NAMESPACE::IEnumeration {
    virtual GENICAM_NAMESPACE::gcstring operator()(){
        return $self->GetCurrentEntry()->GetSymbolic();
    }

    virtual GENICAM_NAMESPACE::gcstring GetValue(){
        return $self->GetCurrentEntry()->GetSymbolic();
    }

    virtual void SetValue( GENICAM_NAMESPACE::gcstring entry ){
        $self->FromString(entry);
    }
};


%extend GENAPI_NAMESPACE::IEnumeration {
    PROP_GET(Symbolics)
    PROP_GET(Entries)
    PROP_GETSET(IntValue)
    PROP_GETSET(Value)
};

%include <GenApi/IEnumeration.h>;
