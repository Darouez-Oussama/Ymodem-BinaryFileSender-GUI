from hex_utils import extract_file_info , file_in_hex , read_file_in_chunks
from packet_utils import build_start_packet , build_data_packet , build_end_of_transmission_packet
from print_utils import print_binary_content , print_file_size , print_all_data_packets

 # /home/oussama/Documents/Seabot_bootloader_cubeide/Application/Debug/Application.bin
 # /home/oussama/Documents/Seabot_bootloader_cubeide/app1/Debug/app1.bin
  # /home/oussama/Documents/Seabot_bootloader_cubeide/app/Debug/app.bin

file_path = input("Enter file path :")
file_name, file_size = extract_file_info(file_path)
hex_content = file_in_hex(file_path)
packet_number=file_size//1024
if file_size % 1024 != 0 :
    packet_number+=1

if hex_content is not None:
    print_file_size(file_name , file_size)
    print_binary_content(hex_content)
    print("start packet :")  
    print(build_start_packet(file_name,file_size))
    print("first data packet :")
    print_all_data_packets(packet_number,file_size,hex_content)
    
 
