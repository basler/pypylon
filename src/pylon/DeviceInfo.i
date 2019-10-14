%rename(DeviceInfo) Pylon::CDeviceInfo;

%include <pylon/PylonVersionNumber.h>

#if PYLON_VERSION_MAJOR < 6

    // swig (3.0.12) cannot handle definitions like:
    // const char* const ManufacturerInfoKey("ManufacturerInfo");
    // Since there is no need for the string constants defined in DeviceInfo.h, we
    // simply rename them and then tell swig to ignore them

    #define ManufacturerInfoKey                 ManufacturerInfoKeyI=
    #define DeviceGUIDKey                       DeviceGUIDKeyI=
    #define VendorIdKey                         VendorIdKeyI=
    #define ProductIdKey                        ProductIdKeyI=
    #define DriverKeyNameKey                    DriverKeyNameKeyI=
    #define UsbDriverTypeKey                    UsbDriverTypeKeyI=
    #define UsbPortVersionBcdKey                UsbPortVersionBcdKeyI=
    #define SpeedSupportBitmaskKey              SpeedSupportBitmaskKeyI=
    #define TransferModeKey                     TransferModeKeyI=
    #define BconAdapterLibraryNameKey           BconAdapterLibraryNameKeyI=
    #define BconAdapterLibraryVersionKey        BconAdapterLibraryVersionKeyI=
    #define BconAdapterLibraryApiVersionKey     BconAdapterLibraryApiVersionKeyI=
    #define SupportedBconAdapterApiVersionKey   SupportedBconAdapterApiVersionKeyI=

    %ignore ManufacturerInfoKeyI;
    %ignore DeviceGUIDKeyI;
    %ignore VendorIdKeyI;
    %ignore ProductIdKeyI;
    %ignore DriverKeyNameKeyI;
    %ignore UsbDriverTypeKeyI;
    %ignore UsbPortVersionBcdKeyI;
    %ignore SpeedSupportBitmaskKeyI;
    %ignore TransferModeKeyI;
    %ignore BconAdapterLibraryNameKeyI;
    %ignore BconAdapterLibraryVersionKeyI;
    %ignore BconAdapterLibraryApiVersionKeyI;
    %ignore SupportedBconAdapterApiVersionKeyI;

#endif

%ignore DeviceIdxKey;
%include <pylon/DeviceInfo.h>;

%pythoncode %{
    CDeviceInfo = DeviceInfo
%}