% from web_utils import get_template_path
<input id="x" type="hidden" value="{{player_types["x"]}}">
<input id="o" type="hidden" value="{{player_types["o"]}}">
% include(get_template_path("board"), game_info=game_info)
