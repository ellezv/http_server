"""Module to set up the server."""
import socket


def server():
    """Start server to receive message and echo back."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ("127.0.0.1", 5011)
    server.bind(address)
    server.listen(1)
    buffer_length = 8
    while True:
        try:
            conn, addr = server.accept()
            message = ""
            while message[-2:] != "\r\n":
                message += conn.recv(buffer_length).decode("utf8")
            conn.sendall(message.encode("utf8"))
            conn.close()
        except KeyboardInterrupt:
            if conn:
                conn.close()
            break
    server.close()
