"""Set up of our client."""
# encoding: utf-8
import socket
import sys


def main():
    """CONTROLER."""
    client(sys.argv[1])


def client(message):
    """Connect client to server, send and receive message."""
    message = message + "<CRLF><CRLF>"
    if sys.version_info[0] == 2:
        message = message.decode("utf8")
    message = message.encode("utf8")
    info = socket.getaddrinfo('127.0.0.1', 5017)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message)
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
