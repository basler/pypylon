// Contains an Image Event Handler that prints a message for each event method call.

#ifndef INCLUDED_IMAGEEVENTPRINTER_H_7884943
#define INCLUDED_IMAGEEVENTPRINTER_H_7884943

#include <pylon/ImageEventHandler.h>
#include <pylon/GrabResultPtr.h>
#include <iostream>

namespace Pylon
{
    class CInstantCamera;

    class CImageEventPrinter : public CImageEventHandler
    {
    public:

        virtual void OnImagesSkipped( CInstantCamera& camera, size_t countOfSkippedImages )
        {
            std::cout << "OnImagesSkipped event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;
            std::cout << countOfSkippedImages << " images have been skipped." << std::endl;
            std::cout << std::endl;
        }


        virtual void OnImageGrabbed( CInstantCamera& camera, const CGrabResultPtr& ptrGrabResult )
        {
            std::cout << "OnImageGrabbed event for device " << camera.GetDeviceInfo().GetModelName() << std::endl;

            // Image grabbed successfully?
            if (ptrGrabResult->GrabSucceeded())
            {
                std::cout << "SizeX: " << ptrGrabResult->GetWidth() << std::endl;
                std::cout << "SizeY: " << ptrGrabResult->GetHeight() << std::endl;
                const uint8_t* pImageBuffer = (uint8_t*) ptrGrabResult->GetBuffer();
                std::cout << "Gray value of first pixel: " << (uint32_t) pImageBuffer[0] << std::endl;
                std::cout << std::endl;
            }
            else
            {
                std::cout << "Error: " << std::hex << ptrGrabResult->GetErrorCode() << std::dec << " " << ptrGrabResult->GetErrorDescription() << std::endl;
            }
        }
    };
}

#endif /* INCLUDED_IMAGEEVENTPRINTER_H_7884943 */
