%rename (GigETransportLayer) Pylon::IGigETransportLayer;
%nodefaultdtor Pylon::IGigETransportLayer;

////////////////////////////////////////////////////////////////////////////////
//
// DeviceInfoList output for EnumerateAllDevices
//

%typemap(in, numinputs=0) (Pylon::DeviceInfoList_t&, bool addToList)
{
    $1 = new Pylon::DeviceInfoList_t();
    $2 = false;
}

%typemap(argout, fragment="t_output_helper") Pylon::DeviceInfoList_t&
{
  Py_DECREF($result);
  PyObject *tpl = PyTuple_New($1->size());
  for (unsigned int i = 0; i < $1->size(); i++) {
    CDeviceInfo *di = new CDeviceInfo((*$1)[i]);
    PyObject *item = SWIG_NewPointerObj(
        SWIG_as_voidptr(di),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, i, item);
  }
  $result = tpl;
  delete $1;
}

// ensure the above typemap will not be applied to const references
%typemap(argout, noblock=1) const Pylon::DeviceInfoList_t & {}

////////////////////////////////////////////////////////////////////////////////
//
// CDeviceInfo output for AnnounceRemoteDevice
//

%typemap(in, numinputs=0) Pylon::CDeviceInfo*
{
    $1 = new Pylon::CDeviceInfo();
}

%typemap(argout) Pylon::CDeviceInfo*
{
    Py_DECREF($result);
    PyObject *tpl = PyTuple_New(2);
    PyTuple_SetItem(tpl, 0, $result);
    PyObject *di = SWIG_NewPointerObj(
        SWIG_as_voidptr($1),
        SWIGTYPE_p_Pylon__CDeviceInfo,
        SWIG_POINTER_OWN
        );
    PyTuple_SetItem(tpl, 1, di);
    // do NOT delete $1, since 'di' took ownership of it
    $result = tpl;
}

////////////////////////////////////////////////////////////////////////////////

// Ignore original 'AnnounceRemoteDevice' and create an overload for it in
// order to get easier type mapping.

%ignore Pylon::IGigETransportLayer::AnnounceRemoteDevice(
    const String_t& IpAddress,
    CDeviceInfo* pInfo=NULL
    );

%extend Pylon::IGigETransportLayer {
    // Create an overload for 'AnnounceRemoteDevice' for easier type mapping.
    bool AnnounceRemoteDevice(CDeviceInfo* pInfo, const String_t& IpAddress)
    {
        return $self->AnnounceRemoteDevice(IpAddress, pInfo);
    }
}

////////////////////////////////////////////////////////////////////////////////

// We can ignore Pylon::GigEActionCommandResult since we are going to wrap
// it into a python tuple.
%ignore Pylon::GigEActionCommandResult;

// Ignore original 'IssueActionCommand' and create two new methods in
// order to get easier type mapping.

%ignore Pylon::IGigETransportLayer::IssueActionCommand(
    uint32_t deviceKey,
    uint32_t groupKey,
    uint32_t groupMask,
    const String_t &broadcastAddress = "255.255.255.255",
    uint32_t timeoutMs = 0,
    uint32_t *pNumResults = 0,
    GigEActionCommandResult results[] = NULL
    );

%extend Pylon::IGigETransportLayer {
    bool IssueActionCommandNoWait(
        uint32_t deviceKey,
        uint32_t groupKey,
        uint32_t groupMask,
        const String_t &broadcastAddress
        )
    {
        return $self->IssueActionCommand(
            deviceKey,
            groupKey,
            groupMask,
            broadcastAddress,
            0,
            NULL,
            NULL
            );
    }

    bool IssueActionCommandWait(
        uint32_t deviceKey,
        uint32_t groupKey,
        uint32_t groupMask,
        const String_t &broadcastAddress,
        uint32_t timeoutMs,
        uint32_t *pNumResults,
        GigEActionCommandResult *results
        )
    {
        return $self->IssueActionCommand(
            deviceKey,
            groupKey,
            groupMask,
            broadcastAddress,
            timeoutMs,
            pNumResults,
            results
            );
    }


    %pythoncode %{


    # Add a custom class that serves two purposes:
    # - Provide a simpler interface that the original 'IssueActionCommand'.
    # - Provide easier typemapping.

    class _ActionCommand:

        def __init__(
            self,
            gige_tl,
            deviceKey,
            groupKey,
            groupMask,
            broadcastAddress="255.255.255.255"
            ):
            self.gige_tl = gige_tl
            self.deviceKey = deviceKey
            self.groupKey = groupKey
            self.groupMask = groupMask
            self.broadcastAddress = broadcastAddress

        def IssueNoWait(self):
            return self.gige_tl.IssueActionCommandNoWait(
                self.deviceKey,
                self.groupKey,
                self.groupMask,
                self.broadcastAddress
                )

        def IssueWait(self, timeoutMs, expected_results):
            return self.gige_tl.IssueActionCommandWait(
                self.deviceKey,
                self.groupKey,
                self.groupMask,
                self.broadcastAddress,
                timeoutMs,
                expected_results
                )

    def ActionCommand(
        self,
        deviceKey,
        groupKey,
        groupMask,
        broadcastAddress="255.255.255.255"
        ):
        return self._ActionCommand(
            self,
            deviceKey,
            groupKey,
            groupMask,
            broadcastAddress
            )
    %}

}

////////////////////////////////////////////////////////////////////////////////
//
// GigEActionCommandResult output for IssueActionCommandWait and
// IssueScheduledActionCommandWait
//

%typemap(typecheck, precedence=SWIG_TYPECHECK_POINTER, numinputs=1)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results)
{
    $1 = PyInt_Check($input) ? 1 : 0;
}


