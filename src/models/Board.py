# models/Board.py

from collections import deque
from typing import Set, Tuple, List
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
    def get_group_and_liberties(self, x: int, y: int) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
        color = self.grid[x][y]
        if color == EMPTY:
            return set(), set()

        visited = set()
        liberties = set()
        queue = deque([(x, y)])
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()
            for nx, ny in self.neighbors(cx, cy):
                if self.grid[nx][ny] == EMPTY:
                    liberties.add((nx, ny))
                elif self.grid[nx][ny] == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return visited, liberties

    def remove_group(self, group: Set[Tuple[int, int]]):
        for x, y in group:
            self.grid[x][y] = EMPTY

    # ---------- thực hiện nước đi ----------
    def is_empty(self, x: int, y: int) -> bool:
        return self.grid[x][y] == EMPTY

    def apply_move(self, x: int, y: int, color: int) -> bool:
        if not self.in_bounds(x, y) or not self.is_empty(x, y):
            return False

        # Đặt quân tạm
        self.grid[x][y] = color
        opponent = -color  # BLACK = -1, WHITE = 1 → -color là đối thủ

        captured_groups = []

        # Kiểm tra các nhóm đối thủ xung quanh
        for nx, ny in self.neighbors(x, y):
            if self.grid[nx][ny] == opponent:
                group, libs = self.get_group_and_liberties(nx, ny)
                if len(libs) == 0 and group not in captured_groups:
                    captured_groups.append(group)

        # Bắt quân đối thủ
        for group in captured_groups:
            self.remove_group(group)

        # Kiểm tra tự sát
        my_group, my_libs = self.get_group_and_liberties(x, y)
        if len(my_libs) == 0 and not captured_groups:  # chỉ tự sát nếu không bắt được quân nào
            # Undo: bỏ quân vừa đặt và phục hồi nhóm bị bắt (nếu có)
            self.grid[x][y] = EMPTY
            for group in captured_groups:
                for gx, gy in group:
                    self.grid[gx][gy] = opponent
            return False

        return True

    # ---------- danh sách nước hợp lệ ----------
    def legal_moves(self, color: int) -> List[Tuple[int, int]]:
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == EMPTY:
                    # Tạo bản sao tạm để thử đặt
                    temp = self.copy()
                    if temp.apply_move(i, j, color):
                        moves.append((i, j))
        return moves

    # ---------- đếm quân ----------
    def count_stones(self, color: int = None) -> int | Tuple[int, int]:
        black = white = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == BLACK:
                    black += 1
                elif self.grid[i][j] == WHITE:
                    white += 1
        if color == BLACK:
            return black
        if color == WHITE:
            return white
        return black, white

    # ---------- tổng số khí ----------
    def count_total_liberties(self, color: int) -> int:
        total = 0
        seen = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == color and (i, j) not in seen:
                    group, liberties = self.get_group_and_liberties(i, j)
                    seen.update(group)
                    total += len(liberties)
        return total

    # ---------- ước lượng lãnh thổ ----------
    def estimate_territory(self) -> Tuple[int, int]:
        visited = [[False] * self.size for _ in range(self.size)]
        black_terr = white_terr = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def flood_fill(r: int, c: int) -> Tuple[set, int]:
            if visited[r][c] or self.grid[r][c] != EMPTY:
                return set(), 0
            queue = [(r, c)]
            visited[r][c] = True
            area = 0
            borders = set()

            while queue:
                x, y = queue.pop(0)
                area += 1
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        cell = self.grid[nx][ny]
                        if cell != EMPTY:
                            borders.add(cell)
                        elif not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
            return borders, area

        for i in range(self.size):
            for j in range(self.size):
                if not visited[i][j] and self.grid[i][j] == EMPTY:
                    borders, size = flood_fill(i, j)
                    if len(borders) == 1:
                        owner = next(iter(borders))
                        if owner == BLACK:
                            black_terr += size
                        elif owner == WHITE:
                            white_terr += size
        return black_terr, white_terr
    
    def count_threatened_groups(self, color: int) -> int:
        """
        Đếm số nhóm của color có <= 2 liberties (dễ bị ăn = atari hoặc gần chết)
        Rất quan trọng để AI biết cứu quân hoặc tấn công!
        """
        threatened = 0
        seen = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == color and (i, j) not in seen:
                    group, liberties = self.get_group_and_liberties(i, j)
                    seen.update(group)
                    if len(liberties) <= 2:  # <= 2 là nguy hiểm
                        threatened += 1
        return threatened

    # ---------- tạm thời để heuristic không crash ----------
    def is_game_over(self) -> bool:
        return False  # Sẽ xử lý sau khi thêm pass liên tiếp trong GameState