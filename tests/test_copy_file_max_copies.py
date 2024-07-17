import unittest
from unittest.mock import patch, MagicMock
from src.FileManagementSystem import FileManager  # Adjust the import according to your actual structure

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.fm = FileManager()
        self.fm.path = '/fake/directory'
        self.fm.files = ['existingfile.txt']



    @patch('src.FileManagementSystem.FileManager.is_valid_path', MagicMock(return_value=False))
    @patch('src.FileManagementSystem.shutil.copy')
    def test_invalid_path(self, mock_copy):
        response = self.fm.copy_file('existingfile.txt', '/invalid/path/newfile.txt')
        self.assertIn('Invalid or inaccessible path specified.', response)

    @patch('src.FileManagementSystem.os.path.exists', MagicMock(side_effect=[True]*10 + [False]))
    @patch('src.FileManagementSystem.shutil.copy')
    @patch('src.FileManagementSystem.FileManager.is_valid_path', MagicMock(return_value=True))
    def test_max_copies_reached(self, mock_copy):
        response = self.fm.copy_file('existingfile.txt', '/fake/directory/existingfile.txt')
        self.assertIn('Error: Maximum number of copies (10) reached.', response)

if __name__ == '__main__':
    unittest.main()