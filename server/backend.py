import socket
import struct

UDP_IP = "192.168.2.45"  #ESP32 IP
UDP_PORT = 8888  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.settimeout(1.0)
sock2.bind(("0.0.0.0", UDP_PORT))

def receive_data():
    data, addr = sock2.recvfrom(17)  # Buffer size is 1024 bytes
    if len(data) == 2 * 4 + 3:  # Assuming 2 floats (4 bytes each) and 3 booleans (1 byte each)
        gyroX, gyroZ, trigger, ability, calibration = struct.unpack('ff???', data)
        print("==========Received data==========")
        print(f"gyroX: {gyroX}")
        print(f"gyroZ: {gyroZ}")
        print(f"Trigger: {trigger}")
        print(f"Ability {ability}")
        print(f"Calibration Mode: {calibration}")
    else:
        print("Invalid data received")

def send_data(laser = False, rumble = False):
    sound_number = 3

    data = struct.pack('<??i', laser, rumble, sound_number)

    # Send data to the ESP32
    sock.sendto(data, (UDP_IP, UDP_PORT))

while True:
    receive_data()
    send_data()
