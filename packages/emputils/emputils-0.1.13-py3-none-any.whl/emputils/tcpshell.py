import socket
from subprocess import Popen, PIPE, STDOUT


class Server():
    BUFFER_SIZE: int = 1024

    def __init__(self) -> None:
        self.socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def configure(self, port: int, ip: str = "") -> None:
        self.socket.bind((ip, port))

    def listen(self, commands: int = -1) -> None:
        self.socket.listen()
        command_index: int = commands
        while command_index != 0:
            conn, addr = self.socket.accept()
            print('Connection address:', addr)
            while 1:
                data: bytes = conn.recv(self.BUFFER_SIZE)
                if not data:
                    break
                p: Popen = Popen(data, shell=True, stdin=PIPE,
                                 stdout=PIPE, stderr=STDOUT, close_fds=True)
                output: str = p.stdout.read().decode('utf-8').strip()
                print("Received data:", data)
                conn.send(output.encode())
            conn.close()

            command_index -= 1

    def close(self) -> None:
        self.socket.close()


class Client():
    BUFFER_SIZE: int = 1024

    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def configure(self, port: str, ip: int) -> None:
        self.socket.connect((ip, port))

    def send(self, message: str) -> str:
        self.socket.send(message.encode())
        data: bytes = self.socket.recv(self.BUFFER_SIZE)
        return data.decode()

    def close(self) -> None:
        self.socket.close()
