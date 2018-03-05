%ignore CBaseRef;
//TODO Ask Thies why the destructor was left out
%ignore ~IBase;
#define DOXYGEN_IGNORE
%include <GenApi/IBase.h>;
#undef DOXYGEN_IGNORE