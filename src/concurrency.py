"""Concurrency for our server.py module."""
import server


def connection(socket, address):
    """Handle new connections to stream server."""
    print('New connection from {}:{}'.format(address[0], address[1]))
    server.handle_connection(socket)

if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    cserver = StreamServer(('127.0.0.1', 10000), connection)
    print('Starting server on port 10000')
    cserver.serve_forever()
