#!/usr/bin/python3

import socket
import sys
import os

BUF_SIZE = 1
HOST = ''
PORT = 12345
path = '/home/pi/Desktop/Lab02/'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # More on this later
sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
sock.listen(1) # Enable server to receive 1 connection at a time
print('Server:', sock.getsockname()) # Source IP and port
while True:
	sc, sockname = sock.accept() # Wait until a connection is established
	print('Client:', sc.getpeername()) # Destination IP and port
	resource = b''
	while True:
		data = sc.recv(BUF_SIZE)
		if data != b'\n':
			resource += data
		else:
			break
	# print(resource)

	file_name = path + resource.decode('utf-8')
	f = open(file_name, "rb")
	temp = f.read()
	#print(len(temp))
	f.close()

	sc.sendall(temp) # Destination IP and port implicit due to accept call
	file_name = ''
	sc.close() # Termination
