from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from functools import partial
from kivy.clock import  Clock
import pygame, sys
import numpy as np
import socket
import logging
import json

class ClientInterface:
    def __init__(self,idplayer='1'):
        self.idplayer=idplayer
        self.server_address=('192.168.1.46',5005)

    def send_command(self,command_str=""):
        global server_address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        logging.warning(f"connecting to {self.server_address}")
        try:
            logging.warning(f"sending message ")
            sock.sendall(command_str.encode())
            # Look for the response, waiting until socket is done (no more data)
            data_received="" #empty string
            while True:
                #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
                data = sock.recv(16)
                if data:
                    #data is not empty, concat with previous content
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        break
                else:
                    # no more data, stop the process by break
                    break
            # at this point, data_received (string) will contain all data coming from the socket
            # to be able to use the data_received as a dict, need to load it using json.loads()
            hasil = json.loads(data_received)
            logging.warning("data received from server:")
            return hasil
        except:
            logging.warning("error during data receiving")
            return False

    def set_location(self,x=100,y=100):
        player = self.idplayer
        command_str=f"set_location {player} {x} {y}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_location(self):
        player = self.idplayer
        command_str=f"get_location {player}"
        hasil = self.send_command(command_str)
        if (hasil['status']=='OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]),int(lokasi[1]))
        else:
            return False




pygame.init()

screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Tic Tac Toe')

# RGB White
white = (255, 255, 255)
# Background color
black = (0, 0, 0)
bg_color = (28, 170, 156)
screen.fill(bg_color)
row = 3
col = 3
player = 1

#drawline
# pygame.draw.line(screen, white, (10, 10), (100, 100), 10)

# board
board = np.zeros((3, 3)).astype(int)

def draw_lines():
    pygame.draw.line(screen, white, (10, 150), (440, 150), 10)
    pygame.draw.line(screen, white, (10, 300), (440, 300), 10)
    pygame.draw.line(screen, white, (150, 10), (150, 440), 10)
    pygame.draw.line(screen, white, (300, 10), (300, 440), 10)
draw_lines()

def draw_figures(player):
    for x in range(row):
        for y in range(col):
            if board[x][y] == 1:
                pygame.draw.circle(screen, (255, 0, 0), (y * 150 +80, x * 150 +80), 50)
                # print("draw 1", board[x][y], "==" , player)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, (0, 0, 255), (y* 150 +80, x * 150 +80), 50)
                # print("draw 2", board[x][y], "==", player)

def mark_square(row, col, player):
    board[row][col] = int(player)
    draw_figures(player)

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for x in range (row):
        for y in range (col):
            if board[x][y] == 0:
                return False
    
    return True;

def restart():
    pass

def check_win(player):
    print("check win", player)
    for x in range(col):
        # print("x", x)
        print("board[x][x]", board[0][x], board[1][x], board[2][x],"player", player)   
        if board[0][x] == player and board[1][x] == player and board[2][x] == player:
            print("draw vertical")
            draw_vertical_win(x, player)
            return True

    for y in range(row):
        print("y", y)
        if board[y][0] == player and board[y][1] == player and board[y][2] == player:
            print("draw horizontal")
            draw_horizontal_win(x, player)
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal_win(player)
        
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        draw_asc_diagonal_win(player)
        return True
    print("game_done")
    return False


def draw_vertical_win(col, player):
    if col == 0:
        pygame.draw.line(screen, black, (80, 10), (80, 440), 10)

    elif col == 1:
        pygame.draw.line(screen, black, (80*3-10, 10), (80*3-10, 440), 10)

    elif col == 2:
        pygame.draw.line(screen, black, (80*5-20, 10), (80*5-20, 440), 10)


def draw_horizontal_win(row, player):
    if row == 0:
        pygame.draw.line(screen, black, (10, 80), (440, 80), 10)

    if row == 1:
        pygame.draw.line(screen, black, (10, 80*3-10), (440, 80*3-10), 10)
    
    if row == 2:
        pygame.draw.line(screen, black, (10, 80*5-20), (440, 80*5-20), 10)
    

def draw_asc_diagonal_win(player):
    pygame.draw.line(screen, black, (430, 20), (20, 430), 10)

def draw_desc_diagonal_win(player):
    pygame.draw.line(screen, black, (20, 20), (430, 430), 10)
    pass

game_over = False

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_col = int(mouseX // 150)
                clicked_row = int(mouseY // 150)

                # send data to server should be here
                if available_square(clicked_row, clicked_col):
                    if player == 1:
                        mark_square(clicked_row, clicked_col, player)
                        game_over = check_win(player)
                        player = 2
                        break
                        
                    if player == 2:
                        mark_square(clicked_row, clicked_col, player)
                        game_over = check_win(player)
                        player = 1
                        break
        if game_over == True or is_board_full() == True:
            restart()
    pygame.display.update()
