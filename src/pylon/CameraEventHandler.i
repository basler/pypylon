%rename(CameraEventHandler) Pylon::CCameraEventHandler;
%rename(InstantCamera) Pylon::CInstantCamera;

%feature("director") Pylon::CCameraEventHandler;

%typemap(directorin) Pylon::String_t const &nodeName{
    $input = PyUnicode_FromStringAndSize($1.c_str(),$1.length());
}

%typemap(directorin) GENAPI_NAMESPACE::INode* pNode {
         swig_type_info *outtype = 0;
         void * outptr = 0;
         switch ($1->GetPrincipalInterfaceType()){
             case GENAPI_NAMESPACE::intfIValue :
                        outtype = $descriptor(GENAPI_NAMESPACE::IValue*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IValue*>($1);
                        break;
             case GENAPI_NAMESPACE::intfIInteger :
                        outtype = $descriptor(GENAPI_NAMESPACE::IInteger*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IInteger*>($1);
                         break;
              case GENAPI_NAMESPACE::intfIBoolean :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBoolean*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBoolean*>($1);
                         break;
             case GENAPI_NAMESPACE::intfICommand :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICommand*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICommand*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIFloat :
                        outtype = $descriptor(GENAPI_NAMESPACE::IFloat*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IFloat*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIString :
                        outtype = $descriptor(GENAPI_NAMESPACE::IString*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IString*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIRegister :
                        outtype = $descriptor(GENAPI_NAMESPACE::IRegister*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IRegister*>($1);
                         break;
             case GENAPI_NAMESPACE::intfICategory :
                        outtype = $descriptor(GENAPI_NAMESPACE::ICategory*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::ICategory*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIEnumeration :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumeration*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumeration*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIEnumEntry :
                        outtype = $descriptor(GENAPI_NAMESPACE::IEnumEntry*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IEnumEntry*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIPort :
                        outtype = $descriptor(GENAPI_NAMESPACE::IPort*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IPort*>($1);
                         break;
             case GENAPI_NAMESPACE::intfIBase :
                        outtype = $descriptor(GENAPI_NAMESPACE::IBase*);
                        outptr  = dynamic_cast<GENAPI_NAMESPACE::IBase*>($1);
                         break;
          };
    $input = SWIG_NewPointerObj(outptr, outtype, $owner);
}

%ignore Pylon::CCameraEventHandler::DebugGetEventHandlerRegistrationCount;
%include <pylon/CameraEventHandler.h>