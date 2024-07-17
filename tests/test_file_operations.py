import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.FileManagementSystem import FileManager

# Use - pytest .tests/test_file_operations.py - in cli to run the tests.


# # Test for listing files

def test_list_files(mocker):
    # Set up the expected file list and mock os.listdir before FileManager instantiation
    expected_files = ["file1.txt", "file2.txt", "file3.txt"]
    mocker.patch('os.listdir', return_value=expected_files) # Mock os.listdir

    # Now create the FileManager instance
    fm = FileManager()

    # Invoke the method
    _, response = fm.list_files()

    # Assert that all expected files are in the response
    assert response == expected_files, f"Expected {expected_files}, but got {response}"

def test_create_file(mocker):
    # Setup the FileManager instance
    fm = FileManager()

    # Mock the 'open' to simulate file creation
    mocker.patch('builtins.open', mock_open())

    # Prepare the filename
    filename = "newfile.txt"

    # Initially, simulate an empty directory
    mocker.patch('os.listdir', return_value=[])

    # Call the method
    response = fm.create_file(filename)

    # Ensure the file creation was reported as successful
    assert "created successfully" in response, "The response should indicate success"

    # Mock 'os.listdir' again to simulate the file now exists after creation
    mocker.patch('os.listdir', return_value=[filename])

    # Validate the file is now listed in 'self.files'
    fm.refresh_files()  # This refresh should now see the new file
    assert filename in fm.files, f"Expected '{filename}' to be in {fm.files}"

# Test for deleting a file
def test_delete_file(mocker):
    # Create an instance of FileManager
    fm = FileManager()
    filename = "delete_me.txt"
    fm.files = [filename]  # Add the file to the list to simulate its presence

    # Mock os.remove to avoid actual file deletion
    mocker.patch('os.remove')
    # Mock os.listdir to simulate file presence initially and its absence after deletion
    mocker.patch('os.listdir', side_effect=[fm.files, []])


    # Call the method
    response = fm.delete_file(filename)

    # Validate response
    assert "deleted successfully" in response, "The response should indicate success"

    # Ensure the file is no longer in the list
    assert filename not in fm.files, f"File {filename} should not be in {fm.files} after deletion"

# Test for renaming a file
def test_rename_file(mocker):
    # Create an instance of FileManager
    fm = FileManager()
    old_name = "old_file.txt"
    new_name = "new_file.txt"
    fm.files = [old_name]  # Simulate the old file's presence

    # Mock os.rename to avoid actual file renaming
    mocker.patch('os.rename')

    # Mock os.listdir to reflect the directory's state before and after renaming
    mocker.patch('os.listdir', side_effect=[[old_name], [new_name]])

    # Ensure that the refresh_files function reads the mock os.listdir correctly
    fm.refresh_files = MagicMock(side_effect=lambda: setattr(fm, 'files', mocker.MagicMock(return_value=[new_name])()))

    # Call the method
    response = fm.rename_file(old_name, new_name)

    # Validate response
    assert "renamed successfully" in response, "The response should indicate success"

    # Ensure the old file name is removed and the new name is added
    assert old_name not in fm.files, f"Old file name {old_name} should not be in {fm.files} after renaming"
    assert new_name in fm.files, f"New file name {new_name} should be in {fm.files} after renaming"

# Test for moving a file
# def test_move_file(mocker):
#     fm = FileManager()
#     filename = "movablefile.txt"
#     fm.files = [filename]
#     new_path = "/new/path/movablefile.txt"

#     mocker.patch('shutil.move')  # Mock the shutil.move function
#     response = fm.move_file(filename, new_path)
#     assert "moved successfully" in response
#     assert filename not in fm.files  # File should be considered moved out of the directory

# Test for moving a file
def test_move_file(mocker):
    fm = FileManager()
    filename = "movablefile.txt"
    new_path = "/new/path/movablefile.txt"
    fm.files = [filename]

    # Setup mocks for the successful move
    move_mock = mocker.patch('shutil.move')
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('os.path.isdir', return_value=True)
    mocker.patch('os.access', return_value=True)

    # Perform the move operation
    response = fm.move_file(filename, new_path)
    assert "moved successfully" in response
    assert filename not in fm.files  # File should be considered moved out of the directory

    # Setup mocks for the failed move due to invalid path
    fm = FileManager()  # Reset FileManager
    fm.files = [filename]
    mocker.patch('os.path.exists', return_value=False)
    mocker.patch('os.path.isdir', return_value=False)  # Important to ensure directory validation fails
    mocker.patch('os.access', return_value=False)

    response = fm.move_file(filename, new_path)
    assert "Invalid or inaccessible path specified" in response

# Test for copying a file when the file does not exist
# def test_copy_file_no_conflicts(mocker):
#     # Setup
#     fm = FileManager()
#     fm.path = '/fake/directory'
#     file_name = "testfile.txt"
#     new_path = os.path.join(fm.path, 'newfile.txt')  # Use os.path.join to handle path separators

#     # Mock the filesystem interactions
#     mocker.patch('os.path.exists', return_value=False)
#     mock_copy = mocker.patch('shutil.copy')
#     mocker.patch('os.listdir', return_value=[file_name, "newfile.txt"])

#     # Call the method
#     response = fm.copy_file(file_name, new_path)

#     # Assertions
#     assert "copied successfully" in response, "The response should indicate success"
#     # Correctly check the mock call with the system-independent path
#     expected_source = os.path.join(fm.path, file_name)
#     expected_destination = os.path.join(fm.path, "newfile.txt")
#     mock_copy.assert_called_once_with(expected_source, expected_destination)