%typemap(in, numinputs=1, noblock=1)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results)
{
    uint32_t num_res_u32;
    unsigned long num_res_ul;
    bool ok;
    ok  = SWIG_IsOK(SWIG_AsVal_unsigned_SS_long($input, &num_res_ul));
    num_res_u32 = static_cast<uint32_t>(num_res_ul);
    if (!ok)
    {
        PyErr_SetString(PyExc_ValueError, "Need an int in range(0, 2**32)");
        SWIG_fail;
    }
    $1 = &num_res_u32;
    $2 = new GigEActionCommandResult[num_res_u32];
}

%typemap(freearg, numinputs=1)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results)
{
    delete $2;
}


%typemap(argout, fragment="t_output_helper")
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results)
{
    uint32_t cnt = *$1;
    PyObject *cmd_res = PyTuple_New(cnt);
    for (uint32_t i = 0; i < cnt; i++)
    {
        PyObject *address = PyString_FromString($2[i].DeviceAddress);
        PyObject *status = PyInt_FromLong($2[i].Status);
        PyObject *sgl_res = PyTuple_New(2);
        PyTuple_SetItem(sgl_res, 0, address);
        PyTuple_SetItem(sgl_res, 1, status);
        PyTuple_SetItem(cmd_res, i, sgl_res);
    }

    PyObject *tpl = PyTuple_New(2);
    PyTuple_SetItem(tpl, 0, $result);
    PyTuple_SetItem(tpl, 1, cmd_res);
    $result = tpl;
}

////////////////////////////////////////////////////////////////////////////////

// Ignore original 'IssueScheduledActionCommand' and create two new methods in
// order to get easier type mapping.

%ignore Pylon::IGigETransportLayer::IssueScheduledActionCommand(
    uint32_t deviceKey,
    uint32_t groupKey,
    uint32_t groupMask,
    uint64_t actionTimeNs,
    const String_t &broadcastAddress = "255.255.255.255",
    uint32_t timeoutMs = 0,
    uint32_t *pNumResults = 0,
    GigEActionCommandResult results[] = NULL
    );

%extend Pylon::IGigETransportLayer {
    bool IssueScheduledActionCommandNoWait(
        uint32_t deviceKey,
        uint32_t groupKey,
        uint32_t groupMask,
        uint64_t actionTimeNs,
        const String_t &broadcastAddress
        )
    {
        return $self->IssueScheduledActionCommand(
            deviceKey,
            groupKey,
            groupMask,
            actionTimeNs,
            broadcastAddress,
            0,
            NULL,
            NULL
            );
    }

    bool IssueScheduledActionCommandWait(
        uint32_t deviceKey,
        uint32_t groupKey,
        uint32_t groupMask,
        uint64_t actionTimeNs,
        const String_t &broadcastAddress,
        uint32_t timeoutMs,
        uint32_t *pNumResults,
        GigEActionCommandResult *results
        )
    {
        return $self->IssueScheduledActionCommand(
            deviceKey,
            groupKey,
            groupMask,
            actionTimeNs,
            broadcastAddress,
            timeoutMs,
            pNumResults,
            results
            );
    }


    %pythoncode %{


    # Add a custom class that serves two purposes:
    # - Provide a simpler interface that the original 'IssueScheduledActionCommand'.
    # - Provide easier typemapping.

    class _ScheduledActionCommand:

        def __init__(
            self,
            gige_tl,
            deviceKey,
            groupKey,
            groupMask,
            actionTimeNs,
            broadcastAddress="255.255.255.255"
            ):
            self.gige_tl = gige_tl
            self.deviceKey = deviceKey
            self.groupKey = groupKey
            self.groupMask = groupMask
            self._actionTimeNs = actionTimeNs
            self.broadcastAddress = broadcastAddress

        # Provide access to actionTimeNs, so that an object can be reused
        # for different action times.

        @property
        def actionTimeNs(self):
            return self._actionTimeNs

        @actionTimeNs.setter
        def actionTimeNs(self, value):
            self._actionTimeNs = value

        def IssueNoWait(self):
            return self.gige_tl.IssueScheduledActionCommandNoWait(
                self.deviceKey,
                self.groupKey,
                self.groupMask,
                self._actionTimeNs,
                self.broadcastAddress
                )

        def IssueWait(self, timeoutMs, expected_results):
            return self.gige_tl.IssueScheduledActionCommandWait(
                self.deviceKey,
                self.groupKey,
                self.groupMask,
                self._actionTimeNs,
                self.broadcastAddress,
                timeoutMs,
                expected_results
                )

    def ScheduledActionCommand(
        self,
        deviceKey,
        groupKey,
        groupMask,
        actionTimeNs,
        broadcastAddress="255.255.255.255"
        ):
        return self._ScheduledActionCommand(
            self,
            deviceKey,
            groupKey,
            groupMask,
            actionTimeNs,
            broadcastAddress
            )

    %}

}



////////////////////////////////////////////////////////////////////////////////

%include <pylon/gige/GigETransportLayer.h>;

////////////////////////////////////////////////////////////////////////////////
// now that the local typemaps are no longer needed, clear them.

%typemap(in) (Pylon::DeviceInfoList_t&, bool addToList);
%typemap(argout) Pylon::DeviceInfoList_t&;
%typemap(argout) const Pylon::DeviceInfoList_t&;
%typemap(in) Pylon::CDeviceInfo*;
%typemap(argout) Pylon::CDeviceInfo*;
%typemap(typecheck)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results);
%typemap(in)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results);
%typemap(freearg)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results);
%typemap(argout)
(uint32_t *pNumResults, Pylon::GigEActionCommandResult *results);

