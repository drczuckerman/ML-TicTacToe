from contextlib import contextmanager

class Board(object):
    EMPTY = 0
    X = 1
    O = -1
    DRAW = 2
    PIECE_DICT = {X: "X", O: "O"}
    WINNER_DICT = {X: "X Wins", O: "O Wins", DRAW: "Draw"}

    def __init__(self):
        self.state = [self.EMPTY]*9

    def is_valid_move(self, position):
        return (position >= 0 and position <= 8 and self.state[position] == self.EMPTY and
            self.get_winner() is None)
    
    def make_move(self, position, piece):
        self.state[position] = piece
        
    @contextmanager
    def try_move(self, position, piece):
        self.make_move(position, piece)
        yield self.get_winner(), tuple(self.state)
        self.make_move(position, self.EMPTY)

    def get_available_moves(self):
        return list(filter(lambda position: self.state[position] == self.EMPTY, range(9)))

    def get_winning_positions(self):
        for a,b,c in ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)):
            if (self.state[a] != self.EMPTY and self.state[a] == self.state[b] and
                self.state[a] == self.state[c]):
                return [a,b,c]

        return []

    def get_winner(self):
        positions = self.get_winning_positions()
        if positions:
            return self.state[positions[0]]

        return self.DRAW if self.state.count(self.EMPTY) == 0 else None

    @staticmethod
    def get_winner_text(winner):
        return Board.WINNER_DICT.get(winner)

    def format_board(self):
        winning_positions = self.get_winning_positions()
        row_sep = "+".join(["---"]*3) + "\n"
        return row_sep.join(self._format_row(row, winning_positions) for row in range(3))

    def _format_row(self, row, winning_positions):
         return "|".join(self._format_piece_with_winning_positions(row, col, winning_positions)
                         for col in range(3)) + "\n"

    def _format_piece_with_winning_positions(self, row, col, winning_positions):
        pos = 3*row + col
        is_winning_position = pos in winning_positions
        prefix = "(" if is_winning_position else " "
        suffix = ")" if is_winning_position else " "
        return prefix + self._format_state(pos) + suffix

    def _format_state(self, pos):
        return self.PIECE_DICT.get(self.state[pos], str(pos + 1))

    @staticmethod
    def format_piece(piece):
        return Board.PIECE_DICT[piece]
