import os

def extract_file_info(file_path):
    # Get the file name
    file_name = os.path.basename(file_path)
    
    # Get the file size
    file_size = os.path.getsize(file_path)
    
    # Print the file name and size
    print(f"File name: {file_name}")
    print(f"File size: {file_size} bytes")
    
    return file_name, file_size

def read_file_in_chunks(file_path):
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read()
                if not chunk:
                    break
                yield chunk  # Yield 1KB chunks
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return chunk     

def file_in_hex(file_path, chunk_size=1024):
    hex_data=""
    try:
        with open(file_path, 'rb') as file:
            chunk_number = 1
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                
                # Convert bytes to hexadecimal
                hex_data += chunk.hex()

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return hex_data