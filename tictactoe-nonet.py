from tabnanny import check
import pygame, sys
import numpy as np

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
