from Figure import Figure


class Pawn(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "pawn"


    def get_available_squares(self, squares):
        self.available_squares.clear()
        if 0 <= self.row + self.direction <= 7:
            forward_sq = squares[self.row + self.direction][self.col]
            if forward_sq.figure is None:
                self.available_squares.append(forward_sq)
                if self.moves_number == 0:
                    forwardx2_sq = squares[self.row + self.direction * 2][self.col]
                    if forwardx2_sq.figure is None:
                        self.available_squares.append(forwardx2_sq)

            if 0 <= self.col + self.direction <= 7:
                left_diag_sq = squares[self.row + self.direction][self.col + self.direction]
                self.mark_square_under_attack(left_diag_sq)
                if (left_diag_sq.figure and left_diag_sq.figure.color != self.color) or left_diag_sq.en_passant > 0:
                    self.available_squares.append(left_diag_sq)

            if 0 <= self.col - self.direction <= 7:
                right_diag_sq = squares[self.row + self.direction][self.col - self.direction]
                self.mark_square_under_attack(right_diag_sq)
                if (right_diag_sq.figure and right_diag_sq.figure.color != self.color) or right_diag_sq.en_passant > 0:
                    self.available_squares.append(right_diag_sq)