from player import Player

class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self.set_interactive()
        self.move = None

    def get_move(self):
        if not self.interactive:
            return self.move

        while True:
            position = input("Enter move: ").strip()
            if not position.isdigit():
                print("Invalid input")
                continue
            
            position = int(position) - 1
            if not self.board.is_valid_move(position):
                print("Invalid move")
                continue

            return position

    def set_interactive(self):
        self.interactive = True

    def set_non_interactive(self):
        self.interactive = False

    def set_move(self, position):
        self.move = position - 1

def run_if_human(player, func):
    if isinstance(player, HumanPlayer):
        func()

