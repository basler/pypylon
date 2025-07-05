// Contains a Configuration Event Handler that prints a message for each event method call.

#ifndef INCLUDED_CONFIGURATIONEVENTPRINTER_H_663006
#define INCLUDED_CONFIGURATIONEVENTPRINTER_H_663006

#include <pylon/ConfigurationEventHandler.h>
#include <iostream>

namespace Pylon
{
    class CInstantCamera;

    class CConfigurationEventPrinter : public CConfigurationEventHandler
    {
    public:
        void OnAttach( CInstantCamera& /*camera*/ )
        {
            std::cout << "OnAttach event" << std::endl;
        }

        void OnAttached( CInstantCamera& camera )
        {
            std::cout << "OnAttached event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnOpen( CInstantCamera& camera )
        {
            std::cout << "OnOpen event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnOpened( CInstantCamera& camera )
        {
            std::cout << "OnOpened event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnGrabStart( CInstantCamera& camera )
        {
            std::cout << "OnGrabStart event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnGrabStarted( CInstantCamera& camera )
        {
            std::cout << "OnGrabStarted event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnGrabStop( CInstantCamera& camera )
        {
            std::cout << "OnGrabStop event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnGrabStopped( CInstantCamera& camera )
        {
            std::cout << "OnGrabStopped event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnClose( CInstantCamera& camera )
        {
            std::cout << "OnClose event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnClosed( CInstantCamera& camera )
        {
            std::cout << "OnClosed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnDestroy( CInstantCamera& camera )
        {
            std::cout << "OnDestroy event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnDestroyed( CInstantCamera& /*camera*/ )
        {
            std::cout << "OnDestroyed event" << std::endl;
        }

        void OnDetach( CInstantCamera& camera )
        {
            std::cout << "OnDetach event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnDetached( CInstantCamera& camera )
        {
            std::cout << "OnDetached event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }

        void OnGrabError( CInstantCamera& camera, const char* errorMessage )
        {
            std::cout << "OnGrabError event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
            std::cout << "Error Message: " << errorMessage << std::endl;
        }

        void OnCameraDeviceRemoved( CInstantCamera& camera )
        {
            std::cout << "OnCameraDeviceRemoved event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
        }
    };
}

#endif /* INCLUDED_CONFIGURATIONEVENTPRINTER_H_663006 */
