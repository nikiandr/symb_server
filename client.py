import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 6666))
try:
    while True:
        print("Enter command: ")
        server.send(input().encode('ascii'))
        result = server.recv(1024).decode('ascii')
        print(result)
except KeyboardInterrupt:
    pass

{
    'mode': 'derivative',
    'variables': ['x'],
    'function': 'x**2',
    'order': ['x']  # 'order': ['x', 'x']
}

{
    'mode': 'derivative',
    'variables': ['x', 'y', 'z'],
    'function': 'x**2 + y**2 + z**2',
    'order': ['x', 'x', 'y', 'z']  # d^4 f / d^2 x dy dz
}

{
    'mode': 'indef_integral',
    'variables': ['x'],
    'function': 'x**2'
}

{
    'mode': 'def_integral',
    'variables': ['x'],
    'function': 'x**2',
    'interval': ('0', '1')
}

{
    'mode': 'simplify',
    'variables': ['x', 'y'],
    'expression': 'sin(x)**2 + cos(x)**2 + sin(y)**2 + cos(y)**2',
}

{
    'mode': 'fourier_series',
    'variables': ['x'],
    'function': 'sin(x)',
    'interval': ('-pi', 'pi')
}
