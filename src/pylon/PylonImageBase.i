%nodefaultctor Pylon::CPylonImageBase;
%warnfilter(403) Pylon::CPylonImageBase;
%rename(PylonImageBase) Pylon::CPylonImageBase;
%ignore Pylon::CPylonImageBase::GetPixelData;
%rename(GetPixelData) Pylon::CPylonImageBase::GetPixelDataValue;

%include <pylon/PylonImageBase.h>;

%extend Pylon::CPylonImageBase {
	Pylon::SPixelData GetPixelDataValue(uint32_t position_x, uint32_t position_y) const {
		return $self->GetPixelData(position_x, position_y);
	}
}
