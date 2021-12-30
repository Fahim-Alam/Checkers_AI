import pygame
from .variables import SQUARE_SIZE, RED, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, window):
        self._base()
        self.window = window

    def _base(self):
        self.selected_piece = None
        self.board = Board()
        self.turn = RED
        self.possible_moves = {}

    def update_board(self):
        self.board.draw(self.window)
        self.draw_possible_moves(self.possible_moves)
        pygame.display.update()

    def reset_game(self):
        self._base()

    def select_piece(self, row, column):
        if self.selected_piece:
            result = self.move_piece(row, column)
            if not result:
                self.selected = None
        
        piece = self.board.get_piece(row, column)
        if piece != 0 and piece.color == self.turn:
            self.selected_piece = piece
            self.possible_moves = self.board.get_possible_moves(piece)
            return True
            
        return False

    def move_piece(self, row, column):
        piece = self.board.get_piece(row, column)

        if self.selected_piece and piece == 0 and (row, column) in self.possible_moves:
            self.board.move_piece(self.selected_piece, row, column)
            skipped = self.possible_moves[(row, column)]

            if skipped:
                self.board.remove_piece(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_possible_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.window, BLUE, (column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.possible_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def winner(self):
        return self.board.winner()

    def get_board(self):
        return self.board

    def ai_move_result(self, board):
        self.board = board
        self.change_turn()