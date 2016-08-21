# -*- encoding: utf-8 *-*
# This is an http-server#
from __future__ import unicode_literals
import socket
import io
import email.utils
from mimetypes import guess_type
import os


CRLF = '\r\n'
ABS_PATH = os.path.abspath(__file__).rsplit('/', 2)[0] + '/webroot'


def server(address, server_socket):
    """Set up a server socket, receive and send back a msg to a client."""
    while True:
        print('started')
        server = server_socket
        #address = ('127.0.0.1', 5000)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(1)
        conn, addr = server.accept()
        buffer_length = 32
        message_complete = False
        request = b''
        while not message_complete:
            buffer_req = conn.recv(buffer_length)
            request += buffer_req
            if len(buffer_req) < buffer_length:
                message_complete = True
        response = response_decision(request)
        conn.sendall(response)
        conn.close()
        server.close()


def response_ok(body, mime=None):
    """Generate response_ok."""
    try:
        body = body.encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass
    lines = []
    first_line = 'HTTP/1.1 200 OK'
    lines.append(first_line)
    headers = {}
    headers['Content-Type'] = str(mime)
    headers['Content-Length'] = str(len(body))
    now = email.utils.formatdate(usegmt=True)
    headers['Date'] = now
    header_lines = [': '.join(item) for item in headers.items()]
    lines.extend(header_lines)
    lines.append('')
    response = CRLF.join(lines) + CRLF
    response = response.encode('utf8')
    response += body
    return response


def response_deconstructor(response):
    """Deconstruct response into basic components.
    Return protocol, status, status message,
    headers as dictionary, length of body, number of components
    separated by first empty line."""
    response_msg = response
    delimeter = (CRLF+CRLF).encode('utf-8')
    first_pass = response_msg.split(delimeter, 1)
    head, body = first_pass
    head_lines = head.decode('utf-8').split(CRLF)
    protocol, status, msg = head_lines[0].split()
    headers = head_lines[1:]
    headers_split = [header.split(':', 1) for header in headers]
    headers_dict = {k.lower(): v.strip() for k, v in headers_split}
    return [protocol, status, msg, headers_dict,
            str(len(body))]


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


class HTTPException(Exception):
    def __init__(self, code, reason, msg_string):
        """Initiate an instance of HTTPException
         with attributes: <code>, <reason>, <msg_string>."""
        self.code = code
        self.reason = reason
        self.msg_string = msg_string

    def response_msg(self):
        """Generate an error message using <code>,
         <reason>, <msg_string>. Return a byte-string"""
        template = u'HTTP/1.1 {} {}\r\n\r\n{}'
        return template.format(self.code, self.reason, self.msg_string)\
            .encode('utf-8')


def parse_req(request):
    """Raise an appropriate error for a bad request or
     return URI for a good request."""
    request_decon = request_deconstructor(request)
    if request_decon[0] != u'GET':
        raise NotImplementedError(u'Method not allowed')
    elif request_decon[2] != u'HTTP/1.1':
        raise TypeError(u'Version of HTTP not supported')
    elif u'host' not in request_decon[3]:
        raise NameError(u'No <host> in headers')
    return request_decon[1]


def response_decision(request):
    """Based on the raised error, return an appropriate http-exception
     and return URI = 'None'. Return an ok-response and URI for a
     good request. Response = byte-string, uri = unicode-string."""
    uri = u'None'
    try:
        parse_req(request)
    except NotImplementedError:
        response = HTTPException(u'405', u'Method Not Allowed',
                                 u'The server supports HTTP/1.1 only.')
        response = response.response_msg()
    except TypeError:
        response = HTTPException(u'505', u'HTTP Version Not supported',
                                 u'The server supports HTTP/1.1 only.')
        response = response.response_msg()
    except NameError:
        response = HTTPException(u'400', u'Bad Request',
                                 u'No <host> in headers.')
        response = response.response_msg()
    except:
        response = HTTPException(u'500', u'Internal Server Error',
                                 u'Something went wrong.')
        response = response.response_msg()
    else:
        uri = parse_req(request)
        response = generate_response(uri)
    return response


def resolve_uri(uri):
    """Return body and mimetype for a given uri or False if
     source not found."""
    path = ABS_PATH + uri
    if os.path.isfile(path):
        files = io.open(path, 'rb')
        mime = guess_type(path)
        read_file = files.read()
        files.close()
        return (read_file, mime)
    elif os.path.isdir(path):
        return (str(os.listdir(path)), None)
    else:
        return False


def generate_response(uri):
    """Generate a response based on the return of resolve_uri(uri):
     a. - ok-message with body and mime if file was found,
     b. - 404 Not Found error msg if file was not found."""
    if resolve_uri(uri):
        body, mime = resolve_uri(uri)
        response = response_ok(body, mime)
    else:
        response = HTTPException(
            u'404',
            u'Resource Not Found',
            u"HTTP Error 404: I can't find what you are looking for.")
        response = response.response_msg()
    return response


if __name__ == '__main__':
    server()
