import os
import shutil
import logging
import sys
import readline
import functools

logging.basicConfig(level=logging.ERROR, filename='fms_errors.log', format='%(asctime)s - %(levelname)s - %(message)s')

def exception_handler(func):
    """Decorator to handle exceptions and perform logging."""
    @functools.wraps(func)  # This preserves the name and docstring of the decorated function.
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            error_message = 'Error: File or directory not found.'
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

def complete(text, state):
    results = [x for x in os.listdir('.') if x.startswith(text)] + [None]
    return results[state]

readline.set_completer(complete)
readline.parse_and_bind("tab: complete")

class Document:
    def __init__(self, file_name):
        self.file_name = file_name

    @exception_handler
    def get_file_content(self):
        """Retrieve and return the content of the file."""
        with open(self.file_name, 'r') as file:
            return file.read()

    @exception_handler
    def write_to_file(self, content):
        """Write specified content to the file."""
        with open(self.file_name, 'w') as file:
            file.write(content)
        return f'Content written to {self.file_name} successfully.'

    @exception_handler
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
    
    @staticmethod
    def is_valid_path(path):
        """Check if the provided path is a valid directory and writable."""
        return os.path.isdir(path) and os.access(path, os.W_OK)
    
    @staticmethod
    def sanitize_filename(name):
        # Normalize the path to prevent directory traversal
        name = os.path.normpath(name).replace("../", "").replace("..\\\\" , "")
        # Allow only alphanumeric, spaces, periods, underscores, and dashes
        return ''.join(char for char in name if char.isalnum() or char in (' ', '.', '_', '-'))
   
    @staticmethod
    def validate_file(file_name, existing_files, operation_type):
        """Validate the filename based on the operation type."""
        if not file_name:
            return False, "Filename cannot be empty."
        
        file_exists = file_name in existing_files

        if operation_type == 'create' and file_exists:
            return False, "File already exists."
        elif operation_type == 'delete' and not file_exists:
            return False, "File does not exist."
        
        return True, "Filename is valid."

    @exception_handler
    def list_files(self, verbose=False):
        """List all files in the current directory."""
        files = self.files
        if verbose:
            print(f"Listing all files in directory: {self.path}")
        return files

    @exception_handler
    def create_file(self, file_name, verbose=False):
        """Create a file if it does not exist, with input sanitization and validation."""
        # Sanitize the input filename
        file_name = FileManager.sanitize_filename(file_name)
        # Validate the filename for creation
        valid, message = FileManager.validate_file(file_name, self.files, 'create')
        if not valid:
            return message
        
        try:
            with open(file_name, 'w') as file:
                file.write('')
            self.files.append(file_name)
            self.refresh_files()
            return 'File created successfully.' if not verbose else f'File {file_name} created successfully in {self.path}.'
        except Exception as e:
            return f"An error occurred while creating the file: {e}"

    @exception_handler
    def delete_file(self, file_name, verbose=False):
        """Delete a file if it exists, with input sanitization and validation."""
        # Sanitize the input filename
        file_name = FileManager.sanitize_filename(file_name)
        # Validate the filename for deletion
        valid, message = FileManager.validate_file(file_name, self.files, 'delete')
        if not valid:
            return message

        try:
            os.remove(file_name)
            self.files.remove(file_name)
            self.refresh_files()
            return 'File deleted successfully.' if not verbose else f'File {file_name} deleted from {self.path}.'
        except Exception as e:
            return f"An error occurred while deleting the file: {e}"

    @exception_handler
    def rename_file(self, old_name, new_name, verbose=False):
        """Rename a file, with input sanitization and validation."""
        # Sanitize the input filenames
        old_name = FileManager.sanitize_filename(old_name)
        new_name = FileManager.sanitize_filename(new_name)
        
        # Validate the old filename for existence
        valid_old, message_old = FileManager.validate_file(old_name, self.files, 'delete')  # Using 'delete' type for existence check
        if not valid_old:
            return message_old
        
        # Validate the new filename to ensure it does not already exist
        valid_new, message_new = FileManager.validate_file(new_name, self.files, 'create')  # Using 'create' type for non-existence check
        if not valid_new:
            return message_new

        try:
            os.rename(old_name, new_name)
            self.files.remove(old_name)
            self.files.append(new_name)
            self.refresh_files()
            return 'File renamed successfully.' if not verbose else f'File {old_name} renamed to {new_name} in {self.path}.'
        except Exception as e:
            return f"An error occurred while renaming the file: {e}"

    @exception_handler
    def move_file(self, file_name, new_path, verbose=False):
        """Move a file to a new path after sanitizing the filename and validating both the filename and path."""
        # Sanitize the input filename
        file_name = FileManager.sanitize_filename(file_name)
        
        # Validate the filename for existence
        valid, message = FileManager.validate_file(file_name, self.files, 'delete')  # 'delete' context used for existence check
        if not valid:
            return message

        # Validate the new path
        if not self.is_valid_path(new_path):
            error_message = 'Invalid or inaccessible path specified.'
            logging.error(error_message)
            return error_message

        try:
            shutil.move(file_name, new_path)
            self.files.remove(file_name)
            self.refresh_files()
            return 'File moved successfully.' if not verbose else f'File {file_name} moved to {new_path}.'
        except Exception as e:
            return f"An error occurred while moving the file: {e}"

    @exception_handler
    def copy_file(self, file_name, new_path, max_copies=10, verbose=False):
        """
        Copy a file to a new path after sanitizing the filename and validating the path.
        Handle file naming to avoid overwrites up to a maximum number of copies.
        If the path is invalid, log the error and return an error message.
        """
        # Sanitize the input filename
        file_name = FileManager.sanitize_filename(file_name)

        # Check if the file exists in the current directory
        if file_name not in self.files:
            return f'Error: The file {file_name} does not exist.'

        # Validate the new path
        if not self.is_valid_path(new_path):
            error_message = 'Invalid or inaccessible path specified.'
            logging.error(error_message)
            return error_message

        # Split the new path into base path and file name
        base_path, file = os.path.split(new_path)
        if base_path == '' or base_path == '.':
            base_path = self.path  # Default to the same directory if no path specified

        # Initialize the original file and counter for copying
        original_file = file
        counter = 1
        while os.path.exists(os.path.join(base_path, file)) and counter <= max_copies:
            file = f"{os.path.splitext(original_file)[0]}_copy{counter}{os.path.splitext(original_file)[1]}"
            counter += 1

        # Copy the file if the maximum number of copies has not been reached
        if counter <= max_copies:
            shutil.copy(os.path.join(self.path, file_name), os.path.join(base_path, file))
            if base_path == self.path:
                self.files.append(file)  # Explicitly add the new file name to the list
                self.refresh_files()
            success_message = f'File {file_name} copied to {os.path.join(base_path, file)} successfully.'
            return 'File copied successfully.' if not verbose else success_message
        else:
            return f'Error: Maximum number of copies ({max_copies}) reached.'

    @exception_handler
    def create_directory(self, directory_name, verbose=False):
        """Create a directory if it does not exist, with input sanitization and validation."""
        # Sanitize the input directory name
        directory_name = FileManager.sanitize_filename(directory_name)

        # Check if the directory exists in the current directory
        if directory_name in self.files:
            return 'Error: Directory already exists.'

        try:
            os.mkdir(directory_name)
            self.files.append(directory_name)
            self.refresh_files()
            return 'Directory created successfully.' if not verbose else f'Directory {directory_name} created successfully in {self.path}.'
        except Exception as e:
            return f"An error occurred while creating the directory: {e}"

    @exception_handler       
    def delete_directory(self, directory_name, verbose=False):
        """Delete a directory."""
        shutil.rmtree(directory_name)
        self.files.remove(directory_name)
        self.refresh_files()
        return 'Directory deleted successfully.' if not verbose else f'Directory {directory_name} deleted from {self.path}.'

    @exception_handler
    def rename_directory(self, old_name, new_name, verbose=False):
        """Rename a directory."""
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.refresh_files()
        return 'Directory renamed successfully.' if not verbose else f'Directory {old_name} renamed to {new_name} in {self.path}.'

    @exception_handler
    def move_directory(self, directory_name, new_path, verbose=False):
        
        """Move a Directory to a new path after validating the path."""
        if not self.is_valid_path(new_path):
            error_message = 'Invalid or inaccessible path specified.'
            logging.error(error_message)
            return error_message
    
        shutil.move(directory_name, new_path)
        self.refresh_files()
        return 'Directory moved successfully.' if not verbose else f'Directory {directory_name} moved to {new_path}.'

    @exception_handler
    def copy_directory(self, directory_name, new_path, max_copies=10, verbose=False):

        """Validate the path."""
        if not self.is_valid_path(new_path):
            error_message = 'Invalid or inaccessible path specified.'
            logging.error(error_message)
            return error_message
        
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
        
    @exception_handler
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

    def get_input(self, prompt):
        readline.set_completer_delims(' \t\n;')
        input_value = input(prompt)
        return input_value
    
    def display_help(self):
        print("""
        1. List files - Lists all files in the current directory.
        2. Create file - Creates a new file. Usage: 'create filename.txt'
        3. Delete file - Deletes a file. Usage: 'delete filename.txt'
        4. Rename file - Renames a file. Usage: 'rename oldname.txt newname.txt'
        5. Move file - Moves a file to a new path. Usage: 'move filename.txt newpath/'
        6. Copy file - Copies a file to a new path. Usage: 'copy filename.txt newpath/'
        7. Create directory - Creates a new directory. Usage: 'create_dir dirname'
        8. Delete directory - Deletes a directory. Usage: 'delete_dir dirname'
        9. Rename directory - Renames a directory. Usage: 'rename_dir oldname newname'
        10. Move directory - Moves a directory to a new path. Usage: 'move_dir dirname newpath/'
        11. Copy directory - Copies a directory to a new path. Usage: 'copy_dir dirname newpath/'
        12. List directories - Lists all directories in the current directory.
        13. Toggle verbosity - Toggle verbose mode on or off.
        14. Exit - Exits the application.
        """)

    def toggle_verbosity(self):
        self.verbose = not self.verbose
        print(f"Verbose mode set to {'on' if self.verbose else 'off'}.")

    def display_menu(self):
        """Display the command menu to the user."""
        options = [
            "1. List files", "2. Create file", "3. Delete file", "4. Rename file",
            "5. Move file", "6. Copy file", "7. Create directory", "8. Delete directory",
            "9. Rename directory", "10. Move directory", "11. Copy directory", "12. List directories", 
            "13. Toggle verbosity", "14. Exit", "Type 'help' for more information."
        ]
        for option in options:
            print(option)
        self.handle_input()

    def handle_input(self):
        """Handle user input from the command menu."""
        choice = self.get_input('Enter your choice: ')
        action = {
            '1': self.list_files, '2': self.create_file, '3': self.delete_file,
            '4': self.rename_file, '5': self.move_file, '6': self.copy_file,
            '7': self.create_directory, '8': self.delete_directory, '9': self.rename_directory,
            '10': self.move_directory, '11': self.copy_directory, '12': self.list_directories,
            '13': self.toggle_verbosity, '14': self.exit, 'help': self.display_help
        }
        result = action.get(choice, lambda: 'Invalid choice. Please try again.')()
        if result:
            print(result)
        self.display_menu()

    def list_files(self):
        """List all files in the current directory."""
        return self.file_manager.list_files()
    
    def create_file(self):
        file_name = self.get_input('Enter the name of the file you would like to create: ')
        result = self.file_manager.create_file(file_name)
        print(result)
        self.display_menu()
    
    def delete_file(self):
        file_name = self.get_input('Enter the name of the file you would like to delete: ')
        result = self.file_manager.delete_file(file_name)
        print(result)
        self.display_menu()
    
    def rename_file(self):
        current_filename = self.get_input('Enter the name of the file you would like to rename: ')
        new_name = input('Enter the new name for the file: ')
        result = self.file_manager.rename_file(current_filename, new_name)
        print(result)
        self.display_menu()

    def move_file(self):
        file_name = self.get_input('Enter the name of the file you would like to move: ')
        new_path = self.get_input('Enter the new path for the file: ')
        result = self.file_manager.move_file(file_name, new_path)
        print(result)
        self.display_menu()
    def copy_file(self):
        file_name = self.get_input('Enter the name of the file you would like to copy: ')
        new_path = self.get_input('Enter the new path for the file: ')
        result = self.file_manager.copy_file(file_name, new_path)
        print(result)
        self.display_menu()
    
    def create_directory(self):
        directory_name = self.get_input('Enter the name of the directory you would like to create: ')
        result = self.file_manager.create_directory(directory_name)
        print(result)
        self.display_menu()
    
    def delete_directory(self):
        directory_name = self.get_input('Enter the name of the directory you would like to delete: ')
        result = self.file_manager.delete_directory(directory_name)
        print(result)
        self.display_menu()

    def rename_directory(self):
        current_filename = self.get_input('Enter the name of the directory you would like to rename: ')
        new_name = self.get_input('Enter the new name for the directory: ')
        result = self.file_manager.rename_directory(current_filename, new_name)
        print(result)
        self.display_menu()
    
    def move_directory(self):
        directory_name = self.get_input('Enter the name of the directory you would like to move: ')
        new_path = self.get_input('Enter the new path for the directory: ')
        result = self.file_manager.move_directory(directory_name, new_path)
        print(result)
        self.display_menu()
    
    def copy_directory(self):
        directory_name = self.get_input('Enter the name of the directory you would like to copy: ')
        new_path = self.get_input('Enter the new path for the directory: ')
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