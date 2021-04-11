import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("localhost", 4446))
print("Enter command: ")
server.send(input().encode('ascii'))
result = server.recv(1024).decode('ascii')
print(result)
