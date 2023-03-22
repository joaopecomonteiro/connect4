import numpy as np
import pygame
import math
from copy import deepcopy
import time
import sys


BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


row_count = 6
column_count = 7


def create_board():
    board = np.zeros((row_count, column_count))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board

def open_row(board, col):
    for row in range(row_count):
        if board[row][col] == 0:
            return row
    return None
        

def is_not_full(board, col):
    return board[row_count-1][col] == 0


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(column_count-3):
        for r in range(row_count):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(column_count):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(column_count-3):
        for r in range(row_count-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(column_count-3):
        for r in range(3, row_count):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 

def score_position(board, player, opponent):

    if winning_move(board, player):
        return 512
    elif winning_move(board, opponent):
        return -512

    score = 0
    # Score horizontal positions
    for r in range(row_count):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(column_count - 3):
            # Create a horizontal window of 4
            window = row_array[c:c + 4]
            score += evaluate_window(window, player, opponent)

    # Score vertical positions
    for c in range(column_count):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(row_count - 3):
            # Create a vertical window of 4
            window = col_array[r:r + 4]
            score += evaluate_window(window, player, opponent)

    # Score positive diagonals
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            # Create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # Score negative diagonals
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            # Create a negative diagonal window of 4
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, player, opponent)

    return score


def evaluate_window(window, player, opponent):
    score = 0
    if window.count(player) == 3 and window.count(0) == 1:
        score += 50
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10
    elif window.count(player) == 1 and window.count(0) == 3:
        score += 1

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 50
    elif window.count(opponent) == 2 and window.count(0) == 2:
        score -= 10
    elif window.count(opponent) == 1 and window.count(0) == 3:
        score -= 1
    return score
    

def evaluate(board, player, opponent):
    if winning_move(board, player):
        return 512
    elif winning_move(board, opponent):
        return -512

    
    evaluation_player = 0
    evaluation_opponent = 0

    #Horizontal direita
    for c in range(column_count-3):
        for r in range(row_count):
            player_count = 0
            opponent_count = 0
            if board[r][c] != 0:
                for i in range(4):
                    if board[r][c+i] == player: 
                        player_count += 1
                    elif board[r][c+i] == opponent:
                        opponent_count += 1
                if opponent_count == 0:
                    if player_count == 1:
                        evaluation_player += 1
                    elif player_count == 2:
                        evaluation_player += 10
                    elif player_count == 3:
                        evaluation_player += 50
                if player_count == 0:
                    if opponent_count == 1:
                        evaluation_opponent += 1
                    elif opponent_count == 2:
                        evaluation_opponent += 10
                    elif opponent_count == 3:
                        evaluation_opponent += 50


    #Horizontal esquerda
    for c in range(3, column_count):
        for r in range(row_count):
            player_count = 0
            opponent_count = 0
            if board[r][c] != 0:
                for i in range(4):
                    if board[r][c-i] == player: 
                        player_count += 1
                    elif board[r][c-i] == opponent:
                        opponent_count += 1
                if opponent_count == 0:
                    if player_count == 1:
                        evaluation_player += 1
                    elif player_count == 2:
                        evaluation_player += 10
                    elif player_count == 3:
                        evaluation_player += 50
                else:
                    if opponent_count == 1:
                        evaluation_opponent += 1
                    elif opponent_count == 2:
                        evaluation_opponent += 10
                    elif opponent_count == 3:
                        evaluation_opponent += 50





    #Vertical
    for c in range(column_count):
        for r in range(row_count-3):
            player_count = 0
            opponent_count = 0
            if board[r][c] != 0:
                for i in range(4):
                    if board[r+i][c] == player: 
                        player_count += 1
                    elif board[r+i][c] == opponent:
                        opponent_count += 1
                if opponent_count == 0:
                    if player_count == 1:
                        evaluation_player += 1
                    elif player_count == 2:
                        evaluation_player += 10
                    elif player_count == 3:
                        evaluation_player += 50
                else:
                    if opponent_count == 1:
                        evaluation_opponent += 1
                    elif opponent_count == 2:
                        evaluation_opponent += 10
                    elif opponent_count == 3:
                        evaluation_opponent += 50

    #Diagonal direita cima
    for c in range(column_count-3):
        for r in range(row_count-3):
            player_count = 0
            opponent_count = 0
            if board[r][c] != 0:
                for i in range(4):
                    if board[r+i][c+i] == player: 
                        player_count += 1
                    elif board[r+i][c+i] == opponent:
                        opponent_count += 1
                if opponent_count == 0:
                    if player_count == 1:
                        evaluation_player += 1
                    elif player_count == 2:
                        evaluation_player += 10
                    elif player_count == 3:
                        evaluation_player += 50
                else:
                    if opponent_count == 1:
                        evaluation_opponent += 1
                    elif opponent_count == 2:
                        evaluation_opponent += 10
                    elif opponent_count == 3:
                        evaluation_opponent += 50

    #Diagonal esquerda cima
    for c in range(3, column_count):
        for r in range(row_count-3):
            player_count = 0
            opponent_count = 0
            if board[r][c] != 0:
                for i in range(4):
                    if board[r+i][c-i] == player: 
                        player_count += 1
                    elif board[r+i][c-i] == opponent:
                        opponent_count += 1
                if opponent_count == 0:
                    if player_count == 1:
                        evaluation_player += 1
                    elif player_count == 2:
                        evaluation_player += 10
                    elif player_count == 3:
                        evaluation_player += 50
                else:
                    if opponent_count == 1:
                        evaluation_opponent += 1
                    elif opponent_count == 2:
                        evaluation_opponent += 10
                    elif opponent_count == 3:
                        evaluation_opponent += 50

    return evaluation_player, evaluation_opponent





