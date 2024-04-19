import pytest
from src.FileManagementSystem import FileManager

def test_create_file():
    manager = FileManager()
    response = manager.create_file("testfile.txt")
    assert "created successfully" in response
    # Clean up
    manager.delete_file("testfile.txt")
