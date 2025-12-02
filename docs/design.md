
---

### `docs/design.md`

```markdown
# Go 9x9 – Design Document

## 1. Overview

This project implements a simplified Go game on a 9x9 board where:
- two humans can play against each other, or
- a human can play against an AI using heuristic Minimax search.

The implementation is written in **Python + Pygame**, with a clear object-oriented structure divided into model, AI, controller, and UI layers.

---

## 2. Architecture

The overall architecture follows a lightweight MVC/MVP style:

- **Model (`models/`)**
  - `Board` – represents the Go board and implements the rules.
  - `GameState` – represents who is to move and holds a reference to `Board`.

- **Players (`players/`)**
  - `Player` (abstract) – common interface for all players.
  - `HumanPlayer` – obtains moves from mouse clicks.
  - `AIPlayer` – obtains moves by running the Minimax search.

- **AI (`ai/`)**
  - `heuristic` – evaluation function for a board state.
  - `minimax` – depth-limited Minimax with alpha–beta pruning.

- **Controller (`controllers/`)**
  - `GameController` – central coordinator of the game:
    - manages game mode (Human vs Human / Human vs AI),
    - handles turns, applying moves, captures, passes, resigns,
    - updates state and interacts with the UI.

- **UI (`ui/`)**
  - `Button` – reusable clickable button with hover effect.
  - `GameUI` – draws the board, control panel, and handles mapping mouse positions to board coordinates and button hits.

- **Entry Point**
  - `main.py` – initializes Pygame, creates `GameController`, and runs the main loop (event handling, update, render).

---

## 3. Model Layer

### 3.1 Board Representation

`Board` stores the current layout of stones:

- Size: `size = 9`
- Grid: `grid[size][size]`, with:
  - `0` = empty,
  - `1` = black stone,
  - `-1` = white stone.

Key methods:

- `in_bounds(x, y)` – check if a coordinate is on the board.
- `neighbors(x, y)` – yield orthogonal neighbors (up, down, left, right).
- `get_group_and_liberties(x, y)` – BFS to find a connected group of same-color stones and its liberties (empty adjacent points).
- `remove_group(group)` – remove all stones in a group from the board.
- `apply_move(x, y, color)` – place a stone, handle captures, and check suicide.
- `legal_moves(color)` – list of candidate intersections (simple version: all empty points).
- `count_stones()` – return `(black_count, white_count)`.

#### Move Application & Suicide Rule

`apply_move` enforces the basic Go rules:

1. Rejects moves on non-empty intersections.
2. Tentatively places the stone.
3. For each neighboring opponent group:
   - computes its liberties,
   - if liberties are zero, removes that group (capture).
4. Computes the liberties of the placed stone’s group:
   - If liberties are zero, this is a **suicide move**:
     - the move is undone,
     - captured stones (if any) are restored,
     - returns `False` (illegal).
5. Otherwise, the move is accepted and returns `True`.

This ensures both human and AI cannot play suicide moves.

---

### 3.2 GameState

`GameState` encapsulates:

- `board: Board`
- `current_player: int` (`1` for Black, `-1` for White)

Methods:

- `switch_player()` – toggles `current_player` between Black and White.

`GameState` separates the notion of “whose turn it is” from the static board.

---

## 4. Players and Game Modes

### 4.1 Abstract Player

`Player` defines:

```python
class Player(ABC):
    def __init__(self, color: int, name: str = ""):
        self.color = color
        self.name = name

    @abstractmethod
    def choose_move(self, state: GameState, click_pos=None):
        """Return (row, col) for the move, or None."""
        pass
