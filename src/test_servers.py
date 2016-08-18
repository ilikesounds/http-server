# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest

from server import response_ok, response_error, response_deconstructor,\
 request_deconstructor

RESPONSE_TABLE = [
   ('content-length', response_deconstructor(response_ok())[3]),
   ('content-type', response_deconstructor(response_ok())[3]),
   ('date', response_deconstructor(response_ok())[3]),
]

FIRST_LINE_TABLE = [
   ('HTTP/1.1', response_deconstructor(response_ok())[0]),
   ('200', response_deconstructor(response_ok())[1]),
   ('OK', response_deconstructor(response_ok())[2]),
   ('8', response_deconstructor(response_ok())[4]),
   ('2', response_deconstructor(response_ok())[5]),
   ('HTTP/1.1', response_deconstructor(response_error())[0]),
   ('500', response_deconstructor(response_error())[1]),
   ('Internal_Server_Error', response_deconstructor(response_error())[2]),
   ('7', response_deconstructor(response_error())[4]),
   ('2', response_deconstructor(response_error())[5])
]

REQUEST_STRING = b'GET /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36\r\nAccept: */*\r\nDNT: 1\r\nReferer: http://127.0.0.1:5000/\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n'


REQUEST_TABLE1 = [
   ('GET', request_deconstructor(REQUEST_STRING)[0]),
   ('/favicon.ico', request_deconstructor(REQUEST_STRING)[1]),
   ('HTTP/1.1', request_deconstructor(REQUEST_STRING)[2]),
   ('2', request_deconstructor(REQUEST_STRING)[4]),
]


REQUEST_TABLE2 = [
    ('host', request_deconstructor(REQUEST_STRING)[3])
]


@pytest.mark.parametrize('part, result', RESPONSE_TABLE)
def test_response_ok(part, result):
    assert part in result


@pytest.mark.parametrize('part, result', FIRST_LINE_TABLE)
def test_response_first_line(part, result):
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_TABLE1)
def test_request_decon(part, result):
    assert part == result


@pytest.mark.parametrize('part, result', REQUEST_TABLE2)
def test_request_decon2(part, result):
    assert part in result
