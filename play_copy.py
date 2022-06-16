# from kivy.uix.button import Button
# from kivy.uix.widget import Widget
# from kivy.uix.label import Label
# from kivy.uix.boxlayout import BoxLayout
# from kivy.app import App
# from kivy.graphics import Color, Rectangle, Line
# from functools import partial
# from kivy.clock import  Clock

from itertools import chain
from multiprocessing.connection import Client
import pygame, sys
import socket
import logging
import json
import numpy as np



row = 3
col = 3
white = (255, 255, 255)
black = (0, 0, 0)

bg_color = (28, 170, 156)

screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(bg_color)
board = np.zeros((row,col)).astype(int)


class ClientInterface:
    def __init__(self,idplayer='1'):
        # self.sreen = screen
        self.idplayer=idplayer
        self.server_address=('192.168.1.19',6666)

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

    def draw_figures(self, screen, board):
        for x in range(row):
            for y in range(col):
                if board[x][y] == 1:
                    pygame.draw.circle(screen, (255, 0, 0), (y * 150 +80, x * 150 +80), 50)
                    # print("draw 1", board[x][y], "==" , player)
                elif board[x][y] == 2:
                    pygame.draw.circle(screen, (0, 0, 255), (y* 150 +80, x * 150 +80), 50)
                    # print("draw 2", board[x][y], "==", player)

    def set_board(self, board):
        # string = []
        # for i in range(3):
        #     for j in range(3):
        #         string+=board[i][j]  

        # board = string

        print("masuk set board")
        player = self.idplayer
        command_str=f"set_board {player} {board}"
        hasil = self.send_command(command_str)
        # self.draw_figures(screen, board)
        if (hasil['status']=='OK'):
            return True
        else:
            return False

    def get_location(self):
        player = self.idplayer
        command_str=f"get_location {player}"
        hasil = self.send_command(command_str)
        print("status ",hasil['status'])
        if (hasil['status']=='OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]),int(lokasi[1]))
        else:
            return False

    def get_board(self, board):
        player = self.idplayer
        command_str=f"get_board {player} {board}"
        hasil = self.send_command(command_str)
        print("status ",hasil['status'])
        print(f" Hasil : {hasil}")
        if (hasil['status']=='OK'):
            hasil = np.reshape(hasil, (3,3))
            print(f" Hasil : {hasil}")
            return hasil
        else:
            return False

    def is_board_full(board):
        for x in range (row):
            for y in range (col):
                if board[x][y] == 0:
                    return False
    
        return True;

    def draw_vertical_win(col, screen):
        if col == 0:
            pygame.draw.line(screen, black, (80, 10), (80, 440), 10)

        elif col == 1:
            pygame.draw.line(screen, black, (80*3-10, 10), (80*3-10, 440), 10)

        elif col == 2:
            pygame.draw.line(screen, black, (80*5-20, 10), (80*5-20, 440), 10)

    def draw_horizontal_win(row, screen):
        if row == 0:
            pygame.draw.line(screen, black, (10, 80), (440, 80), 10)

        if row == 1:
            pygame.draw.line(screen, black, (10, 80*3-10), (440, 80*3-10), 10)
        
        if row == 2:
            pygame.draw.line(screen, black, (10, 80*5-20), (440, 80*5-20), 10)
        
    def draw_asc_diagonal_win(screen):
        pygame.draw.line(screen, black, (430, 20), (20, 430), 10)

    def draw_desc_diagonal_win(screen):
        pygame.draw.line(screen, black, (20, 20), (430, 430), 10)
        pass

    def check_win(player, board, self):
        # print("check win", player)
        for x in range(col):
            # print("x", x)
            # print("board[x][x]", board[0][x], board[1][x], board[2][x],"player", player)   
            if board[0][x] == player and board[1][x] == player and board[2][x] == player:
                print("draw vertical")
                self.draw_vertical_win(x, player)
                return True

        for y in range(row):
            # print("y", y)
            if board[y][0] == player and board[y][1] == player and board[y][2] == player:
                # print("draw horizontal")
                self.draw_horizontal_win(x, player)
                return True

        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            self.draw_desc_diagonal_win(player)
            
            return True

        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            self.draw_asc_diagonal_win(player)
            return True
        print("game_done")
        return False

    def mark_square(self, board, x, y, player, screen):
        print("mark", x, y, player)
        board[x][y] = player
        self.draw_figures(screen, board)
        return board


    # def available_square(row, col, board):
    #     return board[row][col] == 0

    # def button_clicked(self):
    #     event = pygame.event.get()
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #             mouseX = event.pos[0]
    #             mouseY = event.pos[1]

    #             clicked_col = int(mouseX // 150)
    #             clicked_row = int(mouseY // 150)
    #             self.available_square(clicked_row, clicked_col, self.get_board())

    #     return(clicked_col, clicked_row)


class Player:
    def __init__(self,idplayer):
        # self.screen = pygame.display.set_mode((450, 450))
        # pygame.display.set_caption('Tic Tac Toe')
        # self.screen.fill(bg_color)
        # self.current_x = 100
        # self.current_y = 100
        # self.warna_r = r
        # self.warna_g = g
        # self.warna_b = b
        self.idplayer = idplayer
        # self.widget = Widget()
        # self.buttons = None
        self.client_interface = ClientInterface(self.idplayer)
        # self.inisialiasi()
        #self.draw(self.widget,self.warna_r,self.warna_g,self.warna_b)
    def get_client_interface(self):
        return self.client_interface
    def get_idplayer(self):
        return self.idplayer
        #self.draw(self.widget, self.warna_r, self.warna_g, self.warna_b)

    # def get_widget(self):
    #     return self.widget
    # def get_buttons(self):
    #     return self.buttons
        
    # def inisialiasi(self, screen):
    #     pygame.draw.line(self.screen, white, (10, 150), (440, 150), 10)
    #     pygame.draw.line(self.screen, white, (10, 300), (440, 300), 10)
    #     pygame.draw.line(self.screen, white, (150, 10), (150, 440), 10)
    #     pygame.draw.line(self.screen, white, (300, 10), (300, 440), 10)

    def draw(self, screen, board):
        print("draw")
        global col
        global row
        # print("board", board)
        for i in range(row):
            for j in range(col):
                if board[i][j] == 1:
                    self.client_interface.mark_square(board, i, j, self.idplayer, screen)
                elif board[i][j] == 2:
                    self.client_interface.mark_square(board, i, j, self.idplayer, screen)
                else:
                    break


                
 
    def available_square(self, row, col, board):
        # print(row, col, board)
        if board[row][col] == 0:
            return True
        else:
            return False
        # return board[row][col] == 0

    # def get_button_clicked(self):
 
    def button_clicked(self, event, screen, board):
        global row
        global col
        mouseX = event.pos[0]
        mouseY = event.pos[1]

        clicked_col = int(mouseX // 150)
        clicked_row = int(mouseY // 150)
        # print ("clicked_col", clicked_col, "clicked_row", clicked_row)
        # self.sc = screen
        # print(screen)
        if self.available_square(clicked_row, clicked_col,board):
            if self.idplayer == 1:
                self.client_interface.mark_square(board, clicked_row, clicked_col, self.idplayer, screen)
                self.client_interface.set_board(board)
            if self.idplayer == 2:
                self.client_interface.mark_square(board, clicked_row, clicked_col, self.idplayer, screen)
                self.client_interface.set_board(board)
        return(clicked_col, clicked_row)
        # else:
            # p1.draw(screen, board) 
    
    

    # def inisialiasi(self):
    #     wid = self.widget
    #     btn_left = Button(text='left',on_press=partial(self.move, wid, 'left'))
    #     btn_up = Button(text='up',on_press=partial(self.move, wid, 'up'))
    #     btn_down = Button(text='down',on_press=partial(self.move, wid, 'down'))
    #     btn_right = Button(text='right',on_press=partial(self.move, wid, 'right'))

    #     self.buttons = BoxLayout(size_hint=(1, None), height=50)
    #     self.buttons.add_widget(btn_left)
    #     self.buttons.add_widget(btn_up)
    #     self.buttons.add_widget(btn_down)
    #     self.buttons.add_widget(btn_right)



class MyApp():
    players = []

    def refresh(self):
        print("refresh")
        for i in self.players:
            i.draw(self.screen)

    # def refresh(self,callback):
    #     for i in self.players:
    #         i.get_widget().canvas.clear()
    #         i.draw()

    # print(screen)

    def draw_lines(screen):
        pygame.draw.line(screen, white, (10, 150), (440, 150), 10)
        pygame.draw.line(screen, white, (10, 300), (440, 300), 10)
        pygame.draw.line(screen, white, (150, 10), (150, 440), 10)
        pygame.draw.line(screen, white, (300, 10), (300, 440), 10)

    draw_lines(screen)

    def build(self):

        p1 = Player(1)
        self.players.append(p1)
        
        p2 = Player(2)
        self.players.append(p2)

        # p1 = Player('1',1,0,0)
        # p1.set_xy(100,100)
        # widget1 = p1.get_widget()
        # buttons1 = p1.get_buttons()
        # self.players.append(p1)


        # p2 = Player('2',0,1,0)
        # p2.set_xy(100,200)
        # widget2 = p2.get_widget()
        # buttons2 = p2.get_buttons()
        # self.players.append(p2)

        # p3 = Player('3',0,0,1)
        # p3.set_xy(150,150)
        # widget3 = p3.get_widget()
        # buttons3 = p3.get_buttons()
        # self.players.append(p3)


        # root = BoxLayout(orientation='horizontal')
        # root.add_widget(widget1)
        # root.add_widget(buttons1)
        # root.add_widget(widget2)
        # root.add_widget(buttons2)
        # root.add_widget(widget3)
        # root.add_widget(buttons3)


        # Clock.schedule_interval(self.refresh,1/60)
    
    cek = 1

    while True:
        p1 = Player(1)
        p2 = Player(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif cek == 2 and event.type == pygame.MOUSEBUTTONDOWN:
                turn = p2.button_clicked(event, screen, board)
                p1.draw(screen, board)
                print("cek : ", cek)
                cek = 1
                break
                

            elif event.type == pygame.MOUSEBUTTONDOWN and cek == 1:
                print(cek)
                turn = p1.button_clicked(event, screen, board)
                cek = 2
                break

            else:
                p1.draw(screen, board)
                p2.draw(screen, board)

            

            # for i in players:
            # p1 = Player(1)
            #     p1.button_clicked(event, screen, board)
                
                

                # p2 = Player(2)
                # p2.button_clicked(event, screen, board)
                # p2.draw(screen)   
        
        # p1.draw(screen, board)


        # p2.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    MyApp()