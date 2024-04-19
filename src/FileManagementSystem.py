import os
import shutil
import pathlib
import logging
import sys

logging.basicConfig(level=logging.ERROR, filename='fms_errors.log', format='%(asctime)s - %(levelname)s - %(message)s')

def exception_handler():
    """Decorator to handle exceptions and perform logging."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except FileNotFoundError:
                error_message = f'Error: File or directory not found: {args[1]}'
                logging.error(error_message)
                return error_message
            except IsADirectoryError:
                error_message = 'Error: Expected a file but found a directory.'
                logging.error(error_message)
                return error_message
            except PermissionError:
                error_message = 'Error: Permission denied.'
                logging.error(error_message)
                return error_message
            except NotADirectoryError:
                error_message = 'Error: Not a directory.'
                logging.error(error_message)
                return error_message
            except FileExistsError:
                error_message = 'Error: File or directory already exists.'
                logging.error(error_message)
                return error_message
            except Exception as e:
                error_message = f'Error: An unexpected error occurred: {e}'
                logging.error(error_message)
                return error_message
        return wrapper
    return decorator



class Document:
    def __init__(self, file_name):
        self.file_name = file_name

    @exception_handler(verbose=True)
    def get_file_content(self):
        """Retrieve and return the content of the file."""
        with open(self.file_name, 'r') as file:
            return file.read()

    @exception_handler(verbose=True)
    def write_to_file(self, content):
        """Write specified content to the file."""
        with open(self.file_name, 'w') as file:
            file.write(content)
        return f'Content written to {self.file_name} successfully.'

    @exception_handler(verbose=True)
    def get_file_size(self):
        """Get the size of the file."""
        return os.path.getsize(self.file_name)
        
        

class FileManager:
    def __init__(self):
        self.path = os.getcwd()
        self.files = os.listdir(self.path)

    def refresh_files(self):
        """Refresh the list of files in the current directory."""
        self.files = os.listdir(self.path)

    @exception_handler(verbose=True)
    def list_files(self, verbose=False):
        """List all files in the current directory."""
        files = self.files
        if verbose:
            print(f"Listing all files in directory: {self.path}")
        return files

    @exception_handler(verbose=True)
    def create_file(self, file_name, verbose=False):
        """Create a file if it does not exist."""
        if file_name in self.files:
            return 'Error: File already exists.'
        with open(file_name, 'w') as file:
            file.write('')
        self.files.append(file_name)
        self.refresh_files()
        return 'File created successfully.' if not verbose else f'File {file_name} created successfully in {self.path}.'

    @exception_handler(verbose=True)
    def delete_file(self, file_name, verbose=False):
        """Delete a file."""
        os.remove(file_name)
        self.files.remove(file_name)
        self.refresh_files()
        return 'File deleted successfully.' if not verbose else f'File {file_name} deleted from {self.path}.'

    @exception_handler(verbose=True)
    def rename_file(self, old_name, new_name, verbose=False):
        """Rename a file."""
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.refresh_files()
        return 'File renamed successfully.' if not verbose else f'File {old_name} renamed to {new_name} in {self.path}.'

    @exception_handler(verbose=True)
    def move_file(self, file_name, new_path, verbose=False):
        """Move a file to a new path."""
        shutil.move(file_name, new_path)
        self.files.remove(file_name)
        self.refresh_files()
        return 'File moved successfully.' if not verbose else f'File {file_name} moved to {new_path}.'

    @exception_handler(verbose=True)
    def copy_file(self, file_name, new_path, max_copies=10, verbose=False):
        """Copy a file, handling file naming to avoid overwrites up to a max number of copies."""
        base_path, file = os.path.split(new_path)
        if base_path == '' or base_path == '.':
            base_path = self.path  # Same directory

        original_file = file
        counter = 1
        while os.path.exists(os.path.join(base_path, file)) and counter <= max_copies:
            file = f"{os.path.splitext(original_file)[0]}_copy{counter}{os.path.splitext(original_file)[1]}"
            counter += 1

        if counter <= max_copies:
            shutil.copy(os.path.join(self.path, file_name), os.path.join(base_path, file))
            if base_path == self.path:
                self.refresh_files()
            return 'File copied successfully.' if not verbose else f'File {file_name} copied to {os.path.join(base_path, file)} successfully.'
        else:
            return f'Error: Maximum number of copies ({max_copies}) reached.'

    @exception_handler(verbose=True)        
    def create_directory(self, directory_name, verbose=False):
        """Create a directory if it does not exist."""
        if directory_name in self.files:
            return 'Error: Directory already exists.'
        os.mkdir(directory_name)
        self.files.append(directory_name)
        self.refresh_files()
        return 'Directory created successfully.' if not verbose else f'Directory {directory_name} created successfully in {self.path}.'

    @exception_handler(verbose=True)       
    def delete_directory(self, directory_name, verbose=False):
        """Delete a directory."""
        shutil.rmtree(directory_name)
        self.files.remove(directory_name)
        self.refresh_files()
        return 'Directory deleted successfully.' if not verbose else f'Directory {directory_name} deleted from {self.path}.'

    @exception_handler(verbose=True)
    def rename_directory(self, old_name, new_name, verbose=False):
        """Rename a directory."""
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.refresh_files()
        return 'Directory renamed successfully.' if not verbose else f'Directory {old_name} renamed to {new_name} in {self.path}.'

    @exception_handler(verbose=True)
    def move_directory(self, directory_name, new_path, verbose=False):
        """Move a directory."""
        shutil.move(directory_name, new_path)
        self.refresh_files()
        return 'Directory moved successfully.' if not verbose else f'Directory {directory_name} moved to {new_path}.'

    @exception_handler(verbose=True)
    def copy_directory(self, directory_name, new_path, max_copies=10, verbose=False):
        """Copy a directory, handling directory naming to avoid overwrites up to a max number of copies."""
        base_path, directory = os.path.split(new_path)
        if base_path == '' or base_path == '.':
            base_path = self.path  # Same directory

        original_directory = directory
        counter = 1
        while os.path.exists(os.path.join(base_path, directory)) and counter <= max_copies:
            directory = f"{original_directory}_copy{counter}"
            counter += 1

        if counter <= max_copies:
            shutil.copytree(os.path.join(self.path, directory_name), os.path.join(base_path, directory))
            if base_path == self.path:
                self.refresh_files()
            return 'Directory copied successfully.' if not verbose else f'Directory {directory_name} copied to {os.path.join(base_path, directory)} successfully.'
        else:
            return f'Error: Maximum number of copies ({max_copies}) reached.'
        
    @exception_handler(verbose=True)
    def list_directories(self):
        """List all directories in the current directory."""
        directories = []
        for file in self.files:
            if os.path.isdir(file):
                directories.append(file)
        return directories


class CLI:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.verbose = False

    def welcome_message(self):
        print('Welcome to the File Management System!')
        self.display_menu()

    def toggle_verbosity(self):
        self.verbose = not self.verbose
        print(f"Verbose mode set to {'on' if self.verbose else 'off'}.")

    def display_menu(self):
        """Display the command menu to the user."""
        options = [
            "1. List files", "2. Create file", "3. Delete file", "4. Rename file",
            "5. Move file", "6. Copy file", "7. Create directory", "8. Delete directory",
            "9. Rename directory", "10. Move directory", "11. Copy directory", "12. List directories", 
            "13. Toggle verbosity", "14. Exit"
        ]
        for option in options:
            print(option)
        self.handle_input()

    def handle_input(self):
        """Handle user input from the command menu."""
        choice = input('Enter your choice: ')
        action = {
            '1': self.list_files, '2': self.create_file, '3': self.delete_file,
            '4': self.rename_file, '5': self.move_file, '6': self.copy_file,
            '7': self.create_directory, '8': self.delete_directory, '9': self.rename_directory,
            '10': self.move_directory, '11': self.copy_directory, '12': self.list_directories,
            '13': self.toggle_verbosity, '14': self.exit
        }
        result = action.get(choice, lambda: 'Invalid choice. Please try again.')()
        if result:
            print(result)
        self.display_menu()

    def list_files(self):
        """List all files in the current directory."""
        return self.file_manager.list_files()
    
    def create_file(self):
        file_name = input('Enter the name of the file you would like to create: ')
        result = self.file_manager.create_file(file_name)
        print(result)
        self.display_menu()
    
    def delete_file(self):
        file_name = input('Enter the name of the file you would like to delete: ')
        result = self.file_manager.delete_file(file_name)
        print(result)
        self.display_menu()
    
    def rename_file(self):
        current_filename = input('Enter the name of the file you would like to rename: ')
        new_name = input('Enter the new name for the file: ')
        result = self.file_manager.rename_file(current_filename, new_name)
        print(result)
        self.display_menu()

    def move_file(self):
        file_name = input('Enter the name of the file you would like to move: ')
        new_path = input('Enter the new path for the file: ')
        result = self.file_manager.move_file(file_name, new_path)
        print(result)
        self.display_menu()
    def copy_file(self):
        file_name = input('Enter the name of the file you would like to copy: ')
        new_path = input('Enter the new path for the file: ')
        result = self.file_manager.copy_file(file_name, new_path)
        print(result)
        self.display_menu()
    
    def create_directory(self):
        directory_name = input('Enter the name of the directory you would like to create: ')
        result = self.file_manager.create_directory(directory_name)
        print(result)
        self.display_menu()
    
    def delete_directory(self):
        directory_name = input('Enter the name of the directory you would like to delete: ')
        result = self.file_manager.delete_directory(directory_name)
        print(result)
        self.display_menu()

    def rename_directory(self):
        current_filename = input('Enter the name of the directory you would like to rename: ')
        new_name = input('Enter the new name for the directory: ')
        result = self.file_manager.rename_directory(current_filename, new_name)
        print(result)
        self.display_menu()
    
    def move_directory(self):
        directory_name = input('Enter the name of the directory you would like to move: ')
        new_path = input('Enter the new path for the directory: ')
        result = self.file_manager.move_directory(directory_name, new_path)
        print(result)
        self.display_menu()
    
    def copy_directory(self):
        directory_name = input('Enter the name of the directory you would like to copy: ')
        new_path = input('Enter the new path for the directory: ')
        result = self.file_manager.copy_directory(directory_name, new_path)
        print(result)
        self.display_menu()
    
    def list_directories(self):
        result = directories = self.file_manager.list_directories()
        print('Directories in the current directory:')
        print(result)
        self.display_menu()

    def exit(self):
        print("Exiting the application.")
        sys.exit()

if __name__ == '__main__':
    file_manager = FileManager()
    cli = CLI(file_manager)
    cli.welcome_message()
    while True:
        cli.display_menu()


def test_create_file():
    fm = FileManager()  # Assuming FileManager is already defined
    filename = "testfile.txt"
    
    # Ensure file does not exist initially
    if filename in fm.files:
        os.remove(filename)
    
    # Test creating a new file
    result = fm.create_file(filename, verbose=True)
    assert "created successfully" in result, "File should be created successfully."
    
    # Clean up (delete the created file)
    os.remove(filename)

# test_create_file()