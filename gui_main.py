# Developed by ThongND
# Started in 2020
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import os
from configparser import ConfigParser
from change_ftdi_knan_name import *
from copy_nuc_data import *
from nuc_production import *
from sorty import *
#full_app_data_path = os.getcwd()+"\\...\\..."
full_app_data_path = os.getcwd()
# os.chdir('..')
# os.chdir('..')
full_app_data_path = os.getcwd()
pg_textfile_name = os.path.join(full_app_data_path, "config.ini")
print(pg_textfile_name)
config = ConfigParser()
# check and write text file
if os.path.exists(pg_textfile_name):
    print("Config already exists")
else:
    f = open(pg_textfile_name,"w+")
    f.close()

config.read(pg_textfile_name)

if config.has_section('main') == False:
    print("config.has_section('main') == False")
    config.add_section('main')
    config.set('main', 'nuc_base_dir', "")
    config.set('main', 'software_folder', "")
def submitact():
    user = Username.get()
    passw = password.get()
    #logintodb(user, passw)

root = Tk()

def btn_org_dir_cb():
    #print("Refreshing table")
    file_path_variable = search_for_file_path(dir_org_q.get())
    print ("\nfile_path_variable = ", file_path_variable)
    if file_path_variable != "":
        dir_org_q.set(file_path_variable)
        # write to config file
        # config.add_section('main')
        config.set('main', 'nuc_base_dir', file_path_variable)
        status_q.set("Change folder contains NUC folders to: " + file_path_variable)
    

def btn_soft_dir_cb():
    #print("Refreshing table")
    file_path_variable = search_for_file_path(dir_soft_q.get())
    print ("\nfile_path_variable = ", file_path_variable)
    if file_path_variable != "":
        dir_soft_q.set(file_path_variable)
        # write to config file
        # config.add_section('main')
        config.set('main', 'software_folder', file_path_variable)
        status_q.set("Change folder contains KNAN_Software to: " + file_path_variable)

def search_for_file_path(current_dir):
    #currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=current_dir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

wrapper0 = LabelFrame(root, text="Login")
wrapper1 = LabelFrame(root, text="main")
wrapper2 = LabelFrame(root, text="User action")
wrapper3 = LabelFrame (root, text="KNAN NUC TOOL")

wrapper0.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

lblfrstrow = tk.Label(wrapper0, text ="Username -", )
lblfrstrow.place(x = 50, y = 20)
 
Username = tk.Entry(wrapper0, width = 35)
Username.place(x = 150, y = 20, width = 100)
  
lblsecrow = tk.Label(wrapper0, text ="Password -")
lblsecrow.place(x = 50, y = 50)
 
password = tk.Entry(wrapper0, width = 35)
password.place(x = 150, y = 50, width = 100)

submitbtn = tk.Button(wrapper0, text ="Login", 
                      bg ='blue', command = submitact)
submitbtn.place(x = 150, y = 70, width = 55)

def search_btn_cb():
    print("Search button clicked")

# User action wrapper
btn_org_dir_object = tk.Button(wrapper2, text ="ORG_DIR", 
                       bg ='blue', command = btn_org_dir_cb)
btn_org_dir_object.place(x = 10, y = 10, width = 75)
# Search selection
# Search box
q = StringVar()
lbl = Label(wrapper2, text="Search")
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT, padx=6)

# Search button
btn = Button(wrapper2, text="Search", command=search_btn_cb)
btn.pack(side=tk.LEFT, padx=6) 

# Search box
dir_org_q = StringVar()
# lbl = Label(wrapper2, width=10, text="Selected dir")
# lbl.pack(side=tk.LEFT, padx=15)
ent2 = Entry(wrapper2, textvariable=dir_org_q)
ent2.pack(side=tk.LEFT, padx=6)
ent2.place(x=100, y=15, height=20, width=350)
dir_org_q.set(config.get('main', 'nuc_base_dir'))

# data_folder selection
btn_soft_dir_object = tk.Button(wrapper2, text ="SOFT_DIR", 
                       bg ='blue', command = btn_soft_dir_cb)
