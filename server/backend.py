import socket

UDP_IP = "0.0.0.0"  # Listen to all available interfaces
UDP_PORT = 8888  # Use the same port as defined in the ESP32 code

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    print("Received message:", data.decode())
    # Process 'data' as needed within your Python script
