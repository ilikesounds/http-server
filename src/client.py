# -*- encoding: utf-8 *-*
'''This is an http-client'''

import socket

MESSAGE = u'Test' * 8


def client(message):
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))

    buffer_length = 32
    reply_complete = False
    part = b''
    while not reply_complete:
        part += client.recv(buffer_length)
        if len(part) < buffer_length:
            reply_complete = True
    print(part.decode('utf-8'))
    client.close()
