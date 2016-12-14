"""Module to set up the server."""
# encoding: utf-8
import socket
import email.utils


def server():
    """Start server to receive message and echo back."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ("127.0.0.1", 5000)
    server.bind(address)
    server.listen(1)
    buffer_length = 8
    while True:
        try:
            conn, addr = server.accept()
            request = ""
            while request[-4:] != "\r\n\r\n":
                request += conn.recv(buffer_length).decode("utf8")
            print(request)
            conn.sendall(response_ok())
            conn.close()
        except KeyboardInterrupt:
            if conn:
                conn.close()
            break
    server.close()


def response_ok():
    """Set up and return 200 response."""
    headers = {
        "Content-Type": "text/plain",
        "Date": email.utils.formatdate(usegmt=True),
        "Connection": "close"
    }
    response = "HTTP/1.1 200 OK\r\n"
    for key in headers:
        response += key + ': ' + headers[key] + '\r\n'
    response += '\r\n'
    return response.encode("utf8")


def response_error():
    """Set up and return 500 response."""
    headers = {
        "Content-Type": "text/plain",
        "Date": email.utils.formatdate(usegmt=True),
        "Connection": "close"
    }
    response = "HTTP/1.1 500 Internal Server Error\r\n"
    for key in headers:
        response += key + ': ' + headers[key] + '\r\n'
    response += '\r\n'
    return response.encode("utf8")
