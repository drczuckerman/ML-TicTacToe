% import web_utils
% include(web_utils.get_template_path("header"))
% import player_types
% from board import Board

</head>
<body>
<h1>Machine Learning Tic-Tac-Toe</h1>
<div class="select-players">
% for piece_value in [Board.X, Board.O]:
    % piece = Board.format_piece(piece_value)
    % piece_lcase = piece.lower()
    <p class="{{piece_lcase}}">
    <label for="{{piece_lcase}}_player">Select {{piece}} Player:</label>
    <select id="{{piece_lcase}}_player" class="{{piece_lcase}}">
    % for player_type, description in \
    %        zip(player_types.get_player_types(), player_types.get_player_descriptions()):
        <option value="{{player_type}}">{{description}}</option>
    % end
    </select>
    </p>
% end
</div>
<button id="play">Play</button>
% include(web_utils.get_template_path("footer"))
