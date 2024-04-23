import os
import pytest
from unittest.mock import patch
from src.FileManagementSystem import FileManager

import unittest
from unittest.mock import patch, MagicMock


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
    def test_copy_file_with_conflicts(self, mock_is_valid_path, mock_listdir, mock_copy, mock_exists):
        # Setup the is_valid_path to always return True
        mock_is_valid_path.return_value = True

        # Define the behavior of os.path.exists
        mock_exists.side_effect = lambda x: True if '/fake/directory/testfile.txt' in x else False

        # Simulate the initial directory contents
        mock_listdir.return_value = self.file_manager.files

        # Path to copy to (same directory, for simplicity)
        new_path = '/fake/directory/testfile.txt'

        # Expected file names after conflict resolution
        expected_file_name_1 = '/fake/directory/testfile_copy1.txt'
        expected_file_name_2 = '/fake/directory/testfile_copy2.txt'

        # Run the test where maximum copies exceed
        result = self.file_manager.copy_file('testfile.txt', new_path, max_copies=2)
        self.assertEqual(result, 'File copied successfully.', "Should return success message")

        # Test exceeding maximum number of copies
        mock_exists.side_effect = lambda x: True
        result = self.file_manager.copy_file('testfile.txt', new_path, max_copies=2)
        self.assertEqual(result, 'Error: Maximum number of copies (2) reached.', "Should return error message on exceeding max copies")

if __name__ == '__main__':
    unittest.main()