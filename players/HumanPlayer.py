# players/HumanPlayer.py

from typing import Optional, Tuple
from models.GameState import GameState
from .Player import Player


class HumanPlayer(Player):
    def choose_move(
        self, state: GameState, click_pos: Optional[Tuple[int, int]] = None
    ):
        # click_pos đã là (row, col) trong lưới, do GameController chuyển
        return click_pos
