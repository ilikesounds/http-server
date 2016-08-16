# -*- encoding: utf-8 *-*
'''These are tests for client.py and server.py'''
import pytest


from client import client


from server import server


TEST_TABLE = [
    ('test', 'test'),
    ('test' * 20, 'test' * 20),
    ('test' * 8, 'test' * 8),
    ('¡', '¡')
]


@pytest.mark.parametrize('message, result', TEST_TABLE)
def test_client(message, result):
    assert client(message) == result
