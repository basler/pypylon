%{
#include "PyPortImpl.h"
%}

%nodefaultdtor GENAPI_NAMESPACE::CPortImpl;
%nodefaultctor GENAPI_NAMESPACE::CPortImpl;

%warnfilter(403) GENAPI_NAMESPACE::CPortImpl;

%nodefaultdtor GENAPI_NAMESPACE::CPyPortImpl;
%feature("director") GENAPI_NAMESPACE::CPyPortImpl;

%rename(Read) GENAPI_NAMESPACE::CPyPortImpl::PyRead;
%rename(Write) GENAPI_NAMESPACE::CPyPortImpl::PyWrite;
%rename(CPortImpl) CPyPortImpl;


%ignore CPortImpl;
%include <GenApi/PortImpl.h>;
%include "PyPortImpl.h";

%extend GENAPI_NAMESPACE::CPyPortImpl {
    void InvalidateNode();
};


