%nodefaultdtor GENAPI_NAMESPACE::IBoolean;
%ignore CBooleanRef;
%extend GENAPI_NAMESPACE::IBoolean {
    PROP_GETSET(Value)
}
%include <GenApi/IBoolean.h>;