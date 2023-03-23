

		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, PLAYER_PIECE)
			if winning_move(board, PLAYER_PIECE):
				label = myfont.render("Player 1 wins!!", 1, RED)
				screen.blit(label, (40,10))
				game_over = True
						
				turn += 1
				turn = turn % 2
				print_board(board)
				draw_board(board)
				print(score_position(board, PLAYER_PIECE))