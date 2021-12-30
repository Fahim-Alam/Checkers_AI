import pygame
import sys
from src.variables import WHITE, WIDTH, HEIGHT, SQUARE_SIZE
from src.game import Game
from src.algorithm import minimax

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Checkers')

FPS = 60

def get_mouse_position(position):
    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE
    return row, column

def main():
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    if game.winner() != None:
        pygame.time.wait(3000)
        sys.exit()

    while True:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move_result(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                row, column = get_mouse_position(mouse_position)
                game.select_piece(row, column)

        game.update_board()

main()