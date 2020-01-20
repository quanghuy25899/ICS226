#!/usr/bin/python3

import sys
import asyncio

BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345
path = '/home/quanghuy25899/Desktop/226Lab5/'

async def echo(reader, writer):
	data = await reader.read(BUF_SIZE)
	# read the data sent from client
	message = data.decode('utf-8')
	# decode the data received from client
	replacedMessage = message.replace('\n', '')
	# client sent a '\n' to end the sending loop
	# remove the '\n' to get the correct file name
	addr = writer.get_extra_info('peername')
	# get information about the client
	print(f"Received {replacedMessage} from {addr}")
	
	file_name = path + replacedMessage
	# get the correct location after received the file name from the client
	f = open(file_name, "rb")
	# open the file
	while True:	
		temp = f.read(BUF_SIZE)
		# read the file

		writer.write(temp) # starts to write the data to the stream
		await writer.drain() # waits until the data is written
		if temp == b'':
			f.close()
			# close the file
			writer.close()
			# stop sending
			await writer.wait_closed()
			break

async def main():
	server = await asyncio.start_server(echo, HOST, PORT)
	await server.serve_forever()

asyncio.run(main())