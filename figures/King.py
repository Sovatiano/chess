from Figure import Figure


class King(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "king"
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)]


    def check_if_square_under_attack(self, square):
        if square.white_attack and self.color == "black" or square.black_attack and self.color == "white":
            return True
        return False


    def check_if_square_available(self, square):
        if self.check_if_ally(square):
            return False
        else:
            if not self.check_if_square_under_attack(square):
                self.available_squares.append(square)
        self.mark_square_under_attack(square)

    def add_castle_moves(self, squares):
        directions = [-1, 1]
        cur_row = self.row
        for d in directions:
            cur_col = self.col
            while 0 <= cur_col + d <= 7:
                cur_col += d
                next_sq = squares[cur_row][cur_col]
                if self.check_if_enemy(next_sq):
                    break
                if self.check_if_ally(next_sq):
                    if next_sq.figure.type == "rook" and next_sq.figure.moves_number == 0:
                        if cur_col == 0:
                            self.available_squares.append(squares[cur_row][2])
                        elif cur_col == 7:
                            self.available_squares.append(squares[cur_row][6])
                    break
                if self.check_if_square_under_attack(next_sq):
                    break


    def get_available_squares(self, squares):
        self.available_squares.clear()
        for dr, dl in self.directions:
            new_row, new_col = self.row + dr, self.col + dl
            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                new_square = squares[new_row][new_col]
                self.check_if_square_available(new_square)
        if self.moves_number == 0 and not self.check_if_square_under_attack(self.square):
            self.add_castle_moves(squares)
