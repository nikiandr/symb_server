import socket
import json


class SymClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((self.ip, self.port))

    def send_request(self, data):
        server.send(json.dumps(data).encode('ascii'))
        result = server.recv(1024).decode('ascii')
        return result


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 6666))
try:
    while True:
        print("Enter command: ")
        server.send(input().encode('ascii'))
        result = server.recv(1024).decode('ascii')
        print(result)
except KeyboardInterrupt:
    pass
