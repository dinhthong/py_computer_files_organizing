# todo: Check folder content
import os
import sys
from array import *
from datetime import date
from datetime import datetime
import hashlib
import json
# define constant
c_ftdi_length = 8
c_temperatire_file_size = 157286400
g_allow_rename = 1
allow_print_debug_info = 1

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def print_header(s):
	print(bcolors.HEADER + s + bcolors.ENDC)

def print_warning(s):
	print(bcolors.WARNING + s + bcolors.ENDC)

def print_fail(s):
	print(bcolors.FAIL + s + bcolors.ENDC)
def print_ok(s):
	print(bcolors.OKCYAN + s + bcolors.ENDC)

def get_datetime_string():
	now = date.today()
	current_date = now.strftime("%Y_%m_%d")
	print_debug("Today's date:" + current_date)
	now = datetime.now()
	current_time = now.strftime("%H_%M_%S")
	#print("Current Time =", current_time)
	date_time_str = current_date+"T"+current_time
	#print(date_time_str)
	return date_time_str

# return 
# status 
def get_full_ftdi_from_string(file_name):
	# 06-Aug-21: Discard FTDIData*, FTDIGSK* and FTDIDevice*
	# Because in KNAN_software/State the program generates these file for some information, but it's not interested files
	ft_first_index = -1
	if file_name.find("FTDI") >= 0:
		return ft_first_index, ""
	ft_first_index = file_name.find("FT")
	
	if ft_first_index>=0:
		get_ftdi = file_name[ft_first_index:ft_first_index+c_ftdi_length]
		print_ok("FTDI: "+ get_ftdi)
	else:
		get_ftdi = ""
		print_fail("No FTDI string in file is found!, Please check folder content!")
	return ft_first_index, get_ftdi

def get_file_size(_file_fullpath):
	#file_fullpath = fullpath_src_folder + '/' + _fullpath_file
	print("Get file size: "+_file_fullpath)
	if os.path.exists(_file_fullpath)==True and os.path.isfile(_file_fullpath) == True:
		file_size = os.path.getsize(_file_fullpath)
		print_ok("File size = " + str(file_size))
		return file_size
	else:
		print_fail("Can't get file size")
		return -1

def print_check_file_content_message(_ok_temp_file_count, _ok_generated_file_count, _ok_log_file_count):
	temp_str = "_ok_temp_file_count: " + str(_ok_temp_file_count)+"/9"
	file_check_str = ""
	if _ok_temp_file_count == 9:
		print_ok(temp_str)
		file_check_str = "tO"
	else:
		print_fail(temp_str)
		file_check_str = "tF"
	temp_str = "_ok_generated_file_count: " + str(_ok_generated_file_count)+"/5"
	if _ok_generated_file_count == 5:
		print_ok(temp_str)
		file_check_str =file_check_str + "ntO"
	else:
		print_fail(temp_str)
		file_check_str = file_check_str + "ntF"
	temp_str ="_ok_log_file_count: " + str(_ok_log_file_count)+"/1"
	if _ok_log_file_count == 1:
		print_ok(temp_str)
		file_check_str =file_check_str + "logO"
	else:
		print_fail(temp_str)
		file_check_str = file_check_str + "logF"
	return file_check_str

def check_standard_files_count(file_count):
	print("File count: " + str(file_count))
	if file_count == 0:
		print_fail("Folder empty!")
	else:
		if file_count == 15:
			print_ok("File count ok")
		else:
			print_fail("File count error")

def check_nuc_file_name_and_size(_fname, _fsize):
	if _fname.find(".bin") != -1:
		underscore_index_list = find(_fname, "_")
		if len(underscore_index_list)==2:
			if _fsize==c_temperatire_file_size:
				print_ok("Temperature file size ok")
				return 1
			else:
				print_fail("Temperature file size NOT ok")
				return -1
		else:
			print("output file")
			return 2
	elif _fname.find(".txt"):
		print("Log file detected")
		return 3

