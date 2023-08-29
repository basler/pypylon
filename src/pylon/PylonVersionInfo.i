%rename(VersionInfo) Pylon::VersionInfo;

%ignore Pylon::VersionInfo::getVersionString;

%extend Pylon::VersionInfo {
  %pythoncode %{
    def __repr__(self):
        return f"<VersionInfo {self.getMajor()}.{self.getMinor()}.{self.getSubminor()}>"
  %}
};

%include <pylon/PylonVersionInfo.h>;

