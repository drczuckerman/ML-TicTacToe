% import web_utils
% include(web_utils.get_template_path("header"))
</head>
<body>
<h1>Machine Learning Tic-Tac-Toe</h1>
<input id="x" type="hidden" value="{{player_types["x"]}}">
<input id="o" type="hidden" value="{{player_types["o"]}}">
% include(web_utils.get_template_path("board"), game_info=game_info)
% include(web_utils.get_template_path("footer"))
