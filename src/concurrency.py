"""Concurrency for our server.py module."""
import sys
import server
from gevent.server import StreamServer
from gevent.monkey import patch_all


def start_server(port=10000):
    """Start stream server."""
    patch_all()
    sserver = StreamServer(('127.0.0.1', port), connection)
    print('Starting server on port {}'.format(port))
    try:
        sserver.serve_forever()
    except KeyboardInterrupt:
        sserver.close()
        print('Server closed')


def connection(socket, address):
    """Handle new connections to stream server."""
    print('New connection from {}:{}'.format(address[0], address[1]))
    server.handle_connection(socket)


if __name__ == '__main__':
    try:
        start_server(sys.argv[1])
    except:
        start_server()
