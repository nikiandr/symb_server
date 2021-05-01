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
    cl = SymClient("172.17.0.2", 42)
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
            elif command_type == 'indef_integral':
                print("Enter function: ", end="")
                func = str(input())
                print("Enter integrating variable: ", end="")
                integral_var = str(input())
                req_data = {'mode': 'indef_integral',
                            'variables': [integral_var],
                            'function': func}
            elif command_type == 'def_integral':
                print("Enter function: ", end="")
                func = str(input())
                print("Enter integrating variable: ", end="")
                integral_var = str(input())
                print("Enter integrating interval: ", end="")
                integral_interval = str(input()).split(sep=" ")
                req_data = {'mode': 'def_integral',
                            'variables': [integral_var],
                            'function': func,
                            'interval': integral_interval}
            elif command_type == 'simplify':
                print("Enter expression: ", end="")
                func = str(input())
                req_data = {'mode': 'simplify',
                            'expression': func}
            else:
                print("Mode doesn't exist")
                continue
            res = cl.send_request(req_data)['result']
            print(res)
    except KeyboardInterrupt:
        print("Client stopped")
