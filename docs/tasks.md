
---

### `docs/tasks.md`

```markdown
# Go 9x9 Project – Task Breakdown

Assume a team of 2 members. The tasks can be split and then reviewed by both.

---

## Member A – Core Game Logic & AI

### 1. Board and Game Rules (models/)

- Implement `Board`:
  - grid representation,
  - `in_bounds`, `neighbors`,
  - `get_group_and_liberties`,
  - `remove_group`,
  - `apply_move` including:
    - capture rule,
    - suicide detection.
- Implement `count_stones` and `legal_moves`.
- Implement `GameState` with `current_player` and `switch_player`.

### 2. AI Module (ai/)

- Implement `heuristic(board, ai_color)`:
  - stone difference,
  - liberty difference,
  - center score,
  - choose appropriate weights and document them.
- Implement `minimax` with alpha–beta pruning:
  - depth limit,
  - maximizer / minimizer logic,
  - skipping illegal moves (when `apply_move` returns `False`).
- Implement `choose_ai_move(board, ai_color)` and test on small positions.

### 3. Unit Testing / Debugging

- Write small scripts or temporary prints to verify:
  - capturing logic,
  - suicide blocking,
  - heuristic behavior on simple boards,
  - AI does not crash or play illegal moves.

---

## Member B – UI, Controller & Documentation

### 4. Controller Layer (controllers/)

- Implement `GameController`:
  - manage `Board`, `GameState`, players, and mode (`HUMAN_VS_HUMAN` / `HUMAN_VS_AI`),
  - `setup_new_game` (reset board, captures, result),
  - `handle_click` (board clicks vs. button clicks),
  - `apply_move_and_update` (update captures and switch player),
  - `update` (trigger AI move when it is AI’s turn),
  - `draw` (delegate to `GameUI`),
  - `get_window_size`.

### 5. Player Classes (players/)

- Implement `Player` abstract class.
- Implement `HumanPlayer` (returns clicked coordinate).
- Implement `AIPlayer` (calls `choose_ai_move` from AI module).

### 6. UI Layer (ui/)

- Implement `Button` with:
  - rounded corners,
  - base / hover color,
  - centered text.
- Implement `GameUI`:
  - draw board grid, star points, stones,
  - draw ghost stone under mouse for current player,
  - draw right panel (title, turn, captured counts, mode text),
  - add buttons:
    - `New Game` (green),
    - `Pass` (blue),
    - `Resign` (red),
    - `Human vs Human`,
    - `Human vs AI`.
  - implement:
    - `get_window_size`,
    - `pixel_to_board`,
    - `hit_test_buttons`,
    - `draw(screen)`.

### 7. Entry Point & Integration

- Implement `main.py`:
  - initialize Pygame,
  - create `GameController`,
  - event loop, update, draw, quit.
- Coordinate with Member A to connect AI and Board logic.

---

## Both Members – Documentation & Report

### 8. Requirements Document (requirements.md)

- Summarize functional and non-functional requirements.
- Clearly state mode behavior, turn management, captures, and AI constraints.

### 9. Design Document (design.md)

- Describe architecture (layers and packages).
- Explain each main class and responsibility.
- Describe heuristic formula and the choice of depth limit.

### 10. Class Diagram (class_diagram.puml)

- Maintain the PlantUML diagram up-to-date with the actual code.
- Ensure all important relationships (composition, inheritance, utility) are shown.

### 11. Task Summary (tasks.md)

- Keep this file updated to reflect actual work distribution.
- Note who implemented which parts and any major design decisions.

---

This breakdown should be enough for both of you to coordinate, divide responsibilities, and present the project as a well-structured OOP + AI Go 9x9 implementation.
