# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest


# from client import client
from server import response_ok, response_error, server


# TEST_TABLE = [
#     ('test', 'test'),
#     ('test' * 20, 'test' * 20),
#     ('test' * 8, 'test' * 8),
#     ('¡', u'¡')
# ]


# @pytest.mark.parametrize('message, result', TEST_TABLE)
# def test_client(message, result):
#     assert client(message) == result


def test_response_ok_type():
    type_response = type(response_ok())
    type_to_compare = type(b'abc')
    assert type_response == type_to_compare


def test_contents_response_ok():
    response = response_ok().split()
    assert response[0] == b'HTTP/1.1' and response[1] == b'200' and \
        response[2] == b'OK' and response[3] == b'Success'


def test_response_error_type():
    type_response = type(response_error())
    type_to_compare = type(b'abc')
    assert type_response == type_to_compare


def test_contents_response_error():
    response = response_error().split()
    assert response[0] == b'HTTP/1.1' and response[1] == b'500' and \
        response[2] == b'Internal_Server_Error'