def rename_dir(_src, _des):
	print("Rename src dir: " + _src)
	print("Rename des dir: " + _des)
	if g_allow_rename == 1:
		try:
			os.rename(_src, _des)
			print("Dir name (moved) changed sucessfully")
			print("New name: "+_des)
		except OSError:
			print_fail("Error rename, check files/folders!")
	else:
		print("Dir name isn't changed")

def print_debug(s):
	if allow_print_debug_info==1:
		print(bcolors.OKBLUE + "Debug: " + s + bcolors.ENDC)

def get_json_file_name():
	json_file_name = "log_"+ get_datetime_string() +".json"
	if os.path.exists(json_file_name):
		os.remove(json_file_name)
		print_ok("Delete the file ok")
	else:
		print("Can not delete the file as it doesn't exists")
		f = open(json_file_name, 'a+')
		f.close()
	return json_file_name
# program related utils

# Description: check file name and file size 
def check_temperature_file(_nuc_file_fullpath):
	if os.path.isfile(_nuc_file_fullpath):
		return True
	else: 
		print("Not file")

def check_file_count(file_count):
	print("File count: " + str(file_count))
	if file_count == 0:
		print_fail("Folder empty!")
	else:
		if file_count == 15:
			print_ok("File count ok")
		else:
			print_fail("File count error")

def read_and_get_match_dict_by_ftdi_in_json_file(file_name, _input_ftdi):
	#import json
	print("Getting matched dict by ftdi: " + _input_ftdi)
	# Opening JSON file
	#f = open(file_name, "r")
	if os.path.isfile(file_name):
		f = open(file_name, "r")
	else:
		print("File doesn't exist")
		f = open(file_name, 'a+')
	try: 
		dict_lists = json.load(f)
	except ValueError as e:
		print(e)
		f.close()
		print("Reading current file" + file_name + " not success")
		return -1
	dict_searched_by_ftdi = {}
	try:
		dict_searched_by_ftdi = next(item for item in dict_lists if item["FTDI"] == _input_ftdi)
	except:
		print("Can't find corresponding dev_serial from: " + _input_ftdi)
		f.close()
		return -1
	# Closing file
	f.close()
	print("Match dictionary value: " + str(dict_searched_by_ftdi))
	return dict_searched_by_ftdi

def read_and_get_match_dict_by_devserial_in_json_file(file_name, _input_dev_serial):
	#import json
	print("Getting matched dict by dev_serial: " + str(_input_dev_serial))
	# Opening JSON file
	f = open(file_name, "r")
	try: 
		dict_lists = json.load(f)
	except ValueError as e:
		print(e)
		f.close()
		print("Reading current .JSON file:" + file_name + " not success")
		return -1
	dict_searched_by_devserial = {}
	try:
		dict_searched_by_devserial = next(item for item in dict_lists if item["dev_serial"] == _input_dev_serial)
	except:
		print("Can't find corresponding dev_serial from: " + str(_input_dev_serial))
		f.close()
		return -1
	# Closing file
	f.close()
	print("Match dictionary value: " + str(dict_searched_by_devserial))
	return dict_searched_by_devserial

def read_and_get_match_dict_by_devserial_in_list(_list, _input_dev_serial):
	dict_searched_by_devserial = {}
	try:
		dict_searched_by_devserial = next(item for item in _list if item["dev_serial"] == _input_dev_serial)
		match_index = next((i for i, item in enumerate(_list) if item["dev_serial"] == _input_dev_serial), None)
	except:
		print("Can't find corresponding dev_serial from: " + str(_input_dev_serial))
		return [-1, {}]
	print("Match dictionary value: " + str(dict_searched_by_devserial))
	
	return [match_index, dict_searched_by_devserial]

