% import player_types
% from board import Board
<!DOCTYPE html>
<html>
<head>
    <title>Machine Learning Tic-Tac-Toe</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <script src="/js/jquery.js"></script>
    <script src="/js/game.js"></script>
</head>
<body>
    <h1>Machine Learning Tic-Tac-Toe</h1>
    <div id="select-container">
        % for piece_value in [Board.X, Board.O]:
            % piece = Board.format_piece(piece_value)
            % piece_lcase = piece.lower()
            <p class="{{piece_lcase}}">
                <label for="{{piece_lcase}}">Select {{piece}} Player:</label>
                <select id="{{piece_lcase}}" class="{{piece_lcase}}">
                % for player_type, description in \
                %         zip(player_types.get_player_types(), player_types.get_player_descriptions()):
                    <option value="{{player_type}}">{{description}}</option>
                % end
                </select>
            </p>
        % end
        <p>
            <button id="play">Play</button>
        </p>
    </div>

    <div id="game-container"></div>
    <div id="waiting"></div>
    <div id="error"></div>
</body>
</html>
