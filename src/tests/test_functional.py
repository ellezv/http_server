"""Module containg functional client tests."""
import pytest


BAD_REQUEST = b'400 Bad Request: '
BAD_VERSION = b'505 HTTP Version Not Supported: '
BAD_METHOD = b'405 Method Not Allowed: '


BAD_GET_REQUESTS = [
    ["GET uri HTTP/1.1\r\nHost: me", BAD_REQUEST, b"Timed out."],
    ["GET uri HTTP/1.1\r\nDate: tomorrow\r\n\r\n", BAD_REQUEST, b"Host header required"],
    ["GET uri HTTP/1.0\r\nHost: \r\n\r\n", BAD_VERSION, b"HTTP/1.1 only"],
    ["GET HTTP/1.1\r\nHost: me\r\n\r\n", BAD_REQUEST, b"MALFORMED"],
    ["GET uri HTTP/1.1\r\nHost: \r\n\r\n\r\n", BAD_REQUEST, b"MALFORMED"],
    ["GET uri HTTP/1.1\r\n\r\nHost: me\r\n\r\n", BAD_REQUEST, b"MALFORMED"],
    ["POST uri HTTP/1.1\r\nHost: me\r\n\r\n", BAD_METHOD, b"GET only"],
    ["PUT uri HTTP/1.1\r\nHost: me\r\n\r\n", BAD_METHOD, b"GET only"],
    ["get uri HTTP/1.1\r\nHost: me\r\n\r\n", BAD_METHOD, b"GET only"],
]


def test_timeout():
    """Test recv loop times out properly."""
    from client import client
    assert b"Timed out" in client("GET HTTP PLEASE").split(b'\r\n')[0]


@pytest.mark.parametrize("req, reason, resp", BAD_GET_REQUESTS)
def test_client_error(req, reason, resp):
    """Test specific request errors."""
    from client import client
    assert client(req).split(b'\r\n')[0] == b'HTTP/1.1 ' + reason + resp


def test_client_valid():
    """Test client with valid request."""
    body = '''
        This is a very simple text file.
        Just to show that we can serve it up.
        It is three lines long.
    '''
    from client import client
    from server import response_ok
    req = "GET sample.txt HTTP/1.1\r\nHost: me\r\n\r\n"
    assert client(req)[:15] == response_ok("text/plain", body)[:15]


def test_parse_headers_client_err():
    """Test parse headers raises expected error."""
    from client import parse_headers
    with pytest.raises(IndexError):
        parse_headers("something")
