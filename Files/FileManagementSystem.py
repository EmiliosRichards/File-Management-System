import os
import shutil
import pathlib



class Document:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def get_file_content(self):
        with open(self.file_name, 'r') as file:
            return file.read()

    def write_to_file(self, content):
        with open(self.file_name, 'w') as file:
            file.write(content)

    def get_file_size(self):
        return os.path.getsize(self.file_name)
    


class FileManager:
    def __init__(self):
        self.path = os.getcwd()
        self.files = os.listdir(self.path)
        self.needs_refresh = False    # This is a flag to check if the files list needs to be refreshed.

    def list_files(self):
        return self.files

    def create_file(self, file_name):
        with open(file_name, 'w') as file:
            file.write('')
        self.files.append(file_name)
        self.needs_refresh = True

    def delete_file(self, file_name):
        os.remove(file_name)
        self.files.remove(file_name)
        self.needs_refresh = True

    def rename_file(self, old_name, new_name):
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.needs_refresh = True

    def move_file(self, file_name, new_path):
        shutil.move(file_name, new_path)
        self.files.remove(file_name)
        self.needs_refresh = True

    def copy_file(self, file_name, new_path):
        shutil.copy(file_name, new_path)
        self.needs_refresh = True
    def create_directory(self, directory_name):
        os.mkdir(directory_name)
        self.files.append(directory_name)

    def delete_directory(self, directory_name):
        shutil.rmtree(directory_name)
        self.files.remove(directory_name)

    def rename_directory(self, old_name, new_name):
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.needs_refresh = True  

    def move_directory(self, directory_name, new_path):
        shutil.move(directory_name, new_path)
        self.needs_refresh = True

    def copy_directory(self, directory_name, new_path):
        shutil.copytree(directory_name, new_path)
        self.needs_refresh = True

    def list_directories(self):
        directories = []
        for file in self.files:
            if os.path.isdir(file):
                directories.append(file)
        return directories
    
    def refresh_files(self):
        if self.needs_refresh:
            self.files = os.listdir(self.path)
            self.needs_refresh = False
