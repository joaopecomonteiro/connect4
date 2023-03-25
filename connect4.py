import numpy as np
import pygame
import math
import time
import sys
import random
from collections import defaultdict

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


row_count = 6
column_count = 7


class MCTS():
    def __init__(self, state=None, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        # self.untried_cols = None
        self.untried_cols = self.untried_cols()
        

    # def create_state(self, board):
    #     self.state = board

    
    def untried_cols(self):
        # print(self.state)
        self.untried_cols = get_valid_locations(self.state)
        # print("adwawd")
        return self.untried_cols
    

    def q(self):
        return self.results[1] - self.results[-1] 


    def n(self):
        return self.number_of_visits
    

    def mcts_drop_piece(self, board, row, col, piece):
        temp_board = board.copy()
        temp_board[row][col] = piece
        return temp_board



    def expand(self, turn):
        col = self.untried_cols.pop()
        row = open_row(self.state, col)
        if turn == 0:
            next_state = self.mcts_drop_piece(self.state, row, col, player1_piece)
        else:
            next_state = self.mcts_drop_piece(self.state, row, col, player2_piece)
        
        # print(next_state)

        # next_state = self.mcts_drop_piece(self.state, row, col, player2_piece)

        child_node = MCTS(state=next_state, parent=self)
        self.children.append(child_node)
        return child_node
    
                
    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]


    def rollout(self):
        current_rollout_state = self.state
        turn = 0
        while not is_terminal_node(current_rollout_state):
            possible_moves = get_valid_locations(current_rollout_state)
            # print(np.flip(current_rollout_state, 0))
            # print(possible_moves)
            col = self.rollout_policy(possible_moves)
            row = open_row(current_rollout_state, col)
            if turn == 0:
                current_rollout_state = self.mcts_drop_piece(current_rollout_state, row, col, player1_piece)
            else:
                current_rollout_state = self.mcts_drop_piece(current_rollout_state, row, col, player2_piece)
            turn += 1
            turn = turn % 2
        return game_result(current_rollout_state)

    
    def backpropagate(self, result):
        self.number_of_visits += 1
        self.results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)
    

    def is_fully_expanded(self):
        return len(self.untried_cols) == 0


    def best_child(self, c_param=2):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]
    

    def tree_policy(self):
        current_node = self
        turn = 0
        turn += 1
        turn = turn % 2    
        while not is_terminal_node(current_node.state):
            if not current_node.is_fully_expanded():
                return current_node.expand(turn)
            else:
                current_node = current_node.best_child()
            turn += 1
            turn = turn % 2 
        return current_node


    def best_action(self):
        simulation_no = 100
        # print(self.untried_cols)
        for i in range(simulation_no):
            v = self.tree_policy()
            reward = v.rollout()
            print(reward)
            v.backpropagate(reward)
        return self.best_child(c_param=2)





def game_result(board):
    if winning_move(board, player1_piece):
        return -1
    elif winning_move(board, player2_piece):
        return 1
    else:
        return 0




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


def is_valid_location(board, col):
	return board[row_count-1][col] == 0


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
 

def evaluate_window(window, player):
    score = 0
    opponent = 2
    if player == 2:
         opponent = 1

    if window.count(player) == 4:
        score += 512
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 50
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10
    elif window.count(player) == 1 and window.count(0) == 3:
        score += 1

    if window.count(opponent) == 4:
        score -= 512
    elif window.count(opponent) == 3 and window.count(0) == 1:
        score -= 50
    elif window.count(opponent) == 2 and window.count(0) == 2:
        score -= 10
    elif window.count(opponent) == 1 and window.count(0) == 3:
        score -= 1

    return score



def score_position(board, player):

    opponent = 2
    if player == 2:
         opponent = 1

    score = 0

    # Score horizontal positions
    for r in range(row_count):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(column_count - 3):
            # Create a horizontal window of 4
            window = row_array[c:c + 4]
            if window.count(player) == 4:
                return 512
            elif window.count(opponent) == 4:
                return -512
            score += evaluate_window(window, player)

    # Score vertical positions
    for c in range(column_count):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(row_count - 3):
            # Create a vertical window of 4
            window = col_array[r:r + 4]
            if window.count(player) == 4:
                return 512
            elif window.count(opponent) == 4:
                return -512
            score += evaluate_window(window, player)

    # Score positive diagonals
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            # Create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(4)]
            if window.count(player) == 4:
                return 512
            elif window.count(opponent) == 4:
                return -512
            score += evaluate_window(window, player)

    # Score negative diagonals
    for r in range(row_count - 3):
        for c in range(column_count - 3):
            # Create a negative diagonal window of 4
            window = [board[r + 3 - i][c + i] for i in range(4)]
            if window.count(player) == 4:
                return 512
            elif window.count(opponent) == 4:
                return -512
            score += evaluate_window(window, player)

    return score

def get_valid_locations(board):
	valid_locations = []
	for col in range(column_count):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations


def is_terminal_node(board):
	return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0




