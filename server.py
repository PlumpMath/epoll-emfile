#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno, socket, select, logging

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)
sock.setblocking(0)

epoll = select.epoll()
epoll.register(sock.fileno(), select.EPOLLIN)

try:
    connections = {}; packets = {}
    while True:
        events = epoll.poll()
        for fileno, event in events:
            if fileno == sock.fileno():
                try:
                    connection, address = sock.accept()
                    connection.setblocking(0)
                    epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLOUT)
                    connections[connection.fileno()] = connection
                    packets[connection.fileno()] = b''
                except socket.error, ex:
                    if ex.errno != errno.EMFILE:
                        raise
                    logging.error(ex.strerror)
            elif event & select.EPOLLIN:
                packet = connections[fileno].recv(1024)
                if len(packet) == 0:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
                else:
                    packets[fileno] += packet
            elif event & select.EPOLLOUT:
                if len(packets[fileno]) > 0:
                     byteswritten = connections[fileno].send(packets[fileno])
                     packets[fileno] = packets[fileno][byteswritten:]
finally:
    epoll.unregister(sock.fileno())
    epoll.close()
    sock.close()
