from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import time
import unittest
from sys import platform


class InstantCameraTestSuite(PylonEmuTestCase):
    def test_params_set(self):

        # Do not choose a high value (> 15) for priority since that would require
        # admin privileges.
        if platform == 'linux':
            priority_for_test = 0
        else:
            priority_for_test = 15

        camera = pylon.InstantCamera()
        camera.MaxNumBuffer = 20
        camera.MaxNumQueuedBuffer = 40
        camera.MaxNumGrabResults = 700
        camera.ChunkNodeMapsEnable = False
        camera.StaticChunkNodeMapPoolSize = 1
        camera.GrabCameraEvents = True
        camera.MonitorModeActive = True
        camera.InternalGrabEngineThreadPriorityOverride = True
        camera.InternalGrabEngineThreadPriority = priority_for_test
        camera.GrabLoopThreadUseTimeout = True
        camera.GrabLoopThreadTimeout = 10000
        camera.GrabLoopThreadPriorityOverride = True
        camera.GrabLoopThreadPriority = priority_for_test
        camera.OutputQueueSize = 10

        self.assertEqual(20, camera.MaxNumBuffer.Value)
        self.assertEqual(40, camera.MaxNumQueuedBuffer.Value)
        self.assertEqual(700, camera.MaxNumGrabResults.Value)
        self.assertFalse(camera.ChunkNodeMapsEnable.Value)
        self.assertEqual(1, camera.StaticChunkNodeMapPoolSize.Value)
        self.assertTrue(camera.GrabCameraEvents.Value)
        self.assertTrue(camera.MonitorModeActive.Value)
        self.assertTrue(camera.InternalGrabEngineThreadPriorityOverride.Value)
        self.assertEqual(priority_for_test, camera.InternalGrabEngineThreadPriority.Value)
        self.assertTrue(camera.GrabLoopThreadUseTimeout.Value)
        self.assertEqual(10000, camera.GrabLoopThreadTimeout.Value)
        self.assertTrue(camera.GrabLoopThreadPriorityOverride.Value)
        self.assertEqual(priority_for_test, camera.GrabLoopThreadPriority.Value)
        self.assertEqual(10, camera.OutputQueueSize.Value)

    def test_variable_params(self):
        camera = self.create_first()
        camera.Open()
        camera.StartGrabbing()

        self.assertEqual(10, camera.NumQueuedBuffers.Value)
        
        #Busy waiting to work around a bug in python 3.4 that allows sleep to be interrupted
        #https://bugs.python.org/issue32057
        timeout = time.time() + 2
        while time.time() < timeout and camera.NumReadyBuffers.Value == 0:
            time.sleep(0.1)

        self.assertGreater(camera.NumReadyBuffers.Value, 0)
        self.assertEqual(0, camera.NumEmptyBuffers.Value)
        camera.Close()

        camera.MaxNumQueuedBuffer = 5
        camera.Open()
        camera.StartGrabbing()
        self.assertEqual(5, camera.NumEmptyBuffers.Value)
        camera.Close()


if __name__ == "__main__":
    unittest.main()
