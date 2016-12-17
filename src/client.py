"""Set up of our client."""
import socket
import sys
from server import parse_headers


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
    info = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(message)
    print('sent')
    buffer_length = 8
    headers = b""
    body = b""
    while '\r\n\r\n' not in headers:
        try:
            headers += client_.recv(buffer_length)
        except:
            end_headers = headers.index(b'\r\n\r\n') + 4
            headers = headers[:end_headers].decode('utf8')
            break
    headers = parse_headers(headers.split('\r\n')[:-1])
    while
    client_.close()
    print(response)
    return response


# if __name__ == '__main__':  # pragma: no-cover
#     main()
