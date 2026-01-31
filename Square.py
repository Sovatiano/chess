import pygame


class SquareObj:
    def __init__(self, row, column, figure=None):
        self.row = row
        self.col = column
        self.figure = figure
        self.white_attack = False
        self.black_attack = False
        self.en_passant = 0
        self.img = None


    def place_figure(self, figure):
        self.figure = figure


    def mark_en_passant(self, cur_move):
        self.en_passant = cur_move


class SquareImg:
    def __init__(self, pos_x, pos_y, side, color, sq_color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side
        self.color = color
        self.chosen = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.side, self.side)
        self.obj = None
        self.sq_color = sq_color


    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
