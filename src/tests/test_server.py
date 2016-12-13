"""Tests for our http server project."""


def test_response_ok_end_of_header():
    """Test server response ok."""
    from server import response_ok
    assert response_ok().decode("utf8")[-12:] == "<CRLF><CRLF>"


def test_response_ok_number_of_crlf():
    """Test server response contains the right amount of CRLF."""
    from server import response_ok
    assert response_ok().decode("utf8").count('<CRLF>') == 5


def test_response_error_end_of_header():
    """Test server response ok."""
    from server import response_error
    assert response_error().decode("utf8")[-12:] == "<CRLF><CRLF>"


def test_response_error():
    """Test server response ok."""
    from server import response_error
    assert response_error().decode("utf8")[:34] == "HTTP/1.1 500 Internal Server Error"


def test_response_error_number_of_crlf():
    """Test server response contains the right amount of CRLF."""
    from server import response_ok
    assert response_ok().decode("utf8").count('<CRLF>') == 5


def test_reponse_client():
    """Test that client receives response ok."""
    from client import client
    assert client("Something")[0][:15] == "HTTP/1.1 200 OK"
