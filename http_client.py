#!/usr/bin/env python3
"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ssl

def https_get(host, path, port=443):
    raw_socket = socket(AF_INET, SOCK_STREAM)
    client_socket = ssl.wrap_socket(raw_socket)
    client_socket.connect((host, port))
    print("GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" %(path, host))
    client_socket.send(bytes("GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" %(path, host), "utf8"))
    msg = client_socket.recv(1000000).decode("utf8")
    return msg


