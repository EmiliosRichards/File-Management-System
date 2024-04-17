import os
import shutil
import pathlib



class Document:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def get_file_content(self):
        try:
            with open(self.file_name, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f'Error: File {self.file_name} does not exist.'
        except PermissionError:
            return f'Error: You do not have permission to read {self.file_name}.'
        except Exception as e:
            return f'An unexpected error occurred: {e}'

    def write_to_file(self, content):
        try:
            with open(self.file_name, 'w') as file:
                file.write(content)
            return f'Content written to {self.file_name} successfully.'
        except FileNotFoundError:
            return f'Error: File {self.file_name} does not exist.'
        except PermissionError:
            return f'Error: You do not have permission to write to {self.file_name}.'
        except Exception as e:
            return f'An unexpected error occurred: {e}'
        
    def get_file_size(self):
        try:    
            return os.path.getsize(self.file_name)
        except FileNotFoundError:
            return f'Error: File {self.file_name} does not exist.'
        except PermissionError:
            return f'Error: You do not have permission to access {self.file_name}.'
        except Exception as e:
            return f'An unexpected error occurred: {e}'
        

class FileManager:
    def __init__(self):
        self.path = os.getcwd()
        self.files = os.listdir(self.path)
        self.needs_refresh = False    # This is a flag to check if the files list needs to be refreshed.

    def list_files(self):
        try:    
            return self.files
        except FileNotFoundError:
            return f'Error: Directory {self.path} does not exist.'
        except PermissionError:
            return f'Error: You do not have permission to access {self.path}.'
        except Exception as e:
            return f'An unexpected error occurred: {e}'


    def create_file(self, file_name):
        if file_name in self.files:
            print(f'Error: File {file_name} already exists.')
        else:
            try:
                with open(file_name, 'w') as file:
                    file.write('')
                self.files.append(file_name)
                self.needs_refresh = True
                print(f'File {file_name} created successfully.')
            except PermissionError:
                print(f'Error: You do not have permission to create {file_name}.')
            except Exception as e:
                print(f'An unexpected error occurred: {e}')
            

            

    def delete_file(self, file_name):
        try:
            os.remove(file_name)
            self.files.remove(file_name)
            self.needs_refresh = True
            print(f'File {file_name} deleted successfully.')
        except FileNotFoundError:
            print(f'Error: File {file_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to delete {file_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

    def rename_file(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            self.files.remove(old_name)
            self.files.append(new_name)
            self.needs_refresh = True
            print(f'File {old_name} renamed to {new_name} successfully.')
        except FileNotFoundError:
            print(f'Error: File {old_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to rename {old_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')


    def move_file(self, file_name, new_path):
        try:
            shutil.move(file_name, new_path)
            self.files.remove(file_name)
            self.needs_refresh = True
            print(f'File {file_name} moved to {new_path} successfully.')
        except FileNotFoundError:
            print(f'Error: File {file_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to move {file_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')


    def copy_file(self, file_name, new_path):
        try:
            shutil.copy(file_name, new_path)
            self.needs_refresh = True
            print(f'File {file_name} copied to {new_path} successfully.')
        except FileNotFoundError:
            print(f'Error: File {file_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to copy {file_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

            
    def create_directory(self, directory_name):
        if directory_name in self.files:
            print(f'Error: Directory {directory_name} already exists.')
        else:
            try:
                os.mkdir(directory_name)
                self.files.append(directory_name)
                self.needs_refresh = True
                print(f'Directory {directory_name} created successfully.')
            except PermissionError:
                print(f'Error: You do not have permission to create {directory_name}.')
            except Exception as e:
                print(f'An unexpected error occurred: {e}')
           
    def delete_directory(self, directory_name):
        try:
            shutil.rmtree(directory_name)
            self.files.remove(directory_name)
            self.needs_refresh = True
            print(f'Directory {directory_name} deleted successfully.')
        except FileNotFoundError:
            print(f'Error: Directory {directory_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to delete {directory_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')


    def rename_directory(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            self.files.remove(old_name)
            self.files.append(new_name)
            self.needs_refresh = True  
            print(f'Directory {old_name} renamed to {new_name} successfully.')
        except FileNotFoundError:
            print(f'Error: Directory {old_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to rename {old_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

    def move_directory(self, directory_name, new_path):
        try:
            shutil.move(directory_name, new_path)
            self.needs_refresh = True
            print(f'Directory {directory_name} moved to {new_path} successfully.')
        except FileNotFoundError:
            print(f'Error: Directory {directory_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to move {directory_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')


    def copy_directory(self, directory_name, new_path):
        try:
            shutil.copytree(directory_name, new_path)
            self.needs_refresh = True
            print(f'Directory {directory_name} copied to {new_path} successfully.')
        except FileNotFoundError:
            print(f'Error: Directory {directory_name} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to copy {directory_name}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')


    def list_directories(self):
        try:
            directories = []
            for file in self.files:
                if os.path.isdir(file):
                    directories.append(file)
            return directories
        except FileNotFoundError:
            return f'Error: Directory {self.path} does not exist.'
        except PermissionError:
            return f'Error: You do not have permission to access {self.path}.'
        except Exception as e:
            return f'An unexpected error occurred: {e}'
        
    def refresh_files(self):
        try:
            if self.needs_refresh:
                self.files = os.listdir(self.path)
                self.needs_refresh = False
        except FileNotFoundError:   
            print(f'Error: Directory {self.path} does not exist.')
        except PermissionError:
            print(f'Error: You do not have permission to access {self.path}.')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')



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