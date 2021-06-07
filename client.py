import socket
import catp as cp


class SymClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server.connect((self.ip, self.port))

    def request_answer(self, data):
        ec = cp.CATP()
        self.server.sendall(ec.encode(data))
        result = ec.decode(self.server.recv(260))
        return result


if __name__ == '__main__':
    cl = SymClient("localhost", 8888)
    cl.start()
    ec = cp.CATP()
    try:
        while True:
            print("Enter type of command: ", end="")
            command_type = str(input())
            if command_type == "derivative":
                print("Enter function: ", end="")
                func = str(input())
                print("Enter derivative order (variable names parted with space): ", end="")
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
            cl.server.sendall(ec.encode(req_data))
            wait_for_result = True
            while wait_for_result:
                result = ec.decode(cl.server.recv(260))
                if not result:
                    break
                elif result['type'] == 'success' or result['type'] == 'error':
                    wait_for_result = False
                print(result['result'])
    except KeyboardInterrupt:
        print("\nClient stopped")