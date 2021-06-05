

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
        return dict()

    def encode(self, data: dict) -> bytes:
        """
        Encodes specially formatted dictionary internally used to
        encode data to CATP packet / byte string which could be then sent.
        :param data: dictionary containing data needed to be converted
        to package.
        :return:
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
                    content = data['function'].replace(" ", "") + '|'
                    # using vertical bar symbols as delimiters in packet
                    for var in data['order']:
                        content = content + var.replace(" ", "")
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
            return bytes([0 for i in range(4)])


if __name__ == '__main__':
    encoder = CATP()
    print(encoder.encode({
        'type': 'error',
        'mode': 'simplify',  # or any other mode from request
        'result': 'Some shitty error'
    }))
