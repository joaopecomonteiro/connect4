turn += 1
			turn = turn % 2
			print_board(board)
			draw_board(board)
			print(score_position(board, PLAYER_PIECE))