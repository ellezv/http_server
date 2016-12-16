"""Set up of our client."""
import socket
import sys


def main():
    """CONTROLER."""
    client(sys.argv[1])


def client(message):
    """Connect client to server, send and receive message."""
    # message += "\r\n\r\n"
    if sys.version_info[0] == 2:
        message = message.decode("utf8")
    message = message.encode("utf8")
    print(message)
    info = socket.getaddrinfo('127.0.0.1', 5018)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message)
    print('sent')
    buffer_length = 8
    response = ''
    while response[-4:] != "\r\n\r\n":
        response += client_.recv(buffer_length).decode('utf8')
    client_.close()
    print(response)
    return response


if __name__ == '__main__':  # pragma: no-cover
    main()
