from Figure import Figure


class Bishop(Figure):
    def __init__(self, square, color, start_pos):
        super().__init__(square, color, start_pos)
        self.type = "bishop"
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]