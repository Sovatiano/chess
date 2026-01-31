from Figure import Figure


class Queen(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "queen"
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)]