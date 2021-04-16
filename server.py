import socket
from datetime import datetime
# from sympy import symbols, diff, integrate
import sym_wrapper as sw
import json


class SymServer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(2)  # only 5 possible connection requests
        print(f"SymServer started at {self.ip}:" +
              f"{self.port} on {datetime.now()}")
        client, address = server.accept()
        print(f"Sucessfull connection from {address}")
        try:
            while True:
                data = client.recv(1024).decode('ascii')
                if data:
                    print(f"Message recieved: {data}")
                    data = json.loads(data)
                    res = sw.parse_req(data)
                    client.send(res.encode('ascii'))
                    print("Response sent")
        except KeyboardInterrupt:
            pass
        client.close()


if __name__ == '__main__':
    server = SymServer("localhost", 55)
    server.start()
