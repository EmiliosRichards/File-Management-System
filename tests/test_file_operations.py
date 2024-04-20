import pytest
from unittest.mock import patch, mock_open
from src.FileManagementSystem import FileManager

# Use - pytest tests/test_file_operations.py - in cli to run the tests.


# # Test for listing files

def test_list_files(mocker):
    # Set up the expected file list and mock os.listdir before FileManager instantiation
    expected_files = ["file1.txt", "file2.txt", "file3.txt"]
    mocker.patch('os.listdir', return_value=expected_files) # Mock os.listdir

    # Now create the FileManager instance
    fm = FileManager()

    # Invoke the method
    response = fm.list_files()

    # Assert that all expected files are in the response
    assert response == expected_files, f"Expected {expected_files}, but got {response}"

# Test for creating a file  
# def test_create_file(mocker):
#     # Setup
#     fm = FileManager() # Create the FileManager instance
#     mocker.patch('builtins.open', mock_open())  # Mock the open function
#     mocker.patch('os.listdir', return_value=[])  # Mock os.listdir to simulate an empty directory

#     filename = "newfile.txt"
#     response = fm.create_file(filename)  # Call the method

#     # Assertions
#     assert "created successfully" in response, "The response should indicate success"
#     assert filename in fm.files, f"Expected '{filename}' to be in {fm.files}"


# Test for creating a file
def test_create_file(mocker):
    fm = FileManager() # Create the FileManager instance
    mocker.patch('builtins.open', mocker.mock_open())  # Mock the open function to not actually open a file
    mocker.patch('os.listdir', return_value=[])  # Start with an empty directory list

    filename = "newfile.txt"
    fm.files = []  # Explicitly setting the initial state
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

# Test for copying a file
def test_copy_file_no_conflicts(mocker):
    fm = FileManager()
    filename = "testfile.txt"
    fm.files = [filename]
    new_path = "copy_of_testfile.txt"

    mocker.patch('shutil.copy')  # Mock the shutil.copy function
    mocker.patch('os.path.exists', return_value=False)  # Assume no file exists at the new location

    response = fm.copy_file(filename, new_path)
    assert "copied successfully" in response
    assert filename in fm.files  # Original file should still be there
    assert new_path in fm.files  # New file should be added to the list

# Test for copying a file when the file already exists
def test_copy_file_with_conflicts(mocker):
    fm = FileManager()
    filename = "testfile.txt"
    fm.files = [filename, "copy_of_testfile.txt"]
    new_path = "copy_of_testfile.txt"

    mocker.patch('shutil.copy')
    mocker.patch('os.path.exists', side_effect=[True, False])  # First call returns True, second returns False for new copy
    mocker.patch('os.path.join', return_value=new_path)  # Simulate file path joining
    mocker.patch('os.path.splitext', return_value=("copy_of_testfile", ".txt"))  # Split file name and extension

    # Test behavior when the file already exists and needs to be uniquely named
    response = fm.copy_file(filename, new_path)
    assert "copied successfully" in response
    assert "testfile_copy1.txt" in fm.files  # Check if the new path with a unique identifier is mentioned

