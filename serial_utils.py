import serial
import time
from file_utils import extract_info
from packet_utils import build_data_packet, build_start_packet, build_end_of_transmission_packet
from print_utils import print_binary_content, print_file_size

# Initialize serial port
target_device = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

def wait_for_byte(expected_byte, timeout_duration=300):
    start_time = time.time()
    while True:
        if target_device.in_waiting > 0:
            byte = target_device.read(1)
            if byte == expected_byte:
                return True
        if time.time() - start_time > timeout_duration:
            print("Timeout waiting for the expected byte.")
            return False
        time.sleep(0.1)  # Small delay to avoid busy-waiting

def send_packet(packet):
    target_device.write(packet)
    # Wait for a response byte
    if wait_for_byte(b'\x06'):  # Wait for ACK (0x06)
        return b'\x06'
    return None

try:
    file_name, file_size, packet_number, hex_content = extract_info()
    # print_binary_content(hex_content)
    # print(f'File Size: {file_size} bytes')

    # Wait for 'C' from the receiver to start transmission
    print("Waiting for 'C' to send the start packet...")
    if wait_for_byte(b'C'):
        target_device.reset_input_buffer()
        print("Received 'C'")

        # Send start packet
        start_packet = build_start_packet(file_name, file_size)
        response = send_packet(start_packet)
        print(f"Response: {response}")

        # Check if response is ACK (0x06)
        if response == b'\x06':
            print("Start packet acknowledged, waiting for next 'C'...")
            if wait_for_byte(b'C'):
                print("Received 'C', sending data packets")

                # Send data packets
                for i in range(packet_number):
                    data_packet = build_data_packet(packet_number,i + 1, hex_content[i*2048:(i+1)*2048])
                    response = send_packet(data_packet)
                    print("data ",i,"response:",response)
                    if response != b'\x06':  # Check if ACK is received
                        print(f"Data packet {i+1} not acknowledged. Stopping transmission.")
                        break
                    else:
                        print(f"Data packet {i+1} acknowledged.")

                print("Transmission completed.")
            else:
                print("Failed to receive 'C' after start packet.")
        else:
            print("Start packet not acknowledged.")
    else:
        print("Did not receive 'C' to start transmission.")

except serial.SerialException as e:
    print(f"Serial error: {e}")
finally:
    target_device.close()
