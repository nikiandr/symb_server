import socket
import json


class SymClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.connect((self.ip, self.port))

    def send_request(self, data):
        self.server.send(json.dumps(data).encode('ascii'))
        result = json.loads(self.server.recv(1024).decode('ascii'))
        return result


if __name__ == '__main__':
    cl = SymClient("localhost", 56)
    cl.start()
    try:
        while True:
            print("Enter type of command: ", end="")
            command_type = str(input())
            if command_type == "derivative":
                print("Enter function: ", end="")
                func = str(input())
                print("Enter derivative order: ", end="")
                derivative_order = str(input()).split(sep=" ")
                req_data = {'mode': 'derivative',
                            'function': func,
                            'order': derivative_order}
            res = cl.send_request(req_data)['result']
            print(res)
    except KeyboardInterrupt:
        pass
