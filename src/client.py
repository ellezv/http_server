"""Set up of our client."""

import socket


def main():
    """CONTROLER."""
    import sys
    client(sys.argv[1])


def client(message):
    """Connect client to server, send and receive message."""
    message = message + "<CRLF><CRLF>"
    info = socket.getaddrinfo('127.0.0.1', 5013)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message.encode('utf8'))
    buffer_length = 8
    response = ''
    while response[-12:] != "<CRLF><CRLF>":
        response += client_.recv(buffer_length).decode('utf8')
    response = response.replace("<CRLF>", "\r\n")
    client_.close()
    print(response)
    return response


if __name__ == '__main__':  # pragma: no-cover
    main()
