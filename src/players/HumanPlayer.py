# players/HumanPlayer.py

from typing import Optional, Tuple
from models.GameState import GameState
from .Player import Player


class HumanPlayer(Player):
    def choose_move(
        self, state: GameState, click_pos: Optional[Tuple[int, int]] = None
    ):
        return click_pos
