"""Concurrency for our server.py module."""

from server import server

if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 10000), server)
    print('Starting server on port 10000')
    server.serve_forever()
