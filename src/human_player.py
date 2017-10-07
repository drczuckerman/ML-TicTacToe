from player import Player

class HumanPlayer(Player):
    def get_move(self):
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
