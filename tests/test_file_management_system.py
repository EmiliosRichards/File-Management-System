import pytest
from src.FileManagementSystem import FileManager

# Use - pytest tests/test_file_operations.py - in cli to run the tests.



# Test for listing files
def test_list_files(mocker):
    fm = FileManager()
    mocker.patch('os.listdir', return_value=["file1.txt", "file2.txt", "file3.txt"])  # Mock os.listdir

    response = fm.list_files()  # Call the method to list files
    assert "file1.txt" in response
    assert "file2.txt" in response
    assert "file3.txt" in response

# Test for creating a file
def test_create_file(mocker):
    fm = FileManager()
    mocker.patch('builtins.open', mocker.mock_open())  # Mock the open function to not actually open a file
    mocker.patch('os.listdir', return_value=[])  # Start with an empty directory list

    filename = "newfile.txt"
    response = fm.create_file(filename)
    assert "created successfully" in response
    assert filename in fm.files  # Ensure the file is added to the file list

# Test for deleting a file
def test_delete_file(mocker):
    fm = FileManager()
    filename = "deletefile.txt"
    fm.files = [filename]  # Pretend the file exists

    mocker.patch('os.remove')  # Mock the os.remove function to not actually delete the file
    response = fm.delete_file(filename)
    assert "deleted successfully" in response
    assert filename not in fm.files  # Ensure the file is removed from the file list

# Test for renaming a file
def test_rename_file(mocker):
    fm = FileManager()
    old_name = "oldfile.txt"
    new_name = "newfile.txt"
    fm.files = [old_name]

    mocker.patch('os.rename')  # Mock the os.rename function
    response = fm.rename_file(old_name, new_name)
    assert "renamed successfully" in response
    assert old_name not in fm.files
    assert new_name in fm.files

# Test for moving a file
def test_move_file(mocker):
    fm = FileManager()
    filename = "movablefile.txt"
    fm.files = [filename]
    new_path = "/new/path/movablefile.txt"

    mocker.patch('shutil.move')  # Mock the shutil.move function
    response = fm.move_file(filename, new_path)
    assert "moved successfully" in response
    assert filename not in fm.files  # File should be considered moved out of the directory
