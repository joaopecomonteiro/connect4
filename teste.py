import numpy as np
#import pygame
import math
from copy import deepcopy



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
 


def gen_children(board, piece):
    children = []
    for c in range(column_count):
        new = deepcopy(board)
        r = open_row(board, c)
        new = drop_piece(new, r, c, piece)
        children.append(new)
    return children


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
    print()

board = create_board()
drop_piece(board, 0, 0, 1)
print_board(board)
children = gen_children(board, 2)
for child in children:
    print("okok")
    print_board(child)




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
