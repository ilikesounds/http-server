# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest

from server import response_ok, response_deconstructor,\
 request_deconstructor, parse_req, response_decision

RESPONSE_TABLE = [
   ('content-length', response_deconstructor(response_ok())[3]),
   ('content-type', response_deconstructor(response_ok())[3]),
   ('date', response_deconstructor(response_ok())[3]),
]

# FIRST_LINE_TABLE = [
#    ('HTTP/1.1', response_deconstructor(response_ok())[0]),
#    ('200', response_deconstructor(response_ok())[1]),
#    ('OK', response_deconstructor(response_ok())[2]),
#    ('8', response_deconstructor(response_ok())[4]),
#    ('2', response_deconstructor(response_ok())[5]),
#    ('HTTP/1.1', response_deconstructor(response_error())[0]),
#    ('500', response_deconstructor(response_error())[1]),
#    ('Internal_Server_Error', response_deconstructor(response_error())[2]),
#    ('7', response_deconstructor(response_error())[4]),
#    ('2', response_deconstructor(response_error())[5])
# ]

REQUEST_GOOD = b'GET /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36\r\nAccept: */*\r\nDNT: 1\r\nReferer: http://127.0.0.1:5000/\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n'

REQUEST_BAD = [
    b'POST /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\n\r\n',
    b'GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\n\r\n',
    b'GET /favicon.ico HTTP/1.1\r\nConnection: keep-alive\r\n\r\n'
]

RESPONSE_TABLE2 = [
    b'HTTP/1.1 405 Method Not Allowed\r\n\r\nThe server supports HTTP/1.1 only.', 
    b'HTTP/1.1 505 HTTP Version Not supported\r\n\r\nThe server supports HTTP/1.1 only.',
    b'HTTP/1.1 400 Bad Request\r\n\r\nNo <host> in headers.',
    b'HTTP/1.1 200 OK\r\nDate: Fri, 19 Aug 2016 04:28:51 GMT\r\nContent-Length: 8\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nSuccess!',
    u'/favicon.ico'
]


REQUEST_TABLE1 = [
   ('GET', request_deconstructor(REQUEST_GOOD)[0]),
   ('/favicon.ico', request_deconstructor(REQUEST_GOOD)[1]),
   ('HTTP/1.1', request_deconstructor(REQUEST_GOOD)[2]),
   ('2', request_deconstructor(REQUEST_GOOD)[4]),
]


REQUEST_TABLE2 = [
    ('host', request_deconstructor(REQUEST_GOOD)[3])
]


@pytest.mark.parametrize('part, result', RESPONSE_TABLE)
def test_response_ok(part, result):
    assert part in result


# @pytest.mark.parametrize('part, result', FIRST_LINE_TABLE)
# def test_response_first_line(part, result):
#     assert part == result


@pytest.mark.parametrize('part, result', REQUEST_TABLE1)
def test_request_decon(part, result):
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_TABLE2)
def test_request_decon2(part, result):
    assert part in result


def test_parse_req_get():
    with pytest.raises(NotImplementedError):
        parse_req(b'POST /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\n\r\n')


def test_parse_req_http():
    with pytest.raises(TypeError):
        parse_req(b'GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\n\r\n')


def test_parse_req_host():
    with pytest.raises(NameError):
        parse_req(b'GET /favicon.ico HTTP/1.1\r\nConnection: keep-alive\r\n\r\n')


def test_parse_req_good():
    assert parse_req(REQUEST_GOOD) == '/favicon.ico'


def test_response_decision_generate_error_response():
    assert response_decision(REQUEST_BAD[0])[0] == RESPONSE_TABLE2[0]
    assert response_decision(REQUEST_BAD[1])[0] == RESPONSE_TABLE2[1]
    assert response_decision(REQUEST_BAD[2])[0] == RESPONSE_TABLE2[2]


def test_response_decision_generate_ok_response():
    """Compare firs 16 chars in response_ok string, therefore excluding Date and after that."""
    assert response_decision(REQUEST_GOOD)[0][:17] == RESPONSE_TABLE2[3][:17]
    assert response_decision(REQUEST_GOOD)[1][:17] == RESPONSE_TABLE2[4]
