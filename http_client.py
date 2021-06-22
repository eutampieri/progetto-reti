#!/usr/bin/env python3
"""Naive HTTPS clinet"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ssl

def https_get(host, path, port=443):
    raw_socket = socket(AF_INET, SOCK_STREAM)
    client_socket = ssl.wrap_socket(raw_socket)
    client_socket.connect((host, port))
    client_socket.send(bytes("GET %s HTTP/1.0\r\nHost: %s\r\n\r\n" %(path, host), "utf8"))
    msg = ""
    while True:
        try:
            new_part = client_socket.recv(1024).decode("utf8")
            msg = msg + new_part
            if len(new_part) == 0:
                break
        except:
            print("Error")
            break
    return msg.split("\r\n\r\n")[1]


