# todo: Check folder content
import os
from array import *
from utils import *
import json

# global vars
fullpath_src_folder = ""
underscore_index_list = []

def check_and_change_nucfolder_name(_filepath):
	global fullpath_src_folder
	#json code
	#jfilename= get_json_file_name()
	#jsonFile = open(jfilename, "w")
	count = 1
	root_folder_ls_list = os.listdir(_filepath)
	for each_item_folder_name in root_folder_ls_list:
		json_info_dict = {}
		first_ftdi_idx = 0
		good_name_flag = 0
		print_header("***STT: " + str(count))
		json_info_dict['STT'] = count
		count = count + 1
		#print(each_item_folder_name)
		fullpath_src_folder = os.path.join(_filepath, each_item_folder_name)
		print("Full _filepath: " + fullpath_src_folder)
		# all root_folder_ls_list and folder in fullpath_src_folder
		if os.path.isdir(fullpath_src_folder) == False:
			continue
		src_folder_ls = os.listdir(fullpath_src_folder)
		underscore_index_list = find(each_item_folder_name, "_")
		underscore_count = len(underscore_index_list)
		for tb_file in src_folder_ls:
			first_ftdi_idx, extracted_ftdi = get_full_ftdi_from_string(tb_file)
			if first_ftdi_idx != -1:
				break
		# check if folder name is already good
		if first_ftdi_idx >= 0:
			if underscore_count <= 0:
				# continue the for loop for this each_item_folder_name
				print_fail("Discard this for loop as no underscore found")
				continue
			if underscore_count >= 1:
				dev_serial = each_item_folder_name[0:underscore_index_list[0]]
				if dev_serial.isnumeric():
					pad_dev_serial = dev_serial.zfill(4)
					#print(dev_serial)
			if underscore_count == 1:
				new_folder_name = extracted_ftdi
				if (len(each_item_folder_name[underscore_index_list[0]:]) == c_ftdi_length+1) and len(dev_serial) == 4:
					good_name_flag = 1
			elif underscore_count >= 2:
				if (underscore_index_list[1]-underscore_index_list[0] == c_ftdi_length+1) and len(dev_serial) == 4:
					good_name_flag = 1
				new_folder_name = extracted_ftdi+each_item_folder_name[underscore_index_list[1]:]
			if good_name_flag == 1:
				print_ok("Discard this as the each_item_folder_name is already OK")
				continue
			new_fullpath_folder_name = os.path.join(_filepath, pad_dev_serial+"_"+new_folder_name)
			print("fullpath_src_folder: "+ fullpath_src_folder + "; new_fullpath_folder_name: " + new_fullpath_folder_name)
			# start rename
			if g_allow_rename == 1:
				try:
					os.rename(fullpath_src_folder, new_fullpath_folder_name)
					print("Folder name changed sucessfully")
				except OSError:
					print_fail("Error!")
			else:
				print("Folder name isn't change")
		else:
			print_fail("None valid FTDI file is found")
		# json_info_dict.update(dict_folder_info)
		# jsonString = json.dumps(json_info_dict, indent=2, separators=(',', ': '))
		# jsonFile.write(jsonString)
	# jsonFile.close()

# input: D:\Dulieu_NUC_KNAN\fromOneDrive_PC_HDD
def remove_status_msg_from_nuc_folder_name(_full_parentfolder_dir):
	count = 1
	root_folder_ls_list = os.listdir(_full_parentfolder_dir)
	for each_item_folder_name in root_folder_ls_list:
		print_header("***STT: " + str(count))
		count = count + 1
		full_nuc_folder_dir = os.path.join(_full_parentfolder_dir, each_item_folder_name)
		print(full_nuc_folder_dir)
		if os.path.isdir(full_nuc_folder_dir):
			remove_original_app_msg(full_nuc_folder_dir, 1)
		print_header("--------------------------------------------------------------------------------------------")

