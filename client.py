#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket

socks = []
for i in xrange(16):
    socks.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    sock = socks[i]
    sock.connect(('127.0.0.1', 8080))
    sock.send('Hello')

time.sleep(10000)
