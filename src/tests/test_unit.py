"""Tests for our http server project."""
import pytest


REQUESTS = [
    b"POST www.gremlins.com HTTP/1.1\r\nHost: me\r\n\r\n",
    b"GET HTTP/1.1\r\nHost: me\r\n\r\n",
    b"GET HTTP/1.1\r\nHost: me",
    b"GET HTTP/1.1\r\nDate: tomorrow\r\n\r\n",
    b"GET HTTP/1.1\r\nHost: \r\n\r\n",
    b"GET HTTP/1.1\r\n\r\nHost: me\r\n\r\n",
    b"GET HTTP/1.1\r\nHost: \r\n\r\n\r\n",
    b"GET HTTP/1.1 Host: me\r\n\r\n",
]

TYPE_TABLE = [
    ["/images/Sample_Scene_Balls.jpg", "image/jpeg"],
    ["/images/sample_1.png", "image/png"],
    ["/sample.txt", "text/plain"],
    ["/make_time.py", "text/x-python"],
    ["/a_web_page.html", "text/html"],
    ["/images/style.css", "text/css"],
]

ERRORS = [
    "404 File Not Found",
    "405 Method Not Allowed",
    "400 Bad Request",
    "505 HTTP Version Not Supported"
]


def test_parse_headers_ok():
    """Test headers for request."""
    from server import parse_headers
    header_dict = parse_headers([b'Date: Dec 15, 2000',
                                 b'Host: me'])
    assert b"Host" in header_dict and b"Date" in header_dict


def test_parse_headers_error():
    """Test parse headers will raise expected error."""
    from server import parse_headers
    with pytest.raises(IndexError):
        parse_headers([b'something'])


def test_response_ok_number_of_crlf():
    """Test server response contains the right amount of CRLF."""
    from server import response_ok
    assert response_ok("text/plain", "").count(b'\r\n') == 6


def test_response_ok_content_length():
    """Test content-length header."""
    from server import response_ok, parse_headers
    headers = response_ok('text/plain', "12345678910").split(b'\r\n\r\n')[0]
    assert parse_headers(headers.split(b'\r\n')[1:])[b"Content-Length"] == b'11'


def test_parse_request_ok():
    """Test parse_request with valid request."""
    from server import parse_request
    req = b"GET www.gremlins.com HTTP/1.1\r\nHost: me\r\n\r\n"
    assert parse_request(req) == b'www.gremlins.com'


@pytest.mark.parametrize("request", REQUESTS)
def test_parse_request_value_error(request):
    """Test parse_request with invalid request."""
    from server import parse_request
    with pytest.raises(ValueError):
        parse_request(request)


@pytest.mark.parametrize("error", ERRORS)
def test_response_error_number_of_crlf(error):
    """Test server response contains the right amount of CRLF."""
    from server import response_error
    assert response_error(error).count(b'\r\n') == 4


def test_resolve_uri_raises_err():
    """Test resolve_uri will raise the correct error if file not found."""
    from server import resolve_uri
    with pytest.raises(ValueError, message="404 not found"):
        resolve_uri("badpath")


@pytest.mark.parametrize("file_path, file_type", TYPE_TABLE)
def test_resolve_uri_find_type(file_path, file_type):
    """Test resolve_uri will return the type as the second value of returned tuple."""
    from server import resolve_uri
    assert resolve_uri(file_path)[1] == file_type


def test_directory_listing():
    from server import directory_listing
    body = b'<html><body><a style="display:block;margin:10px" href="/">&#128194; root</a><a style="display:block;margin:10px" href="images/index.html">index.html</a><a style="display:block;margin:10px" href="images/JPEG_example.jpg">JPEG_example.jpg</a><a style="display:block;margin:10px" href="images/Mao">Mao&#128194;</a><a style="display:block;margin:10px" href="images/PREVIEW.jpg">PREVIEW.jpg</a><a style="display:block;margin:10px" href="images/sample_1.png">sample_1.png</a><a style="display:block;margin:10px" href="images/Sample_Scene_Balls.jpg">Sample_Scene_Balls.jpg</a><a style="display:block;margin:10px" href="images/style.css">style.css</a><a style="display:block;margin:10px" href="images/van-pic.png">van-pic.png</a></body></html>'
    assert directory_listing('/images'.encode("utf8")) == body


def test_directory_listing_2():
    from server import directory_listing
    body = '<html><body><a style="display:block;margin:10px" href="/.DocumentRevisions-V100">.DocumentRevisions-V100&#128194;</a><a style="display:block;margin:10px" href="/.DS_Store">.DS_Store</a><a style="display:block;margin:10px" href="/.file">.file</a><a style="display:block;margin:10px" href="/.fseventsd">.fseventsd&#128194;</a><a style="display:block;margin:10px" href="/.PKInstallSandboxManager-SystemSoftware">.PKInstallSandboxManager-SystemSoftware&#128194;</a><a style="display:block;margin:10px" href="/.Spotlight-V100">.Spotlight-V100&#128194;</a><a style="display:block;margin:10px" href="/.Trashes">.Trashes&#128194;</a><a style="display:block;margin:10px" href="/.vol">.vol&#128194;</a><a style="display:block;margin:10px" href="/Applications">Applications&#128194;</a><a style="display:block;margin:10px" href="/bin">bin&#128194;</a><a style="display:block;margin:10px" href="/cores">cores&#128194;</a><a style="display:block;margin:10px" href="/dev">dev&#128194;</a><a style="display:block;margin:10px" href="/etc">etc&#128194;</a><a style="display:block;margin:10px" href="/home">home&#128194;</a><a style="display:block;margin:10px" href="/installer.failurerequests">installer.failurerequests</a><a style="display:block;margin:10px" href="/Library">Library&#128194;</a><a style="display:block;margin:10px" href="/net">net&#128194;</a><a style="display:block;margin:10px" href="/Network">Network&#128194;</a><a style="display:block;margin:10px" href="/private">private&#128194;</a><a style="display:block;margin:10px" href="/sbin">sbin&#128194;</a><a style="display:block;margin:10px" href="/System">System&#128194;</a><a style="display:block;margin:10px" href="/tmp">tmp&#128194;</a><a style="display:block;margin:10px" href="/Users">Users&#128194;</a><a style="display:block;margin:10px" href="/usr">usr&#128194;</a><a style="display:block;margin:10px" href="/var">var&#128194;</a><a style="display:block;margin:10px" href="/Volumes">Volumes&#128194;</a></body></html>'
    assert directory_listing('/'.encode("utf8")) == body
