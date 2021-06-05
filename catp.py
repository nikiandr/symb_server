

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
    def __init__(self, version: str = '0.0.1'):
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
        else:
            return dict()

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
            packet = bytes([packet_type, content_len,
                            packet_mode, is_error]) + content
            return packet
        else:
            return bytes([0] * 4)
