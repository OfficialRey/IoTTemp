from socket import socket
from socket import AF_INET, SOCK_DGRAM

import pygame.event

from protocol.game_package import GamePackage
from protocol.server_package import ServerPackage
from protocol.weapon_package import WeaponPackage


def synthesize_package() -> WeaponPackage:
    return WeaponPackage(*pygame.mouse.get_pos(), *pygame.mouse.get_pressed())


class Communication:

    def __init__(self, udp_ip: str, udp_port: int, receiver_ip: str, receiver_port: int, receive_buffer: int, engine,
                 synthesize_connection: bool = False):
        self.sender = socket(AF_INET, SOCK_DGRAM)
        self.sender.bind((receiver_ip, udp_port))

        self.receiver = socket(AF_INET, SOCK_DGRAM)

        self.buffer = receive_buffer

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.synthesize_connection = synthesize_connection
        self.connected = self.synthesize_connection

        self.engine = engine
        self.weapon_package = WeaponPackage()

    def run(self, server_package: ServerPackage) -> WeaponPackage:
        if self.synthesize_connection:
            return synthesize_package()
        if self.connected:
            self.send_package(server_package)
            # Receive weapon package
            # self.receive_package()

    # PC Mode

    def send_package(self, package: GamePackage):
        self.sender.sendto(package.construct(), (self.udp_ip, self.udp_port))

    def receive_package(self):
        data, addr = self.receiver.recvfrom(self.buffer)
        print(data)

    def establish_connection(self):
        while not self.connected or self.synthesize_connection:
            self.connected = True
