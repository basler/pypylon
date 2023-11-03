%rename(RegionEntryRLE32) Pylon::DataProcessing::SRegionEntryRLE32;

%include <pylondataprocessing/RegionEntry.h>;

%extend Pylon::DataProcessing::SRegionEntryRLE32 {

    SRegionEntryRLE32()
    {
        Pylon::DataProcessing::SRegionEntryRLE32* pResult = new Pylon::DataProcessing::SRegionEntryRLE32;
        pResult->StartX = 0;
        pResult->EndX = 0;
        pResult->Y = 0;
        return pResult;
    }
    
    SRegionEntryRLE32(int32_t startX, int32_t endX, int32_t y)
    {
        Pylon::DataProcessing::SRegionEntryRLE32* pResult = new Pylon::DataProcessing::SRegionEntryRLE32;
        pResult->StartX = startX;
        pResult->EndX = endX;
        pResult->Y = y;
        return pResult;
    }

    %pythoncode %{
        def __str__(self):
            result = "StartX = {0}; EndX = {1}; Y = {2}".format(self.StartX, self.EndX, self.Y)
            return result
    %}
}