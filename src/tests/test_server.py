"""Tests for our http server project."""


def test_echo_server():
    """Test server echos back message sent by client."""
    from client import client
    message = "This is the ultimate test!"
    assert client(message) == message
