% from board import Board

% turn_piece = Board.format_piece(game_info["turn"])
<input id="turn" type="hidden" value="{{turn_piece.lower()}}">
% winner = game_info["winner"]
<input id="game-over" type="hidden" value="{{1 if winner is not None else 0}}">

<div class="game-container">
<div class="status">
% winner_piece = None
% if winner == Board.DRAW:
    <span class="draw">Game Over</span>
% elif winner is not None:
    % winner_piece = Board.format_piece(winner)
    <span class="{{winner_piece.lower()}} win">Game Over</span>
% else:
    <span class="{{turn_piece.lower()}}">It's your turn, {{turn_piece}}</span>
% end
</div>

<table class="board">
% row_classes = ["top-row", "middle-row", "bottom-row"]
% col_classes = ["left-col", "middle-col", "right-col"]
% board = game_info["board"]
% winning_positions = game_info["winning_positions"]
% for row in range(3):
    <tr>
    % for col in range(3):
        <td class="{{row_classes[row]}} {{col_classes[col]}}">
        % pos = row*3 + col
        % if board[pos] == Board.EMPTY:
            <span class="empty-disabled">{{pos + 1}}</span>
        % else:
            % piece = Board.format_piece(board[pos])
            % class_names = [piece.lower()]
            % if pos in winning_positions:
                % class_names.append("win")
            % end
            <span class="{{" ".join(class_names)}}">{{piece}}</span>
        % end
        </td>
    % end
    </tr>
% end
</table>

<div class="status">
% if winner is not None:
    % winner_text = Board.get_winner_text(winner)
    % class_name = "draw" if winner == Board.DRAW else winner_piece.lower()
    <span class="{{class_name}}">{{winner_text}}</span>
% end
</div>

% if winner is not None:
    <p>
    <strong>Play Again?</strong><br>
    <button id="same_players_and_pieces">Same Players, Same Pieces</button>
    <button id="same_players_diff_pieces">Same Players, Diff Pieces</button>
    <button id="diff_players">Diff Players</button>
    </p>
% end
</div>
</div>
