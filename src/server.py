# -*- encoding: utf-8 *-*
'''This is an http-server'''

import socket


def server():
    print('started')
    server = socket.socket()
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()

    buffer_length = 32
    message_complete = False
    part = b''
    while not message_complete:
        part += conn.recv(buffer_length)
        print(part.decode('utf8'))
        if len(part) < buffer_length:
            message_complete = True
    print(part)
    conn.sendall(part)
    conn.close()
    server.close()
    print('stopped')
