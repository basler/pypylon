    // Simplified Pixel Type Mapper
// Maps between PFNC integer pixel-format values and Pylon EPixelType.

%{
#include <pylon/PixelTypeMapper.h>
%}

%inline %{
static const char* _pixel_format_name_from_pixel_type(
    Pylon::EPixelType pixel_type,
    bool use_sfnc2
)
{
    Pylon::SFNCVersion sfnc_ver = use_sfnc2 ? Pylon::SFNCVersion_2_0 : Pylon::SFNCVersion_pre2_0;
    return Pylon::CPixelTypeMapper::GetNameByPixelType(pixel_type, sfnc_ver);
}

static Pylon::EPixelType _pixel_type_from_name(const char* name)
{
    return Pylon::CPixelTypeMapper::GetPylonPixelTypeByName(name);
}
%}

%pythoncode %{
def _pixel_mapper_use_sfnc2(sfnc_version):
    if sfnc_version is None:
        return True
    try:
        return sfnc_version >= Sfnc_2_0_0
    except NameError:
        return True


class PixelTypeMapper:
    """
    Provides static methods to map between Pylon pixel types and symbolic
    pixel-format values for SFNC 1.x/2.x versions.

    This class encapsulates pixel type mapping functionality for converting
    between EPixelType enumerations and their symbolic PFNC (Pixel Format
    Naming Convention) representations.
    """

    @staticmethod
    def GetPixelFormatByPixelType(pixel_type, sfnc_version=None):
        """
        Map a Pylon pixel type to its symbolic pixel-format string for SFNC 1.x/2.x.

        Args:
            pixel_type (int): The Pylon pixel type (EPixelType) to convert.
            sfnc_version (int, optional): The SFNC version to use (e.g., Sfnc_2_0_0).
                                         Defaults to SFNC 2.0.0.

        Returns:
            str: The symbolic pixel-format string (e.g., "Mono8", "RGB8"),
                 or empty string if the pixel type is not recognized.

        Examples:
            >>> PixelTypeMapper.GetPixelFormatByPixelType(pylon.PixelType_Mono8)
            'Mono8'
            >>> PixelTypeMapper.GetPixelFormatByPixelType(
            ...     pylon.PixelType_RGB8packed,
            ...     pylon.Sfnc_1_5_0
            ... )
            'RGB8Packed'
        """
        return _pixel_format_name_from_pixel_type(pixel_type, _pixel_mapper_use_sfnc2(sfnc_version))

    @staticmethod
    def GetPylonPixelTypeByPixelFormatValue(pixel_format_value, sfnc_version=None):
        """
        Map an integer pixel-format value (PFNC code) to a Pylon pixel type.

        Args:
            pixel_format_value (int): The integer pixel-format value to convert.
            sfnc_version (int, optional): The SFNC version to use (e.g., Sfnc_2_0_0).
                                         Defaults to SFNC 2.0.0.

        Returns:
            int: The corresponding Pylon EPixelType value, or PixelType_Undefined
                 if the format value is not recognized.

        Examples:
            >>> PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(pylon.PixelType_Mono8)
            # Returns: PixelType_Mono8
            >>> PixelTypeMapper.GetPylonPixelTypeByPixelFormatValue(0xDEADBEEF)
            # Returns: PixelType_Undefined
        """
        pixel_format_name = _pixel_format_name_from_pixel_type(
            pixel_format_value,
            _pixel_mapper_use_sfnc2(sfnc_version)
        )
        if not pixel_format_name:
            return PixelType_Undefined
        return _pixel_type_from_name(pixel_format_name)
%}