def evaluate1(board, player, opponent):
    if winning_move(board, player):
        return 512
    elif winning_move(board, opponent):
        return -512

    else:
        evaluation_player = 0
        evaluation_opponent = 0

        #Player horizontal direita
        for c in range(column_count-3):
            for r in range(row_count):
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r][c+1] == 0 and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_player += 1

        #Player vertical cima
        for c in range(column_count):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c] == 0 and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_player += 1

        #Player diagonal direita cima
        for c in range(column_count-3):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c+1] == 0 and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_player += 1

        #Player diagonal direita baixo
        for c in range(column_count-3):
            for r in range(3, row_count):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r-1][c+1] == 0 and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_player += 1

        #Player diagonal esquerda cima
        for c in range(3, column_count):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c-1] == player and board[r+2][c-2] == player and board[r+3][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c-1] == player and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c-1] == 0 and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_player += 1

        #Player diagonal esquerda baixo
        for c in range(3, column_count):
            for r in range(3, row_count):
                if board[r][c] == player and board[r-1][c-1] == player and board[r-2][c-2] == player and board[r-3][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r-1][c-1] == player and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r-1][c-1] == 0 and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_player += 1

        #Player horizontal esquerda
        for c in range(3, column_count):
            for r in range(row_count):
                if board[r][c] == player and board[r][c-1] == player and board[r][c-2] == player and board[r][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r][c-1] == player and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r][c-1] == 0 and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_player += 1



        #Player horizontal direita
        for c in range(column_count-3):
            for r in range(row_count):
                if board[r][c] == opponent and board[r][c+1] == opponent and board[r][c+2] == opponent and board[r][c+3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r][c+1] == opponent and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r][c+1] == 0 and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_opponent += 1

        #Player vertical cima
        for c in range(column_count):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c] == opponent and board[r+2][c] == opponent and board[r+3][c] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r+1][c] == opponent and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r+1][c] == 0 and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_opponent += 1

        #Player diagonal direita cima
        for c in range(column_count-3):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c+1] == opponent and board[r+2][c+2] == opponent and board[r+3][c+3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r+1][c+1] == opponent and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r+1][c+1] == 0 and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_opponent += 1

        #Player diagonal direita baixo
        for c in range(column_count-3):
            for r in range(3, row_count):
                if board[r][c] == opponent and board[r-1][c+1] == opponent and board[r-2][c+2] == opponent and board[r-3][c+3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r-1][c+1] == opponent and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r-1][c+1] == 0 and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_opponent += 1

        #Player diagonal esquerda cima
        for c in range(3, column_count):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c-1] == opponent and board[r+2][c-2] == opponent and board[r+3][c-3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r+1][c-1] == opponent and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r+1][c-1] == 0 and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_opponent += 1

        #Player diagonal esquerda baixo
        for c in range(3, column_count):
            for r in range(3, row_count):
                if board[r][c] == opponent and board[r-1][c-1] == opponent and board[r-2][c-2] == opponent and board[r-3][c-3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r-1][c-1] == opponent and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r-1][c-1] == 0 and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_opponent += 1

        #Player horizontal esquerda
        for c in range(3, column_count):
            for r in range(row_count):
                if board[r][c] == opponent and board[r][c-1] == opponent and board[r][c-2] == opponent and board[r][c-3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r][c-1] == opponent and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r][c-1] == 0 and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_opponent += 1

        return evaluation_player, evaluation_opponent

def is_board_full(board):
    for c in range(column_count):
        for r in range(row_count):
            if board[r][c] == 0:
                return False
    return True

def get_available_moves(board, piece):
    children = []
    for c in range(column_count):
        new = deepcopy(board)
        r = open_row(board, c)
        if r is not None:
            new = drop_piece(new, r, c, piece)
            children.append(new)
    return children

