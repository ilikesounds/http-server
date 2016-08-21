# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest

from server import response_ok, response_deconstructor,\
 request_deconstructor, parse_req, response_decision, resolve_uri,\
 generate_response

from client import client

REQUEST_GOOD = [
    b'GET / HTTP/1.1\r\n'
    b'Host: 127.0.0.1:5000\r\n'
    b'Connection: keep-alive\r\n'
    b'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    b'(KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36\r\n'
    b'Accept: */*\r\n'
    b'DNT: 1\r\n'
    b'Referer: http://127.0.0.1:5000/\r\n'
    b'Accept-Encoding: gzip, deflate, sdch\r\n'
    b'Accept-Language: en-US,en;q=0.8\r\n\r\n'
]

REQUEST_BAD = [
    b'POST / HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n'
    b'Connection: keep-alive\r\n\r\n',

    b'GET / HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n'
    b'Connection: keep-alive\r\n\r\n',

    b'GET / HTTP/1.1\r\nConnection: keep-alive\r\n\r\n',

    b'GET / HTTP/1.1\r\nConnecti'
]

RESPONSE_ERROR = [
    b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
    b'The server supports HTTP/1.1 only.',

    b'HTTP/1.1 505 HTTP Version Not supported\r\n\r\n'
    b'The server supports HTTP/1.1 only.',

    b'HTTP/1.1 400 Bad Request\r\n\r\n'
    b'No <host> in headers.',

    b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
    b'Something went wrong.'
]

RESPONSE_404 = [
    b'HTTP/1.1 404 Resource Not Found\r\n\r\n'
    b"HTTP Error 404: I can't find what you are looking for."
]

RESPONSE_OK = [
    b'HTTP/1.1 200 OK\r\nDate: Fri, 19 Aug 2016 04:28:51 GMT\r\n'
    b'Content-Length: 8\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n'
    b'Success!'
]

REQUEST_DECON_TABLE1 = [
    ('GET', request_deconstructor(REQUEST_GOOD[0])[0]),
    ('/', request_deconstructor(REQUEST_GOOD[0])[1]),
    ('HTTP/1.1', request_deconstructor(REQUEST_GOOD[0])[2]),
]

REQUEST_DECON_TABLE2 = [
    ('host', request_deconstructor(REQUEST_GOOD[0])[3])
]

RESPONSE_OK_DECON = response_deconstructor(response_ok(b'Success!'))

RESPONSE_DECON_TABLE1 = [
   ('content-length', RESPONSE_OK_DECON[3]),
   ('content-type', RESPONSE_OK_DECON[3]),
   ('date', RESPONSE_OK_DECON[3]),
]

RESPONSE_DECON_TABLE2 = [
   ('HTTP/1.1', RESPONSE_OK_DECON[0]),
   ('200', RESPONSE_OK_DECON[1]),
   ('OK', RESPONSE_OK_DECON[2]),
   ('8', RESPONSE_OK_DECON[4])
]

GENERATE_RESPONSE = [
    ('/sample.txt', '95', "('text/plain', None)"),
    ('/a_web_page.html', '125', "('text/html', None)"),
    ('/make_time.py', '278', "('text/x-python', None)"),
    ('/images/sample_1.png', '8760', "('image/png', None)"),
    ('/images/JPEG_example.jpg', '15138', "('image/jpeg', None)"),
    ('/empty_file.txt', '0', "('text/plain', None)"),
]

EMPTY_URI = [
   '/non_existant_file.txt',
    '/non_existant_folder'
]


@pytest.mark.parametrize('part, result', RESPONSE_DECON_TABLE1)
def test_response_ok_headers(part, result):
    """Test whether response_ok() generates response in appropriate format
     by using response_deconstructor(response_ok()). Checking for the presence
     of particular headers."""
    assert part in result


@pytest.mark.parametrize('part, result', RESPONSE_DECON_TABLE2)
def test_response_ok_first_line_and_body_length(part, result):
    """Test whether response_ok() generates response in appropriate format
     by using response_deconstructor(response_ok()). Checking for the right
     components in the first line and correct lenght of the body."""
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_DECON_TABLE1)
def test_request_deconstructor(part, result):
    """Test whether the client request is appropriately formatted
     by using request_deconstructor(request). Checking for <GET>, <HTTP/1.1>,
     and <PATH> in the first line of the request."""
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_DECON_TABLE2)
def test_request_decon2(part, result):
    """Test whether the client request is appropriately formatted
     by using request_deconstructor(request). Checking for the
     <host> header in the request."""
    assert part in result


