import socket
import catp as cp
import bcrypt

SALT: bytes = b'$2b$12$e9dmCi7tr6kLItHx7HPCte'


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
    isanon = str()
    try:
        while True:
            print("Do you want to use SymbServer anonymously? [Y/n]: ", end='')
            isanon = str(input()).lower()
            if isanon in ('y', 'n'):
                break
            else:
                print("Wrong symbol. Try again.")
                continue
        if isanon == 'n':
            while True:
                print("Do you already have an account? [Y/n]: ", end='')
                isaccount = str(input()).lower()
                if isaccount in ('y', 'n'):
                    break
                else:
                    print("Wrong symbol. Try again.")
                    continue
            if isaccount == 'n':
                print("Let's start with registering in SymbServer system.")
                while True:
                    print("Please enter your nickname: ", end='')
                    nickname = str(input()).strip()
                    print("Now enter your wanted password: ", end='')
                    password = str(input()).strip()
                    cl.server.sendall(ec.encode(
                        {
                            'type': 'registration',
                            'nickname': nickname,
                            'password': bcrypt.hashpw(password.encode('ascii'), SALT)
                        }
                    ))
                    result = ec.decode(cp.catp_mess_get(cl.server))
                    if result['type'] == 'registration_success':
                        break
                    elif result['type'] == 'registration_error':
                        print("There was some kind of error with your request. "
                              + result['result']+ " Let's try again.")
                        continue
            elif isaccount == 'y':
                print("Let's start with logging in SymbServer system.")
                while True:
                    print("Please enter your nickname: ", end='')
                    nickname = str(input()).strip()
                    print("Now enter your wanted password: ", end='')
                    password = str(input()).strip()
                    cl.server.sendall(ec.encode(
                        {
                            'type': 'login',
                            'nickname': nickname,
                            'password': bcrypt.hashpw(password.encode('ascii'), SALT)
                        }
                    ))
                    result = ec.decode(cp.catp_mess_get(cl.server))
                    if result['type'] == 'login_success':
                        break
                    elif result['type'] == 'login_error':
                        print("There was some kind of error with your request. "
                              + result['result']+ " Let's try again.")
                        continue
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
                result = ec.decode(cp.catp_mess_get(cl.server))
                if not result:
                    break
                elif result['type'] == 'success' or result['type'] == 'error':
                    wait_for_result = False
                print(result['result'])
    except KeyboardInterrupt:
        try:
            print("\nClient is about to stop.")
            if isanon == 'n':
                while True:
                    print("Do you want to get your all-time usage history? [Y/n]: ", end='')
                    ishistory = str(input()).lower().strip()
                    if ishistory in ('y', 'n'):
                        break
                    else:
                        print("Wrong symbol. Try again.")
                        continue
                if ishistory == 'y':
                    cl.server.sendall(ec.encode(
                        {
                            'type': 'history_request'
                        }
                    ))
                    history = ec.decode(cp.catp_mess_get(cl.server))
                    if history['type'] == 'history_error':
                        print("There was an error in getting your history. " + history['history'])
                    else:
                        for row in history['history']:
                            print(row, end='\n\n')
                else:
                    print("Bye-bye. Have a nice day.")
        except KeyboardInterrupt:
            print("\nAll right, then. Keep your secrets.")
