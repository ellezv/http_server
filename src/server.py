"""Module to set up the server."""
import socket


def server():
    """Start server to receive message and echo back."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ("127.0.0.1", 5042)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    buffer_length = 8
    message = ""
    while message[-3:] != "END":
        message += conn.recv(buffer_length).decode("utf8")
    conn.sendall(message.encode("utf8"))
    conn.close()
    server.close()
