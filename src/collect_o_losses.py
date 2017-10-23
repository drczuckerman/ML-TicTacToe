import utils
from zipfile import ZipFile

with ZipFile(utils.get_path("data", "o_player_vs_random.zip")) as fzip:
    with fzip.open("o_player_vs_random.txt") as f: 
        lines = f.read().decode("ascii").splitlines()
        
state = 0
moves = []
losing_moves = []
for line in lines:
    if state == 0:
        if line.startswith("Game #"):
            state = 1
            moves = []
    elif state == 1:
        if line.startswith("My move is "):
            moves.append(int(line[len("My move is "):].strip()))
            if len(moves) > 9:
                break
        elif "Draw" in line:
            state = 0
        elif "Wins" in line:
            if line.startswith("X"):
                if moves not in losing_moves:
                    losing_moves.append(moves)
            state = 0

print("Losing moves:")
losing_moves.sort()
for moves in losing_moves:
    print("- {}".format(moves))

