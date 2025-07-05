// Contains a Camera Event Handler that prints a message for each event method call.

#ifndef INCLUDED_CAMERAEVENTPRINTER_H_4683453
#define INCLUDED_CAMERAEVENTPRINTER_H_4683453

#include <pylon/CameraEventHandler.h>
#include <pylon/ParameterIncludes.h>
#include <iostream>

namespace Pylon
{
    class CInstantCamera;

    class CCameraEventPrinter : public CCameraEventHandler
    {
    public:
        virtual void OnCameraEvent( CInstantCamera& camera, intptr_t userProvidedId, GenApi::INode* pNode )
        {
            std::cout << "OnCameraEvent event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
            std::cout << "User provided ID: " << userProvidedId << std::endl;
            std::cout << "Event data node name: " << pNode->GetName() << std::endl;
            CParameter value( pNode );
            if (value.IsValid())
            {
                std::cout << "Event node data: " << value.ToString() << std::endl;
            }
            std::cout << std::endl;
        }
    };
}

#endif /* INCLUDED_CAMERAEVENTPRINTER_H_4683453 */
