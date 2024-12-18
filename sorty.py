# code by Karthik M Prakash (mkarthikprakash.work@gmail.com)
# Reference (https://medium.com/swlh/automation-python-organizing-files-5d2b6b933402)

# Libraries Required 
import os                   # Library contains all the functions that returns system dependent functionality
from shutil import move     # Imports move function from shell utilities
import subprocess
import re

#user  = os.getlogin()            # defining the current username 
user  = 'User' 

#root_dir = '/Users/{}/Downloads/'.format(user)      # Defining the root folder which we want to work on i.e Downloads folder here

Folders = ['Images','Documents','Videos','Softwares','Compressed','Codes','Databases']  # Declaring names of all the folders_list for sorted_files 
 
# Code block to check if the folder already exisits , if not create with the name 
def create_folder(_source_dir):
    print("Create folder")
    for Folder in Folders:
        _path = _source_dir + "/" + Folder
        print(_path)
        if not(os.path.exists(_path)):
            print("Not exist: " + _path)
            os.mkdir(_path)
        else:
            print("Already exists, skip creating folder: " + _path)

image_dir = '/Users/{}/Downloads/Images/'.format(user)
document_dir = '/Users/{}/Downloads/Documents/'.format(user)
code_dir = '/Users/{}/Downloads/Codes/'.format(user)
software_dir = '/Users/{}/Downloads/Softwares/'.format(user)
compressed_dir = '/Users/{}/Downloads/Compressed/'.format(user)
database_dir = '/Users/{}/Downloads/Databases/'.format(user)
video_dir = '/Users/{}/Downloads/Videos/'.format(user)

# category wise file types 
doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx', '.md','.rtf','.tex','.pem')
img_types = ('.cr2','.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif', '.tiff','.psd','.bmp', '.webp')
video_types= ('.3gp','.mkv','.avi','.mov','.mpg','.mpeg','.wmv','.h264', '.mp4')
software_types = ('.exe','.msi')
compressed_types =('.zip','.tar','.rar','.iso','.7z')
programming_types= ('.py','.ino','.m','.java','.js','.html','.htm','.css','.cgi','.sh','.swift','.h','.cpp','.cs')
database_types=('.csv','.dat','.db','.log','.mdb','.sav','.sql','.tar','.xml')

# Function to get all the files in the Downloads folder as a list
def get_non_hidden_files(root_dir):
    return [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir,f)) and not f.startswith('.')] 

def is_file_open(file_path):
    try:
        # Try opening the file in exclusive mode
        with open(file_path, 'r+'):
            return False  # File is not open by another process
    except IOError:
        return True  # File is open by another process
    
# Function to move files to their respective directories 
# Todo: Write code check condition and pattern than else if.

def func_organize_files(_source_dir, files):
    count = 0
    # reset the file list
    doc_file_list = []
    img_file_list = []
    video_file_list = []
    software_file_list = []
    database_types_file_list = []
    programming_types_file_list = []
    compressed_file_list = []
    for file in files:
        source_file_dir = os.path.join(_source_dir,file)
        count = count + 1
        print("Process file number: " + str(count))
        if is_file_open(source_file_dir):
            print("File  is being open, skip: "+ source_file_dir)
            continue
        try:
            if file.lower().endswith(doc_types):
                #dest_dir = /Users/{}/Documents/Images/'.format(user)
                doc_file_list.append(file)
                dest_dir = _source_dir + '/Documents'
            
            elif file.lower().endswith(img_types):
                #dest_dir = '/Users/{}/Downloads/Images/'.format(user)
                dest_dir = _source_dir + '/Images'
                img_file_list.append(file)

            elif file.lower().endswith(video_types):
                #dest_dir = '/Users/{}/Downloads/Videos/'.format(user)
                dest_dir = _source_dir + '/Videos'
                video_file_list.append(file)

            elif file.lower().endswith(software_types):
                #dest_dir = '/Users/{}/Downloads/Softwares/'.format(user)
                dest_dir = _source_dir + '/Softwares'
                software_file_list.append(file)

            elif file.lower().endswith(compressed_types):
                #dest_dir = '/Users/{}/Downloads/Compressed/'.format(user)
                dest_dir = _source_dir + '/Compressed'
                compressed_file_list.append(file)

            elif file.lower().endswith(programming_types):
                #dest_dir = '/Users/{}/Downloads/Codes/'.format(user)
                dest_dir = _source_dir + '/Codes'
                programming_types_file_list.append(file)

            elif file.lower().endswith(database_types):
                #dest_dir = '/Users/{}/Downloads/Databases/'.format(user)
                dest_dir = _source_dir + '/Databases'
                database_types_file_list.append(file)

            else : 
                continue
            print("move: " + os.path.join(_source_dir,file))
            print("destination dir: " + dest_dir)
            move(os.path.join(_source_dir,file),dest_dir)
            
        except IOError as emsg:
            print(emsg)
            pass
    #print(doc_file_list)

