from board import Board

def set_board(board, pieces):
    for index, piece in get_board_state(pieces):
        board.state[index] = piece

def get_board_state(pieces):
    for index, piece in get_index_and_pieces(pieces):
        if piece == "X":
            yield index, Board.X
        elif piece == "O":
            yield index, Board.O
        else:
            yield index, Board.EMPTY

def get_board_state_tuple(pieces):
    return tuple(piece for _, piece in get_board_state(pieces))
    
def assert_board_state_tuple_is(cls, pieces, state):
    cls.assertEqual(get_board_state_tuple(pieces), state)

def assert_board_is(cls, board, pieces=""):
    expected_board = Board()
    for index, piece in get_index_and_pieces(pieces):
        if piece == "X":
            expected_board.state[index] = Board.X
        elif piece == "O":
            expected_board.state[index] = Board.O

    cls.assertEqual(expected_board.state, board.state)

def get_index_and_pieces(pieces):
    return enumerate(pieces.replace("|", ""))

def get_expected_formatted_board(formatted_pieces):
    expected_output = ""
    position = 0
    for piece in formatted_pieces:
        if piece in ["X", "O"]:
            expected_output += "(" + piece + ")"
        elif piece in ["x", "o"]:
            expected_output += " " + piece.upper() + " "
        elif piece == "|":
            expected_output += "---+---+---\n"
        else:
            expected_output += " " + str(position + 1) + " "

        if piece != "|":
            expected_output += "\n" if (position % 3) == 2 else "|"
            position += 1

    return expected_output

def assert_get_move_is(cls, player, board, position, piece, pieces=""):
    player.set_piece(piece)
    set_board(board, pieces)
    cls.assertEqual(position, player.get_move())

def assert_get_move_values_are(cls, player, board, values, piece, pieces=""):
    player.set_piece(piece)
    set_board(board, pieces)
    move_values = player.get_move_values()
    cls.assertEqual(list(values.keys()), list(move_values.keys()))
    for value, move_value in zip(values.values(), move_values.values()):
        cls.assertAlmostEqual(value, move_value)
