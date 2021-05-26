import socket
from datetime import datetime
import sym_wrapper as sw
import json


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
        try_connect = True
        while try_connect:
            print("Waiting for connection")
            client, address = self.server.accept()
            print(f"Successful connection from {address[0]}")
            try:
                while True:
                    data = client.recv(1024).decode('ascii')
                    if not data:
                        break
                    print(f"Message received: {data}")
                    data = json.loads(data)
                    res = sw.parse_request(data)
                    client.sendall(json.dumps(res).encode('ascii'))
                    print(f"Response sent: " +
                          f"{len(json.dumps(res).encode('ascii'))} bytes")
            except KeyboardInterrupt:
                print("\nServer stopped")
                break
            print("Do you want to wait for another connection? (y/n):",
                  end=' ')
            qans = str(input()).lower()
            if qans == 'y':
                try_connect = True
            elif qans == 'n':
                try_connect = False
        client.close()


if __name__ == '__main__':
    # if os.getenv('HNAME'):
    #     sv = SymServer(os.getenv('HNAME'), 42)
    # else:
    #     sv = SymServer(socket.gethostname(), 42)
    sv = SymServer('localhost', 50)
    sv.start()
