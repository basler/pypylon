// Contains functions for creating sample images.

#ifndef INCLUDED_SAMPLEIMAGECREATOR_H_2792867
#define INCLUDED_SAMPLEIMAGECREATOR_H_2792867

#include <pylon/PylonImage.h>
#include <pylon/Pixel.h>
#include <pylon/ImageFormatConverter.h>

namespace SampleImageCreator
{
    Pylon::CPylonImage CreateJuliaFractal( Pylon::EPixelType pixelType, uint32_t width, uint32_t height )
    {
        // Allow all the names in the namespace Pylon to be used without qualification.
        using namespace Pylon;

        // Define Constants.
        static const SRGB8Pixel palette[] =
        {
            {0, 28, 50}, {0, 42, 75}, {0, 56, 100}, {0, 70, 125}, {0, 84, 150},
            {0, 50, 0}, {0, 100, 0}, {0, 150, 0}, {0, 200, 0}, {0, 250, 0},
            {50, 0, 0}, {100, 0, 0}, {150, 0, 0}, {200, 0, 0}, {250, 0, 0}
        };
        uint32_t numColors = sizeof( palette ) / sizeof( palette[0] );

        const double cX = -0.735;
        const double cY = 0.11;
        const double cMaxX = 1.6;
        const double cMinX = -1.6;
        const double cMaxY = 1;
        const double cMinY = -1;
        const uint32_t cMaxIterations = 50;

        // Create image.
        CPylonImage juliaFractal( CPylonImage::Create( PixelType_RGB8packed, width, height ) );

        // Get the pointer to the first pixel.
        SRGB8Pixel* pCurrentPixel = (SRGB8Pixel*) juliaFractal.GetBuffer();

        // Compute the fractal.
        for (uint32_t pixelY = 0; pixelY < height; ++pixelY)
        {
            for (uint32_t pixelX = 0; pixelX < width; ++pixelX, ++pCurrentPixel)
            {
                long double x = ((cMaxX - cMinX) / width) * pixelX + cMinX;
                long double y = cMaxY - pixelY * ((cMaxY - cMinY) / height);
                long double xd = 0;
                long double yd = 0;
                uint32_t i = 0;

                for (; i < cMaxIterations; ++i)
                {
                    xd = x * x - y * y + cX;
                    yd = 2 * x * y + cY;
                    x = xd;
                    y = yd;
                    if ((x * x + y * y) > 4)
                    {
                        break;
                    }
                }

                if (i >= cMaxIterations)
                {
                    *pCurrentPixel = palette[0];
                }
                else
                {
                    *pCurrentPixel = palette[i % numColors];
                }
            }
        }

        // Convert the image to the target format if needed.
        if (juliaFractal.GetPixelType() != pixelType)
        {
            CImageFormatConverter converter;
            converter.OutputPixelFormat = pixelType;
            converter.OutputBitAlignment = OutputBitAlignment_MsbAligned;
            converter.Convert( juliaFractal, CPylonImage( juliaFractal ) );
        }

        // Return the image.
        return juliaFractal;
    }


    Pylon::CPylonImage CreateMandelbrotFractal( Pylon::EPixelType pixelType, uint32_t width, uint32_t height )
    {
        // Allow all the names in the namespace Pylon to be used without qualification.
        using namespace Pylon;

        // Define constants.
        static const SRGB8Pixel palette[] =
        {
            {0, 28, 50}, {0, 42, 75}, {0, 56, 100}, {0, 70, 125}, {0, 84, 150},
            {0, 50, 0}, {0, 100, 0}, {0, 150, 0}, {0, 200, 0}, {0, 250, 0},
            {50, 0, 0}, {100, 0, 0}, {150, 0, 0}, {200, 0, 0}, {250, 0, 0}
        };
        uint32_t numColors = sizeof( palette ) / sizeof( palette[0] );

        const double  cMaxX = 1.0;
        const double  cMinX = -2.0;
        const double  cMaxY = 1.2;
        const double  cMinY = -1.2;
        const uint32_t cMaxIterations = 50;

        // Create image.
        CPylonImage mandelbrotFractal( CPylonImage::Create( PixelType_RGB8packed, width, height ) );

        // Get the pointer to the first pixel.
        SRGB8Pixel* pCurrentPixel = (SRGB8Pixel*) mandelbrotFractal.GetBuffer();

        // Compute the fractal.
        for (uint32_t pixelY = 0; pixelY < height; ++pixelY)
        {
            for (uint32_t pixelX = 0; pixelX < width; ++pixelX, ++pCurrentPixel)
            {
                long double xStart = ((cMaxX - cMinX) / width) * pixelX + cMinX;
                long double yStart = cMaxY - pixelY * ((cMaxY - cMinY) / height);
                long double x = xStart;
                long double y = yStart;
                long double xd = 0;
                long double yd = 0;
                uint32_t i = 0;

                for (; i < cMaxIterations; ++i)
                {
                    xd = x * x - y * y + xStart;
                    yd = 2 * x * y + yStart;
                    x = xd;
                    y = yd;
                    if ((x * x + y * y) > 4)
                    {
                        break;
                    }
                }

                if (i >= cMaxIterations)
                {
                    *pCurrentPixel = palette[0];
                }
                else
                {
                    *pCurrentPixel = palette[i % numColors];
                }
            }
        }

        // Convert the image to the target format if needed.
        if (mandelbrotFractal.GetPixelType() != pixelType)
        {
            CImageFormatConverter converter;
            converter.OutputPixelFormat = pixelType;
            converter.OutputBitAlignment = OutputBitAlignment_MsbAligned;
            converter.Convert( mandelbrotFractal, CPylonImage( mandelbrotFractal ) );
        }

        // Return the image.
        return mandelbrotFractal;
    }

}

#endif /* INCLUDED_SAMPLEIMAGECREATOR_H_2792867 */
