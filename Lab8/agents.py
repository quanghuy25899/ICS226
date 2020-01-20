import sys
import asyncio
import subprocess

BUF_SIZE = 1024
PORT = 12345

async def echo(reader, writer):
    f = open("commands.conf", 'r')

    # wait for agents send the command
    command_from_client = await reader.readline()
    # decoded the command
    decoded_command = command_from_client.decode('utf-8').rstrip('\n')
    print(decoded_command)

    while(True):
        stop = False
        # read command to run from commands.conf file
        command_to_run = f.readline()
        print(command_to_run)

        if decoded_command in command_to_run:
            # strip all \n character
            result = command_to_run.rstrip('\n')
            # put the data in an array separate with tab
            result1 = result.split('\t')
            print(result1)
            break
        elif decoded_command == "quit":
            stop = True
            break

    # print(result1)
    # print(len(result1))
    if stop == False:
        if len(result1) > 3:
            # get the data in result1 array to run subprocess command
            result_to_send = subprocess.check_output([result1[1], result1[2], result1[3]])
            print(result_to_send)
            # send data back to agents
            writer.write(result_to_send)
            await writer.drain()

        else:
            # get the data in result1 array to run subprocess command
            result_to_send = subprocess.check_output([result1[1], result1[2]])
            print(result_to_send)
            # send data back to agents
            writer.write(result_to_send)
            await writer.drain()
    
    # close file
    f.close()
    # close connection
    writer.close()
    await writer.wait_closed()
        
async def main():
    # start server
    server = await asyncio.start_server(echo, "::", PORT)
    await server.serve_forever()
    
asyncio.run(main())