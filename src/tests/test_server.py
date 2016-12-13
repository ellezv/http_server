"""Tests for our http server project."""


def test_response_ok():
    """Test server response ok."""
    from server import response_ok
    assert response_ok().decode("utf8")[-12:] == "<CRLF><CRLF>"


def test_number_of_crlf():
    """Test server response contains the right amount of CRLF"""
    from server import response_ok
    assert response_ok().decode("utf8").count('<CRLF>') == 5