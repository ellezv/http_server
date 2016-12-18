"""Module containg functional client tests."""
import pytest


BAD_GET_REQUESTS = [
    ["GET uri HTTP/1.1\r\nHost: me", b"Missing final carriage returns"],
    ["GET uri HTTP/1.1\r\nDate: tomorrow\r\n\r\n", b"Host header required"],
    ["GET uri HTTP/1.0\r\nHost: \r\n\r\n", b"HTTP/1.1 only"],
]


MALFORMED = [
    "GET HTTP/1.1\r\nHost: me\r\n\r\n",
    "GET uri HTTP/1.1\r\nHost: \r\n\r\n\r\n",
    "GET uri HTTP/1.1\r\n\r\nHost: me\r\n\r\n",
]


PROTO = 'HTTP/1.1'


def test_timeout():
    """Test recv loop times out properly."""
    from client import client
    assert b"Timed out" in client("GET HTTP PLEASE").split(b'\r\n')[0]


def test_client_wrong_method():
    """Test error response for non-get method."""
    from client import client
    req = "POST www.gremlins.com HTTP/1.1\r\nHost: me\r\n\r\n"
    assert client(req).split(b'\r\n')[0] == b"HTTP/1.1 405 Method Not Allowed: GET only"


@pytest.mark.parametrize("request, resp", BAD_GET_REQUESTS)
def test_client_error(request, resp):
    """Test specific request errors."""
    from client import client
    assert client(request).split(b'\r\n')[0] == b'HTTP/1.1 400 Bad Request: ' + resp


@pytest.mark.parametrize("request", MALFORMED)
def test_client_malformed(request):
    """Test general malformed requests."""
    from client import client
    assert client(request).split(b'\r\n')[0] == b'HTTP/1.1 400 Bad Request: MALFORMED'


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
