# ai/heuristic.py

from models.Board import Board
from models.GameState import BOARD_SIZE, BLACK, WHITE


def heuristic(board: Board, ai_color: int) -> float:
    """
    H(state) = w1 * (số quân AI - số quân đối thủ)
             + w2 * (tổng số khí của nhóm AI - nhóm đối thủ)
             + w3 * (ưu tiên quân gần trung tâm)
    """

    size = board.size
    center = (size - 1) / 2.0

    ai_stones = 0
    opp_stones = 0
    ai_libs = 0
    opp_libs = 0
    center_score = 0.0

    seen_groups = set()

    for i in range(size):
        for j in range(size):
            v = board.grid[i][j]
            if v == 0:
                continue
            if (i, j) in seen_groups:
                continue

            group, libs = board.get_group_and_liberties(i, j)
            seen_groups |= group

            if v == ai_color:
                ai_stones += len(group)
                ai_libs += len(libs)
            else:
                opp_stones += len(group)
                opp_libs += len(libs)

    # điểm vị trí gần trung tâm
    for i in range(size):
        for j in range(size):
            v = board.grid[i][j]
            if v == ai_color:
                dist = abs(i - center) + abs(j - center)
                center_score += (size - dist)

    w1, w2, w3 = 10.0, 1.0, 0.5
    diff_stone = ai_stones - opp_stones
    diff_lib = ai_libs - opp_libs
    return w1 * diff_stone + w2 * diff_lib + w3 * center_score
