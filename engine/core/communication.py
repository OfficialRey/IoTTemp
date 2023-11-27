import json
from socket import socket as Socket
from socket import AF_INET, SOCK_DGRAM

from protocol.game_package import GamePackage


class Communication:

    def __init__(self, target_ip: str, target_port: str, receiver_port: str, receive_buffer: int):
        self.sender = Socket(AF_INET, SOCK_DGRAM)
        self.sender.bind((target_ip, target_port))

        self.receiver = Socket(AF_INET, SOCK_DGRAM)
        self.receiver.bind((target_ip, receiver_port))

        self.buffer = receive_buffer

    def run(self, ServerPackage):
        # Send server package
        pass
        # Receive weapon package
        pass

    def send_package(self, package: GamePackage):
        self.sender.send(str(package.construct()))

    def receive_package(self):
        data, addr = self.receiver.recvfrom(self.buffer)
        print(data)
