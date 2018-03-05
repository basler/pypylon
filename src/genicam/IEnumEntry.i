%ignore CEnumEntryRef;
%nodefaultdtor GENAPI_NAMESPACE::IEnumEntry;
%include <GenApi/IEnumEntry.h>;
%extend GENAPI_NAMESPACE::IEnumEntry {
    PROP_GET(Value)
    PROP_GET(Symbolic)
    PROP_GET(NumericValue)
    %pythoncode %{
        def __call__( self ):
            return self.GetValue()
    %}
}
