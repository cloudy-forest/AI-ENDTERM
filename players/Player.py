# players/Player.py

from abc import ABC, abstractmethod
from models.GameState import GameState


class Player(ABC):
    def __init__(self, color: int, name: str = ""):
        self.color = color
        self.name = name or ("Black" if color == 1 else "White")

    @abstractmethod
    def choose_move(self, state: GameState, click_pos=None):
        """
        Với Human: dùng click_pos (tọa độ ô trên lưới).
        Với AI: bỏ qua click_pos, tự chọn.
        Trả về (row, col) hoặc None nếu không có nước.
        """
        pass
