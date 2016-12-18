"""Set up of our client."""
import socket
import sys
import codecs


def client(request, port=5000):
    """Connect client to server, send and receive message."""
    # message += "\r\n\r\n"
    if sys.version_info[0] == 2:
        request = request.decode("utf8")
    request = codecs.escape_decode(request)[0]
    print(request)
    info = socket.getaddrinfo('127.0.0.1', port)
    stream_info = [i for i in info if i[1] == socket.SOCK_STREAM][0]
    client_ = socket.socket(*stream_info[:3])
    client_.connect((stream_info[-1]))
    client_.sendall(request)
    print('sent')
    buffer_length = 8
    response = b""

    while b"\r\n\r\n" not in response:
        response += client_.recv(buffer_length)

    end_headers = response.index(b'\r\n\r\n') + 4
    headers = response[:end_headers].decode('utf8')
    headers_dict = parse_headers(headers.split("\r\n")[1:-2])
    try:
        content_length = int(headers_dict["Content-Length"])
    except KeyError:
        pass
    else:
        body = response[end_headers:]
        while content_length > len(body):
            body += client_.recv(buffer_length)
        response = headers.encode("utf8") + body
    client_.close()
    print(response)
    return response


def parse_headers(headers_lst):
    """Parse headers into a dict."""
    headers = {}
    for header in headers_lst:
        try:
            key = header[:header.index(':')]
            value = header[header.index(':') + 2:].strip()
            headers[key] = value
        except ValueError:
            raise IndexError
    return headers

if __name__ == '__main__':  # pragma: no-cover
    try:
        client(sys.argv[1], sys.argv[2])
    except IndexError:
        client(sys.argv[1])
