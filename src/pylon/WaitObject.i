
%ignore WaitObjectEx;

#ifdef _WIN32
#define PYLON_WIN_BUILD
%ignore Pylon::WaitObject::operator WaitObject_t() const;
#else
#define PYLON_UNIX_BUILD
#endif

%include <pylon/WaitObject.h>


