# ===============================================================================
# This sample shows how to access data containers.
# This is needed when using 3D cameras, e.g., Basler blaze.
# ===============================================================================
import os
from pypylon import pylon
from pypylon import genicam

import sys

# This is used for visualization.
import cv2
import time

# The exit code of the sample application.
exitCode = 0

try:
    # Create a pylon data container object.
    pylonDataContainer = pylon.PylonDataContainer()
    
    # Load the recipe file.
    thisdir = os.path.dirname(__file__)
    filename = os.path.join(thisdir, 'images/3D/little_boxes.gendc')
    pylonDataContainer.Load(filename)
    
    print("Component Count: ", pylonDataContainer.DataComponentCount);

    # Access data components if the component type indicates image data
    for componentIndex in range(pylonDataContainer.DataComponentCount):
        pylonDataComponent = pylonDataContainer.GetDataComponent(componentIndex);
        # Access the component data.
        print("ComponentType: ", pylonDataComponent.ComponentType)
        print("PixelType: ", pylonDataComponent.PixelType)
        print("SizeX: ", pylonDataComponent.Width)
        print("SizeY: ", pylonDataComponent.Height)
        print("OffsetX: ", pylonDataComponent.OffsetX)
        print("OffsetY: ", pylonDataComponent.OffsetY)
        print("PaddingX: ", pylonDataComponent.PaddingX)
        print("DataSize: ", pylonDataComponent.DataSize)
        print("TimeStamp: ", pylonDataComponent.TimeStamp)
        img = pylonDataComponent.Array
        print("Gray value of first pixel: ", img[0, 0])
        if pylonDataComponent.PixelType == pylon.PixelType_Coord3D_ABC32f:
            None
        else:
            cv2.imshow('Image' + str(componentIndex), img)
        # Release the data, otherwise it will not be freed
        # The data is held by the container and the components until all of them are released.
        pylonDataComponent.Release()

    for i in range(60):
        time.sleep(1)
        # Break the endless loop by pressing ESC.
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    # Free the data held by the container
    pylonDataContainer.Release()
        
except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e)
    exitCode = 1

sys.exit(exitCode)
