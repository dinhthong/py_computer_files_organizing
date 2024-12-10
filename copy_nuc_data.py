# todo: Check folder content
import os
from array import *
from utils import *
import json
from shutil import copyfile

# _parent_folder: D:\py_test_KNAN_software: folder contains folders, each folders is deviceserial_FTDI: contains files
def extract_files_in_childfolders(_parent_folder):
	root_folder_ls_list = os.listdir(_parent_folder)
	# each_item_folder_name: 056_FT5OV9NG_ok
	jfilename = get_json_file_name()
	jsonFile = open(jfilename, "w")
	for each_item_folder_name in root_folder_ls_list:
		nuc_folder_fullpath = os.path.join(_parent_folder, each_item_folder_name)
		if os.path.isdir(nuc_folder_fullpath) == True:
			nuc_folder_fullpath_ls = os.listdir(nuc_folder_fullpath)
			count = 0
			for file_in_folder_item in nuc_folder_fullpath_ls:
				#full_file_dir = os.path.join(nuc_folder_fullpath, file_in_folder_item)
				get_ftdi_ok, extracted_ftdi = get_full_ftdi_from_string(file_in_folder_item)
				if get_ftdi_ok != -1:
					json_info_dict = {}
					count = count + 1
					print_header("***STT: " + str(count))
					json_info_dict['STT'] = count
					nuc_file_fullpath = os.path.join(nuc_folder_fullpath, file_in_folder_item)
					print(nuc_file_fullpath)
					if check_temperature_file(nuc_file_fullpath) == True:
						print("nuc_file_fullpath: " + nuc_file_fullpath)
						json_info_dict['original_path'] = nuc_file_fullpath
						new_file_path = os.path.join(_parent_folder, file_in_folder_item)
						print("new_file_path: " + new_file_path)
						json_info_dict['destination_path'] = new_file_path
						os.rename(nuc_file_fullpath, new_file_path)
						print(json_info_dict)
					jsonString = json.dumps(json_info_dict, indent=2, separators=(',', ': '))
					jsonFile.write(jsonString)
		else:
			print_header("Not folder")
		# check_individual_nuc_folder_files(_base_dir_name, each_item_folder_name)
	jsonFile.close()

def arrange_nuc_files_to_folder(knan_software_dir):
	full_item_dir_list = []
	for item in os.listdir(knan_software_dir):
		full_item_dir_list.append(os.path.join(knan_software_dir, item))
	#print_debug(full_item_dir_list)
	create_ftdi_folders_and_move_ftdi_files(full_item_dir_list, knan_software_dir)

#_base_folder = D:\Dulieu_NUC_KNAN\fromOneDrive_PC_HDD
# check if source folder contains [generated nuc_table files], if not skip creating folder
# @todos: don't copy duplicate folder (by checking first file's MD5 eg)
def duplicate_nuc_table_only(_base_folder, _des_folder):
	count = 0
	device_folder_item_list = os.listdir(_base_folder)
	len_device_folder_item_list = len(device_folder_item_list)
	for folder_item in device_folder_item_list:
		full_path = os.path.join(_base_folder, folder_item)
		new_folder = os.path.join(_des_folder, remove_original_app_msg(folder_item, 0))
		if os.path.isdir(full_path) == True:
			folder_create_done_flag = 0
			count = count + 1
			# create new destination folder
			print_ok("***STT: " + str(count) + "/" + str(len_device_folder_item_list))
			print_ok("Working in folder: " + full_path)
			for file_item in os.listdir(full_path):
				full_file_path = os.path.join(full_path, file_item)
				if os.path.isfile(full_file_path) == True:
					#only copy ftdi file
					if file_item.find('FT') >=0:
						underscore_index_list = find(file_item, "_")
						underscore_count = len(underscore_index_list)
						# only copy [generated nuc_table files]
						if underscore_count != 2:
							# create new destination folder and set flag
							if folder_create_done_flag == 0 and os.path.isdir(new_folder) == False:
								try:
									os.mkdir(new_folder)
									folder_create_done_flag = 1
								except OSError as error: 
									print(error)
							src_file = os.path.join(full_path, file_item)
							new_des = os.path.join(new_folder, file_item)
							if os.path.isfile(new_des) == True:
								print_warning("Destination file already exist, skip...")
							else:
								copyfile(src_file, new_des)
					else:
						print_warning("Not FTDI file, skip...")
	print_ok("Done")

def main():
	print("copy_nuc_data")

if __name__ == "__main__":
    main()