players = {}
waiting_timer = null;

$(document).ready(function()
{
    $("#play").click(play_game);
});

function play_game()
{
    players = {x: $("#x").val(), o: $("#o").val()};
    disable_select_players();
    get_game();
}

function get_game()
{
    post_to_server("/play", players, hide_select_players_and_show_game, enable_select_players);
}

function post_to_server(url, data, done_function, error_function)
{
    communicate_with_server(
        {
            method: "POST",
            url: url,
            contentType: "application/json",
            dataType: "html",
            data: JSON.stringify(data),
        },
        done_function, error_function);
}

function get_from_server(url, done_function, error_function)
{
    communicate_with_server(
        {
            method: "GET",
            url: url,
            dataType: "html"
        },
        done_function, error_function);
}

function communicate_with_server(ajax_struct, done_function, error_function)
{
    indicate_no_error();
    deferred_indicate_waiting();
    $.ajax(ajax_struct)
    .done(done_function)
    .fail(function(jqXHR, textStatus, errorThrown)
    {
        if (error_function)
        {
            error_function();
        }
        indicate_not_waiting();
        indicate_error(textStatus, errorThrown);
    });
}

function disable_select_players()
{
    $("#select-container").find("select, button").attr("disabled", "disabled");
}

function enable_select_players()
{
    $("#select-container").find("select, button").removeAttr("disabled");
}

function hide_select_players()
{
    $("#select-container").hide();
}

function show_select_players()
{
    $("#select-container").show();
}

function hide_select_players_and_show_game(data)
{
    hide_select_players();
    show_game(data);
}

function show_game(data)
{
    show_board(data);
    indicate_not_waiting();
    if (!is_game_over())
    {
        if (is_human_player())
        {
            enable_empty_squares();
        }
        else
        {
            setTimeout(get_computer_move, 100);
        }
    }
    else
    {
        bind_and_enable_game_over_buttons();
    }
}

function hide_game()
{
    $("#game-container").html("");
}

function show_board(data)
{
    $("#game-container").html(data);
}

function is_human_player()
{
    piece = get_current_player();
    return players[piece] == "Human";
}

function get_current_player()
{
    return $("#turn").val();
}

function is_game_over()
{
    return $("#game-over").val() == "1";
}

function indicate_error(error_type, error_msg)
{
    msg = error_type.substring(0, 1).toUpperCase() + error_type.substring(1) + " accessing server";
    if (error_msg)
    {
        msg += ": " + error_msg;
    }
    show_class_text("error", error_msg);
}

function indicate_no_error()
{
    $("#error").html("");
}

function deferred_indicate_waiting()
{
    stop_waiting_timer();
    waiting_timer = setTimeout(indicate_waiting, 500);
}

function stop_waiting_timer()
{
    if (waiting_timer)
    {
        clearTimeout(waiting_timer);
    }

    waiting_timer = null;
}

function indicate_waiting()
{
    show_class_text("waiting", "Waiting for server...");
}

function indicate_not_waiting()
{
    stop_waiting_timer();
    $("#waiting").html("");
}

function show_class_text(cls, text)
{
    return $("#" + cls).html('<p><span class="' + cls + '">' + text + "</span></p>");
}

function disable_empty_squares()
{
    $(".empty")
    .removeClass("empty")
    .addClass("empty-disabled")
    .unbind("click");
}

function enable_empty_squares()
{
    $(".empty-disabled")
    .removeClass("empty-disabled")
    .addClass("empty")
    .unbind("click")
    .bind("click", post_human_move);
}

function post_human_move()
{
    var position = $.trim($(this).text());
    disable_empty_squares();
    play_human_move($(this));
    post_to_server("/human_move", {"move": position}, show_game,
        function()
        {
            undo_human_move($(this), position); 
        });
}

function get_computer_move()
{
    get_from_server("/computer_move", show_game);
}

function play_human_move(obj)
{
    var turn = get_current_player();
    obj.removeClass("empty-disabled").addClass(turn).text(turn.toUpperCase());
}

function undo_human_move(obj, position)
{
    var turn = get_current_player();
    obj.removeClass(turn).addClass("empty-disabled").text(position);
    enable_empty_positions();
}

function bind_and_enable_game_over_buttons()
{
    $("#same-players-same-pieces")
    .unbind("click")
    .bind("click", function()
    {
        common_button_actions(play_game);
    })
    .removeAttr("disabled");

    $("#same-players-diff-pieces")
    .unbind("click")
    .bind("click", function()
    {
        common_button_actions(swap_players);
    })
    .removeAttr("disabled");

    $("#diff-players")
    .unbind("click")
    .bind("click", function()
    {
        common_button_actions(select_players);
    })
    .removeAttr("disabled");
}

function unbind_and_disable_game_over_buttons()
{
    $("#same-players-same-pieces").unbind("click").attr("disabled", "disabled");
    $("#same-players-diff-pieces").unbind("click").attr("disabled", "disabled");
    $("#diff-players").unbind("click").attr("disabled", "disabled");
}

function common_button_actions(play_function)
{
    unbind_and_disable_game_over_buttons();
    play_function();
}

function swap_players()
{
    var temp = $("#x").val();
    $("#x").val($("#o").val());
    $("#o").val(temp);
    play_game();
}

function select_players()
{
    show_select_players();
    enable_select_players();
    hide_game();
}
