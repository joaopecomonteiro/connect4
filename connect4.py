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
        oponnent_piece = 2
        col = int(input("Escolha a coluna que quer jogar:"))
        col -= 1
        
        if is_not_full(board, col):
            row = open_row(board, col)
            drop_piece(board, row, col, player_piece)
            if winning_move(board, player_piece):
                print(f"Jogador {player_piece} ganhou!!")
                game_over = True
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
            print_board(board)
            turn += 1
            turn = turn % 2
        else:
            print("A coluna escolhida está cheia")


    










