import socket
from datetime import datetime
import sym_wrapper as sw
import catp as cp
import threading as td


def process_messages(client):
    while True:
        data = client.recv(260)
        if not data:
            break
        print(f"Message received: {data}")
        ec = cp.CATP()
        res = sw.parse_request(ec.decode(data))
        response = ec.encode(res)
        client.sendall(response)
        print(f"Response sent: " +
              f"{len(response)} bytes")


class SymServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.bind((self.ip, self.port))
        self.server.listen(5)  # only 5 possible connection requests
        print(f"SymServer started at {self.ip}:" +
              f"{self.port} on {datetime.now()}")
        connection_number = 0
        try:
            while True:
                print("Waiting for another connection")
                client, address = self.server.accept()
                print(f"Successful connection from {address[0]}")
                process_thread = td.Thread(target=process_messages, args=(client, ))
                process_thread.start()
                connection_number += 1
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == '__main__':
    # if os.getenv('HNAME'):
    #     sv = SymServer(os.getenv('HNAME'), 42)
    # else:
    #     sv = SymServer(socket.gethostname(), 42)
    sv = SymServer('localhost', 50)
    sv.start()
