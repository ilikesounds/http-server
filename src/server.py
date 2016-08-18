# -*- encoding: utf-8 *-*
'''This is an http-server'''

import socket

import email.utils


def server():
    """Set up a server socket, receive and send back a msg to a client."""
    while True:
        print('started')
        server = socket.socket()
        address = ('127.0.0.1', 5000)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        if parse_req(full_mes):
            conn.sendall(response_ok())
        else:
            conn.sendall(response_error(parse_req(full_mes)))
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
    first_pass = uresponse.split(CRLF+CRLF, 1)
    head, body = first_pass
    head_lines = head.split(CRLF)
    protocol, status, msg = head_lines[0].split()
    headers = head_lines[1:]
    headers_split = [header.split(':', 1) for header in headers]
    headers_dict = {k.lower(): v.strip() for k, v in headers_split}
    return [protocol, status, msg, headers_dict,
            str(len(body)), str(len(first_pass))]


def request_deconstructor(request):
    """Deconstruct request into basic components.
    Return method, protocol and validates host header"""
    request_msg = request
    urequest = request_msg.decode('utf8')
    CRLF = '\r\n'
    first_pass = urequest.split(CRLF+CRLF, 1)
    head, body = first_pass
    head_lines = head.split(CRLF)
    method, path, protocol = head_lines[0].split()
    headers = head_lines[1:]
    headers_split = [header.split(':', 1) for header in headers]
    headers_dict = {k.lower(): v.strip() for k, v in headers_split}
    return [method, path, protocol, headers_dict, str(len(first_pass))]


def parse_req(request):
    print(request)
    req_decon = request_deconstructor(request)
    req_decon.extend(req_decon[3].keys())
    try:
        for word in req_decon:
            try:
                word in (u'GET',  u'HTTP/1.1', u'host')
            except:
                raise IndexError(u'This is not a ' + word + ' request')
            else:
                return True
    except IndexError:
        return word


def response_error(word):
    """Generate response_error."""
    response = u' ' + word + '400 Bad_Request' +'\r\n\r\nThis request does not have ' + word
    return response.encode('utf8')


if __name__ == '__main__':
    server()
