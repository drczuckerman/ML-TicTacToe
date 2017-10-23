Web Game Play
=============

Back End
--------

GET / (Select Players)
~~~~~~~~~~~~~~~~~~~~~~
return page to select player types

POST /play (Play Game)
~~~~~~~~~~~~~~~~~~~~~~
Input: {'x': x player type, 'o': o player type}

create new game giving game id
initialize game and players for specified player types
load computer players
return page containing empty board with all squares disabled and game id

POST /computer_move
~~~~~~~~~~~~~~~~~~
Input: {'game_id': game id}

get game with game_id
if not found, return page indicating game expired

freshen game with game_id
make computer move
go to next player
if game over, delete game with game_id
return page portion containing board update

POST /human_move
~~~~~~~~~~~~~~~~
Input: {'game_id', game id, 'move': square number}

get game with game_id
if not found, return page indicating game expired

freshen game with game_id
make human move given square number
go to next player
if game over, delete game with game_id
return page portion containing board update

Front End
---------

Select Players
~~~~~~~~~~~~~~

On Click "Play" button
......................
disable "Play" button
POST /play {'x': x player type, 'o': o player type}

Play Game
~~~~~~~~~
Input: {'x': x player type, 'o': o player type, 'game_id': game id}

save player types and game id
display board
if X player is human, enable empty squares
else:
    indicate waiting
    GET /computer_move

On POST /computer_move Completion or POST /human_move Completion
................................................................
update board
indicate not waiting
if game not over:
    if current player is human, enable empty squares
    else:
        pause small amount of time
        indicate waiting
        GET /computer_move

On Click Empty Square
.....................
disable empty squares
update board with move
indicate waiting
POST /human_move {'move': square number, 'game_id': game id}

On Click "Same Players, Same Pieces" Button
...........................................
do Common Button Actions
POST /play {'x': x player type, 'o': o player type}

On Click "Same Players, Different Pieces" Button
................................................
do Common Button Actions
POST /play {'x': o player type', 'o': x player type}

On click "Diff Players" Button
..............................
do Common Button Actions
GET /

Common Button Actions
.....................
disable buttons
indicate waiting
