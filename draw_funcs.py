import pygame
from Square import SquareImg


def create_sq_images(width, height, vert_padding, light_color, dark_color, squares):
    square_imgs = []
    vert_padding += (height - vert_padding) % 8 / 2
    chess_side = height - vert_padding * 2
    hor_padding = (width - chess_side) / 2
    for row in range(8):
        is_white = True if row % 2 == 0 else False
        new_row = []
        for column in range(8):
            new_square = SquareImg(hor_padding + (chess_side // 8) * column,
                                vert_padding + (chess_side // 8) * row,
                                chess_side // 8,
                                light_color if is_white else dark_color,
                                   "white" if is_white else "black")
            is_white = not is_white
            new_row.append(new_square)
            sq_obj = squares[row][column]
            new_square.obj = sq_obj
            sq_obj.img = new_square
        square_imgs.append(new_row)
    return square_imgs


def load_fig_images(sq_side):
    fig_images = {}
    for color in ("white", "black"):
        for fig_type in ("pawn", "knight", "bishop", "rook", "king", "queen"):
            path = f"src/figures/{color}/"
            new_fig = pygame.image.load(path + f"{fig_type}.png").convert_alpha()
            fig_images[(color, fig_type)] = pygame.transform.scale(new_fig, (sq_side, sq_side))
    return fig_images

def draw_squares(screen, squares):
    for row in squares:
        for square in row:
            pygame.draw.rect(screen, square.color, square.rect, 0)
            if square.chosen:
                border = pygame.Rect(square.pos_x, square.pos_y, square.side, square.side)
                pygame.draw.rect(screen, (50, 205, 50), border, 3)


def draw_figures(screen, figures, fig_images):
    for figure in figures:
        if not figure.captured:
            new_figure = fig_images[(figure.color, figure.type)]
            x = int(figure.square.img.pos_x)
            y = int(figure.square.img.pos_y)
            screen.blit(new_figure, (x, y))


def mark_available(screen, available_squares, fig_type):
    if available_squares:
        radius = available_squares[0].img.side // 5
        for square in available_squares:
            center = (square.img.pos_x + square.img.side // 2,
                      square.img.pos_y + square.img.side // 2)
            if square.figure or square.en_passant != 0 and fig_type == "pawn":
                pygame.draw.circle(screen, (205, 92, 92), center, radius)
            else:
                pygame.draw.circle(screen, (124, 252, 0), center, radius)


def show_evolve_menu(screen, color, square_side, screen_width, screen_height, fig_images):
    menu_width = square_side * 4
    menu_height = square_side
    menu_x = (screen_width - menu_width) // 2
    menu_y = (screen_height - menu_height) // 2

    menu_rect = pygame.Rect(menu_x - 10, menu_y - 10, menu_width + 20, menu_height + 20)
    pygame.draw.rect(screen, (50, 50, 50), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    figure_types = ["queen", "rook", "bishop", "knight"]
    figure_rects = {}

    for i, fig_type in enumerate(figure_types):
        x = menu_x + i * square_side
        y = menu_y

        cell_color = (238, 238, 210) if i % 2 == 0 else (118, 150, 86)
        cell_rect = pygame.Rect(x, y, square_side, square_side)
        pygame.draw.rect(screen, cell_color, cell_rect)

        figure_img = fig_images[(color, fig_type)]
        screen.blit(figure_img, (x, y))

        figure_rects[fig_type] = cell_rect

    return figure_rects