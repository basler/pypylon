%rename(VariantContainer) Pylon::DataProcessing::CVariantContainer;
%rename(Variant) Pylon::DataProcessing::CVariant;

%ignore begin;
%ignore end;
%ignore find;
%ignore erase(const CVariantContainer::iterator& it);
%ignore operator[](const String_t& key);
%ignore operator++();
%ignore operator++(int);
%ignore keyvalue_pair;
%ignore iterator;
%ignore CVariantContainer(CVariantContainer &&);

%warnfilter(389) CVariantContainer;
%warnfilter(383) CVariantContainer;

%include <pylondataprocessing/VariantContainer.h>;

//The VariantContainer is usually mapped to and from a python dictionary. The following extension should not be needed.
%extend Pylon::DataProcessing::CVariantContainer {

    Pylon::DataProcessing::CVariant getValue(const Pylon::String_t& key)
    {
        Pylon::DataProcessing::CVariant v = $self->operator[](key);
		return v;
    }
	
	void setValue(const Pylon::String_t& key, Pylon::DataProcessing::CVariant& v)
    {
		$self->operator[](key) = v;
    }
}
