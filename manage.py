import socket
from datetime import datetime
import sym_wrapper as sw
import json
import os


class SymServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.ip, self.port))
        self.server.listen(1)  # only 2 possible connection requests
        print(f"SymServer started at {self.ip}:" +
              f"{self.port} on {datetime.now()}")
        client, address = self.server.accept()
        print(f"Successful connection from {address}")
        try:
            while True:
                data = client.recv(1024).decode('ascii')
                if data:
                    print(f"Message received: {data}")
                    data = json.loads(data)
                    res = sw.parse_request(data)
                    client.send(json.dumps(res).encode('ascii'))
                    print("Response sent")
        except KeyboardInterrupt:
            pass
        client.close()


if __name__ == '__main__':
    # if os.getenv('HNAME'):
    #     sv = SymServer(os.getenv('HNAME'), 42)
    # else:
    #     sv = SymServer(socket.gethostname(), 42)
    sv = SymServer('localhost', 42)
    sv.start()
