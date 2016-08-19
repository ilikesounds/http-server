# -*- encoding: utf-8 *-*
'''This is an http-server'''

import socket

import email.utils

CRLF = '\r\n'


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
        response_mes, uri = response_decision(full_mes)
        conn.sendall(response_mes)
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
    first_pass = urequest.split(CRLF+CRLF, 1)
    head, body = first_pass
    head_lines = head.split(CRLF)
    method, path, protocol = head_lines[0].split()
    headers = head_lines[1:]
    headers_split = [header.split(':', 1) for header in headers]
    headers_dict = {k.lower(): v.strip() for k, v in headers_split}
    return [method, path, protocol, headers_dict, str(len(first_pass))]

# '405 Method Not Allowed'
# '505 HTTP Version Not supported'
# '400 Bad request'
# '404 Not Found'


class HTTPException(Exception):
    def __init__(self, code, reason, html_string):
        self.code = code
        self.reason = reason
        self.html_string = html_string

    def response_msg(self):
        template = u'HTTP/1.1 {} {}\r\n\r\n{}'
        return template.format(self.code, self.reason, self.html_string).encode('utf-8')


def parse_req(request):
    request_decon = request_deconstructor(request)
    print(request_decon)
    if request_decon[0] != u'GET':
        raise NotImplementedError(u'Method not allowed')
    elif request_decon[2] != u'HTTP/1.1':
        raise TypeError(u'Version of HTTP not supported')
    elif u'host' not in request_decon[3]:
        raise NameError(u'No <host> in headers')
    return request_decon[1]


def response_decision(full_mes):
    uri = None
    try:
        parse_req(full_mes)
    except NotImplementedError:
        response = HTTPException('405', 'Method Not Allowed', 'The server supports HTTP/1.1 only.').response_msg()
    except TypeError:
        response = HTTPException('505', 'HTTP Version Not supported', 'The server supports HTTP/1.1 only.').response_msg()
    except NameError:
        response = HTTPException('400', 'Bad Request', 'No <host> in headers.').response_msg()
    except:
        response = HTTPException('500', 'Internal Server Error', 'Something went wrong.').response_msg()
    else:
        response = response_ok()
        uri = parse_req(full_mes)
    print(response, uri)
    return [response, uri]

# if __name__ == '__main__':
#     server()
