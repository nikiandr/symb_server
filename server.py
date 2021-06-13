import socket
from datetime import datetime
import sym_wrapper as sw
import catp as cp
import threading as td
import time


def catp_mess_get(client):
    message = bytes()
    while True:
        chunk = client.recv(128)
        message += chunk
        if b'\r\n\r\n' in message:
            break
    message = message.split(b'\r\n\r\n')[0]
    return message


def process_messages(client):
    while True:
        data = client.recv(260)
        if not data:
            break
        print(f"Message received: {data}")
        ec = cp.CATP()
        res = sw.parse_request(ec.decode(data))
        time.sleep(1)
        for i in range(10, 100, 10):
            client.sendall(ec.encode({
                'type': 'progress',
                'mode': res['mode'],
                'result': f'Progress {i}/100'
            }))
            time.sleep(1)
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
                try:
                    print("Waiting for another connection")
                    client, address = self.server.accept()
                    print(f"Successful connection from {address[0]}")
                    # daemon=True so that thread is killed when program ends
                    process_thread = td.Thread(target=process_messages, args=(client, ), daemon=True)
                    process_thread.start()
                    connection_number += 1
                except ConnectionError:
                    print('Connection Error')
                    continue
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == '__main__':
    # 0.0.0.0 - basically any address
    sv = SymServer('0.0.0.0', 8888)
    sv.start()
