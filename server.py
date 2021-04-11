import socket
from datetime import datetime
from sympy import symbols, diff, integrate


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
                    x = symbols('x')
                    req = data.split(" ", 1)
                    if len(req) == 1:
                        res = "Unappropriate request"
                    elif req[0] == 'differentiate':
                        res = str(diff(req[1], x).doit())
                    elif req[0] == 'integrate':
                        res = str(integrate(req[1], x).doit())
                    else:
                        res = "Unappropriate request"
                    client.send(res.encode('ascii'))
                    print("Response sent")
        except KeyboardInterrupt:
            pass
        client.close()


if __name__ == '__main__':
    server = SymServer("localhost", 6666)
    server.start()
