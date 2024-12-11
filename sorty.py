# code by Karthik M Prakash (mkarthikprakash.work@gmail.com)
# Reference (https://medium.com/swlh/automation-python-organizing-files-5d2b6b933402)

# Libraries Required 
import os                   # Library contains all the functions that returns system dependent functionality
from shutil import move     # Imports move function from shell utilities


#user  = os.getlogin()            # defining the current username 
user  = 'User' 

#root_dir = '/Users/{}/Downloads/'.format(user)      # Defining the root folder which we want to work on i.e Downloads folder here

Folders = ['Images','Documents','Videos','Softwares','Compressed','Codes','Databases']  # Declaring names of all the folders for sorted_files 
 
# Code block to check if the folder already exisits , if not create with the name 
def create_folder(_source_dir):
    print("Create folder")
    for Folder in Folders:
        _path = _source_dir + "/" + Folder
        print(_path)
        if not(os.path.exists(_path)):
            print("Not exist: " + _path)
            os.mkdir(_path)

image_dir = '/Users/{}/Downloads/Images/'.format(user)
document_dir = '/Users/{}/Downloads/Documents/'.format(user)
code_dir = '/Users/{}/Downloads/Codes/'.format(user)
software_dir = '/Users/{}/Downloads/Softwares/'.format(user)
compressed_dir = '/Users/{}/Downloads/Compressed/'.format(user)
database_dir = '/Users/{}/Downloads/Databases/'.format(user)
video_dir = '/Users/{}/Downloads/Videos/'.format(user)

# category wise file types 
doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx', '.md','.rtf','.tex','.pem')
img_types = ('.cr2','.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif', '.tiff','.psd','.bmp')
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
def move_files(_source_dir, files):
    count = 0
    for file in files:
        source_file_dir = os.path.join(_source_dir,file)
        count = count + 1
        print("Process file number: " + str(count))
        if is_file_open(source_file_dir):
            print("File  is being open, skip"+ source_file_dir)
            continue
        try:
            if file.lower().endswith(doc_types):
                #dest_dir = /Users/{}/Documents/Images/'.format(user)
                dest_dir = _source_dir + '/Documents'
            
            elif file.lower().endswith(img_types):
                #dest_dir = '/Users/{}/Downloads/Images/'.format(user)
                dest_dir = _source_dir + '/Images'
            
            elif file.lower().endswith(video_types):
                #dest_dir = '/Users/{}/Downloads/Videos/'.format(user)
                dest_dir = _source_dir + '/Videos'

            elif file.lower().endswith(software_types):
                #dest_dir = '/Users/{}/Downloads/Softwares/'.format(user)
                dest_dir = _source_dir + '/Softwares'
            
            elif file.lower().endswith(compressed_types):
                #dest_dir = '/Users/{}/Downloads/Compressed/'.format(user)
                dest_dir = _source_dir + '/Compressed'
            
            elif file.lower().endswith(programming_types):
                #dest_dir = '/Users/{}/Downloads/Codes/'.format(user)
                dest_dir = _source_dir + '/Codes'
            elif file.lower().endswith(database_types):
                #dest_dir = '/Users/{}/Downloads/Databases/'.format(user)
                dest_dir = _source_dir + '/Databases'
            else : 
                continue
            print("move: " + os.path.join(_source_dir,file))
            print("destination dir: " + dest_dir)
            move(os.path.join(_source_dir,file),dest_dir)
            
        except IOError as emsg:
            print(emsg)
            pass

def buton_sorty(source_dir):
    print("In sorty")
    create_folder(source_dir)
    files = get_non_hidden_files(source_dir) 
    move_files(source_dir, files)

# Calling the sorting function if particularly running this file
if __name__ == "__main__":
    files = get_non_hidden_files(root_dir) 
    move_files(files)


#Uncomment code below for debugging 

#print(files) 







