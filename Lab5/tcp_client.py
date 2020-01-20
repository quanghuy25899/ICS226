#!/usr/bin/python3

import sys
import asyncio

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

async def client(message):
	# reader = receive
	# writer = send
	reader, writer = await asyncio.open_connection(HOST, PORT)
	# waiting for connection
	writer.write(message.encode('utf-8') + b'\n')
	# send the first argument from the command line
	data = await reader.read(BUF_SIZE)
	# receive the data from server and store to 'data'
	f = open(sys.argv[1], 'wb')

	while data != b'':
		try:
			f.write(data)
			# write the data receiving from server
			data = await reader.read(BUF_SIZE)
			# continue reading data sent from server
		except:
			print('Error!!!')
	
	f.close()
	writer.close() # reader has no close() function
	await writer.wait_closed() # wait until writer completes close()

if len(sys.argv) != 2:
	print(f'{sys.argv[0]} needs 1 argument to transmit')
	sys.exit(-1)

asyncio.run(client(sys.argv[1]))