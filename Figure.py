class Figure:
    def __init__(self, square, color, start_pos):
        square.place_figure(self)
        self.square = square
        self.color = color
        self.type = None
        self.moves_number = 0
        self.available_squares = []
        self.direction = -1 if start_pos == "down" else 1
        self.captured = False
        self.directions = []
        self.row = self.square.row
        self.col = self.square.col


    def move(self, new_square, is_simulation=False):
        if new_square.figure:
            new_square.figure.become_captured()
        self.square.figure = None
        self.square = new_square
        self.row = new_square.row
        self.col = new_square.col
        self.square.figure = self
        if not is_simulation:
            self.moves_number += 1


    def become_captured(self):
        self.square.figure = None
        self.square = None
        self.captured = True


    def check_if_ally(self, square):
        if square.figure and square.figure.color == self.color:
            return True
        return False


    def check_if_enemy(self, square):
        if square.figure and square.figure.color != self.color:
            return True
        return False


    def refresh_available_squares(self, squares):
        if self.captured:
            return None
        self.get_available_squares(squares)


    def get_available_squares(self, squares):
        self.available_squares.clear()
        self.scan_squares(self.directions, squares)


    def mark_square_under_attack(self, square):
        if self.color == "white":
            square.white_attack = True
        else:
            square.black_attack = True


    def check_square(self, row, column, squares):
        if not (0 <= row <= 7 and 0 <= column <= 7):
            return False
        new_square = squares[row][column]
        self.mark_square_under_attack(new_square)
        if self.check_if_ally(new_square):
            return False
        elif self.check_if_enemy(new_square):
            self.available_squares.append(new_square)
            return False
        else:
            self.available_squares.append(new_square)
            return True


    def scan_squares(self, directions, squares):
        for dr, dc in directions:
            cur_row = self.row
            cur_col = self.col
            while True:
                cur_row += dr
                cur_col += dc
                if not self.check_square(cur_row, cur_col, squares):
                    break


