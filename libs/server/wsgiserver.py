#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple multithreaded WSGI HTTP server.
Origin from: https://www.electricmonk.nl/log/2016/02/15/multithreaded-dev-web-server-for-the-python-bottle-web-framework/
"""

from wsgiref.simple_server import make_server, WSGIServer
from SocketServer import ThreadingMixIn


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class Server:
    def __init__(self, wsgi_app, listen='127.0.0.1', port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app, ThreadingWSGIServer)

    def serve_forever(self):
        self.server.serve_forever()

