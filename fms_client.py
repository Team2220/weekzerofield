#!/usr/bin/python3

import socket
import time

HOST = 'localhost'
PORT = 12345

def reserve_fms(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.send(b'L')
        sock.recv(1024)
    except OSError as e:
        sock.close()
        exit(e)
    return sock

def release_fms(sock):
    sock.send(b'X')
    sock.recv(1024)
    sock.close()
    return None

# Do stuff not requiring lock
print('Initial work for 2 seconds')
time.sleep(2)

# Reserve FMS
print('Requesting FMS reservation')
fms_lock = reserve_fms(HOST, PORT)
print('FMS reserved for 15 seconds')
time.sleep(15)

# Release FMS reservation
print('Requesting FMS release')
release_fms(fms_lock)
print('FMS reservation released')

# Do stuff not requiring lock
print('Final work for 2 seconds')
time.sleep(2)
