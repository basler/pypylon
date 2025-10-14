from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
import unittest
import tempfile
import os


class LoadAndSaveTestSuite(PylonEmuTestCase):
    def test_load_and_save(self):
        # Create an instant camera object with the camera device found first.
        camera = self.create_first()
        camera.Open()
        # Print the model name of the camera.
        print("Using device ", camera.GetDeviceInfo().GetModelName())

        # featurePersistence = pylon.FeaturePersistence()

        # Use a temporary file that will be automatically deleted
        # Note: On Windows, NamedTemporaryFile keeps the file open, which prevents
        # pylon from opening it. We use delete=False and manually clean up instead.
        temp_file = tempfile.NamedTemporaryFile(suffix='.pfs', delete=False)
        nodeFile = temp_file.name
        temp_file.close()  # Close it so pylon can open it
        
        try:
            print("Saving camera's node map to file...")
            print(nodeFile)

            # Save the content of the camera's node map into the file.
            pylon.FeaturePersistence.Save(nodeFile, camera.GetNodeMap())

            # Just for demonstration, read the content of the file back to the camera's node map with enabled validation.
            print("Reading file back to camera's node map...")
            pylon.FeaturePersistence.Load(nodeFile, camera.GetNodeMap(), True)
        finally:
            # Clean up the temporary file
            try:
                os.unlink(nodeFile)
            except Exception:
                pass
        
        # Close the camera.
        camera.Close()


if __name__ == "__main__":
    unittest.main()
