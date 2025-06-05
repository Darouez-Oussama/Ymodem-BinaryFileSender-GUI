from hex_utils import extract_file_info ,file_in_hex,read_file_in_chunks

def extract_info():
    file_path = input("Enter file path :")
    file_name, file_size = extract_file_info(file_path)
    hex_content = file_in_hex(file_path)
    packet_number=file_size//1024
    if file_size % 1024 != 0 :
        packet_number+=1
    return file_name , file_size , packet_number , hex_content  