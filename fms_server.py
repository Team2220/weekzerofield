#!/usr/bin/python3

import socket

HOST = 'localhost'
PORT = 12345
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

while (True):
    print('Waiting for new client connection')
    connection,address = sock.accept()
    print('Connection accepted')

    print('Waiting for FMS reserve request')
    connection.recv(1024)
    connection.send(b'K')
    print('FMS reserved')

    print('Waiting for FMS release request')
    connection.recv(1024)
    connection.send(b'K')
    print('FMS released')

    connection.close()
