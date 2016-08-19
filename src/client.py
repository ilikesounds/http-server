# -*- encoding: utf-8 *-*
'''This is an http-client'''

import socket

import sys


def client(message):
    """Set up a client socket, send and receive a msg from a server."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    try:
        message = message.decode('utf8')
    except AttributeError:
        pass
    client.sendall(message.encode('utf8'))
    print(type(message))
    client.shutdown(socket.SHUT_WR)
    buffer_length = 32
    reply_complete = False
    full_mes = b''
    while not reply_complete:
        partial_mes = client.recv(buffer_length)
        full_mes += partial_mes
        if len(partial_mes) < buffer_length:
            reply_complete = True
    print(full_mes.decode('utf-8'))
    client.close()
    return full_mes.decode('utf-8')


if __name__ == '__main__':
    message = sys.argv[1]
    client(message)
