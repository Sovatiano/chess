from Figure import Figure


class Knight(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "knight"

    def get_available_squares(self, squares):
        self.available_squares.clear()

        possible_moves = [(2, -1), (2, 1),
                          (-2, -1), (-2, 1),
                          (-1, 2), (-1, -2),
                          (1, 2), (1, -2)]
        for move in possible_moves:
            new_row = self.row + move[0]
            new_col = self.col + move[1]
            self.check_square(new_row, new_col, squares)