"""Set up of our client."""

import socket


def client(message):
    """Connect client to server, send and receive message."""
    message = message + "\r\n"
    info = socket.getaddrinfo('127.0.0.1', 5011)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message.encode('utf8'))
    buffer_length = 8
    response = ''
    while response[-2:] != "\r\n":
        response += client_.recv(buffer_length).decode('utf8')
    print(response[:-2])
    client_.close()
    return response[:-2]
