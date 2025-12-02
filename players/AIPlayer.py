# players/AIPlayer.py

from typing import Optional, Tuple
from models.GameState import GameState
from .Player import Player
from ai.Minimax import choose_ai_move


class AIPlayer(Player):
    def choose_move(
        self, state: GameState, click_pos: Optional[Tuple[int, int]] = None
    ):
        # click_pos không dùng
        return choose_ai_move(state.board, self.color)
