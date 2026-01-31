def find_clicked_square(squares, pos):
    for row in squares:
        for square in row:
            if square.is_clicked(pos):
                return square.obj
    return None


def mark_chosen(chosen_square, turn, board):
    if chosen_square.figure and chosen_square.figure.color == turn:
        chosen_square.img.chosen = True
        board.check_moves(turn, chosen_square.figure)
        available_squares = chosen_square.figure.available_squares
    else:
        available_squares = []
        chosen_square = None

    return available_squares, chosen_square


def check_if_mate(board):
    num_squares = 0
    for fig in filter(lambda x: x.color == board.check and x.captured == False, board.figures):
        board.check_moves(board.check, fig)
        num_squares += len(fig.available_squares)
    return num_squares == 0


def check_if_stalemate(board):
    num_squares = 0
    for fig in filter(lambda x: x.color == board.turn and x.captured == False, board.figures):
        board.check_moves(board.turn, fig)
        num_squares += len(fig.available_squares)
    return num_squares == 0


def make_materials_list(board, color):
    figures = []
    for fig in filter(lambda x: x.color == color and x.captured == False, board.figures):
        if fig.type == "bishop":
            fig_name = f"{fig.square.img.sq_color}-{fig.type}"
            if fig_name not in figures:
                figures.append(fig_name)
        else:
            figures.append(fig.type)

    return figures


def check_game_end(board):
    if board.check:
        color = board.check
    else:
        color = board.turn
    num_squares = 0
    for fig in filter(lambda x: x.color == color and x.captured == False, board.figures):
        board.check_moves(color, fig)
        num_squares += len(fig.available_squares)

    if num_squares == 0:
        if board.check:
            return f"Мат! Победа {"белых" if board.check == "black" else "чёрных"}"
        else:
            return f"Пат! Ничья"

    if board.halfmove_clock == 100:
        return f"Ничья по правилу 50 ходов!"

    low_material_situations = [["king"], sorted(["king", "knight"]), sorted(["king", "white-bishop"]),
                               sorted(["king", "black-bishop"])]

    white_figures = sorted(make_materials_list(board, "white"))
    black_figures = sorted(make_materials_list(board, "black"))
    if white_figures in low_material_situations and black_figures in low_material_situations:
        return f"Ничья из-за недостатка материала у обеих сторон!"

    return ""


def chose_evolving_figure(evolve_menu_rects, event, board):
    for fig_type, rect in evolve_menu_rects.items():
        if rect.collidepoint(event.pos):
            board.pawn_evolve(board.evolving_pawn, fig_type)
            board.evolving_pawn = None
            board.refresh_all_figures()
            break