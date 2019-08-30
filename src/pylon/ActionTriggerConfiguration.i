%rename(ActionTriggerConfiguration) Pylon::CActionTriggerConfiguration;
%rename(InstantCamera) Pylon::CInstantCamera;

// SWIG does not understand code like this: 'const T var_name(init_value);'
// But it does understand: 'const T var_name = init_value;'
// In the case of 'const uint32_t AllGroupMask(0xffffffff);' we transform the
// former to the latter with this macro:
#define AllGroupMask(x) AllGroupMask=x

%include <pylon/gige/ActionTriggerConfiguration.h>
