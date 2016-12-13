"""Set up of our client."""

import socket


def main():
    """CONTROLER."""
    import sys
    client(sys.argv[1])


def client(message):
    """Connect client to server, send and receive message."""
    message = message + "END"
    infos = socket.getaddrinfo('127.0.0.1', 5054)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message.encode('utf8'))
    buffer_length = 8
    response = ''
    while response[-3:] != "END":
        response += client_.recv(buffer_length).decode('utf8')
    print(response[:-3])
    client_.close()
    return response[:-3]

if __name__ == '__main__':  # pragma: no-cover
    main()