btn_soft_dir_object.place(x = 500, y = 40, width = 75)

dir_soft_q = StringVar()
ent_data = Entry(wrapper2, textvariable=dir_soft_q)
ent_data.pack(side=tk.LEFT, padx=6)
ent_data.place(x=600, y=40, height=20, width=350)
dir_soft_q.set(config.get('main', 'software_folder'))

# working log on GUI
status_q = StringVar()
status_q.set("HELLO")
lbl = Label(wrapper1, width=50, textvariable = status_q)
lbl.pack(side=tk.LEFT, padx=15)

# create new record wrapper
# https://www.kite.com/python/answers/how-to-make-an-array-of-strings-in-python
ftdi_dev_pair_json_dir = "ftdi_dev_pair.json"

def btn_extract_and_save_nuc_folder_info_to_json_file():
    print(dir_org_q.get())
    extract_and_save_nuc_folder_info_to_json_file(dir_org_q.get(), ftdi_dev_pair_json_dir)

# Define buttons
class button_action:
    this_btn = tk.Button()
    btn_text = ""
    callback_func = None
    def __init__(self, _btn_text, _callback_func):
        self.btn_text = _btn_text
        self.callback_func = _callback_func

    def create_button(self, _row, _col):
        self.this_btn = tk.Button(wrapper3, text = self.btn_text, 
                        bg ='#00ffff', command = self.do_when_button_clicked)
        self.this_btn.grid(row = _row, column=_col, pady = 20)

    def do_when_button_clicked(self):
        print("dir = " + dir_org_q.get())
        self.callback_func(dir_org_q.get())

class button_action2(button_action):
    def do_when_button_clicked(self):
        print("button_action2. work with SOURCE ")
        print("dir = " + dir_org_q.get())
        self.callback_func(dir_org_q.get())

class button_action_two_dir(button_action):
    def do_when_button_clicked(self):
        print("dir = " + dir_soft_q.get())
        self.callback_func(dir_org_q.get(), dir_soft_q.get())

button_clean_folder = button_action2("1. Clean up source folder sorty", buton_sorty)
button_clean_folder.create_button(2, 2)

btn_get_ftdi_and_dev_pair = tk.Button(wrapper3, text ="2. Extract NUC folder info to JSON file", 
                       bg ='#ffb3fe', command = btn_extract_and_save_nuc_folder_info_to_json_file)

btn_get_ftdi_and_dev_pair.grid(row = 3, column=2, pady = 20)

button_check_nuc_folder_in_org = button_action("3. Check NUC folder and append msg", check_complete_nuc_folder)
button_check_nuc_folder_in_org.create_button(4, 2)

button_rm_status_msg_in_org = button_action("4. Remove status msg (#)", remove_status_msg_from_nuc_folder_name)
button_rm_status_msg_in_org.create_button(5, 2)

# only use this to arrange files to folder
# the program only tries to search device serial pair and create a new folder based off the json file
# the program doens't know the output and result of these files (after generate NUC and download firmware)
btn_rm_status_msg_in_soft = button_action2("5. Copy all files to download folder", arrange_nuc_files_to_folder) 
btn_rm_status_msg_in_soft.create_button(2, 4)

btn_arr_nuc_files_infirstlevel_in_soft = button_action2("6. Arrange NUC files in SOFT first level", arrange_nuc_files_in_firstlevel_subfolder) 
btn_arr_nuc_files_infirstlevel_in_soft.create_button(3, 4)

btn_rm_status_msg_in_soft = button_action2("7. Extract NUC files in SOFT", extract_files_in_childfolders) 
btn_rm_status_msg_in_soft.create_button(4, 4)

btn_rm_status_msg_in_soft = button_action_two_dir("5. Copy nuc_table files from ORG to SOFT", duplicate_nuc_table_only) 
btn_rm_status_msg_in_soft.create_button(2, 3)

root.title("ThongND work utility tool")
root.geometry("1200x800")
#root.resizable(False, False)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        with open('config.ini', 'w') as f:
            config.write(f)
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()