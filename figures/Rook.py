from Figure import Figure


class Rook(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "rook"
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]