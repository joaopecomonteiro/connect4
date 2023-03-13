import numpy as np
import pygame
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
        

def is_full(board, col):
    return board[row_count]

