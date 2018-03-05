%ignore INode;
%nodefaultdtor GENAPI_NAMESPACE::ICategory;
namespace GENAPI_NAMESPACE {
    typedef value_vector FeatureList_t;
};
%extend GENAPI_NAMESPACE::ICategory{
    PROP_GET(Features)
};
#define DOXYGEN_IGNORE
%include <GenApi/ICategory.h>;
#undef DOXYGEN_IGNORE

