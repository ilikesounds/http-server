# -*- encoding: utf-8 *-*
'''This is an http-server'''

import socket

import email.utils


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
        full_mes = b''
        while not message_complete:
            partial_mes = conn.recv(buffer_length)
            full_mes += partial_mes
            if len(partial_mes) < buffer_length:
                message_complete = True
                full_mes_decoded_to_unicode = full_mes.decode('utf8')
        print(u'request:\r\n', full_mes_decoded_to_unicode)
        conn.sendall(response_ok())
        conn.close()
        server.close()


def response_ok():
    """Generate response_ok."""
    lines = []
    first_line = 'HTTP/1.1 200 OK'
    lines.append(first_line)
    headers = {}
    body = 'Success!'
    headers['Content-Type'] = 'text/plain; charset=utf-8'
    headers['Content-Length'] = str(len(body.encode('utf8')))
    now = email.utils.formatdate(usegmt=True)
    headers['Date'] = now
    header_lines = [': '.join(item) for item in headers.items()]
    lines.extend(header_lines)
    lines.append('')
    lines.append(body)
    CRLF = '\r\n'
    response = CRLF.join(lines)
    response = response.encode('utf8')
    return response


def response_deconstructor(response):
    """Deconstruct response into basic components.
    Return protocol, status, status message,
    headers as dictionary, length of body, number of components
    separated by first empty line."""
    response_msg = response
    uresponse = response_msg.decode('utf8')
    CRLF = '\r\n'
    uresponse.split(CRLF)
    first_pass = uresponse.split(CRLF+CRLF, 1)
    head, body = first_pass
    head_lines = head.split(CRLF)
    protocol, status, msg = head_lines[0].split()
    headers = head_lines[1:]
    headers_split = [header.split(':', 1) for header in headers]
    headers_dict = {k.lower(): v.strip() for k, v in headers_split}
    return [protocol, status, msg, headers_dict,
            str(len(body)), str(len(first_pass))]


def response_error():
    """Generate response_error."""
    response = u'HTTP/1.1 500 Internal_Server_Error\r\n\r\nFailure'
    return response.encode('utf8')


if __name__ == '__main__':
    server()
