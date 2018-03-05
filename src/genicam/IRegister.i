
%nodefaultdtor GENAPI_NAMESPACE::IRegister;
%extend GENAPI_NAMESPACE::IRegister {
    PROP_GET(Length)
    PROP_GET(Address)
};

#define DOXYGEN_IGNORE
%include <GenApi/IRegister.h>;
%pythoncode %{
    def GetAll(self):
        return self.Get(self.GetLength())
    IRegister.GetAll = GetAll
%}
