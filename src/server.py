"""Module to set up the server."""
# encoding: utf-8
import socket
import email.utils


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
            request = ""
            while request[-4:] != "\r\n\r\n":
                request += conn.recv(buffer_length).decode("utf8")
            print(request)
            try:
                parse_request(request)
                conn.sendall(response_ok())
            except ValueError as e:
                conn.sendall(response_error(e.args[0]))
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


def response_error(phrase):
    """Set up and return an error status code and message."""
    headers = {
        "Content-Type": "text/plain",
        "Date": email.utils.formatdate(usegmt=True),
        "Connection": "close"
    }
    response = "HTTP/1.1 " + phrase + '\r\n'
    for key in headers:
        response += key + ': ' + headers[key] + '\r\n'
    response += '\r\n'
    return response.encode("utf8")


def parse_request(request):
    """Check the request for good stuff."""
    lst = request.split("\r\n")
    if lst[0][:3] != "GET":
        raise ValueError("405 Method Not Allowed: GET only")
    if "HTTP/1.1" not in lst[0]:
        raise ValueError("400 Bad Request: HTTP/1.1 only")
    if "Host: " not in lst[1]:
        raise ValueError("400 Bad Request: Host header required")
    else:
        return lst[0].split()[1]
