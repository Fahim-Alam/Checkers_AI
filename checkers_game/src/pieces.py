import pygame
from .variables import SQUARE_SIZE, RED, GREY, CROWN

class Pieces:
    PADDING = 15
    OUTLINE = 0

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.set_position()
        
        if self.color == RED:
            self.direciton = -1
        else: 
            self.direction = 1

    def set_position(self):
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw_pieces(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move_piece(self, row, column):
        self.row = row
        self.column = column
        self.set_position()

    def __repr__(self):
        return str(self.color)