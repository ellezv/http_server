"""Tests for our http server project."""


def test_response_ok():
    """Test server response ok."""
    from server import response_ok
    assert response_ok().decode("utf8")[-12:] == "<CRLF><CRLF>"
