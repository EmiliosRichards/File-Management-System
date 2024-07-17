import os
import unittest
from unittest.mock import patch, MagicMock
from src.FileManagementSystem import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        # Setup the FileManager instance
        self.file_manager = FileManager()
        self.file_manager.path = '/fake/directory'
        self.file_manager.files = ['testfile.txt', 'document.pdf']

    @patch('os.path.exists')
    @patch('shutil.copy')
    @patch('os.listdir')
    @patch('src.FileManagementSystem.FileManager.is_valid_path')  # Mock the is_valid_path static method
    def test_copy_file_no_conflicts(self, mock_is_valid_path, mock_listdir, mock_copy, mock_exists):
        # Setup the is_valid_path to always return True
        mock_is_valid_path.return_value = True

        # Define the behavior of os.path.exists
        mock_exists.side_effect = lambda x: False  # No file conflicts

        # Simulate the initial directory contents
        mock_listdir.return_value = self.file_manager.files

        # Path to copy to (same directory, for simplicity)
        new_path = os.path.join('/fake/directory', 'newfile.txt')

        # Run the test where there are no conflicts
        result = self.file_manager.copy_file('testfile.txt', new_path)
        self.assertEqual(result, 'File copied successfully.', "Should return success message")

        # Ensure the copy function was called correctly
        mock_copy.assert_called_once_with(os.path.join('/fake/directory', 'testfile.txt'), new_path)

if __name__ == '__main__':
    unittest.main()