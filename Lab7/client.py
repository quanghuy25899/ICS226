#!/usr/bin/python3

import requests
import curses
import sys
import json

def main(stdscr):
    while True:
        board = requests.get('https://evening-castle-11801.herokuapp.com/game/')
        player = requests.get('https://evening-castle-11801.herokuapp.com/game/player/1/')
        # print(board.status_code)
        # print(board.text)
        # print(player.status_code)
        # print(player.text)

        for i in range(len(board.json())):
            for j in range(len(board.json()[0])):
                stdscr.addstr(i, j, str(board.json()[i][j]))
        stdscr.refresh()

        move = stdscr.getch()   # down(258), up(259), left(260), right(261)
        # get the player's row position
        player_row = player.json()['row']
        # get the player's col position
        player_col = player.json()['col']
        
        player_loc = []
        # add player position to array
        player_loc.append(player_row)
        player_loc.append(player_col)

        # check move
        if ((move == 261) and (player_loc[1] == len(board.json()[0]))): # right: block out of range
            continue
        elif (move == 260) and (player_loc[1] == 0): # left: block out of range
            continue
        elif (move == 259) and (player_loc[0] == 0): # up: block out of range
            continue
        elif (move == 258) and (player_loc[0] == len(board.json())): # down: block out of range
            continue
        else:
            # move the player
            if move == 261: # right(261)
                player_loc[1] += 1  # col change if needs
            elif move == 260: # left(260) 
                player_loc[1] -= 1   # col change if need
            elif move == 259: # up(259) 
                player_loc[0] -= 1   # row change if need 
            elif move == 258: # down(258) 
                player_loc[0] += 1   # row change if need
            
            # update move
            client = requests.session()
            update = 'https://evening-castle-11801.herokuapp.com/game/player/1/update/'
            client.get(update)
            if 'csrftoken' in client.cookies:
                elements = {'row': player_loc[0], 'col': player_loc[1], 'csrfmiddlewaretoken': client.cookies['csrftoken']}
                post = client.post(update, data = elements, headers = {'Referer': update})

curses.wrapper(main)