import uuid
import threading
import time
from web_game import WebGame

class WebGameManager(object):
    EXPIRE_TIME = 5*60 # 5 minutes

    def __init__(self):
        self.web_game_dict = {}
        self.lock = threading.Lock()

    def new_game(self):
        with self.lock:
            game_id = self._get_game_id()
            game = WebGame()
            self.web_game_dict[game_id] = {"game": game, "time": time.time()}
            return game_id, game

    def _get_game_id(self):
            while True:
                game_id = str(uuid.uuid4())
                if game_id not in self.web_game_dict:
                    return game_id
    
    def get_game(self, game_id):
        with self.lock:
            return self.web_game_dict.get(game_id, {}).get("game")

    def delete_game(self, game_id):
        with self.lock:
            if game_id in self.web_game_dict:
                del self.web_game_dict[game_id]
                return True
        return False

    def refresh_game(self, game_id):
        with self.lock:
            if game_id in self.web_game_dict:
                self.web_game_dict[game_id]["time"] = time.time()
                return True
        return False

    def expire_games(self):
        with self.lock:
            for game_id in self._get_expired_game_ids():
                del self.web_game_dict[game_id]

    def _get_expired_game_ids(self):
        expired_game_ids = []
        current_time = time.time()
        for game_id, game_info in self.web_game_dict.items():
            elapsed_time = current_time - game_info["time"]
            if elapsed_time >= self.EXPIRE_TIME:
                expired_game_ids.append(game_id)
        return expired_game_ids
    
def start_web_game_manager_thread(web_game_manager):
    def run():
        while True:
            time.sleep(60)
            web_game_manager.expire_games()

    t = threading.Thread(target=run, daemon=True)
    t.start()
