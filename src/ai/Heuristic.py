# ai/Heuristic.py

from models.Board import Board
from models.GameState import BLACK, WHITE


def heuristic(board: Board, ai_color: int) -> float:
    """
    Heuristic mạnh cho Go 9x9 - đủ để AI chơi khá thông minh
    """
    # Nếu đã game over (tương lai sẽ xử lý), trả giá trị cực đại
    # if board.is_game_over(): ...

    # 1. Số quân
    ai_stones = board.count_stones(ai_color)
    opp_stones = board.count_stones(-ai_color)

    # 2. Tổng số khí
    ai_libs = board.count_total_liberties(ai_color)
    opp_libs = board.count_total_liberties(-ai_color)

    # 3. Số nhóm đang bị đe dọa (có <=2 liberties)
    ai_threatened = board.count_threatened_groups(ai_color)
    opp_threatened = board.count_threatened_groups(-ai_color)

    # 4. Ước lượng lãnh thổ (rất quan trọng cuối game)
    ai_territory, opp_territory = board.estimate_territory()

    # Trọng số (đã tinh chỉnh để AI chơi hợp lý)
    w_stone = 10.0
    w_lib = 1.3
    w_threat = 18.0        # cứu quân mình / ăn quân địch là ưu tiên cao
    w_territory = 11.0

    score = (
        w_stone * (ai_stones - opp_stones) +
        w_lib * (ai_libs - opp_libs) +
        w_threat * (opp_threatened - ai_threatened) +   # ưu tiên ăn quân địch hơn cứu mình
        w_territory * (ai_territory - opp_territory)
    )

    return score