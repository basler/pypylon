from pylongigetestcase import PylonTestCase
from pypylon import pylon
import unittest


class LoadAndSaveTestSuite(PylonTestCase):
    def test_load_and_save(self):
        nodeFile = "NodeMap.pfs"

        # Create an instant camera object with the camera device found first.
        camera = self.create_first()
        camera.Open()
        # Print the model name of the camera.
        print("Using device ", camera.GetDeviceInfo().GetModelName())

        # featurePersistence = pylon.FeaturePersistence()

        print("Saving camera's node map to file...")
        print(nodeFile)

        # Save the content of the camera's node map into the file.
        pylon.FeaturePersistence.Save(nodeFile, camera.GetNodeMap())

        # Just for demonstration, read the content of the file back to the camera's node map with enabled validation.
        print("Reading file back to camera's node map...")
        pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
        # Close the camera.
        camera.Close()


if __name__ == "__main__":
    unittest.main()
