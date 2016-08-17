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
            part += partial_mes
            if len(partial_mes) < buffer_length:
                message_complete = True
                part_decoded_to_unicode = part.decode('utf8')
        print(u'request:\r\n', part_decoded_to_unicode)
        conn.sendall(response_ok())
        conn.close()
        server.close()
        return part_decoded_to_unicode


def response_ok():
    response = 'HTTP/1.1 200 OK \r\n\r\n Success'
    return response.encode('utf8')


def response_error():
    response = 'HTTP/1.1 500 Internal_Server_Error'
    return response.encode('utf8')


if __name__ == '__main__':
    server()
