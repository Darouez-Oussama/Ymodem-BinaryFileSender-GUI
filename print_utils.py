from packet_utils import build_data_packet , build_start_packet , build_end_of_transmission_packet

def print_file_size(file_name,file_size) : 
    print(file_name , " size : " , file_size)

def print_binary_content (hex_content) :
    hex_offset = 0
    for i in range(0, len(hex_content), 32):  
        print(hex(hex_offset),"|",hex_content[i:i+32])
        hex_offset+=16

def print_all_data_packets(packet_number , file_size ,hex_content) :
    packet_index = 1 
    for j in range(0,file_size*2,2048): 
        print("packet [",packet_index,"] :",build_data_packet(packet_number,packet_index,hex_content[j:j+2048]).hex()) 
        packet_index+=1
        