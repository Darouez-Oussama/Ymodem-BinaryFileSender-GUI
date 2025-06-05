import struct
from crc_utils import calculate_crc

MAX_FILENAME_LENGTH = 255
PACKET_SIZE = 1029
DATA_PACKET_SIZE = 1024
END_OF_TRANSMISSION = b'\x04'

def build_start_packet(filename, filesize):
    if len(filename) > MAX_FILENAME_LENGTH:
        raise ValueError(f"Filename exceeds maximum length of {MAX_FILENAME_LENGTH} characters.")
    
    # Start of packet (fixed 3 bytes)
    start_packet = b'\x02\x00\xFF'
    

    filename_encoded = filename.encode('ascii')
    
    # File size (4 bytes, little-endian format)
    filesize_encoded = f"{filesize}"  # Using 8 bytes for variable length
    filesize_encoded = filesize_encoded.encode('ascii')
    
    # Combine all parts before padding
    packet_without_crc = start_packet + filename_encoded + b'\x00' + filesize_encoded + b'\x20'
   

    # Add padding to reach the required size of 1027 bytes (1029 - 2 bytes for CRC)
    padding_length = PACKET_SIZE - len(packet_without_crc) - 2  # 2 bytes for CRC
    padding = b'\x00' * padding_length
    packet_data = filename_encoded + b'\x00' + filesize_encoded + b'\x20' + padding

    # Combine all parts
    packet = packet_without_crc + padding

    # Calculate CRC
    crc = calculate_crc(packet_data)
    packet += crc

    if len(packet) != PACKET_SIZE:
        raise ValueError("Packet size does not match the expected length of 1029 bytes.")

    return packet

def build_data_packet(numbers_of_packets,packet_number, data):
    # if len(data) != DATA_PACKET_SIZE:
    #     raise ValueError(f"Data must be exactly {DATA_PACKET_SIZE} bytes.")

    # Start of packet (1 byte)
    start_packet = b'\x02'
    
    # Packet number and inverse packet number
    inverse_packet_number = ~packet_number & 0xFF 
    packet_number_encoded = bytes([packet_number])  # Using 8 bytes for variable length
    inverse_packet_number_encoded = bytes([inverse_packet_number])  # Using 8 bytes for variable length
    data_encoded = bytes.fromhex(data)
    # data_encoded = data_encoded.encode('ascii')
    packet = start_packet + packet_number_encoded + inverse_packet_number_encoded + data_encoded
    packet_data = data_encoded  
    if packet_number == numbers_of_packets :
        padding_length = PACKET_SIZE - len(packet) - 2 
        if padding_length > 0 : 
            padding = b'\x1A' * padding_length 
            packet+=padding
            packet_data+=padding

    # Calculate CRC
    crc = calculate_crc(packet_data)
    packet += crc

    # if len(packet) != DATA_PACKET_SIZE + 4:
    #     raise ValueError("Data packet size does not match the expected length.")

    return packet

def build_end_of_transmission_packet():
    return END_OF_TRANSMISSION