# Example data:
# _full_dir_path = D:\Dulieu_NUC_KNAN\fromOneDrive_PC_HDD\002_FT5P16DM
# _each_item_folder_ls_list = [FT5P16DM_190521_50.bin, FT5OUSZM_310521_30.bin, Log_FT5OUSZM.txt]
def get_ftdi_and_check_all_files(_full_dir_path, _each_item_folder_ls_list):
	print(" in func get_ftdi_and_check_all_files")
	done_get_ftdi_flag = 0
	ok_temp_file_count = 0
	ok_generated_file_count = 0
	ok_log_file_count = 0
	file_info_list = []
	# tb_file: FT5P16DM_190521_50.bin
	for tb_file in _each_item_folder_ls_list:
		this_file_info_dict = {}
		full_nuc_file_path = os.path.join(_full_dir_path, tb_file)
		this_file_info_dict['nuc_file_path'] = full_nuc_file_path
		file_type = -1
		if done_get_ftdi_flag == 0:
			get_ftdi_status, extracted_ftdi = get_full_ftdi_from_string(tb_file)
			if get_ftdi_status!=-1:
				done_get_ftdi_flag = 1
		if done_get_ftdi_flag == 1:
			file_size = get_file_size(full_nuc_file_path)
			this_file_info_dict['file_size'] = file_size
			file_type = check_nuc_file_name_and_size(tb_file, file_size)
			if file_type == 1:
				ok_temp_file_count = ok_temp_file_count + 1
			elif file_type == 2:
				ok_generated_file_count = ok_generated_file_count + 1
				# only calculate md5 of the first nuc_table file
				if ok_generated_file_count == 1:
					this_file_info_dict['md5'] = calculate_md5_hash(full_nuc_file_path)
			elif file_type == 3:
				ok_log_file_count = ok_log_file_count + 1
			this_file_info_dict['file_type'] = file_type
			
		file_info_list.append(this_file_info_dict)
	error_st = print_check_file_content_message(ok_temp_file_count, ok_generated_file_count, ok_log_file_count)
	new_folder_name = append_checkmsg_to_folder_name(error_st, _full_dir_path)
	return [extracted_ftdi, error_st, file_info_list, new_folder_name]
	# append check status message to end of folder name

# @INPUT: 
# _base_dir_name: D:/py_test_KNAN_software
# _nuc_dir_name:  061_FT5OV9HL_ok
# @RETURN LIST: [ftdi number, number of files, file name and check status,
# temperature files check status, output files check and status, Log files check and status, check result]
def check_individual_nuc_folder_files(_base_dir_name, _nuc_dir_name):
	this_info_dict = {}
	full_dir_path = os.path.join(_base_dir_name, _nuc_dir_name)
	print(full_dir_path)
	this_info_dict['dir_full_path'] = full_dir_path
	# all root_folder_ls_list and folder in fullpath_src_folder
	if os.path.isdir(full_dir_path):
		each_item_folder_ls_list = os.listdir(full_dir_path)
		each_item_folder_file_count = len(each_item_folder_ls_list)
		this_info_dict['file_count'] = each_item_folder_file_count
		check_standard_files_count(each_item_folder_file_count)
		if each_item_folder_file_count > 0:
			[this_ftdi, check_result, this_all_fileinfo_list, new_path] = get_ftdi_and_check_all_files(full_dir_path, each_item_folder_ls_list)
			this_info_dict['check_result'] = check_result
			this_info_dict['ftdi'] = this_ftdi
			this_info_dict['files_info_list'] = this_all_fileinfo_list
			this_info_dict['new_dir_full_path'] = new_path
	else:
		print("Not a dir")
	print_header("--------------------------------------------------------------------------------------------")
	return this_info_dict

# @description: Check folder's content and apend 
# _full_parentfolder_dir: D:\Dulieu_NUC_KNAN\fromOneDrive_PC_HDD
# root_folder_ls_list: [061_FT5OV9HL_ok, 097_FT5OUWNJ_cancheck]
def check_complete_nuc_folder(_base_dir_name):
	count = 0
	root_folder_ls_list = os.listdir(_base_dir_name)
	jfilename = get_json_file_name()
	jsonFile = open(jfilename, "w")
	json_info_dict = {"command": "check_complete_nuc_folder", "file_name": jfilename}
	jsonString = json.dumps(json_info_dict, indent=2, separators=(',', ': '))
	jsonFile.write(jsonString)
	# each_item_folder_name: 056_FT5OV9NG_ok
	for each_item_folder_name in root_folder_ls_list:
		print("Folder name: " + each_item_folder_name)
		status, FTDI = get_full_ftdi_from_string(each_item_folder_name)
		if status != -1:
			count = count + 1
			json_info_dict = {}
			print_header("***STT: " + str(count))
			json_info_dict['STT'] = count
			dict_folder_info = check_individual_nuc_folder_files(_base_dir_name, each_item_folder_name)
			json_info_dict.update(dict_folder_info)
			jsonString = json.dumps(json_info_dict, indent=2, separators=(',', ': '))
			jsonFile.write(jsonString)
		else:
			print("Not a FTDI folder, discard check folder's content")
	jsonFile.close()

def main():
	print("Hello World!")
	#check_complete_nuc_folder()

if __name__ == "__main__":
    main()