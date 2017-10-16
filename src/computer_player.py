from player import Player

class ComputerPlayer(Player):
    def indicate_move(self, position):
        return "My move is {}".format(position + 1)

def run_if_computer(player, func):
    if isinstance(player, ComputerPlayer):
        func()
