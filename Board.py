from Square import SquareObj
from figures.Bishop import Bishop
from figures.Pawn import Pawn
from figures.Queen import Queen
from figures.Rook import Rook
from figures.Knight import Knight
from figures.King import King


class Board:
    def __init__(self, player_color):
        self.player_side = player_color
        self.squares = self.create_squares()
        self.figures = self.create_figures(self.squares, player_color)
        self.halfmove_clock = 0
        self.moves_counter = 0
        self.turn = "white"
        self.check = None
        self.evolving_pawn = None


    @staticmethod
    def create_squares():
        squares = []
        for row in range(8):
            new_row = []
            for column in range(8):
                new_square = SquareObj(row, column)
                new_row.append(new_square)
            squares.append(new_row)
        return squares


    @staticmethod
    def create_figures(squares, players_side):
        figures_map = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        figures = []
        colors = {
            "player": "white" if players_side == "white" else "black",
            "enemy": "black" if players_side == "white" else "white"
        }
        for column in range(8):
            enemy_figure = figures_map[column](squares[0][column], colors["enemy"], "up")
            enemy_pawn = Pawn(squares[1][column], colors["enemy"], "up")

            player_figure = figures_map[column](squares[7][column], colors["player"], "down")
            player_pawn = Pawn(squares[6][column], colors["player"], "down")

            figures += [enemy_figure, enemy_pawn, player_figure, player_pawn]

        return figures


    def refresh_all_figures(self):
        for row in self.squares:
            for sq in row:
                sq.black_attack = False
                sq.white_attack = False
                if self.moves_counter - sq.en_passant > 1:
                    sq.en_passant = 0

        for figure in self.figures:
            if not figure.captured and figure.type != "king":
                figure.refresh_available_squares(self.squares)

        for figure in self.figures:
            if not figure.captured and figure.type == "king":
                figure.refresh_available_squares(self.squares)


    def check_if_check(self):
        self.check = None
        for fig in filter(lambda x: x.type == "king", self.figures):
            if fig.color == "white" and fig.square.black_attack or fig.color == "black" and fig.square.white_attack:
                self.check = fig.color


    def move_figure(self, figure, square):
        self.halfmove_clock += 1
        if square.figure is not None:
            self.halfmove_clock = 0
        if figure.type == "pawn":
            self.halfmove_clock = 0
            self.move_pawn(figure, square)
        elif figure.type == "king":
            self.move_king(figure, square)
            self.refresh_all_figures()
        else:
            figure.move(square)
            self.refresh_all_figures()
        self.turn = "white" if self.turn == "black" else "black"
        self.moves_counter += 1
        self.check_if_check()


    @staticmethod
    def check_if_last_row(square):
        if square.row in (0, 7):
            return True
        return False


    def do_en_passant(self, square):
        pawn_dir = -1 if self.turn == "white" else 1
        pawn = self.squares[square.row - pawn_dir][square.col].figure
        pawn.become_captured()


    def mark_en_passant(self, square):
        pawn_dir = -1 if self.turn == "white" else 1
        self.squares[square.row - pawn_dir][square.col].mark_en_passant(self.moves_counter)


    def move_pawn(self, pawn, square):
        if self.check_if_last_row(square):
            self.evolving_pawn = pawn
            pawn.move(square)
            return
        if square.en_passant > 0:
            self.do_en_passant(square)
            pawn.move(square)
            self.refresh_all_figures()
            return
        if abs(square.row - pawn.row) == 2:
            self.mark_en_passant(square)
            pawn.move(square)
            self.refresh_all_figures()
            return
        pawn.move(square)
        self.refresh_all_figures()


    def do_castle(self, square, direction):
        if direction == "left":
            rook = self.squares[square.row][0].figure
            rook.move(self.squares[square.row][3])
        else:
            rook = self.squares[square.row][7].figure
            rook.move(self.squares[square.row][5])


    def move_king(self, king, square):
        if abs(square.col - king.col) > 1:
            direction = "left" if king.col > square.col else "right"
            self.do_castle(square, direction)
        king.move(square)

    def simulate_move(self, fig, square, king_square, color):
        is_valid_move = False
        start_sq = fig.square
        att_fig = square.figure

        fig.move(square, True)
        self.refresh_all_figures()

        if fig.type != "king":
            if (not king_square.black_attack and color == "white") or \
                    (not king_square.white_attack and color == "black"):
                is_valid_move = True
        else:
            if (not square.black_attack and color == "white") or \
                    (not square.white_attack and color == "black"):
                is_valid_move = True

        fig.square.figure = None
        fig.square = start_sq
        fig.row = start_sq.row
        fig.col = start_sq.col
        start_sq.figure = fig

        if att_fig:
            square.figure = att_fig
            att_fig.captured = False
            att_fig.square = square
        else:
            square.figure = None

        self.refresh_all_figures()
        return is_valid_move

    def check_moves(self, color, fig):
        king_square = None
        for king_fig in filter(lambda x: x.type == "king" and x.color == color, self.figures):
            king_square = king_fig.square
            break
        new_available_squares = []
        for move in fig.available_squares:
            if self.simulate_move(fig, move, king_square, color):
                new_available_squares.append(move)
        fig.available_squares = new_available_squares


    def pawn_evolve(self, pawn, new_type):
        square = pawn.square
        color = pawn.color

        pawn.become_captured()

        figures_types = {
            "queen": Queen,
            "rook": Rook,
            "knight": Knight,
            "bishop": Bishop
        }

        new_figure = figures_types[new_type](square, color, pawn.direction)
        self.figures.append(new_figure)


