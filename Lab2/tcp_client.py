#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = '10.51.11.120'
PORT = 12345

if len(sys.argv) != 2:
	print(sys.argv[0] + ' <message>')
	sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket
sock.connect((HOST, PORT)) # Initiates 3-way handshake
print('Client:', sock.getsockname()) # Source IP and source port
data = sys.argv[1].encode('utf-8') + b'\n'
sock.sendall(data) # Destination IP and port implicit due to connect call
resource = b''
def writeImage(data):
	try:
		f = open(sys.argv[1], 'wb')
		f.write(data)
		f.close()
		print('File downloaded')
	except:
		print('Error!!!')

while True:
	reply = sock.recv(BUF_SIZE) # recvfrom not needed since address is known
	#print('recv', reply)

	if len(reply) > 0:
		#print(reply)
		resource += reply
	else:
		#print(len(resource))
		break

writeImage(resource)
print('Reply:', resource)
sock.close() # Termination
