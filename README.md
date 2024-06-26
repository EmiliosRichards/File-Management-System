# File Management System Project

Hello and welcome! This document contains insight into my process of designing and building a simple File Manager! 

If you would like to jump straight into using the File Management System find out how [here](https://example).


# Document Contents

- **Project Significance**: What is a File Management System and why build your own custom File Management System
- **Design Phase + Technical Insights**: This section will discuss some challenges I faced, what I did to overcome them.
- **Technical Insights**: For all you nerds out there! This section will talk about technical considerations.
- **Building Process**: Duri
- **Reflection**: During this section, we will discuss the end product, some expectations that did not turn out as planned, and all the lessons I learned on the way.
- **Conclusion**: Here you will find a summary of the project, how you can contribute, as well as new things I will work on in the future.





# Project Significance

## What is a File Management System?

A File Management System (FMS) enables users to manage and organise digital files efficiently. Popular examples include Windows' File Explorer and macOS's Finder. These applications offer users a wide range of management tools through a clean and intuitive interface, enhancing usability and functionality. Core FMS functions include creating, moving, renaming, deleting files and folders.


## The Why?

You might wonder, 'Why create a custom FMS with options like File Explorer and Finder available?' The answer lies in the unique learning opportunities and the abiblity to surpass the limitations of traditional systems. 

A custom built FMS provides the following opportunities:

- **Edicational Tool**: A lesson in object oriented programming, file IO, and exception handling.
- **Customized Workflow**: Create tailor made functionalities for specific needs.
- **Cross Platform Compatibility**: Can be designed to work across different operating systems.
- **Automation**: Automate routine tasks.
- **Learning and Experimentation**: The development of such a system can serve as a sandbox for experimenting with python libraries, exploring data structures, and building user interfaces.


# Design Phase

## Project Overview

**Project Statement and Scope**: The goal of this project is to develop a custom built file management system with python, utilising object oriented programming techniques. This process will also invlove the implementation of File IO operations and exception handling.

**Objective**: The objective of this project is to apply the python concepts mentioned above to create a user friendly custom built file management system. This system will be designed to store, retrieve, and manage documents or records in the form of text files, acting as a simple database.

**Philosophy of project**: Start Small: Begin with core functionalities that are common to all operating systems, and gradually expand features and capabilities.

## Tools and Libraries

### Development Environment
- **Python**: This projects primary programming language, known for its readability and broad support for tasks ranging from web development to automation.
- **GitHub**: Used for version control, tracking changes, and managing project iterations.
- **Coding IDE**: Essential for writing, testing, and debugging code. Use of an IDE that supports Python and integrates well with GitHub allows for seamless development.

### Key Libraries
- **os**: Utilized for handling basic operating system functionalities like reading and writing files, and directory manipulation.
- **shutil**: Helps in performing high-level file operations such as copying and moving files.
- **pathlib**: Offers an object-oriented approach to filesystem paths, making it easier to work with file paths across different operating systems.

## Functional Requirements

The File Management System must be able to:

- Create, read, update, and delete files (CRUD operations).
- Organizing files into directories based on categories or tags. Initially, the system will organize files into predefined categories such as 'Documents', 'Images', etc. Future updates will introduce the ability to create custom tags, enhancing personalization and search functionality.
- Searching for files based on name, content, categorie, tag, or metadata. Perfrom a non case-senstitive search in real-time.


## Non-Functional Requirements

The File Management System should:

- Work through the Command Line.
- Have a clean aesthetic with clear prompts and feedback messages. To acheive a 'clean aesthetic' it must be unclutted with a consistant format.
- Cross platform compatibility.
- Have intuitive commands and seamless exception handling. Commands must be labeled and located in a natural way keeping usage straightforward. 
- Uncluttered code built with the potential of expansion and modification in mind.


## Design and Architecture

### Basic Flow 

A simplified representation of how the File Manager will work:

1. Welcome message
2. Display available actions and corresponding number. 
3. Accept a number as input.
4. Prompt for any relevent additinal input.
5. Perform action. 

Constant: Cancel/ back + exit appliction functionality.

![Design Flowchart](https://github.com/EmiliosRichards/File-Management-System/blob/main/Files/Flowchart.png)

### Code Layout

1. Import required libraries. 
2. Define classes.
3. Implement file operations. 
4. Account for exeption handling.


**This covers the design phase of the project. Next, we will cover how to use the finished product, how I arrived at the completion of said product, and what I learned during the process of creating it.**



# Building Process


# Reflection




# Conclusion

## Future Work

## Contributions

Contributions are welcome! There are many ways you can contribute to this project:

- **Reporting Bugs**: If you find a bug, please open an issue in the GitHub repository, providing a detailed description of the bug and, if possible, steps to reproduce it.
- **Suggesting Enhancements**: Have ideas on how to improve the calculator? Open an issue to suggest new features or enhancements.
- **Submitting Pull Requests**: Feel free to fork the repository and submit pull requests with bug fixes or feature additions.

Please adhere to the following steps for your contributions to be considered:
- Fork the repository and create your branch from `main`.
- If you've added code, ensure it is well documented and tested.
- Ensure your commit messages clearly describe the changes.
- Open a pull request with a clear title and description.

For more information on how to contribute, please read the [Contributions.md](https://github.com/EmiliosRichards/File-Management-System/blob/main/Contributions.md) guide in our repository.

### Licence

This project is licensed under the MIT License - see the [LICENSE]([https://github.com/EmiliosRichards/File-Management-System/blob/main/LICENSE) file for details.

### Contact Information

If you have any questions or comments about the project, or if you're interested in contributing, feel free to reach out:

- **Project Maintainer**: Emilios Richards
- **Email**: emiliosmrichards@gmail.com
- **GitHub Profile**: [EmiliosRichards](https://github.com/EmiliosRichards)

### References

- **Python Official Documentation**: The Python documentation (https://docs.python.org/3/) was invaluable for understanding the standard libraries and functions.
- **Stack Overflow**: Various threads and discussions on Stack Overflow (https://stackoverflow.com/) provided solutions and insights for specific programming challenges encountered during the development of the project.
- **GitHub Docs**: The GitHub documentation (https://docs.github.com/en) was a guide for using Git and GitHub for version control and project management, ensuring best practices in code sharing and collaboration.
