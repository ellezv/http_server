"""Tests for our http server project."""
import pytest


REQUESTS = [
    "POST www.gremlins.com HTTP/1.1\r\nHost: me\r\n\r\n",
    "GET HTTP/1.1\r\nHost: me\r\n\r\n",
    "GET HTTP/1.1\r\nHost: me",
    "GET HTTP/1.1\r\nDate: tomorrow\r\n\r\n",
    "GET HTTP/1.1\r\nHost: \r\n\r\n",
    "GET HTTP/1.1\r\n\r\nHost: me\r\n\r\n",
    "GET HTTP/1.1\r\nHost: \r\n\r\n\r\n",
    "GET HTTP/1.1 Host: me\r\n\r\n",
]

TYPE_TABLE = [
    ["/images/Sample_Scene_Balls.jpg", "image/jpeg"],
    ["/images/sample_1.png", "image/png"],
]


def test_response_ok_end_of_header():
    """Test server response ok."""
    from server import response_ok
    assert response_ok().decode("utf8")[-4:] == "\r\n\r\n"


def test_response_ok_number_of_crlf():
    """Test server response contains the right amount of CRLF."""
    from server import response_ok
    assert response_ok().decode("utf8").count('\r\n') == 5


def test_parse_request_ok():
    """Test parse_request with valid request."""
    from server import parse_request
    req = "GET www.gremlins.com HTTP/1.1\\r\\nHost: me\\r\\n\\r\\n"
    assert parse_request(req) == 'www.gremlins.com'


@pytest.mark.parametrize("request", REQUESTS)
def test_parse_request_value_error(request):
    """Test parse_request with invalid request."""
    from server import parse_request
    with pytest.raises(ValueError):
        parse_request(request)


def test_response_error_number_of_crlf():
    """Test server response contains the right amount of CRLF."""
    from server import response_ok
    assert response_ok().decode("utf8").count('\r\n') == 5


def test_resolve_uri_raises_err():
    """Test resolve_uri will raise the correct error if file not found."""
    from server import resolve_uri
    with pytest.raises(ValueError, message="404 not found"):
        resolve_uri("badpath")


@pytest.mark.parametrize("file_path, file_type", TYPE_TABLE)
def test_resolve_uri_find_type(file_path, file_type):
    """Test resolve_uri will return the type as the second value of returned tuple."""
    from server import resolve_uri
    assert resolve_uri(file_path)[1] == file_type
