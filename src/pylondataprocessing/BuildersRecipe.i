%rename(BuildersRecipe) Pylon::DataProcessing::CBuildersRecipe;

%ignore GetAvailableVToolTypeIDs;
%rename(GetAvailableVToolTypeIDs) GetAvailableVToolTypeIDs2;
%ignore GetVToolIdentifiers;
%rename(GetVToolIdentifiers) GetVToolIdentifiers2;
%ignore GetInputNames;
%rename(GetInputNames) GetInputNames2;
%ignore GetConnectionIdentifiers;
%rename(GetConnectionIdentifiers) GetConnectionIdentifiers2;

%include <pylondataprocessing/BuildersRecipe.h>;

%extend Pylon::DataProcessing::CBuildersRecipe {

    void GetAvailableVToolTypeIDs2(StringList_t& result) const
    {
        $self->GetAvailableVToolTypeIDs(result);
    }
    void GetVToolIdentifiers2(StringList_t& result) const
    {
        $self->GetVToolIdentifiers(result);
    }
    void GetInputNames2(StringList_t& result) const
    {
        $self->GetInputNames(result);
    }

    void GetConnectionIdentifiers2(StringList_t& result) const
    {
        $self->GetConnectionIdentifiers(result);
    }
}