def read_and_get_match_dict_by_devserial_and_md5_in_list(_list, _input_dev_serial, _md5):
	dict_searched_by_devserial = {}
	if _md5 == "":
		return -1
	try:
		dict_searched_by_devserial = next(item for item in _list if item["dev_serial"] == _input_dev_serial and item["FTDI1.bin_md5"] == _md5)
	except:
		print("Can't find corresponding dev_serial from: " + str(_input_dev_serial))
		return -1
	print("Match dictionary value: " + str(dict_searched_by_devserial))
	return dict_searched_by_devserial

# Create if not exist
# if the FTDI is in database -> extract the dev serial number
def create_data_FTDI_folder(base, ftdi):
	#get_datetime_string()
	return_dict = read_and_get_match_dict_by_ftdi_in_json_file("ftdi_dev_pair.json", ftdi)
	if return_dict != -1:
		ftdi_folder_path = os.path.join(base, str(return_dict["dev_serial"]) + "_" + ftdi + "_" + "anew")
	else:
		ftdi_folder_path = os.path.join(base, "data_" + ftdi)
	try:
		os.mkdir(ftdi_folder_path) 
	except OSError as error: 
		print(error)
	return ftdi_folder_path

# item_fullpath_list: [D:/py_test_KNAN_software\\data_FT5P145V', 'D:/py_test_KNAN_software\\data_FT5P31ZZ', 'D:/py_test_KNAN_software\\FT5P145V1.bin']
# full_des_dir: full destination folder
def create_ftdi_folders_and_move_ftdi_files(item_fullpath_list, full_des_dir):
	count = 1
	for full_item_dir in item_fullpath_list:
		print_header("***STT: " + str(count))
		count = count + 1
		#item_fullpath = base_dir + '/' + each_item_folder_name
		print(full_item_dir)
		last_part_of_dir = os.path.basename(os.path.normpath(full_item_dir))
		if os.path.isfile(full_item_dir) == True:
			get_ftdi_ok, extracted_ftdi = get_full_ftdi_from_string(full_item_dir)
			if get_ftdi_ok != -1:
				print("Extracted ftdi: " + extracted_ftdi)
				new_ftdi_folder = create_data_FTDI_folder(full_des_dir, extracted_ftdi)
				file_type = check_nuc_file_name_and_size(full_item_dir, get_file_size(full_item_dir))
				new_file_path = os.path.join(new_ftdi_folder, last_part_of_dir)
				rename_dir(full_item_dir, new_file_path)
		print_header("--------------------------------------------------------------------------------------------")

# Remove string after # character
# VD: D:\Dulieu_NUC_KNAN\fromOneDrive_PC_HDD\031_FT5P10Z3_ok#dasda
# @return: same if there's no '#' character in name
def remove_original_app_msg(dir_name, rename_flag):
	first_status_index = dir_name.find("#")
	new_name = dir_name
	if first_status_index>=0:
		new_name = dir_name[0:first_status_index]
		print_debug(new_name)
		if rename_flag == 1:
			rename_dir(dir_name, new_name)
	return new_name

def append_checkmsg_to_folder_name(st, _dir_full_path):
	new_folder_name = remove_original_app_msg(_dir_full_path, 1)
	end_str = "#" + st
	if new_folder_name == _dir_full_path: # there's no '#' character in name
		_nn = _dir_full_path+end_str
		rename_dir(_dir_full_path, _nn)
	else:
		_nn = new_folder_name+end_str
		rename_dir(new_folder_name, _nn)
	return _nn

# https://www.kite.com/python/answers/how-to-generate-an-md5-checksum-of-a-file-in-python
def calculate_md5_hash(_file_full_dir):
	print("calculate MD5")
	md5_hash = hashlib.md5()

	try:
		a_file = open(_file_full_dir, "rb")
		content = a_file.read()
		md5_hash.update(content)
		digest = md5_hash.hexdigest() 
	except:
		print_debug("Calculate hash failed")
		digest = -1
	print_debug("MD5 hash: " + str(digest))
	return digest