# Intro
+ Save user operations, and error prone.
# Todos
- Improve performance of the code (avoid too much unncessary resources used for iteration...) -> LATER :D
- Merge/handle duplicate folders, remove duplicate files (by checking MD5...)
- Display working file, return status after clicking the button. And the folder status
- Display working messages (fail/ok) to GUI
- Write user working logs (new session, button click...) and save to text file
- JSON file -> more info: check info of each file, display file name and file size... MD5, and the folder it's working. maybe also the commands?
- More strict file type checking function (and more option for easy program change)
# Features
- User can point to 'Phan mem lay mau du lieu', the software then navigates to Data folder, NUC_Table, Log... (or by user selection dir paths) -> check the files:
+ Copy finished FTDI to one folder automatically -> Ready to be copied to store disk.
+ The user can select parent nuc folder. -> and select temperature folder -> Add feature: export valid temperature data files (by checking name and size in subfolders...) to temperature folder (to be generated NUC in software again)
- Export to current folder: json file contains FAIL/OK folders only -> Done for 2 functions
- Better GUI design.
- Display usage text when user hovers to button (manual)
- Add scroll text box to display print message...
# Vietnamese
- Thêm hiển thị thông tin của working directory: có bao nhiêu files, bao nhiêu files đã hoàn thiện, sẵn sàng để copy qua thư mục đích (sử dụng trên máy lấy NUC)… 
- Phần mềm sẽ thường được sử dụng trên 2 máy: máy lấy NUC, máy gen NUC.
- Trên máy lấy NUC: Thêm chức năng gom files vào folder tương ứng nếu đủ các files (9 files nhiệt độ) và dung lượng -> click là có thể copy sang máy khác để gen nuc. Đồng thời hiển thị thông tin của folder KNAN_software đấy (bằng cách click vào). 
- Trên máy gen NUC: Gom files vào folder đối với các thiết bị đã gen xong, đủ files, và Log message đạt yêu cầu (15 files). Click xong là có thể copy sang ổ đĩa HDD để lưu trữ.
- Chưa xét trường hợp: trùng device serial và FTDI nhưng khác tên folder ^^ (kiểu bị trùng dữ liệu). Cái này người dùng tự xử lý cho nó chuẩn đê
# Practices
- Clean code
# References
https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
https://stackoverflow.com/questions/21058935/python-json-loads-shows-valueerror-extra-data
https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary

## JSON
https://stackoverflow.com/questions/53110610/json-dump-in-python-writing-newline-character-and-carriage-returns-in-file/57021651

# Hướng dẫn sử dụng:
Ví dụ:
ORG_DIR = nuc_test
## Nút 1:
- Đi vào từng thư mục có trong ORG_DIR, sau đó đọc FTDI string có trong file, rồi đổi tên của folder full thành tên FTDI. Chú ý trước khi sử dụng nút này thì các ký hiệu khác ngăn cách với FTDI bằng dấu gạch dưới
## Nút 2
- Đi vào từng thư mục có trong ORG_DIR, sau đó kiểm tra các file ở trong thư mục, xem đủ 9 file nhiệt độ, 5 file NUC table, và 1 file Log chưa, và đổi tên thư mục ban đầu + dấu # + kết quả kiểm tra. Đồng thời ghi log ra file .JSON
## Nút 3: 
- Đối với từng thư mục có trong ORG_DIR, Xóa các ký tự sau dấu #
## Nút 4
- Trong thư mục SOFT_DIR: tìm các các file có chứa FTDI của đến thiết bị, nó sẽ tự gom lại và tạo folder đặt tên tương ứng.
- Chú ý đối với Nút 4 và nút 5: Chỉ nên sử dụng khi gom các file để chuẩn bị cho việc gen NUC, nó gom lại không hề biết được ban đầu lấy ra từ folder nào.
## Nút 5
- Tương tự như nút 4, nhưng nó chỉ làm ở files có trong thư mục con (chỉ vào thêm 1 level)
## Nút 6:
- Trong thư mục SOFT_DIR, nó sẽ lấy tất cả các file trong thư mục con ra SOFT_DIR