def minimax(board, depth, alpha, beta, maximizingPlayer):
    if turn != 0:
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, player2_piece):
                    return (None, 100000000000000)
                elif winning_move(board, player1_piece):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, score_position(board, player2_piece))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, player2_piece)
                new_score = minimax(b_copy, depth-1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, player1_piece)
                new_score = minimax(b_copy, depth-1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value








def alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    if turn != 0:
        valid_locations = get_valid_locations(board)
        is_terminal = is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if winning_move(board, 2):
                    return (None, 100000000000000)
                elif winning_move(board, 1):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, score_position(board, 2))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 2)
                new_score = alpha_beta(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, 1)
                new_score = alpha_beta(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value




def greedy(board, piece):
    valid_locations = get_valid_locations(board)
    best_score  = -math.inf
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        print(f"Score: {score}, col: {col+1}")
        if score > best_score:
            best_score = score
            best_col = col
    return best_col





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





player_1 = int(input("Jogador 1(1: Humano,2: Greedy, 3:  Minimax, 4: Alpha Beta): "))
player_2 = int(input("Jogador 2(1: Humano,2: Greedy, 3:  Minimax, 4: Alpha Beta, 5: MonteCarloTreeSearch): "))
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

player1_piece = 1
player2_piece = 2


while not game_over:
    if turn == 0:
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

                    if is_valid_location(board, col):
                        row = open_row(board, col)
                        drop_piece(board, row, col, player1_piece)
                        if len(get_valid_locations(board)) == 0:
                            print(f"Empate!!")
                            label = myfont.render(f"Empate!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        if winning_move(board, player1_piece):
                            print(f"Jogador {player1_piece} ganhou!!")
                            label = myfont.render(f"Player {player1_piece} wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        print(score_position(board, player1_piece))
                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2
                    else:
                        print("A coluna escolhida está cheia")

        if player_1 == 2:
            time.sleep(1)
            for event in pygame.event.get():
                if event.type != pygame.MOUSEBUTTONDOWN:
                    n = 1
            if n == 1:
                col = greedy(board, player2_piece)            
                if is_valid_location(board, col):
                    row = open_row(board, col)
                    drop_piece(board, row, col, player1_piece)
                    if len(get_valid_locations(board)) == 0:
                        print(f"Empate!!")
                        label = myfont.render(f"Empate!!", 1, BLUE)
                        screen.blit(label, (40,10))
                        # pygame.display.update()
                        game_over = True
                    if winning_move(board, player1_piece):
                        print(f"Jogador {player1_piece} ganhou!!")
                        label = myfont.render(f"Player {player1_piece} wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        # pygame.display.update()
                        game_over = True
                    print(score_position(board, player1_piece))
                    print_board(board)
                    draw_board(board)
                    turn += 1
                    turn = turn % 2


    else:
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

                    if is_valid_location(board, col):
                        row = open_row(board, col)
                        drop_piece(board, row, col, player2_piece)
                        if len(get_valid_locations(board)) == 0:
                            print(f"Empate!!")
                            label = myfont.render(f"Empate!!", 1, BLUE)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        if winning_move(board, player2_piece):
                            print(f"Jogador {player2_piece} ganhou!!")
                            label = myfont.render(f"Player {player2_piece} wins!!", 1, RED)
                            screen.blit(label, (40,10))
                            # pygame.display.update()
                            game_over = True
                        print(score_position(board, player2_piece))
                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2
                    else:
                        print("A coluna escolhida está cheia")

        elif player_2 == 2:
            time.sleep(1)
            col = greedy(board, player2_piece)
            if is_valid_location(board, col):
                row = open_row(board, col)
                drop_piece(board, row, col, player2_piece)
                print(score_position(board, player2_piece))
                if len(get_valid_locations(board)) == 0:
                    print(f"Empate!!")
                    label = myfont.render(f"Empate!!", 1, BLUE)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                if winning_move(board, player2_piece):
                    print(f"Jogador {player2_piece} ganhou!!")
                    label = myfont.render(f"Player {player2_piece} wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                print(score_position(board, player2_piece))
                print_board(board)
                draw_board(board)
                turn += 1
                turn = turn % 2


        elif player_2 == 3:

            time.sleep(1)
            col = minimax(board, 5, -math.inf, math.inf, True)[0]
            if is_valid_location(board, col):
                row = open_row(board, col)
                drop_piece(board, row, col, player2_piece)
                print(score_position(board, player2_piece))
                if len(get_valid_locations(board)) == 0:
                    print(f"Empate!!")
                    label = myfont.render(f"Empate!!", 1, BLUE)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                if winning_move(board, player2_piece):
                    print(f"Jogador {player2_piece} ganhou!!")
                    label = myfont.render(f"Player {player2_piece} wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                print_board(board)
                draw_board(board)
                print(score_position(board, player2_piece))
                turn += 1
                turn = turn % 2






        elif player_2 == 4:

            time.sleep(1)
            col = alpha_beta(board, 5, -math.inf, math.inf, True)[0]
            if is_valid_location(board, col):
                row = open_row(board, col)
                drop_piece(board, row, col, player2_piece)
                print(score_position(board, player2_piece))
                if len(get_valid_locations(board)) == 0:
                    print(f"Empate!!")
                    label = myfont.render(f"Empate!!", 1, BLUE)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                if winning_move(board, player2_piece):
                    print(f"Jogador {player2_piece} ganhou!!")
                    label = myfont.render(f"Player {player2_piece} wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
                print_board(board)
                draw_board(board)
                print(score_position(board, player2_piece))
                turn += 1
                turn = turn % 2

        elif player_2 == 5:

            root = MCTS(state=board)
            # root.create_state(board)
            board = root.best_action().state
            if len(get_valid_locations(board)) == 0:
                    print(f"Empate!!")
                    label = myfont.render(f"Empate!!", 1, BLUE)
                    screen.blit(label, (40,10))
                    # pygame.display.update()
                    game_over = True
            if winning_move(board, player2_piece):
                print(f"Jogador {player2_piece} ganhou!!")
                label = myfont.render(f"Player {player2_piece} wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                # pygame.display.update()
                game_over = True
            print_board(board)
            draw_board(board)
            print(score_position(board, player2_piece))
            turn += 1
            turn = turn % 2



while game_over: 
    pygame.display.update()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()