# models/Board.py

from collections import deque
from .GameState import BOARD_SIZE, EMPTY, BLACK, WHITE


class Board:
    def __init__(self, size: int = BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

    # ---------- tiện ích cơ bản ----------
    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def neighbors(self, x: int, y: int):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def copy(self) -> "Board":
        new_b = Board(self.size)
        new_b.grid = [row[:] for row in self.grid]
        return new_b

    # ---------- nhóm quân + khí ----------
    def get_group_and_liberties(self, x: int, y: int):
        """Trả về (set group, set liberties) của quân tại (x,y)."""
        color = self.grid[x][y]
        if color == EMPTY:
            return set(), set()

        visited = set()
        liberties = set()
        q = deque([(x, y)])
        visited.add((x, y))

        while q:
            cx, cy = q.popleft()
            for nx, ny in self.neighbors(cx, cy):
                v = self.grid[nx][ny]
                if v == EMPTY:
                    liberties.add((nx, ny))
                elif v == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))
        return visited, liberties

    def remove_group(self, group):
        for x, y in group:
            self.grid[x][y] = EMPTY

    # ---------- thực hiện nước đi ----------
    def is_empty(self, x: int, y: int) -> bool:
        return self.grid[x][y] == EMPTY

    def apply_move(self, x: int, y: int, color: int) -> bool:
        """
        Đặt quân (nếu ô trống) + bắt quân đối thủ nếu hết khí.
        Có kiểm tra luật tự sát: nếu sau khi đi, nhóm quân vừa đặt
        không còn khí thì nước đi không hợp lệ.
        Trả về True nếu nước đi hợp lệ.
        """
        if not self.in_bounds(x, y) or not self.is_empty(x, y):
            return False

        # đặt quân tạm
        self.grid[x][y] = color
        opponent = BLACK if color == WHITE else WHITE

        # kiểm tra các nhóm đối thủ xung quanh: nếu hết khí thì bị bắt
        to_remove = []
        for nx, ny in self.neighbors(x, y):
            if self.grid[nx][ny] == opponent:
                group, libs = self.get_group_and_liberties(nx, ny)
                if len(libs) == 0:
                    to_remove.extend(group)

        # xóa các nhóm bị bắt (nếu có)
        for gx, gy in to_remove:
            self.grid[gx][gy] = EMPTY

        # sau khi bắt xong, kiểm tra nhóm của chính quân vừa đặt
        group, libs = self.get_group_and_liberties(x, y)
        if len(libs) == 0:
            # nước tự sát → phải undo: bỏ quân vừa đặt và restore đối thủ
            self.grid[x][y] = EMPTY
            for gx, gy in to_remove:
                self.grid[gx][gy] = opponent
            return False

        return True


    def legal_moves(self, color: int):
        """Ở đây đơn giản: mọi ô trống đều là nước đi hợp lệ."""
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == EMPTY:
                    moves.append((i, j))
        return moves
    
    
    def count_stones(self):
        """Đếm số quân đen và trắng hiện có trên bàn."""
        black = 0
        white = 0
        for row in self.grid:
            for v in row:
                if v == BLACK:
                    black += 1
                elif v == WHITE:
                    white += 1
        return black, white

