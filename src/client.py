# -*- encoding: utf-8 *-*
'''This is an http-client'''

import socket

MESSAGE = u'Test' * 8


def client(message):
    """Set up a client socket, send and receive a msg from server."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))

    buffer_length = 32
    reply_complete = False
    part = b''
    while not reply_complete:
        partial_mes = client.recv(buffer_length)
        part += partial_mes
        if len(partial_mes) < buffer_length:
            reply_complete = True
    print(part.decode('utf-8'))
    client.close()
    return part.decode('utf-8')
