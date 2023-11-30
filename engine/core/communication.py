from socket import socket as Socket
from socket import AF_INET, SOCK_DGRAM

from protocol.game_package import GamePackage
from protocol.server_package import ServerPackage


class Communication:

    def __init__(self, udp_ip: str, udp_port: int, receiver_ip: str, receiver_port: int, receive_buffer: int):
        self.sender = Socket(AF_INET, SOCK_DGRAM)
        self.sender.bind((receiver_ip, udp_port))

        self.receiver = Socket(AF_INET, SOCK_DGRAM)

        self.buffer = receive_buffer

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        # TODO: Create connection interface
        self.connected = True

    def run(self, server_package: ServerPackage):
        if self.connected:
            self.send_package(server_package)
            # Receive weapon package
            # self.receive_package()

    def send_package(self, package: GamePackage):
        self.sender.sendto(package.construct(), (self.udp_ip, self.udp_port))

    def receive_package(self):
        data, addr = self.receiver.recvfrom(self.buffer)
        print(data)

    def establish_connection(self):
        while not self.connected:
            self.connected = True
            pass
