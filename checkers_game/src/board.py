import pygame
from .variables import BLACK, WHITE, ROWS, COLUMNS, RED, SQUARE_SIZE
from .pieces import Pieces

class Board:
    def __init__(self):
        self.board = []
        self.red_pieces = self.white_pieces = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(window, RED, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate_position(self):
        return self.white_pieces - self.red_pieces + (self.white_kings / 2 - self.red_kings / 2)

    def get_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)

        return pieces

    def move_piece(self, piece, row, column):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move_piece(row, column)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 
    
    def get_piece(self, row, column):
        return self.board[row][column]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Pieces(row, column, WHITE))
                    elif row > 4:
                        self.board[row].append(Pieces(row, column, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw_pieces(window)

    def remove_piece(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_pieces -= 1
                else:
                    self.white_pieces -= 1

    def winner(self):
        if self.red_pieces <= 0:
            return WHITE
        elif self.white_pieces <= 0:
            return RED
        
        return None

    def get_possible_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self.move_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.move_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self.move_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self.move_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    
        return moves

    def move_left(self, start, end, step, color, left, skipped = []):
        moves = {}
        last = []
        for r in range(start, end, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.move_left(r + step, row, step, color, left - 1, skipped = last))
                    moves.update(self.move_right(r + step, row, step, color, left + 1, skipped = last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def move_right(self, start, end, step, color, right, skipped = []):
        moves = {}
        last = []
        for r in range(start, end, step):
            if right >= COLUMNS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.move_left(r + step, row, step, color, right - 1, skipped = last))
                    moves.update(self.move_right(r + step, row, step, color, right + 1, skipped = last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

    def get_board(self):
        return self.board

    def ai_move_result(self, board):
        self.board = board
        self.change_turn()