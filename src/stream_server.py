# -*- encoding: utf-8 *-*
# This is an http-server, with asynchronous concurrency#
import server
import gevent
import socket


if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    #stream_server = StreamServer(server.server(('127.0.0.1', 5000), gevent.socket.socket()))
    stream_server = StreamServer(('127.0.0.1', 5000), server.server)
    print('Starting stream server on port 5000')
    stream_server.serve_forever()