def test_parse_req_no_get():
    """Test whether parse_req(request) raises <NotImplementedError>
     given a request with <POST> instead of <GET>."""
    with pytest.raises(NotImplementedError):
        parse_req(b'POST ./webroot HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_no_http1_1():
    """Test whether parse_req(request) raises <TypeError>
     given a request with <HTTP/1.0> instead of <HTTP/1.1>."""
    with pytest.raises(TypeError):
        parse_req(b'GET ./webroot HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_no_host():
    """Test whether parse_req(request) raises <NameError>
     given a request with the <host> header."""
    with pytest.raises(NameError):
        parse_req(b'GET ./webroot HTTP/1.1\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_good():
    """Test whether parse_req(request) returns URI
    for an appropriatly formed request."""
    assert parse_req(REQUEST_GOOD[0]) == '/'


# Gave up - couldn't resolve errors,
# substituted by the tests that follow right after this one.
#
# RESPONSE_DECISION_TABLE = [
#     ('POST ./webroot HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n'
#     'Connection: keep-alive\r\n\r\n',
#     'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
#     'The server supports HTTP/1.1 only.'),
#     ('GET ./webroot HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n'
#     'Connection: keep-alive\r\n\r\n',
#     'HTTP/1.1 505 HTTP Version Not supported\r\n\r\n'
#     'The server supports HTTP/1.1 only.',)
# ]
# @pytest.mark.parametrize('request, response', RESPONSE_DECISION_TABLE)
# def test_response_decision_generate_error_response(request, response):
#     """Test whether response_decision(request) generates an appropriate
#      error message and returns URI = None given a bad request."""
#     assert response_decision(request) == response

def test_response_decision_generate_error_response():
    """Test whether response_decision(request) generates an appropriate
     error message and returns URI = None given a bad request."""
    assert response_decision(REQUEST_BAD[0]) == RESPONSE_ERROR[0]
    assert response_decision(REQUEST_BAD[1]) == RESPONSE_ERROR[1]
    assert response_decision(REQUEST_BAD[2]) == RESPONSE_ERROR[2]
    assert response_decision(REQUEST_BAD[3]) == RESPONSE_ERROR[3]


def test_response_decision_generate_ok_response():
    """Test whether response_decision(response) generates an OK-response
     given a good request. Compare firs 16 chars in response_ok string,
     therefore excluding Date and everything after that."""
    assert response_decision(REQUEST_GOOD[0])[:17] == \
        RESPONSE_OK[0][:17]


def test_receive_response():
    """
    Functional test which determines whether server
    is sending back correct info to a client
    """
    assert client(REQUEST_BAD[0]) == RESPONSE_ERROR[0]
    assert client(REQUEST_BAD[1]) == RESPONSE_ERROR[1]
    assert client(REQUEST_BAD[2]) == RESPONSE_ERROR[2]
    assert client(REQUEST_GOOD[0])[:17] == RESPONSE_OK[0][:17]


@pytest.mark.parametrize('uri', EMPTY_URI)
def test_resolve_uri(uri):
    """ Test whether resolve_uri(uri) returns False if uri doesn't exist."""
    assert not resolve_uri(uri)


@pytest.mark.parametrize('uri', EMPTY_URI)
def test_generate_response_no_uri(uri):
    """Test whether 404 response generated when uri doesn't exist."""
    assert generate_response(uri) == RESPONSE_404[0]


@pytest.mark.parametrize('path, body_length, mime', GENERATE_RESPONSE)
def test_generate_response(path, body_length, mime):
    """Test whether generate_response(uri) generates:
      an ok-message with the right body length if file found."""
    response = generate_response(path)
    decon = response_deconstructor(response)
    assert decon[3]['content-length'] == body_length
    assert decon[3]['content-type'] == mime
