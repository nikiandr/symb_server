import socket


def catp_mess_get(client: socket.socket) -> bytes:
    """
    Function for CATP messages receiving by socket library using TCP
    Args:
        client: socket object of connection from where you receive packet

    Returns:
        CATP packet in form of bytes object
    """
    message = bytes()
    while True:
        chunk = client.recv(128)
        if not chunk:
            raise ConnectionError
        message += chunk
        if b'\r\n\r\n' in message:
            break
    message = message.split(b'\r\n\r\n')[0] + b'\r\n\r\n'
    return message


class CATP:
    """
    Class for encoding/decoding CATP packages.

    CATP - computer algebra transfer protocol -
    computer web protocol developed for computer
    algebra web-based distributed systems to transfer data
    efficiently.

    Attributes:
        version: version of protocol
    """
    def __init__(self, version: str = '0.0.2'):
        self.version = version

    def decode(self, packet: bytes) -> dict:
        """
        Decodes CATP packet/byte string to specially formatted dictionary
        which could then be internally used.
        :param packet: CATP packet in byte string.
        :return: specially formatted dictionary for internal usage.
        """
        if self.version == '0.0.1':
            packet_type = packet[0]
            content = packet[4:].decode('ascii')
            if packet_type == 0:
                content_list = content.split('|')
                if packet[2] == 0:
                    return {
                        'mode': 'derivative',
                        'function': content_list[0],
                        'order': content_list[1:]
                    }
                elif packet[2] == 1:
                    return {
                        'mode': 'def_integral',
                        'variables': [content_list[1]],
                        'function': content_list[0],
                        'interval': tuple(content_list[2].split(' '))
                    }
                elif packet[2] == 2:
                    return {
                        'mode': 'indef_integral',
                        'variables': [content_list[1]],
                        'function': content_list[0]
                    }
                elif packet[2] == 3:
                    return {
                        'mode': 'simplify',
                        'expression': content_list[0]
                    }
            elif packet_type == 1:
                # sor - success or error
                sor = str()
                if packet[3] == 0:
                    sor = 'success'
                elif packet[3] == 1:
                    sor = 'error'
                else:
                    raise ValueError('Unacceptable package')
                if packet[2] == 0:
                    return {
                        'type': sor,
                        'mode': 'derivative',
                        'result': content
                    }
                elif packet[2] == 1:
                    return {
                        'type': sor,
                        'mode': 'def_integral',
                        'result': content
                    }
                elif packet[2] == 2:
                    return {
                        'type': sor,
                        'mode': 'indef_integral',
                        'result': content
                    }
                elif packet[2] == 3:
                    return {
                        'type': sor,
                        'mode': 'simplify',
                        'result': content
                    }
            elif packet_type == 2:
                if packet[2] == 0:
                    return {
                        'type': 'progress',
                        'mode': 'derivative',
                        'result': content
                    }
                elif packet[2] == 1:
                    return {
                        'type': 'progress',
                        'mode': 'def_integral',
                        'result': content
                    }
                elif packet[2] == 2:
                    return {
                        'type': 'progress',
                        'mode': 'indef_integral',
                        'result': content
                    }
                elif packet[2] == 3:
                    return {
                        'type': 'progress',
                        'mode': 'simplify',
                        'result': content
                    }
            else:
                raise ValueError("Unacceptable package")
        elif self.version == '0.0.2':
            packet_type = packet[0]
            packet_mode = packet[1]
            packet_success = packet[2]
            # split - to get rid of end delimiter and everything after it
            content = packet[3:].split(b'\r\n\r\n')[0].decode('ascii')
            content_list = content.split('|')
            if packet_type == 0:
                if packet_mode == 0:
                    return {
                        'mode': 'derivative',
                        'function': content_list[0],
                        'order': content_list[1:]
                    }
                elif packet_mode == 1:
                    return {
                        'mode': 'def_integral',
                        'variables': [content_list[1]],
                        'function': content_list[0],
                        'interval': tuple(content_list[2].split(' '))
                    }
                elif packet_mode == 2:
                    return {
                        'mode': 'indef_integral',
                        'variables': [content_list[1]],
                        'function': content_list[0]
                    }
                elif packet_mode == 3:
                    return {
                        'mode': 'simplify',
                        'expression': content_list[0]
                    }
            elif packet_type == 1:
                # sor - success or error
                sor = str()
                if packet_success == 0:
                    sor = 'success'
                elif packet_success == 1:
                    sor = 'error'
                else:
                    raise ValueError('Unacceptable package')
                if packet_mode == 0:
                    return {
                        'type': sor,
                        'mode': 'derivative',
                        'result': content
                    }
                elif packet_mode == 1:
                    return {
                        'type': sor,
                        'mode': 'def_integral',
                        'result': content
                    }
                elif packet_mode == 2:
                    return {
                        'type': sor,
                        'mode': 'indef_integral',
                        'result': content
                    }
                elif packet_mode == 3:
                    return {
                        'type': sor,
                        'mode': 'simplify',
                        'result': content
                    }
            elif packet_type == 2:
                if packet_mode == 0:
                    return {
                        'type': 'progress',
                        'mode': 'derivative',
                        'result': content
                    }
                elif packet_mode == 1:
                    return {
                        'type': 'progress',
                        'mode': 'def_integral',
                        'result': content
                    }
                elif packet_mode == 2:
                    return {
                        'type': 'progress',
                        'mode': 'indef_integral',
                        'result': content
                    }
                elif packet_mode == 3:
                    return {
                        'type': 'progress',
                        'mode': 'simplify',
                        'result': content
                    }
            elif packet_type == 3:
                if packet_mode != 4:
                    raise ValueError('Unacceptable package')
                return {
                    'type': 'login',
                    'nickname': packet[3:].split(b'\r\n\r\n')[0].split(b'\r\n')[0].decode("ascii"),
                    'password': packet[3:].split(b'\r\n\r\n')[0].split(b'\r\n')[1]
                    # didn't take password from content_list so that password is bytes
                }
            elif packet_type == 4:
                if packet_mode != 4:
                    raise ValueError('Unacceptable package')
                if packet_success == 0:
                    return {
                        'type': 'login_success'
                    }
                elif packet_success == 1:
                    return {
                        'type': 'login_error',
                        'result': content
                    }
            elif packet_type == 5:
                if packet_mode != 4:
                    raise ValueError('Unacceptable package')
                return {
                    'type': 'registration',
                    'nickname': packet[3:].split(b'\r\n\r\n')[0].split(b'\r\n')[0].decode('ascii'),
                    'password': packet[3:].split(b'\r\n\r\n')[0].split(b'\r\n')[1]
                    # didn't take password from content_list so that password is bytes
                }
            elif packet_type == 6:
                if packet_mode != 4:
                    raise ValueError('Unacceptable package')
                if packet_success == 0:
                    return {
                        'type': 'registration_success'
                    }
                elif packet_success == 1:
                    return {
                        'type': 'registration_error',
                        'result': content
                    }
            elif packet_type == 7:
                return {
                    'type': 'history_request'
                }
            elif packet_type == 8:
                if packet_success == 0:
                    return {
                        'type': 'history_response',
                        'history': content.split('\r\n')
                    }
                elif packet_success == 1:
                    return {
                        'type': 'history_error',
                        'result': content
                    }
        else:
            raise ValueError("Wrong protocol version")

    def encode(self, data: dict) -> bytes:
        """
        Encodes specially formatted dictionary internally used to
        encode data to CATP packet / byte string which could be then sent.
        :param data: dictionary containing data needed to be converted
        to package.
        :return: CATP packet in form of byte string.
        """
        if self.version == '0.0.1':
            if 'type' in data:
                if data['type'] == 'error' or data['type'] == 'success':
                    # response to computation request
                    packet_type = 1
                else:
                    # progress response
                    packet_type = 2
            else:
                # computation request
                packet_type = 0
            # next we choose computation mode (contains in all types of packages)
            if data['mode'] == 'derivative':
                packet_mode = 0
            elif data['mode'] == 'def_integral':
                packet_mode = 1
            elif data['mode'] == 'indef_integral':
                packet_mode = 2
            elif data['mode'] == 'simplify':
                packet_mode = 3
            else:
                raise ValueError("Unknown mode")
            content = str()
            if packet_type == 0:
                if packet_mode == 0:
                    # deleting all the spaces for more compact placing
                    content = data['function'].replace(" ", "")
                    # using vertical bar symbols as delimiters in packet
                    for var in data['order']:
                        content = content + '|' + var.replace(" ", "")
                elif packet_mode == 1:
                    content = data['function'].replace(" ", "") + '|' \
                              + data['variables'][0].replace(" ", "") + '|' \
                              + data['interval'][0].replace(" ", "") + ' ' \
                              + data['interval'][1].replace(" ", "")
                elif packet_mode == 2:
                    content = data['function'].replace(" ", "") + '|' \
                              + data['variables'][0].replace(" ", "")
                elif packet_mode == 3:
                    content = data['expression'].replace(" ", "")
            else:
                content = data['result'].strip()
            content = content.encode('ascii')
            content_len = len(content)
            if content_len > 255:
                raise ValueError("Too much content")
            is_error = 0
            if packet_type == 1 and data['type'] == 'error':
                is_error = 1
            res = bytes([packet_type, content_len,
                         packet_mode, is_error]) + content
            return res
        elif self.version == '0.0.2':
            # resolving packet type
            if 'type' not in data:
                packet_type = 0
            else:
                if data['type'] == 'error' or data['type'] == 'success':
                    # response to computation request
                    packet_type = 1
                elif data['type'] == 'progress':
                    packet_type = 2
                elif data['type'] == 'login':
                    packet_type = 3
                elif data['type'] == 'login_success' or data['type'] == 'login_error':
                    packet_type = 4
                elif data['type'] == 'registration':
                    packet_type = 5
                elif data['type'] == 'registration_success' or data['type'] == 'registration_error':
                    packet_type = 6
                elif data['type'] == 'history_request':
                    packet_type = 7
                elif data['type'] == 'history_success' or data['type'] == 'history_error':
                    packet_type = 8
                else:
                    raise ValueError("Unacceptable dictionary")
            # resolving packet mode
            if 'mode' not in data:
                packet_mode = 4
            else:
                if data['mode'] == 'derivative':
                    packet_mode = 0
                elif data['mode'] == 'def_integral':
                    packet_mode = 1
                elif data['mode'] == 'indef_integral':
                    packet_mode = 2
                elif data['mode'] == 'simplify':
                    packet_mode = 3
                else:
                    raise ValueError('Unacceptable dictionary')
            # resolving packet success
            if packet_type in (0, 2, 3, 5, 7):
                packet_success = 0
            else:
                if 'success' in data['type']:
                    packet_success = 0
                elif 'error' in data['type']:
                    packet_success = 1
                else:
                    raise ValueError('Unacceptable dictionary')
            # constructing packet content
            content = str()
            if packet_type == 0:
                if packet_mode == 0:
                    # deleting all the spaces for more compact placing
                    content = data['function'].replace(" ", "")
                    # using vertical bar symbols as delimiters in packet
                    for var in data['order']:
                        content = content + '|' + var.replace(" ", "")
                elif packet_mode == 1:
                    content = data['function'].replace(" ", "") + '|' \
                              + data['variables'][0].replace(" ", "") + '|' \
                              + data['interval'][0].replace(" ", "") + ' ' \
                              + data['interval'][1].replace(" ", "")
                elif packet_mode == 2:
                    content = data['function'].replace(" ", "") + '|' \
                              + data['variables'][0].replace(" ", "")
                elif packet_mode == 3:
                    content = data['expression'].replace(" ", "")
                content = content.encode('ascii')
            elif packet_type in (1, 2):
                content = data['result'].strip().encode('ascii')
            elif packet_type in (3, 5):
                content = data["nickname"].encode("ascii") + b'\r\n' + data["password"]
            elif packet_type in (4, 6):
                if packet_success == 0:
                    content = b''
                else:
                    content = data['result'].encode('ascii')
            elif packet_type == 7:
                content = b''
            elif packet_type == 8:
                if packet_success == 0:
                    sep = '\r\n'
                    content = sep.join(data['history']).encode('ascii')
                else:
                    content = data['history'].encode('ascii')
            res = bytes([packet_type, packet_mode, packet_success]) + content + b'\r\n\r\n'
            return res
        else:
            raise ValueError('Wrong protocol version')


if __name__ == "__main__":
    cp = CATP(version='0.0.2')
    data = {
        'type': 'history_error',
        'history': "AAAAAA BLYATB AAAAAA"
    }
    print(data)
    packet = cp.encode(data)
    print(packet)
    data = cp.decode(packet)
    print(data)
