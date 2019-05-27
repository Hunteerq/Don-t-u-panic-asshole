import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
for pings in range(10):

    message = b'test'
    addr = ("127.0.0.1", 7070)

    client_socket.sendto(message, addr)
    try:
        data, server = client_socket.recvfrom(1024)
        print(f'{data} {pings}')
    except socket.timeout:
        print('REQUEST TIMED OUT')
