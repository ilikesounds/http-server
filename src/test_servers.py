# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest

from server import response_ok, response_deconstructor,\
 request_deconstructor, parse_req, response_decision

from client import client

RESPONSE_TABLE = [
   ('content-length', response_deconstructor(response_ok())[3]),
   ('content-type', response_deconstructor(response_ok())[3]),
   ('date', response_deconstructor(response_ok())[3]),
]

FIRST_LINE_BODY_LENGTH_TABLE = [
   ('HTTP/1.1', response_deconstructor(response_ok())[0]),
   ('200', response_deconstructor(response_ok())[1]),
   ('OK', response_deconstructor(response_ok())[2]),
   ('8', response_deconstructor(response_ok())[4]),
]

REQUEST_GOOD = b'GET /favicon.ico HTTP/1.1\r\n'\
    b'Host: 127.0.0.1:5000\r\n'\
    b'Connection: keep-alive\r\n'\
    b'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '\
    b'(KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36\r\n'\
    b'Accept: */*\r\n'\
    b'DNT: 1\r\n'\
    b'Referer: http://127.0.0.1:5000/\r\n'\
    b'Accept-Encoding: gzip, deflate, sdch\r\n'\
    b'Accept-Language: en-US,en;q=0.8\r\n\r\n'

REQUEST_DECON_TABLE1 = [
   ('GET', request_deconstructor(REQUEST_GOOD)[0]),
   ('/favicon.ico', request_deconstructor(REQUEST_GOOD)[1]),
   ('HTTP/1.1', request_deconstructor(REQUEST_GOOD)[2]),
]

REQUEST_DECON_TABLE2 = [
    ('host', request_deconstructor(REQUEST_GOOD)[3])
]

REQUEST_BAD = [
    b'POST /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n'
    b'Connection: keep-alive\r\n\r\n',

    b'GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n'
    b'Connection: keep-alive\r\n\r\n',

    b'GET /favicon.ico HTTP/1.1\r\nConnection: keep-alive\r\n\r\n',

    b'GET /favicon.ico HTTP/1.1\r\nConnecti'
]

RESPONSE_DECISION = [
    (b'HTTP/1.1 405 Method Not Allowed\r\n\r\n'
     b'The server supports HTTP/1.1 only.',
     'None'),

    (b'HTTP/1.1 505 HTTP Version Not supported\r\n\r\n'
     b'The server supports HTTP/1.1 only.',
     'None'),

    (b'HTTP/1.1 400 Bad Request\r\n\r\n'
     b'No <host> in headers.',
     'None'),

    (b'HTTP/1.1 200 OK\r\nDate: Fri, 19 Aug 2016 04:28:51 GMT\r\n'
     b'Content-Length: 8\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n'
     b'Success!',
     u'/favicon.ico'),

    (b'HTTP/1.1 500 Internal Server Error\r\n\r\n'
     b'Something went wrong.',
     'None')
]


@pytest.mark.parametrize('part, result', RESPONSE_TABLE)
def test_response_ok_headers(part, result):
    """Test whether response_ok() generates response in appropriate format
     by using response_deconstructor(response_ok()). Checking for the presence
     of particular headers."""
    assert part in result


@pytest.mark.parametrize('part, result', FIRST_LINE_BODY_LENGTH_TABLE)
def test_response_ok_first_line_and_body_length(part, result):
    """Test whether response_ok() generates response in appropriate format
     by using response_deconstructor(response_ok()). Checking for the right
     components in the first line and correct lenght of the body."""
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_DECON_TABLE1)
def test_request_deconstructor(part, result):
    """Test whether the client request is appropriately formatted
     by using request_deconstructor(request). Checking for the right components
     in the first line of the request."""
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
        parse_req(b'POST /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_no_http1_1():
    """Test whether parse_req(request) raises <TypeError>
     given a request with <HTTP/1.0> instead of <HTTP/1.1>."""
    with pytest.raises(TypeError):
        parse_req(b'GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_no_host():
    """Test whether parse_req(request) raises <NameError>
     given a request with the <host> header."""
    with pytest.raises(NameError):
        parse_req(b'GET /favicon.ico HTTP/1.1\r\n'
                  b'Connection: keep-alive\r\n\r\n')


def test_parse_req_good():
    """Test whether parse_req(request) returns URI
    for an appropriatly formed request."""
    assert parse_req(REQUEST_GOOD) == '/favicon.ico'


def test_response_decision_generate_error_response():
    """Test whether response_decision(request) generates an appropriate
     error message and returns URI = None given a bad request."""
    assert response_decision(REQUEST_BAD[0])[0] == RESPONSE_DECISION[0][0]
    assert response_decision(REQUEST_BAD[0])[1] == RESPONSE_DECISION[0][1]

    assert response_decision(REQUEST_BAD[1])[0] == RESPONSE_DECISION[1][0]
    assert response_decision(REQUEST_BAD[1])[1] == RESPONSE_DECISION[1][1]

    assert response_decision(REQUEST_BAD[2])[0] == RESPONSE_DECISION[2][0]
    assert response_decision(REQUEST_BAD[2])[1] == RESPONSE_DECISION[2][1]

    assert response_decision(REQUEST_BAD[3])[0] == RESPONSE_DECISION[4][0]
    assert response_decision(REQUEST_BAD[3])[1] == RESPONSE_DECISION[4][1]


def test_response_decision_generate_ok_response():
    """Test whether response_decision(response) generates an OK-response
     given a good request. Compare firs 16 chars in response_ok string,
     therefore excluding Date and everything after that."""
    assert response_decision(REQUEST_GOOD)[0][:17] == \
        RESPONSE_DECISION[3][0][:17]
    assert response_decision(REQUEST_GOOD)[1][:17] == \
        RESPONSE_DECISION[3][1]


def test_receive_response():
    """
    Functional test which determines whether server
    is sending back correct info to a client
    """
    assert client(REQUEST_BAD[0]) == RESPONSE_DECISION[0][0]
    assert client(REQUEST_BAD[1]) == RESPONSE_DECISION[1][0]
    assert client(REQUEST_BAD[2]) == RESPONSE_DECISION[2][0]
    assert client(REQUEST_GOOD)[:17] == RESPONSE_DECISION[3][0][:17]
