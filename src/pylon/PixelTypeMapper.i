// Pixel Type Mapper
// Ports Pylon::CPixelTypeMapper::GetPylonPixelTypeByName and
// Pylon::CPixelTypeMapper::GetNameByPixelType, which map between the Pylon
// EPixelType enum and the symbolic PixelFormat names used by GenICam
// cameras. Pixel format names changed with SFNC 2.0 (e.g. "RGB8Packed"
// pre-2.0 became "RGB8" in 2.0). On the Python side, GetNameByPixelType()
// takes the same built-in SFNC version (pylon.VersionInfo, e.g.
// pylon.Sfnc_2_0_0 or camera.GetSfncVersion()) used elsewhere in pypylon to
// select the naming convention, instead of the lower-level Pylon::SFNCVersion
// enum used by the C++ API.
//
// CPixelTypeMapper's instance API (which maps a device's live PixelFormat
// enumeration node) is intentionally not wrapped here: pypylon exposes that
// functionality through the higher-level pylon parameter API
// (e.g. camera.PixelFormat.Value) instead of raw GenApi enumeration nodes.
%{
#include <pylon/PixelTypeMapper.h>
%}

// Pylon::SFNCVersion selects the naming convention used by GetNameByPixelType.
// Re-declared here (values must stay in sync with pylon/PixelTypeMapper.h)
// because CPixelTypeMapper itself is not fully wrapped, see above.
namespace Pylon
{
    enum SFNCVersion
    {
        SFNCVersion_Invalid = 0,
        SFNCVersion_pre2_0  = 1,
        SFNCVersion_2_0     = 200
    };
}

%inline %{
static Pylon::EPixelType _pixel_type_mapper_get_pylon_pixel_type_by_name( const char* pszSymbolicName )
{
    return Pylon::CPixelTypeMapper::GetPylonPixelTypeByName( pszSymbolicName );
}

static const char* _pixel_type_mapper_get_name_by_pixel_type( Pylon::EPixelType pixelType, Pylon::SFNCVersion sfncVer )
{
    return Pylon::CPixelTypeMapper::GetNameByPixelType( pixelType, sfncVer );
}
%}

%pythoncode %{
def _pixel_type_mapper_to_sfnc_version(sfnc_version):
    """
    Maps a pylon.VersionInfo SFNC version (e.g. pylon.Sfnc_2_0_0, or the value
    returned by camera.GetSfncVersion()), or None, to the internal
    Pylon::SFNCVersion used by CPixelTypeMapper::GetNameByPixelType for
    selecting the naming convention.

    Note: Sfnc_2_0_0 is looked up lazily (at call time, not at module-import
    time) because SfncVersion.i, which defines it, is %included after this
    file in pylon.i.
    """
    if sfnc_version is not None and sfnc_version >= Sfnc_2_0_0:
        return SFNCVersion_2_0
    return SFNCVersion_pre2_0


class PixelTypeMapper:
    """
    Provides static methods to map between Pylon pixel types (EPixelType) and
    the symbolic pixel-format names used by a camera's PixelFormat parameter.

    A camera's PixelFormat setting is a symbolic name (e.g. "Mono8", "RGB8").
    The Pylon EPixelType is a separate enumeration used by pylon's image
    handling API (e.g. ImageFormatConverter). Use this class to convert
    between the two.
    """

    @staticmethod
    def GetPylonPixelTypeByName(symbolic_name):
        """
        Returns the Pylon EPixelType for a given symbolic pixel-format name.

        Args:
            symbolic_name (str): The symbolic pixel-format name, e.g. as
                returned by camera.PixelFormat.Value. Note: names are case
                sensitive.

        Returns:
            int: The corresponding EPixelType, or PixelType_Undefined if the
                 name is not recognized.

        Examples:
            >>> PixelTypeMapper.GetPylonPixelTypeByName("Mono16")
            # Returns: PixelType_Mono16
            >>> PixelTypeMapper.GetPylonPixelTypeByName("RGB8Packed")
            # Returns: PixelType_RGB8packed
        """
        return _pixel_type_mapper_get_pylon_pixel_type_by_name(symbolic_name)

    @staticmethod
    def GetNameByPixelType(pixel_type, sfnc_version=None):
        """
        Returns the symbolic pixel-format name for a given Pylon EPixelType.

        Args:
            pixel_type (int): The Pylon EPixelType to convert.
            sfnc_version (VersionInfo, optional): The SFNC version implemented by
                the camera device, e.g. as returned by
                camera.GetSfncVersion(), or one of the built-in SFNC version
                constants (pylon.Sfnc_1_5_0, pylon.Sfnc_2_0_0, …). Some names
                have been changed in SFNC 2.0. Defaults to None (equivalent
                to passing pylon.Sfnc_VersionUndefined), which selects the
                pre-2.0 naming convention, matching the underlying pylon API
                default.

        Returns:
            str: The symbolic pixel-format name (e.g. "Mono16",
                 "RGB8Packed"), or an empty string if the pixel type is not
                 recognized.

        Examples:
            >>> PixelTypeMapper.GetNameByPixelType(pylon.PixelType_Mono16)
            'Mono16'
            >>> PixelTypeMapper.GetNameByPixelType(
            ...     pylon.PixelType_RGB8packed, pylon.Sfnc_2_0_0
            ... )
            'RGB8'
            >>> PixelTypeMapper.GetNameByPixelType(
            ...     pylon.PixelType_RGB8packed, camera.GetSfncVersion()
            ... )
            # Returns: 'RGB8' or 'RGB8Packed', depending on the camera's SFNC version
        """
        return _pixel_type_mapper_get_name_by_pixel_type(
            pixel_type, _pixel_type_mapper_to_sfnc_version(sfnc_version)
        )
%}
