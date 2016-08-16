# -*- encoding: utf-8 *-*
'''This is an http-server'''

import socket


def server():
    """Set up a server socket, receive and send back a msg to a client."""
    while True:
        print('started')
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = ('127.0.0.1', 5000)
        server.bind(address)
        server.listen(1)
        conn, addr = server.accept()

        buffer_length = 32
        message_complete = False
        part = b''
        while not message_complete:
            partial_mes = conn.recv(buffer_length)
            print('partial_mes ', partial_mes)
            part += partial_mes
            print('part before if', part)
            if len(partial_mes) < buffer_length:
                message_complete = True
        print('part after if', part.decode('utf8'))
        conn.sendall(part)
        conn.close()
        server.close()
        
