// Contains a configuration that sets pixel data format and Image AOI.

#ifndef INCLUDED_PIXELFORMATANDAOICONFIGURATION_H_00104928
#define INCLUDED_PIXELFORMATANDAOICONFIGURATION_H_00104928

#include <pylon/ConfigurationEventHandler.h>
#include <pylon/ParameterIncludes.h>

namespace Pylon
{
    class CInstantCamera;
}
class CPixelFormatAndAoiConfiguration : public Pylon::CConfigurationEventHandler
{
public:
    void OnOpened( Pylon::CInstantCamera& camera )
    {
        try
        {
            // Allow all the names in the namespace GenApi to be used without qualification.
            using namespace Pylon;

            // Get the camera control object.
            GenApi::INodeMap& nodemap = camera.GetNodeMap();

            // Get the parameters for setting the image area of interest (Image AOI).
            CIntegerParameter width( nodemap, "Width" );
            CIntegerParameter height( nodemap, "Height" );
            CIntegerParameter offsetX( nodemap, "OffsetX" );
            CIntegerParameter offsetY( nodemap, "OffsetY" );

            // Maximize the Image AOI.
            offsetX.TrySetToMinimum(); // Set to minimum if writable.
            offsetY.TrySetToMinimum(); // Set to minimum if writable.
            width.SetToMaximum();
            height.SetToMaximum();

            // Set the pixel data format.
            CEnumParameter( nodemap, "PixelFormat" ).SetValue( "Mono8" );
        }
        catch (const Pylon::GenericException& e)
        {
            throw RUNTIME_EXCEPTION( "Could not apply configuration. const GenericException caught in OnOpened method msg=%hs", e.what() );
        }
    }
};

#endif /* INCLUDED_PIXELFORMATANDAOICONFIGURATION_H_00104928 */
