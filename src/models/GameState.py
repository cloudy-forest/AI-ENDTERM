# models/GameState.py

from dataclasses import dataclass

BOARD_SIZE = 9
EMPTY = 0
BLACK = 1
WHITE = -1

@dataclass
class GameState:
    board: "Board"
    current_player: int = BLACK
    consecutive_passes: int = 0   # THÊM DÒNG NÀY

    def switch_player(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE

    def pass_move(self):
        self.consecutive_passes += 1
        self.switch_player()

    def place_stone(self):
        self.consecutive_passes = 0  # đặt quân thì reset đếm pass

    def is_game_over(self) -> bool:
        return self.consecutive_passes >= 2