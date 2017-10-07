Computer Player
===============

Params
------
alpha = learning rate
epsilon = exploration rate
draw reward

Defaults
--------
alpha = 0.5
epsilon = 0.1
draw reward = 0.5 for X, 0.5 for O

Notes
-----
if state not found in V:
    if end state:
        V(state) = reward
    else:
        V(state) = 0.5
Init
----
V = empty
states = empty

Get move
--------
Output: move

if random < epsilon:
    best moves = available moves
else:
    Vmax = -1
    best moves = empty
    foreach available move:
        update board with this move
        if V(state) > Vmax:
            Vmax = V(state)
            set best moves to this move
        else if V(state) == Vmax:
            add this move to best moves
        undo this move
    
pick random move based on best moves

Remember state
--------------
Store current board state

Get reward
----------
Input: winner
Output: reward

if winner is me:
    reward = 1
else if winner is other:
    reward = 0
else
    reward = draw reward

Set reward
----------
Input: winner

last state value = get reward(winner)
foreach stored state in reverse order:
    V(state) += alpha * [last value - V(state)]
    last value = V(state)
