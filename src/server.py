"""Module to set up the server."""
import socket
import email.utils
import os
import mimetypes


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
            request = b""
            response = b""
            conn.settimeout(1.5)
            try:
                while request[-4:] != b'\r\n\r\n':
                    request += conn.recv(buffer_length)
                print('received')
                uri = parse_request(request)
                body, file_type = resolve_uri(uri.decode("utf8"))
                response = response_ok(file_type, body)
            except ValueError as e:
                response = response_error(e.args[0])
            except socket.timeout:
                response = response_error("400 Bad Request: Timed out.")
            conn.sendall(response)
            conn.close()
        except KeyboardInterrupt:
            try:
                conn.close()
            except:
                pass
            break
    server.close()


def response_ok(file_type, body):
    """Set up and return 200 response."""
    headers = {
        "Date": email.utils.formatdate(usegmt=True),
        "Connection": "close",
        "Content-Length": str(len(body))
    }
    if file_type:
        headers["Content-Type"] = file_type
    response = "HTTP/1.1 200 OK\r\n"
    for key in headers.keys():
        response += key + ': ' + headers[key] + '\r\n'
    response += '\r\n'
    if file_type and file_type[:5] == 'image' and file_type[6:] != 'x-icon':
        response = b''.join([response.encode('utf8'), body])
    else:
        response += body
        response = response.encode('utf8')
    return response


def response_error(phrase):
    """Set up and return an error status code and message."""
    headers = {
        "Date": email.utils.formatdate(usegmt=True),
        "Connection": "close"
    }
    response = "HTTP/1.1 " + phrase + '\r\n'
    for key in headers:
        response += key + ': ' + headers[key] + '\r\n'
    response += '\r\n'
    return response.encode('utf8')


def parse_request(request):
    """Check the request for good stuff."""
    lst = request.split(b"\r\n")
    try:
        if lst[0].split()[0] != b"GET":
            raise ValueError("405 Method Not Allowed: GET only")
        if lst[0].split()[2] != b"HTTP/1.1":
            if b"HTTP/1.1" in lst[0]:
                raise IndexError
            raise ValueError("505 HTTP Version Not Supported: HTTP/1.1 only")
        headers = parse_headers(lst[1:-2])
        if b'Host' not in headers:
            raise ValueError("400 Bad Request: Host header required")
        if request[-4:] != b'\r\n\r\n':
            raise ValueError("400 Bad Request: Missing final carriage returns")
    except ValueError as e:
        raise e
    except IndexError as e:
        raise ValueError("400 Bad Request: MALFORMED")
    return lst[0].split()[1]


def parse_headers(headers_lst):
    """Parse headers into a dict."""
    headers = {}
    for header in headers_lst:
        try:
            key = header[:header.index(b':')]
            value = header[header.index(b':') + 2:].strip()
            headers[key] = value
        except ValueError:
            raise IndexError
    return headers


def resolve_uri(uri):
    """Try to return response body."""
    path = '/'.join([os.path.dirname(os.path.realpath(__file__)),
                     'webroot',
                     uri])
    body = ""
    try:
        if os.path.isdir(path):
            body = directory_listing(path)
        elif os.path.isfile(path):
            ftype = mimetypes.guess_type(uri)[0]
            r = 'r'
            if ftype[:5] == 'image':
                r = 'rb'
                body = b''
            with open(path, r) as f:
                body = f.read()
        else:
            raise Exception
        return body, mimetypes.guess_type(uri)[0]
    except Exception:
        raise ValueError("404 File Not Found")


def directory_listing(path):
    """Create directory listing."""
    res = ''
    for f in os.listdir(path):
        res += '<a style="display:block" href="' + '/'.join([path.split('/')[-1], f]) + '">' + f + '</a>\r\n'
    return "<html><body>{}</body></html>".format(res)


if __name__ == '__main__':
    server()