def get_all_folder_names(input_folder):
    """
    Get all folder names in the specified input folder.

    Parameters:
        input_folder (str): Path to the input folder.

    Returns:
        list: A list of folder names within the input folder.
    """
    folder_names = []
    try:
        # Iterate over all items in the input folder
        for item in os.listdir(input_folder):
            item_path = os.path.join(input_folder, item)
            # Check if the item is a directory
            if os.path.isdir(item_path):
                folder_names.append(item_path)
    except FileNotFoundError:
        print(f"Error: The folder '{input_folder}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied to access '{input_folder}'.")
    return folder_names

# ChatGPT
def get_git_remote_author(folder_path):
    """
    Retrieves the remote repository owner based on the 'origin' URL.

    Parameters:
        folder_path (str): Path to the Git repository.

    Returns:
        str: The repository owner name (if available).
    """
    try:
        # Get the remote URL
        remote_url = subprocess.check_output(
            ['git', '-C', folder_path, 'remote', 'get-url', 'origin'],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()

        # Extract the username/repository owner for GitHub/GitLab URLs
        match = re.search(r'github\.com[:/](.*?)/', remote_url)
        if match:
            return match.group(1)  # Return the repository owner

        return f"Remote URL: {remote_url} (Unable to determine owner)"

    except subprocess.CalledProcessError:
        return "Error: Not a Git repository or 'origin' not set."
    
def is_git_folder(folder_path):
    """
    Check if a folder is a Git repository by looking for the '.git' folder.

    Parameters:
        folder_path (str): Path to the folder to check.

    Returns:
        bool: True if the folder is a Git repository, False otherwise.
    """
    git_path = os.path.join(folder_path, '.git')
    return os.path.isdir(git_path)

def func_organize_folders(_source_dir, _folders_list):
    print("In func_organize_folders")
    print(_folders_list)
    other_git_project_file_list = []
    thong_git_project_file_list = []
    for folder_path in _folders_list:
        print(folder_path)
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            continue
        if is_git_folder(folder_path):
            print(f"The folder '{folder_path}' is a Git repository.")
            git_author_info = get_git_remote_author(folder_path)
            print(f"Repository Owner: {git_author_info}")
            if git_author_info == 'dinhthong':
                thong_git_project_file_list.append(folder_path)
            else:
                other_git_project_file_list.append(folder_path)
            continue
        else:
            print(f"The folder '{folder_path}' is NOT a Git repository.")
    print(thong_git_project_file_list)
    print(other_git_project_file_list)

def button_clean_up_files_sorty(source_dir):
    print("In sorty")
    create_folder(source_dir)
    files = get_non_hidden_files(source_dir) 
    func_organize_files(source_dir, files)


def button_clean_up_folders_sorty(source_dir):
    print("In button_clean_up_folders_sorty")
    folders_list = get_all_folder_names(source_dir)
    func_organize_folders(source_dir, folders_list)

# Calling the sorting function if particularly running this file
if __name__ == "__main__":
    files = get_non_hidden_files(root_dir) 
    func_organize_files(files)


#Uncomment code below for debugging 

#print(files) 







