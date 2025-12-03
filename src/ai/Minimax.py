# ai/minimax.py

from models.Board import Board
from .Heuristic import heuristic

INF = 10 ** 9
MAX_DEPTH = 2  # độ sâu L (bạn giải thích trong báo cáo)


def minimax(board: Board, depth: int, maximizing: bool, ai_color: int,
            alpha: float = -INF, beta: float = INF):
    if depth == 0:
        return heuristic(board, ai_color), None

    current_color = ai_color if maximizing else -ai_color
    legal = board.legal_moves(current_color)

    if not legal:
        return heuristic(board, ai_color), None

    best_move = None

    if maximizing:
        best_value = -INF
        for move in legal:
            nb = board.copy()
            if not nb.apply_move(move[0], move[1], current_color):
                continue
            val, _ = minimax(nb, depth - 1, False, ai_color, alpha, beta)
            if val > best_value:
                best_value = val
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value, best_move
    else:
        best_value = INF
        for move in legal:
            nb = board.copy()
            if not nb.apply_move(move[0], move[1], current_color):
                continue
            val, _ = minimax(nb, depth - 1, True, ai_color, alpha, beta)
            if val < best_value:
                best_value = val
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value, best_move


def choose_ai_move(board: Board, ai_color: int):
    # ====== THÊM ĐIỀU KIỆN PASS THÔNG MINH ======
    total_empty = sum(1 for i in range(9) for j in range(9) if board.grid[i][j] == 0)
    
    # Nếu còn ít hơn 12 ô trống → 99% là endgame → nên pass nếu đang dẫn trước
    if total_empty <= 12:
        current_heuristic = heuristic(board, ai_color)
        # Nếu AI đang dẫn trước ít nhất 8 điểm → pass luôn cho an toàn
        if current_heuristic > 8:
            return None  # PASS NGAY

    # Nếu bàn cờ gần đầy (còn <= 8 ô trống) → pass vô điều kiện
    if total_empty <= 8:
        return None  # PASS LUÔN

    # ====== BÌNH THƯỜNG: dùng Minimax ======
    _, move = minimax(board, MAX_DEPTH, True, ai_color)
    return move