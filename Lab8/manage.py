import subprocess
import sys
import asyncio

PORT = 12345

async def client():
    # get data in agents.conf file
    data = subprocess.check_output(['cat', 'agents.conf'], encoding='utf-8').rstrip('\n')
    # add data in an array separate by new line
    host = data.split('\n')
    # print(host)

    while True:
        # get user's input
        print("Input command or enter to quit: ")
        command_to_send = input()
        
        for i in range(len(host)):
            # print(host[i])
            # open connection with each agent
            reader, writer = await asyncio.open_connection(host[i], PORT)
            
            if command_to_send != '':
                # send the command to each agent
                writer.write(command_to_send.encode('utf-8') + b'\n')
                await writer.drain()
                
            else:
                writer.write(b'quit' + b'\n')

            final_result = ''
            while True:
                # wait for the agent's data
                result = await reader.readline()
                # print(result)
                if result == b'':
                    break
                final_result = final_result + result.decode('utf-8')
            # print agent's data
            print(final_result)
        
        # close connection
        writer.close()
        await writer.wait_closed()

asyncio.run(client())