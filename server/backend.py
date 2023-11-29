import socket
import struct

UDP_IP = "0.0.0.0"  # Listen on all available interfaces
UDP_PORT = 8888  # Choose the same port as in the ESP32 code

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(17)  # Buffer size is 1024 bytes
    if len(data) == 2 * 4 + 3:  # Assuming 2 floats (4 bytes each) and 3 booleans (1 byte each)
        gyroX, gyroZ, trigger, ability, calibration = struct.unpack('ff???', data)
        print("Received data:")
        print(f"gyroX: {gyroX}")
        print(f"gyroZ: {gyroZ}")
        print(f"Trigger: {trigger}")
        print(f"Ability {ability}")
        print(f"Calibration Mode: {calibration}")
    else:
        print("Invalid data received")
