# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest

from server import response_ok, response_error, response_deconstructor

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


@pytest.mark.parametrize('part, result', RESPONSE_TABLE)
def test_response_ok(part, result):
    assert part in result


@pytest.mark.parametrize('part, result', FIRST_LINE_TABLE)
def test_response_first_line(part, result):
    assert part == result
