"""Module containg functional client tests."""
import pytest


BAD_GET_REQUESTS = [
    ["GET uri HTTP/1.1\\r\\nHost: me", "Missing final carriage returns"],
    ["GET uri HTTP/1.1\\r\\nDate: tomorrow\\r\\n\\r\\n", "Host header required"],
    ["GET uri HTTP/1.0\\r\\nHost: \\r\\n\\r\\n", "HTTP/1.1 only"],
]


MALFORMED = [
    "GET HTTP/1.1\\r\\nHost: me\\r\\n\\r\\n",
    "GET uri HTTP/1.1\\r\\nHost: \\r\\n\\r\\n\\r\\n",
    "GET uri HTTP/1.1 Host: me\\r\\n\\r\\n",
    "GET uri HTTP/1.1\\r\\n\\r\\nHost: me\\r\\n\\r\\n",
]


PROTO = 'HTTP/1.1'


def test_client_wrong_method():
    """Test error response for non-get method."""
    from client import client
    req = "POST www.gremlins.com HTTP/1.1\\r\\nHost: me\\r\\n\\r\\n",
    assert client(req).split('\r\n')[0] == PROTO + "405 Method Not Allowed: GET only"


@pytest.mark.parametrize("request, resp", BAD_GET_REQUESTS)
def test_client_error(request, resp):
    """Test specific request errors."""
    from client import client
    assert client(request).split('\r\n')[0] == PROTO + '400 Bad Request: ' + resp


@pytest.mark.parametrize("request", MALFORMED)
def test_client_malformed(request):
    """Test general malformed requests."""
    from client import client
    assert client(request).split('\r\n')[0] == PROTO + '400 Bad Request: MALFORMED'


def test_client_valid():
    """Test client with valid request."""
    from client import client
    from server import response_ok
    req = "GET www.gremlins.com HTTP/1.1\\r\\nHost: me\\r\\n\\r\\n"
    assert client(req)[:15] == response_ok().decode("utf8")[:15]
