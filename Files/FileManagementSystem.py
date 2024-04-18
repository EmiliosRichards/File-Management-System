import os
import shutil
import pathlib
import logging

logging.basicConfig(level=logging.ERROR, filename='fms_errors.log', format='%(asctime)s - %(levelname)s - %(message)s')

def exception_handler(func):
    """Decorator to handle exceptions and perform logging."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except FileNotFoundError:
            logging.error(f'File or directory not found: {args[1]}')
            return f'Error: {args[1]} does not exist.'
        except IsADirectoryError:
            logging.error(f'Expected a file but found a directory: {args[1]}')
            return 'Error: Expected a file but found a directory.'
        except NotADirectoryError:
            logging.error(f'Expected a directory but found a file: {args[1]}')
            return 'Error: Expected a directory but found a file.'
        except PermissionError:
            logging.error(f'No permission to access: {args[1]}')
            return 'Error: No permission to access the file or directory.'
        except Exception as e:
            logging.error(f'An unexpected error occurred: {e}')
            return f'An unexpected error occurred: {e}'
    return wrapper


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
        self.refresh_files()

    def refresh_files(self):
            self.files = os.listdir(self.path)

    @exception_handler
    def list_files(self):  
            return self.files

    @exception_handler
    def create_file(self, file_name):
        if file_name in self.files:
            print(f'Error: File {file_name} already exists.')
        else:
            with open(file_name, 'w') as file:
                file.write('')
            self.files.append(file_name)
            self.refresh_files()
            print(f'File {file_name} created successfully.')
            
    @exception_handler
    def delete_file(self, file_name):
        os.remove(file_name)
        self.files.remove(file_name)
        self.refresh_files()
        print(f'File {file_name} deleted successfully.')
        
    @exception_handler
    def rename_file(self, old_name, new_name):
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.refresh_files()
        print(f'File {old_name} renamed to {new_name} successfully.')
        
    @exception_handler
    def move_file(self, file_name, new_path):
        shutil.move(file_name, new_path)
        self.files.remove(file_name)
        self.refresh_files()
        print(f'File {file_name} moved to {new_path} successfully.')

    @exception_handler
    def copy_file(self, file_name, new_path, max_copies=10):
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
            print(f'File {file_name} copied to {os.path.join(base_path, file)} successfully.')
        else:
            print(f'Error: Maximum number of copies ({max_copies}) reached.')

        if base_path == self.path:
            self.refresh_files()

    @exception_handler        
    def create_directory(self, directory_name):
        if directory_name in self.files:
            print(f'Error: Directory {directory_name} already exists.')
        else:
            
            os.mkdir(directory_name)
            self.files.append(directory_name)
            self.refresh_files()
            print(f'Directory {directory_name} created successfully.')

    @exception_handler       
    def delete_directory(self, directory_name):
        shutil.rmtree(directory_name)
        self.files.remove(directory_name)
        self.refresh_files()
        print(f'Directory {directory_name} deleted successfully.')
        

    @exception_handler
    def rename_directory(self, old_name, new_name):
        os.rename(old_name, new_name)
        self.files.remove(old_name)
        self.files.append(new_name)
        self.refresh_files() 
        print(f'Directory {old_name} renamed to {new_name} successfully.')
        
    @exception_handler
    def move_directory(self, directory_name, new_path):
        shutil.move(directory_name, new_path)
        self.refresh_files()
        print(f'Directory {directory_name} moved to {new_path} successfully.')
    
    @exception_handler
    def copy_directory(self, directory_name, new_path, max_copies=10):
        
        base_path, directory = os.path.split(new_path)
        if base_path == '' or base_path == '.':
            base_path = self.path  # Same directory

        original_directory = directory
        counter = 1
        while os.path.exists(os.path.join(base_path, directory)) and counter <= max_copies:
            directory = f"{original_directory}_copy{counter}"
            counter += 1

        if counter <= max_copies:
            try:
                shutil.copytree(os.path.join(self.path, directory_name), os.path.join(base_path, directory))
                print(f'Directory {directory_name} copied to {os.path.join(base_path, directory)} successfully.')
            except shutil.Error as e:
                print(f'Directory not copied. Error: {e}')
            except OSError as e:
                print(f'Directory not copied. Error: {e}')
        else:
            print(f'Error: Maximum number of copies ({max_copies}) reached.')

        if base_path == self.path:
            self.refresh_files()


    @exception_handler
    def list_directories(self):
        directories = []
        for file in self.files:
            if os.path.isdir(file):
                directories.append(file)
        return directories




class CLI:
    def __init__(self):
        self.file_manager = FileManager()

    def welcome_message(self):
        print('Welcome to the File Management System!')
        self.display_menu()

    def display_menu(self):
        print('Please choose an option:')
        print('1. List files')
        print('2. Create file')
        print('3. Delete file')
        print('4. Rename file')
        print('5. Move file')
        print('6. Copy file')
        print('7. Create directory')
        print('8. Delete directory')
        print('9. Rename directory')
        print('10. Move directory')
        print('11. Copy directory')
        print('12. List directories')
        print('13. Exit')
        self.handle_input()

    def handle_input(self):
        choice = input('Enter your choice: ')
        if choice == '1':
            self.list_files()
        elif choice == '2':
            self.create_file()
        elif choice == '3':
            self.delete_file()
        elif choice == '4':
            self.rename_file()
        elif choice == '5':
            self.move_file()
        elif choice == '6':
            self.copy_file()
        elif choice == '7':
            self.create_directory()
        elif choice == '8':
            self.delete_directory()
        elif choice == '9':
            self.rename_directory()
        elif choice == '10':
            self.move_directory()
        elif choice == '11':
            self.copy_directory()
        elif choice == '12':
            self.list_directories()
        elif choice == '13':
            exit()
        else:
            print('Invalid choice. Please try again.')
        self.display_menu()

    def list_files(self):
        self.file_manager.refresh_files()
        files = self.file_manager.list_files()
        print('Files in the current directory:')
        for file in files:
            print(file)
    
    def create_file(self):
        file_name = input('Enter the name of the file you would like to create: ')
        self.file_manager.create_file(file_name)
        print(f'File {file_name} created successfully.')
        self.display_menu()
    
    def delete_file(self):
        file_name = input('Enter the name of the file you would like to delete: ')
        self.file_manager.delete_file(file_name)
        print(f'File {file_name} deleted successfully.')
        self.display_menu()
    
    def rename_file(self):
        old_name = input('Enter the name of the file you would like to rename: ')
        new_name = input('Enter the new name for the file: ')
        self.file_manager.rename_file(old_name, new_name)
        print(f'File {old_name} renamed to {new_name} successfully.')
        self.display_menu()

    def move_file(self):
        file_name = input('Enter the name of the file you would like to move: ')
        new_path = input('Enter the new path for the file: ')
        self.file_manager.move_file(file_name, new_path)
        print(f'File {file_name} moved to {new_path} successfully.')
        self.display_menu()

    def copy_file(self):
        file_name = input('Enter the name of the file you would like to copy: ')
        new_path = input('Enter the new path for the file: ')
        self.file_manager.copy_file(file_name, new_path)
        print(f'File {file_name} copied to {new_path} successfully.')
        self.display_menu()
    
    def create_directory(self):
        directory_name = input('Enter the name of the directory you would like to create: ')
        self.file_manager.create_directory(directory_name)
        print(f'Directory {directory_name} created successfully.')
        self.display_menu()
    
    def delete_directory(self):
        directory_name = input('Enter the name of the directory you would like to delete: ')
        self.file_manager.delete_directory(directory_name)
        print(f'Directory {directory_name} deleted successfully.')
        self.display_menu()

    def rename_directory(self):
        old_name = input('Enter the name of the directory you would like to rename: ')
        new_name = input('Enter the new name for the directory: ')
        self.file_manager.rename_directory(old_name, new_name)
        print(f'Directory {old_name} renamed to {new_name} successfully.')
        self.display_menu()
    
    def move_directory(self):
        directory_name = input('Enter the name of the directory you would like to move: ')
        new_path = input('Enter the new path for the directory: ')
        self.file_manager.move_directory(directory_name, new_path)
        print(f'Directory {directory_name} moved to {new_path} successfully.')
        self.display_menu()
    
    def copy_directory(self):
        directory_name = input('Enter the name of the directory you would like to copy: ')
        new_path = input('Enter the new path for the directory: ')
        self.file_manager.copy_directory(directory_name, new_path)
        print(f'Directory {directory_name} copied to {new_path} successfully.')
        self.display_menu()
    
    def list_directories(self):
        directories = self.file_manager.list_directories()
        print('Directories in the current directory:')
        for directory in directories:
            print(directory)
        self.display_menu()

    def exit(self):
        exit()


if __name__ == '__main__':
    file_manager = FileManager()
    cli = CLI(file_manager)
    cli.welcome_message()