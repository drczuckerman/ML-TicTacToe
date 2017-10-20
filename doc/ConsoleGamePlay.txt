Console Game Play
=================
Select Players
while True:
    Play One Game
    ask action:
    - quit
    - same players and pieces
    - same players and diff pieces
    - diff players
    if diff player, Select Players
    elseif same players and diff pieces, Swap Players
    elseif quit, break

Select Players
--------------
select X player (human or some type of computer player)
select O player (human or some type of computer player)
load learning computer players

Play One Game
-------------
current player = X
reset board
reset players
while winner is none:
    indicate current player
    show board
    get move from current player
    announce move
    update board with move
    switch current player to opposite piece
show board
display winner

Swap Players
------------
Swap X and O player
load learning computer players with opposite pieces

