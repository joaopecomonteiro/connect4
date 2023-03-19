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
 

def evaluate(board, player, opponent):
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
                
        #opponent horizontal direita
        for c in range(column_count-3):
            for r in range(row_count):
                if board[r][c] == opponent and board[r][c+1] == opponent and board[r][c+2] == opponent and board[r][c+3] == 0:
                    evaluation_opponent -= 50
                if board[r][c] == opponent and board[r][c+1] == opponent and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_opponent -= 10
                if board[r][c] == opponent and board[r][c+1] == 0 and board[r][c+2] == 0 and board[r][c+3] == 0:
                    evaluation_opponent -= 1

        #Player vertical cima
        for c in range(column_count):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c] == 0 and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_player += 1

        #opponent vertical cima
        for c in range(column_count):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c] == opponent and board[r+2][c] == opponent and board[r+3][c] == 0:
                    evaluation_opponent -= 50
                if board[r][c] == opponent and board[r+1][c] == opponent and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_opponent -= 10
                if board[r][c] == opponent and board[r+1][c] == 0 and board[r+2][c] == 0 and board[r+3][c] == 0:
                    evaluation_opponent -= 1

        #Player diagonal direita cima
        for c in range(column_count-3):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c+1] == 0 and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_player += 1

        #opponent diagonal direita cima
        for c in range(column_count-3):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c+1] == opponent and board[r+2][c+2] == opponent and board[r+3][c+3] == 0:
                    evaluation_opponent -= 50
                if board[r][c] == opponent and board[r+1][c+1] == opponent and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_opponent -= 10
                if board[r][c] == opponent and board[r+1][c+1] == 0 and board[r+2][c+2] == 0 and board[r+3][c+3] == 0:
                    evaluation_opponent -= 1

        #Player diagonal direita baixo
        for c in range(column_count-3):
            for r in range(3, row_count):
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r-1][c+1] == 0 and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_player += 1

        #opponent diagonal direita baixo
        for c in range(column_count-3):
            for r in range(3, row_count):
                if board[r][c] == opponent and board[r-1][c+1] == opponent and board[r-2][c+2] == opponent and board[r-3][c+3] == 0:
                    evaluation_opponent -= 50
                if board[r][c] == opponent and board[r-1][c+1] == opponent and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_opponent -= 10
                if board[r][c] == opponent and board[r-1][c+1] == 0 and board[r-2][c+2] == 0 and board[r-3][c+3] == 0:
                    evaluation_opponent -= 1

        #Player diagonal esquerda cima
        for c in range(3, column_count):
            for r in range(row_count-3):
                if board[r][c] == player and board[r+1][c-1] == player and board[r+2][c-2] == player and board[r+3][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r+1][c-1] == player and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r+1][c-1] == 0 and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_player += 1

        #oponnent diagonal esquerda cima
        for c in range(3, column_count):
            for r in range(row_count-3):
                if board[r][c] == opponent and board[r+1][c-1] == opponent and board[r+2][c-2] == opponent and board[r+3][c-3] == 0:
                    evaluation_opponent -= 50
                if board[r][c] == opponent and board[r+1][c-1] == opponent and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_opponent -= 10
                if board[r][c] == opponent and board[r+1][c-1] == 0 and board[r+2][c-2] == 0 and board[r+3][c-3] == 0:
                    evaluation_opponent -= 1
        
        #Player diagonal esquerda baixo
        for c in range(3, column_count):
            for r in range(3, row_count):
                if board[r][c] == player and board[r-1][c-1] == player and board[r-2][c-2] == player and board[r-3][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r-1][c-1] == player and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r-1][c-1] == 0 and board[r-2][c-2] == 0 and board[r-3][c-3] == 0:
                    evaluation_player += 1

        #opponent diagonal esquerda baixo
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
                if board[r][c] == player and board[r][c-1] == player and board[r][c-2] == player and board[r][c-3] == 0:
                    evaluation_player += 50
                if board[r][c] == player and board[r][c-1] == player and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_player += 10
                if board[r][c] == player and board[r][c-1] == 0 and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_player += 1
        
        #opponent horizontal esquerda
        for c in range(3, column_count):
            for r in range(row_count):
                if board[r][c] == opponent and board[r][c-1] == opponent and board[r][c-2] == opponent and board[r][c-3] == 0:
                    evaluation_opponent += 50
                if board[r][c] == opponent and board[r][c-1] == opponent and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_opponent += 10
                if board[r][c] == opponent and board[r][c-1] == 0 and board[r][c-2] == 0 and board[r][c-3] == 0:
                    evaluation_opponent += 1


    return evaluation_player, evaluation_opponent



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
print_board(board)
game_over = False
turn = 0

while not game_over:

    if turn==0:
        player_piece = 1
        opponent_piece = 2
        col = int(input("Escolha a coluna que quer jogar:"))
        col -= 1
        
        if is_not_full(board, col):
            row = open_row(board, col)
            drop_piece(board, row, col, player_piece)
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                game_over = True
            p, o = evaluate(board, player_piece, opponent_piece)
            print(f"p={p} , o={o}")
            print_board(board)
            turn += 1
            turn = turn % 2
        else:
            print("A coluna escolhida está cheia")
        
    else:
        player_piece = 2
        oponnent_piece = 1
        col = int(input("Escolha a coluna que quer jogar:"))
        col -= 1

        if is_not_full(board, col):
            row = open_row(board, col)
            drop_piece(board, row, col, player_piece)
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                game_over = True
            p, o = evaluate(board, player_piece, opponent_piece)
            print(f"p={p} , o={o}")
            print_board(board)
            turn += 1
            turn = turn % 2
        else:
            print("A coluna escolhida está cheia")


    










