import socket
import struct

CONTROLLER_IP = "192.168.2.45"  #ESP32 IP
GAME_IP = "192.168.0.0"
BACKEND_CONTROLLER_PORT = 8888 
BACKEND_GAME_PORT = 8887 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #used to send data
sock_receive_controller = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive_controller.bind(("0.0.0.0", BACKEND_CONTROLLER_PORT))
sock_receive_game = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive_game.bind(("0.0.0.0", BACKEND_GAME_PORT))

def receive_from_controller():
    data, addr = sock_receive_controller.recvfrom(17)  # Buffer size is 1024 bytes
    if len(data) == 2 * 4 + 3:  # Assuming 2 floats (4 bytes each) and 3 booleans (1 byte each)
        gyroX, gyroZ, trigger, ability, calibration = struct.unpack('ff???', data)
        print("==========Received data==========")
        print(f"gyroX: {gyroX}")
        print(f"gyroZ: {gyroZ}")
        print(f"Trigger: {trigger}")
        print(f"Ability {ability}")
        print(f"Calibration Mode: {calibration}")
        send_to_game(gyroX, gyroZ, trigger, ability, calibration)
    else:
        print("Invalid data received")

def send_to_controller(laser = False, rumble = False, sound_number = 3):

    data = struct.pack('<??i', laser, rumble, sound_number)

    sock.sendto(data, (CONTROLLER_IP, BACKEND_CONTROLLER_PORT))

def send_to_game(gyroX, gyroZ, trigger, ability, calibration):
    input_data = struct.pack('<ff???')
    sock.sendto(input_data, (GAME_IP, BACKEND_GAME_PORT))

def receive_from_game():
    data, addr = sock_receive_game.recvfrom(18)
    if len(data) == 18:  # 18 Booleans
        laser, rumble, sound, leds = struct.unpack('???15?', data)
        send_to_controller(laser, rumble, sound, leds)
    else:
        print("Invalid data received")

while True:
    receive_from_game()
    receive_from_controller()
