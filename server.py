import socket
from datetime import datetime
import sym_wrapper as sw
import catp as cp
import threading as td
import time
import dbinteraction as dbi


def process_messages(client):
    db = dbi.db_connect()
    uid = int()
    is_logged_in = False
    try:
        while True:

            data = cp.catp_mess_get(client)
            if not data:
                break
            print(f"Message received: {data}")
            ec = cp.CATP()
            req = ec.decode(data)
            auth = 'type' in req
            if auth:
                if req['type'] == 'login':
                    res, uid = dbi.login(db, req['nickname'], req['password'].decode('ascii'))
                    is_logged_in = (res['type'] == 'login_success')
                elif req['type'] == 'registration':
                    res, uid = dbi.register(db, req['nickname'], req['password'].decode('ascii'))
                    is_logged_in = (res['type'] == 'registration_success')
                elif req['type'] == 'history_request':
                    res = dbi.read_history(db, uid)
            else:
                res = sw.parse_request(req)
                time.sleep(1)
                for i in range(10, 100, 10):
                    preq = {
                        'type': 'progress',
                        'mode': res['mode'],
                        'result': f'Progress {i}/100'
                    }
                    db.commit()
                    client.sendall(ec.encode(preq))
                    if is_logged_in:
                        dbi.add_history(db, uid, {"No request": None}, preq)
                    time.sleep(1)
            response = ec.encode(res)
            client.sendall(response)
            if is_logged_in and req['type'] != 'history_request':
                dbi.add_history(db, uid, req, res)
            print(f"Response sent: " +
                  f"{len(response)} bytes")
            db.commit()
    except ConnectionError:
        db.close()


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
