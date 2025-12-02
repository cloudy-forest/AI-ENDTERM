from dataclasses import dataclass

BOARD_SIZE = 9
EMPTY = 0
BLACK = 1
WHITE = -1

@dataclass
class GameState:
    # Lưu trữ trạng thái tổng quát của ván cờ :
    # - board: Đối tượng Board (import lazy -> tránh vòng lặp import)
    # - current_player: BLACK hoặc WHITE
    
    board: "Board" # type: ignore  # sẽ import ở nơi khác
    current_player: int = BLACK
    def switch_player(self):
        self.current_player = BLACK if self.current_player == WHITE else WHITE
        