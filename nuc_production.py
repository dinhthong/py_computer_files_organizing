# todo: Check folder content
import os
import sys
from array import *
from utils import *
import json
import operator
# arrange in level 1 subfolders
def arrange_nuc_files_in_firstlevel_subfolder(full_parent_dir):
	for item in os.listdir(full_parent_dir):
		full_dir_path = os.path.join(full_parent_dir, item)
		if os.path.isdir(full_dir_path) == True:
			print(full_dir_path)
			full_item_dir_list = []
			for item in os.listdir(full_dir_path):
				full_item_dir_list.append(os.path.join(full_dir_path, item))
			create_ftdi_folders_and_move_ftdi_files(full_item_dir_list, full_parent_dir)
		else:
			print("Not a folder, skip...")

def extract_and_save_nuc_folder_info_to_json_file(_full_parent_dir, _json_file_name):
	print_debug("In function: extract_and_save_nuc_folder_info_to_json_file")
	# read the current json file and save to list
	if os.path.isfile(_json_file_name):
		f = open(_json_file_name, "r")
	else:
		print("File doesn't exist")
		f = open(_json_file_name, 'a+')
	try:
		extracted_ftdi_dev_list = json.load(f)
	except:
		extracted_ftdi_dev_list = []
	f.close()
	count = 0
	for folder_name in os.listdir(_full_parent_dir):
		count = count + 1
		print_header("***STT: " + str(count))
		full_dir_path = os.path.join(_full_parent_dir, folder_name)
		print(full_dir_path)
		if os.path.isdir(full_dir_path) == True:
			[idx, new_ftdi] = get_full_ftdi_from_string(folder_name)
			if idx!=-1:
				dev_serial = folder_name[0:idx].replace("_","")
				dev_serial = dev_serial.replace(" ","")
				new_user_msg = folder_name[idx+c_ftdi_length:]
				# find "FTDI + n" file and calculate md5
				full_nuc_table_1_file = os.path.join(full_dir_path, new_ftdi+ "1.bin")
				new_FTDI1_md5 = ""
				if os.path.isfile(full_nuc_table_1_file):
					#calculate md5
					new_FTDI1_md5 = calculate_md5_hash(full_nuc_table_1_file)
				if dev_serial.isnumeric():
					add_new_dict_flag = 0 
					dev_serial = dev_serial.zfill(4) # padding zeros
					# Search index match by dev_serial in list
					# If index = -1 (None) -> Add new
					match_index, match_dict = read_and_get_match_dict_by_devserial_in_list(extracted_ftdi_dev_list, dev_serial)
					if match_index == -1:
						add_new_dict_flag = 1
					# If exists same dev_serial in the list: we have to find index match by both 'dev_serial' and 'FTDI_MD5' and check if user updates 'msg'
					# If none match by both (dev_serial and FTDI_MD5) is found: 
					# case 1: The FTDI_MD5 == "": folder doesn't contain this file, if we find the identical (dev_serial, msg, FTDI) then pass, if different -> add new dict to list
					# case 2: FTDI_MD5 != "" -> means that new MD5 file (kind of new different folder) with the same dev_serial -> so we add new dict to list
					else:
						match_dev_md5_index = None
						if new_FTDI1_md5 != "":
							match_dev_md5_index = next((i for i, item in enumerate(extracted_ftdi_dev_list) if item["dev_serial"] == dev_serial and item["FTDI1_md5"] == new_FTDI1_md5), None)
							print("Found dict by dev serial and md5: " + str(dev_serial) + " at index: " + str(match_index))
							print("match both index: " + str(match_dev_md5_index))
							if match_dev_md5_index != None:
								print_debug("Match FTDI1_md5 file")
								if match_dict["msg"] == new_user_msg:
									print_debug("Match user msg, skip update msg")
								else:
									print_debug("Different user msg, updating:...")	
									if match_dev_md5_index>=0:
										extracted_ftdi_dev_list[match_dev_md5_index]["msg"] = new_user_msg
							else:
								add_new_dict_flag = 1
						else:
							#if new_FTDI1_md5 == "":
							ma_index = next((i for i, item in enumerate(extracted_ftdi_dev_list) if item["dev_serial"] == dev_serial and item["FTDI1_md5"] == "" and item['msg'] == new_user_msg), None)
							if ma_index == None:
								add_new_dict_flag = 1

					if add_new_dict_flag == 1:
						json_info_dict = {}
						json_info_dict['dev_serial'] = dev_serial
						json_info_dict['FTDI'] = new_ftdi
						json_info_dict['msg'] = new_user_msg
						json_info_dict['FTDI1_md5'] = new_FTDI1_md5
						print_debug("Extracted dict from folder: " + folder_name)
						print(json_info_dict)
						extracted_ftdi_dev_list.append(json_info_dict)
		else:
			print("Not a folder, skip...")
	# sort the list ascending by 'dev_serial'
	extracted_ftdi_dev_list = sorted(extracted_ftdi_dev_list, key=lambda k: k['dev_serial']) 
	jsonFile = open(_json_file_name, "w")
	jsonString = json.dumps(extracted_ftdi_dev_list, indent=2, separators=(',', ': '))
	jsonFile.write(jsonString)
	jsonFile.close()

hash_file = "D:/Dulieu_NUC_KNAN/fromOneDrive_PC_HDD/024_p150j_ok/" + "FT5P105J_110521_0.bin"

def main():
	print("nuc_production")
	calculate_md5_hash(hash_file)

if __name__ == "__main__":
    main()