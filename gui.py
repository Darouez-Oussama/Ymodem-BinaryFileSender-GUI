import serial
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from file_utils import extract_info
from packet_utils import build_data_packet, build_start_packet, build_end_of_transmission_packet 
from hex_utils import extract_file_info , file_in_hex 

# Initialize serial port
target_device = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

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

def start_transmission(file_path, progress_var):
    try:
        # Extract file information
        file_name, file_size = extract_file_info(file_path)
        hex_content = file_in_hex(file_path)
        packet_number=file_size//1024
        if file_size % 1024 != 0 :
            packet_number+=1

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
                        data_packet = build_data_packet(packet_number, i + 1, hex_content[i * 2048:(i + 1) * 2048])
                        response = send_packet(data_packet)
                        print("Data ", i, "response:", response)
                        if response != b'\x06':  # Check if ACK is received
                            print(f"Data packet {i + 1} not acknowledged. Stopping transmission.")
                            break
                        else:
                            print(f"Data packet {i + 1} acknowledged.")
                            progress_var.set((i + 1) / packet_number * 100)
                            root.update_idletasks()

                    print("Transmission completed.")
                    messagebox.showinfo("Transmission", "Transmission completed successfully!")
                else:
                    print("Failed to receive 'C' after start packet.")
                    messagebox.showerror("Transmission Error", "Failed to receive 'C' after start packet.")
            else:
                print("Start packet not acknowledged.")
                messagebox.showerror("Transmission Error", "Start packet not acknowledged.")
        else:
            print("Did not receive 'C' to start transmission.")
            messagebox.showerror("Transmission Error", "Did not receive 'C' to start transmission.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        messagebox.showerror("Serial Error", f"Serial error: {e}")
    finally:
        target_device.close()

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        progress_var.set(0)
        start_transmission(file_path, progress_var)

# Set up the GUI
root = tk.Tk()
root.title("YModem File Sender")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

btn_select_file = tk.Button(frame, text="Select File", command=select_file)
btn_select_file.pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = Progressbar(frame, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=10, pady=10)

root.mainloop()
