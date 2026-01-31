from Board import Board
from draw_funcs import *
from helpers import *


WIDTH = 800
HEIGHT = 600
DEFAULT_VERT_PADDING = 20
BACKGROUND_COLOR = (255, 99, 71)
LIGHT_COLOR = (238, 238, 210)
DARK_COLOR = (118, 150, 86)


PLAYER_COLOR = "white"


screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = Board(PLAYER_COLOR)
board.refresh_all_figures()

sq_images = create_sq_images(WIDTH, HEIGHT, DEFAULT_VERT_PADDING, LIGHT_COLOR, DARK_COLOR, board.squares)
FIGURE_IMAGES = load_fig_images(int(sq_images[0][0].side))

available_squares = []
chosen_square = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if board.evolving_pawn:
                evolve_menu = show_evolve_menu(screen, board.evolving_pawn.color, sq_images[0][0].side, WIDTH, HEIGHT,
                                               FIGURE_IMAGES)
                chose_evolving_figure(evolve_menu, event, board)
                continue

            if not chosen_square:
                chosen_square = find_clicked_square(sq_images, event.pos)
                if chosen_square:
                    available_squares, chosen_square = mark_chosen(chosen_square, board.turn, board)
                else:
                    available_squares = []

            else:
                chosen_square.img.chosen = False
                new_square = find_clicked_square(sq_images, event.pos)
                if new_square in available_squares:
                    board.move_figure(chosen_square.figure, new_square)

                    game_end_msg = check_game_end(board)
                    if len(game_end_msg) > 0:
                        print(game_end_msg)
                        running = False

                    chosen_square = None
                    available_squares = []
                else:
                    available_squares, chosen_square = mark_chosen(new_square, board.turn, board)

    screen.fill(BACKGROUND_COLOR)
    draw_squares(screen, sq_images)
    draw_figures(screen, board.figures, FIGURE_IMAGES)
    if chosen_square:
        mark_available(screen, available_squares, chosen_square.figure.type)

    if board.evolving_pawn:
        show_evolve_menu(screen, board.evolving_pawn.color, sq_images[0][0].side, WIDTH, HEIGHT, FIGURE_IMAGES)

    pygame.display.flip()

pygame.quit()

