# Ymodem Binary Files Send GUI

A Python-based graphical application for sending binary files over serial connections using the YMODEM protocol. This tool provides a user-friendly interface for firmware updates and file transfers to embedded systems, particularly designed for use with STM32 microcontrollers.

## Features

- **Intuitive GUI Interface**: Built with Tkinter for easy file selection and transfer monitoring
- **YMODEM Protocol Support**: Reliable file transfer with error checking and recovery
- **Serial Communication**: Configurable serial port settings
- **Progress Tracking**: Real-time transfer progress monitoring
- **Error Handling**: Robust error detection and reporting

## Requirements

- Python 3.x
- pyserial
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Ymodemsend.git
cd Ymodemsend
```

2. Install required dependencies:
```bash
pip install pyserial
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Using the GUI:
   - Click "Choose File" to select the binary file to send
   - Select the appropriate COM port from the dropdown menu
   - Configure serial settings if needed (default: 115200 baud)
   - Click "Send" to initiate the file transfer

## YMODEM Protocol Implementation

The application implements the YMODEM protocol with the following features:

### Packet Structure

1. **Initial Packet (Filename Information)**
```
SOH 00 FF "filename" "size" NUL[118] CRC CRC
```

2. **Data Packets**
```
STX NN FF data[1024] CRC CRC
```

3. **End of Transfer**
```
EOT
```

### Transfer Process

1. **Initialization**
   - Waits for receiver's 'C' character
   - Sends filename packet
   - Waits for acknowledgment

2. **Data Transfer**
   - Sends 1024-byte blocks
   - Verifies acknowledgment for each block
   - Handles retransmission if needed

3. **Completion**
   - Sends EOT
   - Confirms final acknowledgment

## Error Handling

- CRC verification for data integrity
- Timeout management
- Automatic retransmission
- User-friendly error messages