def greedy(board, player, opponent):
    valid_moves = get_available_moves(board, player)
    best_score = -math.inf
    best_move = None
    for move in valid_moves:
        score = score_position(move, player, opponent)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def is_terminal_node(board):
	return winning_move(board, 1) or winning_move(board, 2) or is_board_full(board)


def minimax(board, depth, max_player, player, opponent):
    # print("0okokok")
    if depth == 0 or is_terminal_node(board):
        print("??")
        return score_position(board, player, opponent), board
    # print("adwwadwawwdadwg,g,g,g,g")
    if max_player:
        max_eval = -math.inf
        best_move = None
        moves = get_available_moves(board, player)
        # print("odawodkwao")
        for move in moves:
            # print(np.flip(move), 0)

            evaluation = minimax(move, depth-1, False, opponent, player)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
        print(np.flip(best_move, 0))
        return max_eval, best_move
    else:
        # print("dawdwa")
        min_eval = math.inf
        best_move = None
        for move in get_available_moves(board, player):
            # print(np.flip(move), 0)

            evaluation = minimax(move, depth-1, True, opponent, player)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
        print(np.flip(best_move, 0))
        
        return min_eval, best_move
    





def draw_board(board):
	for c in range(column_count):
		for r in range(row_count):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(column_count):
		for r in range(row_count):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()





def print_board(board):
    temp_board = np.flip(board, 0)
    for i in range(row_count):
        b = ""
        for j in range(column_count):
            b += str(int(temp_board[i][j])) + '\t'
        print(b)
    print("-------------------------------------------------")
    b = ""
    for j in range(column_count):
        b += str(j+1) + '\t'
    print(b)
    print("\n\n")



player_1 = int(input("Jogador 1(1: Humano,2: Greedy, 3:  Minimax, 4: Random Moves): "))
player_2 = int(input("Jogador 2(1: Humano,2: Greedy, 3:  Minimax, 4: Random Moves): "))
board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 75

width = column_count * SQUARESIZE
height = (column_count) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 50)








while not game_over:

    if turn==0:
        player_piece = 1
        opponent_piece = 2
        if player_1 == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_not_full(board, col):
                        row = open_row(board, col)
                        board = drop_piece(board, row, col, player_piece)
                        if len(get_available_moves(board, player_piece)) == 0:
                            print(f"Empate!!")
                            label = myfont.render(f"Empate!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        if winning_move(board, player_piece):
                            print(f"Jogador {player_piece} ganhou!!")
                            label = myfont.render(f"Player {player_piece} wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2
                    else:
                        print("A coluna escolhida está cheia")
        elif player_1 == 2:
            time.sleep(1)
            board = greedy(board, player_piece, opponent_piece)
            if len(get_available_moves(board, player_piece)) == 0:
                print(f"Empate!!")
                label = myfont.render(f"Empate!!", 1, BLUE)
                screen.blit(label, (40,10))
                    # pygame.display.update()
                game_over = True
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                label = myfont.render(f"Player {player_piece} wins!!", 1, RED)
                screen.blit(label, (40,10))
                game_over = True
            draw_board(board)
            print_board(board)
            turn += 1
            turn = turn % 2
        
    else:
        player_piece = 2
        opponent_piece = 1
        if player_2 == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_not_full(board, col):
                        row = open_row(board, col)
                        board = drop_piece(board, row, col, player_piece)
                        if len(get_available_moves(board, player_piece)) == 0:
                            print(f"Empate!!")
                            label = myfont.render(f"Empate!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        if winning_move(board, player_piece):
                            print(f"Jogador {player_piece} ganhou!!")
                            label = myfont.render(f"Player {player_piece} wins!!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True
                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2
                    else:
                        print("A coluna escolhida está cheia")
        elif player_2 == 2:
            time.sleep(1)
            board = greedy(board, player_piece, opponent_piece)
            if len(get_available_moves(board, player_piece)) == 0:
                print(f"Empate!!")
                label = myfont.render(f"Empate!!", 1, BLUE)
                screen.blit(label, (40,10))
                            # pygame.display.update()
                game_over = True
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                label = myfont.render(f"Player {player_piece} wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2
        elif player_2 == 3:
            time.sleep(1)
            board = minimax(board, 3, True, player_piece, opponent_piece)[1]
            if len(get_available_moves(board, player_piece)) == 0:
                print(f"Empate!!")
                label = myfont.render(f"Empate!!", 1, BLUE)
                screen.blit(label, (40,10))
                            # pygame.display.update()
                game_over = True
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                label = myfont.render(f"Player {player_piece} wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2




    if game_over:
        pygame.time.wait(3000)









